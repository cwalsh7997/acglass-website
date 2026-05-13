#!/usr/bin/env python3
"""Update Naples + Tampa office addresses sitewide.
Old Naples: 4850 Tamiami Trl N Ste 301, Naples FL 34103
New Naples: 1415 Panther Lane Suite 259, Naples FL 34109

Old Tampa:  3031 N Rocky Point Dr W Ste 600, Tampa FL 33607
New Tampa:  400 N Ashley Drive Suite 2600, Tampa FL 33602
"""
import re
from pathlib import Path

ROOT = Path('/home/user/workspace/acglass-website')

# Pairs of (old_pattern, new_value). Use multiple variants to catch different formatting.
REPLACEMENTS = [
    # Naples — full street + suite + city/state/zip
    ('4850 Tamiami Trl N Ste 301, Naples, FL 34103', '1415 Panther Lane Suite 259, Naples, FL 34109'),
    ('4850 Tamiami Trl N Ste 301, Naples FL 34103', '1415 Panther Lane Suite 259, Naples FL 34109'),
    ('4850 Tamiami Trl N Ste 301', '1415 Panther Lane Suite 259'),
    ('4850 Tamiami Trail N Ste 301', '1415 Panther Lane Suite 259'),
    ('4850 Tamiami Trail North Suite 301', '1415 Panther Lane Suite 259'),
    ('4850+Tamiami+Trl+N+Ste+301', '1415+Panther+Lane+Suite+259'),
    # Naples ZIP changes if only zip is referenced separately
    # (Be careful — don't blanket replace 34103 since it might appear elsewhere)
    # Tampa
    ('3031 N Rocky Point Dr W Ste 600, Tampa, FL 33607', '400 N Ashley Drive Suite 2600, Tampa, FL 33602'),
    ('3031 N Rocky Point Dr W Ste 600, Tampa FL 33607', '400 N Ashley Drive Suite 2600, Tampa FL 33602'),
    ('3031 N Rocky Point Dr W Ste 600', '400 N Ashley Drive Suite 2600'),
    ('3031 N. Rocky Point Dr. W. Ste 600', '400 N Ashley Drive Suite 2600'),
    ('3031 N Rocky Point Drive W Suite 600', '400 N Ashley Drive Suite 2600'),
    ('3031+N+Rocky+Point+Dr+W+Ste+600', '400+N+Ashley+Drive+Suite+2600'),
]

modified_count = 0
files_modified = []
for fp in sorted(ROOT.rglob('*.html')):
    if '.git' in fp.parts: continue
    if fp.name in {'404.html'}: continue
    try:
        html = fp.read_text()
    except: continue
    orig = html
    for old, new in REPLACEMENTS:
        html = html.replace(old, new)
    if html != orig:
        fp.write_text(html)
        files_modified.append(str(fp.relative_to(ROOT)))
        modified_count += 1

# Also do JSON, XML files (sitemap)
for fp in sorted(ROOT.rglob('*.xml')):
    if '.git' in fp.parts: continue
    try: c = fp.read_text()
    except: continue
    o = c
    for old, new in REPLACEMENTS: c = c.replace(old, new)
    if c != o:
        fp.write_text(c)
        files_modified.append(str(fp.relative_to(ROOT)))
        modified_count += 1

# ZIPs in standalone form — handle carefully. Naples 34103 → 34109 only when adjacent to Naples context
ZIP_REGEX_REPLACE = [
    # 34103 → 34109 when in Naples address context (within 100 chars of "Naples")
    # Simple approach: only replace when both Naples and the old zip appear in HTML and not in archived address
    # Skip for safety unless we missed something
]

print(f"Modified {modified_count} files")
print(f"Sample modified files (first 15):")
for f in files_modified[:15]:
    print(f"  - {f}")
if len(files_modified) > 15:
    print(f"  ... and {len(files_modified) - 15} more")
