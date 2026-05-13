#!/usr/bin/env python3
"""
Add a brand disambiguation footer link to every HTML page that contains the
existing 'Built with precision.' span. Adds a visible line above the copyright
that reads:
  ACG | American Commercial Glass — Florida commercial glazing contractor. 
  Not affiliated with ACG Glass & Metals or AGC Inc.
The anchor 'ACG | American Commercial Glass' links to /acg.html.

Idempotent: skipped if the marker string already exists on the page.
"""
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MARKER = 'data-acg-disambig-footer'

INSERT_SNIPPET = (
    '\n      <div class="acg-disambig-footer" ' + MARKER + '="1" '
    'style="border-top:1px solid rgba(255,255,255,0.06);padding:14px 0 6px;'
    'margin-top:8px;font-family:var(--mono, ui-monospace, SFMono-Regular, Menlo, monospace);'
    'font-size:11px;letter-spacing:0.04em;color:rgba(255,255,255,0.55);text-align:left;">'
    '<a href="/acg.html" '
    'style="color:#E11320;text-decoration:none;font-weight:600;letter-spacing:0.06em;text-transform:uppercase;" '
    'aria-label="ACG | American Commercial Glass disambiguation">'
    'ACG | American Commercial Glass'
    '</a>'
    ' &nbsp;&middot;&nbsp; Florida commercial glazing contractor '
    '&nbsp;&middot;&nbsp; CGC1531993 '
    '&nbsp;&middot;&nbsp; <span style="color:rgba(255,255,255,0.4);">Not affiliated with ACG Glass &amp; Metals or AGC Inc.</span>'
    '</div>\n'
)

# Anchor we insert before
ANCHOR = '<div class="footer-bottom">'

# Files to skip
SKIP = {'404.html'}

changed = 0
skipped = 0
unchanged = 0
total_html = 0

for fname in sorted(os.listdir(ROOT)):
    if not fname.endswith('.html'):
        continue
    if fname in SKIP:
        continue
    total_html += 1
    path = os.path.join(ROOT, fname)
    try:
        with open(path, encoding='utf-8') as f:
            html = f.read()
    except Exception as e:
        print(f'SKIP {fname}: read error {e}')
        skipped += 1
        continue
    if MARKER in html:
        unchanged += 1
        continue
    if ANCHOR not in html:
        unchanged += 1
        continue
    new_html = html.replace(ANCHOR, INSERT_SNIPPET + '      ' + ANCHOR, 1)
    if new_html == html:
        unchanged += 1
        continue
    with open(path, 'w', encoding='utf-8') as f:
        f.write(new_html)
    changed += 1

print(f'HTML files scanned: {total_html}')
print(f'Patched: {changed}')
print(f'Unchanged: {unchanged}')
print(f'Skipped: {skipped}')
