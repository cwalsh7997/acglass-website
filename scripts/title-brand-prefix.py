#!/usr/bin/env python3
"""Add 'ACG' or 'ACG (American Commercial Glass)' brand prefix to title tags
that currently lack the brand in their title — high-priority pages first.

Goal: every search result that mentions ACG must look like ACG in the SERP,
not like something Google should autocorrect away from."""
import re
from pathlib import Path

ROOT = Path('/home/user/workspace/acglass-website')

TITLE_RE = re.compile(r'<title>(.*?)</title>', re.IGNORECASE | re.DOTALL)

# Pages where we want the title to BEGIN with the brand
HIGH_PRIORITY = [
    'index.html', 'about.html', 'services.html', 'portfolio.html',
    'commercial-glazing-west-palm-beach.html', 'commercial-glazing-naples.html',
    'commercial-glazing-tampa.html', 'commercial-glazing-miami.html',
    'commercial-glazing-fort-lauderdale.html', 'commercial-glazing-nashville-tn.html',
    'florida-hvhz-glazing-contractor.html', 'miami-hvhz-glazing-contractor.html',
    'storefront-vs-curtainwall.html', 'curtainwall-vs-window-wall.html',
    'commercial-glass-cost-data.html',
    'curtainwall-installation.html', 'commercial-storefront-systems.html',
    'window-wall-systems.html', 'impact-windows-doors-florida.html',
    'fire-rated-glass-systems.html',
    'eswindows-installer-florida.html', 'euro-wall.html',
    'pgt-installer-florida.html', 'allegion-installer-florida.html',
    'tgp-installer-florida.html', 'slimpact-installer-florida.html',
    'bid.html', 'bid-hub.html', 'contact.html', 'send-plans.html',
    'manufacturers.html', 'press.html', 'ask.html', 'glossary.html',
    'project-map.html', 'partners.html',
]

def needs_acg_prefix(title: str) -> bool:
    """Title already contains 'ACG' or 'American Commercial Glass'?"""
    lower = title.lower()
    return not ('acg' in lower or 'american commercial glass' in lower)

modified = 0
already_branded = 0
missing = []

for rel in HIGH_PRIORITY:
    fp = ROOT / rel
    if not fp.exists():
        missing.append(rel)
        continue
    html = fp.read_text()
    m = TITLE_RE.search(html)
    if not m:
        continue
    title = m.group(1).strip()
    if not needs_acg_prefix(title):
        already_branded += 1
        continue
    # Insert ' | ACG' suffix (after stripping any existing trailing brand-ish suffix)
    new_title = title
    # Skip if title already ends with appropriate brand
    if not (new_title.endswith('| ACG') or new_title.endswith('| American Commercial Glass')):
        # Trim trailing pipes
        new_title = re.sub(r'\s*\|\s*$', '', new_title)
        new_title = new_title.rstrip() + ' | ACG'
    if new_title != title:
        # Verify length not blown out
        if len(new_title) > 65:
            # Try just appending
            continue
        html = html.replace(f'<title>{title}</title>', f'<title>{new_title}</title>', 1)
        fp.write_text(html)
        modified += 1
        print(f"  OK  {rel}")
        print(f"      OLD: {title}")
        print(f"      NEW: {new_title}")

print()
print(f"Branded: {modified} pages")
print(f"Already branded: {already_branded}")
if missing:
    print(f"Missing: {missing}")
