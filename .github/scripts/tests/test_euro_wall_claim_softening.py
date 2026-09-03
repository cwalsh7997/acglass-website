#!/usr/bin/env python3
"""Follow-up guards: no /products/eswindows/ hrefs; Euro-Wall cert language gone."""

from __future__ import annotations

import re
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[3]
SKIP_DIRS = {".git", ".github", "_internal", "node_modules", "dealer"}
# Original instruction: do not touch Nashville copy.
NASHVILLE_COPY_SKIP = {"storefront-installer-nashville.html"}
HREF_RE = re.compile(r"""<a\b[^>]*?\bhref\s*=\s*["']([^"']+)["']""", re.I)
FACTORY_CERT_RE = re.compile(r"factory[- ]certif(?:ied|ication)", re.I)
EURO_RE = re.compile(r"euro-?wall", re.I)


def iter_html() -> list[Path]:
    out = []
    for path in REPO_ROOT.rglob("*.html"):
        if SKIP_DIRS.intersection(path.relative_to(REPO_ROOT).parts):
            continue
        out.append(path)
    return out


class NoEsWindowsProductHrefTests(unittest.TestCase):
    def test_no_html_href_points_at_products_eswindows(self):
        bad = []
        for path in iter_html():
            html = path.read_text(encoding="utf-8")
            for raw in HREF_RE.findall(html):
                href = raw.split("#", 1)[0].split("?", 1)[0]
                if "products/eswindows" in href.lower():
                    bad.append(f"{path.relative_to(REPO_ROOT)} -> {raw}")
        self.assertEqual(bad, [])
        self.assertFalse((REPO_ROOT / "products/eswindows/index.html").exists())
        self.assertFalse((REPO_ROOT / "products/eswindows.html").exists())


class EuroWallCertSofteningTests(unittest.TestCase):
    def test_manufacturers_card_is_installer_specifier_not_factory_cert(self):
        html = (REPO_ROOT / "manufacturers.html").read_text(encoding="utf-8")
        self.assertNotIn("holds factory certification", html)
        self.assertNotIn("Installer - factory certified", html)
        self.assertIn("Installer / specifier", html)
        self.assertIn("installs and specifies Euro-Wall", html)

    def test_live_pages_drop_euro_wall_factory_cert_except_nashville_copy(self):
        leftovers = []
        for path in iter_html():
            rel = str(path.relative_to(REPO_ROOT))
            if rel in NASHVILLE_COPY_SKIP:
                continue
            text = path.read_text(encoding="utf-8")
            if not EURO_RE.search(text):
                continue
            if FACTORY_CERT_RE.search(text):
                leftovers.append(rel)
        llms = (REPO_ROOT / "llms.txt").read_text(encoding="utf-8")
        if FACTORY_CERT_RE.search(llms) and EURO_RE.search(llms):
            leftovers.append("llms.txt")
        self.assertEqual(leftovers, [])
        facts = (REPO_ROOT / "facts.html").read_text(encoding="utf-8")
        self.assertIn("Installer and specifier language only.", facts)
        products = (REPO_ROOT / "products/index.html").read_text(encoding="utf-8")
        self.assertIn("Installer / specifier.", products)


if __name__ == "__main__":
    unittest.main(verbosity=2)
