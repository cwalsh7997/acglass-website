"""IndexNow submission: only changed, sitemap-listed pages are pinged."""
from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
SCRIPT = REPO_ROOT / ".github" / "scripts" / "indexnow-ping.py"


def load():
    spec = importlib.util.spec_from_file_location("indexnow_ping", SCRIPT)
    assert spec and spec.loader, SCRIPT
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class PathToUrlTests(unittest.TestCase):
    def setUp(self):
        self.m = load()

    def test_root_index_maps_to_site_root(self):
        self.assertEqual(self.m.path_to_url("index.html"), "https://acglass.com/")

    def test_directory_index_maps_to_trailing_slash(self):
        self.assertEqual(
            self.m.path_to_url("storefront-glazier-west-palm-beach-florida/index.html"),
            "https://acglass.com/storefront-glazier-west-palm-beach-florida/",
        )

    def test_plain_html_file_keeps_its_name(self):
        self.assertEqual(self.m.path_to_url("bid.html"), "https://acglass.com/bid.html")

    def test_non_html_and_internal_paths_are_ignored(self):
        for path in ("robots.txt", "css/acg-proof.css", "_internal/notes.html", ".github/x.html"):
            with self.subTest(path=path):
                self.assertIsNone(self.m.path_to_url(path))


class SelectionTests(unittest.TestCase):
    def setUp(self):
        self.m = load()

    def test_only_sitemap_urls_are_submitted(self):
        listed = {"https://acglass.com/", "https://acglass.com/bid.html"}
        changed = ["index.html", "bid.html", "nashville.html", "robots.txt"]
        self.assertEqual(
            self.m.select_urls(changed, listed),
            ["https://acglass.com/", "https://acglass.com/bid.html"],
        )

    def test_selection_is_deduplicated_and_capped(self):
        listed = {f"https://acglass.com/p{i}.html" for i in range(12)}
        changed = [f"p{i}.html" for i in range(12)] + ["p0.html"]
        self.assertEqual(len(self.m.select_urls(changed, listed, cap=10)), 10)

    def test_sitemap_parser_reads_every_urlset(self):
        listed = self.m.sitemap_urls(REPO_ROOT)
        self.assertIn("https://acglass.com/", listed)
        self.assertIn("https://acglass.com/bid.html", listed)
        self.assertNotIn("https://acglass.com/nashville.html", listed)


class PayloadTests(unittest.TestCase):
    def test_payload_uses_the_published_key_file(self):
        m = load()
        key = (REPO_ROOT / ".indexnow-key").read_text().strip()
        payload = m.build_payload(["https://acglass.com/"], key)
        self.assertEqual(payload["host"], "acglass.com")
        self.assertEqual(payload["key"], key)
        self.assertEqual(payload["keyLocation"], f"https://acglass.com/{key}.txt")
        self.assertTrue((REPO_ROOT / f"{key}.txt").read_text().strip() == key)


if __name__ == "__main__":
    unittest.main()
