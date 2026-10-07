#!/usr/bin/env python3
"""Commercial pages from the 2026-10-07 snippet crawl keep a finished meta description."""

from __future__ import annotations

import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
META_TAG = re.compile(r"<meta\b[^>]*>", re.I)
ATTR = re.compile(r"([:\w-]+)\s*=\s*([\'\"])(.*?)\2", re.S)

PAGES = (
    "1172-s-harbor.html",
    "after-hours-storefront-installation-miami/index.html",
    "approvals/index.html",
    "736-lagoon-dr.html",
    "2143-carib-circle.html",
    "aluminum-extrusion-grades-commercial-glazing/index.html",
    "aluminum-vs-vinyl-windows-commercial/index.html",
    "architect-specs/section-08-87-13-fire-rated-glazing.html",
    "architect-specs/index.html",
    "architect-specs/section-08-44-13-aluminum-curtainwall.html",
    "architect-specs/section-08-41-13-aluminum-storefront.html",
    "architect-specs/section-08-71-00-automatic-entrance-door-hardware.html",
    "architect-specs/section-08-44-23-multi-slide-doors.html",
    "atlantic-fields-performance-center.html",
    "best-glass-for-restaurant-storefronts-florida/index.html",
    "after-hours-commercial-glazing-installation-florida/index.html",
    "architect-specs/section-08-43-29-folding-glass-walls.html",
    "case-study-tomoka-town-center.html",
    "case-study-tradewinds-clubhouse.html",
    "city-of-haines-emergency.html",
    "commercial-glass-board-up-emergency-florida/index.html",
    "commercial-glass-replacement-vs-repair/index.html",
    "commercial-glazing-bid-comparison-florida/index.html",
    "commercial-glazing-for-reits-florida/index.html",
    "commercial-glazing-owner-direct-restaurant-florida/index.html",
    "commercial-glazing-near-me-florida.html",
    "commercial-glazing-melbourne-fl.html",
    "commercial-glazing-parkland-fl.html",
    "case-study-rome-collective.html",
    "commercial-glazing-windermere.html",
    "curtainwall-installation.html",
    "educational-institutional-glazing.html",
    "faq.html",
    "florida-commercial-glazing-report-2026.html",
    "estero-vista-fort-myers.html",
    "glazing-subcontractor-prequalification.html",
    "glazing-submittal-package.html",
    "glazing-subcontractor-florida.html",
    "gym-fitness-commercial-glazing-florida/index.html",
    "how-long-does-commercial-glazing-take-to-install/index.html",
    "how-to-hire-commercial-glazier-florida/index.html",
    "how-to-spec-commercial-impact-glass/index.html",
    "hurricane-glass-replacement-fort-lauderdale/index.html",
    "can-acg-handle-healthcare-glazing-occupied-facility/index.html",
    "how-to-hire-commercial-glazing-contractor-florida.html",
    "ifly-miami.html",
    "industries/healthcare.html",
    "industries/multifamily.html",
    "industries/office-tower.html",
    "interior-glass-partitions.html",
    "licensed-glazing-contractor-florida.html",
    "prestige-marble-bonita-springs.html",
    "press/index.html",
    "occupied-building-glazing-installation-florida/index.html",
    "pvb-vs-sgp-interlayer-comparison/index.html",
    "resources/index.html",
    "project-lift-hobe-sound.html",
    "storefront-bid-checklist-for-gcs.html",
    "low-e-glass-explained-florida/index.html",
    "tradewinds-hobe-sound.html",
    "villa-lonz-riviera-beach.html",
    "wild-blue-clubhouse.html",
)


def meta_descriptions(html: str) -> list[str]:
    found = []
    for tag in META_TAG.findall(html):
        attrs = {key.lower(): value for key, _, value in ATTR.findall(tag)}
        if attrs.get("name", "").lower() == "description":
            found.append(attrs.get("content", ""))
    return found


class CutoffMetaDescriptionTests(unittest.TestCase):
    def test_each_page_has_one_finished_description(self):
        for rel in PAGES:
            html = (ROOT / rel).read_text(encoding="utf-8")
            found = meta_descriptions(html)
            self.assertEqual(1, len(found), rel)
            desc = found[0]
            self.assertGreaterEqual(len(desc), 120, rel)
            self.assertLessEqual(len(desc), 160, rel)
            self.assertTrue(desc.endswith("."), rel)
            self.assertNotIn("\u2026", desc, rel)
            self.assertNotIn("\u2014", desc, rel)
            self.assertNotIn("\u2013", desc, rel)


if __name__ == "__main__":
    unittest.main()
