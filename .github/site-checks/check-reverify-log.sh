#!/usr/bin/env bash
# Every time-bound published fact carries a re-verification date.
#
# A contractor site is full of facts with a shelf life: SAM registration, product
# approvals, insurance, licence status, and copy that dates itself. They do not
# fail loudly when they expire, they just quietly become false, and the reader who
# notices first is usually a plans examiner or a GC's prequal reviewer.
#
# This check does not verify the facts. It verifies that each one has an owner and
# a date to check it on, and fails while any is UNKNOWN.
source "$(dirname "$0")/_lib.sh"
CSV="$ROOT/.github/agent-state/state/reverify.csv"
[ -f "$CSV" ] || { say "CONFIG  reverify-log: reverify.csv missing"; exit 3; }
python3 - "$CSV" <<'PY'
import csv, sys, collections
rows = list(csv.DictReader(open(sys.argv[1])))
unknown = [r for r in rows if r["reverify_on"].strip().upper() == "UNKNOWN"]
by = collections.Counter(r["fact"] for r in unknown)
for f, n in by.most_common():
    pages = sum(int(r["pages"]) for r in unknown if r["fact"] == f)
    print(f"  {f}: {n} item(s), no re-verification date, {pages} page(s)")
if not unknown:
    print(f"PASS    reverify-log ({len(rows)} time-bound facts, all dated)")
    sys.exit(0)
print(f"FAIL    reverify-log: {len(unknown)} of {len(rows)} time-bound facts undated")
sys.exit(1)
PY
