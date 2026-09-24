"""StayAPT Lafayette is in Louisiana. The blog post must not call it Florida."""

from __future__ import annotations

import json
import re
import unittest
from pathlib import Path


REPO = Path(__file__).resolve().parents[3]
POST = "blog/stayapt-suites-lafayette-glazing.html"
KEEPER = "stayapt-suites-lafayette.html"
FALSE_PLACE = "Lafayette, FL"
HERO = "images/projects/stayapt-lafayette/hero.jpg"
INFOGRAPHIC = "infographic-stayapt-suites-lafayette-glazing"
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
TITLE = re.compile(r"<title[^>]*>(.*?)</title>", re.I | re.S)


class StayaptLafayetteLocationTests(unittest.TestCase):
    def test_blog_post_names_louisiana_and_drops_the_false_claims(self):
        html = (REPO / POST).read_text(encoding="utf-8")
        self.assertIn("Lafayette, LA", html)
        self.assertIn("Lafayette, Louisiana", html)
        self.assertNotIn(FALSE_PLACE, html)
        self.assertNotIn("Lafayette LA County", html)
        self.assertNotIn("150 mph", html)
        self.assertNotIn("atlantic-fields-hero", html)
        self.assertNotIn(INFOGRAPHIC, html)
        self.assertIn(HERO, html)
        self.assertIn(
            'rel="canonical" href="https://acglass.com/blog/stayapt-suites-lafayette-glazing.html"',
            html,
        )
        self.assertNotIn("noindex", html.lower())

    def test_public_citations_do_not_call_the_project_florida(self):
        surfaces = [
            POST,
            "blog/index.html",
            "feed.xml",
            "search-index.json",
            "infographics-index.html",
            "sitemap-images.xml",
            KEEPER,
        ]
        for rel in surfaces:
            text = (REPO / rel).read_text(encoding="utf-8")
            self.assertNotIn(FALSE_PLACE, text, rel)
            self.assertNotIn(INFOGRAPHIC, text, rel)

    def test_keeper_stays_lafayette_louisiana(self):
        html = (REPO / KEEPER).read_text(encoding="utf-8")
        self.assertIn("Lafayette, LA", html)
        self.assertNotIn(FALSE_PLACE, html)

    def test_sitemap_still_lists_the_post_and_frozen_titles_hold(self):
        sitemap = (REPO / "sitemap.xml").read_text(encoding="utf-8")
        locs = re.findall(r"<loc>\s*([^<\s]+)\s*</loc>", sitemap)
        self.assertEqual(len(set(locs)), 784)
        self.assertIn(
            "https://acglass.com/blog/stayapt-suites-lafayette-glazing.html",
            locs,
        )
        for rel, title in FROZEN_TITLES.items():
            html = (REPO / rel).read_text(encoding="utf-8")
            found = re.sub(r"\s+", " ", TITLE.search(html).group(1)).strip()
            self.assertEqual(found, title, rel)


if __name__ == "__main__":
    unittest.main()
