#!/usr/bin/env python3
"""Regression contract for bounded indexable Tennessee truth corrections."""

from __future__ import annotations

import html
import hashlib
import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]

TARGETS = {
    "locations.html": {
        "title": "ACG Locations and Coverage | Florida",
        "description": (
            "ACG locations in West Palm Beach, Naples, and Tampa, with commercial "
            "glazing service areas across Florida. Florida CGC #1531993."
        ),
        "canonical": "https://acglass.com/locations.html",
    },
    "service-areas-map/index.html": {
        "title": "ACG Service Areas | Florida Commercial Glazing",
        "description": (
            "Browse ACG commercial glazing service areas across Florida, including "
            "South Florida, Southwest Florida, Tampa Bay, Central Florida, and North "
            "Florida."
        ),
        "canonical": "https://acglass.com/service-areas-map/",
    },
}

SCHEMA_ONLY_TARGETS = {
    "acg-vs-harmon.html",
    "acg-vs-permasteelisa.html",
}

ADDITIONAL_VISIBLE_TARGETS = {
    "acg-vs-giroux-glass.html",
    "glazing-subcontractor-vs-general-contractor.html",
    "restaurant-glazing-contractor.html",
}

METADATA_ONLY_TARGETS = {
    "security-window-film-retrofit.html",
}

PROTECTED_LINE_MARKERS = re.compile(
    r"Rielly|Woman-owned|WBE|51%|\bCEO\b|owner(?:ship|-level)?|Verdex|Panther",
    re.IGNORECASE,
)

PROTECTED_LINE_DIGESTS = {
    "acg-vs-giroux-glass.html": (
        14,
        "0df6239da88c58b668e5c0293cf88bfba52fbb8a3e5746ab294e8617b4cf3215",
    ),
    "acg-vs-harmon.html": (
        14,
        "7a8fc02b3f608928581f2af7595d68cc16598919fdf55f6f2da5110dbb6ff47a",
    ),
    "acg-vs-permasteelisa.html": (
        10,
        "44dbe3c2c4fb99c4170d5e737dae175b13ede2a63ab0e7954f593bebdd17adfe",
    ),
    "glazing-subcontractor-vs-general-contractor.html": (
        6,
        "dff2ada45f5d9cf621a26a16658402973c114bf5421781b8125619646ea502ce",
    ),
}

PROHIBITED_CLAIMS = (
    re.compile(r"\bTennessee\b", re.IGNORECASE),
    re.compile(r"\bTN\b", re.IGNORECASE),
    re.compile(r"\bQ3\s+2026\b", re.IGNORECASE),
    re.compile(r"\b(?:four|4)\s+offices\b", re.IGNORECASE),
    re.compile(r"select\s+Southeast\s+markets", re.IGNORECASE),
    re.compile(r"GC\s+partner\s+relationships", re.IGNORECASE),
)


def extract_title(source: str) -> str:
    match = re.search(r"<title>(.*?)</title>", source, re.DOTALL | re.IGNORECASE)
    if not match:
        return ""
    return html.unescape(re.sub(r"\s+", " ", match.group(1)).strip())


def extract_meta(source: str, key: str, attribute: str = "name") -> str | None:
    match = re.search(
        rf'<meta[^>]+{attribute}="{re.escape(key)}"[^>]+content="([^"]*)"',
        source,
        re.IGNORECASE,
    )
    return html.unescape(match.group(1)) if match else None


def extract_canonical(source: str) -> str | None:
    match = re.search(
        r'<link[^>]+rel="canonical"[^>]+href="([^"]+)"',
        source,
        re.IGNORECASE,
    )
    return match.group(1) if match else None


def jsonld_nodes(source: str):
    blocks = re.findall(
        r'<script[^>]+type="application/ld\+json"[^>]*>(.*?)</script>',
        source,
        re.DOTALL | re.IGNORECASE,
    )
    for block in blocks:
        data = json.loads(block)
        if isinstance(data, list):
            yield from data
        else:
            yield data


def protected_line_digest(source: str) -> tuple[int, str]:
    lines = [
        re.sub(r"\s+", " ", html.unescape(line)).strip()
        for line in source.splitlines()
        if PROTECTED_LINE_MARKERS.search(html.unescape(line))
    ]
    digest = hashlib.sha256("\n".join(lines).encode("utf-8")).hexdigest()
    return len(lines), digest


