#!/usr/bin/env bash
# Deny-list check: fails if a removed project name returns to served HTML.
source "$(dirname "$0")/_lib.sh"
DENY="$ROOT/.github/agent-state/state/deny-list-buy-american.txt"
FROZEN="$ROOT/.github/agent-state/state/byte-frozen-paths.txt"
EXCL=$(mktemp); cat "$DENY" "$FROZEN" 2>/dev/null | grep -v '^#' | grep -v '^$' > "$EXCL"
n=$(git -C "$ROOT" grep -lIi 'panther[ -]national\|PantherNational' -- '*.html' \
    | grep -v '^\.github/' \
    | grep -vxFf "$EXCL" \
    | grep -vE '^(case-study-panther-national|panther-national-clubhouse|blog/panther-national-clubhouse-glazing)\.html$' \
    | wc -l | tr -d ' ')
files=$(git -C "$ROOT" ls-files '*[Pp]anther*' | grep -vE '^\.github/|\.html$' | wc -l | tr -d ' ')
excepted=$(git -C "$ROOT" grep -lIi 'panther' -- '*.html' | grep -xFf "$EXCL" | wc -l | tr -d ' '); rm -f "$EXCL"

printf '  editable pages mentioning the project: %s\n' "$n"
printf '  non-HTML assets remaining:             %s\n' "$files"
printf '  frozen pages still referencing it:      %s (deny list or WPB byte freeze, see PENDING-CONNOR.md)\n' "$excepted"
if [ "$n" -eq 0 ] && [ "$files" -eq 0 ]; then
  say "PASS    removed-projects (removed from every page I am permitted to edit)"; exit 0
fi
say "FAIL    removed-projects: $n page(s), $files asset(s)"
exit 1
