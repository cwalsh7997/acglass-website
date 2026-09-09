#!/usr/bin/env python3
"""D3: no third-party name publishes without an approval row.

Parsed with the csv module, not awk -F,. The first version of this check used
awk and reported PASS with 40 unapproved rows sitting in the file, because a
quoted field containing a comma shifts every column after it. A check that
falsely passes is worse than no check.
"""
import csv, os, sys

ROOT = sys.argv[1] if len(sys.argv) > 1 else "."
p = os.path.join(ROOT, ".github/agent-state/state/project-approvals.csv")
if not os.path.isfile(p):
    print("CONFIG  third-party-approval: ledger missing")
    sys.exit(3)

rows = list(csv.DictReader(open(p)))
if not rows:
    print("CONFIG  third-party-approval: ledger is empty, cannot validate")
    sys.exit(3)

un = [r for r in rows if r.get("status", "").strip().upper() != "APPROVED"]
if not un:
    print(f"PASS    third-party-approval ({len(rows)} items, all approved)")
    sys.exit(0)

occ = sum(int(r.get("pages") or 0) for r in un)
by = {}
for r in un:
    by[r["item_type"]] = by.get(r["item_type"], 0) + 1
print(f"  {len(un)} of {len(rows)} third-party items unapproved, across {occ:,} page-occurrences")
for k in sorted(by):
    print(f"     {by[k]:>3}  {k}")
print("  request: .github/agent-state/state/approvals/PHASE-6-approval-request.md")
print(f"FAIL    third-party-approval: {len(un)} unapproved item(s)")
sys.exit(1)
