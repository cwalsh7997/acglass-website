#!/usr/bin/env python3
"""Crawl-batch-2 guards: author family, city canonical-to-noindex, RFQ, orphans."""

from __future__ import annotations

import os
import re
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path
from urllib.parse import urljoin


REPO_ROOT = Path(__file__).resolve().parents[3]
SM_NS = "{http://www.sitemaps.org/schemas/sitemap/0.9}"
BASE = "https://acglass.com"
SKIP_DIRS = {".git", ".github", "_internal", "node_modules", "dealer"}

AUTHOR_KEEPERS = (
    "authors/connor-walsh.html",
    "authors/rielly-walsh.html",
)
AUTHOR_ALIASES = (
    ("author/connor-walsh/index.html", "/authors/connor-walsh.html"),
    ("author/rielly-walsh/index.html", "/authors/rielly-walsh.html"),
    ("author/connor-walsh.html", "/authors/connor-walsh.html"),
    ("author/rielly-walsh.html", "/authors/rielly-walsh.html"),
)
LEAVE_CITY_ROOTS = ("west-palm-beach", "naples", "tampa")
KEEPER_CITY_ROOTS = (
    "miami",
    "orlando",
    "fort-lauderdale",
    "fort-myers",
    "sarasota",
)
KEEPER_GLAZIERS = (
    "storefront-glazier-west-palm-beach-florida",
    "storefront-glazier-naples-florida",
    "storefront-glazier-tampa-florida",
    "storefront-glazier-miami-florida",
    "storefront-glazier-orlando-florida",
    "storefront-glazier-fort-lauderdale-florida",
    "storefront-glazier-fort-myers-florida",
    "storefront-glazier-sarasota-florida",
)
WAVE4 = {
    "about.html",
    "contact.html",
    "portfolio.html",
    "west-palm-beach-commercial-glazing.html",
    "index.html",
    "florida-commercial-glazing/index.html",
    "miami-dade-noa-explained/index.html",
    "blog/what-is-division-08-construction.html",
    "blog/commercial-glazing-warranties-florida.html",
    "blog/commercial-glazing-submittal-process-guide.html",
    "blog/what-does-a-glazing-contractor-do.html",
    "blog/florida-building-codes-commercial-glazing-2026.html",
    "blog/commercial-glazing-project-turnaround-time-florida.html",
}
HUBS = (
    "services.html",
    "locations.html",
    "manufacturers.html",
    "blog/index.html",
    "storefront-glazier-west-palm-beach-florida/index.html",
    "storefront-glazier-naples-florida/index.html",
    "storefront-glazier-tampa-florida/index.html",
    "storefront-glazier-miami-florida/index.html",
    "storefront-glazier-orlando-florida/index.html",
    "storefront-glazier-fort-lauderdale-florida/index.html",
    "storefront-glazier-fort-myers-florida/index.html",
    "storefront-glazier-sarasota-florida/index.html",
)
ORPHAN_TARGETS = (
    "/architect-resources.html",
    "/authors/connor-walsh.html",
    "/authors/rielly-walsh.html",
    "/blog-2026/commercial-glazing-rfq-checklist-for-architects/",
    "/eswindows-installer-miami.html",
    "/euro-wall-folding-door-installer-naples/",
    "/fort-lauderdale/all-glass-entrances/",
    "/orlando/all-glass-entrances/",
    "/tampa/all-glass-entrances/",
    "/sarasota/all-glass-entrances/",
    "/shop-drawings-glazing-explained/",
    "/west-palm-beach/clematis-street-west-palm-beach/",
)

CANON_RE = re.compile(
    r'<link[^>]+rel=["\']canonical["\'][^>]+href=["\']([^"\']+)', re.I
)
CANON_RE2 = re.compile(
    r'<link[^>]+href=["\']([^"\']+)["\'][^>]+rel=["\']canonical["\']', re.I
)
ROBOTS_RE = re.compile(
    r'<meta[^>]+name=["\']robots["\'][^>]+content=["\']([^"\']+)', re.I
)
ROBOTS_RE2 = re.compile(
    r'<meta[^>]+content=["\']([^"\']+)["\'][^>]+name=["\']robots["\']', re.I
)
REFRESH_RE = re.compile(r'<meta[^>]+http-equiv=["\']refresh["\']', re.I)
HREF_RE = re.compile(r'<a\b[^>]*?\bhref=["\']([^"\'#?]+)', re.I)
RFQ_RE = re.compile(
    r"<!-- ACG RFQ BLOCK -->(.*?)<!-- /ACG RFQ BLOCK -->", re.S
)
BID_RE = re.compile(r'<a href="([^"]+)"[^>]*>Request a bid', re.I)


