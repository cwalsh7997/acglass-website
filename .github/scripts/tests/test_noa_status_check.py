#!/usr/bin/env python3
"""Focused tests for the offline NOA source-ledger gate."""

from __future__ import annotations

import importlib.util
import sys
import unittest
from datetime import date
from pathlib import Path


SCRIPTS_DIR = Path(__file__).resolve().parents[1]


def _load_checker():
    spec = importlib.util.spec_from_file_location(
        "noa_status_check", SCRIPTS_DIR / "noa-status-check.py"
    )
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


checker = _load_checker()


def ledger(row):
    return {
        "partners": {
            "sample": {
                "label": "Sample",
                "systems": [row],
            }
        }
    }


class NoaStatusTests(unittest.TestCase):
    def test_current_https_source_passes(self):
        total, findings = checker.audit(
            ledger(
                {
                    "fl_pa": "sample-id",
                    "status": "Approved",
                    "source_url": "https://example.gov/source",
                    "last_verified": "2026-08-01",
                }
            ),
            date(2026, 8, 11),
            35,
        )
        self.assertEqual(1, total)
        self.assertEqual([], findings)

    def test_stale_source_fails(self):
        _, findings = checker.audit(
            ledger(
                {
                    "fl_pa": "sample-id",
                    "status": "Approved",
                    "source_url": "https://example.gov/source",
                    "last_verified": "2026-06-01",
                }
            ),
            date(2026, 8, 11),
            35,
        )
        self.assertIn("source review is 71 days old", findings[0].reason)

    def test_missing_fields_and_non_https_source_fail(self):
        _, findings = checker.audit(
            ledger(
                {
                    "fl_pa": "sample-id",
                    "status": "Approved",
                    "source_url": "http://example.gov/source",
                    "last_verified": "2026-08-01",
                }
            ),
            date(2026, 8, 11),
            35,
        )
        self.assertEqual("source URL is not HTTPS", findings[0].reason)

    def test_missing_partner_map_fails_closed(self):
        total, findings = checker.audit({}, date(2026, 8, 11), 35)
        self.assertEqual(0, total)
        self.assertEqual("missing partner map", findings[0].reason)


if __name__ == "__main__":
    unittest.main(verbosity=2)
