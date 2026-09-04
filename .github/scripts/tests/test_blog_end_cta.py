#!/usr/bin/env python3
"""Guard the shared blog end CTA: copy, skip rules, and chrome loader."""

from __future__ import annotations

import re
import unittest
from html.parser import HTMLParser
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[3]
CTA_JS = (REPO_ROOT / "js/acg-blog-cta.js").read_text(encoding="utf-8")
CTA_CSS = (REPO_ROOT / "css/acg-blog-cta.css").read_text(encoding="utf-8")
CHROME_JS = (REPO_ROOT / "js/acg-chrome.js").read_text(encoding="utf-8")
BLOG_DIR = REPO_ROOT / "blog"

CHROME_ANCESTOR = re.compile(
    r"header|nav|footer|\.hd|\.hd-mobile|\.hd-cta|\.hd-mobile-cta|\.ft|\.mobile-cta-bar"
)
SEND_HREF = re.compile(r'href=["\']([^"\']*send-plans[^"\']*)["\']', re.I)
PROHIBITED_COPY = (
    "350+",
    "1M SF",
    "1M sf",
    "Nashville office",
    "Nashville HQ",
    "WBENC",
    "\u2013",
    "\u2014",
    "&ndash;",
    "&mdash;",
)


def read(rel: str) -> str:
    return (REPO_ROOT / rel).read_text(encoding="utf-8")


