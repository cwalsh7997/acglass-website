#!/usr/bin/env python3
"""Rielly Walsh joined ACG in 2022. She is CEO and majority owner, not a co-founder."""

from __future__ import annotations

import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
SKIP_PARTS = {".git", "drafts", "node_modules"}
SURFACES = (
    "capabilities.html",
    "authors/connor-walsh.html",
    "authors/rielly-walsh.html",
    "careers.html",
    "acg-glass-florida/index.html",
    "llms-full.txt",
)
# Forward from Rielly's name. A period stops the window so Connor's own
# "President & Co-founder" title, later in the same file, is not a hit.
RIELLY_COFOUNDER = re.compile(r"Rielly[^.]{0,80}co-?founder", re.IGNORECASE)
EXACT_FORBIDDEN = (
    "co-founded American Commercial Glass with my wife",
    "two co-founders",
    "founded on February 18, 2021 by Rielly",
    "Founded February 18, 2021 by Rielly",
    "founded in 2021 by Rielly",
    "Co-Founder &amp; Chief Executive Officer",
    "CEO, Co-founder",
    "CEO & Co-founder",
    "Construction operations &middot; Co-founder, ACG",
    "the owners who founded the company in 2021",
)
JSONLD = re.compile(
    r'<script\b[^>]*type=["\']application/ld\+json["\'][^>]*>(.*?)</script>',
    re.IGNORECASE | re.DOTALL,
)


def _iter_content_files():
    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue
        parts = set(path.relative_to(ROOT).parts)
        if parts & SKIP_PARTS:
            continue
        if path.relative_to(ROOT).parts[:2] == (".github", "agent-state"):
            continue
        if path.suffix.lower() not in {".html", ".txt", ".json", ".xml", ".md"}:
            continue
        yield path


def _founder_refs(html: str) -> list[str]:
    refs = []
    for block in JSONLD.findall(html):
        try:
            data = json.loads(block)
        except json.JSONDecodeError:
            continue
        stack = [data]
        while stack:
            node = stack.pop()
            if isinstance(node, dict):
                founder = node.get("founder")
                founders = founder if isinstance(founder, list) else [founder]
                for item in founders:
                    if isinstance(item, dict):
                        name = item.get("name")
                        ident = item.get("@id")
                        if isinstance(name, str):
                            refs.append(name)
                        if isinstance(ident, str):
                            refs.append(ident)
                    elif isinstance(item, str):
                        refs.append(item)
                stack.extend(node.values())
            elif isinstance(node, list):
                stack.extend(node)
    return refs


class RiellyCofounderScrubTests(unittest.TestCase):
    def test_named_surfaces_do_not_make_rielly_a_founder(self):
        for rel in SURFACES:
            source = (ROOT / rel).read_text(encoding="utf-8")
            with self.subTest(rel=rel):
                self.assertIsNone(
                    RIELLY_COFOUNDER.search(source),
                    RIELLY_COFOUNDER.pattern,
                )
                for phrase in (
                    "co-founded American Commercial Glass with my wife",
                    "two co-founders",
                    "founded on February 18, 2021 by Rielly",
                ):
                    self.assertNotIn(phrase, source)

    def test_corrected_lines_stay_in_place(self):
        capabilities = (ROOT / "capabilities.html").read_text(encoding="utf-8")
        self.assertIn(
            "Chief Executive Officer &amp; Majority Owner",
            capabilities,
        )
        connor = (ROOT / "authors/connor-walsh.html").read_text(encoding="utf-8")
        self.assertIn(
            "In 2021 I co-founded American Commercial Glass. My wife, "
            '<a href="/authors/rielly-walsh.html">Rielly Walsh</a>, joined in 2022 '
            "and leads ACG as CEO and majority owner.",
            connor,
        )
        self.assertIn("President &amp; Co-founder", connor)
        rielly = (ROOT / "authors/rielly-walsh.html").read_text(encoding="utf-8")
        self.assertIn(
            '<div class="author-fact-label">Joined ACG</div>'
            '<div class="author-fact-value">2022</div>',
            rielly,
        )
        self.assertNotIn(
            '<div class="author-fact-label">Founded</div>'
            '<div class="author-fact-value">2021</div>',
            rielly,
        )
        careers = (ROOT / "careers.html").read_text(encoding="utf-8")
        self.assertIn(
            "the owners who still price, plan, and close out every project",
            careers,
        )
        florida = (ROOT / "acg-glass-florida/index.html").read_text(encoding="utf-8")
        self.assertIn('<div class="identity-key">Leadership</div>', florida)
        self.assertNotIn('<div class="identity-key">Founders</div>', florida)
        self.assertIn("Connor Walsh (President)", florida)
        self.assertIn("Rielly Walsh (CEO)", florida)
        llms = (ROOT / "llms-full.txt").read_text(encoding="utf-8")
        self.assertIn("ACG is led by its two owners:", llms)
        self.assertIn(
            "Rielly Walsh - CEO & majority owner (51%), joined ACG in 2022.",
            llms,
        )
        self.assertIn("Connor Walsh - President & Co-founder.", llms)
        self.assertIn("owner, joined 2022)", llms)

    def test_repo_has_no_leftover_rielly_founder_wording(self):
        hits = []
        for path in _iter_content_files():
            source = path.read_text(encoding="utf-8", errors="replace")
            rel = str(path.relative_to(ROOT))
            for match in RIELLY_COFOUNDER.finditer(source):
                # "President and co-founder Connor Walsh" names Connor, not Rielly.
                tail = source[match.end(): match.end() + 24]
                if re.match(r"\s+Connor\b", tail, re.IGNORECASE):
                    continue
                hits.append(f"{rel}: Rielly ... co-founder")
                break
            for phrase in EXACT_FORBIDDEN:
                if phrase in source:
                    hits.append(f"{rel}: {phrase}")
            if path.suffix.lower() == ".html":
                for ref in _founder_refs(source):
                    if "rielly" in ref.lower():
                        hits.append(f"{rel}: founder {ref}")
        self.assertEqual(hits, [])


if __name__ == "__main__":
    unittest.main(verbosity=2)
