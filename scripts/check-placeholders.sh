#!/usr/bin/env bash
# Placeholders, unresolved tokens, square-bracket ban in content files.
source "$(dirname "$0")/_lib.sh"
out=$(gg -E '\[[A-Z][^]]{3,}\]|\{\{NEEDS|TODO|TBD|XXX|FIXME|Lorem|insert .* here')
n=$(printf '%s' "$out" | grep -c . )
[ "$n" -eq 0 ] && { say "PASS    placeholders (none in content)"; exit 0; }
printf '%s\n' "$out" | cut -c1-140 | sed 's/^/  /' | head -20
say "FAIL    placeholders: $n"; exit 1
