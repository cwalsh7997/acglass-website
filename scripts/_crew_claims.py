#!/usr/bin/env python3
"""Assertive ACG crew-training self-claims, frozen by D2 obligation 4."""
import os, re, sys, collections

ROOT = sys.argv[1] if len(sys.argv) > 1 else "."
sys.path.insert(0, os.path.join(ROOT, "scripts"))
from sweep_files import sweep_files

SELF = re.compile(
    r'(?:ACG|American Commercial Glass|we|our)\b[^.<]{0,80}?'
    r'(OSHA[ -]?30|InstallationMasters|Installation Masters)'
    r'|(OSHA[ -]?30|InstallationMasters|Installation Masters)[^.<]{0,40}?'
    r'(crews?|field (?:crew|employee|staff)|trained|certified|record)', re.I)
GENERIC = re.compile(r'\bshould (?:have|be)\b|\bat minimum\b|\bask (?:for|how)\b|\bverify\b', re.I)
IM = re.compile(r'InstallationMasters|Installation Masters', re.I)

osha = collections.Counter()
im = collections.Counter()
for p in sweep_files("*.html"):
    d = open(os.path.join(ROOT, p), encoding="utf-8", errors="replace").read()
    for m in SELF.finditer(d):
        if GENERIC.search(d[max(0, m.start() - 120):m.end() + 60]):
            continue
        (im if IM.search(m.group(0)) else osha)[p] += 1

no, ni = sum(osha.values()), sum(im.values())
print(f"  OSHA 30 as an ACG self-claim:            {no} occurrence(s) on {len(osha)} page(s)")
print(f"  InstallationMasters as an ACG self-claim: {ni} occurrence(s) on {len(im)} page(s)")
for p in sorted(im):
    print(f"     {p}")
if no == 0 and ni == 0:
    print("PASS    crew-training-claims (none published)")
    sys.exit(0)
print(f"FAIL    crew-training-claims: {no + ni} frozen claim(s) published, D2 obligation 4")
sys.exit(1)
