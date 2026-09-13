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
            title_of(hub), "Commercial Storefront Installer Florida | Bid in 48 Hrs"
        )
        self.assertIn(PHRASE, title_of(hub).lower())
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

    def test_jacksonville_installer_noindexes_to_statewide_glazier(self):
        html = read("storefront-installer-jacksonville.html")
        self.assertIn("noindex", robots(html))
        self.assertIn("follow", robots(html))
        self.assertEqual(canonical(html), f"{BASE}/storefront-glazier-florida/")
        self.assertNotIn(
            f"{BASE}/storefront-installer-jacksonville.html", sitemap_locs()
        )

    def test_legacy_statewide_installer_noindexes_to_csi_fl(self):
        html = read("storefront-installer-florida.html")
        self.assertIn("noindex", robots(html))
        self.assertIn("follow", robots(html))
        self.assertEqual(
            canonical(html),
            f"{BASE}/commercial-storefront-installer-florida.html",
        )
        self.assertNotIn(f"{BASE}/storefront-installer-florida.html", sitemap_locs())

    def test_statewide_installer_stays_indexable_and_links_keepers(self):
        html = read("commercial-storefront-installer-florida.html")
        title = title_of(html)
        hub_title = title_of(read("florida-commercial-glazing/index.html"))
        self.assertEqual(
            title, "Commercial Storefront Installer Florida | 48-Hr Scope | ACG"
        )
        self.assertNotEqual(title, hub_title)
        self.assertNotIn("Guide", title)
        self.assertNotIn("Bid in 48 Hrs", title)
        self.assertLessEqual(len(title), 60)
        self.assertIn(PHRASE, title.lower())
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
        self.assertNotIn("ACG meets all six", html)

    def test_services_and_contact_link_office_keepers_and_euro_wall(self):
        services = read("services.html")
        contact = read("contact.html")
        for slug, city in (
            (
                "storefront-glazier-west-palm-beach-florida",
                "West Palm Beach",
            ),
            ("storefront-glazier-naples-florida", "Naples"),
            ("storefront-glazier-tampa-florida", "Tampa"),
        ):
            self.assertIn(f"/{slug}/", services)
            self.assertIn(f"/{slug}/", contact)
            self.assertIn(
                f'href="/{slug}/">{city} commercial storefront installer</a>',
                services,
            )
        self.assertIn("/products/euro-wall/", services)
        self.assertIn(
            "<title>Florida Commercial Glazing Services for Contractors | ACG</title>",
            services,
        )
        self.assertIn(
            "<title>Florida Glazing Bid Desk | Send Plans, 48-Hr Reply</title>",
            contact,
        )

    def test_blog_and_services_carry_installer_anchors_to_hub_or_keepers(self):
        blog = read("blog/what-is-a-storefront-glazing-system.html")
        self.assertIn(
            'href="/florida-commercial-glazing/">commercial storefront installer</a>',
            blog,
        )
        self.assertIn('href="/storefront-glazier-west-palm-beach-florida/"', blog)
        spec = read("blog/how-to-spec-commercial-storefront.html")
        self.assertNotIn('href="/storefront-installer-florida.html"', spec)
        self.assertNotIn('href="../storefront-installer-florida.html"', spec)
        self.assertIn(
            'href="/commercial-storefront-installer-florida.html">commercial storefront installer</a>',
            spec,
        )
        self.assertIn(
            'href="/florida-commercial-glazing/">Florida commercial storefront installer</a>',
            spec,
        )
        guide = read("blog/commercial-storefront-installation-guide.html")
        self.assertIn("/commercial-storefront-installer-florida.html", guide)
        self.assertIn("/florida-commercial-glazing/", guide)
        self.assertIn("/storefront-glazier-west-palm-beach-florida/", guide)
        wpb = read(
            "blog/how-to-choose-commercial-glazing-contractor-west-palm-beach.html"
        )
        self.assertIn("/storefront-glazier-west-palm-beach-florida/", wpb)
        tampa = read("blog/how-to-choose-commercial-glazier-tampa-bay.html")
        self.assertIn(
            'href="/storefront-glazier-tampa-florida/" style="color:var(--accent);">commercial storefront installer</a>',
            tampa,
        )
        home = read("index.html")
        self.assertNotIn("/storefront-glazier-boca-raton-florida/", home)
        self.assertIn('href="/florida-commercial-glazing/"', home)
        html = read("commercial-storefront-installer-florida.html")
        self.assertIn(
            "What does a commercial storefront installer do in Florida?",
            html,
        )
        self.assertIn(
            "bidding statewide from West Palm Beach, Naples, and Tampa",
            html,
        )


