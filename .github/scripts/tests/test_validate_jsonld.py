#!/usr/bin/env python3
"""Focused tests for duplicate @id property collision detection."""

from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parents[1]


def _load_validator():
    spec = importlib.util.spec_from_file_location(
        "validate_jsonld", SCRIPTS_DIR / "validate-jsonld.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


validator = _load_validator()


class DuplicateIdPropertyTests(unittest.TestCase):
    def test_check_file_reports_property_collision(self):
        markup = """<html><head>
<script type="application/ld+json">
{"@id":"https://example.com/#org","name":"First"}
</script>
<script type="application/ld+json">
{"@id":"https://example.com/#org","name":"Second"}
</script>
</head></html>"""
        with tempfile.NamedTemporaryFile("w", suffix=".html", encoding="utf-8") as page:
            page.write(markup)
            page.flush()
            report = validator.Report()
            validator.check_file(page.name, report)
        self.assertEqual(
            [f"{page.name}: https://example.com/#org [name]"],
            report.failures["id_property_conflict"],
        )

    def test_different_values_for_same_property_are_a_collision(self):
        parsed = [
            {"@id": "https://example.com/#org", "name": "First"},
            {"@id": "https://example.com/#org", "name": "Second"},
        ]
        self.assertEqual(
            [("https://example.com/#org", "name")],
            validator.conflicting_id_properties(parsed),
        )

    def test_identical_repeated_values_are_not_a_collision(self):
        parsed = [
            {"@id": "https://example.com/#org", "name": "Same"},
            {"@id": "https://example.com/#org", "name": "Same"},
        ]
        self.assertEqual([], validator.conflicting_id_properties(parsed))

    def test_reference_and_definition_are_not_a_collision(self):
        parsed = [
            {"@id": "https://example.com/#org"},
            {"@id": "https://example.com/#org", "name": "Same"},
        ]
        self.assertEqual([], validator.conflicting_id_properties(parsed))

    def test_complementary_properties_are_not_a_collision(self):
        parsed = [
            {"@id": "https://example.com/#org", "name": "Same"},
            {"@id": "https://example.com/#org", "telephone": "+17724867711"},
        ]
        self.assertEqual([], validator.conflicting_id_properties(parsed))

    def test_same_property_on_different_ids_is_not_a_collision(self):
        parsed = [
            {"@id": "https://example.com/#first", "name": "First"},
            {"@id": "https://example.com/#second", "name": "Second"},
        ]
        self.assertEqual([], validator.conflicting_id_properties(parsed))


if __name__ == "__main__":
    unittest.main()
