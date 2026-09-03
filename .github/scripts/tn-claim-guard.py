#!/usr/bin/env python3
"""
tn-claim-guard.py - offline claim-integrity guard for the Tennessee pages.

Runs against the repo working tree (no HTTP), so it fails *before* deploy  - 
unlike seo-verify.py, which only sees what is already live.

It guards three things that regressed once already because the TN pages were
generated from the Florida templates:

  1. Florida location leakage in TN metadata - ", FL" state tokens, plus the
     Florida-only regulatory constructs (HVHZ, Miami-Dade, NOA) used as if they
     were Tennessee proof.
  2. Staffed-office language ("Nashville HQ", "Tennessee headquarters") that
     implies a Tennessee office that does not exist yet.
  3. Structured data asserting a Tennessee street address, Tennessee
     coordinates, or a Tennessee LocalBusiness node.
  4. Delivery-complete Tennessee claims *anywhere on the site*, not just on TN
     pages. This includes an office count of four, an "Offices FL + TN" label,
     or a delivery verb applied to "Florida and Tennessee" as one present-tense
     territory. Planned-market language is not a truth qualifier.

What it deliberately does NOT flag:
  - The West Palm Beach NAP in the footer of every page. That address is real
    and belongs on TN pages.
  - Body copy that contrasts Florida and Tennessee. This bounded guard does not
    establish whether those statements are true. Technical and market claims
    require independent primary-source review.

Usage:
  python .github/scripts/tn-claim-guard.py            # exit 1 on any violation
  python .github/scripts/tn-claim-guard.py --list     # print discovered TN pages
"""

from __future__ import annotations

import argparse
import hashlib
import html as html_lib
import json
import os
import re
import sys
from html.parser import HTMLParser

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CLAIM_GUARD_ALLOWLIST_PATH = os.path.join(SCRIPT_DIR, "claim-guard-allowlist.json")

SKIP_DIRS = {".git", ".github", "_internal", "node_modules", "fonts", "images", "css", "js"}
CSS_SCAN_SKIP_DIRS = {".git", "_internal", "node_modules"}
REFERENCE_INVENTORY_PATH = os.path.join(
    REPO_ROOT, ".github", "tn-reference-inventory.json"
)

REFERENCE_GROUPS = (
    "path_or_title_discovery",
    "stale_operating_claim_hold",
    "mixed_claim_review",
    "biography_only",
    "technical_or_market_review",
    "license_disclaimer_link_review",
    "source_controlled_project_claim",
    "outside_edge_redirect_source",
)

REFERENCE_GROUP_MEMBERSHIP_SHA256 = {
    "path_or_title_discovery":
        "f61df174a5b1d602577b0457f4a53ae0f8344dd12af0d23ec24b1ed2c6ff37ae",
    "stale_operating_claim_hold":
        "613a78852fe91ee88143740bb72d6e9b313b299a64d2ee1760cb6090284e6ac4",
    "mixed_claim_review":
        "875c20e4a22f237694248ad5101fada3ebd82d263f695f643435bd73e59d8798",
    "biography_only":
        "6d3e95e04f8be403007daf48ddae2078c3c3628277bf6875801cc90e70f818af",
    "technical_or_market_review":
        "e398c6c6583e0dbba6a3125480a233828b59b4d74cf38615eba8ffbfcf72deab",
    "license_disclaimer_link_review":
        "aefebeb2566e5501b8e12bb30fb8c8bc5a1e0027c1e69ccd362087260ded5fdd",
    "source_controlled_project_claim":
        "93adb24c5b616a2cb68ef72cf972f080b4180c009a76565266eae672e068617a",
    "outside_edge_redirect_source":
        "051074a1d5c5f5a1623e45f1e8b9c263b4fc5e99f41eb970b1ce4fadb3ed1fa9",
}

EXCLUDED_FRAGMENT_SURFACE_SHA256 = {
    "services-schema-block.html":
        "bd6a8c8529390709d2be18fb3dab88068854021077bdfaa5ab70e0a9d45ec5d2",
}

TN_CONTENT_TOKEN = re.compile(
    r"(?<![A-Za-z0-9])(?:Tennessee|Nashville|TN)(?![A-Za-z0-9])",
    re.IGNORECASE,
)
HTML_DOCUMENT_MARKER = re.compile(
    r"<!doctype\s+html|<html\b|<head\b|<body\b",
    re.IGNORECASE,
)

STALE_OPERATING_CLAIM_PAGES = (
    "acg-vs-giroux-glass.html",
    "acg-vs-harmon.html",
    "acg-vs-permasteelisa.html",
    "ask.html",
    "best-glazing-subcontractor-florida.html",
    "best-storefront-contractor-florida.html",
    "blog/florida-commercial-construction-2026-outlook.html",
    "commercial-storefront-installer-florida.html",
    "facts.html",
    "glass-canopies-commercial.html",
    "glazing-subcontractor-vs-general-contractor.html",
    "industries.html",
    "locations.html",
    "miami-hvhz-glazing-contractor.html",
    "restaurant-glazing-contractor.html",
    "security-window-film-retrofit.html",
    "service-areas-map/index.html",
)

STALE_OPERATING_CLAIM_ASSETS = (
    "images/acg-coverage-map.svg",
)

ALLOWED_NEUTRAL_TN_REFERENCES = {
    "facts.html": (
        "Concrete Industry Management graduate, Middle Tennessee State University.",
    ),
    "locations.html": (
        "Southeast Florida",
    ),
}

STALE_OPERATING_LANGUAGE = re.compile(
    r"\bNashville\b|\bTennessee\b|\bTN\b|\bSoutheast(?:ern)?\b|\bQ3\s+2026\b",
    re.IGNORECASE,
)

TN_CITIES = (
    "nashville", "knoxville", "memphis", "chattanooga", "franklin", "brentwood",
    "murfreesboro", "clarksville", "hendersonville", "gallatin", "lebanon",
    "smyrna", "columbia", "goodlettsville", "la-vergne", "mt-juliet",
    "spring-hill", "cool-springs",
)

# A page is Tennessee-scoped if the path says so, or the <title> does.
TN_PATH = re.compile(
    r"(^|/)(tennessee|nashville|knoxville|memphis|chattanooga)(/|-|\.|$)"
    r"|-tn(/|-|\.|$)|-tennessee(/|-|\.|$)|(^|/)(" + "|".join(TN_CITIES) + r")-tn",
    re.IGNORECASE,
)
TN_TITLE = re.compile(r"\bTennessee\b|,\s*TN\b|\bTN\s*\|", re.IGNORECASE)

# ", FL" as a state token, and the Florida-only regulatory vocabulary.
FL_STATE = re.compile(r",\s*FL\b|\bFL\s*\|")
FL_REGULATORY = re.compile(r"\bHVHZ\b|\bMiami-Dade\b|\bNOA\b")

# Naming Florida explicitly is the difference between leakage and an honest
# transferable-experience claim: "HVHZ-ready systems in Nashville" is leakage,
# "why Florida HVHZ experience translates to Tennessee" is the thesis of the
# page. Attributed mentions are dropped before the leakage scan.
FL_ATTRIBUTED = re.compile(
    r"Florida(?:'s)?\s+(?:HVHZ|Miami-Dade(?:\s+NOA)?|NOA)"
    r"|no\s+(?:HVHZ|Miami-Dade\s+NOA)",
    re.IGNORECASE,
)

META_FIELDS = (
    ("description", False),
    ("og:title", True),
    ("og:description", True),
    ("twitter:title", False),
    ("twitter:description", False),
)

