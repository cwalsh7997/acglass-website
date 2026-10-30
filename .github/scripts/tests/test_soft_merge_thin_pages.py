#!/usr/bin/env python3
"""Soft-merge of thin and duplicate pages onto existing parents.

Files stay on disk. Each merged page is noindex,follow, canonical and og:url
point at the parent, and the URL is absent from every sitemap.
"""

from __future__ import annotations

import re
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path


REPO = Path(__file__).resolve().parents[3]
BASE = "https://acglass.com"
SM_NS = "{http://www.sitemaps.org/schemas/sitemap/0.9}"

# path relative to repo -> canonical parent URL
MERGED = {
    "solarban-vs-viracon-low-e-glass/index.html": f"{BASE}/low-e-glass-coatings-commercial-explained/",
    "pvb-vs-sgp-interlayer-comparison/index.html": f"{BASE}/what-is-pvb-vs-sgp-interlayer/",
    "aluminum-extrusion-grades-commercial-glazing/index.html": f"{BASE}/commercial-aluminum-finishes-pvdf-anodize-powder/",
    "commercial-glazing-for-general-contractors-florida/index.html": f"{BASE}/for-general-contractors/",
    "commercial-glazing-payment-terms-florida/index.html": f"{BASE}/faq.html",
    "commercial-glazing-for-hospitality-developers-florida/index.html": f"{BASE}/hospitality-glazing-florida.html",
    "commercial-glazing-owner-direct-restaurant-florida/index.html": f"{BASE}/restaurant-glazing-contractor.html",
    "gulfside-twelve.html": f"{BASE}/case-study-gulfside-twelve.html",
}

KEEPER_TITLES = {
    "index.html": "<title>Commercial Glazing Contractor Florida | ACG</title>",
    "florida-commercial-glazing/index.html": "<title>Commercial Storefront Installer Florida | Bid in 48 Hrs</title>",
    "commercial-glazing-jacksonville.html": None,
}


def read(rel: str) -> str:
    return (REPO / rel).read_text(encoding="utf-8")


def canonical(html: str) -> str:
    match = re.search(r'<link[^>]+rel="canonical"[^>]+href="([^"]+)"', html, re.I)
    return match.group(1) if match else ""


def robots(html: str) -> str:
    match = re.search(r'<meta[^>]+name="robots"[^>]+content="([^"]+)"', html, re.I)
    return match.group(1) if match else ""


class ThinPageSoftMergeTests(unittest.TestCase):
    def test_merged_pages_stay_and_point_at_parents(self):
        self.assertEqual(len(MERGED), 8)
        for rel, parent in MERGED.items():
            html = read(rel)
            self.assertTrue((REPO / rel).is_file(), rel)
            self.assertEqual(robots(html), "noindex,follow", rel)
            self.assertEqual(canonical(html), parent, rel)
            self.assertIn(f'property="og:url" content="{parent}"', html, rel)
            self.assertIn(f'href="{parent.removeprefix(BASE)}"', html, rel)
            self.assertNotIn('http-equiv="refresh"', html, rel)

    def test_merged_urls_are_absent_from_every_sitemap(self):
        locs = set()
        for path in list(REPO.glob("sitemap*.xml")) + [REPO / ".github/fixtures/sitemap-pages.xml"]:
            root = ET.parse(path).getroot()
            for el in root.iter(f"{SM_NS}loc"):
                if el.text:
                    locs.add(el.text.strip().rstrip("/"))
        master = re.findall(r"<loc>(.*?)</loc>", read("sitemap.xml"))
        # 2026-10-29: +1 ENR Top 600 news post (685 before).
        self.assertEqual(len(master), 686)
        for rel, parent in MERGED.items():
            if rel.endswith("/index.html"):
                url = f"{BASE}/{rel[: -len('index.html')]}".rstrip("/")
            else:
                url = f"{BASE}/{rel}".rstrip("/")
            self.assertNotIn(url, locs, rel)
            self.assertIn(parent.rstrip("/"), locs, parent)

    def test_news_index_stays_indexable(self):
        html = read("news/index.html")
        self.assertNotIn("noindex", robots(html))
        self.assertEqual(canonical(html), f"{BASE}/news/")
        self.assertIn(f"{BASE}/news/", read("sitemap.xml"))
        self.assertIn("datePublished", read("news/acg-350-projects-milestone.html"))
        self.assertIn("datePublished", read("news/acg-tampa-office-expansion.html"))

    def test_keeper_titles_unchanged(self):
        home = read("index.html")
        florida = read("florida-commercial-glazing/index.html")
        jacksonville = read("commercial-glazing-jacksonville.html")
        self.assertIn(KEEPER_TITLES["index.html"], home)
        self.assertIn(KEEPER_TITLES["florida-commercial-glazing/index.html"], florida)
        self.assertNotIn("noindex", robots(home))
        self.assertNotIn("noindex", robots(florida))
        self.assertNotIn("noindex", robots(jacksonville))
        self.assertIn("<title>", jacksonville)
