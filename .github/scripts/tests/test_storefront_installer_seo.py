#!/usr/bin/env python3
"""Keep commercial storefront installer intent on the eight keepers.

City installer HTML that duplicated those keepers must noindex and
canonicalise away, and must leave every sitemap.
"""

from __future__ import annotations

import re
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[3]
SM_NS = "{http://www.sitemaps.org/schemas/sitemap/0.9}"
BASE = "https://acglass.com"
PHRASE = "commercial storefront installer"

KEEPERS = (
    "storefront-glazier-west-palm-beach-florida",
    "storefront-glazier-naples-florida",
    "storefront-glazier-tampa-florida",
    "storefront-glazier-miami-florida",
    "storefront-glazier-orlando-florida",
    "storefront-glazier-fort-lauderdale-florida",
    "storefront-glazier-fort-myers-florida",
    "storefront-glazier-sarasota-florida",
)
OFFICE_METROS = ("west-palm-beach", "naples", "tampa")
INSTALLER_TO_KEEPER = {
    "storefront-installer-west-palm-beach.html": "storefront-glazier-west-palm-beach-florida",
    "storefront-installer-naples.html": "storefront-glazier-naples-florida",
    "storefront-installer-tampa.html": "storefront-glazier-tampa-florida",
    "storefront-installer-miami.html": "storefront-glazier-miami-florida",
    "storefront-installer-orlando.html": "storefront-glazier-orlando-florida",
    "storefront-installer-fort-lauderdale.html": "storefront-glazier-fort-lauderdale-florida",
}
CANON_RE = re.compile(
    r'<link[^>]+rel=["\']canonical["\'][^>]+href=["\']([^"\']+)', re.I
)
CANON_RE2 = re.compile(
    r'<link[^>]+href=["\']([^"\']+)["\'][^>]+rel=["\']canonical["\']', re.I
)
ROBOTS_RE = re.compile(
    r'<meta[^>]+name=["\']robots["\'][^>]+content=["\']([^"\']+)', re.I
)
TITLE_RE = re.compile(r"<title>(.*?)</title>", re.I | re.S)
DESC_RE = re.compile(
    r'<meta[^>]+name=["\']description["\'][^>]+content=["\']([^"\']+)', re.I
)
H1_RE = re.compile(r"<h1[^>]*>(.*?)</h1>", re.I | re.S)


def read(rel: str) -> str:
    return (REPO_ROOT / rel).read_text(encoding="utf-8")


def canonical(html: str) -> str:
    m = CANON_RE.search(html) or CANON_RE2.search(html)
    return m.group(1).strip() if m else ""


def robots(html: str) -> str:
    m = ROBOTS_RE.search(html)
    return (m.group(1) if m else "").lower()


def title_of(html: str) -> str:
    m = TITLE_RE.search(html)
    return re.sub(r"\s+", " ", m.group(1)).strip() if m else ""


def desc_of(html: str) -> str:
    m = DESC_RE.search(html)
    return m.group(1) if m else ""


def h1_of(html: str) -> str:
    m = H1_RE.search(html)
    if not m:
        return ""
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", m.group(1))).strip()


def sitemap_locs() -> set[str]:
    locs: set[str] = set()
    for path in REPO_ROOT.glob("sitemap*.xml"):
        root = ET.parse(path).getroot()
        for el in root.iter(f"{SM_NS}loc"):
            if el.text:
                locs.add(el.text.strip())
    return locs


class KeeperPhraseTests(unittest.TestCase):
    def test_eight_keepers_name_commercial_storefront_installer(self):
        for slug in KEEPERS:
            html = read(f"{slug}/index.html")
            with self.subTest(slug=slug):
                self.assertIn(PHRASE, title_of(html).lower())
                self.assertIn(PHRASE, desc_of(html).lower())
                self.assertIn(PHRASE, h1_of(html).lower())
                self.assertGreaterEqual(html.lower().count(PHRASE), 3)
                self.assertFalse("noindex" in robots(html))
                self.assertEqual(canonical(html), f"{BASE}/{slug}/")

    def test_office_metros_still_canonicalise_to_keepers(self):
        for city in OFFICE_METROS:
            html = read(f"{city}/index.html")
            self.assertEqual(
                canonical(html),
                f"{BASE}/storefront-glazier-{city}-florida/",
            )
            self.assertNotIn("noindex", robots(html))


class HubTests(unittest.TestCase):
    def test_hub_weaves_installer_and_stays_unique_vs_homepage(self):
        hub = read("florida-commercial-glazing/index.html")
        home = read("index.html")
        self.assertEqual(
            title_of(hub), "Commercial Glazing Contractor Florida | Bid in 48 Hrs"
        )
        self.assertIn(PHRASE, h1_of(hub).lower())
        self.assertNotEqual(title_of(hub), title_of(home))
        self.assertEqual(
            title_of(home), "Commercial Glazing Contractor Florida | ACG"
        )
        for city, slug in (
            ("West Palm Beach", "storefront-glazier-west-palm-beach-florida"),
            ("Naples", "storefront-glazier-naples-florida"),
            ("Tampa", "storefront-glazier-tampa-florida"),
        ):
            needle = (
                f'href="/{slug}/">Commercial storefront installer, {city}</a>'
            )
            self.assertIn(needle, hub)


class CannibalizationTests(unittest.TestCase):
    def test_city_installer_html_noindexes_to_keepers(self):
        locs = sitemap_locs()
        for rel, slug in INSTALLER_TO_KEEPER.items():
            html = read(rel)
            with self.subTest(rel=rel):
                self.assertIn("noindex", robots(html))
                self.assertIn("follow", robots(html))
                self.assertEqual(canonical(html), f"{BASE}/{slug}/")
                self.assertNotIn(f"{BASE}/{rel}", locs)

    def test_jacksonville_installer_stays_primary_without_a_keeper(self):
        html = read("storefront-installer-jacksonville.html")
        self.assertNotIn("noindex", robots(html))
        self.assertEqual(
            canonical(html),
            f"{BASE}/storefront-installer-jacksonville.html",
        )
        self.assertIn(
            f"{BASE}/storefront-installer-jacksonville.html", sitemap_locs()
        )

    def test_statewide_installer_stays_indexable_and_links_keepers(self):
        html = read("commercial-storefront-installer-florida.html")
        self.assertIn(PHRASE, title_of(html).lower())
        self.assertNotIn("noindex", robots(html))
        self.assertEqual(
            canonical(html),
            f"{BASE}/commercial-storefront-installer-florida.html",
        )
        self.assertIn(
            f"{BASE}/commercial-storefront-installer-florida.html",
            sitemap_locs(),
        )
        for slug in KEEPERS:
            self.assertIn(f"/{slug}/", html)

    def test_wpb_installer_copy_is_installer_specifier_not_authorized(self):
        html = read("storefront-installer-west-palm-beach.html")
        self.assertNotRegex(html, r"authoriz(?:ed|ation)", re.I)
        self.assertNotRegex(html, r"factory[- ]certif", re.I)
        self.assertIn("installs and specifies", html)


if __name__ == "__main__":
    unittest.main(verbosity=2)