HQ_LANGUAGE = re.compile(
    r"Nashville\s+HQ"
    r"|Tennessee\s+HQ"
    r"|TN\s+HQ"
    r"|(?:Nashville|Tennessee)\s+headquarters"
    r"|headquartered\s+in\s+(?:Nashville|Tennessee)"
    r"|our\s+Nashville\s+(?:shop|showroom|warehouse|yard|facility)",
    re.IGNORECASE,
)

# Tennessee bounding box, padded. West Palm Beach (26.71, -80.06) is outside it.
TN_LAT = (34.6, 37.0)
TN_LON = (-90.8, -81.3)

# --- delivery-complete Tennessee claims (site-wide) ------------------------
#
# Scanned on every page, not just the TN ones: the claim leaked into
# industries.html, capabilities.html and llms.txt, none of which is TN-scoped,
# so the TN_PATH/TN_TITLE discovery pass never saw them.

OFFICE_COUNT = re.compile(
    r"\b(?:four|4)\s+offices\b"
    r"|\b(?:fourth|4th)\s+office\b"
    r"|\boffice\s+(?:number\s+)?(?:four|4)\b"
    r"|\bOffices?\b(?:\s|&middot;|&nbsp;|·|\|){0,4}(?:FL|Florida)\s*(?:\+|and|&amp;|&)\s*(?:TN|Tennessee)\b",
    re.IGNORECASE,
)

# A verb that puts ACG in both states *now*, close in front of the pair.
DELIVERY_PAIR = re.compile(
    r"\b(?:serves?|serving|installs?|installing|installation|delivers?|delivering"
    r"|operates?|operating|covers?|covering|services|active)\b"
    r"[^.!?]{0,140}?"
    r"\bFlorida\s*(?:and|&amp;|&|/)\s*Tennessee\b",
    re.IGNORECASE,
)

QUALIFIER_BEFORE = 200
QUALIFIER_AFTER = 460

# The delivery regex masks titles. The separate reference inventory still
# classifies and fingerprints every Tennessee title.
TITLE_TAGS = re.compile(
    r"<title>.*?</title>"
    r"|<meta[^>]+(?:name|property)\s*=\s*\"(?:og:title|twitter:title)\"[^>]*>",
    re.DOTALL | re.IGNORECASE,
)

# --- prohibited public positioning (site-wide, all metadata surfaces) ------
#
# These claims are prohibited on *every* HTML surface - <title>, <meta>,
# <meta og:*/twitter:*>, JSON-LD strings, inline <script> literals, and body
# text - because they are load-bearing marketing claims that must not appear
# anywhere the crawler or a user can see them, indexable or not.
#
# On indexable pages any match is a hard fail. On noindex pages (see
# has_noindex_directive) the Nashville/TN office-opening match downgrades to a
# warning so it stays visible while other cleanup PRs run.

# Regex A: AI-augmented positioning is prohibited outright.
AI_AUGMENTED_RE = re.compile(r"\bAI[-\s]?augmented\b", re.IGNORECASE)

# Regex B: WBE / WBENC / woman-owned "certified" without an "in progress",
# "pending", or "filed" qualifier inside the following 60 characters.
WBE_CERTIFIED_RE = re.compile(
    r"(?:WBENC|WBE|woman[-\s]?owned)\s+certified(?![^.]{0,60}(?:pending|in\s+progress|filed))",
    re.IGNORECASE,
)

# Regex C: first-party manufacturer-authorization claims, any noun.
#
# The original version matched the literal word "dealer" only. The site never
# used it: it said "authorized installer", "authorized partner", bare
# "Authorized" card labels and "Manufacturer-authorized only", so roughly 90
# files carried an undocumentable authorization claim and still passed green.
# The rule is now noun-agnostic (installer / dealer / distributor / partner /
# reseller / fabricator), and also covers bare "Authorized" labels and the
# hyphenated "manufacturer-authorized" adjective.
#
# Editorial / third-party phrasing must still pass, and the separation is
# structural rather than allowlist-based wherever possible:
#
#   - C2 requires a first-party SUBJECT (ACG / American Commercial Glass / we /
#     our / its) inside a short window in front of the authorized-noun phrase,
#     so generic advice keeps working: "which manufacturers they are authorized
#     dealers for", "authorized dealers get direct technical support", "most
#     premium systems require authorized-installer status", "a firm that is
#     authorized on ES-50", "non-authorized contractors".
#   - The change-order sense ("priced and authorized before it proceeds") is
#     excluded explicitly - it is a permission to proceed, not a manufacturer
#     grant.
#   - "manufacturer authorization" as a noun ("ask for manufacturer
#     authorization letters") is deliberately NOT matched; only the first-party
#     adjective form "manufacturer-authorized" is.
#
# The block-hash allowlist (authorized_dealer_editorial) still applies to every
# match, unchanged, for editorial blocks the structure cannot separate.

# Nouns that turn "authorized" into a claimed manufacturer relationship.
AUTH_RELATIONSHIP_NOUN = (
    r"(?:installer|dealer|distributor|partner|reseller|fabricator)s?"
)

# First-person / ACG subject. Mirrors TN_E_ACG_SUBJECT but adds the possessive
# "its", which the storefront pages use ("its seven authorized manufacturer
# partners"). "they", "their" and bare "a firm" are deliberately absent: those
# are the editorial voices.
AUTH_ACG_SUBJECT = (
    r"(?:ACG(?:'s|&#(?:39|x27);s|&rsquo;s)?"
    r"|American\s+Commercial\s+Glass(?:'s|&#(?:39|x27);s|&rsquo;s)?"
    r"|we(?:'re|&#(?:39|x27);re|&rsquo;re|\s+are)?"
    r"|our|its)"
)

# "authorized <up to three intervening words> <noun>", hyphen or space joined.
# The intervening words cover "authorized commercial Euro-Wall installer",
# "authorized manufacturer partners", "authorized-installer".
AUTH_NOUN_PHRASE = (
    r"authorized[-\s](?:[A-Za-z][A-Za-z&;.-]*[-\s]){0,3}?" + AUTH_RELATIONSHIP_NOUN + r"\b"
)

# The change-order sense of "authorized" - never a manufacturer claim.
AUTH_CHANGE_ORDER = r"authorized\s+before\s+it\s+proceeds"

AUTHORIZED_DEALER_RE = re.compile(
    # C1 - the original literal dealer patterns, unchanged.
    r"Authorized\s+Dealer\s+[Ff]or\b"                          # "Authorized Dealer For|for" (heading)
    r"|\bauthorized\s+dealer\s+for\s+(?=[A-Z\"\d])"            # "authorized dealer for <Manufacturer>"
    r"|\bwe\s+are\s+an\s+authorized\s+dealer\b"
    r"|\bACG\s+is\s+(?:an\s+)?authorized\s+dealer\b"
    # C2 - first-party subject bound to an authorized-<noun> phrase, either
    #      "ACG is an authorized Euro-Wall installer" or "our authorized
    #      manufacturer partners". Sentence-bounded so the subject has to
    #      actually govern the claim.
    rf"|\b{AUTH_ACG_SUBJECT}\b[^<.!?]{{0,60}}?\b{AUTH_NOUN_PHRASE}"
    # C4 - the hyphenated first-party adjective.
    r"|\bmanufacturer-authorized\b",
    re.IGNORECASE,
)

