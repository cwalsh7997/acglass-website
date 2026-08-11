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
import hashlib
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

# Exact fingerprints for conflicts on pages that cannot be changed in this
# release. A changed value or a new conflict does not match and fails the gate.
HELD_ID_PROPERTY_CONFLICTS = {
    ("city-of-haines-emergency.html", ORG_ID, "telephone"):
        "a1c0b3aec993a9f1e18e952877a6b76705ba06f8d3f80b4a775eae96f40cded7",
    (
        "commercial-glazing-west-palm-beach.html",
        "https://acglass.com/#localbusiness-west-palm-beach",
        "areaServed",
    ): "dba01b48a24c90835637404d3f387a6bdb46c87dee7edc5f89864d2389d9e309",
    (
        "commercial-glazing-west-palm-beach.html",
        "https://acglass.com/#localbusiness-west-palm-beach",
        "description",
    ): "412e9a33f010afec6818e346653e6422d02441d10bad02d12a3a32feb04365b6",
    ("commercial-glazing-tennessee.html", ORG_ID, "alternateName"):
        "eab0e8ce472b4e1932ab93c02743f9dbe474468a21f78ba6208e51231310590e",
    (
        "eswindows-installer-west-palm-beach.html",
        "https://acglass.com/#localbusiness-west-palm-beach",
        "areaServed",
    ): "917108252c623543459178ad3f26b4451386330d55159ed28253ff551c42b184",
    (
        "eswindows-installer-west-palm-beach.html",
        "https://acglass.com/#localbusiness-west-palm-beach",
        "email",
    ): "28a3e6d1f0fd2272228f90d1709c1f9e4abdc05df275956b7ea995c16ffab5a0",
    (
        "eswindows-installer-west-palm-beach.html",
        "https://acglass.com/#localbusiness-west-palm-beach",
        "telephone",
    ): "e6fa53a105eff9e83b7739733c0aa01700f1cc65db2e43ac4ff1d5564dcc22a6",
    ("ocean-prime-ft-lauderdale.html", ORG_ID, "description"):
        "daa291f744019d386f7ce92b33dc5b5613b7888f9cd0e63703cf151dac0500ca",
    ("ocean-prime-ft-lauderdale.html", ORG_ID, "telephone"):
        "a1c0b3aec993a9f1e18e952877a6b76705ba06f8d3f80b4a775eae96f40cded7",
    ("panther-national-clubhouse.html", ORG_ID, "telephone"):
        "5d8f8eab734517871390ff6aea53b4d08c948bc1d11eeff782a29d8d31f8300e",
}

