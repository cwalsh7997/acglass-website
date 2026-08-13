#!/usr/bin/env python3
"""Tests for the site-wide delivery-complete Tennessee claim check.

Run:  python3 -m unittest discover -s .github/scripts/tests -v
"""

from __future__ import annotations

import importlib.util
import re
import sys
import unittest
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parents[1]

_spec = importlib.util.spec_from_file_location(
    "tn_claim_guard", SCRIPTS_DIR / "tn-claim-guard.py"
)
guard = importlib.util.module_from_spec(_spec)
sys.modules["tn_claim_guard"] = guard
_spec.loader.exec_module(guard)


def violations(text: str) -> list[str]:
    out: list[str] = []
    guard.check_delivery_claims("page.html", text, lambda rel, msg: out.append(msg))
    return out


class DeliveryClaimTests(unittest.TestCase):
    def test_bare_office_count_is_a_violation(self):
        self.assertEqual(len(violations("<p>Four offices. One glazing standard.</p>")), 1)
        self.assertEqual(len(violations("<p>FL CGC #1531993. 4 offices FL + TN.</p>")), 1)

    def test_office_count_with_planned_market_qualifier_passes(self):
        # This helper tests the legacy site-wide detector in isolation. The
        # governed Florida-page check rejects the same expansion language.
        self.assertEqual(
            violations(
                "<h1>Four offices. <em>One glazing standard.</em></h1>"
                "<p>West Palm Beach headquarters, Naples and Tampa offices covering "
                "Florida statewide — and a Nashville, Tennessee office opening Q3 2026.</p>"
            ),
            [],
        )

    def test_qualifier_may_sit_below_a_heading_in_a_list(self):
        # The scoped high-visibility page contract is intentionally stricter.
        self.assertEqual(
            violations(
                "ACG operates four offices:\n\n"
                "- West Palm Beach, FL (HQ) — Active\n"
                "- Naples, FL — Active\n"
                "- Tampa, FL — Active\n"
                "- Nashville, TN — Opening Q3 2026\n"
            ),
            [],
        )

    def test_delivery_verb_on_the_state_pair_is_a_violation(self):
        self.assertEqual(
            len(
                violations(
                    '"description": "American Commercial Glass serves hospitality, '
                    "healthcare, government, multifamily, restaurants, and education "
                    'projects across Florida and Tennessee."'
                )
            ),
            1,
        )
        self.assertEqual(
            len(
                violations(
                    '"description": "Commercial glazing services for government and '
                    'public-sector construction projects in Florida and Tennessee"'
                )
            ),
            1,
        )

    def test_qualified_delivery_claim_passes(self):
        self.assertEqual(
            violations(
                '"description": "Commercial glazing services for government and '
                "public-sector construction projects across Florida, with Tennessee "
                'coverage beginning Q3 2026"'
            ),
            [],
        )

    def test_contrastive_copy_is_not_a_delivery_claim(self):
        # Naming both states to explain how their codes differ is the point of
        # the comparison pages, not a claim to be operating in both.
        for text in (
            "<p>Essential-facility designations, wind zone requirements, and state "
            "code adoptions differ between Florida and Tennessee.</p>",
            "<p>The physics of an IGU don't change between Florida and Tennessee. "
            "The priority does.</p>",
            "<p>For a side-by-side on how the two states differ, see our "
            '<a href="/locations.html">Florida and Tennessee service areas</a>.</p>',
        ):
            self.assertEqual(violations(text), [], text)

    def test_titles_are_out_of_scope(self):
        # Title length budgets cannot carry the qualifier, and retitling is a
        # separate ranking decision.
        self.assertEqual(
            violations(
                "<title>Locations &amp; Coverage | 4 Offices FL + TN | ACG</title>\n"
                '<meta property="og:title" content="Locations | 4 Offices FL + TN | ACG">\n'
                '<meta name="twitter:title" content="Locations | 4 Offices FL + TN | ACG">'
            ),
            [],
        )

    def test_state_pair_without_a_delivery_verb_passes(self):
        # The homepage Organization description; frozen path, and honest as a
        # market descriptor rather than a delivery claim.
        self.assertEqual(
            violations(
                '"description": "Florida & Tennessee commercial glazing contractor. '
                'Storefront, curtainwall, impact, and fire-rated glazing for general contractors."'
            ),
            [],
        )


