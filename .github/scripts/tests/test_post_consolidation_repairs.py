#!/usr/bin/env python3
"""Locks the 2026-09-28 post-consolidation SEO repairs.

1. /curtain-wall-contractor-florida/ (hyphenated spelling, never published)
   resolves on GitHub Pages to the indexed curtainwall keeper.
2. /eswindows.html stays a stub onto /es-windows.html, the ESWindows showcase
   the original project-page badge was written for.
3. The WPB edge redirect request aligns the 301 target with the source file's
   rel=canonical, and stays unactivated until applied in Cloudflare.
4. Storefront-installation informational pages link to the transactional
   primary and not to the noindex Florida installer alias.
"""

from __future__ import annotations

import json
import re
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[3]
BASE = "https://acglass.com"
CANONICAL_RE = re.compile(r'<link rel="canonical" href="([^"]+)"')
ROBOTS_RE = re.compile(r'<meta name="robots" content="([^"]+)"')


def read(rel: str) -> str:
    return (REPO_ROOT / rel).read_text(encoding="utf-8")


def canonical(html: str) -> str | None:
    m = CANONICAL_RE.search(html)
    return m.group(1) if m else None


def robots(html: str) -> str:
    m = ROBOTS_RE.search(html)
    return m.group(1).replace(" ", "") if m else ""


def sitemap_text() -> str:
    return "".join(
        p.read_text(encoding="utf-8") for p in sorted(REPO_ROOT.glob("sitemap*.xml"))
    )


class CurtainWallAliasTests(unittest.TestCase):
    STUB = "curtain-wall-contractor-florida/index.html"
    KEEPER = "curtainwall-contractor-florida.html"
    DEST = f"{BASE}/curtainwall-contractor-florida.html"

    def test_hyphenated_path_is_a_noindex_stub_onto_the_keeper(self):
        html = read(self.STUB)
        self.assertEqual(canonical(html), self.DEST)
        self.assertEqual(robots(html), "noindex,follow")
        self.assertIn(f'content="0; url={self.DEST}"', html)
        self.assertIn(f'window.location.replace("{self.DEST}")', html)
        self.assertNotIn(f"{BASE}/curtain-wall-contractor-florida/", sitemap_text())

    def test_keeper_stays_indexable_self_canonical_and_listed(self):
        keeper = read(self.KEEPER)
        self.assertEqual(canonical(keeper), self.DEST)
        self.assertNotIn("noindex", robots(keeper))
        self.assertNotIn('http-equiv="refresh"', keeper)
        self.assertIn(f"<loc>{self.DEST}</loc>", read("sitemap.xml"))


class EsWindowsKeeperTests(unittest.TestCase):
    def test_eswindows_html_points_at_the_showcase_keeper(self):
        dest = f"{BASE}/es-windows.html"
        self.assertEqual(canonical(read("eswindows.html")), dest)
        self.assertEqual(robots(read("eswindows.html")), "noindex,follow")
        keeper = read("es-windows.html")
        self.assertEqual(canonical(keeper), dest)
        self.assertNotIn("noindex", robots(keeper))

    def test_project_page_has_no_link_to_the_bare_alias(self):
        self.assertNotRegex(read("eau-palm-beach-resort.html"), r'href="[^"]*eswindows\.html"')


class WestPalmBeachEdgeRequestTests(unittest.TestCase):
    SOURCE = "/commercial-glazing-west-palm-beach.html"
    KEEPER = "/storefront-glazier-west-palm-beach-florida/"

    def test_manifest_target_matches_the_source_files_canonical(self):
        man = json.loads(read(".github/cloudflare/redirects.manifest.json"))
        self.assertIs(man["activated"], False)
        rules = {r["source"]: r for r in man["rules"]}
        rule = rules[self.SOURCE]
        self.assertEqual(rule["required_destination"], self.KEEPER)
        self.assertEqual(canonical(read("commercial-glazing-west-palm-beach.html")), BASE + self.KEEPER)
        self.assertNotIn(
            self.SOURCE, {x["source"] for x in man["deliberately_not_requested"]}
        )

    def test_mirror_still_records_the_live_edge_until_applied(self):
        mirror = json.loads(read("vercel.json"))["redirects"]
        live = {r["source"]: r["destination"] for r in mirror}
        self.assertEqual(live[self.SOURCE], "/west-palm-beach/")

    def test_wpb_commercial_glazing_intent_stays_frozen_without_primary(self):
        reg = json.loads(read(".github/seo/url-primaries.json"))
        wpb = [
            i for i in reg["intents"]
            if i["market"] == "west-palm-beach" and i["intent"] == "commercial-glazing"
        ]
        self.assertEqual(len(wpb), 1)
        self.assertEqual(wpb[0]["status"], "frozen")
        self.assertIsNone(wpb[0]["primary"])

    def test_destination_stays_indexable_and_self_canonical(self):
        keeper = read("storefront-glazier-west-palm-beach-florida/index.html")
        self.assertEqual(canonical(keeper), BASE + self.KEEPER)
        self.assertNotIn("noindex", robots(keeper))


class StorefrontInstallationLinkTests(unittest.TestCase):
    PRIMARY_LINK = 'href="/commercial-storefront-systems.html">commercial storefront systems and installation</a>'

    def test_registry_primary_is_unchanged(self):
        reg = json.loads(read(".github/seo/url-primaries.json"))
        sf = [i for i in reg["intents"] if i["intent"] == "storefront-systems"][0]
        self.assertEqual(sf["primary"], "/commercial-storefront-systems.html")
        for page in sf["informational_keep"]:
            rel = page["url"].lstrip("/")
            html = read(rel)
            self.assertEqual(canonical(html), BASE + page["url"], rel)
            self.assertNotIn("noindex", robots(html), rel)

    def test_guide_and_timeline_link_up_to_the_primary(self):
        for rel in (
            "blog/commercial-storefront-installation-guide.html",
            "storefront-installation-timeline.html",
        ):
            self.assertIn(self.PRIMARY_LINK, read(rel), rel)

    def test_guide_no_longer_links_the_noindex_alias(self):
        guide = read("blog/commercial-storefront-installation-guide.html")
        self.assertNotIn('href="/commercial-storefront-installer-florida.html"', guide)


if __name__ == "__main__":
    unittest.main()
