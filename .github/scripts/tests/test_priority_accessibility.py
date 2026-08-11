#!/usr/bin/env python3
"""Accessibility structure checks for priority buyer pages."""

from __future__ import annotations

import re
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[3]
PAGES = (
    "capabilities.html",
    "gc.html",
    "for-general-contractors.html",
)


class PriorityAccessibilityTests(unittest.TestCase):
    def test_pages_have_one_skip_target_and_one_main_landmark(self):
        for rel in PAGES:
            with self.subTest(rel=rel):
                source = (REPO_ROOT / rel).read_text(encoding="utf-8")
                self.assertEqual(
                    1,
                    source.count('<main id="main-content" tabindex="-1">'),
                )
                self.assertEqual(1, source.count("</main>"))
                self.assertEqual(
                    1,
                    source.count(
                        '<a class="skip-link" href="#main-content">'
                    ),
                )
                self.assertLess(source.index("<main"), source.index("<h1"))
                self.assertLess(source.index("</header>"), source.index("<main"))
                self.assertLess(source.index("</main>"), source.index("<footer"))

    def test_main_content_heading_levels_do_not_skip(self):
        for rel in PAGES:
            with self.subTest(rel=rel):
                source = (REPO_ROOT / rel).read_text(encoding="utf-8")
                main = source.split("<main", 1)[1].split("</main>", 1)[0]
                levels = [
                    int(level)
                    for level in re.findall(r"<h([1-6])\b", main, re.I)
                ]
                self.assertTrue(levels)
                self.assertEqual(1, levels[0])
                for previous, current in zip(levels, levels[1:]):
                    self.assertLessEqual(current, previous + 1)


if __name__ == "__main__":
    unittest.main(verbosity=2)
