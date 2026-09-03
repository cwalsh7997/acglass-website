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
    "https://acglass.com/ocean-prime-ft-lauderdale.html",
    "https://acglass.com/blog/ocean-prime-ft-lauderdale-glazing.html",
    "https://acglass.com/case-study-ocean-prime-fort-lauderdale.html",
    "https://acglass.com/google9d45280643313cec.html",
)


def _read(rel: str) -> str:
    return (REPO_ROOT / rel).read_text(encoding="utf-8")


def _sitemap_files() -> list[Path]:
    return sorted(REPO_ROOT.glob("sitemap*.xml"))


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


class RetiredSitemapUrlTests(unittest.TestCase):
    def test_retired_urls_absent_from_every_sitemap_file(self):
        leftovers = []
        for path in _sitemap_files():
            body = path.read_text(encoding="utf-8")
            for url in RETIRED:
                if url in body:
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
    def test_projects_index_uses_existing_panther_photo(self):
        page = _read("projects/index.html")
        self.assertNotIn("panther-national-hero.jpg", page)
        self.assertIn(
            "images/projects/panther-national/brochure-clubhouse-hero.jpg", page
        )
        self.assertTrue(
            (REPO_ROOT / "images/projects/panther-national/brochure-clubhouse-hero.jpg").is_file()
        )

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


if __name__ == "__main__":
    unittest.main(verbosity=2)