# Case-SENSITIVE companion rules. These must not run under re.IGNORECASE:
# both depend on a capital letter to tell a first-party claim from editorial
# prose ("is an authorized Euro-Wall installer" vs "which manufacturers they
# are authorized dealers for"; a "Authorized" card label vs the word used
# mid-sentence).
AUTHORIZED_LABEL_RE = re.compile(
    # C3 - "is/are/as an authorized <Manufacturer>". The capitalized token after
    #      the grant is what makes it a named-manufacturer claim. The
    #      change-order sense is excluded explicitly.
    rf"\b(?:[Ii]s|[Aa]re|[Aa]s)\s+(?:an?\s+|the\s+)?authorized\s+(?!{AUTH_CHANGE_ORDER})(?=[A-Z])"
    # C5 - bare "Authorized" used as a label, heading or card value.
    r"|>\s*Authorized[.:;!]?\s*<"
    r"|>\s*Authorized\s+[A-Z][^<]{0,60}<"
)

# A disclaimer is the opposite of a claim. "ACG does not hold authorized-installer
# status for those brands" and "we do not claim authorized-dealer status" are the
# governed *denials* the site is supposed to carry, so a negation immediately in
# front of the grant word suppresses rules C2/C3. The window is short and must
# stay inside the sentence, so "we are an authorized installer. We do not ..."
# cannot launder a real claim.
AUTH_NEGATION_RE = re.compile(
    r"\b(?:not|never|no|without|cannot|can\s*not|don't|doesn't|do\s+not|does\s+not)\b"
    r"[^.!?<]{0,30}$",
    re.IGNORECASE,
)


def _is_negated_authorization(html: str, match: re.Match) -> bool:
    """True when the matched grant word is inside an explicit denial.

    The negation is measured from the grant word itself, not from the start of
    the match: rule C2 starts at the ACG subject, so "ACG does not hold
    authorized-installer status" only reads as a denial when the window is
    anchored on "authorized".
    """
    text = match.group(0)
    offset = text.lower().find("authoriz")
    grant_start = match.start() + (offset if offset >= 0 else 0)
    window = html[max(0, grant_start - 60):grant_start]
    return bool(AUTH_NEGATION_RE.search(window))


# Regex D: "completed federal" / delivered / installed / awarded federal work.
COMPLETED_FEDERAL_RE = re.compile(
    r"\b(?:completed|delivered|installed|awarded)\s+(?:federal|GSA|VA|DoD|USACE)\b",
    re.IGNORECASE,
)

# Regex E: Nashville / Tennessee office-opening claim in ANY surface.
#
# The first version of this regex allowed a *bare* "expansion" alternative
# anywhere within 80 characters of a Tennessee place name. "expansion" on its
# own is not an ACG claim, so that produced two false positives:
#
#   1. "Nashville's BNA airport expansion is a regional example of the demand"
#      (acoustic-glazing-stc-oitc-commercial.html) - the AIRPORT is expanding.
#   2. "Restaurant, hotel, office, medical, and Tennessee expansion
#      observations." (blog/index.html) - market-observation framing in a blog
#      card description, not a first-party ACG claim.
#
# Both are third-party / market-observation uses. The fix is structural, not an
# allowlist entry: an expansion term is only a prohibited claim when it is bound
# to a first-person / ACG SUBJECT inside a short window (E3), or when the
# language is inherently first-party directional (E4), or when it sits next to
# an office/location OPENING term (E1/E2). Any of those still fails; a bare
# "<something> expansion" no longer does.

# Tennessee place tokens Regex E cares about.
TN_E_PLACE = r"(?:nashville|tennessee)"

# First-person / ACG subject. Deliberately does NOT include "us", which shows
# up in unrelated CTA copy ("contact us") close enough to market prose to
# reintroduce the false-positive class we are removing here.
TN_E_ACG_SUBJECT = (
    r"(?:ACG(?:'s|&#(?:39|x27);s)?"
    r"|American\s+Commercial\s+Glass(?:'s|&#(?:39|x27);s)?"
    r"|we(?:'re|&#(?:39|x27);re|\s+are|\s+will|\s+plan)?"
    r"|our)"
)

# Expansion terms. The negative lookahead keeps the governed withdrawal
# language ("expansion evaluated / off the table / not active") visible on the
# page without tripping the guard, even when a subject is nearby.
TN_E_EXPANSION_TERM = (
    r"(?:expansion|expanding|expands|expand)"
    r"(?!\s+(?:evaluated|off\s+the\s+table|not\s+active))"
)

# Office / location opening terms. These are claims regardless of subject: an
# opening date for a place is only ever asserted by the party opening it.
TN_E_OPENING_TERM = (
    r"(?:office|location|branch|shop|facility|showroom)\s+"
    r"(?:opening|opens|open|launch|launching|launches|launched|coming)"
)
TN_E_OPENING_VERB = r"(?:new|opening|opens|open|launch|launching|launches|launched)"

TN_OFFICE_OPENING_RE = re.compile(
    # E1 - office/location opening tied to a TN place name, either order.
    rf"{TN_E_PLACE}[^<]{{0,80}}?{TN_E_OPENING_TERM}"
    rf"|{TN_E_OPENING_VERB}\s+[^<]{{0,40}}?{TN_E_PLACE}\s+"
    r"(?:office|location|branch|shop|facility|showroom)"
    # E2 - a dated opening near a TN place name ("opens Q3 2026").
    rf"|{TN_E_PLACE}[^<]{{0,80}}?(?:opens|opening|launches|launching)\s+"
    r"(?:in\s+)?(?:Q[1-4]|early|late|mid)"
    # E3 - an expansion term bound to an ACG / first-person subject, either
    #      "ACG is expanding into Tennessee" or "our Tennessee expansion".
    rf"|\b{TN_E_ACG_SUBJECT}\b[^<]{{0,60}}?{TN_E_EXPANSION_TERM}[^<]{{0,40}}?{TN_E_PLACE}"
    rf"|\b{TN_E_ACG_SUBJECT}\b[^<]{{0,40}}?{TN_E_PLACE}[^<]{{0,25}}?{TN_E_EXPANSION_TERM}"
    # E4 - inherently first-party directional language; no subject required
    #      because only the mover can be "expanding to" or "coming to" a market.
    rf"|expand(?:ing|s|ed)?\s+(?:in)?to\s+(?:the\s+)?{TN_E_PLACE}"
    rf"|coming\s+(?:soon\s+)?to\s+{TN_E_PLACE}",
    re.IGNORECASE,
)

# Robots-meta noindex detection. Any of: <meta name="robots" content="...noindex...">,
# <meta name="googlebot" content="...noindex...">, X-Robots-Tag http-equiv.
NOINDEX_META_RE = re.compile(
    r'<meta[^>]+(?:name|http-equiv)\s*=\s*"(?:robots|googlebot|x-robots-tag)"'
    r'[^>]*content\s*=\s*"[^"]*\bnoindex\b',
    re.IGNORECASE,
)


def has_noindex_directive(html: str) -> bool:
    return bool(NOINDEX_META_RE.search(html))


def load_claim_guard_allowlist(path: str = CLAIM_GUARD_ALLOWLIST_PATH):
    """Load the block-hash allowlist. Missing file = empty allowlist.

    Schema:
      { "schema_version": 1,
        "authorized_dealer_editorial": {
            "<relpath>": ["<sha256 of exact HTML block>", ...] } }

    Only exact block hashes are honored - no line-number allowances - so any
    edit to a whitelisted block silently invalidates the exemption and re-fails
    the guard.
    """
    if not os.path.exists(path):
        return {"authorized_dealer_editorial": {}}
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def _iter_positioning_matches(rx, html):
    """Yield (match, snippet) for every regex hit, deduped by (start, group)."""
    seen = set()
    for m in rx.finditer(html):
        key = (m.start(), m.group(0).lower())
        if key in seen:
            continue
        seen.add(key)
        start = max(0, m.start() - 80)
        end = min(len(html), m.end() + 80)
        snippet = re.sub(r"\s+", " ", html[start:end]).strip()
        yield m, snippet


