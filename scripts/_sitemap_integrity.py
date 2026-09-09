#!/usr/bin/env python3
"""Sitemap vs canonical vs robots. Prints defects, exits 1 if any."""
import os, re, subprocess, sys

ROOT = sys.argv[1] if len(sys.argv) > 1 else "."
BASE = "https://acglass.com/"
sm = open(os.path.join(ROOT, "sitemap.xml"), encoding="utf-8").read()
sitemap = {u.rstrip("/") for u in re.findall(r"<loc>([^<]+)</loc>", sm)}

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
    if u not in sitemap and not noidx and canon == u:
        print(f"  C {p}: self-canonical and indexable, but absent from the sitemap"); C += 1

n = A + B + C
if n == 0:
    print(f"PASS    sitemap-integrity ({len(sitemap)} URLs agree with canonicals and robots)")
    sys.exit(0)
print(f"FAIL    sitemap-integrity: {A} canonical conflicts, {B} noindex conflicts, {C} missing")
sys.exit(1)
