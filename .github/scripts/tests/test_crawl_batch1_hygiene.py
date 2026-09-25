#!/usr/bin/env python3
"""Focused crawl-batch-1 guards: sitemap advertising, retired locs, TN copy, assets."""

from __future__ import annotations

import re
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[3]
SM_NS = "{http://www.sitemaps.org/schemas/sitemap/0.9}"
APEX = "https://acglass.com/sitemap.xml"
RETIRED = (
    "https://acglass.com/blog/ocean-prime-ft-lauderdale-glazing.html",
    "https://acglass.com/case-study-ocean-prime-fort-lauderdale.html",
    "https://acglass.com/google9d45280643313cec.html",
)


def _read(rel: str) -> str:
    return (REPO_ROOT / rel).read_text(encoding="utf-8")


def _sitemap_files() -> list[Path]:
    files = sorted(REPO_ROOT.glob("sitemap*.xml"))
    fixture = REPO_ROOT / ".github" / "fixtures" / "sitemap-pages.xml"
    if fixture.is_file():
        files.append(fixture)
    return files


class ApexSitemapAdvertisingTests(unittest.TestCase):
    def test_robots_txt_lists_only_apex_sitemap(self):
        lines = re.findall(
            r"^\s*Sitemap:\s*(\S+)", _read("robots.txt"), re.IGNORECASE | re.MULTILINE
        )
        self.assertEqual([APEX], lines)
        self.assertNotIn("sitemap-index.xml", _read("robots.txt"))
        self.assertNotIn("www.acglass.com", _read("robots.txt"))

    def test_ai_txt_and_llms_txt_do_not_advertise_child_sitemaps(self):
        ai = _read("ai.txt")
        llms = _read("llms.txt")
        ai_lines = re.findall(r"^\s*Sitemap:\s*(\S+)", ai, re.IGNORECASE | re.MULTILINE)
        self.assertEqual([APEX], ai_lines)
        self.assertNotIn("sitemap-llm.xml", ai)
        self.assertNotIn("sitemap-index.xml", llms)
        self.assertIn("https://acglass.com/sitemap.xml", llms)
        self.assertNotIn("sitemap-llm.xml", llms)

    def test_sitemap_index_lists_only_the_apex_master(self):
        root = ET.fromstring(_read("sitemap-index.xml"))
        locs = [el.text.strip() for el in root.iter(f"{SM_NS}loc")]
        self.assertEqual([APEX], locs)

    def test_public_sitemap_pages_is_an_empty_retired_stub(self):
        root = ET.fromstring(_read("sitemap-pages.xml"))
        locs = [el.text.strip() for el in root.iter(f"{SM_NS}loc")]
        self.assertEqual(locs, [])
        fixture = REPO_ROOT / ".github" / "fixtures" / "sitemap-pages.xml"
        self.assertTrue(fixture.is_file())
        fixture_locs = [
            el.text.strip()
            for el in ET.fromstring(fixture.read_text(encoding="utf-8")).iter(
                f"{SM_NS}loc"
            )
        ]
        # Floor tracks the retired child urlset after thin-template sitemap
        # drops: 373 after #206-#210, 370 after the emergency-repair cities.
        self.assertGreaterEqual(len(fixture_locs), 370)


class RetiredSitemapUrlTests(unittest.TestCase):
    def test_retired_urls_absent_from_every_sitemap_file(self):
        leftovers = []
        for path in _sitemap_files():
            body = path.read_text(encoding="utf-8")
            for url in RETIRED:
                if f"<loc>{url}</loc>" in body:
                    leftovers.append(f"{url} in {path.name}")
        self.assertEqual(leftovers, [])


class HomepageTennesseeCopyTests(unittest.TestCase):
    def test_homepage_body_does_not_call_acg_a_nashville_contractor(self):
        home = _read("index.html")
        self.assertNotIn("contractor in Nashville", home)
        self.assertNotIn("Commercial glazing contractor in Nashville", home)
        self.assertNotIn("commercial glazing contractor in Tennessee", home)
        self.assertIn("Tennessee glazing supply and consulting", home)
        self.assertIn("furnish materials and consult on Tennessee glazing", home)
        self.assertIn("West Palm Beach", home)
        self.assertIn("Naples", home)
        self.assertIn("Tampa", home)
        # Title/meta stay Wave-4 / freeze owned.
        self.assertIn(
            "<title>Commercial Glazing Contractor Florida | ACG</title>", home
        )


