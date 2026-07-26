#!/usr/bin/env python3
"""scripts/leadtime-ingest.py — Monthly PO-to-delivery lead-time ingestion.

Reads /data/po-export.csv (owner drops it monthly). Computes per-manufacturer
PO-to-delivery range (min/median/max business days) — ranges ONLY, never a
single PO's data — and rewrites /resources/lead-times.html with the updated
table. The accompanying GitHub Actions workflow opens a PR for owner review;
auto-merge is intentionally NOT enabled.

CSV expected columns (case-insensitive, header row required):
  Manufacturer, PO Date, Delivery Date
Additional columns are ignored.

Manufacturers with fewer than 5 POs in the trailing 6 months are aggregated
into 'Other' (no single-order lead time exposed).

Required: nothing — the workflow runs only after the owner pushes the CSV
to /data/po-export.csv, so missing-file behavior exits cleanly with status 0
and a 'no CSV yet' message.
"""
import csv
import sys
from collections import defaultdict
from datetime import date, datetime, timedelta
from pathlib import Path

# This script lives at .github/scripts/ (not served by GitHub Pages), so the
# repo root is three levels up, not two.
ROOT = Path(__file__).resolve().parent.parent.parent
CSV_PATH = ROOT / 'data' / 'po-export.csv'
RESOURCES_DIR = ROOT / 'resources'
OUT_PATH = RESOURCES_DIR / 'lead-times.html'

WINDOW_DAYS = 183  # ~6 months
MIN_POS_FOR_NAMED = 5


def parse_date(s):
    """Try common date formats."""
    for fmt in ('%Y-%m-%d', '%m/%d/%Y', '%m-%d-%Y', '%Y/%m/%d', '%d-%b-%y', '%m/%d/%y'):
        try:
            return datetime.strptime(s.strip(), fmt).date()
        except ValueError:
            continue
    return None


def business_days(a, b):
    """Crude business-day diff: total days minus 2*weeks (no holiday calendar)."""
    days = (b - a).days
    if days < 0:
        return None
    weeks = days // 7
    return days - 2 * weeks


