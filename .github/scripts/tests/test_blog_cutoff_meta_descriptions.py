#!/usr/bin/env python3
"""Blog pages from the 2026-10-07 snippet crawl keep a finished meta description."""

from __future__ import annotations

import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
META_TAG = re.compile(r"<meta\b[^>]*>", re.I)
ATTR = re.compile(r"([:\w-]+)\s*=\s*(['\"])(.*?)\2", re.S)

PAGES = (
    "blog/automatic-entrance-ada-compliance.html",
    "blog/automatic-entrance-systems-commercial-buildings-florida.html",
    "blog/best-glass-types-florida-commercial-climate.html",
    "blog/bi-fold-glass-walls-restaurants-hospitality.html",
    "blog/bradley-daytona-multifamily-glazing.html",
    "blog/commercial-glass-cleaning-maintenance-florida.html",
    "blog/commercial-glass-insurance-claims-florida.html",
    "blog/commercial-glass-property-value-florida.html",
    "blog/commercial-glazing-contractors-tampa-fl.html",
    "blog/commercial-glazing-inspection-florida.html",
    "blog/commercial-glazing-miami-florida.html",
    "blog/commercial-glazing-tampa-bay-market-2026.html",
    "blog/commercial-glazing-tampa-bay-what-gcs-need-to-know.html",
    "blog/commercial-storm-proofing-windows-florida-guide.html",
    "blog/common-commercial-glass-installation-mistakes-avoid.html",
    "blog/cubesmart-davie-glazing.html",
    "blog/curtainwall-vs-storefront-florida.html",
    "blog/dale-mabry-retail-tampa-glazing.html",
    "blog/decorative-glass-storefront-options-florida.html",
    "blog/el-car-wash-northlake-glazing.html",
    "blog/estero-vista-fort-myers-glazing.html",
    "blog/fire-rated-glass-requirements-commercial-buildings.html",
    "blog/florida-commercial-glazing-hurricane-code.html",
    "blog/ginsberg-eye-center-glazing.html",
    "blog/glazing-subcontractor-scope-letter-guide.html",
    "blog/harbour-cay-fort-pierce-glazing.html",
    "blog/hardy-world-melbourne-glazing.html",
    "blog/how-long-do-commercial-windows-last-florida.html",
    "blog/how-much-does-commercial-glazing-cost-florida.html",
    "blog/how-professional-glaziers-ensure-safe-installation.html",
    "blog/how-to-choose-commercial-glass-contractor-florida.html",
    "blog/how-to-choose-glazing-contractor.html",
    "blog/how-to-choose-glazing-subcontractor.html",
    "blog/how-to-evaluate-glazing-subcontractor-bid.html",
    "blog/how-to-know-glazier-did-quality-work.html",
    "blog/hurricane-preparation-commercial-impact-glass.html",
    "blog/hurricane-window-installers-cost-hiring-florida-commercial.html",
    "blog/hvhz-certified-glazing-contractor-florida.html",
    "blog/hvhz-glazing-requirements-florida.html",
    "blog/ifly-miami-glazing.html",
    "blog/impact-window-contractor-commercial-florida.html",
    "blog/impact-windows-vs-hurricane-shutters.html",
    "blog/imperial-crossings-bonita-springs-glazing.html",
    "blog/indiantown-high-school-glazing.html",
    "blog/lake-park-innovation-center-glazing.html",
    "blog/lessons-from-350-florida-commercial-glazing-projects.html",
    "blog/lucie-at-tradition-glazing.html",
    "blog/nashville-commercial-construction-glazing-market.html",
    "blog/pointe-palm-bay-glazing.html",
    "blog/professional-installation-commercial-glazing-important.html",
    "blog/project-lift-hobe-sound-glazing.html",
    "blog/questions-to-ask-glazing-subcontractor-before-hiring.html",
    "blog/savannas-ridge-clubhouse-glazing.html",
    "blog/shoppes-westlake-point-glazing.html",
    "blog/single-vs-double-glazing-commercial-florida.html",
    "blog/smart-glass-technology-commercial-florida.html",
    "blog/tampa-commercial-construction-boom-glazing.html",
    "blog/tennessee-commercial-glazing-code-guide.html",
    "blog/tennessee-vs-florida-commercial-glazing-differences.html",
    "blog/turbine-technologies-jupiter-glazing.html",
    "blog/villa-lonz-riviera-beach-glazing.html",
    "blog/wave-haven-cocoa-beach-glazing.html",
    "blog/waxins-eurowall-clematis-street.html",
    "blog/weatherproof-commercial-windows-florida.html",
    "blog/what-are-impact-windows-commercial-guide.html",
    "blog/what-certifications-professional-glazier-have.html",
    "blog/what-is-a-curtainwall-system.html",
    "blog/what-is-low-e-glass-commercial.html",
    "blog/what-safety-standards-professional-glaziers-follow.html",
    "blog/what-skills-should-commercial-glazier-have.html",
    "blog/why-acg-opened-tampa-office.html",
    "blog/why-does-commercial-glass-fog-up-and-how-to-fix-it.html",
    "blog/why-hire-local-commercial-glazier-florida.html",
    "blog/window-wall-multifamily-guide.html",
    "blog/window-wall-systems-florida-guide.html",

)


def meta_descriptions(html: str) -> list[str]:
    found = []
    for tag in META_TAG.findall(html):
        attrs = {key.lower(): value for key, _, value in ATTR.findall(tag)}
        if attrs.get("name", "").lower() == "description":
            found.append(attrs.get("content", ""))
    return found


class BlogCutoffMetaDescriptionTests(unittest.TestCase):
    def test_each_page_has_one_finished_description(self):
        for rel in PAGES:
            html = (ROOT / rel).read_text(encoding="utf-8")
            found = meta_descriptions(html)
            self.assertEqual(1, len(found), rel)
            desc = found[0]
            self.assertGreaterEqual(len(desc), 120, rel + " " + desc)
            self.assertLessEqual(len(desc), 155, rel + " " + desc)
            self.assertIn(desc[-1], ".!?", rel)
            self.assertNotIn("\u2026", desc, rel)
            self.assertNotIn("...", desc, rel)
            self.assertNotIn("\u2014", desc, rel)
            self.assertNotIn("\u2013", desc, rel)


if __name__ == "__main__":
    unittest.main()