def _authorized_dealer_block_hash(html: str, match: re.Match[str]) -> str:
    """Hash of the enclosing paragraph/heading block for the allowlist."""
    # Walk out to the nearest surrounding block-level open tag on the left and
    # its closing counterpart on the right; fall back to a 400-char window.
    left = html.rfind("<", max(0, match.start() - 2000), match.start())
    right = html.find(">", match.end(), match.end() + 2000)
    if left < 0:
        left = max(0, match.start() - 200)
    if right < 0:
        right = min(len(html), match.end() + 200)
    block = html[left : right + 1]
    normalized = re.sub(r"\s+", " ", block).strip()
    return hashlib.sha256(normalized.encode("utf-8")).hexdigest()


def check_prohibited_public_positioning(
    rel: str,
    html: str,
    fail,
    warn=None,
    allowlist=None,
):
    """Scan the WHOLE HTML file (title, meta, og/twitter, JSON-LD strings,
    inline <script> literals, body) for prohibited public positioning claims.

    Regex E (TN office opening) FAILS on indexable pages and WARNS on
    noindex pages so cleanup PRs can address them separately.
    """
    allowlist = allowlist or {"authorized_dealer_editorial": {}}
    dealer_allow = set(
        allowlist.get("authorized_dealer_editorial", {}).get(rel, [])
    )
    is_indexable = not has_noindex_directive(html)

    # A - AI-augmented positioning
    for _, snippet in _iter_positioning_matches(AI_AUGMENTED_RE, html):
        fail(rel, f"prohibited 'AI-augmented' positioning: …{snippet}…")

    # B - WBE / WBENC / woman-owned "certified" without in-progress qualifier
    for _, snippet in _iter_positioning_matches(WBE_CERTIFIED_RE, html):
        fail(
            rel,
            "prohibited 'WBE certified' claim without an in-progress "
            f"qualifier (pending/in progress/filed within 60 chars): …{snippet}…",
        )

    # C - first-party authorization claim, any noun (editorial mentions are
    #     fine). Two regexes: the case-insensitive rules and the case-sensitive
    #     label / named-manufacturer rules. Both share the block-hash allowlist.
    seen_c = set()
    for rx in (AUTHORIZED_DEALER_RE, AUTHORIZED_LABEL_RE):
        for m, snippet in _iter_positioning_matches(rx, html):
            block_hash = _authorized_dealer_block_hash(html, m)
            if block_hash in dealer_allow:
                continue
            if _is_negated_authorization(html, m):
                continue
            key = (m.start(), block_hash)
            if key in seen_c:
                continue
            seen_c.add(key)
            fail(
                rel,
                f"prohibited first-party manufacturer-authorization claim "
                f"('authorized dealer'/installer class) {m.group(0)!r} "
                f"(block hash {block_hash}) - ...{snippet}...",
            )

    # D - completed / delivered / installed / awarded federal work
    for _, snippet in _iter_positioning_matches(COMPLETED_FEDERAL_RE, html):
        fail(
            rel,
            f"prohibited completed-federal-work claim: …{snippet}…",
        )

    # E - Nashville / TN office-opening claim across ALL surfaces
    for _, snippet in _iter_positioning_matches(TN_OFFICE_OPENING_RE, html):
        message = (
            "prohibited Nashville/Tennessee office-opening claim on ANY surface "
            f"(title, meta, og/twitter, JSON-LD, script, body): …{snippet}…"
        )
        if is_indexable:
            fail(rel, message)
        elif warn is not None:
            warn(rel, message + " [noindex - warning only]")


# No held delivery claims remain. The prior exception covered an "ACG operates
# four offices across two states" line on projects/index.html, retained while
# the Tennessee office was a staged plan. That plan is withdrawn: Tennessee is a
# furnish-and-consulting market with no ACG office and no ACG field labor, so
# the claim was removed at the source rather than governed. Any future held
# claim must be added here with an exact normalized context fingerprint.
HELD_DELIVERY_CLAIMS: dict[tuple[str, str], str] = {}


def iter_html_files():
    for dirpath, dirnames, filenames in os.walk(REPO_ROOT):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS and not d.startswith(".")]
        for fn in filenames:
            if fn.endswith(".html"):
                full = os.path.join(dirpath, fn)
                yield os.path.relpath(full, REPO_ROOT).replace(os.sep, "/"), full


def iter_css_files():
    for dirpath, dirnames, filenames in os.walk(REPO_ROOT):
        dirnames[:] = [d for d in dirnames if d not in CSS_SCAN_SKIP_DIRS]
        for filename in filenames:
            if filename.endswith(".css"):
                full = os.path.join(dirpath, filename)
                yield os.path.relpath(full, REPO_ROOT).replace(os.sep, "/"), full


def extract_title(html: str) -> str:
    m = re.search(r"<title>(.*?)</title>", html, re.DOTALL | re.IGNORECASE)
    return re.sub(r"\s+", " ", m.group(1)).strip() if m else ""


def extract_meta(html: str, name: str, prop: bool) -> str | None:
    attr = "property" if prop else "name"
    m = re.search(
        rf'<meta[^>]+{attr}\s*=\s*"{re.escape(name)}"[^>]*\scontent\s*=\s*"([^"]*)"',
        html,
        re.IGNORECASE,
    )
    return m.group(1) if m else None


def extract_h1(html: str) -> str:
    m = re.search(r"<h1[^>]*>(.*?)</h1>", html, re.DOTALL | re.IGNORECASE)
    if not m:
        return ""
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", m.group(1))).strip()


def jsonld_blocks(html: str):
    return re.findall(
        r'<script[^>]+type\s*=\s*"application/ld\+json"[^>]*>(.*?)</script>',
        html,
        re.DOTALL | re.IGNORECASE,
    )


def is_tn_page(rel: str, html: str) -> bool:
    if TN_PATH.search(rel):
        return True
    return bool(TN_TITLE.search(extract_title(html)))


def javascript_string_literals(source: str):
    literals = []
    index = 0
    while index < len(source):
        if source[index] not in ("\"", "'", "`"):
            index += 1
            continue
        quote = source[index]
        start = index
        index += 1
        pieces = []
        while index < len(source):
            char = source[index]
            if char == quote:
                index += 1
                break
            if char == "\\" and index + 1 < len(source):
                pieces.extend((char, source[index + 1]))
                index += 2
                continue
            pieces.append(char)
            index += 1
        literals.append(
            (
                start,
                index,
                ReferenceSurfaceParser.decode_reference_text("".join(pieces)),
                quote,
            )
        )
    return literals


def javascript_template_expression_end(value: str, start: int) -> int | None:
    depth = 1
    quote = None
    escaped = False
    for index in range(start, len(value)):
        char = value[index]
        if escaped:
            escaped = False
            continue
        if char == "\\":
            escaped = True
            continue
        if quote:
            if char == quote:
                quote = None
            continue
        if char in ("\"", "'", "`"):
            quote = char
        elif char == "{":
            depth += 1
        elif char == "}":
            depth -= 1
            if depth == 0:
                return index
    return None


JS_STATIC_BINDING = re.compile(
    r"(?<![\w.$])(?:(?:const|let|var)\s+)?"
    r"([A-Za-z_$][A-Za-z0-9_$]*)\s*=\s*$"
)


def javascript_static_bindings(source: str, literals):
    bindings = {}
    for start, _, value, _ in literals:
        match = JS_STATIC_BINDING.search(source[max(0, start - 256):start])
        if match:
            bindings.setdefault(match.group(1), []).append(value)
    return bindings


