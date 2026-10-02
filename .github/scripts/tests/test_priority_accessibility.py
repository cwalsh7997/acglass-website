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
# Rebaselined 2026-09-09 (second pass). The CTA label was unified sitewide:
# "Send Us Plans for Bid" became "Send Us Plans" on these two pages, which moves
# hrefs and visible. 1,435 pages already used the short label.
#
# Rebaselined 2026-09-09. Four digests moved for two deliberate reasons:
#   head     impact-windows-doors.html and multi-slide-bifold-doors.html had a
#            twitter:title copied from another page. impact-windows-doors.html
#            was advertising itself to social as "Reviews | ACG Commercial
#            Glazing Contractor". Corrected to match each page's own title.
#   hrefs    privacy-policy.html and terms-of-use.html gained the Security link
#   visible  added beside Privacy and Terms in the sitewide footer.
# The contract is unchanged: these pages are landmark-only and may not drift
# without someone noticing. This drift was intended.
# Rebaselined 2026-09-09 (third pass). Only "hrefs" moved, on these two pages
# only, and only because the footer LinkedIn link was normalised from
# /company/american-commercial-glass-inc (a 301) to /company/acglass (the 200).
# The site carried three LinkedIn company URLs, one of them a 404, which split
# the entity. head, jsonld, scripts and visible are byte-identical, which is the
# evidence that nothing but the href changed.
# 2026-09-21: refresh only two href hashes for shipped commit 63d46e78e,
# which consolidated WPB/Tampa links onto existing storefront keeper URLs.
# Other fingerprints and all accessibility assertions remain unchanged.
# 2026-09-24: head/jsonld/scripts rebaselined after the reviews-template leak
# was removed from og:description, twitter:description, and BreadcrumbList.
# Visible text on impact-windows-doors.html already moved in the HVHZ county
# pass; this pin matches that body. hrefs are unchanged.
# 2026-09-28: multi-slide-bifold-doors.html "hrefs" only, for #225 (efce010a5).
# Its featured-case card now links the live Ocean Prime keeper
# /ocean-prime-ft-lauderdale.html instead of the noindex /projects/ alias.
# That single href is the whole diff; head, jsonld, scripts and visible are
# unchanged, which is the evidence nothing else moved.
# 2026-10-01: head/scripts/hrefs/visible rebaselined for the sitewide architectural chrome
# (new header, menu and footer; css/acg-arch-chrome.css + js/acg-arch-chrome.js). Verified
# byte-identical outside the replaced header/footer and the two include tags; jsonld unchanged.
LANDMARK_ONLY_FINGERPRINTS = {
    "impact-windows-doors.html": {
        # head rebaselined 2026-10-01 (interior redesign): legacy stylesheet links and <style>
        # blocks swapped for acg-arch-interior.css; head is otherwise identical (verified by
        # stripping stylesheet links/style blocks from both versions). Other digests unchanged.
        "head": "6a16c03150ddda8dd7bc25b200307e91aae002779666b08b5d54dbce28ad6aeb",
        "jsonld": "f852722b02bf696556895ae499798e363d3a201035863e44aed0117b0403f452",
        "scripts": "fc9ef4decb6b725a2f461e1f3a5b5f946fbaadf76a6bea893b7fb2ac349f163e",
        # Rebaselined 2026-09-03 after batch-2 RFQ primary moved to /send-plans.html.
        "hrefs": "59eda6361e56ff67fe9e64307b6f2a9bad14ca86eae81c9236991aeff2277d77",
        "visible": "2575af7743b2962083b941c0412e7f6f7dd53bf1580644db8f3594538deb24cc",
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
        # head rebaselined 2026-10-01 (interior redesign): legacy stylesheet links and <style>
        # blocks swapped for acg-arch-interior.css; head is otherwise identical (verified by
        # stripping stylesheet links/style blocks from both versions). Other digests unchanged.
        "head": "82fb705bb4008064360ef254b1cb61a78c7c877f31129e158046c1189329345e",
        "jsonld": "ad79a685eece44118a1212057a51bb2d3ac0224561f209e3672e234bccb7e2a7",
        "scripts": "1d173b7b332767edd8ed61825f17db02bfec58a7dc000632797dad5ac643f0ab",
        # Rebaselined 2026-09-03 after batch-2 RFQ primary moved to /send-plans.html.
        # Visible digest updated 2026-09-03 when the Ocean Prime featured card
        # was pulled back to one Euro-Wall door/opening.
        "hrefs": "0493d4bf8b11f3bc2fb4d0720d4e37865f507e24f0f1a85548d9486f0e1ac9b2",
        "visible": "baa3a9362b0eb147b3354dc7e87746a2cc68461646200f108d6898d77975775f",
    },
    "privacy-policy.html": {
        # head rebaselined 2026-10-01 (interior redesign): legacy stylesheet links and <style>
        # blocks swapped for acg-arch-interior.css; head is otherwise identical (verified by
        # stripping stylesheet links/style blocks from both versions). Other digests unchanged.
        "head": "e3f9d7163f231370a282a755436e1b5ffe59bee8fd43d248935197e679c017a3",
        "jsonld": "cf57f2ef73c50d9fdb040a2ff489b1a7e1eaab9bd91e44b065ad2661507ff42d",
        "scripts": "79b1d73c8555bd00767c5c2e54ebf96f99371a3e6ca68a9f9f7b080588793e54",
        "hrefs": "0da163b04a4aedddf14188550823e26ee564ef76f5c8e03de0ed8993db365881",
        "visible": "7b1503c488c37344fbf6c7935e9040a5c6653823edebbd944c27c8354b0f20f7",
    },
    "terms-of-use.html": {
        # head rebaselined 2026-10-01 (interior redesign): legacy stylesheet links and <style>
        # blocks swapped for acg-arch-interior.css; head is otherwise identical (verified by
        # stripping stylesheet links/style blocks from both versions). Other digests unchanged.
        "head": "93b5a737481c26a194b25990e2be7334aca7366e9dcec45d1097fc445f7bd8df",
        "jsonld": "e0dda3641a0aacd968c4d7fc5fccdf294bd27c72e1d4d04fe9e4f9ba02f5e6d1",
        "scripts": "a0fb3425f2b1c3179c113d7f603129f2c68a0768a5423700cfd33bbc1ad015d6",
        "hrefs": "0da163b04a4aedddf14188550823e26ee564ef76f5c8e03de0ed8993db365881",
        "visible": "15784867daf1f60c1c1c44b8af284a7682d1c4fe940ef055c9a5621f2f8f8543",
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
        # 2026-10-01 interior redesign: the page's <style> block moved into the shared
        # acg-arch-interior.css, so the contract is checked on the page plus that sheet.
        self.assertIn('href="/css/acg-arch-interior.css?v=20261001"', source)
        source += (REPO_ROOT / "css" / "acg-arch-interior.css").read_text(encoding="utf-8")
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
