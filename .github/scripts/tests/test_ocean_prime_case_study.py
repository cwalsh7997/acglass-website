#!/usr/bin/env python3
"""Guard the Ocean Prime Fort Lauderdale case study against portfolio overwrite."""

from __future__ import annotations

import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
PRIMARY = ROOT / "ocean-prime-ft-lauderdale.html"
PRIMARY_URL = "https://acglass.com/ocean-prime-ft-lauderdale.html"
PORTFOLIO_URL = "https://acglass.com/portfolio.html"


def _read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


class OceanPrimeCaseStudyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.html = PRIMARY.read_text(encoding="utf-8")

    def test_page_is_not_a_redirect_stub(self):
        self.assertNotIn('http-equiv="refresh"', self.html.lower())
        self.assertNotIn("window.location.replace", self.html)
        self.assertGreater(len(self.html), 8000)

    def test_self_canonical_not_portfolio(self):
        canonical = re.search(r'rel="canonical"[^>]+href="([^"]+)"', self.html, re.I)
        self.assertIsNotNone(canonical)
        self.assertEqual(PRIMARY_URL, canonical.group(1))
        self.assertNotIn(f'rel="canonical" href="{PORTFOLIO_URL}"', self.html)

    def test_title_og_and_h1_are_ocean_prime(self):
        title = re.search(r"<title>(.*?)</title>", self.html, re.S).group(1)
        h1 = re.search(r"<h1\b[^>]*>(.*?)</h1>", self.html, re.S).group(1)
        h1_text = re.sub(r"<[^>]+>", "", h1)
        self.assertIn("Ocean Prime", title)
        self.assertIn("Fort Lauderdale", title)
        self.assertNotIn("Florida Commercial Glazing Portfolio", title)
        self.assertIn("Ocean Prime", h1_text)
        self.assertNotIn("The record, project by project", h1_text)
        self.assertIn("Ocean Prime", self.html)
        self.assertIn("og:title", self.html)
        self.assertIn("twitter:title", self.html)
        self.assertIn("Euro-Wall", self.html)

    def test_scope_and_address_are_live_truthful(self):
        self.assertIn("171 Las Olas Circle", self.html)
        self.assertIn("Las Olas Marina", self.html)
        self.assertRegex(self.html, r"one Euro-Wall door/opening|single Euro-Wall door/opening")
        self.assertNotIn("Buckeye", self.html)
        self.assertNotIn("Made In Rio", self.html)
        self.assertNotIn("The record, project by project", self.html)
        self.assertNotIn("Florida Commercial Glazing Portfolio", self.html)

    def test_rfq_cta_points_at_send_plans(self):
        self.assertIn("send-plans.html", self.html)
        self.assertIn("Send Us Plans", self.html)

    def test_aliases_do_not_canonical_to_portfolio(self):
        aliases = (
            "projects/ocean-prime-ft-lauderdale.html",
            "case-study-ocean-prime.html",
            "case-study-ocean-prime-fort-lauderdale.html",
            "ocean-prime-fort-lauderdale/index.html",
        )
        for rel in aliases:
            html = _read(rel)
            canonical = re.search(r'rel="canonical"[^>]+href="([^"]+)"', html, re.I)
            self.assertIsNotNone(canonical, rel)
            self.assertEqual(PRIMARY_URL, canonical.group(1), rel)
            self.assertNotIn(f'href="{PORTFOLIO_URL}"', canonical.group(0), rel)

    def test_projects_alias_is_noindex_and_keeper_is_sitemapped(self):
        """Duplicate is noindex. Sitemap lists the keeper, not the projects alias."""
        alias = "https://acglass.com/projects/ocean-prime-ft-lauderdale.html"
        html = _read("projects/ocean-prime-ft-lauderdale.html")
        keeper_line = (
            "<url><loc>https://acglass.com/ocean-prime-ft-lauderdale.html</loc>"
            "<lastmod>2026-08-20</lastmod></url>"
        )
        self.assertIn('<meta name="robots" content="noindex,follow">', html)
        for name in ("sitemap.xml", "sitemap-projects.xml"):
            body = _read(name)
            self.assertNotIn(alias, body, name)
            self.assertIn(keeper_line, body, name)
        self.assertNotIn(alias, _read("sitemap-pages.xml"))

    def test_high_traffic_cards_link_to_the_keeper(self):
        """Keeper returns 200. Indexable cards must not cite the noindex alias."""
        target = "/ocean-prime-ft-lauderdale.html"
        alias = "/projects/ocean-prime-ft-lauderdale.html"
        for rel in (
            "index.html",
            "portfolio.html",
            "past-performance.html",
            "services.html",
            "capabilities.html",
            "florida-commercial-glazing/index.html",
        ):
            html = _read(rel)
            self.assertIn(f'href="{target}"', html, rel)
            self.assertNotIn(f'href="{alias}"', html, rel)

    def test_indexable_pages_do_not_link_the_noindex_alias(self):
        alias = 'href="/projects/ocean-prime-ft-lauderdale.html"'
        robots = re.compile(
            r'<meta[^>]+name=["\']robots["\'][^>]+content=["\']([^"\']+)',
            re.I,
        )
        hits = []
        for path in ROOT.rglob("*.html"):
            rel = path.relative_to(ROOT)
            if set(rel.parts) & {".git", ".github", "node_modules", "drafts"}:
                continue
            html = path.read_text(encoding="utf-8")
            if alias not in html:
                continue
            meta = robots.search(html)
            if meta and "noindex" in meta.group(1).lower():
                continue
            hits.append(str(rel))
        self.assertEqual(hits, [])

    def test_vercel_mirror_does_not_redirect_primary_to_portfolio(self):
        data = json.loads(_read("vercel.json"))
        for rule in data.get("redirects", []):
            source = rule.get("source", "")
            dest = rule.get("destination", "")
            if "ocean-prime" in source:
                self.assertNotEqual("/portfolio.html", dest, source)
                self.assertNotIn("portfolio.html", dest)

    def test_alias_jsonld_cites_the_keeper_and_project_type(self):
        """Alias stays noindex. Its schema names the indexable keeper, which returns 200."""
        live = PRIMARY_URL
        html = _read("projects/ocean-prime-ft-lauderdale.html")
        blocks = [
            json.loads(block)
            for block in re.findall(
                r'<script[^>]*type=["\']application/ld\+json["\'][^>]*>(.*?)</script>',
                html,
                re.I | re.S,
            )
        ]

        def walk(obj):
            if isinstance(obj, dict):
                yield obj
                for value in obj.values():
                    yield from walk(value)
            elif isinstance(obj, list):
                for value in obj:
                    yield from walk(value)

        article = None
        crumbs = []
        for block in blocks:
            for node in walk(block):
                raw = node.get("@type")
                types = set(raw) if isinstance(raw, list) else {raw}
                if "Article" in types or "Project" in types:
                    article = node
                if "ListItem" in types and node.get("position") == 3:
                    crumbs.append(node.get("item"))
        self.assertIsNotNone(article)
        types = article.get("@type")
        self.assertIn("Project", types)
        self.assertIn("Article", types)
        self.assertEqual(live, article.get("url"))
        self.assertEqual(live, article.get("mainEntityOfPage", {}).get("@id"))
        self.assertIn(live, crumbs)
        self.assertNotIn(
            "https://acglass.com/projects/ocean-prime-ft-lauderdale.html",
            json.dumps(blocks),
        )
        self.assertIn("Cameron Mitchell", html)
        self.assertIn("Kobi Karp", html)
        self.assertIn("one Euro-Wall door/opening", html)
        self.assertIn('href="/euro-wall.html"', html)
        self.assertIn('href="/storefront-glazier-fort-lauderdale-florida/"', html)
        self.assertIn('href="/projects/"', html)
        self.assertIn('href="/restaurant-glazing-contractor.html"', html)
        self.assertIn('href="/portfolio.html"', html)
        self.assertIn("send-plans.html", html)
        self.assertNotIn("full-facade package of", html.lower())


if __name__ == "__main__":
    unittest.main(verbosity=2)
