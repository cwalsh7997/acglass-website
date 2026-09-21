"""The four designated GBP destinations must stay indexable and self canonical."""
import json
import re
import unittest
from pathlib import Path
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[3]

class GBPIndexability(unittest.TestCase):
    def test_all_four_destinations_are_indexable_in_sitemap(self):
        locs = {n.text for p in ROOT.glob('sitemap*.xml') for n in ET.parse(p).iter('{http://www.sitemaps.org/schemas/sitemap/0.9}loc')}
        for city in ('west-palm-beach', 'stuart', 'tampa', 'naples'):
            slug = f'storefront-glazier-{city}-florida/'
            html = (ROOT / slug / 'index.html').read_text()
            with self.subTest(city=city):
                metas = re.findall(r'<meta\b[^>]*>', html, re.I)
                for meta in metas:
                    if re.search(r'name=["\x27](robots|googlebot)["\x27]', meta, re.I):
                        value = re.search(r'content=["\x27]([^"\x27]+)', meta, re.I)[1].lower()
                        self.assertNotIn('noindex', value)
                        self.assertNotIn('none', value.split(','))
                self.assertNotRegex(html, r'(?i)http-equiv=["\x27]refresh')
                self.assertIn(f'<link rel="canonical" href="https://acglass.com/{slug}">', html)
                self.assertIn('https://acglass.com/' + slug, locs)

    def test_stuart_has_grounded_service_area_content(self):
        html = (ROOT / 'storefront-glazier-stuart-florida/index.html').read_text()
        graph = json.loads(re.search(r'<script type="application/ld\+json">(.*?)</script>', html, re.S)[1])['@graph']
        self.assertFalse(any(n.get('@type') == 'LocalBusiness' for n in graph))
        faq = next(n for n in graph if n.get('@type') == 'FAQPage')
        for q in faq['mainEntity']:
            self.assertIn(q['name'], html)
            self.assertIn(q['acceptedAnswer']['text'], html)
        for target in ('atlantic-fields-golf-house.html', 'atlantic-fields-performance-center.html'):
            self.assertIn(f'href="/{target}"', html)
            self.assertTrue((ROOT / target).is_file())
        for claim in ('48-hour', '48-Hr', 'emergency dispatch', 'general liability', '170 mph', 'Written by Connor'):
            self.assertNotIn(claim.lower(), html.lower())
