"""Project case studies are not purchasable product detail pages."""
import json
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[3]
PROJECTS = ('eau-palm-beach-resort', 'stayapt-suites-lafayette', 'cudjoe-key-fire-station', 'gulfside-twelve', 'atlantic-fields-golf-house')

def nodes(value):
    if isinstance(value, dict):
        yield value
        for child in value.values():
            yield from nodes(child)
    elif isinstance(value, list):
        for child in value:
            yield from nodes(child)

class ProjectSchema(unittest.TestCase):
    def test_case_studies_do_not_emit_product_offers(self):
        for slug in PROJECTS:
            with self.subTest(project=slug):
                source = (ROOT / (slug + '.html')).read_text()
                blocks = re.findall(r'<script type="application/ld\+json">(.*?)</script>', source, re.S)
                self.assertTrue(blocks)
                types = []
                for block in blocks:
                    for node in nodes(json.loads(block)):
                        value = node.get('@type', [])
                        types.extend(value if isinstance(value, list) else [value])
                self.assertNotIn('Product', types)
                self.assertNotIn('Offer', types)
                self.assertIn('CreativeWork', types)

if __name__ == '__main__':
    unittest.main()
