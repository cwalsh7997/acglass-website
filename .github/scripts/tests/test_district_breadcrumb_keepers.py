"""Sitemap district breadcrumbs must cite live keepers, not noindex city roots.

City roots such as /miami/ stay on disk. They are noindex and already
canonical to the office storefront keeper or the Florida hub. Indexable
sitemap pages must use that canonical in BreadcrumbList.

All-glass city templates are a separate contained set and are not in this
sitemap guard. /doral/ is noindex and self-canonical, so the downtown Doral
page has no other live parent to cite. The West Palm Beach near-me page is
byte-frozen, so its crumb stays on /west-palm-beach/.
"""

from __future__ import annotations

import json
import re
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[3]
SKIP_DIRS = {".git", ".github", "node_modules", "_internal", "drafts"}
SM_NS = "{http://www.sitemaps.org/schemas/sitemap/0.9}"
HUB = "https://acglass.com/florida-commercial-glazing/"
HUB_NAME = "Commercial Storefront Installer Florida"
EURO_KEEPER = "https://acglass.com/euro-wall-installer-florida.html"
EURO_MISSING = "https://acglass.com/euro-wall-folding-door-installer/"
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
CITY_KEEPERS = {
    "miami/design-district-miami/index.html": (
        "Miami",
        "https://acglass.com/storefront-glazier-miami-florida/",
    ),
    "tampa/channelside-tampa/index.html": (
        "Tampa",
        "https://acglass.com/storefront-glazier-tampa-florida/",
    ),
    "naples/fifth-avenue-naples/index.html": (
        "Naples",
        "https://acglass.com/storefront-glazier-naples-florida/",
    ),
    "orlando/downtown-orlando/index.html": (
        "Orlando",
        "https://acglass.com/storefront-glazier-orlando-florida/",
    ),
    "west-palm-beach/clematis-street-west-palm-beach/index.html": (
        "West Palm Beach",
        "https://acglass.com/storefront-glazier-west-palm-beach-florida/",
    ),
    "fort-lauderdale/las-olas-fort-lauderdale/index.html": (
        "Fort Lauderdale",
        "https://acglass.com/storefront-glazier-fort-lauderdale-florida/",
    ),
    "sarasota/sarasota-downtown-main-street/index.html": (
        "Sarasota",
        "https://acglass.com/storefront-glazier-sarasota-florida/",
    ),
}
# Byte-frozen. canonical-verify rejects any edit, so its crumb stays on the
# noindex city root even though that root canonicals to the WPB keeper.
BYTE_FROZEN = {
    "commercial-glazier-near-me-west-palm-beach/index.html",
    "impact-windows-palm-beach.html",
}
HUB_DISTRICTS = (
    "aventura/aventura-mall-area/index.html",
    "coral-gables/coral-gables-miracle-mile/index.html",
    "palm-beach/worth-avenue-palm-beach/index.html",
    "st-petersburg/downtown-st-pete/index.html",
)
JSONLD = re.compile(
    r'<script\b[^>]*type=["\']application/ld\+json["\'][^>]*>(.*?)</script>',
    re.I | re.S,
)
TITLE = re.compile(r"<title[^>]*>(.*?)</title>", re.I | re.S)
ROBOTS = re.compile(
    r'<meta\b[^>]*name=["\'](?:robots|googlebot)["\'][^>]*content=["\']([^"\']+)',
    re.I,
)
CANON = re.compile(
    r'<link[^>]+rel=["\']canonical["\'][^>]+href=["\']([^"\']+)',
    re.I,
)


def _crumbs(html: str) -> list[list[tuple[str, str]]]:
    trails = []
    for block in JSONLD.findall(html):
        try:
            data = json.loads(block)
        except json.JSONDecodeError:
            continue
        stack = [data]
        while stack:
            node = stack.pop()
            if isinstance(node, dict):
                if node.get("@type") == "BreadcrumbList":
                    trail = []
                    for item in node.get("itemListElement") or []:
                        if isinstance(item, dict):
                            trail.append((item.get("name") or "", item.get("item") or ""))
                    trails.append(trail)
                stack.extend(value for value in node.values() if isinstance(value, (dict, list)))
            elif isinstance(node, list):
                stack.extend(node)
    return trails


def _url_of(rel: str) -> str:
    if rel == "index.html":
        return "https://acglass.com/"
    if rel.endswith("/index.html"):
        return "https://acglass.com/" + rel[: -len("index.html")]
    return "https://acglass.com/" + rel


def _resolve(url: str) -> str:
    path = url.split("https://acglass.com", 1)[1].split("#")[0].split("?")[0]
    if path in ("", "/"):
        return "index.html"
    if path.endswith("/"):
        return path.lstrip("/") + "index.html"
    return path.lstrip("/")