def javascript_template_reference_values(value: str, bindings=None):
    bindings = bindings or {}
    option_groups = []
    position = 0
    while position < len(value):
        marker = value.find("${", position)
        if marker < 0:
            option_groups.append([value[position:]])
            break
        option_groups.append([value[position:marker]])
        end = javascript_template_expression_end(value, marker + 2)
        if end is None:
            option_groups.append([value[marker:]])
            break
        expression = value[marker + 2:end]
        options = list(bindings.get(expression.strip(), ()))
        options.extend(javascript_reference_values(expression, bindings))
        options = list(dict.fromkeys(options))
        option_groups.append(options or [""])
        position = end + 1

    if not option_groups:
        return
    variants = [""]
    for options in option_groups:
        variants = [
            prefix + option
            for prefix in variants
            for option in options
        ]
    yield from variants


def javascript_reference_values(source: str, bindings=None):
    literals = javascript_string_literals(source)
    if bindings is None:
        bindings = javascript_static_bindings(source, literals)
    for _, _, value, quote in literals:
        yield value
        if quote == "`":
            yield from javascript_template_reference_values(value, bindings)
    atoms = [(start, end, value) for start, end, value, _ in literals]
    for atom in javascript_character_code_atoms(source):
        atoms.append(atom)
        yield atom[2]
    atoms.sort()
    for position in range(len(atoms)):
        combined = atoms[position][2]
        for _, _, next_value in atoms[position + 1:position + 8]:
            combined += next_value
            if len(combined) > 64:
                break
            yield combined
    for position, (_, end, value, _) in enumerate(literals[:-1]):
        combined = value
        current_end = end
        joined = False
        for next_start, next_end, next_value, _ in literals[position + 1:]:
            if not re.fullmatch(r"\s*\+\s*", source[current_end:next_start]):
                break
            combined += next_value
            current_end = next_end
            joined = True
        if joined:
            yield combined


JS_CHARACTER_CODE_CALL = re.compile(
    r"(?:String\s*\.\s*)?from(?:CharCode|CodePoint)\s*\(([^()]*)\)"
)
JS_INTEGER_LITERAL = re.compile(r"(?:0[xX][0-9a-fA-F]+|[0-9]+)")


def javascript_character_code_atoms(source: str):
    for match in JS_CHARACTER_CODE_CALL.finditer(source):
        parts = [part.strip() for part in match.group(1).split(",")]
        if not parts or not all(JS_INTEGER_LITERAL.fullmatch(part) for part in parts):
            continue
        try:
            value = "".join(chr(int(part, 0)) for part in parts)
        except (ValueError, OverflowError):
            continue
        yield match.start(), match.end(), value


class ReferenceSurfaceParser(HTMLParser):
    BLOCK_TAGS = {
        "address",
        "article",
        "aside",
        "blockquote",
        "br",
        "div",
        "dl",
        "fieldset",
        "figcaption",
        "figure",
        "footer",
        "form",
        "h1",
        "h2",
        "h3",
        "h4",
        "h5",
        "h6",
        "header",
        "hr",
        "li",
        "main",
        "nav",
        "ol",
        "p",
        "pre",
        "script",
        "section",
        "table",
        "td",
        "th",
        "tr",
        "ul",
    }
    SEMANTIC_ATTRIBUTES = {
        "action",
        "alt",
        "aria-label",
        "content",
        "href",
        "hreflang",
        "http-equiv",
        "name",
        "placeholder",
        "property",
        "rel",
        "role",
        "src",
        "title",
        "type",
        "value",
    }

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.pieces = []
        self.token_parts = []
        self.style_depth = 0
        self.script_depth = 0
        self.css_sources = []
        self.css_finalized = False
        self.attribute_sets = []

    @staticmethod
    def decode_reference_text(value):
        decoded = html_lib.unescape(value)
        decoded = re.sub(
            r"\\u([0-9a-fA-F]{4})",
            lambda match: chr(int(match.group(1), 16)),
            decoded,
        )
        return re.sub(
            r"\\x([0-9a-fA-F]{2})",
            lambda match: chr(int(match.group(1), 16)),
            decoded,
        )

    def handle_starttag(self, tag, attrs):
        tag = tag.lower()
        if tag == "style":
            self.style_depth += 1
            return
        if self.style_depth:
            return
        if tag == "script":
            self.script_depth += 1
        if tag in self.BLOCK_TAGS:
            self.token_parts.append(" ")
        element_attributes = {}
        for name, value in attrs:
            if value is None:
                continue
            lowered = name.lower()
            element_attributes.setdefault(lowered, []).append(
                self.decode_reference_text(value)
            )
            if lowered == "style":
                self.add_css_content(value)
            decoded_style = decode_css_text(value) if lowered == "style" else ""
            if (
                lowered in self.SEMANTIC_ATTRIBUTES
                or lowered.startswith("aria-")
                or lowered.startswith("data-")
                or lowered.startswith("on")
                or TN_CONTENT_TOKEN.search(value)
                or TN_CONTENT_TOKEN.search(decoded_style)
            ):
                self.pieces.append(f"@{lowered}={value}")
                self.token_parts.append(
                    f" {self.decode_reference_text(value)} "
                )
                if lowered.startswith("on"):
                    for script_value in javascript_reference_values(value):
                        self.token_parts.append(f" {script_value} ")
        if element_attributes:
            self.attribute_sets.append(element_attributes)

    def add_css_content(self, css):
        self.css_sources.append(css)

    def finalize_css_content(self):
        if self.css_finalized:
            return
        self.css_finalized = True
        css = "\n".join(self.css_sources)
        seen = set()
        attribute_names = css_content_attribute_names(css)
        relevant_attribute_sets = [
            attributes
            for attributes in self.attribute_sets
            if set(attributes) & attribute_names
        ]
        for attributes in ({}, *relevant_attribute_sets):
            for value in css_reference_values(css, attributes):
                if value in seen:
                    continue
                seen.add(value)
                self.pieces.append(f"@css-content={value}")
                self.token_parts.append(f" {value} ")

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)

    def handle_endtag(self, tag):
        tag = tag.lower()
        if tag == "style" and self.style_depth:
            self.style_depth -= 1
            return
        if tag == "script" and self.script_depth:
            self.script_depth -= 1
        if not self.style_depth and tag in self.BLOCK_TAGS:
            self.token_parts.append(" ")

    def handle_data(self, data):
        if self.style_depth:
            self.add_css_content(data)
        elif data.strip():
            self.pieces.append(data)
            self.token_parts.append(self.decode_reference_text(data))
            if self.script_depth:
                for script_value in javascript_reference_values(data):
                    self.token_parts.append(f" {script_value} ")

    def token_text(self):
        self.finalize_css_content()
        return re.sub(r"\s+", " ", "".join(self.token_parts)).strip()


CSS_CONTENT_START = re.compile(r"(?<![-\w])content\s*:", re.IGNORECASE)
CSS_CUSTOM_PROPERTY_START = re.compile(
    r"(?<![-\w])(--[A-Za-z0-9_-]+)\s*:"
)
CSS_VAR_START = re.compile(r"var\(\s*(--[A-Za-z0-9_-]+)", re.IGNORECASE)
CSS_ATTR_START = re.compile(
    r"attr\(\s*([A-Za-z_:][-A-Za-z0-9_:.]*)",
    re.IGNORECASE,
)
CSS_COMMENT = re.compile(r"/\*.*?\*/", re.DOTALL)


