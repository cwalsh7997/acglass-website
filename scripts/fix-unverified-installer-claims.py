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

    # ===== ROUND 2 (2026-06-30): concentrated residual — verbatim strings from the residual scan =====
    # Dedicated brand-page <title> / og:title / og:description / meta description
    ("<title>TGP Authorized Fire-Rated Glass Installer — Florida | ACG</title>",
     "<title>TGP Fire-Rated Glass Installer — Florida | ACG</title>"),
    ("<title>Fire-Rated Glass Systems Installation — TGP Authorized | ACG</title>",
     "<title>Fire-Rated Glass Systems Installation — TGP | ACG</title>"),
    ("<title>TGP Fire-Rated Glazing Certified Installer | ACG</title>",
     "<title>TGP Fire-Rated Glazing Installer | ACG</title>"),
    ("<title>Slimpact Authorized Commercial Installer — Florida | ACG</title>",
     "<title>Slimpact Commercial Installer — Florida | ACG</title>"),
    ("<title>PGT Authorized Commercial Installer — Florida | ACG</title>",
     "<title>PGT Commercial Installer — Florida | ACG</title>"),
    ('content="Slimpact Authorized Commercial Installer — Florida"',
     'content="Slimpact Commercial Installer — Florida"'),
    ('content="PGT Authorized Commercial Installer — Florida"',
     'content="PGT Commercial Installer — Florida"'),
    ('content="Allegion Authorized Commercial Installer — Florida"',
     'content="Allegion Commercial Installer — Florida"'),
    ('content="TGP-authorized fire-rated glass installer. UL-listed assemblies, 20-min to 120-min ratings."',
     'content="TGP fire-rated glass installer. UL-listed assemblies, 20-min to 120-min ratings."'),
    ('content="PGT WinGuard commercial impact-rated windows and doors. 12 active Miami-Dade NOAs. ACG is the authorized commercial installer across Florida."',
     'content="PGT WinGuard commercial impact-rated windows and doors. 12 active Miami-Dade NOAs. ACG installs PGT WinGuard commercial systems across Florida."'),
    ('content="ACG is an authorized commercial installer for PGT WinGuard impact-rated windows and doors. 12 active Miami-Dade NOAs."',
     'content="ACG installs PGT WinGuard impact-rated windows and doors. 12 active Miami-Dade NOAs."'),
    # Per-brand FAQ-schema questions + visible <h3> (drop the "authorized" framing of the question)
    ("Is ACG an authorized PGT installer?", "Does ACG install PGT systems?"),
    ("Is ACG an authorized TGP installer?", "Does ACG install TGP fire-rated glass?"),
    # Per-brand answer/prose: "is an authorized commercial installer (for|of)" -> "installs"
    ("Yes. ACG (FL CGC #1531993) is an authorized commercial installer for PGT WinGuard products across Florida and the Southeast.",
     "Yes. ACG (FL CGC #1531993) installs PGT WinGuard products across Florida and the Southeast."),
    ("ACG is an authorized commercial installer of PGT WinGuard impact-rated aluminum windows and doors.",
     "ACG installs PGT WinGuard impact-rated aluminum windows and doors."),
    ("ACG is an authorized commercial installer for Allegion products on Florida commercial projects.",
     "ACG installs Allegion products on Florida commercial projects."),
    ("American Commercial Glass is an authorized installer of Technical Glass Products (TGP) fire-rated glazing systems.",
     "American Commercial Glass installs Technical Glass Products (TGP) fire-rated glazing systems."),
    ("Authorized installer for ESWindows, Euro-Wall, PGT, Allegion, and TGP commercial impact-rated systems.",
     "Installer of ESWindows, Euro-Wall, PGT, Allegion, and TGP commercial impact-rated systems."),
    ("Authorized TGP installer with experience on hospital, school, multifamily, and federal projects across Florida.",
     "Experienced TGP fire-rated glass installer on hospital, school, multifamily, and federal projects across Florida."),
    ("As an authorized PGT installer, ACG installs PGT impact storefront and entrance systems",
     "ACG installs PGT impact storefront and entrance systems"),
    ("Allegion authorized installer status streamlines the substitution review.",
     "Allegion installation experience streamlines the substitution review."),
    ("Authorized TGP, Vetrotech, and Pyrobel installer.",
     "TGP, Vetrotech, and Pyrobel installer."),
    # "seven authorizations" marketing phrasings (always include the unverified five -> always a violation)
    ("Authorized installer for <strong>ESWindows, Euro-Wall, PGT, Allegion, TGP, Slimpact, and Aldora</strong> commercial storefront systems",
     "Installer of <strong>ESWindows, Euro-Wall, PGT, Allegion, TGP, Slimpact, and Aldora</strong> commercial storefront systems"),
    ("through authorized relationships with Euro-Wall, ESWindows, PGT, Allegion, TGP, Slimpact, and Aldora",
     "through installation relationships with Euro-Wall, ESWindows, PGT, Allegion, TGP, Slimpact, and Aldora"),
    ("ACG's authorized installer relationships across ESWindows, Euro-Wall, PGT, Allegion, TGP, Slimpact, and Aldora",
     "ACG's installer relationships across ESWindows, Euro-Wall, PGT, Allegion, TGP, Slimpact, and Aldora"),
    ("Seven manufacturer authorizations across HVHZ-rated lines.", "Seven manufacturer partners across HVHZ-rated lines."),
    ("Seven manufacturer authorizations.", "Seven manufacturer partners."),
    ("Authorized installer on all seven manufacturers.", "Installer across all seven manufacturers."),
    ("7 authorized manufacturer partners", "7 manufacturer partners"),
    ("ESWindows, Euro-Wall, PGT, Allegion, TGP, Slimpact, Aldora — all authorized, all carried as standard installation options.",
     "ESWindows, Euro-Wall, PGT, Allegion, TGP, Slimpact, Aldora — all carried as standard installation options."),
    ("few are authorized across the Euro-Wall, ESWindows, PGT, Allegion, TGP, Slimpact, Aldora lineup",
     "few install across the Euro-Wall, ESWindows, PGT, Allegion, TGP, Slimpact, Aldora lineup"),
    ("ACG's seven-manufacturer authorized list", "ACG's seven-manufacturer install list"),
    ("seven approved manufacturer partners", "seven manufacturer partners"),
    # WBE certification assertion in FAQ schema -> truthful woman-owned (Connor-sourced: Rielly 51%), no held-cert claim
    ("Yes. American Commercial Glass holds Women-owned Business Enterprise (WBE) certification, qualifying the company for federal and state set-aside programs and prime contractor diversity participation goals. Certificate available on request.",
     "American Commercial Glass is majority woman-owned (Rielly Walsh, 51%). Formal WBE/SBE certification status is being finalized — confirm current certification directly with ACG before relying on it for set-aside or diversity-participation goals."),

    # ===== ROUND 3 (2026-06-30): remaining unambiguous per-brand violations =====
    # Per-brand page meta descriptions
    ('"description": "ACG is an authorized commercial installer for Technical Glass Products (TGP) products across Florida and the Southeast."',
     '"description": "ACG installs Technical Glass Products (TGP) products across Florida and the Southeast."'),
    ('"description": "ACG is an authorized commercial installer for Slimpact / Faour Glass Technologies products across Florida and the Southeast."',
     '"description": "ACG installs Slimpact / Faour Glass Technologies products across Florida and the Southeast."'),
    ('"description": "ACG is an authorized commercial installer for PGT products across Florida and the Southeast."',
     '"description": "ACG installs PGT products across Florida and the Southeast."'),
    ('"description": "ACG is an authorized commercial installer for Allegion products across Florida and the Southeast."',
     '"description": "ACG installs Allegion products across Florida and the Southeast."'),
    # Reference-table lead (common fragment across TGP/Slimpact/PGT/Aldora tables)
    ("commercial glazing systems that ACG is authorized to install.",
     "commercial glazing systems that ACG installs."),
    # Allegion / Slimpact FAQ questions (h3 + schema name)
    ("Is ACG an authorized Allegion installer?", "Does ACG install Allegion products?"),
    ("Is ACG an authorized Slimpact installer?", "Does ACG install Slimpact systems?"),
    # Capability badges / tags
    ('<div class="cat-mfg">Allegion authorized</div>', '<div class="cat-mfg">Allegion</div>'),
    ('<div class="cat-mfg">TGP authorized</div>', '<div class="cat-mfg">TGP</div>'),
    ('<div class="cap-tag">Allegion authorized →</div>', '<div class="cap-tag">Allegion →</div>'),
    ('<div class="cap-tag">TGP authorized →</div>', '<div class="cap-tag">TGP →</div>'),
    ('<div class="meta">TGP · authorized →</div>', '<div class="meta">TGP →</div>'),
    # "other authorized partner" / "ACG-authorized partners" / Aldora & Allegion partner claims
    ("ACG installs ESWindows, Euro-Wall, PGT, and other authorized partner storefront systems across Florida.",
     "ACG installs ESWindows, Euro-Wall, PGT, and other partner storefront systems across Florida."),
    ("ACG-authorized partners such as ESWindows, Euro-Wall, and PGT",
     "manufacturer partners such as ESWindows, Euro-Wall, and PGT"),
    ("TGP fire-rated glass and framing among ACG-authorized partners",
     "TGP fire-rated glass and framing among ACG's manufacturer partners"),
    ("and Aldora authorized manufacturer", "and Aldora manufacturer"),
    ("Allegion — an authorized manufacturer partner —", "Allegion — a manufacturer partner —"),

    # ===== ROUND 4 (2026-06-30): soft-but-real residual + WBE/SBE schema name neutralization =====
    ('"description": "ACG is an authorized commercial installer for PGT WinGuard impact-rated windows and doors. 12 active Miami-Dade NOAs. FL CGC',
     '"description": "ACG installs PGT WinGuard impact-rated windows and doors. 12 active Miami-Dade NOAs. FL CGC'),
    ("Yes. ACG is an authorized installer for ESWindows and Aldora,",
     "Yes. ACG installs ESWindows and Aldora,"),
    ("ACG is an authorized Allegion installation contractor.",
     "ACG is an Allegion installation contractor."),
    ("storefront from our authorized partners", "storefront from our manufacturer partners"),
    ("Allegion, and other authorized partners.", "Allegion, and other manufacturer partners."),
    ("ACG's authorized manufacturer partnerships", "ACG's manufacturer partnerships"),
    ("As an authorized partner for ESWindows, Euro-Wall, PGT, Allegion, TGP, Slimpact, and Aldora, ACG orders systems direct",
     "As an installer of ESWindows, Euro-Wall, PGT, Allegion, TGP, Slimpact, and Aldora systems, ACG orders direct"),
    ("require ACG's specific manufacturer authorizations", "require ACG's specific manufacturer experience"),
    ("ACG's TGP authorization and installation experience", "ACG's TGP fire-rated installation experience"),
    ("<strong>Manufacturer authorization breadth.</strong>", "<strong>Manufacturer breadth.</strong>"),
    # WBE/SBE schema credential NAME neutralization (interim — full object removal + 1,484 prose files queued for Connor).
    # Verified CGC + verified Euro-Wall/ESWindows dealer-authorization credentials are untouched (different name strings).
    ('"name": "Woman-Owned Business Enterprise (WBE)"', '"name": "Woman-owned business (majority owner Rielly Walsh)"'),
    ('"name": "Small Business Enterprise (SBE)"', '"name": "Small business"'),
    ('"name": "WBE — Women\'s Business Enterprise"', '"name": "Woman-owned business"'),
    ('"name": "SBE — Small Business Enterprise"', '"name": "Small business"'),

    # ===== ROUND 5 (2026-06-30): crisp schema name entries on dedicated brand pages (literal \\u2014 em-dash escape) =====
    ('"name": "Authorized Slimpact / Faour Glass Technologies Installer \\u2014 Florida"',
     '"name": "Slimpact / Faour Glass Technologies Installer \\u2014 Florida"'),
    ('"name": "Authorized PGT Installer \\u2014 Florida"',
     '"name": "PGT Installer \\u2014 Florida"'),
    ('"name": "Authorized Allegion Installer \\u2014 Florida"',
     '"name": "Allegion Installer \\u2014 Florida"'),
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
