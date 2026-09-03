#!/usr/bin/env python3
"""FormSubmit AJAX forms must require HTTP OK and JSON success:true."""

from __future__ import annotations

import re
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[3]

# Public FormSubmit AJAX handlers. bid.html / scope-engine.html already gate
# correctly; contact + Nashville early-bid were treating response.ok as success.
AJAX_FORMS = (
    ("contact.html", "function handleContactSubmit"),
    ("commercial-glazing-nashville-tn.html", "function submitIntake"),
    ("bid.html", "function sendBidAjax"),
    ("scope-engine.html", "formsubmit ALWAYS returns HTTP 200"),
)

GATE = "r.ok && String(data.success) === 'true'"
BARE_OK = re.compile(r"if\s*\(\s*(?:response|r)\.ok\s*\)")
THANKS_REDIRECT = "window.location.href = '/thanks.html'"


def read(rel: str) -> str:
    return (REPO_ROOT / rel).read_text(encoding="utf-8")


def handler_source(html: str, marker: str) -> str:
    start = html.find(marker)
    if start < 0:
        return ""
    return html[start:]


class FormSubmitAjaxSuccessGatingTests(unittest.TestCase):
    def test_public_ajax_forms_require_json_success(self):
        for rel, marker in AJAX_FORMS:
            with self.subTest(rel=rel):
                html = read(rel)
                source = handler_source(html, marker)
                self.assertTrue(source, f"missing handler marker in {rel}")
                self.assertIn(GATE, source)
                self.assertIsNone(
                    BARE_OK.search(source),
                    f"{rel} still treats HTTP OK alone as FormSubmit success",
                )

    def test_contact_redirects_and_fires_lead_only_after_confirmed_success(self):
        html = read("contact.html")
        source = handler_source(html, "function handleContactSubmit")
        gate = source.find(GATE)
        lead = source.find("generate_lead")
        thanks = source.find(THANKS_REDIRECT)
        self.assertGreater(gate, 0)
        self.assertGreater(lead, gate)
        self.assertGreater(thanks, gate)
        self.assertNotIn("form.reset()", source)
        self.assertEqual(source.count("generate_lead"), 1)
        self.assertEqual(html.count(THANKS_REDIRECT), 1)

    def test_contact_failure_keeps_form_and_offers_fallback(self):
        html = read("contact.html")
        source = handler_source(html, "function handleContactSubmit")
        self.assertIn('href="/send-plans.html"', source)
        self.assertIn("mailto:connor@acglass.com", source)
        self.assertIn("tel:+17724867711", source)
        self.assertIn("form_submission_failed", source)
        fail = source.find("form_submission_failed")
        thanks = source.find(THANKS_REDIRECT)
        self.assertGreater(fail, 0)
        self.assertLess(thanks, fail)

    def test_nashville_early_bid_gates_success_and_does_not_clear_on_reject(self):
        html = read("commercial-glazing-nashville-tn.html")
        source = handler_source(html, "function submitIntake")
        gate = source.find(GATE)
        lead = source.find("generate_lead")
        reset = source.find("form.reset()")
        self.assertGreater(gate, 0)
        self.assertGreater(lead, gate)
        self.assertGreater(reset, gate)
        self.assertEqual(source.count("form.reset()"), 1)
        self.assertEqual(source.count("generate_lead"), 1)
        self.assertIn('id="intakeStatus"', html)
        self.assertIn('href="/send-plans.html"', source)
        self.assertIn("mailto:connor@acglass.com", source)
        self.assertIn("tel:+17724867711", source)
        self.assertIn("form_submission_failed", source)

    def test_no_other_public_formsubmit_ajax_uses_bare_ok(self):
        offenders = []
        for path in REPO_ROOT.rglob("*.html"):
            if "/.git/" in str(path):
                continue
            text = path.read_text(encoding="utf-8", errors="replace")
            if "formsubmit.co/ajax/" not in text:
                continue
            rel = str(path.relative_to(REPO_ROOT))
            if BARE_OK.search(text) and GATE not in text:
                offenders.append(rel)
        self.assertEqual(offenders, [])


if __name__ == "__main__":
    unittest.main(verbosity=2)
