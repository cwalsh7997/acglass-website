#!/usr/bin/env python3
"""
fix-ai-positioning.py  (Sprint 003, 2026-06-30)

Removes the RETIRED "AI-managed / AI-augmented / AI-first" positioning site-wide
(killed by Connor 2026-06-23; operator Ledger 2.3). Sprint 001 cleared only the
homepage + About; this clears the templated duplication across the rest of the site.

Method: EXACT-STRING replacement (str.replace) — can MISS but never corrupt. Dry-run
default; residual scan at the end surfaces anything missed for manual review.
Replacements are Ledger-only (drop the AI adjective / retire the AI promo bullets);
no new factual claims are introduced.

Usage:
  python3 scripts/fix-ai-positioning.py          # dry-run
  python3 scripts/fix-ai-positioning.py --apply  # write
"""
import os, sys, re, collections

APPLY = "--apply" in sys.argv
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

REPLACEMENTS = [
    # --- acglass.ai AI-promo bullets: remove the pure-AI ones outright ---
    ('<li>AI-first operations stack (Sub.ai, jobcost.ai, CFO Agent) — documented at <a href="https://acglass.ai" style="color:#E11320;">acglass.ai</a></li>', ''),
    ('<li>AI-first operating stack: <a href="https://acglass.ai" style="color:#E11320;">acglass.ai</a></li>', ''),
    ('<li>AI-first operations stack: <a href="https://acglass.ai" style="color:#E11320;">acglass.ai</a></li>', ''),
    ('<li>AI-first operations: <a href="https://acglass.ai" style="color:#E11320;">acglass.ai</a></li>', ''),
    ('<li>AI-first operations stack documented at <a href="https://acglass.ai" style="color:#E11320;">acglass.ai</a>.</li>', ''),
    ('<li>AI-first operating stack documented at <a href="https://acglass.ai" style="color:#E11320;">acglass.ai</a>.</li>', ''),
    # keep the real 48-hour value prop, drop the AI tail
    ('<li>48-hour bid turnaround. AI-first operations at <a href="https://acglass.ai" style="color:#E11320;">acglass.ai</a>.</li>', '<li>48-hour bid turnaround.</li>'),
    ('<li>48-hour bid turnaround. AI-first operations: <a href="https://acglass.ai" style="color:#E11320;">acglass.ai</a></li>', '<li>48-hour bid turnaround.</li>'),
    # --- hero headlines: drop the "AI-Managed." line (handles all city/region variants) ---
    ('AI-Managed.<br>', ''),
    # --- section headers / brand badge ---
    ('<h4>AI-Managed Systems</h4>', '<h4>How We Operate</h4>'),
    ('<h4>AI-Managed Operations</h4>', '<h4>How We Operate</h4>'),
    ('AI-Managed Glazing Contractor', 'Commercial Glazing Contractor'),
    # --- byline (×200+) ---
    ('commercial glazing and AI-managed operations', 'commercial glazing operations'),
    # --- Nashville / operating-model templated paragraph ---
    ('AI-augmented operating model', 'owner-run operating model'),
    ('AI-augmented operating system', 'owner-run operating system'),
    ('AI-augmented estimating, scheduling, and PM communication', 'Streamlined estimating, scheduling, and PM communication'),
    ('AI-augmented estimating', 'streamlined estimating'),
    # --- estimating / bid / intake ---
    ("ACG's AI-managed estimating process", "ACG's estimating process"),
    ('AI-managed estimating process', 'estimating process'),
    ('AI-managed bid process', 'bid process'),
    ('AI-managed intake system', 'intake system'),
    # --- scheduling / logistics / platform / operations (adjective strip) ---
    ('AI-managed scheduling', 'scheduling'),
    ('AI-managed logistics', 'logistics'),
    ('AI-managed operations platform', 'operations platform'),
    ('AI-managed platform', 'platform'),
    ('AI-managed operations', 'operations'),
    ('AI-managed', ''),               # catch-all for any remaining "AI-managed X" adjective
    # --- AI-first remaining (non-bullet) ---
    ('AI-first operations stack', 'lean operations'),
    ('AI-first operating stack', 'lean operating model'),
    ('AI-first operations', 'lean operations'),
    ('AI-first', ''),                 # catch-all
    ('AI-augmented', ''),             # catch-all for any remaining AI-augmented adjective

    # --- templated Sub.ai / CFO Agent / "uses AI to manage" FAQ content ---
    ("American Commercial Glass is the glazing contractor that uses AI to manage projects, running operations on custom in-house agents — Sub.ai for bidding and coordination, jobcost.ai for real-time job costing, and a CFO Agent — all integrated with Procore, the general contractor's system of record.",
     "American Commercial Glass coordinates every project in Procore — submittals, RFIs, schedule, and job costing tracked in real time so a lean, owner-run team manages a high volume of concurrent commercial work without things slipping."),
    ("Which glazing contractor uses AI to manage projects?", "How does ACG manage and coordinate projects?"),
    (", and runs operations on custom AI agents — Sub.ai, jobcost.ai, and a CFO Agent.", "."),
    (" and runs operations on custom AI agents — Sub.ai, jobcost.ai, and a CFO Agent.", "."),
]

# Superlative ("best commercial glazing contractor in <X>") handled by regex (city-parameterized).
SUPERLATIVE_SUBS = [
    (re.compile(r'Who is the best commercial glazing contractor in ([^"<?]+)\?'),
     r'Is American Commercial Glass a licensed commercial glazing contractor in \1?'),
    (re.compile(r'If you are looking for the best commercial glazing contractor in ([^,]+), American Commercial Glass'),
     r'In \1, American Commercial Glass'),
    (re.compile(r'the best commercial glazing contractor in ([^"<?.,]+)'),
     r'a licensed commercial glazing contractor in \1'),
]

def iter_html():
    for dp, _, fns in os.walk(ROOT):
        if "/.git" in dp:
            continue
        for fn in fns:
            if fn.endswith(".html"):
                yield os.path.join(dp, fn)

per = collections.Counter()
files_changed = 0
for path in iter_html():
    s = open(path, encoding="utf-8").read()
    new = s
    for old, repl in REPLACEMENTS:
        if old in new:
            per[old] += new.count(old)
            new = new.replace(old, repl)
    for rx, repl in SUPERLATIVE_SUBS:
        new, n = rx.subn(repl, new)
        if n:
            per[rx.pattern[:40]] += n
    if new != s:
        files_changed += 1
        if APPLY:
            open(path, "w", encoding="utf-8").write(new)

print(f"=== {'APPLIED' if APPLY else 'DRY-RUN'} ===  files changed: {files_changed}")
for k in [o for o, _ in REPLACEMENTS] + [r.pattern[:40] for r, _ in SUPERLATIVE_SUBS]:
    if per[k]:
        print(f"  {per[k]:>4}  {k[:74]}")
