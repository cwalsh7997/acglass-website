#!/usr/bin/env python3
"""
validate-jsonld.py — structured-data regression gate for acglass.com

Runs against the checked-out repo (no network), so it can block a bad merge
before it ever reaches Pages. Every rule below encodes a defect that was
actually shipped at some point; see the docstring on each check.

Usage:
  python .github/scripts/validate-jsonld.py            # whole site
  python .github/scripts/validate-jsonld.py --sample   # representative classes only
  python .github/scripts/validate-jsonld.py -v         # list every offending file
"""

from __future__ import annotations
import argparse
import collections
import glob
import html
import json
import os
import re
import sys
from pathlib import Path

SCRIPT_RE = re.compile(
    r'<script[^>]*type=["\']application/ld\+json["\'][^>]*>(.*?)</script>', re.S | re.I)
STRIP_RE = re.compile(r"<script.*?</script>|<style.*?</style>", re.S | re.I)

ORG_ID = "https://acglass.com/#organization"
ORG_NAME = "American Commercial Glass"

# Offices with a street address, staff on site, and signage (facts.html,
# locations.html). Nashville is announced for Q3 2026 with no street address —
# a LocalBusiness node there would assert premises that do not exist.
VERIFIED_OFFICES = {
    "https://acglass.com/#localbusiness-west-palm-beach": "West Palm Beach",
    "https://acglass.com/#localbusiness-naples": "Naples",
    "https://acglass.com/#localbusiness-tampa": "Tampa",
}

# The parent Organization may carry a postal address, but only the real HQ.
HQ_ADDRESS = {
    "@type": "PostalAddress", "streetAddress": "700 S Rosemary Ave Suite 204",
    "addressLocality": "West Palm Beach", "addressRegion": "FL",
    "postalCode": "33401", "addressCountry": "US",
}

# Legacy @ids for the same entities. Reintroducing one splits the graph.
RETIRED_IDS = {
    "https://acglass.com/#org",
    "https://acglass.com#organization",
    "https://acglass.com/#office-west-palm-beach",
    "https://acglass.com/#office-naples",
    "https://acglass.com/#office-tampa",
    "https://acglass.com/#office-nashville",
    "https://acglass.com/#localbusiness-wpb",
}

# Self-applied ratings violate Google's LocalBusiness spec and are FTC 16 CFR
# 465 exposure. Third-party ratings about a *client's* property are fine, so
# the rule is scoped to ACG's own nodes.
RATING_PROPS = ("aggregateRating", "ratingValue", "reviewCount", "review")

# Properties schema.org defines on Place/LocalBusiness but not on Organization.
PLACE_ONLY = {
    "priceRange", "openingHoursSpecification", "openingHours", "geo", "hasMap",
    "currenciesAccepted", "paymentAccepted", "branchCode",
    "specialOpeningHoursSpecification", "starRating", "smokingAllowed",
}

# Unrendered template placeholders that leaked into shipped markup. Matched
# against string values in the parsed graph, never the raw block — "}}" is
# ordinary structure in compact JSON.
LEAKED_SUBSTRINGS = ("Near Me Florida", "{{", "}}", "${", "%7B%7B")
LEAKED_EXACT = {"undefined", "null", "TODO", "N/A", "None"}

# Sitewide claim guard: BBB accreditation is not held.
BBB_CLAIM_RE = re.compile(r"BBB[- ]accredited|accredited\s+by\s+the\s+Better\s+Business", re.I)

# One file per page class the site actually generates.
SAMPLE = [
    "index.html",
    "services.html",
    "about.html",
    "contact.html",
    "locations.html",
    "portfolio.html",
    "capabilities.html",
    "faq.html",
    "reviews/index.html",
    "west-palm-beach-commercial-glazing.html",
    "commercial-glazing-near-me-florida.html",
    "eau-palm-beach-resort.html",
]


def typelist(node) -> list[str]:
    t = node.get("@type")
    if isinstance(t, list):
        return [x for x in t if isinstance(x, str)]
    return [t] if isinstance(t, str) else []


