#!/usr/bin/env python3
"""Guard the Send plans conversion path so CTAs land on the real intake form."""

from __future__ import annotations

import re
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[3]


def read(rel: str) -> str:
    return (REPO_ROOT / rel).read_text(encoding="utf-8")


class SendPlansCtaTests(unittest.TestCase):
    def test_homepage_send_plans_ctas_go_to_intake(self):
        html = read("index.html")
        self.assertIn('class="btn-plans" href="/send-plans.html">Send plans</a>', html)
        self.assertEqual(
            html.count('href="/send-plans.html">Send plans</a>'),
            4,
            "header, hero, #contact, and footer should all point Send plans at intake",
        )
        self.assertNotIn('href="/scope-engine.html">Send plans</a>', html)

    def test_shared_chrome_send_plans_goes_to_intake(self):
        for rel in ("portfolio.html", "past-performance.html", "index-proof.html"):
            with self.subTest(rel=rel):
                html = read(rel)
                self.assertIn('class="btn-plans" href="/send-plans.html">Send plans</a>', html)
                self.assertNotIn('href="/scope-engine.html">Send plans</a>', html)

    def test_contact_is_not_labeled_as_plan_intake(self):
        html = read("contact.html")
        self.assertIn("<title>Contact ACG | American Commercial Glass</title>", html)
        self.assertIn("Send inquiry", html)
        self.assertIsNone(
            re.search(r"<button[^>]*>\s*Send Us Plans", html),
            "contact submit must not claim to take plans",
        )
        self.assertIn('class="hd-cta">Send Us Plans</a>', html)
        self.assertIn("this form does not accept files", html)
        self.assertIn('href="send-plans.html"', html)
        self.assertIn("window.location.href = '/thanks.html?submitted=1'", html)
        self.assertNotIn('type="file"', html)

    def test_send_plans_posts_files_and_nexts_to_thanks(self):
        html = read("send-plans.html")
        self.assertIn('enctype="multipart/form-data"', html)
        self.assertIn('name="files[]"', html)
        self.assertIn('type="file"', html)
        self.assertIn(
            'name="_next" value="https://acglass.com/thanks.html?submitted=1"',
            html,
        )
        self.assertIn("https://formsubmit.co/connor@acglass.com", html)

    def test_thanks_page_exists_and_thank_you_forwards(self):
        thanks = read("thanks.html")
        self.assertIn("Thanks. We have it.", thanks)
        self.assertIn('id="thanks-confirmed" hidden', thanks)
        self.assertIn("No new submission confirmed", thanks)
        self.assertIn("noindex", thanks)
        self.assertIn("/send-plans.html", thanks)
        stub = read("thank-you.html")
        self.assertIn('content="0;url=/thanks.html"', stub)
        self.assertIn("noindex", stub)

    def test_high_intent_rfq_request_a_bid_goes_to_send_plans(self):
        pages = (
            "services.html",
            "about.html",
            "portfolio.html",
            "capabilities.html",
            "leadership.html",
        )
        bid_link = re.compile(
            r'<a href="([^"]+)"[^>]*>Request a bid',
            re.IGNORECASE,
        )
        for rel in pages:
            with self.subTest(rel=rel):
                html = read(rel)
                start = html.find("<!-- ACG RFQ BLOCK -->")
                end = html.find("<!-- /ACG RFQ BLOCK -->")
                self.assertGreater(start, 0)
                self.assertGreater(end, start)
                block = html[start:end]
                self.assertIn(
                    "Send us the drawings. Scope letter back in 48 hours.",
                    block,
                )
                hrefs = bid_link.findall(block)
                self.assertEqual(hrefs, ["/send-plans.html"])
                self.assertNotIn(
                    'href="/scope-engine.html">Request a bid',
                    block,
                )
                self.assertIn('href="/scope-engine.html"', block)
                self.assertIn(">Scope Engine</a>", block)
                self.assertIn('href="/contact.html"', block)


if __name__ == "__main__":
    unittest.main(verbosity=2)
