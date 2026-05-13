#!/usr/bin/env python3
"""Strengthen brand disambiguation signals across the site.

The problem: Google autocorrects 'acg glass' -> 'agc glass' (AGC Inc / Asahi Glass).
The fix: every brand reference must signal that ACG (American Commercial Glass) is a
distinct entity from AGC Inc. We do this with explicit disambiguatingDescription,
multiple alternateName values, and visible 'ACG (American Commercial Glass)' text patterns.
"""
import re, json
from pathlib import Path

ROOT = Path('/home/user/workspace/acglass-website')

# 1) Update the canonical multi-location Organization graph on homepage/contact/about
# to include explicit disambiguation properties.

DISAMBIG_FIELDS = {
    "alternateName": [
        "ACG",
        "ACG Glass",
        "ACG Florida",
        "American Commercial Glass Florida",
        "ACG Commercial Glass"
    ],
    "disambiguatingDescription": "American Commercial Glass, Inc. (ACG) is a Florida-licensed commercial glazing contractor based in West Palm Beach. ACG is NOT affiliated with AGC Inc. (Asahi Glass Co., the Japanese glass manufacturer). ACG is an installation and service contractor; AGC Inc. is a manufacturer.",
    "slogan": "Florida commercial glazing — storefront, curtainwall, window wall, impact-rated",
    "naics": "238150",
    "iso6523Code": "0199:CGC1531993"
}

# Find and update the @graph in index.html, contact.html, about.html
def patch_graph(html: str) -> tuple[str, bool]:
    """Inject disambiguation fields into the existing Organization graph node."""
    # Find a JSON-LD script with our @id
    pattern = re.compile(
        r'(<script type="application/ld\+json">\s*\{.*?"@id":\s*"https://acglass\.com/#organization".*?\})\s*</script>',
        re.DOTALL
    )
    matches = list(pattern.finditer(html))
    if not matches:
        return html, False
    # We'll parse the matched JSON, patch it, re-serialize
    modified = False
    for m in matches:
        block_text = m.group(1) + '</script>'
        # Extract the JSON content
        json_match = re.search(r'<script type="application/ld\+json">\s*(\{.*\})\s*</script>', block_text, re.DOTALL)
        if not json_match:
            continue
        try:
            data = json.loads(json_match.group(1))
        except json.JSONDecodeError:
            continue
        # Find the organization node (might be at top level or inside @graph)
        org_node = None
        if data.get('@id') == 'https://acglass.com/#organization':
            org_node = data
        elif '@graph' in data:
            for node in data['@graph']:
                if isinstance(node, dict) and node.get('@id') == 'https://acglass.com/#organization':
                    org_node = node
                    break
        if not org_node:
            continue
        # Patch the org node
        existing_alt = org_node.get('alternateName', [])
        if isinstance(existing_alt, str):
            existing_alt = [existing_alt]
        elif not isinstance(existing_alt, list):
            existing_alt = []
        # Merge alternateName uniquely, ACG first
        merged_alt = []
        for v in DISAMBIG_FIELDS['alternateName'] + existing_alt:
            if v not in merged_alt:
                merged_alt.append(v)
        org_node['alternateName'] = merged_alt
        org_node['disambiguatingDescription'] = DISAMBIG_FIELDS['disambiguatingDescription']
        if 'slogan' not in org_node:
            org_node['slogan'] = DISAMBIG_FIELDS['slogan']
        org_node['naics'] = DISAMBIG_FIELDS['naics']
        org_node['iso6523Code'] = DISAMBIG_FIELDS['iso6523Code']
        # Re-serialize this script tag
        new_json = json.dumps(data, indent=2)
        new_script = f'<script type="application/ld+json">\n{new_json}\n</script>'
        # Replace in html
        html = html.replace(json_match.group(0), new_script, 1)
        modified = True
    return html, modified

TARGETS = ['index.html', 'contact.html', 'about.html']
for rel in TARGETS:
    fp = ROOT / rel
    if not fp.exists():
        print(f"  MISS {rel}")
        continue
    html = fp.read_text()
    new_html, ok = patch_graph(html)
    if ok and new_html != html:
        fp.write_text(new_html)
        print(f"  OK   {rel} \u2014 organization graph patched with disambiguation fields")
    else:
        print(f"  SKIP {rel} \u2014 no organization graph found OR already patched")

# 2) Also update standalone LocalBusiness blocks sitewide to add 'ACG' as alternateName
# We'll do a regex substitution that's safe: find LocalBusiness blocks that have
# "name": "American Commercial Glass" but no "alternateName" yet.

LB_RE = re.compile(
    r'(\{\s*"@type":\s*\[?[^\]]*?(?:LocalBusiness|GeneralContractor|HomeAndConstructionBusiness|ProfessionalService)[^\]]*?\]?,?\s*[^}]*?"name":\s*"American Commercial Glass[^"]*")',
    re.DOTALL
)

# Simpler: count files that contain '"name": "American Commercial Glass' but not '"alternateName"'
lb_patch_count = 0
for fp in sorted(ROOT.rglob('*.html')):
    if '.git' in fp.parts or 'drafts' in fp.parts: continue
    try: c = fp.read_text()
    except: continue
    # Skip pages already patched
    if 'index.html' in str(fp) or 'contact.html' in str(fp) or 'about.html' in str(fp):
        continue
    # Inject alternateName: "ACG" into LocalBusiness blocks that lack it
    # Pattern: find a block opening with "@type" containing LocalBusiness etc., with "name": "American Commercial Glass..." but no "alternateName"
    # Use simpler text substitution
    orig = c
    # Match opening of org schema and inject alternateName right after the name
    c = re.sub(
        r'(\{\s*"@context":\s*"https://schema\.org",\s*"@type":\s*"LocalBusiness",\s*"name":\s*"American Commercial Glass[^"]*",)(\s*"address")',
        r'\1\n  "alternateName": ["ACG", "ACG Glass", "American Commercial Glass Florida"],\n  "disambiguatingDescription": "American Commercial Glass (ACG) is a Florida-licensed commercial glazing contractor. Not affiliated with AGC Inc. (Asahi Glass).",\2',
        c
    )
    if c != orig:
        fp.write_text(c)
        lb_patch_count += 1
print(f"\nPatched {lb_patch_count} additional pages with LocalBusiness alternateName + disambiguatingDescription")