class ArchitectResourcesLinkTests(unittest.TestCase):
    def test_no_dead_es_windows_or_euro_wall_file_downloads(self):
        html = _read("architect-resources.html")
        self.assertNotIn("eswindows.com/wp-content", html)
        self.assertNotIn("residential.eswindows.com/wp-content", html)
        self.assertNotIn("vista_ms_brochure_v1_102025-1.pdf", html)
        self.assertIn("/architect-specs/section-08-41-13-aluminum-storefront.html", html)
        self.assertIn("/architect-specs/section-08-44-13-aluminum-curtainwall.html", html)
        hrefs = re.findall(r'href="(https://[^"]+\.(?:pdf|docx))"', html)
        dead = [
            h
            for h in hrefs
            if "eswindows.com" in h or "vista_ms_brochure_v1" in h
        ]
        self.assertEqual(dead, [])


class ProjectImageSrcTests(unittest.TestCase):
    def test_projects_index_carries_no_panther_photo(self):
        # Rewritten 2026-09-09. Panther National was removed from the site on
        # Connor's instruction: the project is in active litigation and he asked
        # for no ACG association online. The original test asserted the opposite,
        # that projects/index.html DOES reference a Panther photo, so it had to
        # invert rather than be deleted. The intent it protects is unchanged:
        # this page must not reference an image that is not on disk.
        page = _read("projects/index.html")
        self.assertNotIn("images/projects/panther-national/", page)
        self.assertFalse((REPO_ROOT / "images/projects/panther-national").exists())

    def test_imperial_gallery_does_not_prefer_the_flaky_webp(self):
        page = _read("imperial-crossings-bonita-springs.html")
        self.assertNotIn(
            "aerial-townhomes-construction.webp", page
        )
        self.assertIn(
            "images/projects/imperial-crossings/aerial-townhomes-construction.jpg",
            page,
        )
        self.assertTrue(
            (
                REPO_ROOT
                / "images/projects/imperial-crossings/aerial-townhomes-construction.jpg"
            ).is_file()
        )


class StubPatternTests(unittest.TestCase):
    def test_wbe_stub_matches_contact_refresh_pattern(self):
        html = _read("wbe-sbe-procurement.html")
        self.assertIn('http-equiv="refresh"', html)
        self.assertIn('content="noindex,follow"', html)
        self.assertIn('canonical" href="https://acglass.com/qualifications.html"', html)
        self.assertIn('window.location.replace("/qualifications.html")', html)


