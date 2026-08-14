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

    def test_exact_projects_claim_is_held_by_context_fingerprint(self):
        root = SCRIPTS_DIR.parents[1]
        source = (root / "projects/index.html").read_text(encoding="utf-8")
        self.assertEqual(violations(source, "projects/index.html"), [])

    def test_held_projects_claim_fails_if_context_changes(self):
        root = SCRIPTS_DIR.parents[1]
        source = (root / "projects/index.html").read_text(encoding="utf-8")
        changed = source.replace("Tennessee from Q3 2026", "Tennessee from Q4 2026")
        self.assertEqual(len(violations(changed, "projects/index.html")), 1)

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
                "document_sources": 151,
                "path_or_title_discovery": 73,
                "outside_discovery": 78,
                "known_edge_301_sources": 4,
                "document_sources_excluding_recorded_edge_sources": 147,
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


if __name__ == "__main__":
    unittest.main()
