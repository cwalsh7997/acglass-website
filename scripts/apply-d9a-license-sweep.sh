#!/usr/bin/env bash
# D9a item 5, ready to run. NOT run automatically. See PC-21.
#
# D9 (locked): the contractor license is held by Jeff Walsh, ACG's qualifying
# agent. "It is not Connor's license."
# D9a item 5 (locked): if the number is not confirmed as Jeff's by the time the
# sweep executes, remove every occurrence sitewide rather than ship a partially
# attributed site.
#
# The number is still unconfirmed, so the pre-authorised path is removal. This
# script does it. It is kept separate and manual because it strips a licensing
# credential from 1,550 pages, and if the DBPR record actually names Connor then
# removal is the wrong direction and costly to undo across that many files.
#
#   ./scripts/apply-d9a-license-sweep.sh --dry-run   # counts only, changes nothing
#   ./scripts/apply-d9a-license-sweep.sh --apply     # performs the removal
#
# One DBPR lookup makes this unnecessary. If the record names Jeff, run --apply,
# then re-add with the D9 attribution pattern. If it names Connor, the config is
# stale and nothing on the site needs to change.
set -euo pipefail
cd "$(dirname "$0")/.."
MODE="${1:---dry-run}"
n=$(git grep -lI '1531993' -- '*.html' | grep -vc '^\.github/')
occ=$(git grep -oI '1531993' -- '*.html' | grep -vc '^\.github/')
echo "pages carrying the number: $n"
echo "occurrences:               $occ"
if [ "$MODE" != "--apply" ]; then
  echo "dry run. nothing changed. pass --apply to execute D9a item 5."
  exit 0
fi
python3 - <<'PY'
import sys, re
sys.path.insert(0, "scripts")
from sweep_files import sweep_files
pat = re.compile(r'\s*(?:CGC\s*#?\s*)?1531993\b')
n = 0
for p in sweep_files("*.html"):
    d = open(p, encoding="utf-8", errors="replace").read()
    new = pat.sub("", d)
    if new != d:
        open(p, "w", encoding="utf-8").write(new)
        n += 1
print(f"stripped the number from {n} files")
PY
echo "now emit the NEEDS token and re-run scripts/verify.sh"