def read(rel: str) -> str:
    return (REPO_ROOT / rel).read_text(encoding="utf-8")


def canonical(html: str) -> str:
    m = CANON_RE.search(html) or CANON_RE2.search(html)
    return m.group(1).strip() if m else ""


def robots(html: str) -> str:
    m = ROBOTS_RE.search(html) or ROBOTS_RE2.search(html)
    return (m.group(1) if m else "").lower()


def is_noindex(html: str) -> bool:
    r = robots(html)
    return "noindex" in r or r == "none"


def sitemap_locs() -> set[str]:
    locs: set[str] = set()
    for path in REPO_ROOT.glob("sitemap*.xml"):
        root = ET.parse(path).getroot()
        for el in root.iter(f"{SM_NS}loc"):
            if el.text:
                locs.add(el.text.strip())
    return locs


def url_for(path: Path) -> str:
    rel = path.relative_to(REPO_ROOT).as_posix()
    if rel.endswith("/index.html"):
        return "/" + rel[: -len("index.html")]
    return "/" + rel


def resolve(src: Path, href: str) -> str | None:
    if href.startswith(("mailto:", "tel:", "javascript:", "http://", "https://")):
        if href.startswith(BASE):
            return href[len(BASE) :] or "/"
        return None
    if href.startswith("/"):
        return href
    return urljoin(url_for(src), href)


class AuthorFamilyTests(unittest.TestCase):
    def test_authors_html_family_stays_indexable_and_in_sitemap(self):
        locs = sitemap_locs()
        for rel in AUTHOR_KEEPERS:
            html = read(rel)
            self.assertFalse(is_noindex(html), rel)
            self.assertFalse(REFRESH_RE.search(html), rel)
            self.assertEqual(canonical(html), f"{BASE}/{rel}")
            self.assertIn(f"{BASE}/{rel}", locs)

    def test_author_directory_family_stubs_onto_authors_html(self):
        locs = sitemap_locs()
        for rel, dest in AUTHOR_ALIASES:
            html = read(rel)
            self.assertTrue(is_noindex(html), rel)
            self.assertTrue(REFRESH_RE.search(html), rel)
            self.assertEqual(canonical(html), f"{BASE}{dest}")
            self.assertIn(dest, html)
            self.assertIn("window.location.replace", html)
        self.assertNotIn(f"{BASE}/author/connor-walsh/", locs)
        self.assertNotIn(f"{BASE}/author/rielly-walsh/", locs)

    def test_indexable_pages_do_not_href_author_directory_aliases(self):
        leftovers = []
        for dirpath, dirnames, filenames in os.walk(REPO_ROOT):
            dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
            for fn in filenames:
                if not fn.endswith(".html"):
                    continue
                path = Path(dirpath) / fn
                rel = path.relative_to(REPO_ROOT).as_posix()
                if rel.startswith("author/"):
                    continue
                html = path.read_text(encoding="utf-8", errors="replace")
                if is_noindex(html) or REFRESH_RE.search(html):
                    continue
                if re.search(r'href=["\'][^"\']*/author/(?:connor|rielly)-walsh/?', html):
                    leftovers.append(rel)
        self.assertEqual(leftovers, [])


