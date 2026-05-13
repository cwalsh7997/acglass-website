#!/usr/bin/env python3
"""Fix title and meta description length violations from the audit.

Rules:
- Titles > 60 chars → trim by removing brand suffixes like " | ACG", " — American Commercial Glass", etc., then truncate
- Titles < 30 chars → add " | ACG" or extend (we'll just flag, don't auto-extend)
- Descriptions > 160 chars → truncate to 157 + "..."
- Descriptions < 120 chars → flag, don't auto-extend (needs human voice)

Outputs report so we know what was changed.
"""
import re
from pathlib import Path

ROOT = Path('/home/user/workspace/acglass-website')

TITLE_RE = re.compile(r'<title>(.*?)</title>', re.IGNORECASE | re.DOTALL)
META_DESC_RE = re.compile(r'<meta\s+name=["\']description["\']\s+content=["\'](.*?)["\']\s*/?>', re.IGNORECASE | re.DOTALL)

# Brand suffixes to strip if title is too long
SUFFIXES = [
    ' | American Commercial Glass',
    ' | ACG',
    ' — American Commercial Glass',
    ' - American Commercial Glass',
    ' — ACG',
    ' - ACG',
    ' | ACG | American Commercial Glass',
    ' — FL CGC',
    ' | Florida CGC',
]

def trim_title(t: str) -> str:
    """Return a trimmed title <=60 chars where possible."""
    orig = t
    # Strip trailing brand suffix(es)
    for s in SUFFIXES:
        if t.endswith(s):
            t = t[:-len(s)].rstrip(' |—-·')
            if len(t) <= 60:
                return t
    # Replace " — American Commercial Glass" mid-string
    t2 = re.sub(r'\s+[—\-|]\s+American Commercial Glass.*$', '', t)
    if len(t2) <= 60 and t2 != t:
        return t2
    # Replace "Commercial Glazing" with "Glazing" if needed
    if 'Commercial Glazing' in t and len(t) > 60:
        t3 = t.replace('Commercial Glazing', 'Glazing', 1)
        if len(t3) <= 60:
            return t3
    # Hard truncate at word boundary at 57 + …
    if len(t) > 60:
        t4 = t[:57]
        # back off to last space
        sp = t4.rfind(' ')
        if sp > 30:
            t4 = t4[:sp]
        return t4 + '…'
    return t

def trim_description(d: str) -> str:
    """Return a description <=160 chars."""
    if len(d) <= 160:
        return d
    # truncate at word boundary, append …
    cut = d[:157]
    sp = cut.rfind(' ')
    if sp > 100:
        cut = cut[:sp]
    return cut + '…'

stats = {'title_long': 0, 'title_short': 0, 'desc_long': 0, 'desc_short': 0, 'files_modified': 0}
short_titles_list = []
short_descs_list = []

for fp in sorted(ROOT.rglob('*.html')):
    if '.git' in fp.parts: continue
    if fp.name in {'404.html', 'location-template-snippet.html', 'google9d45280643313cec.html'}:
        continue
    html = fp.read_text()
    orig = html

    # Title
    m = TITLE_RE.search(html)
    if m:
        title = m.group(1).strip()
        new_title = title
        if len(title) > 60:
            new_title = trim_title(title)
            stats['title_long'] += 1
        elif len(title) < 30:
            short_titles_list.append((fp.relative_to(ROOT), title, len(title)))
            stats['title_short'] += 1
        if new_title != title:
            html = html.replace(f'<title>{title}</title>', f'<title>{new_title}</title>', 1)

    # Meta description
    md = META_DESC_RE.search(html)
    if md:
        desc = md.group(1).strip()
        new_desc = desc
        if len(desc) > 160:
            new_desc = trim_description(desc)
            stats['desc_long'] += 1
        elif len(desc) < 120:
            short_descs_list.append((fp.relative_to(ROOT), desc, len(desc)))
            stats['desc_short'] += 1
        if new_desc != desc:
            html = html.replace(md.group(0), md.group(0).replace(desc, new_desc), 1)

    if html != orig:
        fp.write_text(html)
        stats['files_modified'] += 1

print(f"Files modified: {stats['files_modified']}")
print(f"Titles trimmed (>60 chars): {stats['title_long']}")
print(f"Titles too short (<30 chars, flagged): {stats['title_short']}")
print(f"Descriptions trimmed (>160 chars): {stats['desc_long']}")
print(f"Descriptions too short (<120 chars, flagged): {stats['desc_short']}")
if short_titles_list:
    print("\nShort titles needing manual extension:")
    for f, t, n in short_titles_list:
        print(f"  {n} chars: {f} — \"{t}\"")
if short_descs_list[:10]:
    print(f"\nShort descriptions needing extension (showing first 10 of {len(short_descs_list)}):")
    for f, d, n in short_descs_list[:10]:
        print(f"  {n} chars: {f}")
