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

    def test_every_sitemap_url_is_self_canonical_and_has_matching_og_url(self):
        # Indexable locs must name themselves. A missing canonical used to
        # pass crawl-check because the checker only compared a tag it found.
        canon_re = re.compile(
            r'<link[^>]+rel="canonical"[^>]+href="([^"]+)"', re.I
        )
        og_re = re.compile(
            r'<meta[^>]+property="og:url"[^>]+content="([^"]+)"', re.I
        )
        missing = []
        master = _lastmods("sitemap.xml")
        for loc in master:
            rel = loc.removeprefix("https://acglass.com").lstrip("/")
            if rel == "" or rel.endswith("/"):
                rel += "index.html"
            html = _read(rel)
            canon = canon_re.search(html)
            og = og_re.search(html)
            if not canon or canon.group(1).rstrip("/") != loc.rstrip("/"):
                missing.append(f"canonical {loc}")
            if not og or og.group(1).rstrip("/") != loc.rstrip("/"):
                missing.append(f"og:url {loc}")
        self.assertEqual(missing, [])

    def test_free_scope_review_uses_current_dark_css_cache_key(self):
        html = _read("free-glazing-scope-review.html")
        self.assertIn('href="/css/acg2026-dark.css?v=20260919-a11y"', html)
        self.assertNotIn("v=20260802-unified", html)


class CountyImpactClaimTests(unittest.TestCase):
    """County code paragraphs must agree with the wind-zone card on the same page."""

    WBDR_SENTENCE = (
        "Impact-rated assemblies (or approved shutters) are required for all "
        "openings exposed to design wind pressure."
    )
    INLAND_SENTENCE = (
        "Impact-rated assemblies are not required by code. Standard glazing "
        "meeting wind load requirements is acceptable."
    )

    def test_code_paragraph_matches_wind_zone_card(self):
        wind_re = re.compile(
            r"Wind Code Zone</div>\s*<div[^>]*>(.*?)</div>", re.S | re.I
        )
        para_re = re.compile(r"Florida Building Code 8th Edition.*?</p>", re.S)
        mismatches = []
        for path in sorted(REPO_ROOT.glob("*-county/index.html")):
            html = path.read_text(encoding="utf-8")
            robots = re.search(r'name="robots"[^>]+content="([^"]+)"', html)
            if robots and "noindex" in robots.group(1).lower():
                continue
            wind_m = wind_re.search(html)
            para_m = para_re.search(html)
            if not wind_m or not para_m:
                continue
            wind = re.sub(r"<[^>]+>", "", wind_m.group(1))
            para = re.sub(r"<[^>]+>", "", para_m.group(0))
            wind_l = wind.lower()
            # "no WBDR" is an inland signal. Do not treat that phrase as debris.
            says_no_wbdr = "no wbdr" in wind_l
            debris = (
                "wind-borne" in wind_l
                or "hvhz" in wind_l
                or "impact-rated assemblies required" in wind_l
                or ("wbdr" in wind_l and not says_no_wbdr)
            )
            inland = says_no_wbdr or (
                "inland" in wind_l
                and "wbdr" not in wind_l
                and "wind-borne" not in wind_l
                and "hvhz" not in wind_l
            )
            if debris and self.INLAND_SENTENCE in para:
                mismatches.append(f"{path.parent.name}: WBDR card, inland sentence")
            if inland and self.WBDR_SENTENCE in para:
                mismatches.append(f"{path.parent.name}: inland card, WBDR sentence")
        self.assertEqual(mismatches, [])


if __name__ == "__main__":
    unittest.main(verbosity=2)
