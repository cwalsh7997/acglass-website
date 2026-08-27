#!/usr/bin/env python3
"""Tests for pages-watchdog.py.

Every case injects a fake API payload into `decide()`. Nothing here touches the
network: the watchdog exists because a deploy surface went quiet for 14 hours,
and a test suite that needed the live surface to be healthy would be useless in
exactly that situation.

Run:  cd .github/scripts && python3 -m unittest tests.test_pages_watchdog
"""

from __future__ import annotations

import importlib.util
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parents[1]


def _load_watchdog():
    # The script is hyphenated, so it is not importable by name.
    spec = importlib.util.spec_from_file_location(
        "pages_watchdog", SCRIPTS_DIR / "pages-watchdog.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


wd = _load_watchdog()

NOW = datetime(2026, 8, 27, 5, 30, 0, tzinfo=timezone.utc)
HEAD_SHA = "00272132267c1fa6ef2341b1c31089ad20867d2b"
OLD_SHA = "082cee66f00000000000000000000000000000aa"


def iso(moment):
    return moment.strftime("%Y-%m-%dT%H:%M:%SZ")


def http_date(moment):
    return moment.strftime("%a, %d %b %Y %H:%M:%S GMT")


def build(status="built", sha=HEAD_SHA, created=None, updated=None,
          duration=41647, error_message=None):
    created = created if created is not None else NOW - timedelta(minutes=18)
    updated = updated if updated is not None else created + timedelta(seconds=42)
    return {
        "url": "https://api.github.com/repos/cwalsh7997/acglass-website/"
               "pages/builds/1177869237",
        "status": status,
        "commit": sha,
        "duration": duration,
        "created_at": iso(created),
        "updated_at": iso(updated),
        "error": {"message": error_message},
    }


class HealthyCase(unittest.TestCase):
    """The real 2026-08-27 post-rebuild state: built, current sha, fresh edge."""

    def setUp(self):
        self.latest = build(created=datetime(2026, 8, 27, 5, 12, 50,
                                            tzinfo=timezone.utc))
        self.result = wd.decide(
            self.latest, HEAD_SHA,
            http_date(datetime(2026, 8, 27, 5, 13, 31, tzinfo=timezone.utc)),
            now=NOW)

    def test_passes(self):
        self.assertTrue(self.result.ok)
        self.assertEqual(self.result.exit_code, 0)

    def test_no_warnings(self):
        self.assertEqual(self.result.warnings, [])

    def test_diagnostics_are_printed_even_when_healthy(self):
        rendered = self.result.render()
        for needle in ("latest build status: built", "002721322",
                       "latest build duration: 41.6s", "live last-modified",
                       "main HEAD sha"):
            self.assertIn(needle, rendered)


class ErroredCase(unittest.TestCase):
    def setUp(self):
        self.result = wd.decide(
            build(status="errored", error_message="page build failed"),
            HEAD_SHA, http_date(NOW), now=NOW)

    def test_fails(self):
        self.assertFalse(self.result.ok)
        self.assertEqual(self.result.exit_code, 1)

    def test_reports_the_api_error_message(self):
        joined = " ".join(self.result.failures)
        self.assertIn("ERRORED", joined)
        self.assertIn("page build failed", joined)


class HungBuildingCase(unittest.TestCase):
    """The 2026-08-26 signature: 'building' since 15:08:11Z, 14 hours stuck."""

    def test_fails_after_14_hours(self):
        hang_start = datetime(2026, 8, 26, 15, 8, 11, tzinfo=timezone.utc)
        result = wd.decide(
            build(status="building", created=hang_start, updated=hang_start,
                  duration=None),
            HEAD_SHA, http_date(hang_start - timedelta(hours=2)),
            now=hang_start + timedelta(hours=14))
        self.assertFalse(result.ok)
        self.assertIn("HUNG", " ".join(result.failures))

    def test_fails_just_over_the_threshold(self):
        result = wd.decide(
            build(status="building", created=NOW - timedelta(minutes=15, seconds=30),
                  duration=None),
            HEAD_SHA, http_date(NOW), now=NOW)
        self.assertFalse(result.ok)

    def test_passes_for_a_merely_slow_build(self):
        # 9 minutes is far past normal but not yet the hang threshold, so a
        # slow build must not page anyone.
        result = wd.decide(
            build(status="building", created=NOW - timedelta(minutes=9),
                  duration=None),
            HEAD_SHA, http_date(NOW), now=NOW)
        self.assertTrue(result.ok)
        self.assertIn("build in progress", result.render())

    def test_unparsable_created_at_is_treated_as_a_hang(self):
        payload = build(status="building", duration=None)
        payload["created_at"] = "not a timestamp"
        result = wd.decide(payload, HEAD_SHA, http_date(NOW), now=NOW)
        self.assertFalse(result.ok)


class StaleBuiltShaCase(unittest.TestCase):
    """Pages says built, but it built an older commit than main HEAD."""

    def setUp(self):
        self.result = wd.decide(build(status="built", sha=OLD_SHA), HEAD_SHA,
                                http_date(NOW), now=NOW)

    def test_fails(self):
        self.assertFalse(self.result.ok)
        self.assertEqual(self.result.exit_code, 1)

    def test_names_both_shas(self):
        joined = " ".join(self.result.failures)
        self.assertIn(OLD_SHA[:9], joined)
        self.assertIn(HEAD_SHA[:9], joined)

    def test_unknown_head_sha_fails_rather_than_passing_quietly(self):
        result = wd.decide(build(), None, http_date(NOW), now=NOW)
        self.assertFalse(result.ok)


class LiveStalenessWarningCase(unittest.TestCase):
    def test_edge_more_than_30_min_behind_warns_without_failing(self):
        success_at = NOW - timedelta(minutes=5)
        result = wd.decide(
            build(created=success_at - timedelta(seconds=42), updated=success_at),
            HEAD_SHA, http_date(success_at - timedelta(minutes=95)), now=NOW)
        self.assertTrue(result.ok, "edge staleness must warn, not fail")
        self.assertEqual(len(result.warnings), 1)
        joined = " ".join(result.warnings)
        self.assertIn("live edge", joined)
        self.assertIn("older than the newest successful build", joined)

    def test_edge_inside_the_window_does_not_warn(self):
        success_at = NOW - timedelta(minutes=5)
        result = wd.decide(
            build(created=success_at - timedelta(seconds=42), updated=success_at),
            HEAD_SHA, http_date(success_at - timedelta(minutes=20)), now=NOW)
        self.assertEqual(result.warnings, [])

    def test_edge_ahead_of_the_build_does_not_warn(self):
        success_at = NOW - timedelta(minutes=30)
        result = wd.decide(
            build(created=success_at - timedelta(seconds=42), updated=success_at),
            HEAD_SHA, http_date(NOW), now=NOW)
        self.assertEqual(result.warnings, [])

    def test_missing_header_warns_instead_of_silently_passing(self):
        result = wd.decide(build(), HEAD_SHA, None, now=NOW)
        self.assertTrue(result.ok)
        self.assertIn("last-modified", " ".join(result.warnings))

    def test_staleness_uses_the_injected_success_when_latest_is_hung(self):
        hang_start = NOW - timedelta(hours=3)
        success = build(updated=NOW - timedelta(minutes=10))
        result = wd.decide(
            build(status="building", created=hang_start, duration=None),
            HEAD_SHA, http_date(NOW - timedelta(minutes=200)),
            latest_success=success, now=NOW)
        self.assertFalse(result.ok)
        self.assertIn("live edge", " ".join(result.warnings))


class UnknownStateCase(unittest.TestCase):
    def test_missing_payload_fails(self):
        result = wd.decide(None, HEAD_SHA, http_date(NOW), now=NOW)
        self.assertFalse(result.ok)

    def test_fetch_errors_are_surfaced_as_failures(self):
        result = wd.decide(None, None, None, now=NOW,
                           errors=["pages/builds/latest: HTTP 403"])
        self.assertFalse(result.ok)
        self.assertIn("HTTP 403", " ".join(result.failures))

    def test_unrecognised_status_fails(self):
        result = wd.decide(build(status="queued"), HEAD_SHA, http_date(NOW),
                           now=NOW)
        self.assertFalse(result.ok)


class ParsingCase(unittest.TestCase):
    def test_iso8601_z_suffix(self):
        self.assertEqual(
            wd.parse_iso8601("2026-08-27T05:12:50Z"),
            datetime(2026, 8, 27, 5, 12, 50, tzinfo=timezone.utc))

    def test_iso8601_rejects_garbage(self):
        self.assertIsNone(wd.parse_iso8601("nope"))
        self.assertIsNone(wd.parse_iso8601(None))

    def test_http_date(self):
        self.assertEqual(
            wd.parse_http_date("Thu, 27 Aug 2026 05:13:31 GMT"),
            datetime(2026, 8, 27, 5, 13, 31, tzinfo=timezone.utc))

    def test_http_date_rejects_garbage(self):
        self.assertIsNone(wd.parse_http_date("whenever"))

    def test_newest_successful_build_skips_failures(self):
        builds = [
            build(status="building", created=NOW - timedelta(minutes=1)),
            build(status="errored", created=NOW - timedelta(minutes=2)),
            build(status="built", updated=NOW - timedelta(hours=9)),
            build(status="built", updated=NOW - timedelta(minutes=40)),
        ]
        newest = wd.newest_successful_build(builds)
        self.assertEqual(newest["updated_at"], iso(NOW - timedelta(minutes=40)))

    def test_newest_successful_build_handles_empty(self):
        self.assertIsNone(wd.newest_successful_build([]))
        self.assertIsNone(wd.newest_successful_build(None))


if __name__ == "__main__":
    unittest.main()
