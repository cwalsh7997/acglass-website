#!/usr/bin/env python3
"""Update HTML <img src=> tags that reference infographic PNGs to use WebP versions,
or wrap in <picture> with WebP fallback for browsers that don't support it.
"""
import re
from pathlib import Path

ROOT = Path('/home/user/workspace/acglass-website')

# For static GitHub Pages, simplest reliable change: swap src=...png -> src=...webp
# Modern browser support is universal (>97% globally per caniuse) so we don't need a picture fallback.
# We DO need to preserve all other attributes.

PNG_REF_RE = re.compile(r'(src=["\'])(images/infographics/[^"\']+?)\.png(["\'])', re.IGNORECASE)

# Also catch srcset references
SRCSET_RE = re.compile(r'(srcset=["\'][^"\']*?images/infographics/[^"\']+?)\.png([^"\']*?["\'])', re.IGNORECASE)

# And meta og:image
OG_RE = re.compile(r'(content=["\'][^"\']*?images/infographics/[^"\']+?)\.png(["\'])', re.IGNORECASE)

def process(fp: Path):
    html = fp.read_text()
    orig = html
    html = PNG_REF_RE.sub(r'\1\2.webp\3', html)
    html = SRCSET_RE.sub(r'\1.webp\2', html)
    # For og:image — keep PNG for crawlers that don't support WebP (Facebook does, but some don't)
    # Actually, og:image traditionally PNG/JPG is safer. Skip.
    if html != orig:
        fp.write_text(html)
        return True
    return False

count = 0
for fp in sorted(ROOT.rglob('*.html')):
    if '.git' in fp.parts: continue
    if process(fp): count += 1
print(f"Updated {count} HTML files to use WebP infographic references")
