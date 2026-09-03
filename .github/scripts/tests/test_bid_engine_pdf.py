#!/usr/bin/env python3
"""Guard Bid Engine PDF deliverable: real jsPDF URL, honest copy, confirmed-only control."""

from __future__ import annotations

import importlib.util
import re
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[3]
BID = (REPO_ROOT / "bid.html").read_text(encoding="utf-8")

# Last 2.5.x UMD on cdnjs that returns 200 application/javascript.
# 2.5.2 does not exist there (404, text/html) and was the live breakage.
JSPDF_SRC = "https://cdnjs.cloudflare.com/ajax/libs/jspdf/2.5.1/jspdf.umd.min.js"
JSPDF_SRI = "sha384-JcnsjUPPylna1s1fvi1u12X5qjY5OL56iySh75FdtrwhO/SWXgMjoVqcKyIIWOLk"
TITLE_MAX = 60
TITLE_MIN = 30


def _load_checker():
    spec = importlib.util.spec_from_file_location(
        "crawl_check",
        Path(__file__).resolve().parents[1] / "crawl-check.py",
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _function_body(name: str) -> str:
    start = BID.find(f"function {name}(")
    if start < 0:
        raise AssertionError(f"missing function {name}()")
    depth = 0
    i = BID.find("{", start)
    for j in range(i, len(BID)):
        if BID[j] == "{":
            depth += 1
        elif BID[j] == "}":
            depth -= 1
            if depth == 0:
                return BID[start : j + 1]
    raise AssertionError(f"unclosed function {name}()")


def _between(start_token: str, end_token: str) -> str:
    start = BID.find(start_token)
    if start < 0:
        raise AssertionError(f"missing {start_token}")
    end = BID.find(end_token, start)
    if end < 0:
        raise AssertionError(f"missing {end_token} after {start_token}")
    return BID[start:end]


class BidEnginePdfLibraryTests(unittest.TestCase):
    def test_jspdf_script_is_the_pinned_working_cdnjs_url(self):
        scripts = re.findall(r"<script\b[^>]*\bsrc=['\"]([^'\"]+)['\"]", BID)
        jspdf = [src for src in scripts if "jspdf" in src.lower()]
        self.assertEqual([JSPDF_SRC], jspdf)
        self.assertNotIn("/jspdf/2.5.2/", BID)
        self.assertIn(f'integrity="{JSPDF_SRI}"', BID)
        self.assertIn("crossorigin", BID)


class BidEnginePdfButtonTests(unittest.TestCase):
    def test_download_control_is_in_confirmed_results_not_cost_card(self):
        results = _between('id="results-panel"', "<!-- end results-panel -->")
        fail = _between('id="send-fail-panel"', 'id="results-panel"')
        self.assertIn('id="download-pdf-btn"', results)
        self.assertIn("Download Preliminary Scope (PDF)", results)
        self.assertNotIn("Official Bid Estimate", BID)
        self.assertNotIn("be-cost-card", BID)
        self.assertNotIn("be-cost-display", BID)
        self.assertNotIn('id="download-pdf-btn"', fail)
        show = _function_body("showResults")
        self.assertIn("preparePdfDownload()", show)
        self.assertNotIn("be-cost-card", show)
        self.assertNotIn("be-cost-display", show)
        self.assertNotIn("createElement", show)


class BidEnginePdfFailureGuardTests(unittest.TestCase):
    def test_generate_bid_pdf_returns_when_library_or_data_missing(self):
        fn = _function_body("generateBidPDF")
        self.assertIn("function jspdfCtor()", BID)
        self.assertIn("window.jspdf && window.jspdf.jsPDF", BID)
        self.assertNotRegex(
            fn,
            r"function generateBidPDF\(\)\s*\{\s*const\s*\{\s*jsPDF\s*\}\s*=\s*window\.jspdf",
        )
        self.assertIn("jspdfCtor()", fn)
        self.assertIn("The PDF library did not load", fn)
        self.assertIn("hasScopePdfData()", fn)
        self.assertIn("return false", fn)
        self.assertIn("try {", fn)
        self.assertIn("catch", fn)
        self.assertIn("ACG-Scope-Summary-", fn)
        self.assertIn("PRELIMINARY SCOPE ESTIMATE", fn)
        self.assertIn("formatRequirements()", fn)

    def test_show_results_stays_behind_confirmed_send(self):
        # Preserve PR 78 gating: native submit happens before showResults,
        # and the return path requires the awaiting-confirm flag.
        overlay = BID.find("function runAnalysisAndSend()")
        results_call = BID.find("showResults()", overlay)
        native_submit = BID.find("bid-form').submit()", overlay)
        self.assertGreater(overlay, 0)
        self.assertGreater(results_call, overlay)
        self.assertGreater(native_submit, overlay)
        self.assertLess(native_submit, results_call)
        restore = _function_body("restoreAfterConfirmedSend")
        self.assertIn("acg_bid_engine_awaiting_confirm", BID)
        self.assertIn("submitted", restore)
        self.assertIn("showResults()", restore)


class BidEnginePdfTitleTests(unittest.TestCase):
    def test_title_includes_hours_and_fits_limit(self):
        checker = _load_checker()
        title = checker.title_content(BID)
        self.assertIn("48 Hours", title)
        self.assertGreaterEqual(len(title), TITLE_MIN)
        self.assertLessEqual(len(title), TITLE_MAX)
        self.assertLessEqual(len(title), checker.TITLE_MAX)
        self.assertNotEqual(
            title,
            "ACG Bid Engine | Upload Plans. Get a Glazing Scope in 48",
        )
        self.assertIn(
            'content="ACG Bid Engine | Upload Plans. Get a Glazing Scope in 48 Hours."',
            BID,
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
