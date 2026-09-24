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


class PalmBeachNotHvhzTests(unittest.TestCase):
    """FBC HVHZ is Miami-Dade and Broward only. Palm Beach is not in it.

    The West Palm Beach keeper already says so. These phrases were the
    live contradiction: indexable explainers and Palm Beach pages calling
    part of the county HVHZ, including an east-of-Military-Trail boundary
    and a 170-200 mph figure that was attached to that false geography.
    """

    FORBIDDEN = (
        "parts of Palm Beach",
        "portions of Palm Beach",
        "east of Military Trail",
        "HVHZ partial",
        "HVHZ portion of Palm Beach",
        "Palm Beach County HVHZ",
        "fully HVHZ designated",
        "falls within the HVHZ",
        "falls within HVHZ",
        "South Palm Beach (HVHZ)",
        "170-200 mph",
        "hardened HVHZ",
        "HVHZ tri-county",
        "Military Trail is the line",
        "same HVHZ standards",
        "same HVHZ detailing",
        "and Palm Beach counties - Florida's High Velocity Hurricane Zone",
        "Palm Beach County's High Velocity Hurricane Zone",
        "Palm Beach County&rsquo;s High Velocity Hurricane Zone",
    )

    def test_no_html_puts_palm_beach_inside_the_hvhz(self):
        hits = []
        for path in REPO_ROOT.rglob("*.html"):
            rel = path.relative_to(REPO_ROOT)
            if set(rel.parts) & {".git", "node_modules", ".github"}:
                continue
            html = path.read_text(encoding="utf-8", errors="replace")
            for phrase in self.FORBIDDEN:
                if phrase in html:
                    hits.append(f"{rel}: {phrase}")
        self.assertEqual(hits, [])

    def test_no_paragraph_puts_a_palm_beach_place_inside_hvhz(self):
        places = re.compile(
            r"Palm Beach|Boynton Beach|Delray Beach|Wellington|Boca Raton|"
            r"Riviera Beach|Lake Worth|Jupiter Island|North Palm Beach",
            re.I,
        )
        membership = re.compile(
            r"fall(?:s|ing)? within the High Velocity Hurricane Zone|"
            r"within Florida's High Velocity Hurricane Zone",
            re.I,
        )
        negation = re.compile(
            r"not in the (?:High Velocity Hurricane Zone|HVHZ)|"
            r"not the High Velocity Hurricane Zone|"
            r"outside the High Velocity Hurricane Zone",
            re.I,
        )
        hits = []
        for path in REPO_ROOT.rglob("*.html"):
            rel = path.relative_to(REPO_ROOT)
            if set(rel.parts) & {".git", "node_modules", ".github"}:
                continue
            html = path.read_text(encoding="utf-8", errors="replace")
            for chunk in re.findall(r"<p\b[^>]*>[\s\S]*?</p>", html, re.I):
                text = re.sub(r"<[^>]+>", " ", chunk)
                text = re.sub(r"\s+", " ", text)
                if places.search(text) and membership.search(text) and not negation.search(text):
                    hits.append(f"{rel}: {text.strip()[:180]}")
        self.assertEqual(hits, [])

    def test_palm_beach_county_page_does_not_claim_hvhz_certified(self):
        html = _read("commercial-glazing-palm-beach-county.html")
        self.assertNotIn("HVHZ-certified", html)
        self.assertNotIn("HVHZ Impact Windows", html)
        self.assertNotIn("HVHZ or FBC", html)
        self.assertIn("not HVHZ", html)
        self.assertIn("Florida Product Approval", html)

    def test_palm_beach_cards_keep_existing_wind_numbers(self):
        county = (REPO_ROOT / "palm-beach-county/index.html").read_text(encoding="utf-8")
        self.assertIn("165 mph (east) / 150 mph (west)", county)
        self.assertIn("Not HVHZ", county)
        lookup = (REPO_ROOT / "tools/hvhz-zone-lookup/index.html").read_text(encoding="utf-8")
        self.assertIn(">165 mph<", lookup)
        self.assertIn("Not HVHZ. Wind-borne debris region.", lookup)


