#!/usr/bin/env bash
# Placeholders, unresolved tokens, square-bracket ban in content files.
source "$(dirname "$0")/_lib.sh"
ALLOW="$CFG/bracket-allowlist.txt"
raw=$(gg -E '\[[A-Z][^]]{3,}\]|\{\{NEEDS|\\bTODO\\b|\\bTBD\\b|\\bXXX\\b|\\bFIXME\\b|\\bLorem\\b|insert [^<>]{0,40} here')
if [ -f "$ALLOW" ]; then
  pat=$(grep -vE '^#|^$' "$ALLOW" | paste -sd'|' -)
  out=$(printf '%s\n' "$raw" | grep -vE "$pat" | grep -vE '\[(Math|Object|Array|JSON|String|Number|Boolean|Date)\.')
else
  out="$raw"
fi
n=$(printf '%s' "$out" | grep -c . )
[ "$n" -eq 0 ] && { say "PASS    placeholders (none in content)"; exit 0; }
printf '%s\n' "$out" | cut -c1-140 | sed 's/^/  /' | head -20
say "FAIL    placeholders: $n"; exit 1
