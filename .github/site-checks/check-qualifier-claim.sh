#!/usr/bin/env bash
# The published qualifier of record must match the confirmed one.
#
# RESOLVED 2026-09-09. Connor confirmed he is the qualifier of record on CGC
# #1531993, which is what 5 pages have been publishing. D9 asserted the licence was
# Jeff Walsh's; it was written on a wrong premise and D9 obligation 3 required this
# confirmation before publishing an attributed sentence. See decisions.md.
#
# The check now guards the opposite direction from before: it fails if a DIFFERENT
# name is published as qualifier of record, or if the confirmed name stops appearing
# alongside the claim. Jeff Walsh must not appear as qualifying agent anywhere,
# because he is not one.
source "$(dirname "$0")/_lib.sh"
CFGF="$ROOT/.github/agent-state/config/license.txt"
NAME=$(sed -n 's/^ATTRIBUTION=//p' "$CFGF" | head -1)
[ -z "$NAME" ] && { say "CONFIG  qualifier-claim: no ATTRIBUTION in license.txt"; exit 3; }

fail=0
# every page asserting a qualifier of record must name the confirmed person
while IFS= read -r p; do
  [ -z "$p" ] && continue
  grep -qF "$NAME" "$ROOT/$p" || {
    printf '  %s: names a qualifier of record without "%s"\n' "$p" "$NAME"; fail=$((fail+1)); }
done <<< "$(git -C "$ROOT" grep -lI 'qualifier of record' -- '*.html' | grep -v '^\.github/')"

# and the superseded name must not be published as qualifying agent
sup=$(git -C "$ROOT" grep -lIiE 'qualifying agent[^.<]{0,30}jeff|jeff[^.<]{0,30}qualifying agent' -- '*.html' | grep -vc '^\.github/')
[ "$sup" -gt 0 ] && { printf '  %s page(s) publish Jeff Walsh as qualifying agent. D9 was superseded.\n' "$sup"; fail=$((fail+1)); }

n=$(git -C "$ROOT" grep -lI 'qualifier of record' -- '*.html' | grep -vc '^\.github/')
[ "$fail" -eq 0 ] && { say "PASS    qualifier-claim ($n page(s), all name the confirmed qualifier $NAME)"; exit 0; }
say "FAIL    qualifier-claim: $fail problem(s)"
exit 1