class NonHvhzCountyClaimTests(unittest.TestCase):
    """Monroe, Lee, and Collier are wind-borne debris regions, not HVHZ.

    Indexable pages and the Florida Keys pages linked from the indexable hub
    were still telling GCs those counties are HVHZ and that Miami-Dade NOA is
    required. The county cards already publish the wind speeds used here.
    """

    FORBIDDEN = (
        "Lee County HVHZ",
        "Collier County HVHZ",
        "Florida Keys HVHZ",
        "Florida Keys (HVHZ)",
        "Keys · HVHZ",
        "Keys HVHZ",
        "FL Keys HVHZ",
        "Gulf Coast HVHZ",
        "HVHZ Lee County",
        "HVHZ - Direct Gulf Exposure",
        "Coastal HVHZ package",
        "Every commercial opening in Florida Keys is in HVHZ",
        "Florida Keys is in HVHZ",
        "Florida Keys is in Florida's HVHZ envelope",
        "Florida Keys (Monroe County) is in Florida's HVHZ envelope",
        "in Florida's High-Velocity Hurricane Zone (HVHZ). Every commercial storefront",
        "In HVHZ Florida Keys",
        "HVHZ Florida Keys",
        "Portions of Collier County",
        "172 mph design pressure",
        "Palm Beach · Coastal HVHZ",
        "Palm Beach · HVHZ",
        "Coastal HVHZ.",
        "multi-building HVHZ envelope, Hobe Sound",
        "which enforces Florida Keys HVHZ",
        "which enforces Lee County HVHZ",
        "which enforces Collier County HVHZ",
        "NOA requirements that apply in Pinellas",
        "all of Pinellas County is within the High-Velocity Hurricane Zone",
        "The coastal areas of these counties are also in the High Velocity Hurricane Zone",
    )

    def _indexable_html(self):
        robots_re = re.compile(
            r'<meta[^>]+name=["\']robots["\'][^>]+content=["\']([^"\']+)',
            re.I,
        )
        for path in REPO_ROOT.rglob("*.html"):
            rel = path.relative_to(REPO_ROOT)
            if set(rel.parts) & {".git", "node_modules", ".github"}:
                continue
            html = path.read_text(encoding="utf-8", errors="replace")
            robots = robots_re.search(html)
            if robots and "noindex" in robots.group(1).lower():
                continue
            yield rel, html

    def test_projects_cudjoe_card_does_not_call_monroe_hvhz(self):
        html = _read("projects/index.html")
        self.assertNotIn("Monroe County HVHZ", html)
        self.assertIn("not HVHZ", html)
        self.assertIn("Florida Product Approval", html)

    def test_indexable_pages_do_not_put_non_hvhz_counties_in_the_hvhz(self):
        hits = []
        for rel, html in self._indexable_html():
            for phrase in self.FORBIDDEN:
                if phrase in html:
                    hits.append(f"{rel}: {phrase}")
        self.assertEqual(hits, [])

    def test_keys_pages_linked_from_the_hub_match_the_monroe_card(self):
        # These two are noindex, but the indexable Florida Keys hub links them.
        for rel in (
            "florida-keys/commercial-storefronts/index.html",
            "florida-keys/impact-windows-hurricane/index.html",
        ):
            html = _read(rel)
            for phrase in self.FORBIDDEN:
                self.assertNotIn(phrase, html, rel)
            self.assertIn("not in the HVHZ", html)
            self.assertIn("Florida Product Approval", html)

    def test_scope_engine_keys_follow_the_monroe_card(self):
        html = _read("scope-engine.html")
        self.assertIn("Florida Keys (WBDR)", html)
        self.assertNotIn("Florida Keys (HVHZ)", html)
        self.assertIn("designWind: '180 mph'", html)
        self.assertNotIn("designWind: '190 mph'", html)
        self.assertIn("hvhz: false, wbd: true,  designWind: '180 mph'", html)
        self.assertIn("Miami-Dade NOA is not required.", html)

    def test_county_cards_keep_published_wind_speeds(self):
        monroe = _read("monroe-county/index.html")
        lee = _read("lee-county/index.html")
        collier = _read("collier-county/index.html")
        self.assertIn("Wind-Borne Debris Region (severe). Florida Keys.", monroe)
        self.assertIn("180 mph (Risk Cat II)", monroe)
        self.assertIn("Wind-Borne Debris Region. Heavy Hurricane Ian impact zone (2022).", lee)
        self.assertIn("160 mph (Risk Cat II)", lee)
        self.assertIn("Wind-Borne Debris Region. Impact-rated assemblies required.", collier)
        self.assertIn("160 mph (Risk Cat II)", collier)
        areas = _read("service-areas.html")
        self.assertIn(">Keys · WBDR<", areas)
        self.assertIn("Monroe County · Keys WBDR", areas)


if __name__ == "__main__":
    unittest.main(verbosity=2)
