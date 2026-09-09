#!/usr/bin/env python3
"""On-page SEO hygiene scan. Prints one line per issue, then COUNT=<n>.

Exclusions, each deliberate:
  redirect stubs   ~690-byte meta-refresh pages, noindexed. None of these rules
                   is meaningful there.
  D8 never-touch   Buy American pages. Hard stop 4 forbids editing them, so
                   flagging one would demand a change another check forbids.
                   The deny list wins and neither check is weakened.
  google*.html     Search Console verification stub, byte-exact by policy.
  services-schema  JSON-LD include fragment, not a page, robots-disallowed.
"""
import os
import re
import subprocess
import sys

ROOT = sys.argv[1] if len(sys.argv) > 1 else "."

r = subprocess.run(["git", "-C", ROOT, "ls-tree", "-r", "--name-only", "HEAD"],
                   capture_output=True, text=True).stdout.splitlines()
pages = [p for p in r if p.endswith(".html") and not p.startswith(".github/")]

STUB = re.compile(r'http-equiv=["\']?refresh', re.I)
EXEMPT_H1 = re.compile(r"^google[0-9a-f]+\.html$|services-schema-block\.html$")

deny = set()
dl = os.path.join(ROOT, ".github/agent-state/state/deny-list-buy-american.txt")
if os.path.isfile(dl):
    deny = {l.strip() for l in open(dl) if l.strip() and not l.startswith("#")}

fails = []
for p in pages:
    fp = os.path.join(ROOT, p)
    if not os.path.isfile(fp) or p in deny:
        continue
    d = open(fp, encoding="utf-8", errors="replace").read()
    if STUB.search(d):
        continue

    t = re.search(r"<title[^>]*>(.*?)</title>", d, re.S)
    if t:
        T = re.sub(r"\s+", " ", t.group(1)).strip()
        if len(T) > 60:
            fails.append((p, f"title {len(T)} chars, max 60"))

    m = re.search(r'<meta\s+name="description"\s+content="([^"]*)"', d)
    if m and len(m.group(1)) > 155:
        fails.append((p, f"description {len(m.group(1))} chars, max 155"))

    h1 = len(re.findall(r"<h1\b", d, re.I))
    if h1 > 1:
        fails.append((p, f"{h1} h1 elements, exactly 1 required"))
    elif h1 == 0 and not EXEMPT_H1.search(p):
        fails.append((p, "no h1"))

    og = re.search(r'property="og:title"\s+content="([^"]*)"', d)
    tw = re.search(r'name="twitter:title"\s+content="([^"]*)"', d)
    if og and tw and og.group(1).strip() != tw.group(1).strip():
        fails.append((p, "og:title != twitter:title"))

    if re.search(r'(?:content|title|alt|placeholder)="[^"]*<!--', d):
        fails.append((p, "HTML comment inside an attribute value"))

for p, msg in fails[:25]:
    print(f"  {p}: {msg}")
print(f"COUNT={len(fails)}")