def is_acg(node) -> bool:
    name = node.get("name") if isinstance(node.get("name"), str) else ""
    legal = node.get("legalName") if isinstance(node.get("legalName"), str) else ""
    if ORG_NAME in f"{name} {legal}":
        return True
    return name.strip() in ("ACG", "ACG Glass") or node.get("@id") in (
        {ORG_ID} | set(VERIFIED_OFFICES) | RETIRED_IDS)


def visible_text(src: str) -> str:
    s = STRIP_RE.sub(" ", src)
    s = re.sub(r"<[^>]+>", " ", s)
    return re.sub(r"\s+", " ", html.unescape(s)).lower()


def norm_q(q) -> str:
    return re.sub(r"\s+", " ", html.unescape(str(q))).strip().strip("?").strip().lower()


class Report:
    def __init__(self) -> None:
        self.failures: dict[str, list[str]] = collections.defaultdict(list)
        self.counts: collections.Counter = collections.Counter()
        self.files = 0

    def fail(self, rule: str, where: str) -> None:
        self.failures[rule].append(where)


def iter_strings(obj):
    if isinstance(obj, str):
        yield obj
    elif isinstance(obj, dict):
        for k, v in obj.items():
            yield k
            yield from iter_strings(v)
    elif isinstance(obj, list):
        for v in obj:
            yield from iter_strings(v)


def iter_nodes(obj):
    if isinstance(obj, dict):
        yield obj
        for v in obj.values():
            yield from iter_nodes(v)
    elif isinstance(obj, list):
        for v in obj:
            yield from iter_nodes(v)


def conflicting_id_properties(parsed: list) -> list[tuple[str, str]]:
    """Return properties that assert different values for the same @id.

    A second node with only @id, or with @id and @type, is a reference and is
    intentionally ignored. Separate definitions with disjoint properties are
    complementary. Only repeated properties with different JSON values are
    collisions.
    """
    values: dict[str, dict[str, set[str]]] = collections.defaultdict(
        lambda: collections.defaultdict(set))
    for data in parsed:
        for node in iter_nodes(data):
            nid = node.get("@id")
            if not isinstance(nid, str):
                continue
            for prop, value in node.items():
                if prop in {"@context", "@id", "@type"}:
                    continue
                values[nid][prop].add(
                    json.dumps(value, sort_keys=True, separators=(",", ":")))
    return sorted(
        (nid, prop)
        for nid, properties in values.items()
        for prop, asserted in properties.items()
        if len(asserted) > 1
    )


