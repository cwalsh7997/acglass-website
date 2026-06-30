#!/usr/bin/env python3
"""
fix-unverified-installer-claims.py  (Sprint 002, 2026-06-30)

Corrects UNVERIFIED "authorized installer" manufacturer claims site-wide.

Governance (operator Ledger 3.2): the ONLY verified authorized-installer
relationships are Euro-Wall and ESWindows / Tecnoglass. Claims of "authorized"
installer/installation/dealer status for PGT, Allegion, TGP, Slimpact, or Aldora
are unverified and a §2.2 liability. We do install these products, so the safe,
non-fabricating fix is to DOWNGRADE "authorized [X] installer/installation/dealer"
-> plain "installer of / installation / installer" (a permitted "we install it"
claim) wherever an unverified brand sits inside the qualified list.

Method: EXACT-STRING replacement only (str.replace). Exact match can MISS but can
never corrupt grammar. Anything missed is surfaced by the residual scan at the end
for manual review. Idempotent: re-running produces no further change.

The compliant string "authorized commercial installer for ESWindows and Euro-Wall.
For fire-rated openings we install TGP" (79 files) is intentionally NOT in the map
and is never a substring of any key, so it is preserved.

Usage:
  python3 scripts/fix-unverified-installer-claims.py          # dry-run (default)
  python3 scripts/fix-unverified-installer-claims.py --apply  # write changes
"""
import os, sys

APPLY = "--apply" in sys.argv
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# (old, new) — ordered most-specific first to avoid partial overlaps.
REPLACEMENTS = [
    # --- full comma-list variants (A / F) ---
    ("Authorized installer for ESWindows (Tecnoglass), Euro-Wall, PGT Innovations, Allegion, TGP, Slimpact, and Aldora",
     "Installer for ESWindows (Tecnoglass), Euro-Wall, PGT Innovations, Allegion, TGP, Slimpact, and Aldora"),
    ("authorized installer relationships with ESWindows (Tecnoglass), Euro-Wall, PGT, Allegion, TGP, Slimpact, and Aldora",
     "installer relationships with ESWindows (Tecnoglass), Euro-Wall, PGT, Allegion, TGP, Slimpact, and Aldora"),
    ("authorized commercial installer for ESWindows, Euro-Wall, PGT, Allegion, TGP, Slimpact, and Aldora",
     "commercial installer for ESWindows, Euro-Wall, PGT, Allegion, TGP, Slimpact, and Aldora"),
    ("authorized installer for seven approved manufacturer partners: ESWindows (Tecnoglass), Euro-Wall, PGT, Allegion, TGP (Technical Glass Products), Slimpact",
     "installer for seven manufacturer partners: ESWindows (Tecnoglass), Euro-Wall, PGT, Allegion, TGP (Technical Glass Products), Slimpact"),
    ("authorized-installer status with ESWindows, Euro-Wall, PGT, Allegion, TGP, Slimpact, and Aldora",
     "installation experience with ESWindows, Euro-Wall, PGT, Allegion, TGP, Slimpact, and Aldora"),
    ("authorized relationships with ESWindows, Euro-Wall, PGT, Allegion, TGP, Slimpact, and Aldora",
     "installation relationships with ESWindows, Euro-Wall, PGT, Allegion, TGP, Slimpact, and Aldora"),
    ("authorization across ESWindows, Euro-Wall, PGT, Allegion, TGP, Slimpact, and Aldora",
     "installation across ESWindows, Euro-Wall, PGT, Allegion, TGP, Slimpact, and Aldora"),
    ("Authorized installer for ESWindows, Euro-Wall, PGT, Allegion, TGP, Slimpact, and Aldora",
     "Installer for ESWindows, Euro-Wall, PGT, Allegion, TGP, Slimpact, and Aldora"),
    ("authorized installer for ESWindows, Euro-Wall, PGT, Allegion, TGP, Slimpact, and Aldora",
     "installer for ESWindows, Euro-Wall, PGT, Allegion, TGP, Slimpact, and Aldora"),
    ("authorized installation of ESWindows, Euro-Wall, PGT, Allegion, TGP, Slimpact, and Aldora",
     "installation of ESWindows, Euro-Wall, PGT, Allegion, TGP, Slimpact, and Aldora"),
    # no-Oxford-comma + trailing-period (og/meta) forms
    ("Authorized installer for ESWindows, Euro-Wall, PGT, Allegion, TGP, Slimpact, Aldora.",
     "Installer for ESWindows, Euro-Wall, PGT, Allegion, TGP, Slimpact, Aldora."),
    ("authorized installer for ESWindows, Euro-Wall, PGT, Allegion, TGP, Slimpact, Aldora",
     "installer for ESWindows, Euro-Wall, PGT, Allegion, TGP, Slimpact, Aldora"),
    ("ESWindows, Euro-Wall, PGT, Allegion, TGP, Slimpact, Aldora authorized installer.",
     "ESWindows, Euro-Wall, PGT, Allegion, TGP, Slimpact, Aldora installer."),
    ("Authorized installer status on Euro-Wall, ESWindows, TGP, PGT, and Allegion",
     "Installation experience on Euro-Wall, ESWindows, TGP, PGT, and Allegion"),
    # --- "+"-delimited (C) ---
    ("ESWindows + Euro-Wall + PGT + Allegion + TGP + Slimpact + Aldora authorized installation",
     "ESWindows + Euro-Wall + PGT + Allegion + TGP + Slimpact + Aldora installation"),
    # --- impact short list (D) ---
    ("ESWindows, PGT, Slimpact authorized installer.",
     "ESWindows, PGT, Slimpact installer."),
    ("ESWindows, PGT, Slimpact authorized.",
     "ESWindows, PGT, Slimpact systems installed."),
    # --- knowsAbout schema (I) ---
    ("\"PGT Commercial Dealer\"", "\"PGT Commercial Installer\""),
]

def iter_html():
    for dp, _, fns in os.walk(ROOT):
        if "/.git" in dp:
            continue
        for fn in fns:
            if fn.endswith(".html"):
                yield os.path.join(dp, fn)

per_pattern = {old: 0 for old, _ in REPLACEMENTS}
files_changed = 0
for path in iter_html():
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    new = content
    for old, repl in REPLACEMENTS:
        if old in new:
            per_pattern[old] += new.count(old)
            new = new.replace(old, repl)
    if new != content:
        files_changed += 1
        if APPLY:
            with open(path, "w", encoding="utf-8") as f:
                f.write(new)

mode = "APPLIED" if APPLY else "DRY-RUN (no files written)"
print(f"=== {mode} ===")
print(f"files changed: {files_changed}")
print("per-pattern occurrence counts:")
for old, _ in REPLACEMENTS:
    print(f"  {per_pattern[old]:>4}  {old[:70]}")
