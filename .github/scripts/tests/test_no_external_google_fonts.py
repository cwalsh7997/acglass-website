#!/usr/bin/env python3
"""Local-font delivery and protected-page checks."""

from __future__ import annotations

import hashlib
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
PAGE = ROOT / "projects" / "ocean-prime-ft-lauderdale.html"
FONT = ROOT / "fonts" / "inter-variable-latin.woff2"

PROTECTED_HASHES = {
    "anchors": "555ddaef659d5c7e6a3727696117aed782500731bbf530e36e32dd81a53e1dd5",
    "body": "3a8e91eb130f2882cb97b51958b192b052e4b267c7e6be166b2574aa039c856d",
    "forms": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
    "images": "7b9e50a4aa712fc774f975ac315135fe1ec1b90344faf8f8df685c82ef38e95b",
    "jsonld": "d6078e92ff30d6acee2bf9656a6d145ee432c17149931707c3f752aa037e74a0",
    "metadata": "8e8ce0ff76fb12b7b21ad2e349a8df43ac98cab962cb8a621d661bd42a3ff02a",
    "scripts": "59d80dfe70fb34b631f5af37c031aa15a9fb62d74c3f0c7f7ba40f348fd81567",
}


def _sha256(value: str) -> str:
    return hashlib.sha256(value.encode()).hexdigest()


def _protected_fragments(source: str) -> dict[str, str]:
    head_match = re.search(r"<head\b[^>]*>(.*?)</head>", source, re.I | re.S)
    body_match = re.search(r"<body\b[^>]*>.*?</body>", source, re.I | re.S)
    if head_match is None or body_match is None:
        raise AssertionError("Ocean Prime document structure is incomplete")
    head = head_match.group(1)
    metadata = "\n".join(
        re.findall(
            r'<title\b[^>]*>.*?</title>|<meta\b[^>]*>|'
            r'<link\b[^>]*rel=["\'](?:canonical|icon)["\'][^>]*>',
            head,
            re.I | re.S,
        )
    )
    return {
        "anchors": "\n".join(
            re.findall(r'<a\b[^>]*\bhref=["\']([^"\']*)', source, re.I)
        ),
        "body": body_match.group(0),
        "forms": "\n".join(
            re.findall(r"<form\b[^>]*>.*?</form>", source, re.I | re.S)
        ),
        "images": "\n".join(re.findall(r"<img\b[^>]*>", source, re.I | re.S)),
        "jsonld": "\n".join(
            re.findall(
                r'<script\b[^>]*type=["\']application/ld\+json["\'][^>]*>'
                r".*?</script>",
                source,
                re.I | re.S,
            )
        ),
        "metadata": metadata,
        "scripts": "\n".join(
            re.findall(
                r'<script\b(?![^>]*type=["\']application/ld\+json)[^>]*>'
                r".*?</script>",
                source,
                re.I | re.S,
            )
        ),
    }


class NoExternalGoogleFontsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.source = PAGE.read_text(encoding="utf-8")

    def test_deployed_html_has_no_google_font_hosts(self):
        offenders = []
        for page in ROOT.rglob("*.html"):
            source = page.read_text(encoding="utf-8", errors="ignore")
            if "fonts.googleapis.com" in source or "fonts.gstatic.com" in source:
                offenders.append(str(page.relative_to(ROOT)))
        self.assertEqual([], offenders)

    def test_local_inter_font_is_valid_and_pinned(self):
        data = FONT.read_bytes()
        self.assertEqual(b"wOF2", data[:4])
        self.assertEqual(48256, len(data))
        self.assertEqual(
            "3100e775e8616cd2611beecfa23a4263d7037586789b43f035236a2e6fbd4c62",
            hashlib.sha256(data).hexdigest(),
        )

    def test_ocean_prime_preloads_and_declares_local_inter_once(self):
        preload = (
            '<link rel="preload" href="/fonts/inter-variable-latin.woff2" '
            'as="font" type="font/woff2" crossorigin>'
        )
        font_face = (
            "@font-face{font-family:'Inter';"
            "src:url('/fonts/inter-variable-latin.woff2') format('woff2');"
            "font-style:normal;font-weight:100 900;font-display:swap;}"
        )
        self.assertEqual(1, self.source.count(preload))
        self.assertEqual(1, self.source.count(font_face))

    def test_page_content_and_behavior_contracts_are_unchanged(self):
        fragments = _protected_fragments(self.source)
        self.assertEqual(set(PROTECTED_HASHES), set(fragments))
        for name, expected in PROTECTED_HASHES.items():
            with self.subTest(fragment=name):
                self.assertEqual(expected, _sha256(fragments[name]))


if __name__ == "__main__":
    unittest.main(verbosity=2)
