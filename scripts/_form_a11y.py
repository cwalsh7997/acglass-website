#!/usr/bin/env python3
"""Every visible form control must have an accessible name.

Four ways a control gets one, and a check that only knows the first will invent
defects that are not there:

  1  <label for="x">  paired with  id="x"
  2  a WRAPPING label: <label>Email <input></label>, valid with no id at all
  3  aria-label
  4  aria-labelledby

Honeypots are excluded on purpose. A spam trap named _gotcha or _honey is meant
to be invisible to humans and unlabelled, and labelling one would defeat it.
"""
import os, re, subprocess, sys

ROOT = sys.argv[1] if len(sys.argv) > 1 else "."
sys.path.insert(0, os.path.join(ROOT, "scripts"))
from sweep_files import sweep_files

HONEY = re.compile(r'name="(_gotcha|_honey|honeypot|_subject)"')
SKIP_TYPE = re.compile(r'type="(hidden|submit|button|reset|image)"')

bad = []
for p in sweep_files("*.html"):
    d = open(os.path.join(ROOT, p), encoding="utf-8", errors="replace").read()
    for f in re.findall(r"<form\b.*?</form>", d, re.S):
        for_ids = set(re.findall(r'<label\b[^>]*\bfor="([^"]+)"', f))
        # controls sitting inside a wrapping label
        wrapped = set()
        for lm in re.finditer(r"<label\b[^>]*>(.*?)</label>", f, re.S):
            for cm in re.finditer(r"<(?:input|textarea|select)\b[^>]*>", lm.group(1)):
                wrapped.add(cm.group(0))
        for m in re.finditer(r"<(?:input|textarea|select)\b[^>]*>", f):
            t = m.group(0)
            if SKIP_TYPE.search(t) or HONEY.search(t):
                continue
            if t in wrapped:
                continue
            i = re.search(r'\bid="([^"]+)"', t)
            if i and i.group(1) in for_ids:
                continue
            if 'aria-label' in t:
                continue
            nm = re.search(r'name="([^"]*)"', t)
            bad.append((p, nm.group(1) if nm else "-", (i.group(1) if i else "no id")))

for p, n, i in bad[:20]:
    print(f"  {p}: control name={n} ({i}) has no accessible name")
if not bad:
    print("PASS    form-a11y (every visible form control has an accessible name)")
    sys.exit(0)
print(f"FAIL    form-a11y: {len(bad)} control(s) with no accessible name")
sys.exit(1)
