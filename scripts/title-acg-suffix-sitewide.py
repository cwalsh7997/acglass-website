#!/usr/bin/env python3
"""
Add " | ACG" suffix to every page title that:
  1. Does not already contain "ACG" or "American Commercial Glass"
  2. Is a service/location/cornerstone/manufacturer page (not utility)
  3. Title length + suffix stays <= 70 chars (Google cutoff sweet spot)
     If title would exceed 70 chars, trim safely from the end first.

Idempotent. Reports what it changed.
"""
import os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Skip utility pages
SKIP = {
    '404.html', 'search.html', 'sitemap.html',
    'google9d45280643313cec.html', 'location-template-snippet.html',
    'contact.html',   # already brand-heavy
    'privacy.html', 'terms.html',
    'ai-overview.html',  # already has brand
}

# Target patterns: service / location / cornerstone / manufacturer / project pages
TARGET_PATTERNS = [
    r'^commercial-glazing-',
    r'^commercial-storefront-',
    r'^commercial-glass-',
    r'^euro-wall',
    r'^eswindows-',
    r'^pgt-installer',
    r'^allegion-installer',
    r'^tgp-installer',
    r'^slimpact-installer',
    r'^impact-',
    r'^curtainwall-',
    r'^window-wall-',
    r'^storefront-',
    r'^division-08',
    r'^florida-',
    r'^miami-',
    r'^ocean-prime',
    r'^panther-national',
    r'^atlantic-fields',
    r'^wild-blue',
    r'^haines-city',
    r'^baron-shoppes',
    r'^siena-lakes',
    r'^tradewinds-',
    r'^tomoka-',
    r'^gulf-harbour',
    r'^aspen-dental',
    r'^bobcat-',
    r'^bradley-',
    r'^causeway-',
    r'^city-of-',
    r'^cudjoe-',
    r'^illumia-',
    r'^gulfside-',
    r'^rome-',
    r'^westlake-',
    r'^1172-',
    r'^2143-',
    r'^736-',
    r'^aia-g702',
    r'^aia-a201',
    r'^architect-resources',
    r'^automatic-entrance',
    r'^bid-hub',
    r'^bid\.html',
    r'^bid$',
    r'^best-',
    r'^capabilities',
    r'^ask\.html',
    r'^careers',
    r'^author-',
    r'^acg-vs',
    r'^ai-managed',
    r'^ai-overview',  # safety; SKIP catches it
    r'^aia-',
]

SUFFIX = " | ACG"

def is_target(name):
    for p in TARGET_PATTERNS:
        if re.match(p, name):
            return True
    return False

changed = 0
unchanged_no_match = 0
unchanged_has_acg = 0
skipped = 0

for fname in sorted(os.listdir(ROOT)):
    if not fname.endswith('.html'):
        continue
    if fname in SKIP:
        skipped += 1
        continue
    if not is_target(fname):
        unchanged_no_match += 1
        continue
    path = os.path.join(ROOT, fname)
    with open(path) as f: html = f.read()
    m = re.search(r'<title>(.*?)</title>', html, re.S | re.I)
    if not m:
        skipped += 1
        continue
    title = m.group(1).strip()
    if 'ACG' in title or 'American Commercial Glass' in title:
        unchanged_has_acg += 1
        continue
    # Try appending suffix; if too long, trim title and try again
    new_title = (title + SUFFIX).strip()
    if len(new_title) > 70:
        # Trim from end of original title until fits
        target = 70 - len(SUFFIX)
        trimmed = title[:target].rstrip(' —-|·,.')
        new_title = trimmed + SUFFIX
    if new_title == title:
        continue
    new_html = html.replace(m.group(0), f'<title>{new_title}</title>', 1)
    if new_html == html:
        continue
    with open(path, 'w') as f: f.write(new_html)
    changed += 1

print(f'Target pages patched: {changed}')
print(f'Already had ACG brand: {unchanged_has_acg}')
print(f'Skipped (not target):  {unchanged_no_match}')
print(f'Skipped (utility):     {skipped}')
