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
    # Rebaselined 2026-09-03: Ocean Prime scope pulled back to one Euro-Wall
    # opening at 171 Las Olas Circle. Anchors and scripts unchanged.
    "body": "9d726b7f0205a1014bdd68f326382293744d8ab4a4c5d6e3dff08ac5cb42852b",
    "forms": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
    "images": "f293b0d3972fa909d8f9a1216132ebcf89a99f46d4961977d74dc90801f19d51",
    "jsonld": "d3051ce529b38fb0ab09fe6121b9c6a1c95e6fe3017decd2bfd185cb2c907426",
    "metadata": "0122da70a793d448c278c1cf00e099d8e4ca22279fa05e9eefe296188e15fb53",
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
