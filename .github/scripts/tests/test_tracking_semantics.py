#!/usr/bin/env python3
"""Regression tests for truthful form tracking semantics."""

from __future__ import annotations

import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[3]


class TrackingSemanticsTests(unittest.TestCase):
    def test_generic_submit_listener_records_attempt_only(self):
        source = (REPO_ROOT / "js" / "track.js").read_text(encoding="utf-8")
        self.assertIn("trackEvent('form_submit_attempt'", source)
        self.assertNotIn("trackEvent('form_submit'", source)

    def test_tracking_does_not_read_form_field_values(self):
        source = (REPO_ROOT / "js" / "track.js").read_text(encoding="utf-8")
        self.assertNotIn("FormData(", source)
        self.assertNotIn(".elements[", source)


if __name__ == "__main__":
    unittest.main(verbosity=2)
