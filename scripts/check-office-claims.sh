#!/usr/bin/env bash
# Every address published as an ACG location is a confirmed one.
#
# RESOLVED 2026-09-09. Connor confirmed both regional offices are real leased space:
# Naples at 4850 Tamiami Trail N Ste 301, and Tampa at 3031 N Rocky Point Dr W
# Ste 600. Both stay in body copy and in LocalBusiness schema on all 17 pages each.
# Nothing was removed.
#
# The check guards the opposite direction now. Before, it pinned two unconfirmed
# addresses so they could not spread while unresolved. Now it fails if a street
# address is published in ACG's own PostalAddress schema that is NOT in
# config/offices.txt, which is the case that actually matters: a new location
# appearing in machine-readable form without anyone confirming it exists.
#
# Structured-data office claims are the reason this is a check and not a style
# note. Google may use them for local pack eligibility, so a wrong one is a false
# business location submitted to a search engine rather than a wording slip.
source "$(dirname "$0")/_lib.sh"
CFGF="$ROOT/.github/agent-state/config/offices.txt"
[ -f "$CFGF" ] || { say "CONFIG  office-claims: offices.txt missing"; exit 3; }
python3 - "$ROOT" "$CFGF" <<'PY'
import json, os, re, sys
ROOT, CFGF = sys.argv[1], sys.argv[2]
sys.path.insert(0, os.path.join(ROOT, "scripts"))
from sweep_files import sweep_files

ok = set()
for line in open(CFGF):
    if "=" in line and not line.startswith("#"):
        ok.add(line.split("=", 1)[1].split("|")[0].strip().lower())

# ACG's own addresses only. Manufacturer and third-party Organization nodes carry
# their own addresses and are none of this check's business.
found = {}
def walk(node, page):
    if isinstance(node, dict):
        nm = str(node.get("name", ""))
        t = node.get("@type", "")
        t = t if isinstance(t, str) else "+".join(str(x) for x in t)
        # Organization-like types ONLY, and the name must be ACG. A Place or a
        # Hotel with an address is a PROJECT SITE, not an ACG location, and an
        # @id under acglass.com does not make the entity ACG: page-scoped fragment
        # ids like "...#place" live on our domain by definition. Matching on @id
        # flagged Atlantic Fields and Eau Palm Beach Resort as unconfirmed ACG
        # offices, which they obviously are not.
        org = any(k in t for k in ("Organization", "LocalBusiness", "HomeAndConstructionBusiness"))
        mine = org and ("american commercial glass" in nm.lower() or nm.strip().upper() == "ACG")
        a = node.get("address")
        if mine and isinstance(a, dict):
            s = str(a.get("streetAddress", "")).strip()
            if s and s.lower() not in ok:
                found.setdefault(s, set()).add(page)
        for v in node.values():
            walk(v, page)
    elif isinstance(node, list):
        for v in node:
            walk(v, page)

for p in sweep_files("*.html"):
    d = open(os.path.join(ROOT, p), encoding="utf-8", errors="replace").read()
    for b in re.findall(r'<script[^>]+application/ld\+json[^>]*>(.*?)</script>', d, re.S):
        try:
            walk(json.loads(b), p)
        except Exception:
            pass

for s, pages in list(found.items())[:8]:
    print(f"  unconfirmed ACG address in schema: \"{s}\" on {len(pages)} page(s)")
if not found:
    print(f"PASS    office-claims ({len(ok)} confirmed location(s), no unconfirmed address in schema)")
    sys.exit(0)
print(f"FAIL    office-claims: {len(found)} address(es) not in config/offices.txt")
sys.exit(1)
PY
