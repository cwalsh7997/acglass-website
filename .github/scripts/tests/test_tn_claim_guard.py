#!/usr/bin/env python3
"""Tests for the site-wide delivery-complete Tennessee claim check.

Run:  python3 -m unittest discover -s .github/scripts/tests -v
"""

from __future__ import annotations

import importlib.util
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
        self.assertEqual(
            violations(
                "<h1>Four offices. <em>One glazing standard.</em></h1>"
                "<p>West Palm Beach headquarters, Naples and Tampa offices covering "
                "Florida statewide — and a Nashville, Tennessee office opening Q3 2026.</p>"
            ),
            [],
        )

    def test_qualifier_may_sit_below_a_heading_in_a_list(self):
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


if __name__ == "__main__":
    unittest.main()