# Exact fingerprints for legacy Place nodes with coordinates on pages held out
# of this release. Editable pages must not publish Place coordinates without a
# cited source. Any changed node, new page, or stale exception fails the gate.
HELD_PLACE_GEO_HASHES = {
    "brentwood-tn/index.html": (
        "099321b42b880409e643cc8912e620635f8c7b7eef5c534e78fdd60d552505bd",
    ),
    "brentwood-tn/maryland-farms-brentwood/index.html": (
        "901a4bd05c75bd209bb89550a088d86dd5596f5d9a0d79b17118eec9d070ff6a",
    ),
    "chattanooga/downtown-chattanooga/index.html": (
        "3d97f91aed844d98a0a5ebb0754cb35e5b268bdd7244025c568d5191b6d1a37a",
    ),
    "chattanooga/index.html": (
        "d232ee0c49a767d009542a5586957d77147558b0d215ad9b70c370e4830060e2",
    ),
    "city-of-haines-emergency.html": (
        "602cdb1ee85d0e2057176413f1dc9dfc9352f74d3a5d855fa618eb9f5d5add89",
        "d8af7802035eb2b99628790016146ddfa2097814e690f2dd820a5c1a71eb03dc",
    ),
    "commercial-glazier-near-me-west-palm-beach/index.html": (
        "7a7110dfa87efbe1f05fb0040a1c2ff069045beacd30ffb1bdfe84f0ede529b4",
    ),
    "commercial-glazing-tennessee.html": (
        "58745bdd60bacead2257132d71db208cdcec9bae306828be8ef862656fecf9e1",
        "65e3bca55dfe20ecdfbf642749697e49469bbf738bda08d635ea7f08afc6ea89",
    ),
    "commercial-glazing-west-palm-beach.html": (
        "7a7110dfa87efbe1f05fb0040a1c2ff069045beacd30ffb1bdfe84f0ede529b4",
        "a906bcbae144a79dcc0c2f0eca71401a923d886f854338e68827eb28900e4e7d",
    ),
    "franklin-tn/cool-springs-franklin/index.html": (
        "e2314f9b246b1a0841bfe2d8f5bf719ff7070f091bc1a2bd6d9392548cf93bf0",
    ),
    "franklin-tn/downtown-franklin/index.html": (
        "c100a1e727235adcf59a5688471cfde5f3f58784cfd0ee1e5044ae4fa8efc40f",
    ),
    "franklin-tn/index.html": (
        "84b126dd66b8fde984be7229f0bedc37fa0ad35d63b2617d9fc0c5581364a6c6",
    ),
    "knoxville/downtown-knoxville/index.html": (
        "53be82e5d03fdbd9a821041a9baf0841af8d3f856024504b22beb11058cc1eac",
    ),
    "knoxville/index.html": (
        "c34b9747346b8c09780e9b08e4d5e1f9d3c6da6a55f4deb5b57a6b57ef8b1ef1",
    ),
    "knoxville/turkey-creek-knoxville/index.html": (
        "49d5cffd12d8354e407f6cb3364c94b11e8b219e4ea6692df772c2cd1da196fa",
    ),
    "memphis/downtown-memphis/index.html": (
        "bda1c082e6e0005f504b139d26a853c26308fb0b00e6c1e14a68df7eb422f261",
    ),
    "memphis/east-memphis-poplar/index.html": (
        "716e4978cc9e4b1e285c93828eeab659f003386f8b068da3ef4a9ad20fb105b7",
    ),
    "memphis/index.html": (
        "b2c39edfdc78f1bcd3ff3acc7ec928ab089d72c64381640250b7eaa134128745",
    ),
    "murfreesboro-tn/index.html": (
        "7c70b6842b4adfe080de44245e9f6dd09e086d58aec9b18b6c565ed6468454fd",
    ),
    "nashville/east-nashville/index.html": (
        "db1867f1f8b11de68f4d92eb8490679169885eed11a7abeb6950aade24cd98c1",
    ),
    "nashville/index.html": (
        "cdeb6130d596f602776269826dc3054818b687ed1242db6ef580e80ab5184d5e",
    ),
    "nashville/sobro-nashville/index.html": (
        "d661465ed1a9fb5b673d0336a2fee42f3b0de11dd667934e2de26197d2ab14b1",
    ),
    "nashville/the-gulch-nashville/index.html": (
        "6eb0c6551f509e2a459782585e06772dcaddddcc9cf7ca9c04686febf2df128b",
    ),
    "ocean-prime-ft-lauderdale.html": (
        "25551ef21c950f8a9f33ff37175ad6730072e93dafbce36441b67f4371f8ac7f",
        "350628098ae7abb828ea0360ce763984905abfc9d45d535c68795366c3292bb6",
    ),
    "panther-national-clubhouse.html": (
        "362ebad2cd210b356dd063b5b16d910d2371d8f1e8a7a98c51583bf2c401c87a",
        "5cbf7ecfbbe9bb4cdbd67636374dfc5fb7cee333d73db080aecf4c4a29cc2e49",
        "8c9abfbd45853639a94d50aac12ec0c6e371dce8cd480b65672a08cf347333ea",
    ),
    "tennessee/index.html": (
        "3e444c1cd7d3188dc1a919ccd47d1402daea48e9686f681f74deb8bdbeb412b7",
    ),
    "west-palm-beach/clematis-street-west-palm-beach/index.html": (
        "44ec9488219f6c1bf840490e86a342d86dadd3db31f772a517f2b37619290d4a",
        "eb79d533e77a5be21c4cbb47b19f3d0eac9c4566a13d871877359707ddbbccba",
    ),
    "west-palm-beach/rosemary-square-west-palm-beach/index.html": (
        "a80b50ff47c7ee5f39e36cdb7b103b516e9181ddb3b21e0fe250c81289e2dfe0",
        "f326301a6af2b4aa2824f04d82be8563062a18215b5e9875443e65a7fa6db562",
    ),
}

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
        self.held_id_property_conflicts: list[str] = []
        self.held_id_property_conflict_keys: set[tuple[str, str, str]] = set()
        self.held_place_geo_paths: set[str] = set()

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


