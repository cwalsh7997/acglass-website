#!/usr/bin/env python3
"""Patch all JSON-LD blocks that reference https://acglass.com/#organization
to include disambiguation fields. Works on both top-level and @graph patterns."""
import re, json
from pathlib import Path

ROOT = Path('/home/user/workspace/acglass-website')

DISAMBIG = {
    "alternateName": [
        "ACG",
        "ACG Glass",
        "ACG Florida",
        "American Commercial Glass Florida",
        "ACG Commercial Glass"
    ],
    "disambiguatingDescription": (
        "American Commercial Glass, Inc. (ACG) is a Florida-licensed commercial "
        "glazing contractor based in West Palm Beach. ACG is NOT affiliated with "
        "AGC Inc. (Asahi Glass Co.), the Japanese glass manufacturer. ACG installs; "
        "AGC manufactures."
    ),
    "naics": "238150",
    "iso6523Code": "0199:CGC1531993"
}


def patch_org_node(node: dict) -> bool:
    """Patch an organization-shaped node. Returns True if modified."""
    if not isinstance(node, dict):
        return False
    is_org = (
        node.get('@id') == 'https://acglass.com/#organization'
        or 'American Commercial Glass' in str(node.get('name', ''))
    )
    if not is_org:
        return False
    modified = False
    # alternateName -- merge into list
    existing = node.get('alternateName')
    existing_list = [existing] if isinstance(existing, str) else (existing if isinstance(existing, list) else [])
    merged = []
    for v in DISAMBIG['alternateName'] + existing_list:
        if v and v not in merged:
            merged.append(v)
    if merged != existing_list:
        node['alternateName'] = merged
        modified = True
    if node.get('disambiguatingDescription') != DISAMBIG['disambiguatingDescription']:
        node['disambiguatingDescription'] = DISAMBIG['disambiguatingDescription']
        modified = True
    if 'naics' not in node:
        node['naics'] = DISAMBIG['naics']
        modified = True
    if 'iso6523Code' not in node:
        node['iso6523Code'] = DISAMBIG['iso6523Code']
        modified = True
    return modified


def walk_and_patch(data) -> bool:
    """Recursively walk a JSON-LD structure and patch all matching org nodes."""
    if isinstance(data, dict):
        modified = patch_org_node(data)
        for v in data.values():
            if walk_and_patch(v):
                modified = True
        return modified
    elif isinstance(data, list):
        modified = False
        for item in data:
            if walk_and_patch(item):
                modified = True
        return modified
    return False


def patch_html(html: str) -> str:
    """Find every JSON-LD script in the HTML, parse, patch, re-serialize."""
    pattern = re.compile(r'(<script type="application/ld\+json">)(\s*)(\{.*?\})(\s*)(</script>)', re.DOTALL)

    def repl(m):
        opener, lead_ws, json_text, trail_ws, closer = m.groups()
        try:
            data = json.loads(json_text)
        except json.JSONDecodeError:
            return m.group(0)
        # Only operate if this block mentions our org id
        if 'acglass.com/#organization' not in json_text and 'American Commercial Glass' not in json_text:
            return m.group(0)
        if walk_and_patch(data):
            new_json = json.dumps(data, indent=2)
            return f'{opener}{lead_ws}{new_json}{trail_ws}{closer}'
        return m.group(0)

    return pattern.sub(repl, html)


changed_files = 0
total_blocks_touched = 0

for fp in sorted(ROOT.rglob('*.html')):
    if '.git' in fp.parts or 'drafts' in fp.parts: continue
    try:
        html = fp.read_text()
    except: continue
    if 'American Commercial Glass' not in html and 'acglass.com/#organization' not in html:
        continue
    new_html = patch_html(html)
    if new_html != html:
        fp.write_text(new_html)
        changed_files += 1

print(f"Patched disambiguation fields into {changed_files} files")

# Validate
print()
print("=== Validation ===")
for f in ['index.html','contact.html','about.html']:
    fp = ROOT / f
    c = fp.read_text()
    blocks = re.findall(r'<script type="application/ld\+json">(.*?)</script>', c, re.DOTALL)
    errs = 0
    has_disambig = False
    for b in blocks:
        try:
            d = json.loads(b)
            if DISAMBIG['disambiguatingDescription'][:30] in json.dumps(d):
                has_disambig = True
        except: errs += 1
    print(f'  {f}: {len(blocks)} blocks, {errs} errors, disambig present={has_disambig}')
