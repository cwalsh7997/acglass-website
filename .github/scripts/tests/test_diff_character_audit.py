#!/usr/bin/env python3

from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path


SCRIPTS_DIR = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "diff_character_audit", SCRIPTS_DIR / "diff-character-audit.py"
)
MODULE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)


def patch_with(line: str) -> str:
    return (
        "diff --git a/page.html b/page.html\n"
        "--- a/page.html\n"
        "+++ b/page.html\n"
        "@@ -1,0 +2,1 @@\n"
        f"+{line}\n"
    )


class DiffCharacterAuditTests(unittest.TestCase):
    def test_plain_text_passes(self):
        self.assertEqual([], MODULE.scan_patch(patch_with("Clear project copy.")))

    def test_hyphenated_terms_pass(self):
        self.assertEqual([], MODULE.scan_patch(patch_with("Impact-rated Low-E glass")))

    def test_unicode_codepoints_fail(self):
        for codepoint in (0x2013, 0x2014):
            with self.subTest(codepoint=codepoint):
                findings = MODULE.scan_patch(
                    patch_with("left" + chr(codepoint) + "right")
                )
                self.assertEqual(1, len(findings))

    def test_html_entities_fail(self):
        for entity in ("&" + "ndash;", "&" + "mdash;", "&" + "NDASH;", "&" + "MDASH;"):
            with self.subTest(entity=entity):
                findings = MODULE.scan_patch(patch_with("left" + entity + "right"))
                self.assertEqual(1, len(findings))

    def test_removed_legacy_character_is_ignored(self):
        patch = (
            "diff --git a/page.html b/page.html\n"
            "--- a/page.html\n"
            "+++ b/page.html\n"
            "@@ -1,1 +1,1 @@\n"
            "-left" + chr(0x2014) + "right\n"
            "+left: right\n"
        )
        self.assertEqual([], MODULE.scan_patch(patch))


if __name__ == "__main__":
    unittest.main(verbosity=2)
