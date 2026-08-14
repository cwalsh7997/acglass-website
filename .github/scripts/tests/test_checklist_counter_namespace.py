#!/usr/bin/env python3
from __future__ import annotations

import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
CHECKLIST = ROOT / "tools" / "glazing-spec-checklist" / "index.html"
MAIN_JS = ROOT / "js" / "main.js"

SECTION_KEYS = (
    "discovery",
    "wind",
    "glass",
    "frame",
    "hardware",
    "fire",
    "submittal",
    "closeout",
)


class ChecklistCounterNamespaceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.checklist = CHECKLIST.read_text(encoding="utf-8")
        cls.main_js = MAIN_JS.read_text(encoding="utf-8")

    def test_all_eight_section_keys_use_private_namespace(self) -> None:
        found = tuple(re.findall(r'data-section-count="([a-z]+)"', self.checklist))
        self.assertEqual(found, SECTION_KEYS)

    def test_checklist_selector_uses_private_namespace(self) -> None:
        selector = "'.gsc-sec-count[data-section-count=\"'+sec+'\"]'"
        self.assertIn(selector, self.checklist)
        self.assertNotIn(".gsc-sec-count[data-count", self.checklist)

    def test_shared_numeric_namespace_has_no_string_values(self) -> None:
        nonnumeric: list[tuple[Path, str]] = []
        for path in ROOT.rglob("*.html"):
            if any(part in {".git", "node_modules"} for part in path.parts):
                continue
            source = path.read_text(encoding="utf-8")
            for value in re.findall(r'data-count="([^"]+)"', source):
                if not re.fullmatch(r"[+-]?(?:\d+(?:\.\d+)?|\.\d+)", value):
                    nonnumeric.append((path.relative_to(ROOT), value))
        self.assertEqual(nonnumeric, [])

    def test_shared_counter_engine_remains_numeric_only(self) -> None:
        self.assertIn("document.querySelectorAll('[data-count]')", self.main_js)
        self.assertIn("const end = parseInt(target.dataset.count);", self.main_js)
        self.assertNotIn("data-section-count", self.main_js)

    def test_update_counts_still_writes_completed_over_total(self) -> None:
        self.assertIn("label.textContent = secDone + ' / ' + secBoxes.length;", self.checklist)
        self.assertIn("updateCounts();", self.checklist)


if __name__ == "__main__":
    unittest.main()
