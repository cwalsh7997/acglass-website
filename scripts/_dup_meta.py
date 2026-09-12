#!/usr/bin/env python3
"""No two indexable pages may share a title or a meta description.

Two pages with the same title compete for the same query and split the signal
between them. Redirect stubs and noindexed pages are excluded because neither
competes for anything.

A shared title is NOT a defect when both pages canonical to the SAME url: Google
consolidates them into one page, which is the whole point of a canonical. Four of
the five duplicate pairs here are exactly that, correctly consolidated city pages,
and flagging them would have meant "fixing" work that was already right.
"""
import collections, os, re, sys

ROOT = sys.argv[1] if len(sys.argv) > 1 else "."
sys.path.insert(0, os.path.join(ROOT, "scripts"))
from sweep_files import sweep_files

STUB = re.compile(r'http-equiv=["\']?refresh', re.I)
NOIDX = re.compile(r'name=["\']robots["\'][^>]*content=["\'][^"\']*noindex', re.I)

titles, descs, canon = collections.defaultdict(list), collections.defaultdict(list), {}
for p in sweep_files("*.html"):
    d = open(os.path.join(ROOT, p), encoding="utf-8", errors="replace").read()
    if STUB.search(d) or NOIDX.search(d):
        continue
    c = re.search(r'rel=["\']?canonical["\']?[^>]*href=["\']([^"\']+)', d)
    canon[p] = c.group(1).rstrip("/") if c else p
    m = re.search(r"<title[^>]*>(.*?)</title>", d, re.S)
    if m:
        titles[re.sub(r"\s+", " ", m.group(1)).strip()].append(p)
    m = re.search(r'<meta\s+name="description"\s+content="([^"]*)"', d)
    if m:
        descs[m.group(1).strip()].append(p)

bad = []
for label, M in (("title", titles), ("description", descs)):
    for v, ps in M.items():
        if len(ps) > 1 and len({canon[p] for p in ps}) > 1:
            bad.append((label, v, ps))

for label, v, ps in bad[:10]:
    print(f"  duplicate {label} across {len(ps)} pages with different canonicals:")
    print(f"    \"{v[:70]}\"")
    for p in ps:
        print(f"      {p} -> {canon[p]}")
if not bad:
    print(f"PASS    dup-meta ({len(titles)} titles, {len(descs)} descriptions, no competing duplicates)")
    sys.exit(0)
print(f"FAIL    dup-meta: {len(bad)} competing duplicate(s)")
sys.exit(1)