class SchemaFollowupTests(unittest.TestCase):
    """Missing LocalBusiness / FAQPage on four live pages. Titles stay frozen."""

    FROZEN_TITLES = {
        "index.html": "Commercial Glazing Contractor Florida | ACG",
        "florida-commercial-glazing/index.html": (
            "Commercial Storefront Installer Florida | Bid in 48 Hrs"
        ),
        "commercial-storefront-installer-florida.html": (
            "Commercial Storefront Installer Florida | 48-Hr Scope | ACG"
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
        "storefront-glazier-miami-florida/index.html": (
            "Commercial Storefront Installer Miami | 48-Hr Bids"
        ),
        "storefront-glazier-orlando-florida/index.html": (
            "Commercial Storefront Installer Orlando | 48-Hr Bids"
        ),
        "storefront-glazier-fort-lauderdale-florida/index.html": (
            "Commercial Storefront Installer Fort Lauderdale | Bid"
        ),
        "storefront-glazier-fort-myers-florida/index.html": (
            "Commercial Storefront Installer Fort Myers | 48-Hr Bid"
        ),
        "storefront-glazier-sarasota-florida/index.html": (
            "Commercial Storefront Installer Sarasota | 48-Hr Bid"
        ),
        "storefront-glazier-florida/index.html": (
            "Commercial Storefront Glazier Florida Guide for GCs | ACG"
        ),
        "services.html": (
            "Florida Commercial Glazing Services for Contractors | ACG"
        ),
    }

    def _ld_blocks(self, html: str) -> list:
        return [
            __import__("json").loads(block)
            for block in re.findall(
                r'<script[^>]*type=["\']application/ld\+json["\'][^>]*>(.*?)</script>',
                html,
                re.I | re.S,
            )
        ]

    def _walk(self, obj):
        if isinstance(obj, dict):
            yield obj
            for value in obj.values():
                yield from self._walk(value)
        elif isinstance(obj, list):
            for value in obj:
                yield from self._walk(value)

    def _types(self, node: dict) -> set[str]:
        raw = node.get("@type")
        if isinstance(raw, list):
            return {item for item in raw if isinstance(item, str)}
        return {raw} if isinstance(raw, str) else set()

    def test_frozen_titles_unchanged(self):
        for rel, expected in self.FROZEN_TITLES.items():
            self.assertEqual(title_of(read(rel)), expected, rel)

    def test_hub_has_localbusiness_and_keeps_faqpage(self):
        html = read("florida-commercial-glazing/index.html")
        types = set()
        local_ids = set()
        for block in self._ld_blocks(html):
            for node in self._walk(block):
                found = self._types(node)
                types |= found
                if "LocalBusiness" in found:
                    local_ids.add(node.get("@id"))
                    self.assertEqual(
                        node.get("parentOrganization", {}).get("@id"),
                        f"{BASE}/#organization",
                    )
                    self.assertEqual(node.get("telephone"), "+17724867711")
                    self.assertEqual(
                        node.get("address", {}).get("streetAddress"),
                        "700 S Rosemary Ave Suite 204",
                    )
        self.assertIn("LocalBusiness", types)
        self.assertIn("HomeAndConstructionBusiness", types)
        self.assertIn("FAQPage", types)
        self.assertEqual(local_ids, {f"{BASE}/#localbusiness-west-palm-beach"})

    def test_statewide_glazier_faqpage_uses_on_page_facts(self):
        html = read("storefront-glazier-florida/index.html")
        self.assertIn("How fast can a GC get a Florida storefront bid from ACG?", html)
        self.assertIn("What Florida license covers ACG commercial storefront work?", html)
        self.assertIn(
            "Which Florida offices and markets does ACG cover for storefront?",
            html,
        )
        types = set()
        for block in self._ld_blocks(html):
            for node in self._walk(block):
                types |= self._types(node)
                if "FAQPage" in self._types(node):
                    names = [q["name"] for q in node["mainEntity"]]
                    self.assertEqual(len(names), 3)
                    joined = " ".join(
                        q["acceptedAnswer"]["text"] for q in node["mainEntity"]
                    )
                    self.assertIn("48-hour bid", joined)
                    self.assertIn("CGC #1531993", joined)
                    self.assertIn("79 Florida cities", joined)
                    self.assertNotIn("bonded", joined.lower())
        self.assertIn("FAQPage", types)

    def test_csi_florida_has_localbusiness(self):
        html = read("commercial-storefront-installer-florida.html")
        types = set()
        local_ids = set()
        for block in self._ld_blocks(html):
            for node in self._walk(block):
                found = self._types(node)
                types |= found
                if "LocalBusiness" in found:
                    local_ids.add(node.get("@id"))
                    self.assertEqual(node.get("telephone"), "+17724867711")
                    self.assertEqual(
                        node.get("parentOrganization", {}).get("@id"),
                        f"{BASE}/#organization",
                    )
        self.assertIn("LocalBusiness", types)
        self.assertEqual(local_ids, {f"{BASE}/#localbusiness-west-palm-beach"})

    def test_services_faqpage_and_organization_nap(self):
        html = read("services.html")
        self.assertIn(
            "How fast does ACG bid a Florida commercial glazing package?", html
        )
        orgs = []
        types = set()
        for block in self._ld_blocks(html):
            for node in self._walk(block):
                found = self._types(node)
                types |= found
                if (
                    found == {"Organization"}
                    and node.get("@id") == f"{BASE}/#organization"
                    and node.get("telephone")
                ):
                    orgs.append(node)
        self.assertIn("FAQPage", types)
        self.assertTrue(orgs)
        org = orgs[0]
        self.assertEqual(org.get("telephone"), "+17724867711")
        self.assertEqual(
            org.get("address"),
            {
                "@type": "PostalAddress",
                "streetAddress": "700 S Rosemary Ave Suite 204",
                "addressLocality": "West Palm Beach",
                "addressRegion": "FL",
                "postalCode": "33401",
                "addressCountry": "US",
            },
        )


class RetailDuplicateTests(unittest.TestCase):
    RETAIL_TO_KEEPER = {
        "retail-storefront-installer-tampa/index.html": (
            "storefront-glazier-tampa-florida"
        ),
        "retail-storefront-installer-miami/index.html": (
            "storefront-glazier-miami-florida"
        ),
        "retail-storefront-installer-naples/index.html": (
            "storefront-glazier-naples-florida"
        ),
        "retail-storefront-installer-orlando/index.html": (
            "storefront-glazier-orlando-florida"
        ),
        "retail-storefront-installer-sarasota/index.html": (
            "storefront-glazier-sarasota-florida"
        ),
        "retail-storefront-installer-fort-lauderdale/index.html": (
            "storefront-glazier-fort-lauderdale-florida"
        ),
    }

    def test_retail_city_pages_noindex_to_keepers(self):
        locs = sitemap_locs()
        for rel, slug in self.RETAIL_TO_KEEPER.items():
            html = read(rel)
            with self.subTest(rel=rel):
                self.assertIn("noindex", robots(html))
                self.assertIn("follow", robots(html))
                self.assertEqual(canonical(html), f"{BASE}/{slug}/")
                self.assertNotIn(f"{BASE}/{rel.replace('/index.html', '/')}", locs)

    def test_retail_jacksonville_noindexes_to_statewide_glazier(self):
        html = read("retail-storefront-installer-jacksonville/index.html")
        self.assertIn("noindex", robots(html))
        self.assertIn("follow", robots(html))
        self.assertEqual(canonical(html), f"{BASE}/storefront-glazier-florida/")
        self.assertNotIn(
            f"{BASE}/retail-storefront-installer-jacksonville/",
            sitemap_locs(),
        )


class ThinTemplateContainmentTests(unittest.TestCase):
    TO_KEEPER = {
        "retail-storefront-installer-florida/index.html": "storefront-glazier-florida",
        "restaurant-glazier-florida/index.html": "storefront-glazier-florida",
        "restaurant-glazier-fort-lauderdale/index.html": (
            "storefront-glazier-fort-lauderdale-florida"
        ),
        "restaurant-glazier-miami/index.html": "storefront-glazier-miami-florida",
        "restaurant-glazier-naples/index.html": "storefront-glazier-naples-florida",
        "restaurant-glazier-orlando/index.html": "storefront-glazier-orlando-florida",
        "restaurant-glazier-sarasota/index.html": "storefront-glazier-sarasota-florida",
        "restaurant-glazier-tampa/index.html": "storefront-glazier-tampa-florida",
        "school-glazier-florida/index.html": "storefront-glazier-florida",
        "school-glazier-fort-lauderdale/index.html": (
            "storefront-glazier-fort-lauderdale-florida"
        ),
        "school-glazier-jacksonville/index.html": "storefront-glazier-florida",
        "school-glazier-miami/index.html": "storefront-glazier-miami-florida",
        "school-glazier-naples/index.html": "storefront-glazier-naples-florida",
        "school-glazier-orlando/index.html": "storefront-glazier-orlando-florida",
        "school-glazier-sarasota/index.html": "storefront-glazier-sarasota-florida",
        "school-glazier-tampa/index.html": "storefront-glazier-tampa-florida",
        "commercial-glazier-near-me-miami/index.html": (
            "storefront-glazier-miami-florida"
        ),
        "commercial-glazier-near-me-tampa/index.html": (
            "storefront-glazier-tampa-florida"
        ),
    }

    def test_thin_templates_noindex_to_keepers(self):
        locs = sitemap_locs()
        for rel, slug in self.TO_KEEPER.items():
            html = read(rel)
            with self.subTest(rel=rel):
                self.assertIn("noindex", robots(html))
                self.assertIn("follow", robots(html))
                self.assertEqual(canonical(html), f"{BASE}/{slug}/")
                self.assertNotIn(
                    f"{BASE}/{rel.replace('/index.html', '/')}", locs
                )

    def test_frozen_wpb_near_me_stays_indexable(self):
        html = read("commercial-glazier-near-me-west-palm-beach/index.html")
        self.assertNotIn("noindex", robots(html))
        self.assertEqual(
            canonical(html),
            f"{BASE}/commercial-glazier-near-me-west-palm-beach/",
        )
        self.assertIn(
            f"{BASE}/commercial-glazier-near-me-west-palm-beach/",
            sitemap_locs(),
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
