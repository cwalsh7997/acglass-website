import re
import unittest
from html.parser import HTMLParser
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
CSS_PATH = ROOT / "css" / "acg-chrome.css"
DARK_SYSTEM_CSS_PATH = ROOT / "css" / "acg-dusk.css"
TEMPLATE_MARKER = ".wpb-section-eyebrow"
QUICK_ANSWER_MARKER = ".quick-answer-label"
EXPECTED_TEMPLATE_PAGE_COUNT = 79
CACHE_VERSION = "20260814-template-contrast"
FROZEN_TEMPLATE_PATHS = {
    "storefront-glazier-west-palm-beach-florida/index.html",
}
OUTSIDE_QUICK_ANSWER_PATHS = {
    "acg-glass-florida/index.html",
    "storefront-glazier-florida/index.html",
}
CHROME_LINK = re.compile(
    r'<link[^>]+href=["\'](?P<href>[^"\']*css/acg-chrome\.css(?:\?[^"\']*)?)["\']',
    re.IGNORECASE,
)
REQUIRED_TEMPLATE_MARKERS = (
    ".wpb-section-eyebrow",
    ".quick-answer-label",
    ".system-card-tagline",
    ".project-cat",
    ".costs-table td.price",
    ".author-title",
    ".wpb-section a",
)
EXPECTED_CSS_OVERRIDE = """.wpb-section-eyebrow,
.wpb-section .quick-answer-label,
.system-card-tagline,
.project-cat,
.costs-table td.price,
.author-title,
.wpb-section a{color:#f5303c!important}
.wpb-section a:hover{color:#fff!important}"""
DARK_BACKGROUNDS = (
    "#050a12",
    "#0a0f17",
    "#0b1018",
    "#10151c",
)


class ClassTokenParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.tokens = set()

    def handle_starttag(self, tag, attrs):
        del tag
        for name, value in attrs:
            if name.lower() == "class" and value:
                self.tokens.update(value.split())

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)


def html_class_tokens(source: str) -> set[str]:
    parser = ClassTokenParser()
    parser.feed(source)
    parser.close()
    return parser.tokens


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


class TemplateContrastContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.css = CSS_PATH.read_text(encoding="utf-8")
        cls.dark_system_css = DARK_SYSTEM_CSS_PATH.read_text(encoding="utf-8")

    def test_bright_red_matches_existing_dark_system_token(self):
        self.assertIn("--red-2:#F5303C", self.dark_system_css)

    def test_html_class_token_parser_detects_exact_scope_token(self):
        source = '<style>.wpb-section{display:block}</style><section class="x wpb-section y">'
        self.assertEqual({"x", "wpb-section", "y"}, html_class_tokens(source))

    def test_bright_red_meets_normal_text_contrast_on_template_backgrounds(self):
        for background in DARK_BACKGROUNDS:
            with self.subTest(background=background):
                self.assertGreaterEqual(contrast_ratio("#f5303c", background), 4.5)

    def test_shared_stylesheet_contains_exact_template_overrides(self):
        self.assertIn(EXPECTED_CSS_OVERRIDE, self.css)

    def test_template_cohort_and_cache_keys_are_exact(self):
        pages = []
        page_relatives = set()
        frozen = []
        missing_markers = []
        missing_chrome = []
        stale_cache_keys = []

        for path in ROOT.rglob("*.html"):
            source = path.read_text(encoding="utf-8", errors="ignore")
            if TEMPLATE_MARKER not in source:
                continue
            pages.append(path)
            relative = path.relative_to(ROOT).as_posix()
            page_relatives.add(relative)
            absent = [marker for marker in REQUIRED_TEMPLATE_MARKERS if marker not in source]
            if absent:
                missing_markers.append((relative, absent))
            match = CHROME_LINK.search(source)
            if not match:
                missing_chrome.append(relative)
                continue
            if relative in FROZEN_TEMPLATE_PATHS:
                frozen.append(relative)
                continue
            expected = f"/css/acg-chrome.css?v={CACHE_VERSION}"
            if match.group("href") != expected:
                stale_cache_keys.append((relative, match.group("href")))

        self.assertEqual(EXPECTED_TEMPLATE_PAGE_COUNT, len(pages))
        self.assertEqual(FROZEN_TEMPLATE_PATHS, set(frozen))
        self.assertEqual([], missing_markers)
        self.assertEqual([], missing_chrome)
        self.assertEqual([], stale_cache_keys)

        quick_answer_pages = {
            path.relative_to(ROOT).as_posix()
            for path in ROOT.rglob("*.html")
            if QUICK_ANSWER_MARKER in path.read_text(encoding="utf-8", errors="ignore")
        }
        self.assertEqual(
            OUTSIDE_QUICK_ANSWER_PATHS,
            quick_answer_pages - page_relatives,
        )
        for relative in OUTSIDE_QUICK_ANSWER_PATHS:
            source = (ROOT / relative).read_text(encoding="utf-8", errors="ignore")
            self.assertNotIn("wpb-section", html_class_tokens(source))


if __name__ == "__main__":
    unittest.main()