def decode_css_text(value: str) -> str:
    decoded = html_lib.unescape(value)
    decoded = re.sub(r"\\(?:\r\n|[\n\r\f])", "", decoded)
    decoded = re.sub(
        r"\\([0-9a-fA-F]{1,6})(?:[ \t\r\n\f])?",
        lambda match: chr(int(match.group(1), 16)),
        decoded,
    )
    return re.sub(r"\\([^\n\r\f])", r"\1", decoded)


def css_declaration_value(source: str, start: int) -> str:
    quote = None
    escaped = False
    paren_depth = 0
    end = len(source)
    for index in range(start, len(source)):
        char = source[index]
        if escaped:
            escaped = False
            continue
        if char == "\\":
            escaped = True
            continue
        if quote:
            if char == quote:
                quote = None
            continue
        if char in ("\"", "'"):
            quote = char
        elif char == "(":
            paren_depth += 1
        elif char == ")" and paren_depth:
            paren_depth -= 1
        elif not paren_depth and char in (";", "}"):
            end = index
            break
    return source[start:end]


def css_content_declarations(css: str):
    source = CSS_COMMENT.sub("", css)
    for match in CSS_CONTENT_START.finditer(source):
        yield css_declaration_value(source, match.end())


def css_custom_properties(css: str):
    source = CSS_COMMENT.sub("", css)
    properties = {}
    for match in CSS_CUSTOM_PROPERTY_START.finditer(source):
        properties.setdefault(match.group(1), []).append(
            css_declaration_value(source, match.end())
        )
    return properties


def css_string_values(value: str):
    index = 0
    while index < len(value):
        if value[index] not in ("\"", "'"):
            index += 1
            continue
        quote = value[index]
        index += 1
        pieces = []
        while index < len(value):
            char = value[index]
            if char == quote:
                index += 1
                break
            if char == "\\" and index + 1 < len(value):
                pieces.extend((char, value[index + 1]))
                index += 2
                continue
            pieces.append(char)
            index += 1
        yield decode_css_text("".join(pieces))


def css_generated_variants(
    value: str,
    properties: dict,
    seen=frozenset(),
    attributes=None,
):
    option_groups = []
    index = 0
    while index < len(value):
        if value[index] in ("\"", "'"):
            quote = value[index]
            index += 1
            pieces = []
            while index < len(value):
                char = value[index]
                if char == quote:
                    index += 1
                    break
                if char == "\\" and index + 1 < len(value):
                    pieces.extend((char, value[index + 1]))
                    index += 2
                    continue
                pieces.append(char)
                index += 1
            option_groups.append([decode_css_text("".join(pieces))])
            continue
        match = CSS_VAR_START.match(value, index)
        if match:
            name = match.group(1)
            options = []
            if name not in seen:
                for declaration in properties.get(name, ()):
                    options.extend(
                        css_generated_variants(
                            declaration,
                            properties,
                            seen | {name},
                            attributes,
                        )
                    )
            if options:
                option_groups.append(list(dict.fromkeys(options)))
            index = match.end()
            continue
        match = CSS_ATTR_START.match(value, index)
        if match:
            options = (attributes or {}).get(match.group(1).lower(), ())
            if options:
                option_groups.append(list(dict.fromkeys(options)))
            index = match.end()
            continue
        index += 1

    if not option_groups:
        return []
    variants = [""]
    for options in option_groups:
        variants = [
            prefix + option
            for prefix in variants
            for option in options
        ]
    return variants


def css_generated_content_values(css: str, attributes=None):
    properties = css_custom_properties(css)
    for declaration in css_content_declarations(css):
        yield from css_generated_variants(
            declaration, properties, attributes=attributes
        )


def css_content_custom_property_names(css: str):
    properties = css_custom_properties(css)
    names = set()
    for declaration in css_content_declarations(css):
        names.update(
            match.group(1) for match in CSS_VAR_START.finditer(declaration)
        )
    pending = list(names)
    while pending:
        name = pending.pop()
        for declaration in properties.get(name, ()):
            for match in CSS_VAR_START.finditer(declaration):
                dependency = match.group(1)
                if dependency not in names:
                    names.add(dependency)
                    pending.append(dependency)
    return names


def css_content_attribute_names(css: str):
    properties = css_custom_properties(css)
    declarations = list(css_content_declarations(css))
    names = set()
    followed_properties = set()
    position = 0
    while position < len(declarations):
        declaration = declarations[position]
        position += 1
        names.update(
            match.group(1).lower()
            for match in CSS_ATTR_START.finditer(declaration)
        )
        for match in CSS_VAR_START.finditer(declaration):
            property_name = match.group(1)
            if property_name in followed_properties:
                continue
            followed_properties.add(property_name)
            declarations.extend(properties.get(property_name, ()))
    return names


def css_reference_values(css: str, attributes=None):
    seen = set()
    for value in css_generated_content_values(css, attributes):
        if value not in seen:
            seen.add(value)
            yield value
    for declarations in css_custom_properties(css).values():
        for declaration in declarations:
            value = "".join(css_string_values(declaration))
            if TN_CONTENT_TOKEN.search(value) and value not in seen:
                seen.add(value)
                yield value


def external_css_generated_content_violations(sources: dict[str, str]):
    errors = []
    for rel, source in sorted(sources.items()):
        for value in css_reference_values(source):
            if TN_CONTENT_TOKEN.search(value):
                errors.append((rel, f"generated Tennessee content {value!r}"))
    if not errors:
        combined = "\n".join(source for _, source in sorted(sources.items()))
        for value in css_reference_values(combined):
            if TN_CONTENT_TOKEN.search(value):
                errors.append(
                    (
                        ".github/tn-reference-inventory.json",
                        "cross-file generated Tennessee content",
                    )
                )
                break
    return errors


def reference_token_text(source: str, external_css: str = "") -> str:
    parser = ReferenceSurfaceParser()
    parser.feed(source)
    if external_css:
        parser.css_sources.insert(0, external_css)
    return parser.token_text()


def has_tennessee_reference_token(source: str, external_css: str = "") -> bool:
    return bool(
        TN_CONTENT_TOKEN.search(reference_token_text(source, external_css))
    )


def reference_surface_digest(source: str) -> str:
    parser = ReferenceSurfaceParser()
    parser.feed(source)
    parser.finalize_css_content()
    normalized = "\n".join(
        re.sub(r"\s+", " ", piece).strip()
        for piece in parser.pieces
        if piece.strip()
    )
    return hashlib.sha256(normalized.encode("utf-8")).hexdigest()


