#!/usr/bin/env python3
"""Guard the RFQ success page and plan-intake CTAs."""

from __future__ import annotations

import os
import re
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[3]
SKIP_DIRS = {".git", ".github", "_internal", "node_modules", "dealer"}
WAVE4 = {
    "about.html",
    "contact.html",
    "portfolio.html",
    "west-palm-beach-commercial-glazing.html",
    "index.html",
    "florida-commercial-glazing/index.html",
    "miami-dade-noa-explained/index.html",
    "blog/what-is-division-08-construction.html",
    "blog/commercial-glazing-warranties-florida.html",
    "blog/commercial-glazing-submittal-process-guide.html",
    "blog/what-does-a-glazing-contractor-do.html",
    "blog/florida-building-codes-commercial-glazing-2026.html",
    "blog/commercial-glazing-project-turnaround-time-florida.html",
}

ANCHOR = re.compile(
    r'<a\b[^>]*\bhref=["\']([^"\']+)["\'][^>]*>(.*?)</a>',
    re.I | re.S,
)
PLAN_LABEL = re.compile(
    r"send\s+us\s+(your\s+)?plans|send\s+us\s+your\s+drawings|send\s+your\s+plans|"
    r"send\s+drawings|send\s+bid\s+drawings|send\s+the\s+spec|upload\s+drawings",
    re.I,
)


def read(rel: str) -> str:
    return (REPO_ROOT / rel).read_text(encoding="utf-8")


def visible_text(html: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", html)).strip()


class ThanksIntakeTests(unittest.TestCase):
    def test_thanks_directory_alias_forwards_and_stays_noindex(self):
        alias = read("thanks/index.html")
        self.assertIn('rel="canonical"', alias)
        self.assertIn("https://acglass.com/thanks.html", alias)
        self.assertIn("noindex", alias)
        self.assertIn("location.search", alias)
        self.assertIn("/thanks.html", alias)

    def test_thanks_confirms_from_session_flag_not_query_alone(self):
        thanks = read("thanks.html")
        self.assertIn("var confirmed = !!source;", thanks)
        self.assertNotIn("var confirmed = redirected && !!source;", thanks)
        self.assertIn("Thanks. We have your plans.", thanks)
        self.assertIn("This path does not attach drawings", thanks)
        self.assertIn("noindex", thanks)

    def test_partners_form_posts_to_thanks_and_does_not_claim_files(self):
        html = read("partners.html")
        self.assertIn('action="https://formsubmit.co/connor@acglass.com"', html)
        self.assertIn(
            'name="_next" value="https://acglass.com/thanks.html?submitted=1"',
            html,
        )
        self.assertIn("acg_form_awaiting_confirm", html)
        self.assertNotIn("handlePartnerSubmit", html)
        self.assertNotIn('type="file"', html)
        self.assertIn("This form does not attach files", html)
        self.assertIn("/send-plans.html", html)

    def test_scope_engine_does_not_claim_emailed_pdf(self):
        html = read("scope-engine.html")
        self.assertNotIn("emailed to you AND downloaded", html)
        self.assertNotIn("your report is on its way to your inbox", html)
        self.assertIn("FormSubmit does not attach that PDF", html)
        self.assertIn('href="/send-plans.html"', html)

    def test_non_wave4_plan_upload_ctas_do_not_point_at_contact(self):
        leftovers = []
        for dirpath, dirnames, filenames in os.walk(REPO_ROOT):
            dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
            for fn in filenames:
                if not fn.endswith(".html"):
                    continue
                path = Path(dirpath) / fn
                rel = path.relative_to(REPO_ROOT).as_posix()
                if rel in WAVE4:
                    continue
                html = path.read_text(encoding="utf-8", errors="replace")
                for href, inner in ANCHOR.findall(html):
                    if not PLAN_LABEL.search(visible_text(inner)):
                        continue
                    dest = href.split("?")[0].split("#")[0].rstrip("/")
                    if dest.endswith("contact.html") or dest.endswith("/contact"):
                        leftovers.append((rel, href, visible_text(inner)[:80]))
        self.assertEqual(leftovers, [])


if __name__ == "__main__":
    unittest.main(verbosity=2)
