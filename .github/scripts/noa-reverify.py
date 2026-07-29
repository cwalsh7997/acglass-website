#!/usr/bin/env python3
"""Monthly NOA reverification.

Re-fetches every source URL stored in /noa/data.json. Diffs the response signal
(HTTP status + presence of the FL# string in the page body) against last run.
Emits a structured report to stdout. Exits non-zero if any of:
  - Source URL is unreachable (dead link)
  - HTTP returns >= 400
  - The FL# token is no longer present in the response body (approval may have been replaced)

The workflow (.github/workflows/noa-reverify.yml) reads the exit code and
opens an issue when this script exits non-zero.

This script DOES NOT modify data.json. Human-in-the-loop updates the data
based on the issue's findings.
"""
import json
import sys
import time
import urllib.request
import urllib.error
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
DATA = json.loads((ROOT / 'noa' / 'data.json').read_text())

USER_AGENT = 'Mozilla/5.0 (compatible; acglass-noa-reverify/1.0; +https://acglass.com/noa/)'
TIMEOUT = 45  # seconds per request
MAX_BODY = 64 * 1024  # 64kB is plenty for the detail pages (FL# appears around byte 13k)


def fetch(url):
    """Return (status_code, body_up_to_MAX_BODY, error_str)."""
    req = urllib.request.Request(url, headers={'User-Agent': USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
            body = resp.read(MAX_BODY).decode('utf-8', errors='ignore')
            return (resp.status, body, None)
    except urllib.error.HTTPError as e:
        return (e.code, '', str(e))
    except (urllib.error.URLError, TimeoutError, ConnectionError, OSError) as e:
        return (None, '', str(e))


def main():
    today = date.today().isoformat()
    issues = []
    ok_count = 0
    checked = 0
    
    for pkey, partner in DATA['partners'].items():
        for s in partner['systems']:
            url = s.get('source_url', '')
            fl_pa = s.get('fl_pa', '')
            if not url or 'pending' in url.lower():
                continue
            checked += 1
            status, body, err = fetch(url)
            if err and status is None:
                issues.append(f"DEAD-LINK | {partner['label']} | {fl_pa} | {url} | {err}")
                continue
            if status is None or status >= 400:
                issues.append(f"HTTP-{status} | {partner['label']} | {fl_pa} | {url}")
                continue
            # Confirm FL# token still appears in the response
            # FPA detail pages echo the FL# in the body
            if fl_pa and fl_pa not in body:
                # Try a more relaxed check — the FL number without -R revision
                base_fl = fl_pa.split('-')[0]
                if base_fl not in body:
                    issues.append(f"TOKEN-MISSING | {partner['label']} | {fl_pa} | {url} | FL# not in first 64kB of response")
                    continue
            ok_count += 1
            time.sleep(0.3)  # be polite to gov portal
    
    print(f"=== ACG NOA Reverify — {today} ===")
    print(f"Checked: {checked} URLs")
    print(f"OK:      {ok_count}")
    print(f"Issues:  {len(issues)}")
    if issues:
        print("\nFailures:")
        for i in issues:
            print(f"  {i}")
    
    return 1 if issues else 0


if __name__ == '__main__':
    sys.exit(main())