class IndexableTennesseeTruthCleanupTests(unittest.TestCase):
    def test_exact_page_contract(self):
        self.assertEqual(
            set(TARGETS),
            {"locations.html", "service-areas-map/index.html"},
        )
        for rel, expected in TARGETS.items():
            with self.subTest(rel=rel):
                source = (ROOT / rel).read_text(encoding="utf-8")
                self.assertEqual(extract_title(source), expected["title"])
                self.assertEqual(
                    extract_meta(source, "description"),
                    expected["description"],
                )
                self.assertEqual(
                    extract_meta(source, "og:title", "property"),
                    expected["title"],
                )
                self.assertEqual(
                    extract_meta(source, "og:description", "property"),
                    expected["description"],
                )
                self.assertEqual(extract_canonical(source), expected["canonical"])
                self.assertNotRegex(
                    source,
                    r'<meta[^>]+name="robots"[^>]+content="[^"]*noindex',
                )
                self.assertGreaterEqual(len(expected["description"]), 80)
                self.assertLessEqual(len(expected["description"]), 155)
                for pattern in PROHIBITED_CLAIMS:
                    self.assertIsNone(pattern.search(source), pattern.pattern)

    def test_additional_indexable_pages_remove_stale_operating_claims(self):
        expected = {
            "acg-vs-giroux-glass.html",
            "acg-vs-harmon.html",
            "acg-vs-permasteelisa.html",
            "glazing-subcontractor-vs-general-contractor.html",
            "restaurant-glazing-contractor.html",
            "security-window-film-retrofit.html",
        }
        self.assertEqual(
            SCHEMA_ONLY_TARGETS | ADDITIONAL_VISIBLE_TARGETS | METADATA_ONLY_TARGETS,
            expected,
        )
        for rel in sorted(expected):
            with self.subTest(rel=rel):
                source = (ROOT / rel).read_text(encoding="utf-8")
                self.assertNotRegex(
                    source,
                    r'<meta[^>]+name="robots"[^>]+content="[^"]*noindex',
                )
                for pattern in PROHIBITED_CLAIMS:
                    self.assertIsNone(pattern.search(source), pattern.pattern)

    def test_security_page_social_title_is_florida_only(self):
        source = (ROOT / "security-window-film-retrofit.html").read_text(
            encoding="utf-8"
        )
        expected = "Security Window Film Retrofit | ACG Florida"
        self.assertEqual(extract_meta(source, "og:title", "property"), expected)
        self.assertEqual(extract_meta(source, "twitter:title"), expected)

    def test_protected_ownership_and_project_lines_remain_exact(self):
        for rel, expected in PROTECTED_LINE_DIGESTS.items():
            with self.subTest(rel=rel):
                source = (ROOT / rel).read_text(encoding="utf-8")
                self.assertEqual(protected_line_digest(source), expected)

    def test_protected_line_contract_fails_on_mutation(self):
        rel = "acg-vs-giroux-glass.html"
        source = (ROOT / rel).read_text(encoding="utf-8")
        changed = source.replace("Rielly Walsh", "Changed protected name", 1)
        self.assertNotEqual(
            protected_line_digest(changed),
            PROTECTED_LINE_DIGESTS[rel],
        )

    def test_competitor_page_area_served_is_florida_only(self):
        for rel in (
            "acg-vs-giroux-glass.html",
            "acg-vs-harmon.html",
            "acg-vs-permasteelisa.html",
        ):
            with self.subTest(rel=rel):
                source = (ROOT / rel).read_text(encoding="utf-8")
                org = next(
                    node
                    for node in jsonld_nodes(source)
                    if node.get("@id") == "https://acglass.com/#organization"
                )
                self.assertEqual(org.get("areaServed"), ["Florida"])

    def test_visible_corrections_remain_exact(self):
        giroux = (ROOT / "acg-vs-giroux-glass.html").read_text(encoding="utf-8")
        comparison = (
            ROOT / "glazing-subcontractor-vs-general-contractor.html"
        ).read_text(encoding="utf-8")
        restaurant = (ROOT / "restaurant-glazing-contractor.html").read_text(
            encoding="utf-8"
        )
        self.assertIn(
            "Your project is in Florida, where ACG holds Florida CGC #1531993.",
            giroux,
        )
        self.assertIn(
            "ACG operates in Florida statewide. Sub availability expands with "
            "national-reach subs.",
            comparison,
        )
        self.assertIn("FL CGC #1531993: licensed in Florida", comparison)
        self.assertIn('<div class="num">FL</div>', restaurant)

    def test_locations_webpage_schema_is_florida_only(self):
        source = (ROOT / "locations.html").read_text(encoding="utf-8")
        page = next(
            node
            for node in jsonld_nodes(source)
            if node.get("@id") == "https://acglass.com/locations.html#webpage"
        )
        self.assertEqual(
            page.get("name"),
            "ACG Locations and Commercial Glazing Coverage in Florida",
        )

    def test_service_area_schema_remains_florida_only(self):
        source = (ROOT / "service-areas-map/index.html").read_text(encoding="utf-8")
        org = next(
            node
            for node in jsonld_nodes(source)
            if node.get("@id") == "https://acglass.com/#organization"
        )
        self.assertEqual(
            org.get("areaServed"),
            [{"@type": "State", "name": "Florida"}],
        )


if __name__ == "__main__":
    unittest.main()
