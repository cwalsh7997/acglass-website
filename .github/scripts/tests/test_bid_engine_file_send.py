#!/usr/bin/env python3
"""Guard Bid Engine so plan files are actually sent, not only shown in the UI."""

from __future__ import annotations

import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[3]
BID = (REPO_ROOT / "bid.html").read_text(encoding="utf-8")
SEND_PLANS = (REPO_ROOT / "send-plans.html").read_text(encoding="utf-8")


class BidEngineFileSendTests(unittest.TestCase):
    def test_hidden_form_is_multipart_to_formsubmit(self):
        self.assertIn('id="bid-form"', BID)
        self.assertIn('enctype="multipart/form-data"', BID)
        self.assertIn("https://formsubmit.co/connor@acglass.com", BID)
        self.assertIn('name="files[]"', BID)
        self.assertIn('id="form-files"', BID)
        self.assertNotIn('action="send-plans.html"', BID)

    def test_files_are_copied_onto_the_form_before_send(self):
        self.assertIn("function attachFilesToForm()", BID)
        self.assertIn("input.files = dt.files", BID)
        self.assertIn("state.uploadedFiles.forEach", BID)

    def test_success_is_gated_on_confirmed_send(self):
        self.assertNotIn(".catch(() => {})", BID)
        self.assertIn("showSendFailure", BID)
        self.assertIn("acg_bid_engine_awaiting_confirm", BID)
        self.assertIn("String(data.success) === 'true'", BID)
        self.assertIn("bid.html?submitted=1", BID)
        # Results stay behind a confirmed send; the old overlay called showResults first.
        overlay_idx = BID.find("function runAnalysisAndSend()")
        results_call = BID.find("showResults()", overlay_idx)
        native_submit = BID.find("bid-form').submit()", overlay_idx)
        self.assertGreater(overlay_idx, 0)
        self.assertGreater(results_call, overlay_idx)
        self.assertGreater(native_submit, overlay_idx)
        self.assertLess(native_submit, results_call)

    def test_failure_offers_email_and_send_plans_handoff(self):
        self.assertIn("function continueToSendPlans()", BID)
        self.assertIn("mailto:connor@acglass.com", BID)
        self.assertIn("/send-plans.html", BID)
        self.assertIn("id=\"send-fail-panel\"", BID)
        self.assertIn("from: 'bid-engine'", BID)
        self.assertIn("stashBidHandoff", BID)

    def test_send_plans_restores_bid_engine_files(self):
        self.assertIn("prefillFromBidEngine", SEND_PLANS)
        self.assertIn("restoreBidEngineFiles", SEND_PLANS)
        self.assertIn("acg-bid-handoff", SEND_PLANS)


if __name__ == "__main__":
    unittest.main(verbosity=2)