class _LinkScanner(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.stack: list[tuple[str, set[str]]] = []
        self.in_chrome = 0
        self.body_buttons: list[str] = []
        self._capture: list[str] | None = None
        self._capture_cls = ""
        self._capture_style = ""
        self._capture_chrome = False
        self.has_rfq = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attrs_d = {k: (v or "") for k, v in attrs}
        classes = set(attrs_d.get("class", "").split())
        self.stack.append((tag, classes))
        chrome_here = tag in {"header", "nav", "footer"} or bool(
            classes
            & {
                "hd",
                "hd-cta",
                "hd-mobile",
                "hd-mobile-cta",
                "ft",
                "mobile-cta-bar",
            }
        )
        if chrome_here:
            self.in_chrome += 1
        if "acg-rfq" in classes or "bdgc-cta" in classes:
            self.has_rfq = True
        if tag == "a" and "send-plans" in attrs_d.get("href", "").lower():
            self._capture = []
            self._capture_cls = attrs_d.get("class", "")
            self._capture_style = attrs_d.get("style", "")
            self._capture_chrome = self.in_chrome > 0

    def handle_endtag(self, tag: str) -> None:
        if self._capture is not None and tag == "a":
            text = re.sub(r"\s+", " ", "".join(self._capture)).strip()
            style = self._capture_style
            is_btn = (
                bool(re.search(r"send us plans", text, re.I))
                or "btn" in self._capture_cls.split()
                or ("padding" in style and "background" in style)
            )
            if is_btn and not self._capture_chrome:
                self.body_buttons.append(text)
            self._capture = None
        for i in range(len(self.stack) - 1, -1, -1):
            if self.stack[i][0] == tag:
                classes = self.stack[i][1]
                chrome_here = tag in {"header", "nav", "footer"} or bool(
                    classes
                    & {
                        "hd",
                        "hd-cta",
                        "hd-mobile",
                        "hd-mobile-cta",
                        "ft",
                        "mobile-cta-bar",
                    }
                )
                if chrome_here and self.in_chrome:
                    self.in_chrome -= 1
                del self.stack[i]
                break

    def handle_data(self, data: str) -> None:
        if "Pricing this scope" in data:
            self.has_rfq = True
        if self._capture is not None:
            self._capture.append(data)


def page_has_body_cta(html: str) -> bool:
    parser = _LinkScanner()
    parser.feed(html)
    return parser.has_rfq or bool(parser.body_buttons)


def is_refresh_stub(html: str) -> bool:
    return bool(re.search(r'http-equiv=["\']refresh', html, re.I))


class BlogEndCtaTests(unittest.TestCase):
    def test_shared_files_exist_and_chrome_loads_them(self):
        self.assertTrue((REPO_ROOT / "js/acg-blog-cta.js").is_file())
        self.assertTrue((REPO_ROOT / "css/acg-blog-cta.css").is_file())
        self.assertIn("/js/acg-blog-cta.js", CHROME_JS)
        self.assertIn("/css/acg-blog-cta.css", CHROME_JS)
        self.assertIn("index.html", CHROME_JS)
        self.assertIn("/blog/", CHROME_JS)
        self.assertIn("bid-day-glazing-checker.html", CHROME_JS)

    def test_cta_copy_is_constrained(self):
        blob = CTA_JS + "\n" + CTA_CSS
        self.assertIn("/send-plans.html", CTA_JS)
        self.assertIn("tel:+17724867711", CTA_JS)
        self.assertIn("(772) 486-7711", CTA_JS)
        self.assertIn("FL CGC #1531993", CTA_JS)
        self.assertIn("Pricing this scope?", CTA_JS)
        self.assertIn("Working a similar package?", CTA_JS)
        self.assertIn("Send Us Plans", CTA_JS)
        self.assertIn("Send the elevations and the door and window schedule.", CTA_JS)
        self.assertIn("var SEND = '/send-plans.html'", CTA_JS)
        self.assertIn("var TEL = 'tel:+17724867711'", CTA_JS)
        self.assertRegex(CTA_JS, r'href="\' \+ SEND \+ \'"')
        self.assertRegex(CTA_JS, r'href="\' \+ TEL \+ \'"')
        other_hrefs = [
            href
            for href in re.findall(r'href=["\']([^"\']+)["\']', CTA_JS)
            if href not in {"/send-plans.html", "tel:+17724867711"}
        ]
        self.assertEqual(other_hrefs, [])
        for token in PROHIBITED_COPY:
            self.assertNotIn(token, blob)
        self.assertNotIn("WBENC", blob)
        self.assertIn("#0e284f", CTA_CSS)
        self.assertIn("#e11320", CTA_CSS)
        self.assertIn("@media print", CTA_CSS)
        self.assertIn(".mobile-cta-bar", CTA_CSS)
        self.assertIn("padding-bottom: calc(110px", CTA_CSS)

    def test_flagship_already_has_rfq_so_js_will_skip(self):
        html = read("blog/ufc-glazing-vs-florida-noa.html")
        self.assertIn("Pricing this scope?", html)
        self.assertIn('class="acg-rfq"', html)
        self.assertTrue(page_has_body_cta(html))

    def test_project_with_body_button_is_skipped(self):
        html = read("blog/cubesmart-davie-glazing.html")
        self.assertTrue(page_has_body_cta(html))
        self.assertIn("send-plans.html", html)

    def test_mill_contact_cta_does_not_count(self):
        html = read("blog/how-to-get-a-glazing-bid-florida.html")
        self.assertFalse(page_has_body_cta(html))
        self.assertIn("../contact.html", html)
        self.assertIn("class=\"hd-cta\"", html)

    def test_project_contact_cta_does_not_count(self):
        html = read("blog/waxins-eurowall-clematis-street.html")
        self.assertFalse(page_has_body_cta(html))
        self.assertIn("../contact.html", html)

    def test_bid_day_tool_already_has_end_cta(self):
        html = read("tools/bid-day-glazing-checker.html")
        self.assertIn('class="bdgc-cta"', html)
        self.assertIn('href="/send-plans.html"', html)
        self.assertIn("Send Us Plans", html)
        self.assertTrue(page_has_body_cta(html))

    def test_every_blog_post_loads_chrome_and_index_is_excluded(self):
        posts = sorted(BLOG_DIR.glob("*.html"))
        self.assertGreater(len(posts), 200)
        index = read("blog/index.html")
        self.assertIn("acg-chrome.js", index)
        missing = []
        add = 0
        skip = 0
        stubs = 0
        for path in posts:
            html = path.read_text(encoding="utf-8")
            if path.name == "index.html":
                continue
            if is_refresh_stub(html):
                stubs += 1
                continue
            if "acg-chrome.js" not in html:
                missing.append(path.name)
            if page_has_body_cta(html):
                skip += 1
            else:
                add += 1
        self.assertEqual(missing, [])
        self.assertGreaterEqual(add, 100)
        self.assertGreaterEqual(skip, 20)
        self.assertEqual(stubs, 2)
        self.assertIn("file !== 'index.html'", CHROME_JS)

    def test_skip_detects_existing_body_button_helpers_in_js(self):
        self.assertIn("hasExistingBodyCta", CTA_JS)
        self.assertIn(".acg-rfq", CTA_JS)
        self.assertIn(".bdgc-cta", CTA_JS)
        self.assertIn("Pricing this scope?", CTA_JS)
        self.assertIn("About the author", CTA_JS)
        self.assertIn("Related resources", CTA_JS)


if __name__ == "__main__":
    unittest.main(verbosity=2)
