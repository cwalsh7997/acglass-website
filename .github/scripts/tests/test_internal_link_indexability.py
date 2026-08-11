#!/usr/bin/env python3
"""Focused tests for indexability-aware internal link checks."""

from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parents[1]


def _load_audit():
    spec = importlib.util.spec_from_file_location(
        "internal_link_audit", SCRIPTS_DIR / "internal-link-audit.py"
    )
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


audit = _load_audit()


class MetaParsingTests(unittest.TestCase):
    def test_detects_directives_regardless_of_order_case_or_quoting(self):
        doc = """
        <META CONTENT='NONE, follow' NAME='GoogleBot'>
        <meta content=0;url=/new.html HTTP-EQUIV=Refresh>
        """
        self.assertEqual((True, True), audit.page_indexing_flags(doc))

    def test_index_and_ordinary_metadata_remain_indexable(self):
        doc = """
        <meta name="robots" content="index, follow">
        <meta name="description" content="Refresh glass system documentation">
        """
        self.assertEqual((False, False), audit.page_indexing_flags(doc))


class IndexableLinkTargetTests(unittest.TestCase):
    def setUp(self):
        self.tempdir = tempfile.TemporaryDirectory()
        self.root = Path(self.tempdir.name)

    def tearDown(self):
        self.tempdir.cleanup()

    def page(self, url: str, head: str = "") -> Path:
        path = self.root / (url.strip("/") or "index.html")
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(f"<html><head>{head}</head><body></body></html>", encoding="utf-8")
        return path

    def run_gate(self, pages, inbound, redirects=None, frozen=None):
        results = []
        audit.check_indexable_link_targets(
            results,
            inbound,
            pages,
            redirects or {},
            frozen or set(),
        )
        return {result.name: result for result in results}

    def test_blocks_noindex_refresh_and_known_redirect_targets(self):
        pages = {
            "/source.html": self.page("/source.html"),
            "/hidden.html": self.page(
                "/hidden.html", '<meta name="robots" content="noindex, follow">'
            ),
            "/refresh.html": self.page(
                "/refresh.html", '<meta http-equiv="refresh" content="0; url=/new.html">'
            ),
        }
        inbound = {
            "/hidden.html": {"/source.html": ["Hidden"]},
            "/refresh.html": {"/source.html": ["Old route"]},
            "/old.html": {"/source.html": ["Redirect source"]},
        }
        results = self.run_gate(
            pages, inbound, redirects={"/old.html": "/new.html"}
        )

        self.assertFalse(results["Indexable pages do not link to noindex pages"].ok)
        self.assertFalse(results["Indexable pages do not link to meta-refresh stubs"].ok)
        self.assertFalse(results["Indexable pages do not link to known redirect sources"].ok)
        self.assertIn("/source.html", results["Indexable pages do not link to noindex pages"].detail)

    def test_noindex_and_refresh_sources_are_not_treated_as_indexable(self):
        pages = {
            "/hidden-source.html": self.page(
                "/hidden-source.html", '<meta name="robots" content="noindex">'
            ),
            "/refresh-source.html": self.page(
                "/refresh-source.html", '<meta http-equiv="refresh" content="0; url=/new.html">'
            ),
            "/hidden-target.html": self.page(
                "/hidden-target.html", '<meta name="robots" content="noindex">'
            ),
        }
        inbound = {
            "/hidden-target.html": {
                "/hidden-source.html": ["Hidden"],
                "/refresh-source.html": ["Hidden"],
            },
            "/old.html": {
                "/hidden-source.html": ["Old"],
                "/refresh-source.html": ["Old"],
            },
        }
        results = self.run_gate(
            pages, inbound, redirects={"/old.html": "/new.html"}
        )

        self.assertTrue(all(result.ok for result in results.values()))

    def test_frozen_indexable_source_remains_excluded(self):
        pages = {
            "/frozen.html": self.page("/frozen.html"),
            "/hidden.html": self.page(
                "/hidden.html", '<meta name="robots" content="noindex">'
            ),
        }
        inbound = {"/hidden.html": {"/frozen.html": ["Hidden"]}}
        results = self.run_gate(pages, inbound, frozen={"/frozen.html"})

        self.assertTrue(all(result.ok for result in results.values()))

    def test_indexable_target_passes(self):
        pages = {
            "/source.html": self.page("/source.html"),
            "/target.html": self.page("/target.html"),
        }
        inbound = {"/target.html": {"/source.html": ["Target"]}}
        results = self.run_gate(pages, inbound)

        self.assertTrue(all(result.ok for result in results.values()))

    def test_noindex_auth_target_is_allowed(self):
        pages = {
            "/source.html": self.page("/source.html"),
            "/dealer/login.html": self.page(
                "/dealer/login.html", '<meta name="robots" content="noindex">'
            ),
        }
        inbound = {
            "/dealer/login.html": {"/source.html": ["Dealer sign in"]}
        }
        results = self.run_gate(pages, inbound)

        self.assertTrue(all(result.ok for result in results.values()))

    def test_exact_held_edge_is_allowed_but_new_source_is_blocked(self):
        held_source = "/scope-engine.html"
        new_source = "/new-source.html"
        held_target = "/commercial-glazing-nashville-tn.html"
        pages = {
            held_source: self.page(held_source),
            new_source: self.page(new_source),
            held_target: self.page(
                held_target, '<meta name="robots" content="noindex">'
            ),
        }

        held_only = self.run_gate(
            pages,
            {held_target: {held_source: ["Held destination"]}},
        )
        self.assertTrue(all(result.ok for result in held_only.values()))

        with_new_source = self.run_gate(
            pages,
            {
                held_target: {
                    held_source: ["Held destination"],
                    new_source: ["New destination"],
                }
            },
        )
        result = with_new_source[
            "Indexable pages do not link to noindex pages"
        ]
        self.assertFalse(result.ok)
        self.assertIn(new_source, result.detail)


if __name__ == "__main__":
    unittest.main(verbosity=2)
