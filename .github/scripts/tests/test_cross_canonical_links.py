#!/usr/bin/env python3

from __future__ import annotations

import importlib.util
import json
import sys
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[3]
SPEC = importlib.util.spec_from_file_location(
    "canonical_verify_cross_links",
    REPO_ROOT / ".github/scripts/canonical-verify.py",
)
CV = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = CV
SPEC.loader.exec_module(CV)


class CrossCanonicalLinkTests(unittest.TestCase):
    def test_safe_indexable_edge_fails(self):
        edges = {("safe.html", "/alias"): ["/alias/ :: Same visible text"]}
        offenders, frozen, matched, stale = CV.classify_cross_canonical_edges(
            edges, {"safe.html"}, set(), {}
        )
        self.assertEqual(1, len(offenders))
        self.assertEqual([], frozen)
        self.assertEqual(set(), matched)
        self.assertEqual([], stale)

    def test_exact_hold_is_allowed_but_changed_hold_fails(self):
        edge = ("held.html", "/alias")
        entries = ["/alias/ :: Same visible text"]
        held = {edge: CV.cross_canonical_edge_fingerprint(entries)}
        exact = CV.classify_cross_canonical_edges(
            {edge: entries}, {"held.html"}, set(), held
        )
        self.assertEqual([], exact[0])
        self.assertEqual({edge}, exact[2])
        self.assertEqual([], exact[3])

        changed = CV.classify_cross_canonical_edges(
            {edge: ["/alias/ :: Changed text"]}, {"held.html"}, set(), held
        )
        self.assertEqual(1, len(changed[0]))
        self.assertEqual([edge], changed[3])

    def test_unpinned_frozen_edge_fails(self):
        edge = ("frozen.html", "/alias")
        result = CV.classify_cross_canonical_edges(
            {edge: ["/alias/ :: Frozen"]}, {"frozen.html"}, {"frozen.html"}, {}
        )
        self.assertEqual([], result[0])
        self.assertEqual(1, len(result[1]))

    def test_repo_has_only_exact_held_cross_canonical_debt(self):
        registry = json.loads(
            (REPO_ROOT / ".github/seo/url-primaries.json").read_text(encoding="utf-8")
        )
        aliases, edges, indexable, frozen = CV.cross_canonical_inventory(
            registry, CV.redirect_sources()
        )
        offenders, unpinned, matched, stale = CV.classify_cross_canonical_edges(
            edges,
            indexable,
            frozen,
            CV.HELD_CROSS_CANONICAL_EDGE_HASHES,
        )
        declared = {
            CV.norm(intent["primary"])
            for intent in registry["intents"] if intent.get("primary")
        }
        self.assertTrue(aliases)
        self.assertTrue(all(CV.norm(primary) in declared for primary in aliases.values()))
        self.assertEqual([], offenders)
        self.assertEqual([], unpinned)
        self.assertEqual(set(CV.HELD_CROSS_CANONICAL_EDGE_HASHES), matched)
        self.assertEqual([], stale)


if __name__ == "__main__":
    unittest.main(verbosity=2)
