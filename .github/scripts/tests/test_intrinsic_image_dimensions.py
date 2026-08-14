import unittest
from html.parser import HTMLParser
from pathlib import Path
from xml.etree import ElementTree


ROOT = Path(__file__).resolve().parents[3]
EXPECTED = {
    "atlanta-commercial-glazing.html": {
        "images/acg-coverage-map.svg": (900, 560),
    },
    "euro-wall-installer-national.html": {
        "images/acg-coverage-map.svg": (900, 560),
    },
    "index-proof.html": {
        "/images/hero/tower-360.jpg": (2000, 1116),
        "/images/projects/ocean-prime-ft-lauderdale/ocean-prime-ftl-twilight-exterior.jpg": (1600, 1197),
        "/images/projects/atlantic-fields-golf-house/hero-golden-hour.jpg": (1564, 1028),
        "/images/projects/gulfside-twelve/hero-twilight-beachfront.jpg": (1920, 1071),
    },
}
JPEG_START_OF_FRAME_MARKERS = {
    0xC0,
    0xC1,
    0xC2,
    0xC3,
    0xC5,
    0xC6,
    0xC7,
    0xC9,
    0xCA,
    0xCB,
    0xCD,
    0xCE,
    0xCF,
}
PROHIBITED_PUNCTUATION = {chr(0x2013), chr(0x2014)}


class ImageParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.images = []

    def handle_starttag(self, tag, attrs):
        if tag.lower() != "img":
            return
        image = {name.lower(): value for name, value in attrs}
        source = image.get("src") or ""
        dynamic = not source or any(token in source for token in ("{{", "${", '\"+', "'+"))
        if not dynamic:
            self.images.append(image)

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)


def parsed_images(path: Path) -> list[dict[str, str]]:
    parser = ImageParser()
    parser.feed(path.read_text(encoding="utf-8", errors="ignore"))
    parser.close()
    return parser.images


def jpeg_dimensions(path: Path) -> tuple[int, int]:
    with path.open("rb") as image:
        if image.read(2) != b"\xff\xd8":
            raise ValueError(f"not a JPEG: {path}")
        while True:
            marker_start = image.read(1)
            if not marker_start:
                raise ValueError(f"JPEG dimensions not found: {path}")
            if marker_start != b"\xff":
                continue
            marker = image.read(1)
            while marker == b"\xff":
                marker = image.read(1)
            marker_value = marker[0]
            if marker_value in (0xD8, 0xD9):
                continue
            segment_length = int.from_bytes(image.read(2), "big")
            if marker_value in JPEG_START_OF_FRAME_MARKERS:
                image.read(1)
                height = int.from_bytes(image.read(2), "big")
                width = int.from_bytes(image.read(2), "big")
                return width, height
            image.seek(segment_length - 2, 1)


def asset_dimensions(path: Path) -> tuple[int, int]:
    if path.suffix.lower() == ".svg":
        root = ElementTree.parse(path).getroot()
        view_box = root.attrib["viewBox"].split()
        return int(float(view_box[2])), int(float(view_box[3]))
    return jpeg_dimensions(path)


class IntrinsicImageDimensionTests(unittest.TestCase):
    def test_every_static_image_has_intrinsic_dimensions(self):
        missing = []
        for path in ROOT.rglob("*.html"):
            relative = path.relative_to(ROOT).as_posix()
            for image in parsed_images(path):
                if "width" not in image or "height" not in image:
                    missing.append((relative, image.get("src")))
        self.assertEqual([], missing)

    def test_added_dimensions_match_source_assets(self):
        for relative, expected_images in EXPECTED.items():
            images = parsed_images(ROOT / relative)
            by_source = {image["src"]: image for image in images}
            for source, expected_dimensions in expected_images.items():
                with self.subTest(page=relative, source=source):
                    image = by_source[source]
                    html_dimensions = (int(image["width"]), int(image["height"]))
                    asset_path = ROOT / source.lstrip("/")
                    self.assertEqual(expected_dimensions, html_dimensions)
                    self.assertEqual(expected_dimensions, asset_dimensions(asset_path))

    def test_touched_alt_text_uses_permitted_punctuation(self):
        for relative, expected_images in EXPECTED.items():
            images = parsed_images(ROOT / relative)
            by_source = {image["src"]: image for image in images}
            for source in expected_images:
                with self.subTest(page=relative, source=source):
                    alt_text = by_source[source].get("alt", "")
                    self.assertTrue(PROHIBITED_PUNCTUATION.isdisjoint(alt_text))


if __name__ == "__main__":
    unittest.main()
