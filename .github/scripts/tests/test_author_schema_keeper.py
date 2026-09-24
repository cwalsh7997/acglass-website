"""Author schema and site search must cite the indexable bio, not the stub."""

from __future__ import annotations

import json
import re
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[3]
SKIP_DIRS = {".git", ".github", "node_modules"}
KEEPER = "https://acglass.com/authors/connor-walsh.html"
RIELLY = "https://acglass.com/authors/rielly-walsh.html"
STUBS = (
    "author-connor-walsh.html",
    "author/connor-walsh.html",
    "author-rielly-walsh.html",
    "author/rielly-walsh.html",
)
FROZEN_TITLES = {
    "index.html": "Commercial Glazing Contractor Florida | ACG",
    "florida-commercial-glazing/index.html": (
        "Commercial Storefront Installer Florida | Bid in 48 Hrs"
    ),
    "storefront-glazier-west-palm-beach-florida/index.html": (
        "Commercial Storefront Installer, West Palm Beach | Bid"
    ),
    "storefront-glazier-naples-florida/index.html": (
        "Commercial Storefront Installer Naples | 48-Hr Bids"
    ),
    "storefront-glazier-tampa-florida/index.html": (
        "Commercial Storefront Installer Tampa | 48-Hr Bids"
    ),
}
# Pages that used to publish Person.url at a noindex refresh stub.
SAMPLE_PAGES = (
    "storefront-glazier-west-palm-beach-florida/index.html",
    "impact-windows-doors-florida.html",
    "blog/ocean-prime-ft-lauderdale-glazing.html",
    "acoustic-glazing-stc-oitc-commercial.html",
    "news/acg-tampa-office-expansion.html",
)
JSONLD = re.compile(
    r'<script\b[^>]*type=["\']application/ld\+json["\'][^>]*>(.*?)</script>',
    re.I | re.S,
)
TITLE = re.compile(r"<title[^>]*>(.*?)</title>", re.I | re.S)


def _iter_public():
    for path in REPO_ROOT.rglob("*"):
        if not path.is_file():
            continue
        if SKIP_DIRS.intersection(path.relative_to(REPO_ROOT).parts):
            continue
        if path.suffix not in {".html", ".json", ".txt", ".xml", ".js"}:
            continue
        yield path


def _person_urls(html: str) -> list[str]:
    urls = []
    for block in JSONLD.findall(html):
        try:
            data = json.loads(block)
        except json.JSONDecodeError:
            continue
        stack = [data]
        while stack:
            node = stack.pop()
            if isinstance(node, dict):
                types = node.get("@type")
                types = types if isinstance(types, list) else [types]
                if "Person" in types and isinstance(node.get("url"), str):
                    urls.append(node["url"])
                stack.extend(node.values())
            elif isinstance(node, list):
                stack.extend(node)
    return urls


class AuthorSchemaKeeperTests(unittest.TestCase):
    def test_public_files_do_not_cite_author_stubs(self):
        hits = []
        for path in _iter_public():
            text = path.read_text(encoding="utf-8", errors="replace")
            for stub in STUBS:
                if stub in text:
                    hits.append(f"{path.relative_to(REPO_ROOT)}: {stub}")
        self.assertEqual(hits, [])

    def test_refresh_stubs_stay_noindex_and_canonical_to_the_bio(self):
        stubs = {
            "author-connor-walsh.html": KEEPER,
            "author/connor-walsh.html": KEEPER,
            "author/connor-walsh/index.html": KEEPER,
            "author-rielly-walsh.html": RIELLY,
            "author/rielly-walsh.html": RIELLY,
            "author/rielly-walsh/index.html": RIELLY,
        }
        for rel, keeper in stubs.items():
            html = (REPO_ROOT / rel).read_text(encoding="utf-8")
            self.assertIn('content="noindex,follow"', html, rel)
            self.assertIn('http-equiv="refresh"', html, rel)
            self.assertIn(f'href="{keeper}"', html, rel)
            self.assertTrue((REPO_ROOT / rel).is_file(), rel)

    def test_sample_person_urls_name_the_connor_bio(self):
        for rel in SAMPLE_PAGES:
            html = (REPO_ROOT / rel).read_text(encoding="utf-8")
            urls = _person_urls(html)
            self.assertIn(KEEPER, urls, rel)
            for url in urls:
                self.assertNotIn("author-connor-walsh", url, rel)
                self.assertNotIn("author/connor-walsh", url, rel)

    def test_site_search_lists_the_bios_not_the_stubs(self):
        data = json.loads((REPO_ROOT / "search-index.json").read_text())
        by_url = {item["u"]: item["t"] for item in data}
        self.assertEqual(
            by_url["/authors/connor-walsh.html"],
            "Connor Walsh - President, American Commercial Glass",
        )
        self.assertEqual(
            by_url["/authors/rielly-walsh.html"],
            "Rielly Walsh - CEO, American Commercial Glass | Author",
        )
        self.assertNotIn("/author-connor-walsh.html", by_url)
        self.assertNotIn("/author-rielly-walsh.html", by_url)

    def test_frozen_money_titles_stay_exact(self):
        for rel, expected in FROZEN_TITLES.items():
            html = (REPO_ROOT / rel).read_text(encoding="utf-8")
            title = re.sub(r"\s+", " ", TITLE.search(html).group(1)).strip()
            self.assertEqual(title, expected, rel)
