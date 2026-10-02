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

# Rebaselined 2026-09-14: live JSON-LD url/breadcrumb now name the /projects/
# 200 (Cloudflare 301s the short URL to portfolio). Added Project @type,
# GC takeaway, and contextual Euro-Wall / FTL / restaurant / projects links.
# Images, forms, and non-JSON-LD scripts are unchanged.
# Metadata rebaselined 2026-09-23: robots is noindex,follow on this duplicate.
# Metadata rebaselined 2026-09-27: twitter:image mirrors the existing og:image.
# JSON-LD rebaselined 2026-09-28 for #225 (efce010a5), which merged a deliberate
# change the pin never picked up: the Article/Project @id, url, mainEntityOfPage
# and the breadcrumb item moved from this noindex /projects/ alias to the live
# keeper /ocean-prime-ft-lauderdale.html, the URL this page has rel=canonical'd
# to since #201 (957961430). Those four URL values are the only JSON-LD change.
# Every other fragment digest is byte-identical to the previous pin.
# 2026-10-01: anchors/body/images/scripts rebaselined for the sitewide architectural chrome;
# the page is byte-identical outside the replaced header/footer and the two include tags.
# 2026-10-01 (interior redesign): body/images rebaselined. The page moved onto
# acg-arch-interior.css; inline style attributes were dropped (img tags are identical
# with style attributes removed) and visible text, links, images, forms, JSON-LD and
# scripts were verified unchanged with an HTML5 parser. Anchors/forms/jsonld/metadata/
# scripts digests are unchanged. The @font-face moved from the page <style> block to
# the shared interior sheet.
PROTECTED_HASHES = {
    "anchors": "08cbc65e66beafb717e364479df4ac9dafb7938674d4bd5e20b57471b1ad6973",
    "body": "b9cdfebe56e5eb927d8617360e9ccea73b2d1b207419645f6aa2df6910c878de",
    "forms": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
    "images": "59ccfef5b2b2882acbcdc80aa4bbeb2a4d6c8f3309ce23d3ca6a02fb909baeba",
    "jsonld": "cf8be9f3f9f118b8ed4260510f3920e4c3a9f3c8c2dff3d7624bbfe7d9097170",
    "metadata": "f34f096e64ce1e4283154d8cdf34c46247be47df04ef5888ecd6f06cd83019ef",
    "scripts": "ffbda8d04e09ae363b47ab94d78dd00e21a72c74651cfedf2402c0d67e70e442",
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
        # Interior-theme pages declare Inter once, in the shared sheet they link.
        interior_link = '<link rel="stylesheet" href="/css/acg-arch-interior.css?v=20261001">'
        if interior_link in self.source:
            sheet = (ROOT / "css" / "acg-arch-interior.css").read_text(encoding="utf-8")
            self.assertEqual(0, self.source.count("@font-face"))
            self.assertEqual(1, sheet.count(
                "@font-face{font-family:Inter;src:url('/fonts/inter-variable-latin.woff2') "
                "format('woff2');font-weight:100 900;font-display:swap}"
            ))
        else:
            self.assertEqual(1, self.source.count(font_face))

    def test_page_content_and_behavior_contracts_are_unchanged(self):
        fragments = _protected_fragments(self.source)
        self.assertEqual(set(PROTECTED_HASHES), set(fragments))
        for name, expected in PROTECTED_HASHES.items():
            with self.subTest(fragment=name):
                self.assertEqual(expected, _sha256(fragments[name]))


if __name__ == "__main__":
    unittest.main(verbosity=2)
