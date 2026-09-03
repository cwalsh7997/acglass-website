#!/usr/bin/env python3
"""Guard send-plans upload copy and client checks against the FormSubmit path."""

from __future__ import annotations

import re
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[3]


def read(rel: str) -> str:
    return (REPO_ROOT / rel).read_text(encoding="utf-8")


class SendPlansFormsubmitBudgetTests(unittest.TestCase):
    def setUp(self):
        self.send = read("send-plans.html")
        self.thanks = read("thanks.html")

    def test_copy_uses_nine_mb_not_twenty_five(self):
        self.assertNotIn("25 MB", self.send)
        self.assertNotIn("25MB", self.send)
        self.assertGreaterEqual(self.send.count("9 MB"), 4)
        self.assertIn("File uploads accept up to 9 MB total.", self.send)
        self.assertIn("PDF, DWG, ZIP, DOCX, XLSX &middot; 9 MB total", self.send)
        self.assertIn("9 MB total through the form.", self.send)

    def test_budget_constant_stays_under_formsubmit_cap(self):
        self.assertIn("var FORMSUBMIT_MAX_BYTES = 9 * 1024 * 1024;", self.send)
        self.assertIn("ALLOWED_EXTS = { pdf:1, dwg:1, zip:1, doc:1, docx:1, xls:1, xlsx:1, jpg:1, jpeg:1, png:1 }", self.send)
        self.assertIn(".pdf,.dwg,.zip,.doc,.docx,.xls,.xlsx,.jpg,.jpeg,.png", self.send)

    def test_oversize_is_blocked_with_gc_handoff(self):
        self.assertIn("if (bytes > FORMSUBMIT_MAX_BYTES)", self.send)
        self.assertIn("e.preventDefault();", self.send)
        self.assertIn("OVERSIZE_COPY", self.send)
        self.assertIn("These files are over the 9 MB form limit, so they were not sent.", self.send)
        self.assertIn("connor@acglass.com", self.send)
        self.assertIn("Procore", self.send)
        self.assertIn("BuildingConnected", self.send)
        self.assertIn("BIM 360", self.send)
        submit = self.send[self.send.find("form.addEventListener('submit'") :]
        self.assertIn("if (!check.ok)", submit)
        self.assertLess(submit.find("e.preventDefault();"), submit.find("sessionStorage.setItem"))
        self.assertNotIn("gtag('event', 'generate_lead'", submit)

    def test_keeps_native_multipart_formsubmit_post(self):
        self.assertIn('action="https://formsubmit.co/connor@acglass.com"', self.send)
        self.assertIn('method="POST"', self.send)
        self.assertIn('enctype="multipart/form-data"', self.send)
        self.assertIn('name="files[]"', self.send)
        self.assertNotIn("formsubmit.co/ajax", self.send)
        self.assertIsNone(re.search(r"fetch\s*\(\s*['\"]https://formsubmit", self.send))

    def test_thanks_only_claims_receipt_after_formsubmit_redirect(self):
        self.assertIn('name="_next" value="https://acglass.com/thanks.html?submitted=1"', self.send)
        self.assertIn("acg_form_awaiting_confirm", self.send)
        self.assertIn("sessionStorage.setItem(AWAITING_KEY, 'send-plans')", self.send)
        self.assertIn('id="thanks-confirmed" hidden', self.thanks)
        self.assertIn('id="thanks-unconfirmed"', self.thanks)
        unconfirmed = self.thanks[
            self.thanks.find('id="thanks-unconfirmed"') : self.thanks.find(
                'id="thanks-confirmed"'
            )
        ]
        self.assertIn("No new submission confirmed", unconfirmed)
        self.assertNotIn("Thanks. We have it.", unconfirmed)
        self.assertNotIn("a copy is with our team", unconfirmed)
        self.assertIn("var redirected = new URLSearchParams(location.search).get('submitted') === '1'", self.thanks)
        self.assertIn("var confirmed = redirected && !!source;", self.thanks)
        self.assertIn("received.hidden = false", self.thanks)
        self.assertIn("Thanks. We have it.", self.thanks[self.thanks.find('id="thanks-confirmed"') :])


if __name__ == "__main__":
    unittest.main(verbosity=2)
