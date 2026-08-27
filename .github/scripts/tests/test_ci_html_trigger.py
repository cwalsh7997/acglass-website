#!/usr/bin/env python3
"""The measurement-layer workflow must run when page markup changes.

Several suites in this workflow pin sha256 digests of page HTML fragments.
A path filter that omits HTML makes those digests unenforceable: the exact
change they exist to catch is the one that skips them.

This is a regression test for a real incident. The "Sprint 011" mass edit of
2026-07-31 preceded a ranking collapse on 2026-08-01. Its two most
consequential commits -- 850f44d11 (homepage title/H1/meta/og rewrite) and
15d053320 (head cleanup, breadcrumbs, schema) -- touched only HTML, so neither
triggered this workflow and neither was checked against the pinned digests.

Stdlib only, matching the workflow's own constraint: it declares no pip step
and no network, so PyYAML cannot be assumed. The block this needs to read is a
flat list of quoted strings, which does not require a YAML parser.
"""

from __future__ import annotations

import re
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
WORKFLOW = REPO_ROOT / ".github" / "workflows" / "seo-report.yml"

# Suites in this workflow that assert on page markup. If one of these exists,
# HTML must be a trigger or the suite is decorative.
MARKUP_PINNING_SUITES = (
    "test_priority_accessibility.py",
    "test_no_external_google_fonts.py",
)

EVENTS = ("pull_request", "push")


def _strip_comment(line: str) -> str:
    return line.split("#", 1)[0].rstrip() if "#" in line else line.rstrip()


def _paths_for(event: str, text: str) -> list[str] | None:
    """Return the `paths:` list under `on.<event>`, or None if unfiltered.

    Raises AssertionError if the event is absent, so a deleted trigger fails
    loudly rather than reading as "no filter, everything runs".
    """
    lines = text.splitlines()
    start = None
    for i, raw in enumerate(lines):
        if re.match(rf"^  {re.escape(event)}:\s*$", _strip_comment(raw)):
            start = i
            break
    assert start is not None, f"`on.{event}` trigger is missing from {WORKFLOW.name}"

    paths: list[str] | None = None
    for raw in lines[start + 1:]:
        line = _strip_comment(raw)
        if not line:
            continue
        indent = len(line) - len(line.lstrip())
        if indent <= 2:
            break  # next event, or the end of the `on:` mapping
        if re.match(r"^\s{4}paths:\s*$", line):
            paths = []
            continue
        if paths is not None:
            m = re.match(r"^\s{6}-\s*['\"]?([^'\"]+)['\"]?\s*$", line)
            if m:
                paths.append(m.group(1))
            elif indent <= 4:
                break
    return paths


class HtmlTriggerTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        assert WORKFLOW.is_file(), f"missing {WORKFLOW}"
        cls.text = WORKFLOW.read_text(encoding="utf-8")

    def test_parser_finds_a_nonempty_filter(self):
        # Guards the test itself: a parser that silently returns [] would make
        # every assertion below vacuous.
        for event in EVENTS:
            with self.subTest(event=event):
                paths = _paths_for(event, self.text)
                if paths is not None:
                    self.assertTrue(paths, f"parsed an empty paths list for {event}")

    def test_pull_request_and_push_both_trigger_on_html(self):
        for event in EVENTS:
            with self.subTest(event=event):
                paths = _paths_for(event, self.text)
                if paths is None:
                    continue  # no filter at all means everything triggers
                self.assertTrue(
                    any(p.endswith("*.html") for p in paths),
                    f"{event} path filter does not include HTML: {paths}. "
                    "The suites in this workflow pin HTML digests, so an "
                    "HTML-only change would skip them -- the Sprint 011 hole.",
                )

    def test_css_is_a_trigger_not_just_one_stylesheet(self):
        # The filter used to name css/acg-proof.css alone, so a change to any
        # other stylesheet skipped the contrast and nav-opacity suites.
        for event in EVENTS:
            with self.subTest(event=event):
                paths = _paths_for(event, self.text)
                if paths is None:
                    continue
                self.assertTrue(
                    any(p == "css/**" or p.endswith("*.css") for p in paths),
                    f"{event} filter still pins a single stylesheet: {paths}",
                )

    def test_markup_pinning_suites_are_present(self):
        # If these are ever removed or renamed, this test's premise changes and
        # it should be revisited rather than silently passing.
        tests_dir = Path(__file__).resolve().parent
        for name in MARKUP_PINNING_SUITES:
            with self.subTest(suite=name):
                self.assertTrue((tests_dir / name).is_file(),
                                f"{name} moved or was removed; revisit this guard")


if __name__ == "__main__":
    unittest.main(verbosity=2)