def stats(values):
    if not values:
        return None
    vs = sorted(values)
    return {
        'n': len(vs),
        'min': vs[0],
        'median': vs[len(vs) // 2],
        'max': vs[-1],
    }


def ingest():
    if not CSV_PATH.exists():
        print(f"No CSV at {CSV_PATH}. Owner needs to drop the monthly PO export.")
        return None
    today = date.today()
    cutoff = today - timedelta(days=WINDOW_DAYS)
    
    per_mfr = defaultdict(list)
    skipped = 0
    parsed = 0
    
    with CSV_PATH.open(newline='') as f:
        reader = csv.DictReader(f)
        # Normalize headers
        cols = {h.lower().strip(): h for h in reader.fieldnames or []}
        if 'manufacturer' not in cols or 'po date' not in cols or 'delivery date' not in cols:
            print("::error::CSV must have columns: Manufacturer, PO Date, Delivery Date", file=sys.stderr)
            sys.exit(1)
        f.seek(0); next(f)  # skip header
        reader = csv.DictReader(f, fieldnames=reader.fieldnames)
        for row in reader:
            mfr = (row.get(cols['manufacturer']) or '').strip()
            pd = parse_date(row.get(cols['po date']) or '')
            dd = parse_date(row.get(cols['delivery date']) or '')
            if not mfr or not pd or not dd:
                skipped += 1
                continue
            if pd < cutoff:
                continue
            bd = business_days(pd, dd)
            if bd is None:
                skipped += 1
                continue
            per_mfr[mfr].append(bd)
            parsed += 1
    
    print(f"Parsed: {parsed} POs from last {WINDOW_DAYS} days. Skipped: {skipped}.")
    
    # Roll up small manufacturers into 'Other'
    out = {}
    other_vals = []
    for mfr, vals in per_mfr.items():
        if len(vals) >= MIN_POS_FOR_NAMED:
            out[mfr] = stats(vals)
        else:
            other_vals.extend(vals)
    if other_vals:
        out['Other (aggregated <5 PO sample)'] = stats(other_vals)
    
    return {'window': (cutoff.isoformat(), today.isoformat()), 'per_mfr': out, 'parsed': parsed, 'skipped': skipped}


def render(data):
    today = date.today().isoformat()
    if not data:
        body_rows = '<tr><td colspan="5" style="text-align:center;color:rgba(255,255,255,0.5);padding:32px;">No PO export available yet. The lead-time table is refreshed monthly after the owner drops a PO export to /data/po-export.csv.</td></tr>'
        meta_line = "<em>No data yet. Awaiting first PO export.</em>"
    else:
        rows = []
        for mfr, st in sorted(data['per_mfr'].items()):
            if st is None: continue
            rows.append(f'        <tr><td>{mfr}</td><td>{st["n"]}</td><td>{st["min"]}</td><td>{st["median"]}</td><td>{st["max"]}</td></tr>')
        body_rows = '\n'.join(rows)
        meta_line = f"<em>Window: {data['window'][0]} → {data['window'][1]}. Parsed {data['parsed']} POs; {data['skipped']} skipped (missing or unparseable dates).</em>"
    
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Manufacturer Lead Times | ACG</title>
  <meta name="description" content="ACG manufacturer PO-to-delivery lead-time ranges, refreshed monthly from real purchase-order data. Ranges only — no single-order data exposed.">
  <link rel="canonical" href="https://acglass.com/resources/lead-times.html">
  <meta name="robots" content="index,follow">
  <style>
    body{{font-family:'Inter',system-ui,sans-serif;background:#0a1628;color:#fff;margin:0;padding:48px 24px;line-height:1.65;}}
    .wrap{{max-width:880px;margin:0 auto;}}
    h1{{font-size:2rem;margin:0 0 8px;}}
    table{{width:100%;border-collapse:collapse;margin:24px 0;font-size:14px;}}
    th{{text-align:left;padding:12px;border-bottom:2px solid #e11320;color:#e11320;font-size:11px;letter-spacing:0.08em;text-transform:uppercase;}}
    td{{padding:12px;border-bottom:1px solid rgba(255,255,255,0.08);}}
    .note{{background:rgba(255,255,255,0.04);border-left:3px solid #e11320;padding:16px 20px;border-radius:4px;margin:24px 0;font-size:14px;}}
  </style>
</head>
<body>
  <div class="wrap">
    <h1>Manufacturer Lead Times</h1>
    <p style="color:rgba(255,255,255,0.7);">Rolling window of PO-to-delivery business days, by manufacturer, from ACG's purchase-order data. Refreshed monthly.</p>
    <p style="font-size:13px;color:rgba(255,255,255,0.6);">{meta_line}</p>
    
    <div class="note">
      <strong>Ranges only.</strong> ACG does not publish single-order lead times. Manufacturers with fewer than 5 POs in the window are aggregated into &lsquo;Other&rsquo; to prevent single-order inference. Use these as a planning reference; ACG quotes project-specific lead time in writing on every bid from the most recent factory acknowledgement &mdash; not from this published average.
    </div>
    
    <table>
      <thead>
        <tr><th>Manufacturer</th><th>POs</th><th>Min (business days)</th><th>Median</th><th>Max</th></tr>
      </thead>
      <tbody>
{body_rows}
      </tbody>
    </table>
    
    <p style="font-size:13px;color:rgba(255,255,255,0.55);margin-top:32px;">Generated by scripts/leadtime-ingest.py on {today}. Source: /data/po-export.csv (not published).</p>
  </div>
</body>
</html>
'''


def main():
    RESOURCES_DIR.mkdir(parents=True, exist_ok=True)
    data = ingest()
    if data is None and not OUT_PATH.exists():
        # No CSV yet AND no existing page — write the placeholder
        OUT_PATH.write_text(render(None))
        print(f"Wrote placeholder: {OUT_PATH}")
        return 0
    if data is None:
        # No CSV yet, but page exists — leave it alone
        print("No CSV; leaving existing page untouched.")
        return 0
    OUT_PATH.write_text(render(data))
    print(f"Wrote: {OUT_PATH}")
    return 0


if __name__ == '__main__':
    sys.exit(main())
