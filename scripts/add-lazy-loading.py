#!/usr/bin/env python3
"""Add loading='lazy' and decoding='async' to <img> tags that don't have them.
Preserve the FIRST <img> on each page (likely above-the-fold / LCP element) as eager."""
import re
from pathlib import Path

ROOT = Path('/home/user/workspace/acglass-website')

IMG_RE = re.compile(r'<img\b([^>]*?)>', re.IGNORECASE)

def fix_img(tag_text: str, is_first: bool) -> str:
    """Return modified <img ...> string."""
    inner = tag_text  # everything between <img and >
    # Skip if already has loading attribute
    has_loading = re.search(r'\bloading\s*=', inner, re.IGNORECASE) is not None
    has_decoding = re.search(r'\bdecoding\s*=', inner, re.IGNORECASE) is not None
    has_fetchpriority = re.search(r'\bfetchpriority\s*=', inner, re.IGNORECASE) is not None

    additions = []
    if is_first:
        # Above-the-fold: eager + high priority, not lazy
        if not has_loading:
            additions.append(' loading="eager"')
        if not has_fetchpriority:
            additions.append(' fetchpriority="high"')
        if not has_decoding:
            additions.append(' decoding="async"')
    else:
        if not has_loading:
            additions.append(' loading="lazy"')
        if not has_decoding:
            additions.append(' decoding="async"')
    return f'<img{inner}{"".join(additions)}>'

def process_file(fp: Path) -> int:
    """Returns number of <img> tags modified."""
    html = fp.read_text()
    matches = list(IMG_RE.finditer(html))
    if not matches:
        return 0

    # Build new string left-to-right
    out = []
    last = 0
    modified = 0
    for idx, m in enumerate(matches):
        out.append(html[last:m.start()])
        new_tag = fix_img(m.group(1), is_first=(idx == 0))
        if new_tag != m.group(0):
            modified += 1
        out.append(new_tag)
        last = m.end()
    out.append(html[last:])
    new_html = ''.join(out)
    if modified:
        fp.write_text(new_html)
    return modified

# Process every HTML file, skipping noindex / template stubs
SKIP = {'404.html', 'location-template-snippet.html', 'google9d45280643313cec.html'}

total_files_modified = 0
total_imgs_modified = 0
files_scanned = 0
for fp in sorted(ROOT.rglob('*.html')):
    if fp.name in SKIP:
        continue
    if '.git' in fp.parts:
        continue
    files_scanned += 1
    n = process_file(fp)
    if n:
        total_files_modified += 1
        total_imgs_modified += n

print(f"Scanned {files_scanned} HTML files")
print(f"Modified {total_files_modified} files")
print(f"Updated {total_imgs_modified} <img> tags")
