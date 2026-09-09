#!/usr/bin/env bash
# D6: the word bonded comes out of JSON-LD, OG and Twitter. Vocabulary family,
# because three live variants were measured on 2026-09-08.
source "$(dirname "$0")/_lib.sh"
pat=$(grep -vE '^#|^$' "$CFG/bonding-vocab.txt" | paste -sd'|' -)
[ -z "$pat" ] && { say "CONFIG  bonding: vocabulary list empty"; exit 3; }
TECH="$CFG/technique-vocab.txt"
out=$(ggi -E "$pat" | grep -iE 'ld\+json|og:description|twitter:description|"description"|name="description"')
if [ -f "$TECH" ]; then
  tp=$(grep -vE '^#|^$' "$TECH" | paste -sd'|' -)
  out=$(printf '%s\n' "$out" | grep -viE "$tp")
fi
n=$(printf '%s' "$out" | grep -c . )
[ "$n" -eq 0 ] && { say "PASS    bonding (no bonding claim in JSON-LD, OG or Twitter)"; exit 0; }
printf '%s\n' "$out" | cut -c1-150 | sed 's/^/  /' | head -20
say "FAIL    bonding: $n structured/meta occurrences"; exit 1