def reference_inventory_violations(
    sources: dict[str, str],
    inventory: dict,
    external_css_sources: dict[str, str] | None = None,
):
    errors = []
    stats = {}

    if inventory.get("schema_version") != 1:
        errors.append("schema_version must be 1")

    groups = inventory.get("reference_groups")
    if not isinstance(groups, dict):
        return ["reference_groups must be an object"], stats

    if set(groups) != set(REFERENCE_GROUPS):
        errors.append(
            "reference group names differ from the exact governed classification set"
        )

    classified = []
    for name in REFERENCE_GROUPS:
        paths = groups.get(name)
        if not isinstance(paths, list) or not all(isinstance(p, str) for p in paths):
            errors.append(f"{name} must be a list of paths")
            continue
        if paths != sorted(paths):
            errors.append(f"{name} paths must be sorted")
        if len(paths) != len(set(paths)):
            errors.append(f"{name} contains duplicate paths")
        membership_digest = hashlib.sha256(
            "\n".join(paths).encode("utf-8")
        ).hexdigest()
        if REFERENCE_GROUP_MEMBERSHIP_SHA256.get(name) != membership_digest:
            errors.append(f"{name} membership differs from the governed baseline")
        classified.extend(paths)

    if len(classified) != len(set(classified)):
        errors.append("a document source appears in more than one reference group")

    fingerprints = inventory.get("reference_surface_sha256")
    if not isinstance(fingerprints, dict) or not all(
        isinstance(path, str) and isinstance(digest, str)
        for path, digest in (fingerprints or {}).items()
    ):
        errors.append("reference_surface_sha256 must be a path to digest object")
        fingerprints = {}
    else:
        if list(fingerprints) != sorted(fingerprints):
            errors.append("reference_surface_sha256 paths must be sorted")

    fragments = inventory.get("excluded_non_page_fragments")
    if not isinstance(fragments, list) or not all(
        isinstance(p, str) for p in fragments
    ):
        errors.append("excluded_non_page_fragments must be a list of paths")
        fragments = []
    elif fragments != sorted(set(fragments)):
        errors.append("excluded_non_page_fragments must be sorted and unique")

    edge_sources = inventory.get("known_edge_301_sources")
    if not isinstance(edge_sources, list) or not all(
        isinstance(p, str) for p in edge_sources
    ):
        errors.append("known_edge_301_sources must be a list of paths")
        edge_sources = []
    elif edge_sources != sorted(set(edge_sources)):
        errors.append("known_edge_301_sources must be sorted and unique")

    discovery = {rel for rel, source in sources.items() if is_tn_page(rel, source)}
    external_css = "\n".join(
        source for _, source in sorted((external_css_sources or {}).items())
    )
    external_content_vars = css_content_custom_property_names(external_css)
    external_content_attrs = css_content_attribute_names(external_css)

    def contextual_external_css(source):
        source_custom_vars = {
            match.group(1)
            for match in CSS_CUSTOM_PROPERTY_START.finditer(source)
        }
        if source_custom_vars & external_content_vars:
            return external_css
        if any(
            re.search(
                rf"(?<![-\w]){re.escape(name)}\s*=",
                source,
                re.IGNORECASE,
            )
            for name in external_content_attrs
        ):
            return external_css
        return ""

    content_tokens = {
        rel for rel, source in sources.items()
        if has_tennessee_reference_token(
            source, contextual_external_css(source)
        )
    }
    fragment_set = set(fragments)
    if fragment_set != set(EXCLUDED_FRAGMENT_SURFACE_SHA256):
        errors.append("excluded fragment membership differs from the governed baseline")
    document_sources = discovery | (content_tokens - fragment_set)
    classified_set = set(classified)

    for rel in sorted(fragment_set):
        source = sources.get(rel)
        if source is None:
            errors.append(f"excluded fragment is missing: {rel}")
            continue
        if not has_tennessee_reference_token(source):
            errors.append(f"excluded fragment has no Tennessee content token: {rel}")
        if HTML_DOCUMENT_MARKER.search(source):
            errors.append(f"excluded fragment looks like a standalone document: {rel}")
        expected_digest = EXCLUDED_FRAGMENT_SURFACE_SHA256.get(rel)
        actual_digest = reference_surface_digest(source)
        if expected_digest != actual_digest:
            errors.append(
                f"excluded fragment surface changed for {rel}: "
                f"expected {expected_digest}, computed {actual_digest}"
            )

    expected_discovery = set(groups.get("path_or_title_discovery", []))
    for rel in sorted(discovery - expected_discovery):
        errors.append(f"unclassified path or title discovery source: {rel}")
    for rel in sorted(expected_discovery - discovery):
        errors.append(f"stale path or title discovery classification: {rel}")

    for rel in sorted(document_sources - classified_set):
        errors.append(f"unclassified Tennessee reference document: {rel}")
    for rel in sorted(classified_set - document_sources):
        errors.append(f"stale Tennessee reference classification: {rel}")

    fingerprint_paths = set(fingerprints)
    for rel in sorted(classified_set - fingerprint_paths):
        errors.append(f"missing Tennessee reference surface fingerprint: {rel}")
    for rel in sorted(fingerprint_paths - classified_set):
        errors.append(f"stale Tennessee reference surface fingerprint: {rel}")
    for rel in sorted(classified_set & fingerprint_paths & set(sources)):
        actual_digest = reference_surface_digest(sources[rel])
        if fingerprints[rel] != actual_digest:
            errors.append(
                f"Tennessee reference surface changed for {rel}: "
                f"expected {fingerprints[rel]}, computed {actual_digest}"
            )

    if not set(edge_sources).issubset(classified_set):
        errors.append("known edge sources must be classified document sources")

    counts = inventory.get("expected_counts")
    if not isinstance(counts, dict):
        errors.append("expected_counts must be an object")
        counts = {}

    actual_counts = {
        "document_sources": len(document_sources),
        "path_or_title_discovery": len(discovery),
        "outside_discovery": len(document_sources - discovery),
        "known_edge_301_sources": len(edge_sources),
        "document_sources_excluding_recorded_edge_sources": len(document_sources)
        - len(edge_sources),
        "excluded_non_page_fragments": len(fragment_set),
    }
    for name, actual in actual_counts.items():
        if counts.get(name) != actual:
            errors.append(
                f"expected_counts.{name} is {counts.get(name)!r}; computed {actual}"
            )

    stats.update(actual_counts)
    return errors, stats


def check_reference_inventory(fail):
    try:
        with open(REFERENCE_INVENTORY_PATH, encoding="utf-8") as fh:
            inventory = json.load(fh)
    except (OSError, json.JSONDecodeError) as exc:
        fail(".github/tn-reference-inventory.json", f"cannot load inventory: {exc}")
        return {}

    sources = {}
    for rel, full in iter_html_files():
        with open(full, encoding="utf-8") as fh:
            sources[rel] = fh.read()

    css_sources = {}
    for rel, full in iter_css_files():
        with open(full, encoding="utf-8") as fh:
            css_sources[rel] = fh.read()

    errors, stats = reference_inventory_violations(
        sources, inventory, css_sources
    )
    for message in errors:
        fail(".github/tn-reference-inventory.json", message)
    return stats


def check_external_css_generated_content(fail):
    sources = {}
    for rel, full in iter_css_files():
        with open(full, encoding="utf-8") as fh:
            sources[rel] = fh.read()
    for rel, message in external_css_generated_content_violations(sources):
        fail(rel, message)


def walk_nodes(obj, under_area_served=False):
    """Yield (node, under_area_served). areaServed geo pins the *served city*,
    which is legitimate; only business-level geo asserts premises."""
    if isinstance(obj, dict):
        yield obj, under_area_served
        for k, v in obj.items():
            yield from walk_nodes(v, under_area_served or k == "areaServed")
    elif isinstance(obj, list):
        for it in obj:
            yield from walk_nodes(it, under_area_served)


def check_metadata(rel: str, html: str, fail):
    fields = {"<title>": extract_title(html), "<h1>": extract_h1(html)}
    for name, prop in META_FIELDS:
        v = extract_meta(html, name, prop)
        if v is not None:
            fields[name] = v

    for field, value in fields.items():
        if not value:
            continue
        if FL_STATE.search(value):
            fail(rel, f"{field} carries a Florida state token: {value!r}")
        if FL_REGULATORY.search(FL_ATTRIBUTED.sub("", value)):
            fail(
                rel,
                f"{field} uses Florida-only regulatory proof (HVHZ/Miami-Dade/NOA) "
                f"on a Tennessee page: {value!r}",
            )


