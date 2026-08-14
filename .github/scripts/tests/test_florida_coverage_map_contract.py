import re
import unittest
from html.parser import HTMLParser
from pathlib import Path
from xml.etree import ElementTree


ROOT = Path(__file__).resolve().parents[3]
MAP_PATH = ROOT / "images" / "acg-coverage-map.svg"
CACHE_VERSION = "20260814-florida"
EXPECTED_REFERENCE_COUNTS = {
    "atlanta-commercial-glazing.html": 3,
    "buildingconnected-basisboard-glazing.html": 2,
    "euro-wall-installer-national.html": 3,
    "glazed-aluminum-curtain-wall-contractor.html": 2,
    "glazing-subcontractor-vs-general-contractor.html": 2,
    "industries.html": 2,
    "press.html": 1,
    "procore-integrated-glazing-subcontractor.html": 2,
    "projects/index.html": 2,
    "tgp-fire-rated-glass-installer.html": 2,
}
FORBIDDEN_COVERAGE_LABEL = re.compile(
    r"\b(?:Tennessee|Nashville|Southeast|Tier|GA|AL|SC|NC|MS)\b|Q3\s+2026",
    re.IGNORECASE,
)
PROHIBITED_PUNCTUATION = {chr(0x2013), chr(0x2014)}
RELATIVE_MAP_REFERENCE = f"images/acg-coverage-map.svg?v={CACHE_VERSION}"
ABSOLUTE_MAP_REFERENCE = (
    f"https://acglass.com/images/acg-coverage-map.svg?v={CACHE_VERSION}"
)
EXPECTED_ROOT_STYLE = (
    "max-width:100%;height:auto;display:block;"
    "font-family:'Inter',-apple-system,BlinkMacSystemFont,sans-serif;"
)
BLOCKED_TEXT_RENDER_ATTRIBUTES = {
    "opacity",
    "fill-opacity",
    "filter",
    "mask",
    "mix-blend-mode",
    "style",
}
EXPECTED_TEXT_FILLS = {
    "AMERICAN COMMERCIAL GLASS": "rgba(255,255,255,0.5)",
    "Florida Coverage": "#fff",
    "WEST PALM BEACH | NAPLES | TAMPA": "rgba(255,255,255,0.62)",
    "FLORIDA OPERATIONS": "rgba(255,255,255,0.5)",
    "350+": "#fff",
    "Commercial projects": "rgba(255,255,255,0.82)",
    "1M+ SF": "#fff",
    "Glazing installed": "rgba(255,255,255,0.82)",
    "3": "#fff",
    "Current Florida offices": "rgba(255,255,255,0.82)",
    "FLORIDA FOOTPRINT": "rgba(255,255,255,0.5)",
    "TAMPA": "#fff",
    "NAPLES": "#fff",
    "WEST PALM BEACH": "#fff",
    "HEADQUARTERS": "rgba(255,255,255,0.62)",
    "COMMERCIAL GLAZING | DIVISION 08 | FLORIDA": "rgba(255,255,255,0.5)",
    "acglass.com": "rgba(255,255,255,0.5)",
}
MAP_LABELS_ON_RED = {"TAMPA", "NAPLES", "WEST PALM BEACH", "HEADQUARTERS"}
EXPECTED_GRADIENT_STOPS = {
    "background": (
        ("0%", "#0B1424", "1"),
        ("100%", "#050A12", "1"),
    ),
    "floridaFill": (
        ("0%", "#E11320", "0.48"),
        ("100%", "#9F0C17", "0.22"),
    ),
}


class CoverageMapReferenceParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.references = []

    def handle_starttag(self, tag, attrs):
        for name, value in attrs:
            if value and "acg-coverage-map.svg" in value:
                self.references.append((tag.lower(), name.lower(), value))


def is_exact_map_reference(tag: str, attribute: str, value: str) -> bool:
    return (tag, attribute, value) in {
        ("img", "src", RELATIVE_MAP_REFERENCE),
        ("meta", "content", ABSOLUTE_MAP_REFERENCE),
    }


