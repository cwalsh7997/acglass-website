"""Indexable storefront breadcrumbs must cite live keepers, not noindex stubs."""

from __future__ import annotations

import json
import re
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[3]
HUB = "https://acglass.com/florida-commercial-glazing/"
STUB = "https://acglass.com/commercial-storefront-installer-florida.html"
WPB = "https://acglass.com/storefront-glazier-west-palm-beach-florida/"
WPB_STUB = "https://acglass.com/west-palm-beach-commercial-glazing.html"
PARENT_NAME = "Commercial Storefront Installer Florida"
STOREFRONT_PAGES = (
    "storefront-bid-checklist-for-gcs.html",
    "storefront-cost-per-square-foot-florida.html",
    "storefront-fbc-1609-compliance.html",
    "storefront-glossary.html",
    "storefront-hardware-commercial.html",
    "storefront-installation-mistakes.html",
    "storefront-installation-timeline.html",
    "storefront-maintenance-commercial.html",
    "storefront-replacement-commercial-florida.html",
    "storefront-rough-opening-tolerances.html",
    "storefront-shop-drawings-submittal.html",
    "storefront-water-intrusion-repair.html",
)
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
JSONLD = re.compile(
    r'<script\b[^>]*type=["\']application/ld\+json["\'][^>]*>(.*?)</script>',
    re.I | re.S,
)
TITLE = re.compile(r"<title[^>]*>(.*?)</title>", re.I | re.S)


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


class StorefrontBreadcrumbKeeperTests(unittest.TestCase):
    def test_sitemap_storefront_pages_cite_the_florida_hub(self):
        for rel in STOREFRONT_PAGES:
            html = (REPO_ROOT / rel).read_text(encoding="utf-8")
            trails = _crumbs(html)
            self.assertEqual(len(trails), 1, rel)
            self.assertEqual(
                trails[0],
                [
                    ("Home", "https://acglass.com/"),
                    (PARENT_NAME, HUB),
                    (trails[0][2][0], f"https://acglass.com/{rel}"),
                ],
                rel,
            )
            self.assertNotIn(STUB, html)

    def test_west_palm_beach_keeper_matches_the_other_office_crumbs(self):
        html = (
            REPO_ROOT / "storefront-glazier-west-palm-beach-florida/index.html"
        ).read_text(encoding="utf-8")
        self.assertEqual(
            _crumbs(html),
            [[("Home", "https://acglass.com/"), ("West Palm Beach", WPB)]],
        )
        self.assertNotIn(WPB_STUB, html)
        for rel in (
            "storefront-glazier-naples-florida/index.html",
            "storefront-glazier-tampa-florida/index.html",
        ):
            sibling = (REPO_ROOT / rel).read_text(encoding="utf-8")
            trails = _crumbs(sibling)
            self.assertEqual(len(trails), 1, rel)
            self.assertEqual(len(trails[0]), 2, rel)
            self.assertEqual(trails[0][0], ("Home", "https://acglass.com/"), rel)

    def test_stubs_stay_on_disk_and_keep_their_roles(self):
        stub = (REPO_ROOT / "commercial-storefront-installer-florida.html").read_text(
            encoding="utf-8"
        )
        self.assertIn('name="robots" content="noindex,follow"', stub)
        self.assertIn(f'rel="canonical" href="{HUB}"', stub)
        refresh = (REPO_ROOT / "west-palm-beach-commercial-glazing.html").read_text(
            encoding="utf-8"
        )
        self.assertIn('name="robots" content="noindex,follow"', refresh)
        self.assertIn(f'rel="canonical" href="{WPB}"', refresh)
        self.assertIn("http-equiv=\"refresh\"", refresh)

    def test_frozen_titles_are_unchanged(self):
        for rel, expected in FROZEN_TITLES.items():
            html = (REPO_ROOT / rel).read_text(encoding="utf-8")
            match = TITLE.search(html)
            self.assertIsNotNone(match, rel)
            title = re.sub(r"\s+", " ", match.group(1)).strip()
            self.assertEqual(title, expected, rel)


if __name__ == "__main__":
    unittest.main()
