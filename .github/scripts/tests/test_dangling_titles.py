#!/usr/bin/env python3
"""Document titles that were cut mid-phrase stay restored.

The <title> Google shows was chopped before a preposition, a dash, or
"| American". The complete wording already lived in og:title, the
schema name, or the same tag with one stray token. These titles are
that wording, at or under 60 characters. Frozen keeper titles stay
exact.
"""

from __future__ import annotations

import html
import re
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[3]
BASE = "https://acglass.com"
SM_NS = "{http://www.sitemaps.org/schemas/sitemap/0.9}"
TITLE_RE = re.compile(r"<title[^>]*>(.*?)</title>", re.I | re.S)
OG_RE = re.compile(
    r'<meta\b[^>]*property=["\']og:title["\'][^>]*>', re.I
)
CONTENT_RE = re.compile(r'\bcontent="([^"]*)"', re.I)

# A title that ends on one of these is the cut this guard exists for.
DANGLING = (
    re.compile(
        r"\b(?:in|for|to|of|my|on|with|and|by|at|from|who)\s+\|\s+ACG\s*$",
        re.I,
    ),
    re.compile(r"[-:]\s+\|\s+ACG\s*$"),
    re.compile(r"\|\s+American\s*$"),
    re.compile(r"\|\s+Florida Commercial\s*$"),
    re.compile(r": A Tenant\s*$"),
    re.compile(r": Design\s*$"),
    re.compile(r"Annual \| ACG\s*$"),
)

RESTORED = {
    "how-to-hire-commercial-glazing-contractor-florida.html": (
        "How to Hire a Commercial Glazing Contractor in Florida | ACG"
    ),
    "blog/budget-commercial-glass-replacement-florida.html": (
        "How to Budget for Commercial Glass Replacement in Florida"
    ),
    "blog/how-to-choose-glass-options-storefront.html": (
        "How Do I Choose Between Glass Options for My Storefront?"
    ),
    "blog/find-glazier-who-handles-design-build.html": (
        "How to Find a Commercial Glazier Who Handles Design-Build"
    ),
    "blog/how-to-know-glazier-did-quality-work.html": (
        "How to Know If Your Commercial Glazier Did Quality Work"
    ),
    "glazing-submittal-package.html": (
        "Commercial Glazing Submittal Package - Sample for GCs | ACG"
    ),
    "case-study-gulfside-twelve.html": (
        "Gulfside Twelve - Gulf Coast Multifamily Glazing | ACG"
    ),
    "wild-blue-clubhouse.html": (
        "Wild Blue at Waterside Clubhouse | Resort Glazing - ACG"
    ),
    "blog/commercial-glass-partition-systems-offices.html": (
        "Commercial Glass Partition Systems for Offices"
    ),
    "blog/commercial-skylights-glass-ceilings-florida.html": (
        "Commercial Skylights and Glass Ceilings in Florida"
    ),
    "florida-commercial-glaziers-compared/index.html": (
        "Florida Commercial Glaziers Compared - How to Evaluate"
    ),
    "storefront-systems-comparison.html": (
        "Commercial Storefront Systems Comparison | ACG"
    ),
    "acg-glass.html": "ACG Glass - American Commercial Glass",
    "florida-commercial-glazing-report-2026.html": (
        "State of Florida Commercial Glazing 2026"
    ),
    "best-glazing-subcontractor-florida.html": (
        "Florida Commercial Glazing Subcontractor | ACG"
    ),
    "best-storefront-contractor-florida.html": (
        "Florida Commercial Storefront Contractor | ACG"
    ),
    "blog/commercial-glazier-hourly-rate-florida-2026.html": (
        "Commercial Glazier Hourly Rate in Florida 2026 | ACG"
    ),
    "blog/union-vs-non-union-glazier-florida.html": (
        "Union vs Non-Union Commercial Glazier in Florida | ACG"
    ),
    "storefront-bid-checklist-for-gcs.html": (
        "Storefront Bid Checklist for General Contractors | ACG"
    ),
    "storefront-cost-per-square-foot-florida.html": (
        "Commercial Storefront Cost Per Square Foot Florida | ACG"
    ),
    "storefront-water-intrusion-repair.html": (
        "Commercial Storefront Water Intrusion Repair | ACG"
    ),
}

