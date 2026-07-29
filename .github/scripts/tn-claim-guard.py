#!/usr/bin/env python3
"""
tn-claim-guard.py — offline claim-integrity guard for the Tennessee pages.

Runs against the repo working tree (no HTTP), so it fails *before* deploy —
unlike seo-verify.py, which only sees what is already live.

It guards three things that regressed once already because the TN pages were
generated from the Florida templates:

  1. Florida location leakage in TN metadata — ", FL" state tokens, plus the
     Florida-only regulatory constructs (HVHZ, Miami-Dade, NOA) used as if they
     were Tennessee proof.
  2. Staffed-office language ("Nashville HQ", "Tennessee headquarters") that
     implies a Tennessee office that does not exist yet.
  3. Structured data asserting a Tennessee street address, Tennessee
     coordinates, or a Tennessee LocalBusiness node.

What it deliberately does NOT flag:
  - The West Palm Beach NAP in the footer of every page. That address is real
    and belongs on TN pages.
  - Body copy that contrasts Florida and Tennessee ("there is no HVHZ anywhere
    in Tennessee", "Florida HVHZ engineering discipline transfers to TN").
    Those statements are true and are the point of the pages, so only metadata
    is scanned for the Florida regulatory terms.

Usage:
  python .github/scripts/tn-claim-guard.py            # exit 1 on any violation
  python .github/scripts/tn-claim-guard.py --list     # print discovered TN pages
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

SKIP_DIRS = {".git", ".github", "_internal", "node_modules", "fonts", "images", "css", "js"}

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


def iter_html_files():
    for dirpath, dirnames, filenames in os.walk(REPO_ROOT):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS and not d.startswith(".")]
        for fn in filenames:
            if fn.endswith(".html"):
                full = os.path.join(dirpath, fn)
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
        fail(rel, f"unsupported Tennessee office language {m.group(0)!r} — …{snippet}…")


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
                    f"({node.get('addressLocality')}, TN) — ACG has no TN address yet",
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
                        "Tennessee — no TN premises exist",
                    )
            node_id = node.get("@id")
            if isinstance(node_id, str) and node_id.endswith("#office-nashville"):
                fail(rel, "JSON-LD declares a #office-nashville location node")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--list", action="store_true", help="print discovered TN pages and exit")
    args = ap.parse_args()

    violations: list[tuple[str, str]] = []

    def fail(rel, msg):
        violations.append((rel, msg))

    tn_pages = []
    for rel, full in sorted(iter_html_files()):
        with open(full, encoding="utf-8") as fh:
            html = fh.read()

        # #office-nashville must not exist anywhere, TN page or not.
        if "#office-nashville" in html and not args.list:
            fail(rel, "references a #office-nashville location node")

        if not is_tn_page(rel, html):
            continue
        tn_pages.append(rel)

        if args.list:
            continue

        check_metadata(rel, html, fail)
        check_hq_language(rel, html, fail)
        check_structured_data(rel, html, fail)

    if args.list:
        for p in tn_pages:
            print(p)
        print(f"\n{len(tn_pages)} Tennessee pages discovered")
        return 0

    print(f"tn-claim-guard: scanned {len(tn_pages)} Tennessee pages\n")
    if not violations:
        print("  [✓] no Florida leakage, no unsupported Tennessee office claims")
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