def conflicting_id_property_values(
    parsed: list,
) -> list[tuple[str, str, tuple[str, ...]]]:
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
        (nid, prop, tuple(sorted(asserted)))
        for nid, properties in values.items()
        for prop, asserted in properties.items()
        if len(asserted) > 1
    )


def conflicting_id_properties(parsed: list) -> list[tuple[str, str]]:
    """Return the public pair shape retained for focused unit tests."""
    return [
        (nid, prop)
        for nid, prop, _values in conflicting_id_property_values(parsed)
    ]


def stale_held_conflicts(
    observed: set[tuple[str, str, str]],
) -> list[tuple[str, str, str]]:
    return sorted(set(HELD_ID_PROPERTY_CONFLICTS) - observed)


def place_geo_fingerprints(parsed: list) -> tuple[str, ...]:
    fingerprints = []
    for data in parsed:
        for node in iter_nodes(data):
            if "Place" not in typelist(node) or "geo" not in node:
                continue
            canonical = json.dumps(node, sort_keys=True, separators=(",", ":"))
            fingerprints.append(hashlib.sha256(canonical.encode()).hexdigest())
    return tuple(sorted(fingerprints))


def stale_held_place_geo(observed: set[str]) -> list[str]:
    return sorted(set(HELD_PLACE_GEO_HASHES) - observed)


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

    for nid, prop, values in conflicting_id_property_values(parsed):
        where = f"{path}: {nid} [{prop}]"
        fingerprint = hashlib.sha256("\n".join(values).encode()).hexdigest()
        if HELD_ID_PROPERTY_CONFLICTS.get((path, nid, prop)) == fingerprint:
            rep.held_id_property_conflicts.append(where)
            rep.held_id_property_conflict_keys.add((path, nid, prop))
        else:
            rep.fail("id_property_conflict", where)

    place_geo = place_geo_fingerprints(parsed)
    if place_geo:
        if HELD_PLACE_GEO_HASHES.get(path) == place_geo:
            rep.held_place_geo_paths.add(path)
        else:
            rep.fail("unsourced_place_geo", f"{path}: {len(place_geo)} node(s)")

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
    if not args.sample:
        stale = stale_held_conflicts(rep.held_id_property_conflict_keys)
        for path, nid, prop in stale:
            rep.fail(
                "stale_held_id_property_conflict",
                f"{path}: {nid} [{prop}]",
            )
        for path in stale_held_place_geo(rep.held_place_geo_paths):
            rep.fail("stale_held_place_geo", path)

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
    if rep.held_id_property_conflicts:
        print(
            "  [✓] held id_property_conflict baseline: "
            f"{len(rep.held_id_property_conflicts)} exact conflict(s)"
        )
    if rep.held_place_geo_paths:
        print(
            "  [✓] held Place geo baseline: "
            f"{len(rep.held_place_geo_paths)} exact page(s)"
        )
    print(f"\nSummary: {total} violations across {len(rep.failures)} rules\n")
    return 1 if total else 0


if __name__ == "__main__":
    sys.exit(main())
