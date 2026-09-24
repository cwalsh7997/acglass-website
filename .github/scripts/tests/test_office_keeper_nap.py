"""Naples and Tampa money pages must publish their own office, not the WPB node."""

from __future__ import annotations

import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
JSONLD = re.compile(
    r'<script[^>]*type=["\']application/ld\+json["\'][^>]*>(.*?)</script>',
    re.I | re.S,
)
TITLE = re.compile(r"<title[^>]*>(.*?)</title>", re.I | re.S)

# Already published on the homepage LocalBusiness nodes and locations.html.
OFFICES = {
    "storefront-glazier-naples-florida/index.html": {
        "id": "https://acglass.com/#localbusiness-naples",
        "street": "4850 Tamiami Trail N Ste 301",
        "locality": "Naples",
        "postal": "34103",
        "lat": 26.20528,
        "lng": -81.79975,
        "title": "Commercial Storefront Installer Naples | 48-Hr Bids",
    },
    "storefront-glazier-tampa-florida/index.html": {
        "id": "https://acglass.com/#localbusiness-tampa",
        "street": "3031 N Rocky Point Dr W Ste 600",
        "locality": "Tampa",
        "postal": "33607",
        "lat": 27.96863,
        "lng": -82.56867,
        "title": "Commercial Storefront Installer Tampa | 48-Hr Bids",
    },
}
WPB_ID = "https://acglass.com/#localbusiness-west-palm-beach"
WPB_STREET = "700 S Rosemary Ave Suite 204"
ALIASES = {
    "commercial-glazing-naples.html": OFFICES["storefront-glazier-naples-florida/index.html"],
    "commercial-glazing-tampa.html": OFFICES["storefront-glazier-tampa-florida/index.html"],
}


def blocks(html: str):
    for raw in JSONLD.findall(html):
        yield json.loads(raw)


def walk(node):
    if isinstance(node, dict):
        yield node
        for value in node.values():
            yield from walk(value)
    elif isinstance(node, list):
        for value in node:
            yield from walk(value)


def local_businesses(html: str):
    found = []
    for block in blocks(html):
        for node in walk(block):
            raw = node.get("@type")
            types = raw if isinstance(raw, list) else [raw]
            if "LocalBusiness" in types:
                found.append(node)
    return found


class OfficeKeeperNapTests(unittest.TestCase):
    def test_storefront_keepers_use_published_office_identity(self):
        for rel, office in OFFICES.items():
            html = (ROOT / rel).read_text(encoding="utf-8")
            with self.subTest(rel=rel):
                self.assertEqual(TITLE.search(html).group(1).strip(), office["title"])
                nodes = local_businesses(html)
                self.assertEqual(1, len(nodes))
                node = nodes[0]
                address = node["address"]
                geo = node["geo"]
                self.assertEqual(office["id"], node["@id"])
                self.assertNotEqual(WPB_ID, node["@id"])
                self.assertEqual(office["street"], address["streetAddress"])
                self.assertEqual(office["locality"], address["addressLocality"])
                self.assertEqual(office["postal"], address["postalCode"])
                self.assertNotEqual(WPB_STREET, address["streetAddress"])
                self.assertEqual(office["lat"], geo["latitude"])
                self.assertEqual(office["lng"], geo["longitude"])
                self.assertIn(office["street"], html)

    def test_office_aliases_do_not_restamp_the_west_palm_node(self):
        for rel, office in ALIASES.items():
            html = (ROOT / rel).read_text(encoding="utf-8")
            with self.subTest(rel=rel):
                nodes = local_businesses(html)
                self.assertTrue(nodes)
                ids = {node.get("@id") for node in nodes}
                self.assertNotIn(WPB_ID, ids)
                self.assertIn(office["id"], ids)
                for node in nodes:
                    self.assertNotEqual(WPB_STREET, node.get("address", {}).get("streetAddress"))
                for node in walk_all(html):
                    if node.get("mainEntityOfPage"):
                        self.assertEqual("https://acglass.com/", node.get("mainEntityOfPage"))

    def test_west_palm_keeper_stays_on_the_hq_node(self):
        html = (ROOT / "storefront-glazier-west-palm-beach-florida/index.html").read_text(
            encoding="utf-8"
        )
        self.assertEqual(
            "Commercial Storefront Installer, West Palm Beach | Bid",
            TITLE.search(html).group(1).strip(),
        )
        nodes = local_businesses(html)
        self.assertEqual(1, len(nodes))
        self.assertEqual(WPB_ID, nodes[0]["@id"])
        self.assertEqual(WPB_STREET, nodes[0]["address"]["streetAddress"])

    def test_wpb_id_hours_match_the_homepage_node(self):
        """Homepage LocalBusiness for this @id is Mon-Fri 07:00-18:00.
        Naples and Tampa keepers use their own @ids and already match that window.
        Every duplicate of the West Palm Beach @id must publish the same hours.
        """
        home = next(
            node
            for node in local_businesses((ROOT / "index.html").read_text(encoding="utf-8"))
            if node.get("@id") == WPB_ID
        )
        spec = home["openingHoursSpecification"]
        self.assertEqual(
            [
                {
                    "@type": "OpeningHoursSpecification",
                    "dayOfWeek": [
                        "Monday",
                        "Tuesday",
                        "Wednesday",
                        "Thursday",
                        "Friday",
                    ],
                    "opens": "07:00",
                    "closes": "18:00",
                }
            ],
            spec,
        )
        mismatches = []
        for path in ROOT.rglob("*.html"):
            if ".git" in path.parts:
                continue
            html = path.read_text(encoding="utf-8", errors="replace")
            if WPB_ID not in html:
                continue
            for node in local_businesses(html):
                if node.get("@id") != WPB_ID:
                    continue
                hours = node.get("openingHoursSpecification")
                if hours and hours != spec:
                    mismatches.append(str(path.relative_to(ROOT)))
        self.assertEqual(mismatches, [])
        for rel in OFFICES:
            node = local_businesses((ROOT / rel).read_text(encoding="utf-8"))[0]
            self.assertEqual(spec, node["openingHoursSpecification"])


def walk_all(html: str):
    for block in blocks(html):
        yield from walk(block)


if __name__ == "__main__":
    unittest.main()
