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
        "head": "7f9d07ce7ab230d9d2fc0471f49e88819227b255df70092bcb815e8aba702831",
        "jsonld": "13bcb19f4382060a48bf2c75bec106ef1267e44427b51ee0d41057138be11600",
        "scripts": "701d93f0e5535e23d301a89f9745fc2ca9916bd5bec164bf0db0d28264b320c2",
        # Rebaselined 2026-09-03 after batch-2 RFQ primary moved to /send-plans.html.
        "hrefs": "98d0bbf6e368b3f8e301e67fc1da4ddcb672087727ddefad58498a82e3dcecab",
        "visible": "f8ed5be4194044d3d045b0bf51cb9192fc5d147f90e24e9105dcda77b0ecd0c7",
    },
    "multi-slide-bifold-doors.html": {
        # Rebaselined 2026-08-27 (second pass, first-party authorization sweep):
        # "Authorized Euro-Wall ..." removed from the Service JSON-LD
        # description in <head>, the "Authorized on the ..." H2 became
        # "Installed on the ...", and "installed by an authorized Florida
        # installer" became "installed by a Florida commercial installer".
        # head/jsonld/scripts move because the edited JSON-LD block lives in
        # <head>. hrefs/visible moved again 2026-09-03 when the RFQ primary
        # went to /send-plans.html.
        # Digests recomputed with this module's own _fingerprints() helper.
        "head": "b35b27924a0cd4e9ba6c4cbe29fad6fbad932770734290d0b8b8338a82625f07",
        "jsonld": "4afbd33f45d172e288866ca76b1c7378573aa821bcd033a5187ec2d0cf0352f6",
        "scripts": "99ef7cbb1dac5a40482698f99990ac2b56180e7a51b2c40102dd25060118b69e",
        # Rebaselined 2026-09-03 after batch-2 RFQ primary moved to /send-plans.html.
        # Visible digest updated 2026-09-03 when the Ocean Prime featured card
        # was pulled back to one Euro-Wall door/opening.
        "hrefs": "ef2fb6c07b6f693de3e51369c131d60ead08f494c4956c69e03e12dbed760050",
        "visible": "5946f0c8fa87ba1d2c355f1f58356e44fb1d853039147deca6de83942b92fc05",
    },
    "privacy-policy.html": {
        "head": "b259a593708ec0c5d1295afc309e3159c82da4a5f12597e4a0c2af3d346b48f5",
        "jsonld": "cf57f2ef73c50d9fdb040a2ff489b1a7e1eaab9bd91e44b065ad2661507ff42d",
        "scripts": "602b81cc175a16c0d7104e55d880b415e295f6aa24f13dbb41c6d89507861945",
        "hrefs": "90d3fd7f9ba02d99f8af0273c3353778bc090581896c722a90f714ec4cc08e4b",
        "visible": "0616a02edf9c35c49405839abcec88e30be41956ff910ae9b55b02242b5d7c22",
    },
    "terms-of-use.html": {
        "head": "353fb9c5f91945a215c3af07a55b360f37c776714c98143e29ae9da7f00a3c02",
        "jsonld": "e0dda3641a0aacd968c4d7fc5fccdf294bd27c72e1d4d04fe9e4f9ba02f5e6d1",
        "scripts": "31c1c638780ee6d016e87b4cc4d6d823c4a41abbfd14225a58d6f5504555f3f4",
        "hrefs": "90d3fd7f9ba02d99f8af0273c3353778bc090581896c722a90f714ec4cc08e4b",
        "visible": "42f09d5327726f4c31cd79455351f5c6fff42b938079617de4c7743681df005b",
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
        self.assertIn("const CACHE = 'acg-navigation-v1-2026-08-12';", source)
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
