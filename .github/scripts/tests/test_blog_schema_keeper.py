"""Blog schema and the RSS channel must cite the live blog, not the stub."""

from __future__ import annotations

import json
import re
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[3]
SKIP_DIRS = {".git", ".github", "node_modules"}
KEEPER = "https://acglass.com/blog/"
STUB_URL = "https://acglass.com/blog.html"
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
SAMPLE_PAGES = (
    "blog/ocean-prime-ft-lauderdale-glazing.html",
    "blog/how-to-choose-commercial-glass-contractor-florida.html",
    "blog-2026/florida-impact-glass-cost-guide-2026/index.html",
)
JSONLD = re.compile(
    r'<script\b[^>]*type=["\']application/ld\+json["\'][^>]*>(.*?)</script>',
    re.I | re.S,
)
TITLE = re.compile(r"<title[^>]*>(.*?)</title>", re.I | re.S)


def _iter_html():
    for path in REPO_ROOT.rglob("*.html"):
        if SKIP_DIRS.intersection(path.relative_to(REPO_ROOT).parts):
            continue
        yield path


def _blog_parent_urls(html: str) -> list[str]:
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
                if "Blog" in types and isinstance(node.get("url"), str):
                    urls.append(node["url"])
                if node.get("@type") == "BreadcrumbList":
                    for item in node.get("itemListElement") or []:
                        if (
                            isinstance(item, dict)
                            and item.get("name") == "Blog"
                            and isinstance(item.get("item"), str)
                        ):
                            urls.append(item["item"])
                stack.extend(node.values())
            elif isinstance(node, list):
                stack.extend(node)
    return urls


class BlogSchemaKeeperTests(unittest.TestCase):
    def test_public_html_does_not_cite_the_blog_stub(self):
        hits = []
        for path in _iter_html():
            rel = path.relative_to(REPO_ROOT).as_posix()
            if rel == "blog.html":
                continue
            html = path.read_text(encoding="utf-8", errors="replace")
            if STUB_URL in html or 'href="/blog.html"' in html:
                hits.append(rel)
        self.assertEqual(hits, [])

    def test_sample_pages_point_blog_schema_at_the_live_index(self):
        for rel in SAMPLE_PAGES:
            html = (REPO_ROOT / rel).read_text(encoding="utf-8")
            urls = _blog_parent_urls(html)
            self.assertTrue(urls, rel)
            self.assertTrue(all(url == KEEPER for url in urls), f"{rel}: {urls}")

    def test_live_blog_and_stub_stay_in_their_roles(self):
        live = (REPO_ROOT / "blog" / "index.html").read_text(encoding="utf-8")
        self.assertIn(f'"url": "{KEEPER}"', live)
        self.assertIn('rel="canonical" href="https://acglass.com/blog/"', live)
        stub = (REPO_ROOT / "blog.html").read_text(encoding="utf-8")
        self.assertIn('http-equiv="refresh" content="0; url=/blog/"', stub)
        self.assertIn('name="robots" content="noindex,follow"', stub)
        self.assertIn('rel="canonical" href="https://acglass.com/blog/"', stub)
        self.assertNotIn(STUB_URL, stub)

    def test_news_crumb_on_the_tampa_release_points_at_news(self):
        # This alias's crumb is named News. It used to cite the blog stub.
        # The live news index is /news/, not the blog.
        html = (REPO_ROOT / "press-release-tampa.html").read_text(encoding="utf-8")
        self.assertIn('"name": "News"', html)
        self.assertIn('"item": "https://acglass.com/news/"', html)
        self.assertNotIn(STUB_URL, html)
        self.assertNotIn(KEEPER, html)

    def test_feed_and_site_search_use_the_live_blog(self):
        feed = (REPO_ROOT / "feed.xml").read_text(encoding="utf-8")
        self.assertIn(f"<link>{KEEPER}</link>", feed)
        self.assertNotIn(STUB_URL, feed)
        rows = json.loads((REPO_ROOT / "search-index.json").read_text(encoding="utf-8"))
        blog_rows = [row for row in rows if row.get("u") in {"/blog.html", "/blog/"}]
        self.assertEqual([row["u"] for row in blog_rows], ["/blog/"])

    def test_frozen_titles_are_unchanged(self):
        for rel, expected in FROZEN_TITLES.items():
            html = (REPO_ROOT / rel).read_text(encoding="utf-8")
            match = TITLE.search(html)
            self.assertIsNotNone(match, rel)
            title = re.sub(r"\s+", " ", match.group(1)).strip()
            self.assertEqual(title, expected, rel)


if __name__ == "__main__":
    unittest.main()
