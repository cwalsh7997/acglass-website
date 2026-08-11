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

    def test_conflict_value_set_is_stable_and_sorted(self):
        parsed = [
            {"@id": "https://example.com/#org", "name": "Second"},
            {"@id": "https://example.com/#org", "name": "First"},
        ]
        self.assertEqual(
            [
                (
                    "https://example.com/#org",
                    "name",
                    ('"First"', '"Second"'),
                )
            ],
            validator.conflicting_id_property_values(parsed),
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

    def test_changed_held_fingerprint_is_not_accepted(self):
        path = "held.html"
        node_id = "https://example.com/#org"
        prop = "name"
        markup = """<html><head>
<script type="application/ld+json">
{"@id":"https://example.com/#org","name":"First"}
</script>
<script type="application/ld+json">
{"@id":"https://example.com/#org","name":"Changed"}
</script>
</head></html>"""
        with tempfile.TemporaryDirectory() as tempdir:
            page = Path(tempdir) / path
            page.write_text(markup, encoding="utf-8")
            report = validator.Report()
            original = validator.HELD_ID_PROPERTY_CONFLICTS
            validator.HELD_ID_PROPERTY_CONFLICTS = {
                (str(page), node_id, prop): "not-the-current-fingerprint"
            }
            try:
                validator.check_file(str(page), report)
            finally:
                validator.HELD_ID_PROPERTY_CONFLICTS = original
        self.assertIn("id_property_conflict", report.failures)
        self.assertEqual(set(), report.held_id_property_conflict_keys)

    def test_unobserved_held_exception_is_stale(self):
        original = validator.HELD_ID_PROPERTY_CONFLICTS
        key = ("held.html", "https://example.com/#org", "name")
        validator.HELD_ID_PROPERTY_CONFLICTS = {key: "fingerprint"}
        try:
            self.assertEqual([key], validator.stale_held_conflicts(set()))
            self.assertEqual([], validator.stale_held_conflicts({key}))
        finally:
            validator.HELD_ID_PROPERTY_CONFLICTS = original

    def test_new_place_geo_is_rejected(self):
        markup = """<html><head>
<script type="application/ld+json">
{"@type":"Place","name":"Example","geo":{"latitude":1,"longitude":2}}
</script>
</head></html>"""
        with tempfile.NamedTemporaryFile("w", suffix=".html", encoding="utf-8") as page:
            page.write(markup)
            page.flush()
            report = validator.Report()
            validator.check_file(page.name, report)
        self.assertIn("unsourced_place_geo", report.failures)

    def test_changed_held_place_geo_is_rejected(self):
        markup = """<html><head>
<script type="application/ld+json">
{"@type":"Place","name":"Changed","geo":{"latitude":1,"longitude":2}}
</script>
</head></html>"""
        with tempfile.NamedTemporaryFile("w", suffix=".html", encoding="utf-8") as page:
            page.write(markup)
            page.flush()
            report = validator.Report()
            original = validator.HELD_PLACE_GEO_HASHES
            validator.HELD_PLACE_GEO_HASHES = {
                page.name: ("not-the-current-fingerprint",)
            }
            try:
                validator.check_file(page.name, report)
            finally:
                validator.HELD_PLACE_GEO_HASHES = original
        self.assertIn("unsourced_place_geo", report.failures)
        self.assertEqual(set(), report.held_place_geo_paths)

    def test_exact_held_place_geo_is_accepted(self):
        markup = """<html><head>
<script type="application/ld+json">
{"@type":"Place","name":"Held","geo":{"latitude":1,"longitude":2}}
</script>
</head></html>"""
        with tempfile.NamedTemporaryFile("w", suffix=".html", encoding="utf-8") as page:
            page.write(markup)
            page.flush()
            report = validator.Report()
            parsed = [{
                "@type": "Place",
                "name": "Held",
                "geo": {"latitude": 1, "longitude": 2},
            }]
            fingerprint = validator.place_geo_fingerprints(parsed)
            original = validator.HELD_PLACE_GEO_HASHES
            validator.HELD_PLACE_GEO_HASHES = {page.name: fingerprint}
            try:
                validator.check_file(page.name, report)
            finally:
                validator.HELD_PLACE_GEO_HASHES = original
        self.assertNotIn("unsourced_place_geo", report.failures)
        self.assertEqual({page.name}, report.held_place_geo_paths)

    def test_unobserved_held_place_geo_is_stale(self):
        original = validator.HELD_PLACE_GEO_HASHES
        validator.HELD_PLACE_GEO_HASHES = {"held.html": ("fingerprint",)}
        try:
            self.assertEqual(
                ["held.html"], validator.stale_held_place_geo(set()))
            self.assertEqual(
                [], validator.stale_held_place_geo({"held.html"}))
        finally:
            validator.HELD_PLACE_GEO_HASHES = original


if __name__ == "__main__":
    unittest.main()
