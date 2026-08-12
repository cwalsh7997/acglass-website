#!/usr/bin/env python3
"""Accessibility structure checks for priority buyer pages."""

from __future__ import annotations

import hashlib
import html
import re
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[3]
PAGES = (
    "capabilities.html",
    "gc.html",
    "for-general-contractors.html",
)
LANDMARK_ONLY_PAGES = (
    "impact-windows-doors.html",
    "multi-slide-bifold-doors.html",
    "privacy-policy.html",
    "terms-of-use.html",
)
LANDMARK_ONLY_FINGERPRINTS = {
    "impact-windows-doors.html": {
        "head": "0c050792c18e22e7b8adf31d15075d1739f99e74069530bcf787b4d81be38ccc",
        "jsonld": "cbe03bce400f4b8693960a5c82e327a79a509253738e0218f0219f219254ebd3",
        "scripts": "886fe08506e6b1884d31e50b169bca1d5735995f83cd3e9e4d7ac7766499e7a4",
        "hrefs": "7e30d5e0bb79f0616da02b9a99147904c583c8aa00d7595335dae51520775736",
        "visible": "083eb903cf8bc489bb794499f368d7f758bfe6bf390c43a60419a57d9505c76e",
    },
    "multi-slide-bifold-doors.html": {
        "head": "98b48b78f60afbe1fd2f17c8c527c2fb4e7b495eb4a6e148f9879b8b6e531050",
        "jsonld": "432be9b17b3f18a2713c074fde86eae96827e65c4dff3f95cfbe837a6f5ef697",
        "scripts": "2feebda52a455b15084cd36667e638052049110598326beeff6f47e28efd2e25",
        "hrefs": "ae423c9f86df0ebc059db4bfaf61f167b9fda64651a1a3eb0f28e0209f46006e",
        "visible": "7756822ce2c4f3e5bc517240ea6c3e1010424dd3fa14a2bcde9d4d9c242d17c7",
    },
    "privacy-policy.html": {
        "head": "6724051cd3c3b52e4d7356ff3c4634ce8667b9eb3c9b4ea7d17f2e22f84fff32",
        "jsonld": "cf57f2ef73c50d9fdb040a2ff489b1a7e1eaab9bd91e44b065ad2661507ff42d",
        "scripts": "602b81cc175a16c0d7104e55d880b415e295f6aa24f13dbb41c6d89507861945",
        "hrefs": "90d3fd7f9ba02d99f8af0273c3353778bc090581896c722a90f714ec4cc08e4b",
        "visible": "7cb3ed5eab55c71154c0470413e93de7f73e838fb03aac48a85de0e3705bb864",
    },
    "terms-of-use.html": {
        "head": "2034c36628ed34fbea85e0234d7a3fa9005bda35aaa3df6826eaa7d354112426",
        "jsonld": "e0dda3641a0aacd968c4d7fc5fccdf294bd27c72e1d4d04fe9e4f9ba02f5e6d1",
        "scripts": "31c1c638780ee6d016e87b4cc4d6d823c4a41abbfd14225a58d6f5504555f3f4",
        "hrefs": "90d3fd7f9ba02d99f8af0273c3353778bc090581896c722a90f714ec4cc08e4b",
        "visible": "5389bac37fb7c2ef77bebc3f7f2029fde8ef26552da17143ec085cbbe6f2ac00",
    },
}


