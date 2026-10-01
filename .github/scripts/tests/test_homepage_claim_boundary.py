"""Prevent bond offers, unverified bonding figures, and unsupported engineering/insurance claims."""
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[3]

class HomepageClaimBoundary(unittest.TestCase):
    def test_homepage_does_not_offer_bonds_or_imply_in_house_sealing(self):
        html = (ROOT / 'index.html').read_text()
        text = re.sub(r'<[^>]+>', ' ', html)
        low = text.lower()
        # Connor 2026-10-01: the website may state the verified bonding capacity
        # ($3M single / $6M aggregate, confirmed current 2026-09-09). It still
        # never offers a bond or quotes a bond rate.
        self.assertNotRegex(low, r'bond(?:ing)?\s+(?:rate|premium|pricing)|\d+(?:\.\d+)?\s*%[^.<]{0,40}\bbond|\bbond[^.<]{0,40}\d+(?:\.\d+)?\s*%')
        for m in re.finditer(r'bond|surety', low):
            window = low[max(0, m.start() - 80):m.end() + 80]
            for fig in re.findall(r'\$\s?(\d+(?:\.\d+)?)\s?m\b', window):
                self.assertIn(fig, {'3', '6'}, window)
        self.assertNotRegex(text.lower(), r'engineer.sealed|sealed shop drawings|produced in.house')
        self.assertNotRegex(text.lower(), r'general liability.{0,60}\$|workers.{0,20}comp.{0,40}\$')
        self.assertIn('Coordinated shop drawings', text)

if __name__ == '__main__':
    unittest.main()
