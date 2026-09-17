#!/usr/bin/env python3
"""Follow-up guards: no /products/eswindows/ hrefs; Euro-Wall cert language gone."""

from __future__ import annotations

import json
import re
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[3]
SKIP_DIRS = {".git", ".github", "_internal", "node_modules", "dealer"}
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
        stub = REPO_ROOT / "products/eswindows/index.html"
        self.assertTrue(stub.is_file())
        stub_html = stub.read_text(encoding="utf-8")
        self.assertIn('href="https://acglass.com/es-windows.html"', stub_html)
        self.assertIn('content="noindex,follow"', stub_html)
        self.assertIn('http-equiv="refresh"', stub_html)
        self.assertFalse((REPO_ROOT / "products/eswindows.html").exists())

    def test_products_index_links_eswindows_hub_not_process_excuse(self):
        html = (REPO_ROOT / "products/index.html").read_text(encoding="utf-8")
        self.assertIn('href="/es-windows.html"', html)
        self.assertIn('href="/eswindows-installer-florida.html"', html)
        self.assertNotIn("was not created in this pass", html)
        self.assertNotIn("Cloudflare security challenge", html)
        self.assertNotIn("<code>/products/eswindows/</code>", html)

    def test_vercel_json_mirrors_both_eswindows_product_path_rules(self):
        rules = json.loads((REPO_ROOT / "vercel.json").read_text(encoding="utf-8")).get(
            "redirects", []
        )
        pair = {
            (r.get("source"), r.get("destination"), r.get("permanent"))
            for r in rules
            if r.get("source") in {"/products/eswindows", "/products/eswindows/"}
        }
        self.assertEqual(
            pair,
            {
                ("/products/eswindows", "/es-windows.html", True),
                ("/products/eswindows/", "/es-windows.html", True),
            },
        )

    def test_eswindows_products_path_apply_note_is_not_activated(self):
        note = json.loads(
            (REPO_ROOT / ".github/cloudflare/eswindows-products-path.json").read_text(
                encoding="utf-8"
            )
        )
        self.assertIs(note.get("activated"), False)
        self.assertEqual(note.get("id"), "eswindows-products-path")
        sources = {r.get("source") for r in note.get("rules", [])}
        dests = {r.get("destination") for r in note.get("rules", [])}
        self.assertEqual(
            sources,
            {
                "https://acglass.com/products/eswindows",
                "https://acglass.com/products/eswindows/",
            },
        )
        self.assertEqual(dests, {"https://acglass.com/es-windows.html"})
        md = (REPO_ROOT / ".github/cloudflare/eswindows-products-path.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("NOT ACTIVATED", md)
        self.assertIn("preserve query string", md.lower())


class EuroWallCertSofteningTests(unittest.TestCase):
    def test_manufacturers_card_is_installer_specifier_not_factory_cert(self):
        html = (REPO_ROOT / "manufacturers.html").read_text(encoding="utf-8")
        self.assertNotIn("holds factory certification", html)
        self.assertNotIn("Installer - factory certified", html)
        self.assertIn("Installer / specifier", html)
        self.assertIn("installs and specifies Euro-Wall", html)

    def test_live_pages_drop_euro_wall_factory_cert_claims(self):
        leftovers = []
        for path in iter_html():
            rel = str(path.relative_to(REPO_ROOT))
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
        self.assertIn("Installer and specifier: two. Installed: seven.", facts)
        self.assertNotIn("Authorized: two. Installed: seven.", facts)
        products = (REPO_ROOT / "products/index.html").read_text(encoding="utf-8")
        self.assertIn("Installer / specifier.", products)
        nashville = (REPO_ROOT / "storefront-installer-nashville.html").read_text(
            encoding="utf-8"
        )
        self.assertIn("an installer and specifier rather than a one-time special order", nashville)
        self.assertNotIn("factory-certified installer", nashville)
        self.assertNotIn("office opening", nashville.lower())


if __name__ == "__main__":
    unittest.main(verbosity=2)