class AiCitationHygieneTests(unittest.TestCase):
    """AI citation files name live indexable pages, and they do not name Panther."""

    CITATION_FILES = (
        "llms.txt",
        "llms-full.txt",
        "mcp/data/acg_facts.json",
        "feed.xml",
        "search-index.json",
        "data/project-locations.json",
        "data/projects-map.json",
        "js/acg-blog-cta.js",
    )
    DEAD = (
        "https://acglass.com/panther-national.html",
        "https://acglass.com/haines-city-eoc.html",
        "https://acglass.com/gulf-harbour.html",
        "https://acglass.com/tomoka-town-center.html",
        "https://acglass.com/projects/ocean-prime-ft-lauderdale.html",
        "https://acglass.com/projects/ocean-prime/",
        "https://acglass.com/projects/panther-national/",
        "https://acglass.com/projects/wild-blue/",
        "https://acglass.com/projects/haines-city-eoc/",
        "https://acglass.com/projects/gulf-harbour/",
        "https://acglass.com/projects/tomoka-town-center/",
        "https://acglass.com/projects/rome-collective/",
    )

    def test_public_citation_files_do_not_name_panther_national(self):
        for rel in self.CITATION_FILES:
            text = _read(rel).lower()
            self.assertNotIn("panther national", text, rel)
            self.assertNotIn("panther-national", text, rel)

    def test_dead_project_urls_are_gone_from_ai_files(self):
        blob = "\n".join(_read(rel) for rel in ("llms.txt", "llms-full.txt", "mcp/data/acg_facts.json"))
        for url in self.DEAD:
            self.assertNotIn(url, blob, url)

    def test_llms_citations_resolve_to_indexable_keepers(self):
        locs = set(re.findall(r"<loc>(.*?)</loc>", _read("sitemap.xml")))
        # 785 after legal.html joined the master sitemap (784 before).
        self.assertEqual(len(locs), 785)
        cited = []
        for rel in ("llms.txt", "llms-full.txt"):
            cited.extend(re.findall(r"https://acglass.com(/[^)\s]+)", _read(rel)))
        self.assertGreaterEqual(len(cited), 40)
        seen = set()
        for path in cited:
            path = path.rstrip(".,)")
            if path in seen or path.endswith((".pdf", ".txt", ".xml")):
                seen.add(path)
                continue
            seen.add(path)
            if path.endswith("/"):
                page = REPO_ROOT / path.strip("/") / "index.html"
                self.assertTrue(page.is_file(), path)
                html = page.read_text(encoding="utf-8")
                self.assertNotIn("noindex", html.lower(), path)
                self.assertIn(f"https://acglass.com{path}", locs, path)
                continue
            self.assertTrue(path.endswith(".html"), path)
            page = REPO_ROOT / path.lstrip("/")
            self.assertTrue(page.is_file(), path)
            html = page.read_text(encoding="utf-8")
            self.assertNotIn("noindex", html.lower(), path)
            self.assertIn(f'href="https://acglass.com{path}"', html, path)
            url = f"https://acglass.com{path}"
            self.assertIn(url, locs, path)
            slug = path[1:-5]
            stub_path = REPO_ROOT / slug / "index.html"
            self.assertTrue(stub_path.is_file(), slug)
            stub = stub_path.read_text(encoding="utf-8")
            self.assertIn("noindex", stub.lower(), slug)
            self.assertIn("follow", stub.lower(), slug)
            self.assertTrue(
                f"url={path}" in stub or f"url=https://acglass.com{path}" in stub,
                slug,
            )
            self.assertIn(f'href="https://acglass.com{path}"', stub, slug)
            self.assertNotIn(f"https://acglass.com/{slug}/", locs, slug)

    def test_facts_json_pages_exist_and_are_indexable(self):
        import json

        data = json.loads(_read("mcp/data/acg_facts.json"))
        pages = [row["page"] for row in data["services"]] + [
            row["page"] for row in data["published_projects"]
        ]
        self.assertNotIn("Panther National", [row["name"] for row in data["published_projects"]])
        self.assertEqual(
            next(row for row in data["published_projects"] if row["name"] == "Wild Blue Clubhouse")[
                "location"
            ],
            "Lakewood Ranch, FL",
        )
        self.assertEqual(
            next(row for row in data["published_projects"] if row["name"] == "Rome Collective")[
                "location"
            ],
            "Florida",
        )
        for url in pages:
            path = url.split("https://acglass.com", 1)[1]
            if path.endswith("/"):
                page = REPO_ROOT / path.strip("/") / "index.html"
            else:
                page = REPO_ROOT / path.lstrip("/")
            self.assertTrue(page.is_file(), url)
            html = page.read_text(encoding="utf-8")
            self.assertNotIn("noindex", html.lower(), url)

    def test_facts_ledger_cites_the_ocean_prime_keeper(self):
        html = _read("facts.html")
        self.assertIn('href="/ocean-prime-ft-lauderdale.html"', html)
        self.assertNotIn('href="/projects/ocean-prime-ft-lauderdale.html"', html)

    def test_frozen_keeper_titles_are_unchanged(self):
        self.assertIn(
            "<title>Commercial Glazing Contractor Florida | ACG</title>",
            _read("index.html"),
        )
        self.assertIn(
            "<title>Commercial Storefront Installer Florida | Bid in 48 Hrs</title>",
            _read("florida-commercial-glazing/index.html"),
        )
        for rel, needle in (
            (
                "storefront-glazier-west-palm-beach-florida/index.html",
                "Commercial Storefront Installer, West Palm Beach",
            ),
            (
                "storefront-glazier-naples-florida/index.html",
                "Commercial Storefront Installer Naples",
            ),
            (
                "storefront-glazier-tampa-florida/index.html",
                "Commercial Storefront Installer Tampa",
            ),
        ):
            title = re.search(r"<title[^>]*>(.*?)</title>", _read(rel), re.I | re.S)
            self.assertIsNotNone(title, rel)
            self.assertIn(needle, title.group(1), rel)


if __name__ == "__main__":
    unittest.main(verbosity=2)
