import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
CSS_PATH = ROOT / "css" / "acg-chrome.css"
SCOPE_MARKER = 'data-acg-block="full-scope-v1"'
TEMPLATE_MARKER = ".wpb-section-eyebrow"
EXPECTED_SCOPE_PAGE_COUNT = 328
CACHE_VERSION = "20260814-contrast"
TEMPLATE_CACHE_VERSION = "20260814-template-contrast"
FROZEN_SCOPE_PATHS = {
    "commercial-glazier-near-me-west-palm-beach/index.html",
    "commercial-glazing-west-palm-beach.html",
    "eswindows-installer-west-palm-beach.html",
    "impact-windows-palm-beach.html",
    "storefront-glazier-west-palm-beach-florida/index.html",
    "storefront-installer-west-palm-beach.html",
    "west-palm-beach/index.html",
}
CHROME_LINK = re.compile(
    r'<link[^>]+href=["\'](?P<href>[^"\']*css/acg-chrome\.css(?:\?[^"\']*)?)["\']',
    re.IGNORECASE,
)


def relative_luminance(hex_color: str) -> float:
    channels = [int(hex_color[index:index + 2], 16) / 255 for index in (1, 3, 5)]
    linear = [
        value / 12.92 if value <= 0.04045 else ((value + 0.055) / 1.055) ** 2.4
        for value in channels
    ]
    return 0.2126 * linear[0] + 0.7152 * linear[1] + 0.0722 * linear[2]


def contrast_ratio(foreground: str, background: str) -> float:
    light, dark = sorted(
        (relative_luminance(foreground), relative_luminance(background)),
        reverse=True,
    )
    return (light + 0.05) / (dark + 0.05)


class SharedContrastContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.css = CSS_PATH.read_text(encoding="utf-8")

    def test_shared_scope_colors_meet_normal_text_contrast(self):
        self.assertGreaterEqual(contrast_ratio("#d8101e", "#f5f1ea"), 4.5)
        self.assertGreaterEqual(contrast_ratio("#626c7c", "#f5f1ea"), 4.5)

    def test_footer_wordmark_meets_large_text_contrast(self):
        navy = "#0e284f"
        white = "#ffffff"
        alpha = 0.35
        blended = "#" + "".join(
            f"{round(int(white[index:index + 2], 16) * alpha + int(navy[index:index + 2], 16) * (1 - alpha)):02x}"
            for index in (1, 3, 5)
        )
        self.assertGreaterEqual(contrast_ratio(blended, navy), 3.0)

    def test_shared_stylesheet_contains_exact_overrides(self):
        self.assertIn(
            '[data-acg-block="full-scope-v1"]>div>div:first-child{color:#d8101e!important}',
            self.css,
        )
        self.assertIn(
            '[data-acg-block="full-scope-v1"] li>span{color:#626c7c!important}',
            self.css,
        )
        self.assertIn(
            '.ft-word span{-webkit-text-stroke-color:rgba(255,255,255,.35)!important}',
            self.css,
        )

    def test_every_full_scope_page_loads_shared_chrome(self):
        pages = []
        missing = []
        frozen = []
        stale_cache_keys = []
        for path in ROOT.rglob("*.html"):
            source = path.read_text(encoding="utf-8", errors="ignore")
            if SCOPE_MARKER not in source:
                continue
            pages.append(path)
            relative = path.relative_to(ROOT).as_posix()
            match = CHROME_LINK.search(source)
            if not match:
                missing.append(relative)
                continue
            if relative in FROZEN_SCOPE_PATHS:
                frozen.append(relative)
                continue
            version = TEMPLATE_CACHE_VERSION if TEMPLATE_MARKER in source else CACHE_VERSION
            expected = f"/css/acg-chrome.css?v={version}"
            if match.group("href") != expected:
                stale_cache_keys.append((relative, match.group("href")))
        self.assertEqual(EXPECTED_SCOPE_PAGE_COUNT, len(pages))
        self.assertEqual(FROZEN_SCOPE_PATHS, set(frozen))
        self.assertEqual([], missing)
        self.assertEqual([], stale_cache_keys)


if __name__ == "__main__":
    unittest.main()
