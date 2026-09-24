#!/usr/bin/env python3
"""Tech SEO hygiene batch 3: retired sitemap-pages, lastmod, robots, OG, CSS key."""

from __future__ import annotations

import re
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[3]
SM_NS = "{http://www.sitemaps.org/schemas/sitemap/0.9}"
LASTMOD_ALIGNED = (
    "https://acglass.com/glazing-value-engineering.html",
    "https://acglass.com/occupied-building-glazing-installation-florida/",
)
ROBOTS_INDEXABLE = "index,follow,max-image-preview:large,max-snippet:-1"


def _read(rel: str) -> str:
    return (REPO_ROOT / rel).read_text(encoding="utf-8")


def _lastmods(rel: str) -> dict[str, str]:
    root = ET.fromstring(_read(rel))
    out: dict[str, str] = {}
    for url in root.findall(f"{SM_NS}url"):
        loc = (url.findtext(f"{SM_NS}loc") or "").strip()
        lastmod = (url.findtext(f"{SM_NS}lastmod") or "").strip()
        if loc:
            out[loc] = lastmod
    return out


class SitemapPagesRetirementTests(unittest.TestCase):
    def test_public_stub_has_no_locs(self):
        locs = [
            el.text.strip()
            for el in ET.fromstring(_read("sitemap-pages.xml")).iter(f"{SM_NS}loc")
        ]
        self.assertEqual(locs, [])

    def test_fixture_keeps_the_retired_child_urlset(self):
        fixture = _lastmods(".github/fixtures/sitemap-pages.xml")
        # Floor tracks the retired child urlset after thin-template sitemap
        # drops: 373 after #206-#210, 370 after the emergency-repair cities.
        self.assertGreaterEqual(len(fixture), 370)


class LastmodAlignmentTests(unittest.TestCase):
    def test_named_urls_share_lastmod_across_master_blog_and_fixture(self):
        master = _lastmods("sitemap.xml")
        blog = _lastmods("sitemap-blog.xml")
        fixture = _lastmods(".github/fixtures/sitemap-pages.xml")
        for loc in LASTMOD_ALIGNED:
            self.assertEqual(master[loc], "2026-09-12", loc)
            self.assertEqual(blog[loc], master[loc], loc)
            self.assertEqual(fixture[loc], master[loc], loc)


class HeadHygieneTests(unittest.TestCase):
    def test_leadership_has_site_standard_robots(self):
        html = _read("leadership.html")
        match = re.search(
            r'<meta\s+name="robots"\s+content="([^"]+)"', html
        )
        self.assertIsNotNone(match)
        self.assertEqual(match.group(1), ROBOTS_INDEXABLE)

    def test_homepage_og_image_has_alt_width_height(self):
        html = _read("index.html")
        self.assertIn(
            'property="og:image" content="https://acglass.com/images/hero/gulfside-twelve-twilight.jpg"',
            html,
        )
        self.assertIn('property="og:image:width" content="1200"', html)
        self.assertIn('property="og:image:height" content="630"', html)
        self.assertIn(
            'property="og:image:alt" content="American Commercial Glass - Florida\'s commercial glazing specialists"',
            html,
        )

    def test_portfolio_og_image_has_alt_width_height(self):
        html = _read("portfolio.html")
        self.assertIn(
            'property="og:image" content="https://acglass.com/images/projects/atlantic-fields-golf-house/hero-golden-hour.jpg"',
            html,
        )
        self.assertIn('property="og:image:width" content="1200"', html)
        self.assertIn('property="og:image:height" content="630"', html)
        self.assertIn(
            'property="og:image:alt" content="Atlantic Fields Golf House, full-height clubhouse glazing"',
            html,
        )

    def test_free_scope_review_uses_current_dark_css_cache_key(self):
        html = _read("free-glazing-scope-review.html")
        self.assertIn('href="/css/acg2026-dark.css?v=20260919-a11y"', html)
        self.assertNotIn("v=20260802-unified", html)


if __name__ == "__main__":
    unittest.main(verbosity=2)
