#!/usr/bin/env python3
"""Focused tests for exact metadata debt fingerprints."""

from __future__ import annotations

import importlib.util
import json
import re
import unittest
from pathlib import Path


SCRIPTS_DIR = Path(__file__).resolve().parents[1]
REPO_ROOT = SCRIPTS_DIR.parents[1]


def _load_checker():
    spec = importlib.util.spec_from_file_location(
        "crawl_check", SCRIPTS_DIR / "crawl-check.py"
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


checker = _load_checker()


class HeldDescriptionTests(unittest.TestCase):
    REPAIRED_DESCRIPTIONS = {
        "acg-vs-permasteelisa.html": "Compare ACG and Permasteelisa for commercial glazing and facade work. See where each contractor fits by project type, delivery model, and scope.",
        "lantana/all-glass-entrances/index.html": "All-glass entrance installation in Lantana, Florida, including glass, hardware, operator coordination, and the bid information ACG needs.",
        "euro-wall-folding-door-installer-miami/index.html": "Euro-Wall folding door installation for Miami commercial projects, with system scope, building applications, and the information ACG needs to bid.",
        "medical-office-glazier-fort-lauderdale/index.html": "Medical office glazing in Fort Lauderdale, Florida, with project scope, coordination points, code context, and the information ACG needs to bid.",
        "medical-office-glazier-west-palm-beach/index.html": "Medical office glazing in West Palm Beach, Florida, with code context, project coordination, and the information ACG needs to prepare a bid.",
        "multifamily-glazing-orlando/index.html": "Multifamily glazing in Orlando, Florida, covering common building scopes, project coordination, and the documents ACG needs to prepare a bid.",
        "naples/all-glass-entrances/index.html": "All-glass entrance installation in Naples, Florida, including glass, hardware, operator coordination, and the bid information ACG needs.",
        "palm-harbor/glass-railings/index.html": "Glass railing installation in Palm Harbor, Florida, with code context, glass standards, engineering considerations, and bid requirements.",
        "cutler-bay/glass-railings/index.html": "Glass railing installation in Cutler Bay, Florida, with code context, glass standards, engineering considerations, and bid requirements.",
        "hobe-sound/glass-railings/index.html": "Glass railing installation in Hobe Sound, Florida, with code context, glass standards, engineering considerations, and bid requirements.",
        "islamorada/glass-railings/index.html": "Glass railing installation in Islamorada, Florida, with code context, glass standards, engineering considerations, and bid requirements.",
        "st-petersburg/downtown-st-pete/index.html": "Commercial storefront glazing in Downtown St. Petersburg, Florida, including installation scope, permit context, and the documents ACG needs to bid.",
    }
    SERVICE_DESCRIPTION_HASHES = {
        "lantana/all-glass-entrances/index.html": "ac300220c56142c36ba7270a78639e2347ea7a93fa7cf389c3b57806175d6b5a",
        "naples/all-glass-entrances/index.html": "503cf28979acebd8d922873261fa9ff5513e2f9d16972dcee602c1e6bcfc0e5d",
        "palm-harbor/glass-railings/index.html": "da985c742bccc1fe46fd531ddba120ded7b543055325c58bc91f219250920e6e",
        "cutler-bay/glass-railings/index.html": "cacdfd099a43d7c9a06d71a36b76fa67446a6e84e0b4ae85cdd2daf48274f377",
        "hobe-sound/glass-railings/index.html": "7696d6009f3991ba15b2a0bb0bf7ed4042b57d06d80394ace142c6a67404d647",
        "islamorada/glass-railings/index.html": "20d9b82f39527dc7fe06a322cec3889d4868f869eff10fac6e3752457cc4be12",
    }

    def test_current_held_descriptions_match_exact_fingerprints(self):
        for rel in checker.HELD_LONG_DESCRIPTION_HASHES:
            with self.subTest(rel=rel):
                source = (REPO_ROOT / rel).read_text(encoding="utf-8")
                description = checker.meta_content(source, "description")
                self.assertTrue(
                    checker.held_long_description_matches(rel, description)
                )

    def test_changed_held_description_does_not_match(self):
        rel = "index.html"
        source = (REPO_ROOT / rel).read_text(encoding="utf-8")
        description = checker.meta_content(source, "description")
        self.assertFalse(
            checker.held_long_description_matches(rel, description + " changed")
        )

    def test_unknown_path_never_matches(self):
        self.assertFalse(
            checker.held_long_description_matches("new-page.html", "x" * 200)
        )

    def test_held_description_set_is_only_the_byte_frozen_homepage(self):
        # Emptied down to index.html on 2026-08-20 (main commit 70308a175): the
        # three government pages now fit the 155-char limit with approval-gated
        # claims removed, so they no longer need an overlength exception.
        # index.html stays held only because it is byte-frozen in
        # .github/seo/url-primaries.json.
        self.assertEqual(
            {"index.html"},
            set(checker.HELD_LONG_DESCRIPTION_HASHES),
        )

    def test_repaired_metadata_is_bounded_and_socially_consistent(self):
        for rel, expected in self.REPAIRED_DESCRIPTIONS.items():
            with self.subTest(rel=rel):
                source = (REPO_ROOT / rel).read_text(encoding="utf-8")
                description = checker.meta_content(source, "description")
                self.assertEqual(expected, description)
                self.assertGreaterEqual(len(description), checker.DESC_MIN)
                self.assertLessEqual(len(description), checker.DESC_MAX)
                self.assertNotIn("\N{EM DASH}", description)
                self.assertNotIn("\N{EN DASH}", description)
                match = re.search(
                    r'<meta\b[^>]*property=["\']og:description["\'][^>]*content=["\']([^"\']*)["\']',
                    source,
                    re.I,
                )
                self.assertIsNotNone(match)
                self.assertEqual(description, match.group(1))

    def test_comparison_description_matches_twitter_and_webpage_schema(self):
        source = (REPO_ROOT / "acg-vs-permasteelisa.html").read_text(
            encoding="utf-8"
        )
        description = self.REPAIRED_DESCRIPTIONS["acg-vs-permasteelisa.html"]
        self.assertIn(
            f'<meta name="twitter:description" content="{description}">', source
        )
        blocks = re.findall(
            r'<script[^>]*type=["\']application/ld\+json["\'][^>]*>(.*?)</script>',
            source,
            re.I | re.S,
        )
        webpage_descriptions = []
        for block in blocks:
            data = json.loads(block)
            if isinstance(data, dict) and data.get("@type") == "WebPage":
                webpage_descriptions.append(data.get("description"))
        self.assertEqual([description], webpage_descriptions)

    def test_independent_service_descriptions_remain_exact(self):
        import hashlib

        for rel, expected_hash in self.SERVICE_DESCRIPTION_HASHES.items():
            with self.subTest(rel=rel):
                source = (REPO_ROOT / rel).read_text(encoding="utf-8")
                blocks = re.findall(
                    r'<script[^>]*type=["\']application/ld\+json["\'][^>]*>(.*?)</script>',
                    source,
                    re.I | re.S,
                )
                descriptions = []
                for block in blocks:
                    data = json.loads(block)
                    stack = [data]
                    while stack:
                        item = stack.pop()
                        if isinstance(item, dict):
                            if item.get("@type") == "Service" and isinstance(
                                item.get("description"), str
                            ):
                                descriptions.append(item["description"])
                            stack.extend(item.values())
                        elif isinstance(item, list):
                            stack.extend(item)
                self.assertEqual(1, len(descriptions))
                actual_hash = hashlib.sha256(descriptions[0].encode()).hexdigest()
                self.assertEqual(expected_hash, actual_hash)


if __name__ == "__main__":
    unittest.main(verbosity=2)