def check_file(path: str, rep: Report) -> None:
    src = Path(path).read_text(encoding="utf-8")
    blocks = SCRIPT_RE.findall(src)
    if not blocks:
        return
    rep.files += 1
    vis = visible_text(src)

    parsed = []
    for i, blk in enumerate(blocks):
        try:
            data = json.loads(blk)
        except json.JSONDecodeError as e:
            rep.fail("json_parse", f"{path} block#{i}: {e}")
            continue
        parsed.append(data)
        for s in iter_strings(data):
            hit = next((t for t in LEAKED_SUBSTRINGS if t in s), None)
            if hit is None and s.strip() in LEAKED_EXACT:
                hit = s.strip()
            if hit:
                rep.fail("template_leak", f"{path} block#{i}: {hit!r} in {s[:60]!r}")

    if BBB_CLAIM_RE.search(src):
        rep.fail("bbb_accreditation_claim", path)

    id_types: dict[str, set[tuple]] = collections.defaultdict(set)
    faq_pages = []

    for data in parsed:
        for node in iter_nodes(data):
            types = typelist(node)
            for t in types:
                rep.counts[t] += 1
            nid = node.get("@id")

            if isinstance(nid, str):
                if nid in RETIRED_IDS:
                    rep.fail("retired_id", f"{path}: {nid}")
                if types:
                    id_types[nid].add(tuple(sorted(types)))

            if "FAQPage" in types:
                faq_pages.append(node)

            acg = is_acg(node)

            if acg and any(p in node for p in RATING_PROPS):
                found = [p for p in RATING_PROPS if p in node]
                rep.fail("self_rating", f"{path}: {nid or node.get('name')} {found}")

            if "LocalBusiness" in types and acg:
                if nid not in VERIFIED_OFFICES:
                    rep.fail("unverified_localbusiness", f"{path}: @id={nid!r}")
                else:
                    addr = node.get("address")
                    if not isinstance(addr, dict) or not addr.get("streetAddress"):
                        rep.fail("localbusiness_no_street", f"{path}: {nid}")
                    elif addr.get("addressLocality") != VERIFIED_OFFICES[nid]:
                        rep.fail(
                            "localbusiness_wrong_city",
                            f"{path}: {nid} -> {addr.get('addressLocality')!r}")
                    if node.get("parentOrganization", {}).get("@id") != ORG_ID:
                        rep.fail("localbusiness_orphan", f"{path}: {nid}")

            if types == ["Organization"] and acg:
                if nid != ORG_ID:
                    rep.fail("org_wrong_id", f"{path}: @id={nid!r}")
                if node.get("name") != ORG_NAME:
                    rep.fail("org_wrong_name", f"{path}: {node.get('name')!r}")
                addr = node.get("address")
                if addr is not None and addr != HQ_ADDRESS:
                    rep.fail("org_wrong_address", f"{path}: {json.dumps(addr)[:120]}")
                stray = sorted(PLACE_ONLY & set(node))
                if stray:
                    rep.fail("org_place_props", f"{path}: {stray}")

            # A node must not be both the page and a business.
            if "WebPage" in types and (set(types) & {"LocalBusiness", "Organization"}):
                rep.fail("webpage_business_conflation", f"{path}: {types}")

    for nid, tsets in id_types.items():
        if len(tsets) > 1:
            rep.fail("id_type_conflict", f"{path}: {nid} {sorted(tsets)}")

    for nid, prop in conflicting_id_properties(parsed):
        rep.fail("id_property_conflict", f"{path}: {nid} [{prop}]")

    # Google requires structured data to match visible page text. Questions the
    # user cannot see on the page are an AI-features policy violation.
    if len(faq_pages) > 1:
        rep.fail("duplicate_faqpage", f"{path}: {len(faq_pages)} FAQPage nodes")
    for faq in faq_pages:
        me = faq.get("mainEntity")
        qs = [me] if isinstance(me, dict) else [q for q in (me or []) if isinstance(q, dict)]
        invisible = [q.get("name") for q in qs if q.get("name") and norm_q(q["name"]) not in vis]
        if qs and len(invisible) == len(qs):
            rep.fail("invisible_faq", f"{path}: {len(qs)} questions, none in body text")


PRESERVE = ["Organization", "WebSite", "Service", "BreadcrumbList", "Article",
            "Project", "FAQPage", "LocalBusiness", "WebPage", "Person"]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--sample", action="store_true",
                    help="check one file per page class instead of the whole site")
    ap.add_argument("-v", "--verbose", action="store_true",
                    help="list every offending file, not just the first few")
    ap.add_argument("--root", default=".", help="repo root")
    args = ap.parse_args()

    os.chdir(args.root)
    if args.sample:
        files = [f for f in SAMPLE if os.path.exists(f)]
        missing = [f for f in SAMPLE if not os.path.exists(f)]
        if missing:
            print(f"warning: sample files not found: {missing}")
    else:
        files = sorted(glob.glob("**/*.html", recursive=True))

    rep = Report()
    for f in files:
        check_file(f, rep)

    print(f"\nvalidate-jsonld: {rep.files} files with JSON-LD "
          f"({'sample' if args.sample else 'full site'})\n")

    print("schema types present:")
    for t in PRESERVE:
        print(f"  {t:16} {rep.counts.get(t, 0)}")
    print()

    total = 0
    for rule in sorted(rep.failures):
        hits = rep.failures[rule]
        total += len(hits)
        print(f"  [✗] {rule}: {len(hits)}")
        shown = hits if args.verbose else hits[:5]
        for h in shown:
            print(f"        {h}")
        if len(hits) > len(shown):
            print(f"        … {len(hits) - len(shown)} more (-v to list)")

    if not total:
        print("  [✓] all structured-data rules pass")
    print(f"\nSummary: {total} violations across {len(rep.failures)} rules\n")
    return 1 if total else 0


if __name__ == "__main__":
    sys.exit(main())
