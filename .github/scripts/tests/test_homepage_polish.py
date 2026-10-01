#!/usr/bin/env python3
"""Homepage conversion and accuracy outcomes for the Florida-GC landing page."""

from __future__ import annotations

import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
HOME = (ROOT / "index.html").read_text(encoding="utf-8")
CSS = (ROOT / "css" / "acg-architectural.css").read_text(encoding="utf-8")


def _visible(html: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", html))


class HomepagePolishTests(unittest.TestCase):
    def test_ocean_prime_is_one_opening_not_full_facade(self):
        self.assertIn('href="/ocean-prime-ft-lauderdale.html"', HOME)
        self.assertNotIn('href="/projects/ocean-prime-ft-lauderdale.html"', HOME)
        self.assertIn("one Euro-Wall opening", HOME)
        self.assertIn("not the full facade", HOME)
        self.assertNotIn("full façade", HOME)
        self.assertNotIn("full facade package", HOME.lower())

    def test_midway_tn_is_marked_supply_only(self):
        # The 2026-10-01 redesign dropped the project-geography map. If Midway,
        # TN returns to the homepage it must still be marked supply-only.
        if "Midway, TN" in HOME:
            self.assertIn("Supply-only window package", HOME)
        self.assertNotIn("Tennessee installation", HOME)

    def test_hero_names_a_written_bid_and_omits_office_cities(self):
        h1 = re.search(r"<h1\b[^>]*>(.*?)</h1>", HOME, re.S).group(1)
        h1_text = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", h1)).strip()
        self.assertEqual("Commercial glazing. Written bid in 48 hours.", h1_text)
        sub = re.search(r'<p class="hero-sub">(.*?)</p>', HOME, re.S).group(1)
        self.assertIn("Storefront, curtain wall, and hurricane-impact.", sub)
        self.assertNotIn("West Palm Beach", sub)
        self.assertNotIn("Naples", sub)
        self.assertNotIn("Tampa", sub)

    def test_florida_proof_comes_before_federal_theater(self):
        record = HOME.index('id="work"')
        scope = HOME.index('id="scope"')
        markets = HOME.index('id="markets"')
        federal = HOME.index('id="federal-registrations"')
        self.assertLess(record, markets)
        self.assertLess(scope, markets)
        self.assertLess(markets, federal)

    def test_send_plans_is_the_dominant_hero_cta(self):
        start = HOME.index('class="hero"')
        hero = HOME[start : HOME.index("</section>", start)]
        self.assertIn('class="hero-cta" href="/send-plans.html">Send Us Plans</a>', hero)
        self.assertNotIn('class="btn btn-ghost"', hero)
        self.assertIn("Request capability statement", hero)
        creds = HOME.index('class="credentials"')
        self.assertNotIn('class="hero-cta"', HOME[creds : HOME.index("</main>")])

    def test_social_description_is_florida_gc_not_federal_lead(self):
        og = re.search(
            r'property="og:description"[^>]*content="([^"]*)"', HOME
        ).group(1)
        tw = re.search(
            r'name="twitter:description"[^>]*content="([^"]*)"', HOME
        ).group(1)
        self.assertEqual(og, tw)
        self.assertTrue(og.startswith("Florida's commercial glazing contractor"))
        self.assertNotIn("Federal-ready", og)
        self.assertNotIn("SAM.gov", og)
        self.assertIn("48 hrs", og)
        self.assertIn("CGC", og)

    def test_tennessee_is_not_parked_under_central_florida(self):
        markets = HOME[HOME.index('id="markets"') : HOME.index('class="coverage-bottom"')]
        central = markets[markets.index("Central") : markets.index("home-tail")]
        self.assertNotIn("Tennessee", central)
        self.assertNotIn("Nashville", central)
        self.assertIn("Tennessee glazing supply and consulting", markets)

    def test_favicon_paths_are_root_relative(self):
        self.assertIn('href="/images/favicon-32.png"', HOME)
        self.assertIn('href="/images/apple-touch-icon.png"', HOME)
        self.assertNotIn('href="images/favicon-32.png"', HOME)
        self.assertNotIn('href="images/apple-touch-icon.png"', HOME)

    def test_cgc_blurb_does_not_name_a_qualifier(self):
        self.assertIn("CGC #1531993", HOME)
        self.assertNotIn("owner-operator who runs the work", HOME)
        self.assertNotIn("Jeffrey", HOME)
        at = HOME.index("Florida contractor license")
        licensed = HOME[at - 200 : at + 400]
        self.assertNotIn("Connor", licensed)

    def test_project_and_geo_cards_have_spaced_accessible_names(self):
        start = HOME.index('class="record-more"')
        strip = HOME[start : HOME.index("</section>", start)]
        self.assertNotRegex(strip, r"</span><h[34]>")
        self.assertIn('aria-label="Fort Lauderdale Ocean Prime One Euro-Wall opening"', strip)
        if "geo-projects" in HOME:
            geo = HOME[HOME.index("geo-projects") : HOME.index("geo-foot")]
            self.assertNotIn("</span><b>", geo)

    def test_sticky_header_has_scroll_padding(self):
        self.assertIn("scroll-padding-top", CSS)
        self.assertIn("6.25rem", CSS)


if __name__ == "__main__":
    unittest.main(verbosity=2)
