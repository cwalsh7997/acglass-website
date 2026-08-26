#!/usr/bin/env python3
"""Tests for the site-root semantic freeze in canonical-verify.py.

The dedicated West Palm Beach pages are byte-frozen and need no tests here: a
byte comparison cannot be subtly wrong, and `test_wpb_pages_stay_byte_frozen`
below is enough to catch someone quietly moving one into the semantic mode.

The root is different. It is frozen field by field so that ordinary body work
can continue during a freeze with no end date, which means the freeze is only
as good as its field extraction. So every protected field gets a negative test
proving an altered value is actually caught, and the permitted case gets a
positive test proving the gate is not a byte freeze wearing a new name.

Run:  python3 -m unittest discover -s .github/scripts/tests -t .github/scripts/tests -v
"""

from __future__ import annotations

import importlib.util
import json
import unittest
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parents[1]
REPO_ROOT = SCRIPTS_DIR.parents[1]


def _load_verifier():
    # The script is hyphenated, so it is not importable by name.
    spec = importlib.util.spec_from_file_location(
        "canonical_verify", SCRIPTS_DIR / "canonical-verify.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


cv = _load_verifier()
REGISTRY = json.loads((REPO_ROOT / ".github" / "seo" / "url-primaries.json").read_text())
SEMANTIC = REGISTRY["semantic_freeze"]
ROOT_SPEC = SEMANTIC["/"]
PROTECTED = list(ROOT_SPEC["protected_fields"])
BYTE_FROZEN = {cv.norm(u) for u in REGISTRY["frozen_prefixes"]
               if u not in SEMANTIC and not u.startswith("_")}
HOME = (REPO_ROOT / ROOT_SPEC["file"]).read_text(encoding="utf-8")


def diff(base: str, new: str):
    return cv.semantic_freeze_diff(base, new, BYTE_FROZEN)


def sub(text: str, old: str, new: str) -> str:
    """Replace exactly one known occurrence, or fail loudly.

    A mutation that silently matches nothing would make its negative test pass
    for the wrong reason — the gate would look like it caught a change that was
    never made.
    """
    assert text.count(old) == 1, f"expected exactly 1 occurrence of {old!r}, got {text.count(old)}"
    return text.replace(old, new)


def title_of(text: str) -> str:
    return cv.TITLE_RE.search(text).group(1)


def drop_ld_node(text: str, id_fragment: str) -> str:
    """Remove one @graph node by @id, via a JSON round-trip.

    Splicing this out with a regex is what a careless edit would look like, and
    a regex that quietly matches nothing produces a test that passes for the
    wrong reason.
    """
    m = cv.LD_JSON_RE.search(text)
    data = json.loads(m.group(1))
    before = len(data["@graph"])
    data["@graph"] = [n for n in data["@graph"] if id_fragment not in str(n.get("@id", ""))]
    assert len(data["@graph"]) == before - 1, f"no node matched {id_fragment!r}"
    return text[:m.start(1)] + json.dumps(data) + text[m.end(1):]


# The Tampa LocalBusiness node as it existed before the claim-safety removal.
# The carve-out tests inject it rather than reading it from the tree, so they
# keep exercising the carve-out after the node is gone from index.html.
TAMPA_NODE = {
    "@type": ["LocalBusiness", "HomeAndConstructionBusiness"],
    "@id": "https://acglass.com/#localbusiness-tampa",
    "name": "American Commercial Glass",
    "parentOrganization": {"@id": "https://acglass.com/#organization"},
    "address": {
        "@type": "PostalAddress",
        "streetAddress": "3031 N Rocky Point Dr W Ste 600",
        "addressLocality": "Tampa",
        "addressRegion": "FL",
        "postalCode": "33607",
        "addressCountry": "US",
    },
    "geo": {"@type": "GeoCoordinates", "latitude": 27.96863, "longitude": -82.56867},
    "telephone": "+1-772-486-7711",
    "url": "https://acglass.com/",
}


def with_tampa_node(text: str) -> str:
    """Return `text` with the historical Tampa identity node spliced back in."""
    m = cv.LD_JSON_RE.search(text)
    data = json.loads(m.group(1))
    assert not any("localbusiness-tampa" in str(n.get("@id", ""))
                   for n in data["@graph"]), "Tampa node unexpectedly still present"
    data["@graph"] = data["@graph"] + [TAMPA_NODE]
    return text[:m.start(1)] + json.dumps(data) + text[m.end(1):]


# A body-only addition of the kind the freeze is meant to permit: truthful
# contextual navigation to service and market hubs, no protected field touched.
CONTEXTUAL_NAV = """
  <section class="sys" id="markets-followup">
    <h2>Where we work</h2>
    <a href="/glazing-contractor-florida.html">Commercial glazing contractor in Florida</a>
    <a href="/commercial-glazing-south-florida.html">South Florida commercial glazing</a>
    <a href="/commercial-glazing-nashville-tn.html">Nashville commercial glazing</a>
    <a href="/service-areas.html">All service areas</a>
  </section>
"""

# One mutation per protected field. Each must change that field and only that
# field, so a failure set of exactly {field} proves the extraction is specific
# as well as sensitive.
MUTATIONS = {
    "title": lambda t: sub(t, f"<title>{title_of(t)}</title>",
                           "<title>Glass Company Near Me | ACG</title>"),
    "meta-description": lambda t: sub(
        t, 'name="description" content="Florida\'s commercial glazing',
        'name="description" content="Rewritten. Florida\'s commercial glazing'),
    "canonical": lambda t: sub(t, '<link rel="canonical" href="https://acglass.com/"',
                               '<link rel="canonical" href="https://acglass.com/index.html"'),
    "meta-robots": lambda t: sub(
        t,
        'name="robots" content="index,follow,max-image-preview:large,max-snippet:-1"',
        'name="robots" content="noindex,follow,max-image-preview:large,max-snippet:-1"',
    ),
    # The H1 is split across spans, so the mutation targets the source markup
    # rather than the normalized text the extractor produces.
    "h1": lambda t: sub(t, '<span class="l1">Commercial glazing.</span>',
                        '<span class="l1">Florida\'s best glass company.</span>'),
    "og:title": lambda t: sub(t, 'property="og:title" content="Commercial',
                              'property="og:title" content="Rewritten Commercial'),
    "og:url": lambda t: sub(t, 'property="og:url" content="https://acglass.com/"',
                            'property="og:url" content="https://acglass.com/index.html"'),
    # Location identity: the geo of the #localbusiness-west-palm-beach node the
    # map pack resolves against.
    "schema-identity": lambda t: sub(t, '"latitude": 26.70716', '"latitude": 26.9'),
    "wpb-text": lambda t: sub(
        t,
        "headquartered in West Palm Beach. ACG installs",
        "headquartered in Palm Beach. ACG installs",
    ),
}

# wpb-links has no base case to remove: the root links no frozen WPB URL today.
# The test supplies one, so the check is exercised rather than skipped.
WPB_LINK = '<a href="/west-palm-beach/">Our headquarters market</a>'


class NegativeTests(unittest.TestCase):
    """Each protected field must fail when altered."""

    def test_each_protected_field_fails_when_altered(self):
        for field, mutate in MUTATIONS.items():
            with self.subTest(field=field):
                failures, _ = diff(HOME, mutate(HOME))
                self.assertIn(field, failures, f"{field} was altered but not caught")
                self.assertEqual(
                    {field}, set(failures),
                    f"{field} mutation also tripped {set(failures) - {field}}; "
                    "the extraction is not specific to this field")

    def test_wpb_links_fails_when_an_existing_link_is_removed(self):
        base = sub(HOME, "</body>", f"{WPB_LINK}</body>")
        failures, _ = diff(base, HOME)
        self.assertEqual({"wpb-links"}, set(failures))
        self.assertIn("/west-palm-beach/", failures["wpb-links"])

    def test_wpb_links_fails_when_an_existing_link_is_reworded(self):
        base = sub(HOME, "</body>", f"{WPB_LINK}</body>")
        new = sub(base, "Our headquarters market", "HQ")
        failures, _ = diff(base, new)
        self.assertEqual({"wpb-links"}, set(failures))

    def test_removing_an_identity_node_is_caught(self):
        # Uses a verified-office node, not the carved-out Tampa node: the Tampa
        # node was removed as a false physical-location claim, so mutating it
        # here would make this test pass for the wrong reason.
        new = drop_ld_node(HOME, "localbusiness-naples")
        failures, _ = diff(HOME, new)
        self.assertEqual({"schema-identity"}, set(failures))
        self.assertIn("removed", failures["schema-identity"])

    def test_unparseable_schema_is_caught(self):
        new = sub(HOME, '"@context": "https://schema.org"', '"@context": "https://schema.org",,')
        failures, _ = diff(HOME, new)
        self.assertIn("schema-identity", failures)


class PositiveTests(unittest.TestCase):
    """Permitted additions must pass, or the freeze is a byte freeze in disguise."""

    def test_contextual_nav_section_passes(self):
        new = sub(HOME, "</body>", f"{CONTEXTUAL_NAV}</body>")
        failures, added = diff(HOME, new)
        self.assertEqual({}, failures, f"a body-only nav addition was blocked: {failures}")
        self.assertEqual(set(), added)

    def test_contextual_nav_plus_in_page_anchor_passes(self):
        new = sub(HOME, "</body>", f"{CONTEXTUAL_NAV}</body>")
        new = sub(new, '<a href="#capability">', '<a href="#markets-followup">Markets</a><a href="#capability">')
        failures, _ = diff(HOME, new)
        self.assertEqual({}, failures)

    def test_adding_wpb_text_is_permitted_when_nothing_is_removed(self):
        new = sub(HOME, "</body>",
                  "<p>Our West Palm Beach crews self-perform every opening.</p></body>")
        failures, _ = diff(HOME, new)
        self.assertEqual({}, failures)

    def test_new_wpb_link_is_reported_but_not_a_failure(self):
        new = sub(HOME, "</body>", f"{WPB_LINK}</body>")
        failures, added = diff(HOME, new)
        self.assertEqual({}, failures)
        self.assertEqual(1, len(added), "a new link into a frozen WPB URL must be surfaced")
        self.assertIn("/west-palm-beach/", next(iter(added)))

    def test_identical_input_yields_nothing(self):
        self.assertEqual(({}, set()), diff(HOME, HOME))


class PolicyTests(unittest.TestCase):
    def test_every_declared_field_has_a_negative_test(self):
        covered = set(MUTATIONS) | {"wpb-links"}
        self.assertEqual(set(PROTECTED), covered,
                         "a protected field was declared in url-primaries.json with no "
                         "negative test, or a test exists for a field that is not enforced")

    def test_wpb_pages_stay_byte_frozen(self):
        for url in REGISTRY["frozen_prefixes"]:
            if url == "/" or url.startswith("_"):
                continue
            with self.subTest(url=url):
                self.assertNotIn(url, SEMANTIC,
                                 "the contested WPB URLs must stay byte-frozen; the ranking "
                                 "URL among them is unknown, so body copy is frozen too")

    def test_root_is_semantically_frozen_and_still_listed_as_frozen(self):
        # PR #17's internal-link-audit reads frozen_prefixes to skip breakage
        # checks on frozen pages. The root must remain in that list.
        self.assertIn("/", REGISTRY["frozen_prefixes"])
        self.assertIn("/", SEMANTIC)
        self.assertEqual("index.html", ROOT_SPEC["file"])


class SchemaIdentityCarveOutTests(unittest.TestCase):
    """The claim-safety carve-out must be removal-only and narrowly scoped.

    Tampa is an ACG service area, not an office. A LocalBusiness node asserting
    a Tampa postal address, geo and opening hours is a false physical-location
    claim, and claim safety outranks ranking stability -- so removing it is
    permitted. Every other use of the carve-out must still fail, or the freeze
    becomes a rename-and-reword hole.
    """

    CARVE = "https://acglass.com/#localbusiness-tampa"
    VERIFIED = ("https://acglass.com/#localbusiness-west-palm-beach",
                "https://acglass.com/#localbusiness-naples",
                "https://acglass.com/#localbusiness-stuart")

    def _drop_node(self, html, node_id):
        i = html.find(f'"@id": "{node_id}"')
        if i < 0:
            self.fail(f"{node_id} not present in the fixture")
        depth, start = 0, None
        for j in range(i, -1, -1):
            if html[j] == "}":
                depth += 1
            elif html[j] == "{":
                if depth == 0:
                    start = j
                    break
                depth -= 1
        depth, end = 0, None
        for j in range(start, len(html)):
            if html[j] == "{":
                depth += 1
            elif html[j] == "}":
                depth -= 1
                if depth == 0:
                    end = j
                    break
        rest = html[end + 1:]
        stripped = rest.lstrip()
        if stripped.startswith(","):
            rest = stripped[1:]
        return html[:start] + rest

    def test_declared_removable_id_may_be_removed(self):
        base = with_tampa_node(HOME)
        failures, _ = cv.semantic_freeze_diff(
            base, HOME, BYTE_FROZEN, frozenset([self.CARVE]))
        self.assertNotIn("schema-identity", failures,
                         "the declared claim-safety removal was blocked")

    def test_removal_still_fails_when_not_declared(self):
        base = with_tampa_node(HOME)
        failures, _ = cv.semantic_freeze_diff(base, HOME, BYTE_FROZEN)
        self.assertIn("schema-identity", failures,
                      "an undeclared node removal slipped through")
        self.assertIn("removed", failures["schema-identity"])

    def test_carve_out_does_not_permit_altering_the_node(self):
        # The carve-out is removal-only, so a reworded address on a carved-out
        # node must still fail.
        base = with_tampa_node(HOME)
        new = base.replace("3031 N Rocky Point Dr W Ste 600", "999 Example St")
        self.assertNotEqual(base, new, "the address mutation matched nothing")
        failures, _ = cv.semantic_freeze_diff(
            base, new, BYTE_FROZEN, frozenset([self.CARVE]))
        self.assertIn("schema-identity", failures,
                      "the carve-out wrongly permitted an edit, not just a removal")

    def test_carve_out_does_not_permit_re_adding_the_node(self):
        # Re-adding the false Tampa node must fail even though it is declared
        # removable, or the carve-out becomes a two-way door.
        new = with_tampa_node(HOME)
        failures, _ = cv.semantic_freeze_diff(
            HOME, new, BYTE_FROZEN, frozenset([self.CARVE]))
        self.assertIn("schema-identity", failures,
                      "the carve-out wrongly permitted re-adding the node")
        self.assertIn("added", failures["schema-identity"])

    def test_carve_out_does_not_cover_verified_offices(self):
        removable = frozenset(ROOT_SPEC.get("schema_identity_removable", ()))
        for node_id in self.VERIFIED:
            self.assertNotIn(node_id, removable,
                             f"{node_id} is a verified office and must stay frozen")

    def test_verified_office_removal_still_fails_under_the_declared_carve_out(self):
        declared = frozenset(ROOT_SPEC.get("schema_identity_removable", ()))
        for node_id in self.VERIFIED:
            frag = node_id.rsplit("#", 1)[1]
            if frag not in HOME:
                continue
            new = drop_ld_node(HOME, frag)
            failures, _ = cv.semantic_freeze_diff(HOME, new, BYTE_FROZEN, declared)
            self.assertIn("schema-identity", failures,
                          f"removing {node_id} was permitted")

    def test_carve_out_list_is_documented_and_minimal(self):
        removable = ROOT_SPEC.get("schema_identity_removable", [])
        self.assertEqual([self.CARVE], removable,
                         "the carve-out list grew; each entry needs its own review")
        self.assertIn("CARVE-OUT", ROOT_SPEC["protected_fields"]["schema-identity"],
                      "the carve-out must be documented on the protected field")
        self.assertTrue(ROOT_SPEC.get("carve_out_log"),
                        "every carve-out needs a dated log entry naming the reason")

    def test_no_tampa_address_remains_on_the_root(self):
        self.assertNotIn("Rocky Point", HOME,
                         "a Tampa street address is still asserted on the root")
        self.assertNotIn("localbusiness-tampa", HOME,
                         "the Tampa LocalBusiness node is still on the root")



if __name__ == "__main__":
    unittest.main(verbosity=2)
