#!/usr/bin/env python3
"""Tests for the site-wide delivery-complete Tennessee claim check.

Run:  python3 -m unittest discover -s .github/scripts/tests -v
"""

from __future__ import annotations

import copy
import importlib.util
import json
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


def violations(text: str, rel: str = "page.html") -> list[str]:
    out: list[str] = []
    guard.check_delivery_claims(rel, text, lambda path, msg: out.append(msg))
    return out


class DeliveryClaimTests(unittest.TestCase):
    def test_bare_office_count_is_a_violation(self):
        self.assertEqual(len(violations("<p>Four offices. One glazing standard.</p>")), 1)
        self.assertEqual(len(violations("<p>FL CGC #1531993. 4 offices FL + TN.</p>")), 1)
        self.assertEqual(
            len(violations("<p>ACG's fourth office is now open.</p>")),
            1,
        )
        self.assertEqual(
            len(violations("<p>Office number four is now serving projects.</p>")),
            1,
        )

    def test_planned_market_language_does_not_qualify_office_count(self):
        self.assertEqual(
            len(
                violations(
                    "<h1>Four offices. <em>One glazing standard.</em></h1>"
                    "<p>West Palm Beach headquarters, Naples and Tampa offices covering "
                    "Florida statewide. A Nashville, Tennessee office is planned.</p>"
                )
            ),
            1,
        )

    def test_opening_language_in_a_list_does_not_qualify_office_count(self):
        self.assertEqual(
            len(
                violations(
                    "ACG operates four offices:\n\n"
                    "- West Palm Beach, FL (HQ): Active\n"
                    "- Naples, FL: Active\n"
                    "- Tampa, FL: Active\n"
                    "- Nashville, TN: Opening Q3 2026\n"
                )
            ),
            1,
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

    def test_planned_delivery_claim_is_a_violation(self):
        self.assertEqual(
            len(
                violations(
                    '"description": "Commercial glazing services for government and '
                    "public-sector construction projects across Florida and Tennessee, "
                    'with Tennessee coverage beginning Q3 2026"'
                )
            ),
            1,
        )

    def test_projects_page_is_clean_without_any_held_exception(self):
        # The 2026-08 compliance scrub removed the Tennessee delivery claim from
        # projects/index.html at source, so the page passes on its own merits and
        # HELD_DELIVERY_CLAIMS is empty. This is strictly stronger than the old
        # fingerprint hold it replaces: there is no exception left to drift.
        root = SCRIPTS_DIR.parents[1]
        source = (root / "projects/index.html").read_text(encoding="utf-8")
        self.assertEqual(violations(source, "projects/index.html"), [])
        self.assertEqual(guard.HELD_DELIVERY_CLAIMS, {})

    def test_reintroducing_the_projects_claim_is_a_violation(self):
        # Regression lock: if anyone restores the retired operating claim, the
        # guard must fail rather than fall back to a held exception.
        root = SCRIPTS_DIR.parents[1]
        source = (root / "projects/index.html").read_text(encoding="utf-8")
        self.assertNotIn("Tennessee from Q3 2026", source)
        restored = source.replace(
            "ACG operates Florida offices in West Palm Beach, Naples, and Stuart",
            "ACG operates four offices across two states - serving Florida now, "
            "Tennessee from Q3 2026. ACG operates Florida offices in West Palm Beach, Naples, and Stuart",
            1,
        )
        self.assertNotEqual(restored, source)
        self.assertEqual(len(violations(restored, "projects/index.html")), 1)

    def test_missing_held_fingerprint_is_reported(self):
        out = []
        guard.check_held_delivery_claims(set(), lambda rel, msg: out.append((rel, msg)))
        self.assertEqual(len(out), len(guard.HELD_DELIVERY_CLAIMS))

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

    def test_delivery_regex_masks_titles_but_inventory_governs_them(self):
        # Title text is governed by the separate reference inventory.
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


class ReferenceInventoryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.root = SCRIPTS_DIR.parents[1]
        cls.inventory = json.loads(
            (cls.root / ".github/tn-reference-inventory.json").read_text(
                encoding="utf-8"
            )
        )
        cls.sources = {
            rel: Path(full).read_text(encoding="utf-8")
            for rel, full in guard.iter_html_files()
        }
        cls.css_sources = {
            rel: Path(full).read_text(encoding="utf-8")
            for rel, full in guard.iter_css_files()
        }

    def test_current_reference_inventory_is_exact(self):
        errors, stats = guard.reference_inventory_violations(
            self.sources, self.inventory, self.css_sources
        )
        self.assertEqual(errors, [])
        self.assertEqual(
            stats,
            {
                "document_sources": 150,
                "path_or_title_discovery": 73,
                "outside_discovery": 77,
                "known_edge_301_sources": 4,
                "document_sources_excluding_recorded_edge_sources": 146,
                "excluded_non_page_fragments": 1,
            },
        )
        self.assertEqual(
            {
                name: len(paths)
                for name, paths in self.inventory["reference_groups"].items()
            },
            {
                "path_or_title_discovery": 73,
                "stale_operating_claim_hold": 26,
                "mixed_claim_review": 1,
                "biography_only": 39,
                "technical_or_market_review": 8,
                "license_disclaimer_link_review": 1,
                "source_controlled_project_claim": 1,
                "outside_edge_redirect_source": 2,
            },
        )

    def test_new_content_token_source_fails_closed(self):
        sources = dict(self.sources)
        sources["new-market.html"] = (
            "<!doctype html><html><body>ACG serves Tennessee.</body></html>"
        )
        errors, _ = guard.reference_inventory_violations(sources, self.inventory)
        self.assertTrue(
            any("unclassified Tennessee reference document" in e for e in errors)
        )

    def test_entity_encoded_token_source_fails_closed(self):
        sources = dict(self.sources)
        sources["encoded-market.html"] = (
            "<!doctype html><html><body>ACG serves Tennes&#115;ee.</body></html>"
        )
        errors, _ = guard.reference_inventory_violations(sources, self.inventory)
        self.assertTrue(
            any("unclassified Tennessee reference document" in e for e in errors)
        )

    def test_inline_fragmented_token_source_fails_closed(self):
        sources = dict(self.sources)
        sources["fragmented-market.html"] = (
            "<!doctype html><html><body>ACG serves Tennes<span>see</span>.</body></html>"
        )
        errors, _ = guard.reference_inventory_violations(sources, self.inventory)
        self.assertTrue(
            any("unclassified Tennessee reference document" in e for e in errors)
        )

    def test_jsonld_unicode_escape_token_source_fails_closed(self):
        sources = dict(self.sources)
        sources["encoded-schema.html"] = (
            r'<script type="application/ld+json">{"areaServed":"Tenn\u0065ssee"}</script>'
        )
        errors, _ = guard.reference_inventory_violations(sources, self.inventory)
        self.assertTrue(
            any("unclassified Tennessee reference document" in e for e in errors)
        )

    def test_css_generated_content_token_source_fails_closed(self):
        sources = dict(self.sources)
        sources["generated-market.html"] = (
            "<!doctype html><style>"
            ".market::after{content:'Tennes\\73 ee service';}"
            "</style><div class='market'></div>"
        )
        errors, _ = guard.reference_inventory_violations(sources, self.inventory)
        self.assertTrue(
            any("unclassified Tennessee reference document" in e for e in errors)
        )

    def test_css_attr_split_content_fails_closed(self):
        sources = dict(self.sources)
        sources["css-attr-market.html"] = (
            "<!doctype html><style>"
            ".market::after{content:attr(data-a)attr(data-b)}"
            "</style><div class='market' data-a='Tennes' data-b='see'></div>"
        )
        errors, _ = guard.reference_inventory_violations(sources, self.inventory)
        self.assertTrue(
            any("unclassified Tennessee reference document" in e for e in errors)
        )

    def test_external_css_attr_split_content_fails_closed(self):
        sources = dict(self.sources)
        sources["external-css-attr-market.html"] = (
            "<!doctype html><div class='market' "
            "data-a='Tennes' data-b='see'></div>"
        )
        css_sources = {
            "css/attr-market.css": (
                ".market::after{content:attr(data-a)attr(data-b)}"
            )
        }
        errors, _ = guard.reference_inventory_violations(
            sources, self.inventory, css_sources
        )
        self.assertTrue(
            any("unclassified Tennessee reference document" in e for e in errors)
        )

    def test_style_attribute_generated_content_fails_closed(self):
        sources = dict(self.sources)
        sources["generated-inline-market.html"] = (
            "<!doctype html><div style=\"content:'Tennes\\73 ee service'\"></div>"
        )
        errors, _ = guard.reference_inventory_violations(sources, self.inventory)
        self.assertTrue(
            any("unclassified Tennessee reference document" in e for e in errors)
        )

    def test_style_attribute_custom_property_fails_closed(self):
        sources = dict(self.sources)
        sources["generated-variable-market.html"] = (
            "<!doctype html><div style=\"--market:'Tennes\\73 ee service'\"></div>"
        )
        errors, _ = guard.reference_inventory_violations(sources, self.inventory)
        self.assertTrue(
            any("unclassified Tennessee reference document" in e for e in errors)
        )

    def test_inline_event_handler_escape_fails_closed(self):
        sources = dict(self.sources)
        sources["event-market.html"] = (
            r"<!doctype html><button onclick=\"this.textContent='Tenn\u0065ssee'\">"
            "Show market</button>"
        )
        errors, _ = guard.reference_inventory_violations(sources, self.inventory)
        self.assertTrue(
            any("unclassified Tennessee reference document" in e for e in errors)
        )

    def test_inline_script_split_string_fails_closed(self):
        sources = dict(self.sources)
        sources["script-market.html"] = (
            "<!doctype html><script>"
            "document.body.textContent='Tennes'+'see'"
            "</script>"
        )
        errors, _ = guard.reference_inventory_violations(sources, self.inventory)
        self.assertTrue(
            any("unclassified Tennessee reference document" in e for e in errors)
        )

    def test_inline_event_split_string_fails_closed(self):
        sources = dict(self.sources)
        sources["event-split-market.html"] = (
            "<!doctype html><button "
            "onclick=\"this.textContent='Tennes'+'see'\">Show</button>"
        )
        errors, _ = guard.reference_inventory_violations(sources, self.inventory)
        self.assertTrue(
            any("unclassified Tennessee reference document" in e for e in errors)
        )

    def test_inline_script_concat_call_fails_closed(self):
        sources = dict(self.sources)
        sources["script-concat-market.html"] = (
            "<!doctype html><script>"
            "document.body.textContent='Tennes'.concat('see')"
            "</script>"
        )
        errors, _ = guard.reference_inventory_violations(sources, self.inventory)
        self.assertTrue(
            any("unclassified Tennessee reference document" in e for e in errors)
        )

    def test_inline_script_character_codes_fail_closed(self):
        sources = dict(self.sources)
        sources["script-character-code-market.html"] = (
            "<!doctype html><script>"
            "document.body.textContent='Tennes'+"
            "String.fromCharCode(115,101,101)"
            "</script>"
        )
        errors, _ = guard.reference_inventory_violations(sources, self.inventory)
        self.assertTrue(
            any("unclassified Tennessee reference document" in e for e in errors)
        )

    def test_inline_script_template_interpolation_fails_closed(self):
        sources = dict(self.sources)
        sources["script-template-market.html"] = (
            "<!doctype html><script>"
            "document.body.textContent=`Tennes${'see'}`"
            "</script>"
        )
        errors, _ = guard.reference_inventory_violations(sources, self.inventory)
        self.assertTrue(
            any("unclassified Tennessee reference document" in e for e in errors)
        )

    def test_inline_event_template_interpolation_fails_closed(self):
        sources = dict(self.sources)
        sources["event-template-market.html"] = (
            "<!doctype html><button "
            "onclick=\"this.textContent=`Tennes${'see'}`\">Show</button>"
        )
        errors, _ = guard.reference_inventory_violations(sources, self.inventory)
        self.assertTrue(
            any("unclassified Tennessee reference document" in e for e in errors)
        )

    def test_template_empty_interpolation_fails_closed(self):
        sources = dict(self.sources)
        sources["script-empty-template-market.html"] = (
            "<!doctype html><script>"
            "document.body.textContent=`Tennes${''}see`"
            "</script>"
        )
        errors, _ = guard.reference_inventory_violations(sources, self.inventory)
        self.assertTrue(
            any("unclassified Tennessee reference document" in e for e in errors)
        )

    def test_template_static_variable_interpolation_fails_closed(self):
        sources = dict(self.sources)
        sources["script-variable-template-market.html"] = (
            "<!doctype html><script>"
            "const suffix='see';"
            "document.body.textContent=`Tennes${suffix}`"
            "</script>"
        )
        errors, _ = guard.reference_inventory_violations(sources, self.inventory)
        self.assertTrue(
            any("unclassified Tennessee reference document" in e for e in errors)
        )

    def test_external_css_generated_content_fails_closed(self):
        examples = (
            ".market::after{content:'Tennessee service';}",
            ".market::after{content:'Tennes\\73 ee service';}",
            ".market::after{content:'Tennes' 'see service';}",
            ":root{--market:'Tennes' 'see service';}"
            ".market::after{content:var(--market);}",
        )
        for source in examples:
            with self.subTest(source=source):
                self.assertTrue(
                    guard.external_css_generated_content_violations(
                        {"css/test.css": source}
                    )
                )

    def test_cross_file_css_custom_property_fails_closed(self):
        sources = {
            "css/tokens.css": ":root{--market:'Tennes\\73 ee service';}",
            "css/component.css": ".market::after{content:var(--market);}",
        }
        self.assertTrue(
            guard.external_css_generated_content_violations(sources)
        )

    def test_html_and_external_css_custom_properties_fail_closed(self):
        sources = dict(self.sources)
        sources["cross-surface-market.html"] = (
            "<!doctype html><div class='market' "
            "style=\"--a:'Tennes';--b:'see'\"></div>"
        )
        css_sources = {
            "css/cross-surface.css": (
                ".market::after{content:var(--a)var(--b)}"
            )
        }
        errors, _ = guard.reference_inventory_violations(
            sources, self.inventory, css_sources
        )
        self.assertTrue(
            any("unclassified Tennessee reference document" in e for e in errors)
        )

    def test_nested_external_css_custom_properties_fail_closed(self):
        sources = dict(self.sources)
        sources["nested-cross-surface-market.html"] = (
            "<!doctype html><div class='market' "
            "style=\"--a:'Tennes';--b:'see'\"></div>"
        )
        css_sources = {
            "css/nested-cross-surface.css": (
                ":root{--label:var(--a)var(--b)}"
                ".market::after{content:var(--label)}"
            )
        }
        errors, _ = guard.reference_inventory_violations(
            sources, self.inventory, css_sources
        )
        self.assertTrue(
            any("unclassified Tennessee reference document" in e for e in errors)
        )

    def test_external_css_comments_are_not_generated_content(self):
        source = ".market{color:red}/* content:'Tennessee service'; */"
        self.assertEqual(
            guard.external_css_generated_content_violations(
                {"css/test.css": source}
            ),
            [],
        )

    def test_layout_content_property_is_not_generated_content(self):
        source = ".market{align-content:'Tennessee service';}"
        self.assertEqual(
            list(guard.css_generated_content_values(source)),
            [],
        )

    def test_current_external_css_generated_content_is_clean(self):
        sources = {
            rel: Path(full).read_text(encoding="utf-8")
            for rel, full in guard.iter_css_files()
        }
        self.assertEqual(
            guard.external_css_generated_content_violations(sources),
            [],
        )

    def test_new_claim_on_classified_source_fails_surface_contract(self):
        sources = dict(self.sources)
        rel = "about.html"
        sources[rel] += (
            "\n<p>American Commercial Glass operates a Nashville office.</p>"
        )
        errors, _ = guard.reference_inventory_violations(sources, self.inventory)
        self.assertTrue(
            any(
                f"Tennessee reference surface changed for {rel}" in error
                for error in errors
            )
        )

    def test_distant_non_token_claim_change_fails_surface_contract(self):
        sources = dict(self.sources)
        rel = "acg-glass-florida/index.html"
        sources[rel] += (
            "\n<p>ACG opened another office and now serves more projects.</p>"
        )
        errors, _ = guard.reference_inventory_violations(sources, self.inventory)
        self.assertTrue(
            any(
                f"Tennessee reference surface changed for {rel}" in error
                for error in errors
            )
        )

    def test_surface_digest_excludes_css_but_includes_copy(self):
        first = "<style>.x{color:red}</style><p>Tennessee reference</p>"
        css_change = "<style>.x{color:blue}</style><p>Tennessee reference</p>"
        copy_change = "<style>.x{color:red}</style><p>Tennessee service claim</p>"
        self.assertEqual(
            guard.reference_surface_digest(first),
            guard.reference_surface_digest(css_change),
        )
        self.assertNotEqual(
            guard.reference_surface_digest(first),
            guard.reference_surface_digest(copy_change),
        )

    def test_surface_digest_includes_metadata_identity_attributes(self):
        pairs = (
            (
                '<meta name="description" content="same">',
                '<meta name="keywords" content="same">',
            ),
            (
                '<meta property="og:title" content="same">',
                '<meta property="og:description" content="same">',
            ),
            (
                '<link rel="canonical" href="/same">',
                '<link rel="alternate" href="/same">',
            ),
            (
                '<link rel="alternate" hreflang="en" href="/same">',
                '<link rel="alternate" hreflang="es" href="/same">',
            ),
            (
                '<script type="application/ld+json">same</script>',
                '<script type="text/javascript">same</script>',
            ),
        )
        for first, second in pairs:
            with self.subTest(first=first):
                self.assertNotEqual(
                    guard.reference_surface_digest(first),
                    guard.reference_surface_digest(second),
                )

    def test_surface_digest_includes_inline_event_handlers(self):
        first = '<button onclick="this.textContent=\'four offices\'">Show</button>'
        second = '<button onclick="this.textContent=\'three offices\'">Show</button>'
        self.assertNotEqual(
            guard.reference_surface_digest(first),
            guard.reference_surface_digest(second),
        )

    def test_new_path_discovery_source_fails_closed(self):
        sources = dict(self.sources)
        sources["nashville-new.html"] = (
            "<!doctype html><html><head><title>New market</title></head></html>"
        )
        errors, _ = guard.reference_inventory_violations(sources, self.inventory)
        self.assertTrue(
            any("unclassified path or title discovery source" in e for e in errors)
        )

    def test_fragment_exclusion_cannot_hide_a_document(self):
        sources = dict(self.sources)
        rel = "services-schema-block.html"
        sources[rel] = "<!doctype html><html>" + sources[rel]
        errors, _ = guard.reference_inventory_violations(sources, self.inventory)
        self.assertTrue(
            any("excluded fragment looks like a standalone document" in e for e in errors)
        )

    def test_excluded_fragment_surface_is_exact(self):
        sources = dict(self.sources)
        rel = "services-schema-block.html"
        sources[rel] = sources[rel].replace(
            "Tennessee climate zones",
            "changed Tennessee climate zones",
            1,
        )
        errors, _ = guard.reference_inventory_violations(sources, self.inventory)
        self.assertTrue(
            any(f"excluded fragment surface changed for {rel}" in e for e in errors)
        )

    def test_reference_groups_cannot_overlap(self):
        inventory = copy.deepcopy(self.inventory)
        duplicate = inventory["reference_groups"]["biography_only"][0]
        inventory["reference_groups"]["technical_or_market_review"].append(duplicate)
        inventory["reference_groups"]["technical_or_market_review"].sort()
        errors, _ = guard.reference_inventory_violations(self.sources, inventory)
        self.assertIn(
            "a document source appears in more than one reference group",
            errors,
        )

    def test_reference_group_membership_cannot_be_swapped(self):
        inventory = copy.deepcopy(self.inventory)
        groups = inventory["reference_groups"]
        stale = "acg-glass-florida/index.html"
        biography = "about.html"
        groups["stale_operating_claim_hold"].remove(stale)
        groups["stale_operating_claim_hold"].append(biography)
        groups["stale_operating_claim_hold"].sort()
        groups["biography_only"].remove(biography)
        groups["biography_only"].append(stale)
        groups["biography_only"].sort()
        errors, _ = guard.reference_inventory_violations(self.sources, inventory)
        self.assertTrue(
            any("membership differs from the governed baseline" in e for e in errors)
        )

    def test_expected_counts_are_fail_closed(self):
        inventory = copy.deepcopy(self.inventory)
        inventory["expected_counts"]["document_sources"] += 1
        errors, _ = guard.reference_inventory_violations(self.sources, inventory)
        self.assertTrue(
            any("expected_counts.document_sources" in e for e in errors)
        )


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
                "acg-vs-giroux-glass.html",
                "acg-vs-harmon.html",
                "acg-vs-permasteelisa.html",
                "ask.html",
                "best-glazing-subcontractor-florida.html",
                "best-storefront-contractor-florida.html",
                "blog/florida-commercial-construction-2026-outlook.html",
                "commercial-storefront-installer-florida.html",
                "facts.html",
                "glass-canopies-commercial.html",
                "glazing-subcontractor-vs-general-contractor.html",
                "industries.html",
                "locations.html",
                "miami-hvhz-glazing-contractor.html",
                "restaurant-glazing-contractor.html",
                "security-window-film-retrofit.html",
                "service-areas-map/index.html",
            ),
        )

    def test_exact_governed_asset_set(self):
        self.assertEqual(
            guard.STALE_OPERATING_CLAIM_ASSETS,
            ("images/acg-coverage-map.svg",),
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

    def test_southeast_florida_region_label_is_preserved(self):
        self.assertEqual(
            self.scoped_violations("locations.html", "Southeast Florida"),
            [],
        )

    def test_southeast_market_claim_is_not_exempted(self):
        self.assertTrue(
            self.scoped_violations(
                "locations.html",
                "Select Southeast markets are bid through GC relationships.",
            )
        )

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

    def test_current_governed_assets_have_no_stale_operating_language(self):
        root = SCRIPTS_DIR.parents[1]
        for rel in guard.STALE_OPERATING_CLAIM_ASSETS:
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


# ---------------------------------------------------------------------------
# Prohibited public-positioning coverage (Regexes A - E)
#
# Each test drives check_prohibited_public_positioning directly against a
# synthetic HTML fixture built inline - no bad HTML is ever committed to
# disk. Fixtures embed the offending claim in the metadata surface the rule
# is supposed to catch (title, meta description, og/twitter, JSON-LD, inline
# script, body) so each surface is exercised.
# ---------------------------------------------------------------------------


def _positioning_violations(html: str, rel: str = "page.html"):
    fails: list[str] = []
    warns: list[str] = []
    guard.check_prohibited_public_positioning(
        rel,
        html,
        lambda path, msg: fails.append(msg),
        warn=lambda path, msg: warns.append(msg),
    )
    return fails, warns


class ProhibitedPublicPositioningTests(unittest.TestCase):
    def test_ai_augmented_is_flagged_in_body(self):
        fails, _ = _positioning_violations(
            "<html><body><p>ACG is an AI-augmented glazing contractor.</p></body></html>"
        )
        self.assertTrue(any("AI-augmented" in m for m in fails))

    def test_ai_augmented_variant_with_space_is_flagged(self):
        fails, _ = _positioning_violations(
            "<html><body><p>Our AI augmented estimating engine.</p></body></html>"
        )
        self.assertTrue(any("AI-augmented" in m for m in fails))

    def test_ai_augmented_inside_title_is_flagged(self):
        fails, _ = _positioning_violations(
            "<html><head><title>AI-Augmented Glazing | ACG</title></head></html>"
        )
        self.assertTrue(any("AI-augmented" in m for m in fails))

    def test_wbe_certified_without_qualifier_is_flagged(self):
        fails, _ = _positioning_violations(
            "<html><body><p>ACG is WBE certified and serves projects statewide.</p></body></html>"
        )
        self.assertTrue(any("WBE certified" in m for m in fails))

    def test_wbenc_certified_without_qualifier_is_flagged(self):
        fails, _ = _positioning_violations(
            "<html><body><p>WBENC certified glazing subcontractor.</p></body></html>"
        )
        self.assertTrue(any("WBE certified" in m for m in fails))

    def test_wbe_certified_with_in_progress_is_ok(self):
        fails, _ = _positioning_violations(
            "<html><body><p>ACG's WBE certified in progress; expected 2027.</p></body></html>"
        )
        self.assertEqual([m for m in fails if "WBE certified" in m], [])

    def test_wbe_certified_with_pending_is_ok(self):
        fails, _ = _positioning_violations(
            "<html><body><p>Woman-owned certified, pending WBENC review.</p></body></html>"
        )
        self.assertEqual([m for m in fails if "WBE certified" in m], [])

    def test_wbe_certified_with_filed_is_ok(self):
        fails, _ = _positioning_violations(
            "<html><body><p>WBENC certified; application filed with the council.</p></body></html>"
        )
        self.assertEqual([m for m in fails if "WBE certified" in m], [])

    def test_authorized_dealer_heading_is_flagged(self):
        fails, _ = _positioning_violations(
            "<html><body><div>Authorized Dealer For</div>"
            "<div>ESWindows &middot; Euro-Wall &middot; PGT</div></body></html>"
        )
        self.assertTrue(any("authorized dealer" in m.lower() for m in fails))

    def test_authorized_dealer_for_manufacturer_is_flagged(self):
        fails, _ = _positioning_violations(
            "<html><body><p>We are an authorized dealer for ESWindows.</p></body></html>"
        )
        self.assertTrue(any("authorized dealer" in m.lower() for m in fails))

    def test_we_are_an_authorized_dealer_is_flagged(self):
        fails, _ = _positioning_violations(
            "<html><body><p>Come to ACG - we are an authorized dealer.</p></body></html>"
        )
        self.assertTrue(any("authorized dealer" in m.lower() for m in fails))

    def test_editorial_authorized_dealer_plural_is_not_flagged(self):
        html = (
            "<html><body><p>Ask specifically which manufacturers they are "
            "authorized dealers for, and verify it if the answer matters to "
            "your spec.</p></body></html>"
        )
        fails, _ = _positioning_violations(html)
        self.assertEqual([m for m in fails if "authorized dealer" in m.lower()], [])

    def test_editorial_authorized_dealers_get_is_not_flagged(self):
        html = (
            "<html><body><p>Why does this matter? Authorized dealers get direct "
            "technical support from the manufacturer.</p></body></html>"
        )
        fails, _ = _positioning_violations(html)
        self.assertEqual([m for m in fails if "authorized dealer" in m.lower()], [])

    def test_completed_federal_work_is_flagged(self):
        fails, _ = _positioning_violations(
            "<html><body><p>ACG has completed federal glazing projects in the region.</p></body></html>"
        )
        self.assertTrue(any("federal" in m for m in fails))

    def test_awarded_gsa_is_flagged(self):
        fails, _ = _positioning_violations(
            "<html><body><p>ACG was awarded GSA contracts last year.</p></body></html>"
        )
        self.assertTrue(any("federal" in m for m in fails))

    def test_delivered_usace_is_flagged(self):
        fails, _ = _positioning_violations(
            "<html><body><p>Delivered USACE glazing packages on schedule.</p></body></html>"
        )
        self.assertTrue(any("federal" in m for m in fails))

    def test_tn_office_opening_in_title_of_indexable_page_fails(self):
        html = (
            "<!doctype html><html><head>"
            "<title>Nashville Office Opening Q3 2026 | ACG</title>"
            "</head><body><p>Body.</p></body></html>"
        )
        fails, warns = _positioning_violations(html)
        self.assertTrue(any("office-opening" in m for m in fails))
        self.assertEqual([m for m in warns if "office-opening" in m], [])

    def test_tn_office_opening_in_meta_description_of_indexable_page_fails(self):
        html = (
            "<!doctype html><html><head>"
            "<meta name=\"description\" content=\"Nashville office opening Q3 2026.\">"
            "</head><body></body></html>"
        )
        fails, _ = _positioning_violations(html)
        self.assertTrue(any("office-opening" in m for m in fails))

    def test_tn_office_opening_in_og_description_of_indexable_page_fails(self):
        html = (
            "<!doctype html><html><head>"
            "<meta property=\"og:description\" content=\"Coming to Nashville soon.\">"
            "</head><body></body></html>"
        )
        fails, _ = _positioning_violations(html)
        self.assertTrue(any("office-opening" in m for m in fails))

    def test_tn_office_opening_in_jsonld_of_indexable_page_fails(self):
        html = (
            "<!doctype html><html><head>"
            "<script type=\"application/ld+json\">"
            "{\"@type\":\"FAQPage\",\"mainEntity\":[{\"name\":\"When is ACG's "
            "Nashville office opening?\"}]}"
            "</script></head><body></body></html>"
        )
        fails, _ = _positioning_violations(html)
        self.assertTrue(any("office-opening" in m for m in fails))

    def test_tn_office_opening_in_inline_script_of_indexable_page_fails(self):
        html = (
            "<!doctype html><html><head>"
            "<script>var msg = 'Nashville office opens Q3 2026';</script>"
            "</head><body></body></html>"
        )
        fails, _ = _positioning_violations(html)
        self.assertTrue(any("office-opening" in m for m in fails))

    def test_tn_office_opening_on_noindex_page_warns_not_fails(self):
        html = (
            "<!doctype html><html><head>"
            "<meta name=\"robots\" content=\"noindex,follow\">"
            "<title>Nashville Office Opens Q3 2026 | ACG</title>"
            "</head><body></body></html>"
        )
        fails, warns = _positioning_violations(html)
        self.assertEqual([m for m in fails if "office-opening" in m], [])
        self.assertTrue(any("office-opening" in m for m in warns))

    def test_expanding_to_nashville_variant_is_caught(self):
        html = (
            "<!doctype html><html><head><title>ACG</title></head>"
            "<body><p>ACG is expanding to Nashville next year.</p></body></html>"
        )
        fails, _ = _positioning_violations(html)
        self.assertTrue(any("office-opening" in m for m in fails))

    def test_expansion_governed_qualifier_is_not_flagged(self):
        # "expansion evaluated / off the table / not active" documents that the
        # plan is withdrawn and must not trip the guard.
        for qualifier in (
            "expansion evaluated",
            "expansion off the table",
            "expansion not active",
        ):
            with self.subTest(qualifier=qualifier):
                html = (
                    "<!doctype html><html><body><p>Tennessee "
                    f"{qualifier}; no ACG office.</p></body></html>"
                )
                fails, warns = _positioning_violations(html)
                self.assertEqual([m for m in fails if "office-opening" in m], [])
                self.assertEqual([m for m in warns if "office-opening" in m], [])

    # ------------------------------------------------------------------
    # Regex E false-positive regression tests.
    #
    # The first cut of Regex E carried a bare "expansion" alternative that
    # fired on any "expansion" token within 80 characters of a Tennessee place
    # name. Both phrases below are verbatim from the repo and are third-party /
    # market-observation uses, not ACG claims. They must never be flagged, and
    # they are fixed in the regex rather than in the allowlist so the whole
    # class of false positive is gone.
    # ------------------------------------------------------------------

    def test_third_party_airport_expansion_is_not_flagged(self):
        # acoustic-glazing-stc-oitc-commercial.html - the AIRPORT is expanding.
        html = (
            "<!doctype html><html><body><div class=\"prose rv\"><p>Acoustic "
            "glazing shows up most often on projects where exterior noise is a "
            "known, named problem at the design stage, and healthcare or "
            "education buildings where interior sound isolation is part of the "
            "program. Nashville's BNA airport expansion is a regional example "
            "of the demand - the on-site Hilton at BNA was specified with "
            "triple-pane acoustical windows.</p></div></body></html>"
        )
        fails, warns = _positioning_violations(html)
        self.assertEqual([m for m in fails if "office-opening" in m], [])
        self.assertEqual([m for m in warns if "office-opening" in m], [])

    def test_blog_card_market_observation_expansion_is_not_flagged(self):
        # blog/index.html - a blog card description framing market observations.
        html = (
            "<!doctype html><html><body><h3>Florida Commercial Construction "
            "2026 Outlook</h3><p>What the 2026 Florida commercial construction "
            "market looks like from inside a 350-project glazing contractor. "
            "Restaurant, hotel, office, medical, and Tennessee expansion "
            "observations.</p></body></html>"
        )
        fails, warns = _positioning_violations(html)
        self.assertEqual([m for m in fails if "office-opening" in m], [])
        self.assertEqual([m for m in warns if "office-opening" in m], [])

    def test_bare_third_party_expansion_nouns_are_not_flagged(self):
        # Same class of false positive: someone else's project expanding.
        for phrase in (
            "Sumner Regional Medical Center expansion, charter schools, and "
            "grocery-anchored retail are the dominant Nashville project types.",
            "Nashville leads it - corporate campuses, hotels, multifamily "
            "towers, and healthcare expansion are all going vertical at once.",
            "Each state is unlocked by the Tennessee license, making the "
            "expansion efficient rather than 5 separate applications.",
            "The Tennessee stadium expansion broke ground in March.",
        ):
            with self.subTest(phrase=phrase):
                html = f"<!doctype html><html><body><p>{phrase}</p></body></html>"
                fails, warns = _positioning_violations(html)
                self.assertEqual([m for m in fails if "office-opening" in m], [])
                self.assertEqual([m for m in warns if "office-opening" in m], [])

    # ------------------------------------------------------------------
    # Regex E must still catch genuine first-party ACG expansion claims.
    # ------------------------------------------------------------------

    def test_acg_is_expanding_into_tennessee_is_flagged(self):
        html = (
            "<!doctype html><html><body><p>ACG is expanding into Tennessee "
            "to serve Middle TN general contractors.</p></body></html>"
        )
        fails, _ = _positioning_violations(html)
        self.assertTrue(any("office-opening" in m for m in fails))

    def test_our_tennessee_expansion_is_flagged(self):
        html = (
            "<!doctype html><html><body><p>Read more about our Tennessee "
            "expansion and what it means for your project.</p></body></html>"
        )
        fails, _ = _positioning_violations(html)
        self.assertTrue(any("office-opening" in m for m in fails))

    def test_expanding_to_nashville_with_quarter_is_flagged(self):
        html = (
            "<!doctype html><html><head>"
            "<meta name=\"description\" content=\"Expanding to Nashville in "
            "Q3 2026.\"></head><body></body></html>"
        )
        fails, _ = _positioning_violations(html)
        self.assertTrue(any("office-opening" in m for m in fails))

    def test_new_nashville_office_opening_is_flagged(self):
        html = (
            "<!doctype html><html><body><h2>New Nashville office opening</h2>"
            "</body></html>"
        )
        fails, _ = _positioning_violations(html)
        self.assertTrue(any("office-opening" in m for m in fails))

    def test_first_person_and_full_company_expansion_claims_are_flagged(self):
        for phrase in (
            "American Commercial Glass is expanding into Tennessee this year.",
            "ACG's Tennessee expansion begins in the spring.",
            "We are planning our expansion into Nashville.",
            "We're opening a Nashville office in the fall.",
            "Our new Nashville branch launches early 2027.",
            "Our Nashville location opens Q3 2026.",
        ):
            with self.subTest(phrase=phrase):
                html = f"<!doctype html><html><body><p>{phrase}</p></body></html>"
                fails, _ = _positioning_violations(html)
                self.assertTrue(
                    any("office-opening" in m for m in fails),
                    f"genuine ACG expansion claim not flagged: {phrase}",
                )

    def test_genuine_claim_still_only_warns_on_a_noindex_page(self):
        html = (
            "<!doctype html><html><head>"
            "<meta name=\"robots\" content=\"noindex,follow\">"
            "<title>Our Tennessee expansion | ACG</title>"
            "</head><body></body></html>"
        )
        fails, warns = _positioning_violations(html)
        self.assertEqual([m for m in fails if "office-opening" in m], [])
        self.assertTrue(any("office-opening" in m for m in warns))


class RegexEExpansionBindingTests(unittest.TestCase):
    """Direct assertions on TN_OFFICE_OPENING_RE, independent of surfaces.

    These pin the structural rule: an expansion term is a claim only when it is
    bound to an ACG / first-person subject, is inherently directional, or sits
    next to an office/location opening term.
    """

    FALSE_POSITIVES = (
        "Nashville's BNA airport expansion is a regional example of the demand",
        "Restaurant, hotel, office, medical, and Tennessee expansion observations.",
        "Sumner Regional Medical Center expansion near Nashville Pike",
        "healthcare expansion is going vertical across Nashville",
        "the Tennessee license, making the expansion efficient",
    )

    GENUINE_CLAIMS = (
        "ACG is expanding into Tennessee",
        "our Tennessee expansion",
        "expanding to Nashville in Q3 2026",
        "new Nashville office opening",
        "American Commercial Glass is expanding into Tennessee",
        "ACG's Tennessee expansion begins in the spring",
        "We are opening a Nashville office",
        "Our Nashville location opens Q3 2026",
    )

    def test_bare_expansion_no_longer_matches(self):
        for phrase in self.FALSE_POSITIVES:
            with self.subTest(phrase=phrase):
                self.assertIsNone(
                    guard.TN_OFFICE_OPENING_RE.search(phrase),
                    f"regex E still fires on a third-party expansion: {phrase}",
                )

    def test_subject_bound_expansion_still_matches(self):
        for phrase in self.GENUINE_CLAIMS:
            with self.subTest(phrase=phrase):
                self.assertIsNotNone(
                    guard.TN_OFFICE_OPENING_RE.search(phrase),
                    f"regex E no longer catches a genuine claim: {phrase}",
                )

    def test_governed_withdrawal_language_never_matches(self):
        for phrase in (
            "our Tennessee expansion evaluated and closed",
            "ACG Tennessee expansion off the table",
            "our Nashville expansion not active",
        ):
            with self.subTest(phrase=phrase):
                self.assertIsNone(guard.TN_OFFICE_OPENING_RE.search(phrase))

    def test_no_allowlist_class_exists_for_regex_e(self):
        # The two false positives above are fixed structurally, so no page-level
        # exemption is needed. Guard against a regression that re-adds one.
        #
        # This used to assert the whole allowlist file was empty, which was true
        # only because nothing had ever been exempted. Regex C now carries
        # entries (spec-section requirement text and the byte-frozen West Palm
        # Beach pages), so the assertion is narrowed to its actual intent: regex
        # E must still have no exemption class of its own.
        loaded = guard.load_claim_guard_allowlist()
        self.assertEqual(
            sorted(k for k in loaded if not k.startswith("_")),
            ["authorized_dealer_editorial", "schema_version"],
        )
        for key in loaded:
            self.assertNotIn("expansion", key)
            self.assertNotIn("office", key)


class NoindexDetectionTests(unittest.TestCase):
    def test_noindex_meta_is_detected(self):
        self.assertTrue(
            guard.has_noindex_directive(
                '<meta name="robots" content="noindex,follow">'
            )
        )
        self.assertTrue(
            guard.has_noindex_directive(
                '<meta name="googlebot" content="noindex">'
            )
        )

    def test_index_page_is_not_detected_as_noindex(self):
        self.assertFalse(
            guard.has_noindex_directive('<meta name="robots" content="index,follow">')
        )
        self.assertFalse(guard.has_noindex_directive("<html><body></body></html>"))


class ClaimGuardAllowlistTests(unittest.TestCase):
    def test_missing_file_returns_empty_allowlist(self):
        # Point at a path that doesn't exist; guard must not raise.
        empty = guard.load_claim_guard_allowlist(
            path=str(SCRIPTS_DIR / "claim-guard-allowlist-DOES-NOT-EXIST.json")
        )
        self.assertEqual(empty.get("authorized_dealer_editorial", {}), {})

    def test_repo_allowlist_loads(self):
        loaded = guard.load_claim_guard_allowlist()
        self.assertEqual(loaded.get("schema_version"), 1)
        self.assertIsInstance(
            loaded.get("authorized_dealer_editorial", {}), dict
        )

    def test_block_hash_allowlist_exempts_matching_authorized_dealer_block(self):
        html = (
            "<html><body><div>Authorized Dealer For</div>"
            "<span>ESWindows</span></body></html>"
        )
        # First discover the block hash the guard would compute.
        m = guard.AUTHORIZED_DEALER_RE.search(html)
        self.assertIsNotNone(m)
        block_hash = guard._authorized_dealer_block_hash(html, m)
        allowlist = {"authorized_dealer_editorial": {"page.html": [block_hash]}}
        fails: list[str] = []
        guard.check_prohibited_public_positioning(
            "page.html", html, lambda p, msg: fails.append(msg), allowlist=allowlist
        )
        self.assertEqual([m for m in fails if "authorized dealer" in m.lower()], [])

    def test_allowlist_only_exempts_the_named_relpath(self):
        html = (
            "<html><body><div>Authorized Dealer For</div>"
            "<span>ESWindows</span></body></html>"
        )
        m = guard.AUTHORIZED_DEALER_RE.search(html)
        block_hash = guard._authorized_dealer_block_hash(html, m)
        allowlist = {
            "authorized_dealer_editorial": {
                "blog/some-other-page.html": [block_hash]
            }
        }
        fails: list[str] = []
        guard.check_prohibited_public_positioning(
            "commercial-glazing-west-palm-beach.html",
            html,
            lambda p, msg: fails.append(msg),
            allowlist=allowlist,
        )
        self.assertTrue(any("authorized dealer" in m.lower() for m in fails))


# ---------------------------------------------------------------------------
# Regex C - first-party manufacturer-authorization claims, any noun.
#
# The rule used to match the literal word "dealer" only. The site said
# "authorized installer", "authorized partner", carried bare "Authorized" card
# labels and "Manufacturer-authorized only", so roughly 90 files asserted an
# undocumentable manufacturer grant and still passed. These tests pin the
# noun-agnostic behaviour AND the editorial phrasings that must keep passing.
# ---------------------------------------------------------------------------


def _authorization_fails(html: str, rel: str = "page.html", allowlist=None):
    fails: list[str] = []
    guard.check_prohibited_public_positioning(
        rel, html, lambda path, msg: fails.append(msg), allowlist=allowlist
    )
    return [m for m in fails if "manufacturer-authorization claim" in m]


class AuthorizationClaimNounCoverageTests(unittest.TestCase):
    """Positive controls: one per noun, plus the label and adjective forms."""

    def test_every_relationship_noun_is_caught_with_an_acg_subject(self):
        for noun in ("installer", "dealer", "distributor", "partner",
                     "reseller", "fabricator"):
            html = (
                "<html><body><p>ACG is an authorized Euro-Wall commercial "
                f"{noun} in Florida.</p></body></html>"
            )
            with self.subTest(noun=noun):
                self.assertTrue(_authorization_fails(html), noun)

    def test_plural_noun_with_first_party_subject_is_caught(self):
        html = (
            "<html><body><p>ACG installs commercial storefront in Orlando from "
            "its seven authorized manufacturer partners.</p></body></html>"
        )
        self.assertTrue(_authorization_fails(html))

    def test_we_are_an_authorized_installer_is_caught(self):
        html = (
            "<html><body><p>We are an authorized commercial installer for "
            "ESWindows and Euro-Wall.</p></body></html>"
        )
        self.assertTrue(_authorization_fails(html))

    def test_hyphenated_authorized_installer_status_is_caught(self):
        html = (
            "<html><body><p>American Commercial Glass holds authorized-installer "
            "status with Euro-Wall Systems.</p></body></html>"
        )
        self.assertTrue(_authorization_fails(html))

    def test_bare_authorized_card_label_is_caught(self):
        html = '<html><body><div class="card-num">Authorized</div></body></html>'
        self.assertTrue(_authorization_fails(html))

    def test_authorized_label_with_trailing_punctuation_is_caught(self):
        html = "<html><body><h2>Authorized. <span>Certified.</span></h2></body></html>"
        self.assertTrue(_authorization_fails(html))

    def test_authorized_heading_with_manufacturer_is_caught(self):
        html = "<html><body><h4>Authorized ESWindows &amp; Euro-Wall</h4></body></html>"
        self.assertTrue(_authorization_fails(html))

    def test_manufacturer_authorized_adjective_is_caught(self):
        html = "<html><body><p>Manufacturer-authorized only.</p></body></html>"
        self.assertTrue(_authorization_fails(html))

    def test_is_an_authorized_named_manufacturer_is_caught(self):
        html = (
            "<html><body><p>Yes. Because ACG is an authorized Euro-Wall Florida "
            "installer, the manufacturer warranty is intact.</p></body></html>"
        )
        self.assertTrue(_authorization_fails(html))

    def test_claim_is_caught_in_metadata_and_json_ld_surfaces(self):
        title = (
            "<html><head><title>Authorized Euro-Wall Commercial Installer (USA) "
            "| ACG</title></head></html>"
        )
        meta = (
            '<html><head><meta name="description" content="ACG is an authorized '
            'Euro-Wall commercial installer (USA)."></head></html>'
        )
        jsonld = (
            '<html><head><script type="application/ld+json">{"@type": "Answer", '
            '"text": "American Commercial Glass is an authorized Euro-Wall '
            'commercial installer serving the USA."}</script></head></html>'
        )
        for surface, html in (("title", title), ("meta", meta), ("json-ld", jsonld)):
            with self.subTest(surface=surface):
                self.assertTrue(_authorization_fails(html), surface)


class AuthorizationClaimEditorialTests(unittest.TestCase):
    """Negative controls: third-party / editorial / denial phrasing must pass."""

    def test_plural_editorial_advice_is_not_a_first_party_claim(self):
        html = (
            "<html><body><p>Ask specifically which manufacturers they are "
            "authorized dealers for, and verify it if the answer matters to your "
            "spec.</p></body></html>"
        )
        self.assertEqual(_authorization_fails(html), [])

    def test_generic_benefit_statement_about_dealers_passes(self):
        html = (
            "<html><body><p>Authorized dealers get direct technical support and "
            "priority production slots.</p></body></html>"
        )
        self.assertEqual(_authorization_fails(html), [])

    def test_warranty_precondition_advice_passes(self):
        html = (
            "<html><body><p>Most premium glazing systems - ESWindows, Euro-Wall, "
            "PGT, TGP - require authorized-installer status as a warranty "
            "precondition.</p></body></html>"
        )
        self.assertEqual(_authorization_fails(html), [])

    def test_third_party_firm_phrasing_passes(self):
        html = (
            "<html><body><p>Authorization is not transferable: a firm that is "
            "authorized on ESWindows ES-50 storefront is not automatically "
            "authorized on ES-70 curtain wall.</p></body></html>"
        )
        self.assertEqual(_authorization_fails(html), [])

    def test_manufacturer_authorization_letters_advice_passes(self):
        html = (
            "<html><body><p>Confirm bonding capacity, manufacturer authorization "
            "letters, and AAMA InstallationMasters training.</p></body></html>"
        )
        self.assertEqual(_authorization_fails(html), [])

    def test_change_order_authorization_passes(self):
        html = (
            "<html><body><p>Documented change orders keep added glazing work "
            "properly priced and authorized before it proceeds.</p></body></html>"
        )
        self.assertEqual(_authorization_fails(html), [])

    def test_explicit_denial_passes(self):
        denials = (
            "<html><body><p>ACG also installs and coordinates PGT, Allegion, TGP, "
            "Slimpact, and Aldora systems; ACG does not hold authorized-installer "
            "status for those brands.</p></body></html>",
            "<html><body><p>We install these products; we do not claim "
            "authorized-dealer status for them.</p></body></html>",
        )
        for html in denials:
            with self.subTest(html=html[:60]):
                self.assertEqual(_authorization_fails(html), [])

    def test_denial_cannot_launder_a_separate_claim_in_the_next_sentence(self):
        html = (
            "<html><body><p>ACG does not claim certification. ACG is an "
            "authorized Euro-Wall installer.</p></body></html>"
        )
        self.assertTrue(_authorization_fails(html))

    def test_factual_installer_list_passes(self):
        html = (
            "<html><body><p>Installer for ESWindows (Tecnoglass), Euro-Wall, PGT "
            "Innovations, Allegion, TGP, Slimpact, and Aldora. Direct factory "
            "engineering support.</p></body></html>"
        )
        self.assertEqual(_authorization_fails(html), [])

    def test_scrubbed_replacement_copy_passes(self):
        html = (
            "<html><body>"
            '<div class="card-num">Product Lines</div>'
            "<p>Do you install ESWindows and Euro-Wall systems?</p>"
            "<p>Yes. ACG installs ESWindows (Tecnoglass) and Euro-Wall systems on "
            "commercial projects across Florida, with direct factory engineering "
            "support.</p>"
            "<h4>ESWindows &amp; Euro-Wall Systems</h4>"
            "<p>Manufacturer systems only.</p>"
            "</body></html>"
        )
        self.assertEqual(_authorization_fails(html), [])


class AuthorizationClaimAllowlistTests(unittest.TestCase):
    def test_block_hash_allowlist_still_exempts_an_installer_class_block(self):
        html = (
            "<html><body><p>B. Installer: Manufacturer-authorized; minimum 5 "
            "installations of similar size in Florida.</p></body></html>"
        )
        self.assertTrue(_authorization_fails(html))
        m = guard.AUTHORIZED_DEALER_RE.search(html)
        block_hash = guard._authorized_dealer_block_hash(html, m)
        allowlist = {"authorized_dealer_editorial": {"spec.html": [block_hash]}}
        self.assertEqual(
            _authorization_fails(html, rel="spec.html", allowlist=allowlist), []
        )
        # Same block, different page: still a violation.
        self.assertTrue(
            _authorization_fails(html, rel="other.html", allowlist=allowlist)
        )

    def test_repo_allowlist_entries_are_all_live(self):
        """Every allowlisted hash must still match a block in its file.

        A stale entry means the copy changed and the exemption should have been
        deleted with it.
        """
        allowlist = guard.load_claim_guard_allowlist()
        repo_root = Path(guard.REPO_ROOT)
        for rel, hashes in allowlist["authorized_dealer_editorial"].items():
            path = repo_root / rel
            self.assertTrue(path.exists(), rel)
            html = path.read_text(encoding="utf-8")
            live = set()
            for rx in (guard.AUTHORIZED_DEALER_RE, guard.AUTHORIZED_LABEL_RE):
                for m in rx.finditer(html):
                    live.add(guard._authorized_dealer_block_hash(html, m))
            for h in hashes:
                with self.subTest(rel=rel, block_hash=h[:12]):
                    self.assertIn(h, live)


class AuthorizationClaimSiteScanTests(unittest.TestCase):
    def test_tracked_html_carries_no_unexempted_authorization_claim(self):
        """Negative control for the scrub itself.

        This is the check that fails on the pre-scrub content and passes after
        it, without needing the full guard run.
        """
        allowlist = guard.load_claim_guard_allowlist()
        offenders = []
        for rel, full in guard.iter_html_files():
            with open(full, encoding="utf-8") as fh:
                html = fh.read()
            if _authorization_fails(html, rel=rel, allowlist=allowlist):
                offenders.append(rel)
        self.assertEqual(offenders, [])


if __name__ == "__main__":
    unittest.main()