class CityCanonicalTests(unittest.TestCase):
    def test_no_city_root_canonicals_to_a_noindex_storefront_glazier(self):
        broken = []
        for path in sorted(REPO_ROOT.glob("*/index.html")):
            city = path.parent.name
            if city.startswith("storefront-glazier-"):
                continue
            html = path.read_text(encoding="utf-8")
            if REFRESH_RE.search(html):
                continue
            canon = canonical(html)
            if "storefront-glazier-" not in canon:
                continue
            slug = canon.rstrip("/").split("/")[-1]
            target = REPO_ROOT / slug / "index.html"
            if target.is_file() and is_noindex(target.read_text(encoding="utf-8")):
                broken.append(f"/{city}/ -> {canon}")
        self.assertEqual(broken, [])

    def test_wave4_office_metros_left_to_wave4(self):
        # Wave-4 owns these files. Do not retarget them in this batch.
        for city in LEAVE_CITY_ROOTS:
            html = read(f"{city}/index.html")
            self.assertEqual(canonical(html), f"{BASE}/{city}/")
            self.assertFalse(is_noindex(html))

    def test_satellite_city_roots_still_point_at_indexable_keepers(self):
        for city in KEEPER_CITY_ROOTS:
            html = read(f"{city}/index.html")
            canon = canonical(html)
            self.assertIn(f"/storefront-glazier-{city}-florida/", canon)
            slug = canon.rstrip("/").split("/")[-1]
            target = read(f"{slug}/index.html")
            self.assertFalse(is_noindex(target), city)

    def test_eight_keepers_remain_indexable_self_canonical(self):
        locs = sitemap_locs()
        for slug in KEEPER_GLAZIERS:
            html = read(f"{slug}/index.html")
            self.assertFalse(is_noindex(html), slug)
            self.assertEqual(canonical(html), f"{BASE}/{slug}/")
            self.assertIn(f"{BASE}/{slug}/", locs)

    def test_wave2_templates_stay_noindex_self_canonical(self):
        count = 0
        for path in REPO_ROOT.glob("storefront-glazier-*-florida/index.html"):
            slug = path.parent.name
            if slug in KEEPER_GLAZIERS or slug == "storefront-glazier-florida":
                continue
            html = path.read_text(encoding="utf-8")
            self.assertTrue(is_noindex(html), slug)
            self.assertEqual(canonical(html), f"{BASE}/{slug}/")
            count += 1
        self.assertEqual(count, 93)

    def test_all_glass_entrances_city_pages_were_not_noindexed(self):
        pages = list(REPO_ROOT.glob("*/all-glass-entrances/index.html"))
        self.assertGreaterEqual(len(pages), 70)
        noindexed = [
            p.parent.parent.name
            for p in pages
            if is_noindex(p.read_text(encoding="utf-8"))
        ]
        self.assertEqual(noindexed, [])


class RfqCtaTests(unittest.TestCase):
    def test_non_wave4_drawing_rfq_primary_goes_to_send_plans(self):
        leftovers = []
        missing_secondary = []
        for dirpath, dirnames, filenames in os.walk(REPO_ROOT):
            dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
            for fn in filenames:
                if not fn.endswith(".html"):
                    continue
                path = Path(dirpath) / fn
                rel = path.relative_to(REPO_ROOT).as_posix()
                if rel in WAVE4:
                    continue
                html = path.read_text(encoding="utf-8", errors="replace")
                if "<!-- ACG RFQ BLOCK -->" not in html:
                    continue
                for block in RFQ_RE.findall(html):
                    if "Send us the drawings" not in block:
                        continue
                    hrefs = BID_RE.findall(block)
                    if not hrefs:
                        continue
                    if hrefs != ["/send-plans.html"]:
                        leftovers.append((rel, hrefs))
                    if ">Scope Engine</a>" not in block:
                        missing_secondary.append(rel)
        self.assertEqual(leftovers, [])
        self.assertEqual(missing_secondary, [])

    def test_wave4_rfq_files_were_not_retargeted(self):
        # Leave Wave-4 title-set files alone, including leftover mixed CTAs.
        html = read("blog/what-is-division-08-construction.html")
        block = RFQ_RE.search(html).group(1)
        self.assertEqual(BID_RE.findall(block), ["/scope-engine.html"])


class OrphanInboundTests(unittest.TestCase):
    def test_hubs_link_selected_sitemap_orphans(self):
        locs = {u[len(BASE):] or "/" for u in sitemap_locs() if u.startswith(BASE)}
        found = {u: False for u in ORPHAN_TARGETS}
        for rel in HUBS:
            path = REPO_ROOT / rel
            html = path.read_text(encoding="utf-8")
            for raw in HREF_RE.findall(html):
                dest = resolve(path, raw)
                if dest in found:
                    found[dest] = True
        missing = [u for u, ok in found.items() if not ok]
        self.assertEqual(missing, [])
        for u in ORPHAN_TARGETS:
            self.assertIn(u, locs)

    def test_hubs_were_not_turned_into_directory_dumps(self):
        for rel in ("services.html", "locations.html", "manufacturers.html"):
            hrefs = HREF_RE.findall(read(rel))
            self.assertLess(len(hrefs), 180, rel)


if __name__ == "__main__":
    unittest.main(verbosity=2)