class DiscoveryTests(unittest.TestCase):
    def test_claim_scan_covers_files_the_tn_discovery_pass_cannot_see(self):
        # industries.html is not Tennessee-scoped, which is exactly why the
        # residual survived there: is_tn_page() never returns True for it.
        self.assertFalse(guard.is_tn_page("industries.html", "<title>Industries | ACG</title>"))
        names = {rel for rel, _ in guard.iter_claim_files()}
        self.assertIn("industries.html", names)
        self.assertIn("llms.txt", names)


class ScopedStaleOperatingClaimTests(unittest.TestCase):
    def scoped_violations(self, rel: str, text: str) -> list[str]:
        out: list[str] = []
        guard.check_scoped_stale_operating_claims(
            rel, text, lambda path, msg: out.append(msg)
        )
        return out

    def test_exact_governed_page_set(self):
        self.assertEqual(
            guard.STALE_OPERATING_CLAIM_PAGES,
            (
                "ask.html",
                "best-glazing-subcontractor-florida.html",
                "best-storefront-contractor-florida.html",
                "blog/florida-commercial-construction-2026-outlook.html",
                "commercial-storefront-installer-florida.html",
                "facts.html",
                "glass-canopies-commercial.html",
                "industries.html",
                "miami-hvhz-glazing-contractor.html",
            ),
        )

    def test_operating_language_fails_on_governed_pages(self):
        examples = (
            "Nashville office opening in 2026",
            "Tennessee coverage",
            "ACG has a Tennessee office.",
            "ACG is opening a TN office in 2027.",
            "ACG is bidding TN commercial glazing projects.",
            "ACG serves Middle Tennessee.",
            "ACG is expanding into Tennessee.",
            "ACG works across Florida and the Southeast.",
            "Middle TN projects",
            "Nashville Q3 2026",
            "Q3 2026 launch",
        )
        for rel in guard.STALE_OPERATING_CLAIM_PAGES:
            for text in examples:
                with self.subTest(rel=rel, text=text):
                    self.assertTrue(self.scoped_violations(rel, text))

    def test_neutral_education_reference_is_preserved(self):
        text = "Concrete Industry Management graduate, Middle Tennessee State University."
        self.assertEqual(self.scoped_violations("facts.html", text), [])

    def test_neutral_education_reference_is_path_bound(self):
        text = "Concrete Industry Management graduate, Middle Tennessee State University."
        self.assertTrue(self.scoped_violations("ask.html", text))

    def test_university_name_is_not_a_blanket_claim_exception(self):
        text = "ACG serves Middle Tennessee State University projects."
        self.assertTrue(self.scoped_violations("facts.html", text))

    def test_metadata_schema_and_visible_copy_all_fail_closed(self):
        examples = (
            '<meta name="description" content="ACG serves Tennessee projects.">',
            '<script type="application/ld+json">'
            '{"description":"ACG is opening a Nashville office."}'
            "</script>",
            "<p>ACG is bidding TN projects.</p>",
        )
        for text in examples:
            with self.subTest(text=text):
                self.assertTrue(self.scoped_violations("industries.html", text))

    def test_non_governed_neutral_references_remain_out_of_scope(self):
        examples = (
            "Tennessee adopted the 2018 IBC.",
            "Florida and Tennessee code requirements differ.",
            "Metro Nashville Codes office administers permits.",
            "Nashville office construction is recovering.",
            "Harmon operates a Nashville office.",
        )
        for text in examples:
            with self.subTest(text=text):
                self.assertEqual(self.scoped_violations("comparison.html", text), [])

    def test_current_governed_pages_have_no_stale_operating_language(self):
        root = SCRIPTS_DIR.parents[1]
        for rel in guard.STALE_OPERATING_CLAIM_PAGES:
            with self.subTest(rel=rel):
                text = (root / rel).read_text(encoding="utf-8")
                self.assertEqual(self.scoped_violations(rel, text), [])

    def test_ask_question_count_matches_rendered_questions(self):
        root = SCRIPTS_DIR.parents[1]
        text = (root / "ask.html").read_text(encoding="utf-8")
        rendered_count = len(re.findall(r'class="qa-item"', text))
        stated = re.search(r'<b>Questions</b>\s+(\d+)', text)
        self.assertIsNotNone(stated)
        self.assertEqual(int(stated.group(1)), rendered_count)


if __name__ == "__main__":
    unittest.main()
