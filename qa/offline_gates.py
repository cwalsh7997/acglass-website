#!/usr/bin/env python3
"""Offline gates: real upscale check against file dimensions, and the dash gate."""
import json, os, re, sys, glob
from PIL import Image

root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(root)
fails = []

# ---------- upscale gate ----------
rep = json.load(open('qa/report.json'))
dims = {}
def natural(path):
    p = path.lstrip('/')
    if p not in dims:
        dims[p] = Image.open(p).size if os.path.exists(p) else None
    return dims[p]

worst = {}
for ctx, v in rep.items():
    if 'rendered' not in v.get('images', {}): continue
    dpr = 1
    for r in v['images']['rendered']:
        n = natural(r['file'])
        if not n: fails.append(f'{ctx}: missing file {r["file"]}'); continue
        need = r['layoutWidth'] * dpr
        ratio = need / n[0]
        key = (ctx, r['file'])
        worst[key] = ratio
        if need > n[0] + 1:
            fails.append(f'UPSCALED {ctx}: {r["file"]} natural {n[0]}px drawn at {need}px')
top = sorted(worst.items(), key=lambda kv: -kv[1])[:5]
print('closest-to-native images (layout px / natural px):')
for (ctx, f), r in top:
    print(f'  {r:.2f}  {ctx}  {f}')

# ---------- dash gate ----------
BAD = {
    '\u2014': 'em dash', '\u2013': 'en dash', '\u2012': 'figure dash',
    '\u2011': 'non-breaking hyphen', '\u2015': 'horizontal bar', '\u2212': 'minus sign',
}
ENT = ['&mdash;', '&ndash;', '&#8211;', '&#8212;', '&#8209;', '&#x2011;', '&#x2013;', '&#x2014;']
files = sorted(glob.glob('**/*.html', recursive=True) + glob.glob('**/*.css', recursive=True))
files = [f for f in files if not f.startswith('qa/')]
scanned = 0
for f in files:
    raw = open(f, encoding='utf-8').read()
    # the platform injects an inline-edit script at the end of every page whose JS
    # comments contain em dashes; it is not authored site source, so it is excluded
    body = raw.split('<script data-pplx-inline-edit')[0]
    scanned += 1
    for i, line in enumerate(body.splitlines(), 1):
        for ch, name in BAD.items():
            if ch in line:
                fails.append(f'DASH {f}:{i} {name} -> {line.strip()[:90]}')
        for e in ENT:
            if e in line:
                fails.append(f'DASH-ENTITY {f}:{i} {e} -> {line.strip()[:90]}')
print(f'dash gate scanned {scanned} authored html/css files')

if fails:
    print('\nFAILURES:')
    for f in fails: print(' ', f)
    sys.exit(1)
print('\nOFFLINE GATES PASS')
