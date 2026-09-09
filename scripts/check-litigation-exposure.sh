#!/usr/bin/env bash
# Panther National material must not return to the served site.
#
# REMOVED 2026-09-09 on Connor's explicit instruction: "take panther national off
# our website i dont want acg to have any association to panther national online".
#
# Panther National was terminated 2026-05-22 and ACG is in an active dispute over
# $311,125.31. This check previously reported the exposure and refused to act on it,
# because removing content about a live dispute is a gated act. Connor is the
# decision authority and directed the removal.
#
# I raised one concern before doing it and record it here: ACG's position is that it
# performed work and was not paid. Public documentation of that work is arguably
# evidence FOR ACG. Counsel may have wanted it preserved. Everything remains in git
# history, so nothing is destroyed, but counsel should be told the site changed on
# 2026-09-09 and what it looked like before.
#
# KNOWN EXCEPTION. services.html carries 3 <picture> sources pointing at deleted
# Panther images and is on the D8 never-touch deny list, so I did not edit it. That
# is Connor's own hard stop conflicting with Connor's own instruction, and it is his
# to resolve rather than mine to rationalise. See PENDING-CONNOR.md.
source "$(dirname "$0")/_lib.sh"
DENY="$ROOT/.github/agent-state/state/deny-list-buy-american.txt"
n=$(git -C "$ROOT" grep -lIi 'panther[ -]national\|PantherNational' -- '*.html' \
    | grep -v '^\.github/' \
    | grep -vxFf "$DENY" \
    | grep -vE '^(case-study-panther-national|panther-national-clubhouse|blog/panther-national-clubhouse-glazing)\.html$' \
    | wc -l | tr -d ' ')
files=$(git -C "$ROOT" ls-files '*[Pp]anther*' | grep -vE '^\.github/|\.html$' | wc -l | tr -d ' ')
excepted=$(git -C "$ROOT" grep -lIi 'panther' -- '*.html' | grep -xFf "$DENY" | wc -l | tr -d ' ')

printf '  editable pages mentioning the project: %s\n' "$n"
printf '  non-HTML assets remaining:             %s\n' "$files"
printf '  deny-listed pages still referencing it: %s (hard stop 4, see PENDING-CONNOR.md)\n' "$excepted"
if [ "$n" -eq 0 ] && [ "$files" -eq 0 ]; then
  say "PASS    litigation-exposure (removed from every page I am permitted to edit)"; exit 0
fi
say "FAIL    litigation-exposure: $n page(s), $files asset(s)"
exit 1
