"""Service pages must not inherit the reviews template's social copy or crumb."""

from __future__ import annotations

import json
import re
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[3]
SKIP_DIRS = {".git", ".github", "node_modules", "dealer"}

# Stale reviews.html social blurb. The live reviews page no longer uses it.
# It was left on four sitemap service pages, so Open Graph and Twitter cards
# described those URLs as client reviews.
STALE_REVIEWS_BLURB = (
    "Client reviews and testimonials for American Commercial Glass (ACG). "
    "General contractor and architect feedback on ACG's Division 08 scope "
    "delivery, submittals, HVHZ compliance, and project execution across Florida."
)

# Visible breadcrumb text, in order. The JSON-LD trail must match it, and the
# last item must be this page rather than /reviews.html.
EXPECTED_CRUMBS = {
    "impact-windows-doors.html": (
        "Home",
        "Services",
        "Impact Windows & Doors",
    ),
    "curtainwall-systems.html": (
        "Home",
        "Services",
        "Curtain Wall",
    ),
    "multi-slide-bifold-doors.html": (
        "Home",
        "Services",
        "Multi-Slide & Bifold Doors",
    ),
    "architect-resources.html": (
        "Home",
        "Architect Resources",
    ),
}

META_DESC = re.compile(
    r'<meta\b[^>]*name=["\']description["\'][^>]*content=["\']([^"\']*)["\']',
    re.I,
)
OG_DESC = re.compile(
    r'<meta\b[^>]*property=["\']og:description["\'][^>]*content=["\']([^"\']*)["\']',
    re.I,
)
TW_DESC = re.compile(
    r'<meta\b[^>]*name=["\']twitter:description["\'][^>]*content=["\']([^"\']*)["\']',
    re.I,
)
JSONLD = re.compile(
    r'<script\b[^>]*type=["\']application/ld\+json["\'][^>]*>(.*?)</script>',
    re.I | re.S,
)


def _iter_html():
    for path in REPO_ROOT.rglob("*.html"):
        if any(part in SKIP_DIRS for part in path.relative_to(REPO_ROOT).parts):
            continue
        yield path


def _meta(pattern: re.Pattern[str], html: str) -> str:
    match = pattern.search(html)
    if match is None:
        return ""
    return match.group(1)


def _breadcrumb_names(html: str) -> list[list[str]]:
    trails = []
    for block in JSONLD.findall(html):
        try:
            data = json.loads(block)
        except json.JSONDecodeError:
            continue
        nodes = data if isinstance(data, list) else [data]
        if isinstance(data, dict) and "@graph" in data:
            nodes = data["@graph"]
        for node in nodes:
            if not isinstance(node, dict) or node.get("@type") != "BreadcrumbList":
                continue
            names = []
            for item in node.get("itemListElement") or []:
                if isinstance(item, dict):
                    names.append(item.get("name") or "")
            trails.append(names)
    return trails


class ServiceSchemaCrumbTests(unittest.TestCase):
    def test_stale_reviews_social_blurb_is_gone(self):
        hits = []
        for path in _iter_html():
            html = path.read_text(encoding="utf-8", errors="replace")
            if STALE_REVIEWS_BLURB in html:
                hits.append(path.relative_to(REPO_ROOT).as_posix())
        self.assertEqual(hits, [])

    def test_reviews_breadcrumb_name_stays_on_the_reviews_page(self):
        leaks = []
        for path in _iter_html():
            rel = path.relative_to(REPO_ROOT).as_posix()
            if rel == "reviews.html":
                continue
            html = path.read_text(encoding="utf-8", errors="replace")
            for trail in _breadcrumb_names(html):
                if "Reviews" in trail:
                    leaks.append(f"{rel}: {trail}")
        self.assertEqual(leaks, [])

    def test_service_social_descriptions_match_the_page_meta(self):
        for rel in EXPECTED_CRUMBS:
            html = (REPO_ROOT / rel).read_text(encoding="utf-8")
            meta = _meta(META_DESC, html)
            self.assertTrue(meta, rel)
            self.assertEqual(_meta(OG_DESC, html), meta, rel)
            self.assertEqual(_meta(TW_DESC, html), meta, rel)
            self.assertNotIn("reviews.html", html.split("</head>", 1)[0])

    def test_service_breadcrumb_jsonld_matches_the_visible_trail(self):
        for rel, expected in EXPECTED_CRUMBS.items():
            html = (REPO_ROOT / rel).read_text(encoding="utf-8")
            trails = _breadcrumb_names(html)
            self.assertEqual(trails, [list(expected)], rel)
            self.assertIn(f"https://acglass.com/{rel}", html)
            self.assertNotIn(
                '"name":"Reviews"',
                html,
            )
