#!/usr/bin/env python3
"""Guards the mobile nav surfaces in css/acg-proof.css against bleed-through.

The fixed header bar and the full-screen menu overlay both sit directly over
display-weight page copy at phone widths. Any alpha below 1 lets that copy ghost
through behind the wordmark, the menu button and the menu links.

Run:  python3 -m unittest discover -s .github/scripts/tests -v
"""

from __future__ import annotations

import re
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
CSS = (REPO_ROOT / "css" / "acg-proof.css").read_text(encoding="utf-8")

# The two surfaces that cover page content at phone widths.
NAV_SURFACES = ("nav.links", "header.nav.scrolled")

ALPHA_FUNC = re.compile(r"\b(?:rgba|hsla)\(([^)]*)\)")
HEX_WITH_ALPHA = re.compile(r"#(?:[0-9a-fA-F]{4}|[0-9a-fA-F]{8})\b")
RULE = re.compile(r"([^{}]+)\{([^{}]*)\}")


def strip_comments(css: str) -> str:
    return re.sub(r"/\*.*?\*/", "", css, flags=re.DOTALL)


def media_blocks(css: str) -> list[tuple[str, str]]:
    """(condition, body) for every @media rule, found by brace matching."""
    out = []
    for match in re.finditer(r"@media([^{]*)\{", css):
        depth, i = 1, match.end()
        while i < len(css) and depth:
            depth += {"{": 1, "}": -1}.get(css[i], 0)
            i += 1
        out.append((match.group(1).strip(), css[match.end() : i - 1]))
    return out


def rules_for(body: str, selector: str) -> list[str]:
    """Declaration blocks in `body` whose selector list includes `selector`."""
    return [
        rule.group(2)
        for rule in RULE.finditer(body)
        if selector in [s.strip() for s in rule.group(1).split(",")]
    ]


def backgrounds(block: str) -> list[str]:
    out = []
    for decl in block.split(";"):
        prop, _, value = decl.partition(":")
        if prop.strip() in ("background", "background-color"):
            out.append(value.strip())
    return out


def alpha(token: str) -> float:
    token = token.strip()
    return float(token.rstrip("%")) / 100 if token.endswith("%") else float(token)


def is_opaque(value: str) -> bool:
    """False for any value that can let page content show through."""
    if "gradient" in value or "transparent" in value:
        return False
    if HEX_WITH_ALPHA.search(value):
        return False
    for args in ALPHA_FUNC.findall(value):
        parts = re.split(r"[,/]", args)
        if len(parts) > 3 and alpha(parts[3]) < 1:
            return False
    return True


class MobileNavOpacityTests(unittest.TestCase):
    """Every mobile-scoped background on a nav surface must be fully opaque."""

    @classmethod
    def setUpClass(cls):
        cls.mobile = [
            body
            for condition, body in media_blocks(strip_comments(CSS))
            if "max-width" in condition and "prefers-" not in condition
        ]

    def test_obsidian_variable_is_opaque(self):
        self.assertRegex(CSS, r"--obsidian:\s*#05070C\b")

    def test_mobile_nav_surfaces_are_opaque(self):
        for selector in NAV_SURFACES:
            found = [
                value
                for body in self.mobile
                for block in rules_for(body, selector)
                for value in backgrounds(block)
            ]
            with self.subTest(selector=selector):
                self.assertTrue(found, f"no mobile background declared for {selector}")
                for value in found:
                    self.assertTrue(
                        is_opaque(value),
                        f"{selector} background {value!r} is not fully opaque",
                    )

    def test_wordmark_clears_the_menu_overlay(self):
        """The overlay covers the bar, so the wordmark needs the button's layer."""
        layers = {}
        for selector in (".wordmark", ".menu-btn"):
            for body in self.mobile:
                for block in rules_for(body, selector):
                    found = re.search(r"z-index:\s*(\d+)", block)
                    if found:
                        layers[selector] = int(found.group(1))
        self.assertIn(".wordmark", layers, "wordmark has no mobile z-index")
        self.assertGreaterEqual(layers[".wordmark"], layers[".menu-btn"])


if __name__ == "__main__":
    unittest.main()
