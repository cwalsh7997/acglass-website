#!/usr/bin/env python3
"""Every internal href must resolve to a file on disk."""
import os, re, subprocess, sys, collections

ROOT = sys.argv[1] if len(sys.argv) > 1 else "."
pages = [p for p in subprocess.run(["git", "-C", ROOT, "ls-files", "*.html"],
         capture_output=True, text=True).stdout.split() if not p.startswith(".github/")]

bad = collections.defaultdict(list)
for p in pages:
    d = open(os.path.join(ROOT, p), encoding="utf-8", errors="replace").read()
    for h in re.findall(r'href="(/[^":#?]*)"', d):
        t = h.lstrip("/")
        if not t:
            continue
        cands = (t, t + "index.html", t.rstrip("/") + "/index.html", t.rstrip("/") + ".html")
        if not any(os.path.isfile(os.path.join(ROOT, c)) for c in cands):
            bad[h].append(p)

for t, srcs in sorted(bad.items(), key=lambda x: -len(x[1]))[:15]:
    print(f"  {t} :: {len(srcs)} occurrence(s), e.g. {srcs[0]}")
n = sum(len(v) for v in bad.values())
if n == 0:
    print(f"PASS    broken-links (every internal href on {len(pages)} pages resolves)")
    sys.exit(0)
print(f"FAIL    broken-links: {n} occurrence(s) across {len(bad)} distinct target(s)")
sys.exit(1)