def _sha256(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def _fingerprints(source: str) -> dict[str, str]:
    head = re.search(r"<head\b[^>]*>.*?</head>", source, re.I | re.S)
    body = re.search(r"<body\b[^>]*>(.*?)</body>", source, re.I | re.S)
    assert head is not None
    assert body is not None
    jsonld = re.findall(
        r'<script\b[^>]*type=["\']application/ld\+json["\'][^>]*>.*?</script>',
        source,
        re.I | re.S,
    )
    scripts = re.findall(r"<script\b[^>]*>.*?</script>", source, re.I | re.S)
    hrefs = re.findall(r'<a\b[^>]*\bhref=["\']([^"\']*)["\']', source, re.I)
    visible = re.sub(
        r"<(?:script|style)\b[^>]*>.*?</(?:script|style)>",
        " ",
        body.group(1),
        flags=re.I | re.S,
    )
    visible = " ".join(html.unescape(re.sub(r"<[^>]+>", " ", visible)).split())
    return {
        "head": _sha256(head.group(0)),
        "jsonld": _sha256("\n".join(jsonld)),
        "scripts": _sha256("\n".join(scripts)),
        "hrefs": _sha256("\n".join(hrefs)),
        "visible": _sha256(visible),
    }


class PriorityAccessibilityTests(unittest.TestCase):
    def test_pages_have_one_skip_target_and_one_main_landmark(self):
        for rel in PAGES:
            with self.subTest(rel=rel):
                source = (REPO_ROOT / rel).read_text(encoding="utf-8")
                self.assertEqual(
                    1,
                    source.count('<main id="main-content" tabindex="-1">'),
                )
                self.assertEqual(1, source.count("</main>"))
                self.assertEqual(
                    1,
                    source.count(
                        '<a class="skip-link" href="#main-content">'
                    ),
                )
                self.assertLess(source.index("<main"), source.index("<h1"))
                self.assertLess(source.index("</header>"), source.index("<main"))
                self.assertLess(source.index("</main>"), source.index("<footer"))

    def test_primary_service_hubs_have_one_main_without_content_drift(self):
        for rel in LANDMARK_ONLY_PAGES:
            with self.subTest(rel=rel):
                source = (REPO_ROOT / rel).read_text(encoding="utf-8")
                self.assertEqual(
                    1,
                    source.count('<main id="main-content" tabindex="-1">'),
                )
                self.assertEqual(1, source.count("</main>"))
                self.assertEqual(1, source.count('id="main-content"'))
                self.assertEqual(
                    1,
                    source.count('<a class="skip-link" href="#main-content">'),
                )
                self.assertLess(source.index("</header>"), source.index("<main"))
                self.assertLess(source.index("<main"), source.index("<h1"))
                self.assertLess(source.index("<h1"), source.index("</main>"))
                self.assertLess(source.index("</main>"), source.index("<footer"))
                self.assertEqual(0, len(re.findall(r"<form\b", source, re.I)))
                self.assertEqual(
                    LANDMARK_ONLY_FINGERPRINTS[rel],
                    _fingerprints(source),
                )

    def test_main_content_heading_levels_do_not_skip(self):
        for rel in PAGES:
            with self.subTest(rel=rel):
                source = (REPO_ROOT / rel).read_text(encoding="utf-8")
                main = source.split("<main", 1)[1].split("</main>", 1)[0]
                levels = [
                    int(level)
                    for level in re.findall(r"<h([1-6])\b", main, re.I)
                ]
                self.assertTrue(levels)
                self.assertEqual(1, levels[0])
                for previous, current in zip(levels, levels[1:]):
                    self.assertLessEqual(current, previous + 1)

    def test_smooth_scroll_excludes_skip_links(self):
        source = (REPO_ROOT / "js/main.js").read_text(encoding="utf-8")
        self.assertIn(
            'document.querySelectorAll(\'.skip-link[href^="#"]\')',
            source,
        )
        self.assertIn(
            "window.setTimeout(() => target.focus({ preventScroll: true }), 0);",
            source,
        )
        self.assertIn(
            'document.querySelectorAll(\'a[href^="#"]:not(.skip-link)\')',
            source,
        )
        self.assertNotIn(
            'document.querySelectorAll(\'a[href^="#"]\')',
            source,
        )

    def test_general_contractor_skip_link_is_visible_above_fixed_header(self):
        source = (REPO_ROOT / "for-general-contractors.html").read_text(
            encoding="utf-8"
        )
        self.assertRegex(
            source,
            r"\.skip-link\{[^}]*position:fixed;[^}]*top:-100px;"
            r"[^}]*z-index:10000;",
        )
        self.assertIn(".skip-link:focus{top:0;", source)

    def test_service_worker_cache_version_releases_updated_shared_script(self):
        source = (REPO_ROOT / "sw.js").read_text(encoding="utf-8")
        self.assertIn("const CACHE = 'acg-v5-2026-08-11';", source)
        self.assertNotIn("const CACHE = 'acg-v1-2026-06-06';", source)

    def test_priority_pages_request_current_shared_script(self):
        for rel in ("capabilities.html", "gc.html"):
            with self.subTest(rel=rel):
                source = (REPO_ROOT / rel).read_text(encoding="utf-8")
                self.assertEqual(
                    1,
                    source.count('src="js/main.js?v=20260811d"'),
                )


if __name__ == "__main__":
    unittest.main(verbosity=2)
