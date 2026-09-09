#!/usr/bin/env python3
"""Sitemap vs canonical vs robots. Prints defects, exits 1 if any."""
import glob, os, re, subprocess, sys

ROOT = sys.argv[1] if len(sys.argv) > 1 else "."
BASE = "https://acglass.com/"
# Every sitemap, not just the apex. There are nine files and an index, and an
# earlier version of this check read sitemap.xml alone. It passed while four
# child sitemaps still carried URLs that had been removed from the site.
sitemap = set()
for f in glob.glob(os.path.join(ROOT, "sitemap*.xml")):
    sitemap |= {u.rstrip("/") for u in
                re.findall(r"<loc>([^<]+)</loc>", open(f, encoding="utf-8").read())}

# URLs deliberately retired from every sitemap by an earlier workstream, listed in
# .github/scripts/crawl-check.py. This check once reported them as "missing" and I
# added them back. A deliberate exclusion is not a defect.
RETIRED = set()
cc = os.path.join(ROOT, ".github/scripts/crawl-check.py")
if os.path.isfile(cc):
    m = re.search(r"RETIRED_SITEMAP_URLS\s*=\s*\((.*?)\)", open(cc).read(), re.S)
    if m:
        RETIRED = {u.rstrip("/") for u in re.findall(r'"([^"]+)"', m.group(1))}

pages = [p for p in subprocess.run(["git", "-C", ROOT, "ls-files", "*.html"],
         capture_output=True, text=True).stdout.split() if not p.startswith(".github/")]
CANON = re.compile(r'<link[^>]+rel=["\']?canonical["\']?[^>]*href=["\']([^"\']+)', re.I)
NOIDX = re.compile(r'name=["\']robots["\'][^>]*content=["\'][^"\']*noindex', re.I)
STUB = re.compile(r'http-equiv=["\']?refresh', re.I)

A = B = C = 0
for p in pages:
    d = open(os.path.join(ROOT, p), encoding="utf-8", errors="replace").read()
    if STUB.search(d):
        continue
    u = (BASE + (p[:-len("index.html")] if p.endswith("index.html") else p)).rstrip("/")
    m = CANON.search(d)
    canon = m.group(1).rstrip("/") if m else ""
    noidx = bool(NOIDX.search(d))
    if u in sitemap and canon and canon != u:
        print(f"  A {p}: sitemapped, but canonical points to {canon}"); A += 1
    if u in sitemap and noidx:
        print(f"  B {p}: sitemapped, but the page is noindex"); B += 1
    if u not in sitemap and not noidx and canon == u and u not in RETIRED:
        print(f"  C {p}: self-canonical and indexable, but absent from the sitemap"); C += 1

n = A + B + C
if n == 0:
    print(f"PASS    sitemap-integrity ({len(sitemap)} URLs agree with canonicals and robots)")
    sys.exit(0)
print(f"FAIL    sitemap-integrity: {A} canonical conflicts, {B} noindex conflicts, {C} missing")
sys.exit(1)
