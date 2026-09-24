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
    "storefront-glazier-stuart-florida",
    "storefront-glazier-west-palm-beach-florida",
    "storefront-glazier-naples-florida",
    "storefront-glazier-tampa-florida",
    "storefront-glazier-miami-florida",
    "storefront-glazier-orlando-florida",
    "storefront-glazier-fort-lauderdale-florida",
    "storefront-glazier-fort-myers-florida",
    "storefront-glazier-sarasota-florida",
)
THIN_CITY_TEMPLATES = (
    "commercial-glazing-apopka.html",
    "commercial-glazing-brandon.html",
    "commercial-glazing-coconut-creek.html",
    "commercial-glazing-coral-springs.html",
    "commercial-glazing-greenacres.html",
    "commercial-glazing-homestead.html",
    "commercial-glazing-largo.html",
    "commercial-glazing-lauderhill.html",
    "commercial-glazing-lehigh-acres.html",
    "commercial-glazing-margate.html",
    "commercial-glazing-melbourne.html",
    "commercial-glazing-miami-gardens.html",
    "commercial-glazing-miramar.html",
    "commercial-glazing-north-port.html",
    "commercial-glazing-pinellas-park.html",
    "commercial-glazing-plantation.html",
    "commercial-glazing-riverview.html",
    "commercial-glazing-sanford.html",
    "commercial-glazing-spring-hill.html",
    "commercial-glazing-st-cloud.html",
    "commercial-glazing-sunrise.html",
    "commercial-glazing-tamarac.html",
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

    def test_wave4_office_metros_noindex_to_indexable_keepers(self):
        # Office city roots stay live and still canonicalize to the indexable
        # keepers. They are noindex,follow so they stop competing in the index.
        for city in LEAVE_CITY_ROOTS:
            html = read(f"{city}/index.html")
            keeper = f"{BASE}/storefront-glazier-{city}-florida/"
            self.assertEqual(canonical(html), keeper)
            self.assertEqual(robots(html), "noindex,follow")
            self.assertFalse(is_noindex(read(f"storefront-glazier-{city}-florida/index.html")))

    def test_leftover_city_roots_noindex_to_hub_not_noindex_templates(self):
        # SEO: never canonical-to-noindex. Leftover city roots stay live,
        # canonicalize to the Florida hub, and are noindex,follow so they
        # stop competing with that hub. Leave keeper files indexable.
        contained = []
        bad = []
        hub = f"{BASE}/florida-commercial-glazing/"
        for path in sorted(REPO_ROOT.glob("storefront-glazier-*-florida/index.html")):
            slug = path.parent.name
            city = slug[len("storefront-glazier-") : -len("-florida")]
            if (
                city in LEAVE_CITY_ROOTS
                or city in KEEPER_CITY_ROOTS
                or slug == "storefront-glazier-florida"
            ):
                continue
            city_page = REPO_ROOT / city / "index.html"
            if not city_page.is_file():
                continue
            glazier_html = path.read_text(encoding="utf-8")
            # GitHub Pages 404 stubs are noindex + meta-refresh to a keeper.
            # They are not wave-2 templates and must not pull leftover city
            # roots (e.g. /jacksonville/) into this hub-canonical check.
            if REFRESH_RE.search(glazier_html) or not is_noindex(glazier_html):
                continue
            html = city_page.read_text(encoding="utf-8")
            if REFRESH_RE.search(html):
                continue
            contained.append(city)
            if robots(html) != "noindex,follow":
                bad.append(f"/{city}/ robots={robots(html)!r}")
            canon = canonical(html)
            if canon != hub:
                bad.append(f"/{city}/ -> {canon}")
            if "storefront-glazier-" in canon:
                target = REPO_ROOT / canon.rstrip("/").split("/")[-1] / "index.html"
                if target.is_file() and is_noindex(target.read_text(encoding="utf-8")):
                    bad.append(f"/{city}/ still points at noindex {canon}")
        self.assertGreaterEqual(len(contained), 60)
        self.assertEqual(bad, [])
        # Slug mismatches from the live leftover set (hollywood-florida vs
        # storefront-glazier-hollywood-florida, winter-heaven vs winter-haven, …).
        for city in (
            "gulfstream",
            "hollywood-florida",
            "key-biscayne-village",
            "miami-shores-village",
            "palmetto-bay-village",
            "st-petersburg",
            "winter-heaven",
        ):
            html = read(f"{city}/index.html")
            self.assertEqual(canonical(html), hub, city)
            self.assertEqual(robots(html), "noindex,follow", city)
        locs = sitemap_locs()
        self.assertNotIn(f"{BASE}/boca-raton/", locs)

    def test_satellite_city_roots_still_point_at_indexable_keepers(self):
        for city in KEEPER_CITY_ROOTS:
            html = read(f"{city}/index.html")
            canon = canonical(html)
            self.assertEqual(robots(html), "noindex,follow", city)
            self.assertIn(f"/storefront-glazier-{city}-florida/", canon)
            slug = canon.rstrip("/").split("/")[-1]
            target = read(f"{slug}/index.html")
            self.assertFalse(is_noindex(target), city)

    def test_jacksonville_and_stuart_roots_noindex_without_touching_keepers(self):
        jax = read("jacksonville/index.html")
        self.assertEqual(robots(jax), "noindex,follow")
        self.assertEqual(
            canonical(jax), f"{BASE}/commercial-glazing-jacksonville.html"
        )
        self.assertFalse(is_noindex(read("commercial-glazing-jacksonville.html")))
        stuart = read("stuart/index.html")
        self.assertEqual(robots(stuart), "noindex,follow")
        self.assertEqual(canonical(stuart), f"{BASE}/florida-commercial-glazing/")
        self.assertFalse(is_noindex(read("storefront-glazier-stuart-florida/index.html")))
        self.assertFalse(is_noindex(read("florida-commercial-glazing/index.html")))

    def test_sanford_city_root_stays_self_canonical_and_indexable(self):
        html = read("sanford/index.html")
        self.assertNotIn("noindex", robots(html))
        self.assertEqual(canonical(html), f"{BASE}/sanford/")
        self.assertIn(f"{BASE}/sanford/", sitemap_locs())

    def test_nine_keepers_remain_indexable_self_canonical(self):
        locs = sitemap_locs()
        for slug in KEEPER_GLAZIERS:
            html = read(f"{slug}/index.html")
            self.assertFalse(is_noindex(html), slug)
            self.assertEqual(canonical(html), f"{BASE}/{slug}/")
            self.assertIn(f"{BASE}/{slug}/", locs)

    def test_thin_city_templates_are_noindex_self_canonical_and_off_sitemap(self):
        locs = sitemap_locs()
        self.assertEqual(len(THIN_CITY_TEMPLATES), 22)
        for rel in THIN_CITY_TEMPLATES:
            html = read(rel)
            self.assertEqual(robots(html), "noindex,follow", rel)
            self.assertEqual(canonical(html), f"{BASE}/{rel}")
            self.assertNotIn(f"{BASE}/{rel}", locs)
            self.assertTrue((REPO_ROOT / rel).is_file(), rel)

    def test_gc_alias_noindexes_to_general_contractors(self):
        html = read("gc.html")
        self.assertEqual(robots(html), "noindex,follow")
        self.assertEqual(canonical(html), f"{BASE}/for-general-contractors/")
        self.assertNotIn(f"{BASE}/gc.html", sitemap_locs())
        self.assertTrue((REPO_ROOT / "gc.html").is_file())

    def test_wave2_templates_stay_noindex_self_canonical(self):
        count = 0
        for path in REPO_ROOT.glob("storefront-glazier-*-florida/index.html"):
            slug = path.parent.name
            if slug in KEEPER_GLAZIERS or slug == "storefront-glazier-florida":
                continue
            html = path.read_text(encoding="utf-8")
            if REFRESH_RE.search(html):
                continue
            self.assertTrue(is_noindex(html), slug)
            self.assertEqual(canonical(html), f"{BASE}/{slug}/")
            count += 1
        self.assertEqual(count, 92)

    def test_sitemap_all_glass_city_pages_are_noindex_self_canonical(self):
        # Weekly hygiene 2026-09-08: the 28 city URLs that were still in
        # sitemaps take the wave-2 containment (noindex,follow + self-canonical
        # + sitemap drop). The hub stays indexable. The 49 zero-impression
        # city pages stay hub-canonical and are not noindexed.
        hub = f"{BASE}/all-glass-entrances/"
        pages = list(REPO_ROOT.glob("*/all-glass-entrances/index.html"))
        self.assertEqual(len(pages), 77)
        noindexed = []
        hub_canonical = []
        for path in pages:
            html = path.read_text(encoding="utf-8")
            city = path.parent.parent.name
            if is_noindex(html):
                noindexed.append(city)
                self.assertEqual(canonical(html), f"{BASE}/{city}/all-glass-entrances/")
            elif canonical(html) == hub:
                hub_canonical.append(city)
            else:
                self.fail(f"{city} is neither noindex-self nor hub-canonical")
        self.assertEqual(len(noindexed), 28)
        self.assertEqual(len(hub_canonical), 49)
        locs = sitemap_locs()
        for city in noindexed:
            self.assertNotIn(f"{BASE}/{city}/all-glass-entrances/", locs)
        hub_html = read("all-glass-entrances/index.html")
        self.assertFalse(is_noindex(hub_html))
        self.assertEqual(canonical(hub_html), hub)
        self.assertIn(hub, locs)

    def test_thin_city_roots_winter_park_and_wynwood_are_contained(self):
        locs = sitemap_locs()
        for city in ("winter-park", "wynwood"):
            html = read(f"{city}/index.html")
            self.assertTrue(is_noindex(html), city)
            self.assertEqual(canonical(html), f"{BASE}/{city}/")
            self.assertNotIn(f"{BASE}/{city}/", locs)
        # 2026-09-21: the Park Avenue neighborhood page consolidates onto the
        # Winter Park file. Both are noindex and off every sitemap.
        park = read("winter-park/winter-park-park-ave/index.html")
        self.assertEqual(robots(park), "noindex,follow")
        self.assertEqual(
            canonical(park), f"{BASE}/commercial-glazing-winter-park.html"
        )
        self.assertNotIn(f"{BASE}/winter-park/winter-park-park-ave/", locs)
        winter = read("commercial-glazing-winter-park.html")
        self.assertEqual(robots(winter), "noindex,follow")
        self.assertEqual(
            canonical(winter), f"{BASE}/commercial-glazing-winter-park.html"
        )
        self.assertNotIn(f"{BASE}/commercial-glazing-winter-park.html", locs)

    def test_2026_09_21_thin_non_office_pages_are_noindex_and_off_sitemap(self):
        # Self-canonical + noindex,follow, matching commercial-glazing-st-cloud.
        # Files stay on disk. Park Avenue is covered above (cross-canonical).
        pages = (
            "impact-windows-anna-maria-island.html",
            "impact-windows-bonita-springs.html",
            "impact-windows-bradenton.html",
            "impact-windows-cape-coral.html",
            "impact-windows-venice-fl.html",
            "commercial-glazier-boca-raton/index.html",
            "commercial-glazier-lakeland/index.html",
            "commercial-glazier-vero-beach/index.html",
            "miami/wynwood-miami/index.html",
        )
        locs = sitemap_locs()
        for rel in pages:
            html = read(rel)
            url = f"{BASE}{url_for(REPO_ROOT / rel)}"
            self.assertEqual(robots(html), "noindex,follow", rel)
            self.assertEqual(canonical(html), url, rel)
            self.assertNotIn(url, locs, rel)
            self.assertTrue((REPO_ROOT / rel).is_file(), rel)
        tampa = read("impact-windows-tampa.html")
        self.assertNotIn("noindex", robots(tampa))

    def test_2026_09_24_thin_commercial_glazier_cities_are_noindex_and_off_sitemap(self):
        # Same template as the already-noindexed Boca Raton / Lakeland / Vero
        # Beach pages (~95% of main text). Self-canonical noindex,follow.
        # Files stay. Distinct commercial-glazier pages stay indexable.
        pages = (
            "commercial-glazier-coral-springs/index.html",
            "commercial-glazier-delray-beach/index.html",
            "commercial-glazier-doral-fl/index.html",
            "commercial-glazier-hialeah/index.html",
            "commercial-glazier-hollywood-fl/index.html",
            "commercial-glazier-jupiter/index.html",
            "commercial-glazier-pembroke-pines/index.html",
            "commercial-glazier-pinecrest/index.html",
            "commercial-glazier-wellington/index.html",
        )
        keepers = (
            "commercial-glazier-bid-process-florida/index.html",
            "commercial-glazier-near-me-west-palm-beach/index.html",
            "commercial-glazier-questions-to-ask-before-hiring/index.html",
        )
        locs = sitemap_locs()
        self.assertEqual(len(pages), 9)
        for rel in pages:
            html = read(rel)
            url = f"{BASE}{url_for(REPO_ROOT / rel)}"
            self.assertEqual(robots(html), "noindex,follow", rel)
            self.assertEqual(canonical(html), url, rel)
            self.assertNotIn(url, locs, rel)
            self.assertTrue((REPO_ROOT / rel).is_file(), rel)
        for rel in keepers:
            html = read(rel)
            url = f"{BASE}{url_for(REPO_ROOT / rel)}"
            self.assertNotIn("noindex", robots(html), rel)
            self.assertIn(url, locs, rel)

    def test_2026_09_24_near_duplicate_verticals_are_noindex_and_off_sitemap(self):
        # City-swapped templates that share ~95% of their body. Self-canonical
        # noindex,follow, files kept, dropped from every sitemap. Statewide
        # hubs stay indexable. /euro-wall-folding-door-installer-naples/ stays
        # indexable because the orphan-inbound guard requires it in the sitemap.
        pages = (
            "assisted-living-glazing-naples/index.html",
            "assisted-living-glazing-orlando/index.html",
            "assisted-living-glazing-west-palm-beach/index.html",
            "automotive-showroom-glazing-fort-lauderdale/index.html",
            "automotive-showroom-glazing-orlando/index.html",
            "automotive-showroom-glazing-tampa/index.html",
            "automotive-showroom-glazing-west-palm-beach/index.html",
            "bar-brewery-glazing-miami/index.html",
            "bar-brewery-glazing-orlando/index.html",
            "bar-brewery-glazing-tampa/index.html",
            "country-club-glazing-boca-raton/index.html",
            "country-club-glazing-naples/index.html",
            "country-club-glazing-palm-beach/index.html",
            "eswindows-impact-window-installer-boca-raton/index.html",
            "eswindows-impact-window-installer-palm-beach/index.html",
            "euro-wall-folding-door-installer-miami/index.html",
            "government-municipal-glazing-miami/index.html",
            "government-municipal-glazing-tallahassee/index.html",
            "gym-fitness-glazing-miami/index.html",
            "gym-fitness-glazing-naples/index.html",
            "gym-fitness-glazing-orlando/index.html",
            "gym-fitness-glazing-tampa/index.html",
            "healthcare-glazing-jacksonville/index.html",
            "healthcare-glazing-miami/index.html",
            "healthcare-glazing-orlando/index.html",
            "healthcare-glazing-tampa/index.html",
            "marina-glazing-miami-beach/index.html",
            "marina-glazing-naples/index.html",
            "multifamily-glazing-fort-lauderdale/index.html",
            "multifamily-glazing-miami/index.html",
            "multifamily-glazing-naples/index.html",
            "multifamily-glazing-orlando/index.html",
            "multifamily-glazing-tampa/index.html",
            "multifamily-glazing-west-palm-beach/index.html",
            "religious-glazing-miami/index.html",
            "religious-glazing-orlando/index.html",
            "religious-glazing-tampa/index.html",
            "showroom-glazing-miami/index.html",
            "showroom-glazing-naples/index.html",
            "university-college-glazing-gainesville/index.html",
            "university-college-glazing-miami/index.html",
            "university-college-glazing-orlando/index.html",
            "university-college-glazing-tampa/index.html",
        )
        hubs = (
            "healthcare-glazing-florida.html",
            "healthcare-commercial-glazing-florida/index.html",
            "gym-fitness-commercial-glazing-florida/index.html",
            "multifamily-commercial-glazing-florida/index.html",
            "euro-wall-installer-florida.html",
            "eswindows-installer-florida.html",
        )
        locs = sitemap_locs()
        self.assertEqual(len(pages), 43)
        for rel in pages:
            html = read(rel)
            url = f"{BASE}{url_for(REPO_ROOT / rel)}"
            self.assertEqual(robots(html), "noindex,follow", rel)
            self.assertEqual(canonical(html), url, rel)
            self.assertNotIn(url, locs, rel)
            self.assertTrue((REPO_ROOT / rel).is_file(), rel)
        for rel in hubs:
            html = read(rel)
            url = f"{BASE}{url_for(REPO_ROOT / rel)}"
            self.assertNotIn("noindex", robots(html), rel)
            self.assertIn(url, locs, rel)
        naples = read("euro-wall-folding-door-installer-naples/index.html")
        self.assertNotIn("noindex", robots(naples))
        self.assertIn(f"{BASE}/euro-wall-folding-door-installer-naples/", locs)

    def test_2026_09_24_thin_emergency_repair_cities_are_noindex_and_off_sitemap(self):
        # Miami / Orlando / Tampa share ~95% of their main text with each
        # other. Self-canonical noindex,follow. Files stay. The statewide
        # emergency page stays indexable and in the sitemap.
        pages = (
            "emergency-commercial-glass-repair-miami/index.html",
            "emergency-commercial-glass-repair-orlando/index.html",
            "emergency-commercial-glass-repair-tampa/index.html",
        )
        locs = sitemap_locs()
        self.assertEqual(len(pages), 3)
        for rel in pages:
            html = read(rel)
            url = f"{BASE}{url_for(REPO_ROOT / rel)}"
            self.assertEqual(robots(html), "noindex,follow", rel)
            self.assertEqual(canonical(html), url, rel)
            self.assertNotIn(url, locs, rel)
            self.assertTrue((REPO_ROOT / rel).is_file(), rel)
        hub = read("emergency-commercial-glass-repair-florida/index.html")
        hub_url = f"{BASE}/emergency-commercial-glass-repair-florida/"
        self.assertNotIn("noindex", robots(hub))
        self.assertEqual(canonical(hub), hub_url)
        self.assertIn(hub_url, locs)


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
        # services and manufacturers keep the original bound. Their job is to
        # explain a small number of things, so a link wall there is the failure
        # this test was written to catch. Both are unchanged: 97 and 61.
        for rel in ("services.html", "manufacturers.html"):
            hrefs = HREF_RE.findall(read(rel))
            self.assertLess(len(hrefs), 180, rel)

    def test_locations_hub_is_a_bounded_index_not_an_unbounded_dump(self):
        # locations.html rose from 150 to 294 hrefs during the refresh, because
        # 144 city and submarket pages were sitting in the sitemap with zero
        # inbound links: advertised to Google and unreachable by a visitor.
        # Linking them was the fix and a locations index is the honest place for
        # location links, so the bound rises rather than the orphans going back.
        #
        # It is still a bound. If this page keeps growing it should be split into
        # county sub-hubs, and 340 is the line where that becomes the answer.
        hrefs = HREF_RE.findall(read("locations.html"))
        self.assertLess(len(hrefs), 340, "locations.html")


class Hard404RedirectStubTests(unittest.TestCase):
    def test_florida_commercial_glazing_html_alias_is_github_pages_redirect_stub(self):
        stub = REPO_ROOT / "florida-commercial-glazing.html"
        self.assertTrue(stub.is_file())
        html = stub.read_text(encoding="utf-8")
        dest = f"{BASE}/florida-commercial-glazing/"
        self.assertEqual(canonical(html), dest)
        self.assertIn(f'content="0; url={dest}"', html)
        self.assertEqual(robots(html), "noindex,follow")
        self.assertIn("This page has moved.", html)
        self.assertIn(f'<a href="{dest}">/florida-commercial-glazing/</a>', html)
        self.assertNotIn(f"{BASE}/florida-commercial-glazing.html", sitemap_locs())
        keeper = read("florida-commercial-glazing/index.html")
        self.assertFalse(is_noindex(keeper))
        self.assertEqual(canonical(keeper), dest)

    def test_jacksonville_storefront_glazier_dir_is_github_pages_redirect_stub(self):
        stub = REPO_ROOT / "storefront-glazier-jacksonville-florida" / "index.html"
        self.assertTrue(stub.is_file())
        html = stub.read_text(encoding="utf-8")
        dest = f"{BASE}/commercial-glazing-jacksonville.html"
        self.assertEqual(canonical(html), dest)
        self.assertIn(f'content="0; url={dest}"', html)
        self.assertEqual(robots(html), "noindex,follow")
        self.assertIn("This page has moved.", html)
        self.assertIn(f'<a href="{dest}">/commercial-glazing-jacksonville.html</a>', html)
        self.assertNotIn(
            f"{BASE}/storefront-glazier-jacksonville-florida/", sitemap_locs()
        )
        keeper = read("commercial-glazing-jacksonville.html")
        self.assertFalse(is_noindex(keeper))
        self.assertEqual(canonical(keeper), dest)


class EuroWallAliasRedirectStubTests(unittest.TestCase):
    STUBS = (
        "products/eurowall/index.html",
        "eurowall.html",
        "eurowall/index.html",
        "euro-wall/index.html",
    )
    DEST = f"{BASE}/euro-wall.html"

    def test_eurowall_alias_paths_are_github_pages_redirect_stubs(self):
        locs = sitemap_locs()
        dest = self.DEST
        for rel in self.STUBS:
            stub = REPO_ROOT / rel
            self.assertTrue(stub.is_file(), rel)
            html = stub.read_text(encoding="utf-8")
            self.assertEqual(canonical(html), dest, rel)
            self.assertIn(f'content="0; url={dest}"', html, rel)
            self.assertEqual(robots(html), "noindex,follow", rel)
            self.assertIn("This page has moved.", html, rel)
            self.assertIn(f'<a href="{dest}">/euro-wall.html</a>', html, rel)
            self.assertIn(f'window.location.replace("{dest}")', html, rel)
        self.assertNotIn(f"{BASE}/products/eurowall/", locs)
        self.assertNotIn(f"{BASE}/eurowall.html", locs)
        self.assertNotIn(f"{BASE}/eurowall/", locs)
        self.assertNotIn(f"{BASE}/euro-wall/", locs)
        keeper = read("euro-wall.html")
        self.assertFalse(is_noindex(keeper))
        self.assertEqual(canonical(keeper), dest)
        # Real product page stays put; do not stub /products/euro-wall/.
        product = read("products/euro-wall/index.html")
        self.assertFalse(is_noindex(product))
        self.assertFalse(REFRESH_RE.search(product))
        self.assertEqual(canonical(product), f"{BASE}/products/euro-wall/")


class EsWindowsLinkTests(unittest.TestCase):
    def test_es_windows_does_not_link_unverified_product_paths(self):
        html = read("es-windows.html")
        self.assertNotIn("eswindows.com/product/", html)
        self.assertNotIn("es-9000-impact-door", html)
        self.assertIn('href="https://eswindows.com"', html)
        self.assertFalse((REPO_ROOT / "products/eswindows.html").exists())

    def test_eswindows_product_path_is_github_pages_redirect_stub(self):
        stub = REPO_ROOT / "products/eswindows/index.html"
        self.assertTrue(stub.is_file())
        html = stub.read_text(encoding="utf-8")
        self.assertIn(
            'rel="canonical" href="https://acglass.com/es-windows.html"', html
        )
        self.assertIn(
            'content="0; url=https://acglass.com/es-windows.html"', html
        )
        self.assertIn('content="noindex,follow"', html)
        self.assertIn(
            'window.location.replace("https://acglass.com/es-windows.html")',
            html,
        )
        self.assertNotIn("eswindows.com/product/", html)
        self.assertNotIn("<h1", html.lower())
        for loc in sitemap_locs():
            self.assertNotIn("/products/eswindows", loc)


class EsWindowsAliasRedirectStubTests(unittest.TestCase):
    STUBS = (
        "eswindows.html",
        "eswindows/index.html",
        "products/es-windows/index.html",
        "products/eswindows/index.html",
    )
    DEST = f"{BASE}/es-windows.html"

    def test_eswindows_alias_paths_are_github_pages_redirect_stubs(self):
        locs = sitemap_locs()
        dest = self.DEST
        for rel in self.STUBS:
            stub = REPO_ROOT / rel
            self.assertTrue(stub.is_file(), rel)
            html = stub.read_text(encoding="utf-8")
            self.assertEqual(canonical(html), dest, rel)
            self.assertIn(f'content="0; url={dest}"', html, rel)
            self.assertEqual(robots(html), "noindex,follow", rel)
            self.assertIn("This page has moved.", html, rel)
            self.assertIn(f'<a href="{dest}">/es-windows.html</a>', html, rel)
            self.assertIn(f'window.location.replace("{dest}")', html, rel)
        self.assertNotIn(f"{BASE}/eswindows.html", locs)
        self.assertNotIn(f"{BASE}/eswindows/", locs)
        self.assertNotIn(f"{BASE}/products/es-windows/", locs)
        self.assertNotIn(f"{BASE}/products/eswindows/", locs)
        keeper = read("es-windows.html")
        self.assertFalse(is_noindex(keeper))
        self.assertEqual(canonical(keeper), dest)
        self.assertFalse(REFRESH_RE.search(keeper))


class MetroInstallerAliasRedirectStubTests(unittest.TestCase):
    STUBS = (
        (
            "commercial-storefront-installer-west-palm-beach.html",
            "storefront-glazier-west-palm-beach-florida/",
        ),
        (
            "commercial-storefront-installer-naples.html",
            "storefront-glazier-naples-florida/",
        ),
        (
            "commercial-storefront-installer-tampa.html",
            "storefront-glazier-tampa-florida/",
        ),
    )

    def test_metro_installer_alias_paths_are_github_pages_redirect_stubs(self):
        locs = sitemap_locs()
        for rel, slug in self.STUBS:
            dest = f"{BASE}/{slug}"
            stub = REPO_ROOT / rel
            self.assertTrue(stub.is_file(), rel)
            html = stub.read_text(encoding="utf-8")
            self.assertEqual(canonical(html), dest, rel)
            self.assertIn(f'content="0; url={dest}"', html, rel)
            self.assertEqual(robots(html), "noindex,follow", rel)
            self.assertIn("This page has moved.", html, rel)
            self.assertIn(f'<a href="{dest}">/{slug}</a>', html, rel)
            self.assertIn(f'window.location.replace("{dest}")', html, rel)
            self.assertNotIn(f"{BASE}/{rel}", locs)
            keeper = read(f"{slug.rstrip('/')}/index.html")
            self.assertFalse(is_noindex(keeper), slug)
            self.assertEqual(canonical(keeper), dest, slug)
            self.assertFalse(REFRESH_RE.search(keeper), slug)
        florida_hub = read("commercial-storefront-installer-florida.html")
        self.assertFalse(REFRESH_RE.search(florida_hub))
        self.assertIn("noindex", robots(florida_hub))
        self.assertEqual(
            canonical(florida_hub), f"{BASE}/florida-commercial-glazing/"
        )


class HomepageJsonLdTests(unittest.TestCase):
    def test_homepage_jsonld_is_florida_contractor_not_tennessee(self):
        html = read("index.html")
        self.assertIn(
            '"description": "Florida commercial glazing contractor. '
            "Storefront, curtainwall, impact, and fire-rated glazing for general contractors.\"",
            html,
        )
        self.assertNotIn("Florida & Tennessee commercial glazing contractor", html)
        # Wave-4 / semantic freeze: title, meta, og, H1 stay put.
        self.assertIn("<title>Commercial Glazing Contractor Florida | ACG</title>", html)
        self.assertIn(
            'content="Florida\'s commercial glazing contractor for storefront, curtainwall, and impact glass',
            html,
        )
        self.assertIn(
            'property="og:title" content="Commercial Glazing Contractor Florida | ACG"',
            html,
        )
        self.assertIn('<span class="l1">Commercial glazing.</span>', html)


class NashvilleResidualTests(unittest.TestCase):
    def test_nashville_office_opening_is_gone_not_a_refresh_200(self):
        html = read("acg-nashville-office-opening/index.html")
        self.assertTrue(is_noindex(html))
        self.assertFalse(REFRESH_RE.search(html))
        self.assertIn("410 Gone", html)
        self.assertNotIn("This page has been removed. Redirecting", html)
        worker = read("cloudflare-410-worker.js")
        self.assertIn('"/acg-nashville-office-opening"', worker)
        self.assertIn('"/acg-nashville-office-opening/"', worker)
        self.assertNotIn(f"{BASE}/acg-nashville-office-opening/", sitemap_locs())

    def test_tennessee_hub_title_drops_orphan_q3(self):
        html = read("tennessee-commercial-glazing/index.html")
        self.assertNotIn("consulting Q3", html)
        # Title shortened for length during the refresh. The governance point
        # this test protects is the "consulting Q3" orphan above and the supply
        # and consulting framing, not the exact old wording.
        self.assertIn(
            "<title>Tennessee Glazing Supply &amp; Consulting | ACG</title>", html
        )
        self.assertIn("Supply", html)

    def test_nashville_copy_does_not_read_as_an_office_move(self):
        html = read("nashville/index.html")
        self.assertNotIn("moving into Nashville", html)
        self.assertNotIn("when the office furnishes", html)
        self.assertNotIn("until the local team is in place", html)
        self.assertIn("holds no Tennessee office", html)
        self.assertIn("furnish-and-consult", html)
        healthcare = read("healthcare-glazing-nashville/index.html")
        self.assertNotIn("when the office furnishes", healthcare)

    def test_nashville_storefront_faq_is_furnish_specify_not_eswindows_installer(self):
        html = read("storefront-installer-nashville.html")
        self.assertNotIn("ACG is an installer of ESWindows", html)
        self.assertNotIn("installer of ESWindows", html)
        self.assertNotIn("systems installed in Nashville", html)
        self.assertNotIn("Q3 2026", html)
        self.assertNotRegex(html, r"factory[- ]certif", re.I)
        self.assertIn(
            "ACG furnishes and specifies ESWindows (Tecnoglass) storefront systems "
            "for commercial projects in Nashville",
            html,
        )
        self.assertIn(
            "ACG holds no Tennessee office and performs no Tennessee field labor",
            html,
        )
        self.assertGreaterEqual(html.count("ACG furnishes and specifies ESWindows"), 2)
        self.assertNotIn("Commercial storefront installation in Nashville", html)
        self.assertNotIn(
            "Full Division 08 commercial storefront installation in Nashville", html
        )
        self.assertNotIn("fields OSHA 30 trained crews", html)
        self.assertNotIn("OSHA 30 trained field crews", html)
        self.assertNotIn("serviceType\": \"Commercial glazing - storefront installation\"", html)
        self.assertIn("storefront systems supply and consulting", html)
        self.assertIn(
            "field installation is coordinated with in-state install partners", html
        )

    def test_nashville_storefront_copy_is_not_doubled_furnish_consult(self):
        html = read("storefront-installer-nashville.html")
        garbled = (
            "project consulting furnishing glazing materials",
            "consulting for Middle Tennessee furnishing glazing materials",
            "is a licensed commercial glazing contractor furnishing glazing materials and consulting",
        )
        for phrase in garbled:
            with self.subTest(phrase=phrase):
                self.assertNotIn(phrase, html)
        self.assertIn(
            "furnishes glazing materials and provides project consulting in Middle Tennessee",
            html,
        )
        self.assertNotIn("ACG is an installer of ESWindows", html)
        self.assertNotIn("Q3 2026", html)

    def test_no_html_calls_acg_an_eswindows_installer_for_nashville(self):
        leftover = re.compile(
            r"ACG is an installer of ESWindows.{0,160}Nashville",
            re.I | re.S,
        )
        bad = []
        for path in REPO_ROOT.rglob("*.html"):
            if SKIP_DIRS.intersection(path.relative_to(REPO_ROOT).parts):
                continue
            text = path.read_text(encoding="utf-8")
            if leftover.search(text):
                bad.append(str(path.relative_to(REPO_ROOT)))
        self.assertEqual(bad, [])

    def test_nashville_commercial_hub_is_furnish_consult_not_install_crews(self):
        html = read("commercial-glazing-nashville-tn.html")
        self.assertNotIn("AAMA InstallationMasters trained crews", html)
        self.assertNotIn("Every laminated and tempered assembly ACG installs", html)
        self.assertNotIn("manufacturer-specified installation only", html)
        self.assertIn(
            "ACG holds no Tennessee office and performs no Tennessee field labor",
            html,
        )
        self.assertIn(
            "field installation is coordinated with in-state install partners",
            html,
        )
        self.assertNotIn("ACG installs commercial glazing; AGC manufactures", html)
        self.assertIn(
            "ACG furnishes and installs commercial glazing in Florida; "
            "Tennessee is material supply and consulting",
            html,
        )


class HighIntentTrailingSlashStubTests(unittest.TestCase):
    """GitHub Pages 404s /slug/ when the keeper is slug.html.

    These noindex directory indexes match locations/index.html and forward
    query and hash to the canonical .html page. Keepers stay indexable.
    """

    STUBS = (
        "es-windows",
        "eswindows-installer-florida",
        "euro-wall-installer-florida",
        "impact-windows-doors-florida",
        "impact-windows-doors",
        "commercial-glazing-jacksonville",
        "commercial-glazing-south-florida",
        "commercial-glazing-treasure-coast",
        "healthcare-glazing-florida",
        "hospitality-glazing-florida",
        "multifamily-glazing-contractor-florida",
        "government-glazing-contractor-florida",
        "senior-living-glazing-florida",
        "restaurant-glazing-contractor",
        "retail-storefront-glazing",
        "allegion-installer-florida",
        "pgt-installer-florida",
        "tgp-fire-rated-glass-installer",
        "commercial-storefront-systems",
        "curtainwall-systems",
        "fire-rated-glass-systems",
        "automatic-entrance-systems",
        "glazing-subcontractor-florida",
        "commercial-glass-installation-florida",
        "how-to-hire-commercial-glazing-contractor-florida",
        "best-glazing-subcontractor-florida",
        "best-storefront-contractor-florida",
        "licensed-glazing-contractor-florida",
        "florida-hvhz-glazing-requirements",
        "florida-noa-explained",
        "miami-dade-noa-glazing",
        "faq",
        "eswindows-installer-west-palm-beach",
        "eswindows-installer-naples",
        "eswindows-installer-tampa",
        "eswindows-installer-miami",
        "eswindows-installer-fort-lauderdale",
        "euro-wall-installer-fort-lauderdale",
        "euro-wall-restaurant-installer-florida",
        "miami-hvhz-glazing-contractor",
        "storefront-bid-checklist-for-gcs",
        "storefront-cost-per-square-foot-florida",
        "storefront-shop-drawings-submittal",
        "glazed-aluminum-curtain-wall-contractor",
        "tgp-installer-florida",
    )
    # Slash path differs from the keeper filename or hub.
    ALIASES = (
        (
            "commercial-storefront-installer-florida",
            "/florida-commercial-glazing/",
            "florida-commercial-glazing/index.html",
        ),
        (
            "storefront-installer-florida",
            "/florida-commercial-glazing/",
            "florida-commercial-glazing/index.html",
        ),
        (
            "slimact-installer-florida",
            "/slimpact-installer-florida.html",
            "slimpact-installer-florida.html",
        ),
    )

    def test_slash_stubs_refresh_to_indexable_html_keepers(self):
        locs = sitemap_locs()
        self.assertEqual(len(self.STUBS), 45)
        for slug in self.STUBS:
            dest = f"/{slug}.html"
            stub = read(f"{slug}/index.html")
            keeper = read(f"{slug}.html")
            self.assertEqual(canonical(stub), f"{BASE}{dest}", slug)
            self.assertIn("noindex", robots(stub), slug)
            self.assertIn("follow", robots(stub), slug)
            self.assertIn(f'content="0;url={dest}"', stub, slug)
            self.assertIn(f'href="{dest}"', stub, slug)
            self.assertIn("location.search", stub, slug)
            self.assertIn(f"var next = '{dest}'", stub, slug)
            self.assertNotIn(f"{BASE}/{slug}/", locs, slug)
            self.assertNotIn(f"{BASE}{dest}/", locs, slug)
            self.assertFalse(is_noindex(keeper), slug)
            self.assertFalse(REFRESH_RE.search(keeper), slug)
            self.assertEqual(canonical(keeper), f"{BASE}{dest}", slug)
            self.assertIn(f"{BASE}{dest}", locs, slug)

    def test_alias_slash_stubs_refresh_to_keepers(self):
        locs = sitemap_locs()
        self.assertEqual(len(self.ALIASES), 3)
        self.assertFalse((REPO_ROOT / "slimact-installer-florida.html").is_file())
        for slug, dest, keeper_rel in self.ALIASES:
            stub = read(f"{slug}/index.html")
            keeper = read(keeper_rel)
            self.assertEqual(canonical(stub), f"{BASE}{dest}", slug)
            self.assertIn("noindex", robots(stub), slug)
            self.assertIn("follow", robots(stub), slug)
            self.assertIn(f'content="0;url={dest}"', stub, slug)
            self.assertIn(f'href="{dest}"', stub, slug)
            self.assertIn("location.search", stub, slug)
            self.assertIn(f"var next = '{dest}'", stub, slug)
            self.assertNotIn(f"{BASE}/{slug}/", locs, slug)
            self.assertFalse(is_noindex(keeper), slug)
            self.assertFalse(REFRESH_RE.search(keeper), slug)
            self.assertEqual(canonical(keeper), f"{BASE}{dest}", slug)
            self.assertIn(f"{BASE}{dest}", locs, slug)

    def test_indexable_pages_do_not_href_the_new_slash_stubs(self):
        leftovers = []
        targets = {f"/{slug}/" for slug in self.STUBS}
        targets.update(f"/{slug}/" for slug, _, _ in self.ALIASES)
        for dirpath, dirnames, filenames in os.walk(REPO_ROOT):
            dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
            for fn in filenames:
                if not fn.endswith(".html"):
                    continue
                path = Path(dirpath) / fn
                html = path.read_text(encoding="utf-8", errors="replace")
                if is_noindex(html) or REFRESH_RE.search(html):
                    continue
                for href in HREF_RE.findall(html):
                    dest = resolve(path, href)
                    if dest in targets:
                        leftovers.append(
                            f"{path.relative_to(REPO_ROOT).as_posix()} -> {href}"
                        )
        self.assertEqual(leftovers, [])


if __name__ == "__main__":
    unittest.main(verbosity=2)