FROZEN_TITLES = {
    "index.html": "Commercial Glazing Contractor Florida | ACG",
    "florida-commercial-glazing/index.html": (
        "Commercial Storefront Installer Florida | Bid in 48 Hrs"
    ),
    "storefront-glazier-west-palm-beach-florida/index.html": (
        "Commercial Storefront Installer, West Palm Beach | Bid"
    ),
    "storefront-glazier-naples-florida/index.html": (
        "Commercial Storefront Installer Naples | 48-Hr Bids"
    ),
    "storefront-glazier-tampa-florida/index.html": (
        "Commercial Storefront Installer Tampa | 48-Hr Bids"
    ),
}


def title_of(html_text: str) -> str:
    match = TITLE_RE.search(html_text)
    if not match:
        return ""
    return re.sub(r"\s+", " ", html.unescape(match.group(1))).strip()


def og_title_of(html_text: str) -> str:
    tag = OG_RE.search(html_text)
    if not tag:
        return ""
    content = CONTENT_RE.search(tag.group(0))
    if not content:
        return ""
    return re.sub(r"\s+", " ", html.unescape(content.group(1))).strip()


def path_for(url: str) -> Path:
    rel = url[len(BASE):]
    if rel in ("", "/"):
        return REPO_ROOT / "index.html"
    if rel.endswith("/"):
        return REPO_ROOT / rel.strip("/") / "index.html"
    direct = REPO_ROOT / rel.lstrip("/")
    if direct.is_file():
        return direct
    return REPO_ROOT / rel.strip("/") / "index.html"


class DanglingTitleTests(unittest.TestCase):
    def test_restored_titles_match_the_published_wording(self):
        for rel, expected in RESTORED.items():
            html_text = (REPO_ROOT / rel).read_text(encoding="utf-8")
            self.assertEqual(title_of(html_text), expected, rel)
            self.assertLessEqual(len(expected), 60, rel)
            og = og_title_of(html_text)
            # og:title is the same phrase, or the longer social title the
            # document title was cut down from. " | ACG" is only a brand
            # suffix on the document title.
            stem = expected[: -len(" | ACG")] if expected.endswith(" | ACG") else expected
            self.assertTrue(
                og == expected or og.startswith(stem),
                f"{rel} og:title {og!r} does not contain the document title",
            )

    def test_sitemap_titles_are_not_cut_mid_phrase(self):
        hits = []
        root = ET.parse(REPO_ROOT / "sitemap.xml").getroot()
        for el in root.iter(f"{SM_NS}loc"):
            if not el.text:
                continue
            path = path_for(el.text.strip())
            if not path.is_file():
                continue
            title = title_of(path.read_text(encoding="utf-8", errors="replace"))
            if len(title) > 60:
                hits.append(f"{path.relative_to(REPO_ROOT)}: {len(title)} chars")
            for pattern in DANGLING:
                if pattern.search(title):
                    hits.append(f"{path.relative_to(REPO_ROOT)}: {title}")
        self.assertEqual(hits, [])

    def test_frozen_keeper_titles_are_unchanged(self):
        for rel, expected in FROZEN_TITLES.items():
            html_text = (REPO_ROOT / rel).read_text(encoding="utf-8")
            self.assertEqual(title_of(html_text), expected, rel)

    def test_hire_page_title_keeps_florida(self):
        html_text = (
            REPO_ROOT / "how-to-hire-commercial-glazing-contractor-florida.html"
        ).read_text(encoding="utf-8")
        title = title_of(html_text)
        self.assertIn("Florida", title)
        self.assertNotIn(" in | ACG", title)


if __name__ == "__main__":
    unittest.main()