def text_fill_contract_violations(root) -> list[str]:
    inventory = {}
    violations = []
    parent_by_child = {
        child: parent
        for parent in root.iter()
        for child in parent
    }
    if root.attrib.get("style") != EXPECTED_ROOT_STYLE:
        violations.append("root style changed")
    if root.find(".//{http://www.w3.org/2000/svg}style") is not None:
        violations.append("embedded stylesheet added")
    for text in root.iter("{http://www.w3.org/2000/svg}text"):
        label = "".join(text.itertext()).strip()
        if label in inventory:
            violations.append(f"duplicate text label: {label}")
        inventory[label] = text.attrib.get("fill")
        if list(text):
            violations.append(f"{label} uses child text markup")
        current = text
        while current is not None:
            blocked_attributes = BLOCKED_TEXT_RENDER_ATTRIBUTES
            if current is root:
                blocked_attributes = blocked_attributes - {"style"}
            for attribute in blocked_attributes:
                if attribute in current.attrib:
                    violations.append(f"{label} uses rendering override {attribute}")
            current = parent_by_child.get(current)
    if inventory != EXPECTED_TEXT_FILLS:
        violations.append("text label or fill inventory changed")
    return violations


def rgb_from_hex(value: str) -> tuple[float, float, float]:
    value = value.lstrip("#")
    if len(value) == 3:
        value = "".join(character * 2 for character in value)
    return tuple(int(value[index:index + 2], 16) for index in (0, 2, 4))


def composite(foreground, alpha: float, background):
    return tuple(
        foreground[index] * alpha + background[index] * (1 - alpha)
        for index in range(3)
    )


def relative_luminance(color) -> float:
    channels = []
    for value in color:
        normalized = value / 255
        channels.append(
            normalized / 12.92
            if normalized <= 0.04045
            else ((normalized + 0.055) / 1.055) ** 2.4
        )
    return 0.2126 * channels[0] + 0.7152 * channels[1] + 0.0722 * channels[2]


def contrast_ratio(first, second) -> float:
    first_luminance = relative_luminance(first)
    second_luminance = relative_luminance(second)
    return (max(first_luminance, second_luminance) + 0.05) / (
        min(first_luminance, second_luminance) + 0.05
    )


def rendered_fill(fill: str, background):
    if fill == "#fff":
        return (255, 255, 255)
    match = re.fullmatch(r"rgba\(255,255,255,([0-9.]+)\)", fill)
    if not match:
        raise ValueError(f"unsupported text fill: {fill}")
    return composite((255, 255, 255), float(match.group(1)), background)


class FloridaCoverageMapContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = MAP_PATH.read_text(encoding="utf-8")
        cls.root = ElementTree.fromstring(cls.source)
        cls.text = " ".join(part.strip() for part in cls.root.itertext() if part.strip())

    def test_asset_is_well_formed_and_keeps_exact_geometry(self):
        self.assertEqual("0 0 900 560", self.root.attrib["viewBox"])
        self.assertEqual("img", self.root.attrib["role"])
        self.assertEqual(EXPECTED_ROOT_STYLE, self.root.attrib["style"])

    def test_audited_gradient_surfaces_remain_exact(self):
        for gradient_id, expected in EXPECTED_GRADIENT_STOPS.items():
            gradient = self.root.find(f".//*[@id='{gradient_id}']")
            self.assertIsNotNone(gradient, gradient_id)
            actual = tuple(
                (
                    stop.attrib["offset"],
                    stop.attrib["stop-color"],
                    stop.attrib.get("stop-opacity", "1"),
                )
                for stop in gradient
            )
            self.assertEqual(expected, actual, gradient_id)

    def test_asset_contains_only_current_florida_coverage_labels(self):
        self.assertIsNone(FORBIDDEN_COVERAGE_LABEL.search(self.text))
        for required in (
            "ACG Florida coverage map",
            "WEST PALM BEACH | NAPLES | TAMPA",
            "350+",
            "1M+ SF",
            "Current Florida offices",
            "HEADQUARTERS",
        ):
            with self.subTest(required=required):
                self.assertIn(required, self.text)

    def test_asset_contains_no_prohibited_punctuation(self):
        self.assertTrue(PROHIBITED_PUNCTUATION.isdisjoint(self.source))

    def test_text_fill_inventory_is_exact(self):
        self.assertEqual([], text_fill_contract_violations(self.root))

    def test_text_fill_contract_rejects_alternate_low_contrast_syntax(self):
        for invalid_fill in ("rgba(255, 255, 255,0.10)", "#222222"):
            altered = ElementTree.fromstring(self.source)
            target = next(
                text
                for text in altered.iter("{http://www.w3.org/2000/svg}text")
                if "".join(text.itertext()).strip() == "acglass.com"
            )
            target.set("fill", invalid_fill)
            with self.subTest(fill=invalid_fill):
                self.assertNotEqual([], text_fill_contract_violations(altered))

    def test_text_fill_contract_rejects_opacity_and_child_overrides(self):
        altered_opacity = ElementTree.fromstring(self.source)
        opacity_target = next(
            text
            for text in altered_opacity.iter("{http://www.w3.org/2000/svg}text")
            if "".join(text.itertext()).strip() == "acglass.com"
        )
        opacity_target.set("opacity", "0.1")
        self.assertNotEqual(
            [],
            text_fill_contract_violations(altered_opacity),
        )

        altered_child = ElementTree.fromstring(self.source)
        child_target = next(
            text
            for text in altered_child.iter("{http://www.w3.org/2000/svg}text")
            if "".join(text.itertext()).strip() == "acglass.com"
        )
        child_target.text = None
        child = ElementTree.SubElement(
            child_target,
            "{http://www.w3.org/2000/svg}tspan",
            {"style": "fill:#222222"},
        )
        child.text = "acglass.com"
        self.assertNotEqual(
            [],
            text_fill_contract_violations(altered_child),
        )

    def test_every_text_label_meets_wcag_normal_text_contrast(self):
        lightest_background = rgb_from_hex("#0B1424")
        strongest_red_surface = composite(
            rgb_from_hex("#E11320"),
            0.48,
            lightest_background,
        )
        for label, fill in EXPECTED_TEXT_FILLS.items():
            background = (
                strongest_red_surface
                if label in MAP_LABELS_ON_RED
                else lightest_background
            )
            ratio = contrast_ratio(rendered_fill(fill, background), background)
            with self.subTest(label=label, ratio=ratio):
                self.assertGreaterEqual(ratio, 4.5)

    def test_reference_cohort_and_cache_key_are_exact(self):
        references = {}
        for path in ROOT.rglob("*.html"):
            source = path.read_text(encoding="utf-8", errors="ignore")
            raw_count = source.count("acg-coverage-map.svg")
            if not raw_count:
                continue
            relative = path.relative_to(ROOT).as_posix()
            parser = CoverageMapReferenceParser()
            parser.feed(source)
            parser.close()
            self.assertEqual(raw_count, len(parser.references), relative)
            references[relative] = len(parser.references)
            for tag, attribute, value in parser.references:
                with self.subTest(page=relative, tag=tag, attribute=attribute):
                    self.assertTrue(
                        is_exact_map_reference(tag, attribute, value),
                        value,
                    )
        self.assertEqual(EXPECTED_REFERENCE_COUNTS, references)

    def test_reference_validator_rejects_non_exact_variants(self):
        exact = (
            ("img", "src", RELATIVE_MAP_REFERENCE),
            ("meta", "content", ABSOLUTE_MAP_REFERENCE),
        )
        invalid = (
            ("img", "src", f"images/prefix-{RELATIVE_MAP_REFERENCE}"),
            ("img", "src", f"{RELATIVE_MAP_REFERENCE}-stale"),
            ("img", "src", f"{RELATIVE_MAP_REFERENCE}&stale=1"),
            (
                "meta",
                "content",
                f"https://example.com/images/acg-coverage-map.svg?v={CACHE_VERSION}",
            ),
            ("img", "src", f"{RELATIVE_MAP_REFERENCE}#stale"),
            (
                "meta",
                "content",
                f"https:images/acg-coverage-map.svg?v={CACHE_VERSION}",
            ),
            (
                "meta",
                "content",
                f"https:///images/acg-coverage-map.svg?v={CACHE_VERSION}",
            ),
            (
                "meta",
                "content",
                f"////images/acg-coverage-map.svg?v={CACHE_VERSION}",
            ),
            ("img", "content", RELATIVE_MAP_REFERENCE),
            ("meta", "src", ABSOLUTE_MAP_REFERENCE),
        )
        for tag, attribute, value in exact:
            with self.subTest(exact=value):
                self.assertTrue(is_exact_map_reference(tag, attribute, value))
        for tag, attribute, value in invalid:
            with self.subTest(invalid=value):
                self.assertFalse(is_exact_map_reference(tag, attribute, value))


if __name__ == "__main__":
    unittest.main()
