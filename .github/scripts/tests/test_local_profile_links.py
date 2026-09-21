"""Local landing pages must resolve their provider and eight profile services."""
import json
from pathlib import Path
import re
import unittest
import subprocess
import shutil

ROOT = Path(__file__).resolve().parents[3]
CITIES = ('west-palm-beach', 'stuart', 'tampa', 'naples')
SERVICES = ('commercial-storefront-systems.html', 'curtainwall-systems.html',
            'window-wall-systems.html', 'impact-windows-doors.html',
            'multi-slide-bifold-doors.html', 'fire-rated-glass-systems.html',
            'automatic-entrance-systems.html', 'interior-glass-partitions.html')

class LocalProfileLinks(unittest.TestCase):
    def test_attribution_behavior_in_javascript(self):
        node = shutil.which("node")
        self.assertIsNotNone(node, "Node is required for the browser attribution regression")
        result = subprocess.run([node, str(ROOT / ".github/scripts/tests/test_gbp_attribution.js")], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_attribution_loads_on_landing_and_lead_pages(self):
        pages = [('storefront-glazier-' + city + '-florida/index.html') for city in CITIES]
        pages += ['send-plans.html', 'bid.html', 'contact.html', 'free-glazing-scope-review.html']
        for page in pages:
            with self.subTest(page=page):
                text = (ROOT / page).read_text()
                self.assertEqual(text.count('/js/acg-gbp-attribution.js?v=20260921'), 1)


    def test_each_city_has_resolved_provider_and_service_links(self):
        for city in CITIES:
            with self.subTest(city=city):
                page = ROOT / ('storefront-glazier-' + city + '-florida/index.html')
                text = page.read_text()
                graph = json.loads(re.search(r'<script type="application/ld\+json">(.*?)</script>', text, re.S)[1])['@graph']
                nodes = {node['@id']: node for node in graph if '@id' in node}
                service = next(node for node in graph if node.get('@type') == 'Service')
                provider = nodes[service['provider']['@id']]
                self.assertEqual(provider['@type'], 'Organization')
                self.assertEqual(provider['@id'], 'https://acglass.com/#organization')
                scope = re.search(r'<section aria-label="Full commercial glass scope".*?</section>', text, re.S)[0]
                for destination in SERVICES:
                    self.assertIn('href="/' + destination + '"', scope)
                    self.assertTrue((ROOT / destination).is_file())
                self.assertIn('href="https://acglass.com/storefront-glazier-' + city + '-florida/"', text)

if __name__ == '__main__':
    unittest.main()
