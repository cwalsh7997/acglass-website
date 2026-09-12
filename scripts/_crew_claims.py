#!/usr/bin/env python3
"""Crew-training claims, D2 obligation 4.

RESOLVED 2026-09-09 by Connor, answering questionnaire items 25 and 26.

  25  OSHA 30: every field employee holds current OSHA 30. The claim is accurate
      and all 201 occurrences stay as written. D2 froze it pending an answer, and
      the answer unfreezes it.
  26  AAMA InstallationMasters: ACG does NOT hold a current certification. All 6
      ACG self-claims removed.

WHAT WAS REMOVED, AND WHAT DELIBERATELY WAS NOT. My earlier count said 8
occurrences on 5 pages and treated them as one class. They are two, and only one
was a false claim:

  REMOVED, assertive ACG self-claims:
    "ACG holds the FL CGC license and AAMA InstallationMasters credentials
     required for impact-rated work"                          x3
    "...and AAMA InstallationMasters training required for HVHZ work"  x2
    a credentials list reading "FL CGC #1531993, AAMA InstallationMasters
     training, ..."                                            x1

  LEFT ALONE, because none of it claims ACG holds anything:
    architect-specs/*  spec sections stating what an INSTALLER must hold. ACG
                       writes these for architects. A requirement is not a claim.
    blog advice        pages telling a GC what to look for when vetting a glazier.
    glossary.html      an entry explaining what the programme is.

This check therefore guards one thing: no ACG self-claim to InstallationMasters
returns. It does not sweep the term, because sweeping it would delete correct spec
language and useful advice.
"""
import os, re, sys

ROOT = sys.argv[1] if len(sys.argv) > 1 else "."
sys.path.insert(0, os.path.join(ROOT, "scripts"))
from sweep_files import sweep_files

# assertive ACG self-claim to holding the certification
SELF = re.compile(
    r'(?:ACG|American Commercial Glass|we|our)\b[^.<>"]{0,90}?'
    r'(?:holds?|carr(?:y|ies)|maintain(?:s)?|certified|trained)[^.<>"]{0,60}?'
    r'(InstallationMasters|Installation Masters)'
    r'|(?:CGC\s*#?\s*\d{6,8})[^.<>"]{0,20}(InstallationMasters|Installation Masters)',
    re.I)

hits = []
for p in sweep_files("*.html"):
    d = open(os.path.join(ROOT, p), encoding="utf-8", errors="replace").read()
    for m in SELF.finditer(d):
        hits.append((p, m.group(0)[:90]))

for p, s in hits[:10]:
    print(f"  {p}: {s}")
if not hits:
    print("PASS    crew-training-claims (OSHA 30 confirmed accurate; no InstallationMasters self-claim)")
    sys.exit(0)
print(f"FAIL    crew-training-claims: {len(hits)} InstallationMasters self-claim(s), D2 item 26 is NO")
sys.exit(1)
