#!/usr/bin/env python3
"""Focused tests for exact metadata debt fingerprints."""

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


class HeldDescriptionTests(unittest.TestCase):
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


if __name__ == "__main__":
    unittest.main(verbosity=2)
