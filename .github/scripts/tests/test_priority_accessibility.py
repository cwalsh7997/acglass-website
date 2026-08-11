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

    def test_smooth_scroll_excludes_skip_links(self):
        source = (REPO_ROOT / "js/main.js").read_text(encoding="utf-8")
        self.assertIn(
            'document.querySelectorAll(\'.skip-link[href^="#"]\')',
            source,
        )
        self.assertIn(
            "window.setTimeout(() => target.focus({ preventScroll: true }), 0);",
            source,
        )
        self.assertIn(
            'document.querySelectorAll(\'a[href^="#"]:not(.skip-link)\')',
            source,
        )
        self.assertNotIn(
            'document.querySelectorAll(\'a[href^="#"]\')',
            source,
        )

    def test_general_contractor_skip_link_is_visible_above_fixed_header(self):
        source = (REPO_ROOT / "for-general-contractors.html").read_text(
            encoding="utf-8"
        )
        self.assertRegex(
            source,
            r"\.skip-link\{[^}]*position:fixed;[^}]*top:-100px;"
            r"[^}]*z-index:10000;",
        )
        self.assertIn(".skip-link:focus{top:0;", source)

    def test_service_worker_cache_version_releases_updated_shared_script(self):
        source = (REPO_ROOT / "sw.js").read_text(encoding="utf-8")
        self.assertIn("const CACHE = 'acg-v5-2026-08-11';", source)
        self.assertNotIn("const CACHE = 'acg-v1-2026-06-06';", source)

    def test_priority_pages_request_current_shared_script(self):
        for rel in ("capabilities.html", "gc.html"):
            with self.subTest(rel=rel):
                source = (REPO_ROOT / rel).read_text(encoding="utf-8")
                self.assertEqual(
                    1,
                    source.count('src="js/main.js?v=20260811d"'),
                )


if __name__ == "__main__":
    unittest.main(verbosity=2)
