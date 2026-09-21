"""Prevent retired bond offers and unsupported engineering/insurance claims."""
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[3]

class HomepageClaimBoundary(unittest.TestCase):
    def test_homepage_does_not_offer_bonds_or_imply_in_house_sealing(self):
        html = (ROOT / 'index.html').read_text()
        text = re.sub(r'<[^>]+>', ' ', html)
        self.assertNotRegex(text.lower(), r'\bbond(?:ing|ed)?\b|\bsurety\b')
        self.assertNotRegex(text.lower(), r'engineer.sealed|sealed shop drawings|produced in.house')
        self.assertNotRegex(text.lower(), r'general liability.{0,60}\$|workers.{0,20}comp.{0,40}\$')
        self.assertIn('Coordinated shop drawings', text)

if __name__ == '__main__':
    unittest.main()
