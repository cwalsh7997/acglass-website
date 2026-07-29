#!/usr/bin/env python3
"""Monthly NOA hub status check.

Reports verification gaps and stale entries. Does NOT modify data — it only
emits a status summary to STDOUT and a non-zero exit code if any system has
been 'pending verification' for more than 90 days.

This script intentionally does NOT fabricate approvals. Live portal fetches are
unreliable from CI (robots.txt + session cookies on floridabuilding.org), so
the human in the loop verifies and updates /noa/data.json by hand.

Run: python3 scripts/noa-status-check.py
"""
import json
import sys
from datetime import date, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
DATA = json.loads((ROOT / 'noa' / 'data.json').read_text())

today = date.today()
pending_count = 0
stale_count = 0
verified_count = 0
total = 0
stale_entries = []

for key, partner in DATA['partners'].items():
    for sys_row in partner['systems']:
        total += 1
        is_pending = (
            isinstance(sys_row.get('fl_pa'), str)
            and sys_row['fl_pa'].lower().startswith('pending')
        )
        if is_pending:
            pending_count += 1
            last_attempted = sys_row.get('last_attempted')
            if last_attempted:
                age = (today - datetime.fromisoformat(last_attempted).date()).days
                if age > 90:
                    stale_count += 1
                    stale_entries.append(
                        f"  - {partner['label']} / {sys_row['series']}: "
                        f"pending {age} days (last attempt {last_attempted})"
                    )
        else:
            verified_count += 1

print(f"=== ACG NOA Hub Status — {today.isoformat()} ===")
print(f"Total systems tracked: {total}")
print(f"Verified: {verified_count}")
print(f"Pending verification: {pending_count}")
print(f"Stale (>90 days pending): {stale_count}")
if stale_entries:
    print("\nStale entries:")
    for e in stale_entries:
        print(e)

# Exit non-zero if anything is stale > 90 days
sys.exit(1 if stale_count > 0 else 0)
