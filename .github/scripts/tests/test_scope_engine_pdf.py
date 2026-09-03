#!/usr/bin/env python3
"""Guard Scope Engine PDF library: same working jsPDF pin as Bid Engine."""

from __future__ import annotations

import re
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[3]
SCOPE = (REPO_ROOT / "scope-engine.html").read_text(encoding="utf-8")

JSPDF_SRC = "https://cdnjs.cloudflare.com/ajax/libs/jspdf/2.5.1/jspdf.umd.min.js"
JSPDF_SRI = "sha384-JcnsjUPPylna1s1fvi1u12X5qjY5OL56iySh75FdtrwhO/SWXgMjoVqcKyIIWOLk"


def _function_body(name: str) -> str:
    start = SCOPE.find(f"function {name}(")
    if start < 0:
        raise AssertionError(f"missing function {name}()")
    depth = 0
    i = SCOPE.find("{", start)
    for j in range(i, len(SCOPE)):
        if SCOPE[j] == "{":
            depth += 1
        elif SCOPE[j] == "}":
            depth -= 1
            if depth == 0:
                return SCOPE[start : j + 1]
    raise AssertionError(f"unclosed function {name}()")


class ScopeEnginePdfLibraryTests(unittest.TestCase):
    def test_jspdf_script_is_the_pinned_working_cdnjs_url(self):
        scripts = re.findall(r"<script\b[^>]*\bsrc=['\"]([^'\"]+)['\"]", SCOPE)
        jspdf = [src for src in scripts if "jspdf" in src.lower()]
        self.assertEqual([JSPDF_SRC], jspdf)
        self.assertNotIn("/jspdf/2.5.2/", SCOPE)
        self.assertIn(f'integrity="{JSPDF_SRI}"', SCOPE)
        self.assertIn("crossorigin", SCOPE)

    def test_generate_branded_pdf_uses_defensive_ctor(self):
        fn = _function_body("generateBrandedPDF")
        self.assertIn("function jspdfCtor()", SCOPE)
        self.assertIn("window.jspdf && window.jspdf.jsPDF", SCOPE)
        self.assertIn("jspdfCtor()", fn)
        self.assertNotRegex(
            fn,
            r"function generateBrandedPDF\(\)\s*\{\s*const\s*\{\s*jsPDF\s*\}\s*=\s*window\.jspdf",
        )
        self.assertIn("jsPDF not loaded yet", fn)
        self.assertIn("return null", fn)


if __name__ == "__main__":
    unittest.main(verbosity=2)
