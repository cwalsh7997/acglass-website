#!/usr/bin/env python3
"""indexnow-ping.py - tell IndexNow engines which sitemap pages a deploy changed.

Run by .github/workflows/indexnow.yml after GitHub Pages has published the
pushed commit. Only changed .html files whose URL is listed in a sitemap are
submitted, so noindex pages, redirect stubs and internal files never go out.
IndexNow shares each submission with Bing, Yandex, Naver, Seznam and the other
participating engines. The key file (.indexnow-key and /<key>.txt) was added
in e83a8978b; this script is the part that was missing.

Usage:
  python3 .github/scripts/indexnow-ping.py --before SHA --after SHA [--dry-run]
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

HOST = "acglass.com"
ORIGIN = f"https://{HOST}"
ENDPOINT = "https://api.indexnow.org/indexnow"
SITEMAP_NS = "{http://www.sitemaps.org/schemas/sitemap/0.9}"
IGNORED_PREFIXES = ("_internal/", ".github/", "drafts/", "node_modules/")
MAX_URLS = 10000  # IndexNow protocol limit per request
REPO_ROOT = Path(__file__).resolve().parents[2]


def path_to_url(path: str) -> str | None:
    if not path.endswith(".html") or path.startswith(IGNORED_PREFIXES):
        return None
    if path == "index.html":
        return f"{ORIGIN}/"
    if path.endswith("/index.html"):
        return f"{ORIGIN}/{path[: -len('index.html')]}"
    return f"{ORIGIN}/{path}"


def sitemap_urls(root: Path) -> set[str]:
    urls: set[str] = set()
    for sitemap in sorted(Path(root).glob("sitemap*.xml")):
        try:
            tree = ET.parse(sitemap)
        except ET.ParseError:
            continue
        if tree.getroot().tag != f"{SITEMAP_NS}urlset":
            continue  # sitemap index files list sitemaps, not pages
        for loc in tree.getroot().iter(f"{SITEMAP_NS}loc"):
            if loc.text:
                urls.add(loc.text.strip())
    return urls


def select_urls(changed: list[str], listed: set[str], cap: int = MAX_URLS) -> list[str]:
    selected: list[str] = []
    for path in changed:
        url = path_to_url(path)
        if url and url in listed and url not in selected:
            selected.append(url)
    return selected[:cap]


def build_payload(urls: list[str], key: str) -> dict:
    return {
        "host": HOST,
        "key": key,
        "keyLocation": f"{ORIGIN}/{key}.txt",
        "urlList": urls,
    }


def changed_files(before: str, after: str) -> list[str]:
    if not before or set(before) == {"0"}:
        before = f"{after}^"
    out = subprocess.run(
        ["git", "diff", "--name-only", "--diff-filter=AMR", before, after],
        cwd=REPO_ROOT, capture_output=True, text=True, check=True,
    ).stdout
    return [line.strip() for line in out.splitlines() if line.strip()]


def submit(payload: dict) -> tuple[int, str]:
    req = urllib.request.Request(
        ENDPOINT,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json; charset=utf-8"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return resp.status, resp.read().decode("utf-8", "replace")[:300]
    except urllib.error.HTTPError as exc:
        return exc.code, exc.read().decode("utf-8", "replace")[:300]


def main() -> int:
    parser = argparse.ArgumentParser(description="Submit changed sitemap pages to IndexNow.")
    parser.add_argument("--before", default="")
    parser.add_argument("--after", default="HEAD")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    key = (REPO_ROOT / ".indexnow-key").read_text().strip()
    urls = select_urls(changed_files(args.before, args.after), sitemap_urls(REPO_ROOT))
    print(f"IndexNow: {len(urls)} changed sitemap URL(s)")
    for url in urls[:50]:
        print(f"  {url}")
    if not urls or args.dry_run:
        return 0
    status, body = submit(build_payload(urls, key))
    print(f"IndexNow response: HTTP {status} {body}".rstrip())
    if status not in (200, 202):
        # Best effort: a refused ping must not block or fail a deploy.
        print("::warning::IndexNow submission was not accepted")
    return 0


if __name__ == "__main__":
    sys.exit(main())
