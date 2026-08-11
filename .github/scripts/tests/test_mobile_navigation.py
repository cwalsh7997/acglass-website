#!/usr/bin/env python3

from __future__ import annotations

import re
import unittest
from pathlib import Path
from urllib.parse import urljoin


REPO_ROOT = Path(__file__).resolve().parents[3]
MAIN_JS = (REPO_ROOT / "js/main.js").read_text(encoding="utf-8")
CHROME_JS = (REPO_ROOT / "js/acg-chrome.js").read_text(encoding="utf-8")
ACG2026_JS = (REPO_ROOT / "js/acg2026.js").read_text(encoding="utf-8")
CHROME_CSS = (REPO_ROOT / "css/acg-chrome.css").read_text(encoding="utf-8")


class MobileNavigationTests(unittest.TestCase):
    def test_sticky_send_plans_url_resolves_from_nested_pages(self):
        match = re.search(
            r'<a href="([^"]+)" class="mcb-btn mcb-plans"', MAIN_JS
        )
        self.assertIsNotNone(match, "sticky Send Plans CTA was not found")
        self.assertEqual("/send-plans.html", match.group(1))
        self.assertEqual(
            "https://acglass.com/send-plans.html",
            urljoin("https://acglass.com/nashville/project/", match.group(1)),
        )

    def test_closed_chrome_menu_is_not_focusable(self):
        self.assertRegex(
            CHROME_CSS,
            r"\.hd-mobile\{[^}]*visibility:hidden[^}]*pointer-events:none",
        )
        self.assertRegex(
            CHROME_CSS,
            r"\.hd-mobile\.open\{[^}]*visibility:visible[^}]*pointer-events:auto",
        )
        for script in (CHROME_JS, ACG2026_JS):
            with self.subTest(script=script.splitlines()[0]):
                self.assertIn("mobile.setAttribute('inert', '')", script)
                self.assertIn("mobile.removeAttribute('inert')", script)

    def test_escape_closes_each_menu_and_restores_button_focus(self):
        for script in (MAIN_JS, CHROME_JS, ACG2026_JS):
            with self.subTest(script=script.splitlines()[0]):
                self.assertRegex(script, r"(?:e|event)\.key === 'Escape'")
                self.assertRegex(script, r"setMenuState\(false, true\)")
                self.assertRegex(script, r"if \(returnFocus\) \w+\.focus\(\)")

    def test_legacy_menu_keeps_scroll_lock_and_inert_state_in_sync(self):
        self.assertIn("document.body.style.overflow = open ? 'hidden' : ''", MAIN_JS)
        self.assertIn("navLinks.setAttribute('inert', '')", MAIN_JS)
        self.assertIn("navLinks.removeAttribute('inert')", MAIN_JS)
        self.assertIn("setMenuState(false, true)", MAIN_JS)


if __name__ == "__main__":
    unittest.main(verbosity=2)