def check_hq_language(rel: str, html: str, fail):
    for m in HQ_LANGUAGE.finditer(html):
        start = max(0, m.start() - 80)
        snippet = re.sub(r"\s+", " ", html[start : m.end() + 80])
        fail(rel, f"unsupported Tennessee office language {m.group(0)!r} - …{snippet}…")


def check_structured_data(rel: str, html: str, fail):
    for raw in jsonld_blocks(html):
        try:
            data = json.loads(raw)
        except json.JSONDecodeError as e:
            fail(rel, f"JSON-LD does not parse: {e}")
            continue

        for node, under_area_served in walk_nodes(data):
            if node.get("@type") == "PostalAddress" and node.get("addressRegion") == "TN":
                fail(
                    rel,
                    "JSON-LD PostalAddress asserts a Tennessee business address "
                    f"({node.get('addressLocality')}, TN) - ACG has no TN address yet",
                )
            if node.get("@type") == "GeoCoordinates" and not under_area_served:
                try:
                    lat = float(node.get("latitude"))
                    lon = float(node.get("longitude"))
                except (TypeError, ValueError):
                    continue
                if TN_LAT[0] < lat < TN_LAT[1] and TN_LON[0] < lon < TN_LON[1]:
                    fail(
                        rel,
                        f"JSON-LD GeoCoordinates ({lat}, {lon}) place the business in "
                        "Tennessee - no TN premises exist",
                    )
            node_id = node.get("@id")
            if isinstance(node_id, str) and node_id.endswith("#office-nashville"):
                fail(rel, "JSON-LD declares a #office-nashville location node")


def mask_titles(text: str) -> str:
    """Blank out title tags, preserving offsets so context windows stay honest."""
    return TITLE_TAGS.sub(lambda m: " " * len(m.group(0)), text)


def delivery_claim_context_fingerprint(body: str, match: re.Match[str]) -> str:
    window = body[
        max(0, match.start() - QUALIFIER_BEFORE) : match.end() + QUALIFIER_AFTER
    ]
    visible = html_lib.unescape(re.sub(r"<[^>]+>", " ", window))
    normalized = re.sub(r"\s+", " ", visible).strip()
    return hashlib.sha256(normalized.encode("utf-8")).hexdigest()


def check_delivery_claims(rel: str, text: str, fail, held_observed=None):
    body = mask_titles(text)
    for label, rx in (("office-count", OFFICE_COUNT), ("combined-state delivery", DELIVERY_PAIR)):
        for m in rx.finditer(body):
            fingerprint = delivery_claim_context_fingerprint(body, m)
            held_key = (rel, label)
            if HELD_DELIVERY_CLAIMS.get(held_key) == fingerprint:
                if held_observed is not None:
                    held_observed.add((rel, label, fingerprint))
                continue
            snippet = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", m.group(0))).strip()
            fail(
                rel,
                f"unqualified {label} claim {snippet!r}. ACG has three Florida "
                "offices; drop or independently govern the additional claim. "
                f"Context fingerprint: {fingerprint}",
            )


def check_held_delivery_claims(held_observed, fail):
    for (rel, label), fingerprint in HELD_DELIVERY_CLAIMS.items():
        observed_key = (rel, label, fingerprint)
        if observed_key not in held_observed:
            fail(
                rel,
                f"exact held {label} fingerprint was not observed: {fingerprint}",
            )


def check_scoped_stale_operating_claims(rel: str, text: str, fail):
    """Keep stale expansion language off the governed Florida pages."""
    if rel not in STALE_OPERATING_CLAIM_PAGES + STALE_OPERATING_CLAIM_ASSETS:
        return
    checked = text
    for allowed in ALLOWED_NEUTRAL_TN_REFERENCES.get(rel, ()):
        checked = checked.replace(allowed, "")
    for match in STALE_OPERATING_LANGUAGE.finditer(checked):
        fail(rel, f"stale Tennessee operating language {match.group(0)!r}")


def iter_claim_files():
    for rel, full in iter_html_files():
        yield rel, full
    for name in ("llms.txt", "llms-full.txt", "ai.txt"):
        full = os.path.join(REPO_ROOT, name)
        if os.path.exists(full):
            yield name, full
    for name in STALE_OPERATING_CLAIM_ASSETS:
        yield name, os.path.join(REPO_ROOT, name)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--list", action="store_true", help="print discovered TN pages and exit")
    args = ap.parse_args()

    violations: list[tuple[str, str]] = []
    warnings: list[tuple[str, str]] = []

    def fail(rel, msg):
        violations.append((rel, msg))

    def warn(rel, msg):
        warnings.append((rel, msg))

    allowlist = load_claim_guard_allowlist()

    tn_pages = []
    scanned = 0
    held_observed = set()
    for rel, full in sorted(iter_claim_files()):
        with open(full, encoding="utf-8") as fh:
            html = fh.read()
        scanned += 1

        # #office-nashville must not exist anywhere, TN page or not.
        if "#office-nashville" in html and not args.list:
            fail(rel, "references a #office-nashville location node")

        # Delivery-complete claims are site-wide: they leaked onto pages that
        # are not Tennessee-scoped and so are invisible to the discovery pass.
        if not args.list:
            check_delivery_claims(rel, html, fail, held_observed)
            check_scoped_stale_operating_claims(rel, html, fail)
            # Prohibited public positioning (A - E) is also site-wide and covers
            # both indexable and noindex HTML. Only .html files carry the
            # metadata surfaces this rule scans - llms.txt et al are text-only.
            if rel.endswith(".html"):
                check_prohibited_public_positioning(
                    rel, html, fail, warn=warn, allowlist=allowlist
                )

        if not rel.endswith(".html") or not is_tn_page(rel, html):
            continue
        tn_pages.append(rel)

        if args.list:
            continue

        check_metadata(rel, html, fail)
        check_hq_language(rel, html, fail)
        check_structured_data(rel, html, fail)

    if not args.list:
        check_held_delivery_claims(held_observed, fail)
        reference_stats = check_reference_inventory(fail)
        check_external_css_generated_content(fail)
    else:
        reference_stats = {}

    if warnings and not args.list:
        print("tn-claim-guard warnings (non-blocking):")
        by_file_w: dict[str, list[str]] = {}
        for rel, msg in warnings:
            by_file_w.setdefault(rel, []).append(msg)
        for rel in sorted(by_file_w):
            print(f"  {rel}")
            for msg in by_file_w[rel]:
                print(f"    [!] {msg}")
        print(f"  ({len(warnings)} warning(s) across {len(by_file_w)} file(s))\n")

    if args.list:
        for p in tn_pages:
            print(p)
        print(f"\n{len(tn_pages)} Tennessee pages discovered")
        return 0

    print(
        f"tn-claim-guard: {len(tn_pages)} Tennessee pages checked for leakage; "
        f"{scanned} files checked for delivery-complete claims\n"
    )
    if not violations:
        print("  [✓] governed route, site-wide delivery, and exact stale-page checks pass")
        print(f"  [i] {len(HELD_DELIVERY_CLAIMS)} exact held claim fingerprint observed")
        print(
            "  [i] "
            f"{reference_stats['document_sources']} classified Tennessee reference "
            f"documents; {reference_stats['known_edge_301_sources']} recorded edge sources"
        )
        return 0

    by_file: dict[str, list[str]] = {}
    for rel, msg in violations:
        by_file.setdefault(rel, []).append(msg)
    for rel in sorted(by_file):
        print(f"  {rel}")
        for msg in by_file[rel]:
            print(f"    [✗] {msg}")
    print(f"\n{len(violations)} violation(s) across {len(by_file)} file(s)")
    return 1


if __name__ == "__main__":
    sys.exit(main())
