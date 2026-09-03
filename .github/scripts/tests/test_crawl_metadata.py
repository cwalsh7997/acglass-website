#!/usr/bin/env python3
"""Focused tests for crawl-check metadata extraction and limits."""

from __future__ import annotations

import importlib.util
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


class TitleMetadataTests(unittest.TestCase):
    def test_title_extraction_normalizes_whitespace(self):
        markup = "<title data-source='test'>  Commercial\n Glazing | ACG </title>"
        self.assertEqual(
            "Commercial Glazing | ACG",
            checker.title_content(markup),
        )

    def test_title_extraction_decodes_entities(self):
        self.assertEqual(
            "TAA, BABA & Buy American Act Glazing | ACG",
            checker.title_content(
                "<title>TAA, BABA &amp; Buy American Act Glazing | ACG</title>"
            ),
        )

    def test_missing_title_returns_empty_string(self):
        self.assertEqual("", checker.title_content("<html></html>"))

    def test_known_malformed_title_is_removed(self):
        page = REPO_ROOT / (
            "can-acg-bid-multifamily-projects-over-2-million/index.html"
        )
        title = checker.title_content(page.read_text(encoding="utf-8"))
        self.assertGreaterEqual(len(title), checker.TITLE_MIN)
        self.assertLessEqual(len(title), checker.TITLE_MAX)

    def test_west_palm_beach_title_fits_limit(self):
        rel = "west-palm-beach/index.html"
        source = (REPO_ROOT / rel).read_text(encoding="utf-8")
        title = checker.title_content(source)
        self.assertGreaterEqual(len(title), checker.TITLE_MIN)
        self.assertLessEqual(len(title), checker.TITLE_MAX)
        self.assertEqual({}, checker.HELD_LONG_TITLE_HASHES)


if __name__ == "__main__":
    unittest.main(verbosity=2)
