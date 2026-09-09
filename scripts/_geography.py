#!/usr/bin/env python3
"""Hard stop 8: no assertive self-perform claim outside the confirmed counties.

The previous version of this check did nothing. Once geography-counties.txt was
complete it printed PASS and exited, having validated no page at all. A green tick
that means nothing is worse than a red one, because it stops anyone looking.

WHAT IT ACTUALLY CHECKS NOW. An ALLOWLIST of assertive self-perform phrasing tied
to a named county. "Our crews install in X County" is a claim about where ACG puts
labour. "Serving X County" or "commercial glazing in X" is coverage language and is
deliberately left alone: ACG may quote, furnish and consult far more widely than it
self-performs, and conflating the two would flag most of the site for no reason.

Out-of-state claims are handled separately by check-out-of-state-claims.sh, which
requires them to be noindexed.
"""
import os, re, sys

ROOT = sys.argv[1] if len(sys.argv) > 1 else "."
sys.path.insert(0, os.path.join(ROOT, "scripts"))
from sweep_files import sweep_files

CFG = os.path.join(ROOT, ".github/agent-state/config/geography-counties.txt")
ok = {l.strip().lower() for l in open(CFG) if l.strip() and not l.startswith("#")}

FL_COUNTIES = [
    "Palm Beach", "Martin", "St. Lucie", "Broward", "Miami-Dade", "Lee", "Collier",
    "Orange", "Osceola", "Seminole", "Hillsborough", "Pinellas", "Pasco", "Polk",
    "Sarasota", "Manatee", "Charlotte", "Volusia", "Brevard", "Duval", "Alachua",
    "Leon", "Escambia", "Monroe", "Indian River", "Okeechobee", "Highlands",
]
SELF = (r'(?:our|ACG(?:\'s)?|we)\s+(?:own\s+)?(?:field\s+)?'
        r'(?:crews?|installers?|glaziers?|teams?)\s+'
        r'(?:[a-z]+\s+){0,3}?(?:install|self-perform|work|operate|are based)')
ALSO = r'(?:we|ACG)\s+self-perform'

bad = []
for p in sweep_files("*.html"):
    d = open(os.path.join(ROOT, p), encoding="utf-8", errors="replace").read()
    for m in re.finditer(SELF + "|" + ALSO, d, re.I):
        window = d[m.start():m.start() + 260]
        for c in FL_COUNTIES:
            if c.lower() in ok:
                continue
            m2 = re.search(re.escape(c) + r"\s+Count", window, re.I)
            if not m2:
                continue
            # "familiar with X County's review process" is knowledge of a
            # jurisdiction, not a claim to put crews in it. ACG can know Orange
            # County's Building Division without self-performing there, and
            # flagging that would be flagging competence.
            between = window[m.end() - m.start():m2.start()]
            if re.search(r"familiar with|know|understand|experience with|versed in", between, re.I):
                continue
            bad.append((p, c, re.sub(r"\s+", " ", window[:110])))
            break

for p, c, s in bad[:12]:
    print(f"  {p}: self-perform claim tied to {c} County, which is not on the list")
    print(f"      {s}")
if not bad:
    print(f"PASS    geography ({len(ok)} confirmed counties, no self-perform claim outside them)")
    sys.exit(0)
print(f"FAIL    geography: {len(bad)} out-of-area self-perform claim(s)")
sys.exit(1)