class DistrictBreadcrumbKeeperTests(unittest.TestCase):
    def test_office_districts_cite_the_city_keeper(self):
        for rel, (name, keeper) in CITY_KEEPERS.items():
            html = (REPO_ROOT / rel).read_text(encoding="utf-8")
            trails = _crumbs(html)
            self.assertEqual(len(trails), 1, rel)
            self.assertEqual(trails[0][1], (name, keeper), rel)

    def test_hub_districts_cite_the_florida_hub(self):
        for rel in HUB_DISTRICTS:
            html = (REPO_ROOT / rel).read_text(encoding="utf-8")
            trails = _crumbs(html)
            self.assertEqual(len(trails), 1, rel)
            self.assertEqual(trails[0][1], (HUB_NAME, HUB), rel)

    def test_sitemap_breadcrumbs_do_not_cite_a_noindex_alias(self):
        pages = {}
        for path in REPO_ROOT.rglob("*.html"):
            rel = path.relative_to(REPO_ROOT)
            if set(rel.parts) & SKIP_DIRS:
                continue
            html = path.read_text(encoding="utf-8", errors="replace")
            robots = ROBOTS.search(html)
            canon = CANON.search(html)
            pages[rel.as_posix()] = {
                "html": html,
                "noindex": bool(robots and "noindex" in robots.group(1).lower()),
                "canon": canon.group(1) if canon else None,
                "url": _url_of(rel.as_posix()),
            }
        sitemap = set()
        root = ET.parse(REPO_ROOT / "sitemap.xml").getroot()
        for loc in root.iter(f"{SM_NS}loc"):
            if loc.text:
                sitemap.add(loc.text.strip().rstrip("/"))
        leaks = []
        for rel, info in pages.items():
            if rel in BYTE_FROZEN:
                continue
            if info["noindex"] or info["url"].rstrip("/") not in sitemap:
                continue
            for trail in _crumbs(info["html"]):
                for name, url in trail:
                    if not isinstance(url, str) or not url.startswith("https://acglass.com"):
                        continue
                    target = _resolve(url)
                    page = pages.get(target)
                    if not page or not page["noindex"] or not page["canon"]:
                        continue
                    canon_rel = _resolve(page["canon"])
                    canon_page = pages.get(canon_rel)
                    if (
                        canon_page
                        and not canon_page["noindex"]
                        and page["canon"].rstrip("/") != page["url"].rstrip("/")
                    ):
                        leaks.append(f"{rel}: {name} -> {url} canonical {page['canon']}")
        self.assertEqual(leaks, [])

    def test_euro_wall_parent_is_the_live_installer(self):
        for rel in (
            "euro-wall-folding-door-installer-naples/index.html",
            "euro-wall-folding-door-installer-miami/index.html",
        ):
            html = (REPO_ROOT / rel).read_text(encoding="utf-8")
            trails = _crumbs(html)
            self.assertEqual(trails[0][1][1], EURO_KEEPER, rel)
            self.assertNotIn(EURO_MISSING, html)
        self.assertFalse((REPO_ROOT / "euro-wall-folding-door-installer" / "index.html").exists())

    def test_doral_stays_self_canonical_and_noindex(self):
        # No live keeper exists for this root, so downtown Doral still names it.
        root = (REPO_ROOT / "doral" / "index.html").read_text(encoding="utf-8")
        self.assertIn('name="robots" content="noindex, follow"', root)
        self.assertIn('rel="canonical" href="https://acglass.com/doral/"', root)
        district = (REPO_ROOT / "doral" / "downtown-doral" / "index.html").read_text(
            encoding="utf-8"
        )
        self.assertIn('"item": "https://acglass.com/doral/"', district)

    def test_city_roots_stay_on_disk(self):
        roots = {
            "miami/index.html": "https://acglass.com/storefront-glazier-miami-florida/",
            "tampa/index.html": "https://acglass.com/storefront-glazier-tampa-florida/",
            "naples/index.html": "https://acglass.com/storefront-glazier-naples-florida/",
            "west-palm-beach/index.html": (
                "https://acglass.com/storefront-glazier-west-palm-beach-florida/"
            ),
            "aventura/index.html": HUB,
        }
        for rel, keeper in roots.items():
            html = (REPO_ROOT / rel).read_text(encoding="utf-8")
            self.assertIn("noindex", html, rel)
            self.assertIn(f'href="{keeper}"', html, rel)

    def test_byte_frozen_near_me_page_keeps_the_city_root_crumb(self):
        html = (
            REPO_ROOT / "commercial-glazier-near-me-west-palm-beach" / "index.html"
        ).read_text(encoding="utf-8")
        trails = _crumbs(html)
        self.assertEqual(
            trails[0][1],
            ("West Palm Beach", "https://acglass.com/west-palm-beach/"),
        )

    def test_body_links_to_contained_city_urls_stay(self):
        # Containment left these hrefs in place. This pass only fixes schema.
        near_me = (
            REPO_ROOT / "commercial-glazier-near-me-west-palm-beach" / "index.html"
        ).read_text(encoding="utf-8")
        self.assertIn('href="/west-palm-beach/"', near_me)
        district = (REPO_ROOT / "miami" / "design-district-miami" / "index.html").read_text(
            encoding="utf-8"
        )
        self.assertIn('href="/miami/commercial-storefronts/"', district)

    def test_frozen_titles_are_unchanged(self):
        for rel, expected in FROZEN_TITLES.items():
            html = (REPO_ROOT / rel).read_text(encoding="utf-8")
            match = TITLE.search(html)
            self.assertIsNotNone(match, rel)
            title = re.sub(r"\s+", " ", match.group(1)).strip()
            self.assertEqual(title, expected, rel)


if __name__ == "__main__":
    unittest.main()
