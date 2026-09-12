#!/usr/bin/env bash
# D6: the word bonded comes out of JSON-LD, OG and Twitter. Vocabulary family,
# because three live variants were measured on 2026-09-08.
source "$(dirname "$0")/_lib.sh"
pat=$(grep -vE '^#|^$' "$CFG/bonding-vocab.txt" | paste -sd'|' -)
[ -z "$pat" ] && { say "CONFIG  bonding: vocabulary list empty"; exit 3; }
TECH="$CFG/technique-vocab.txt"
# JSON-LD, OG and Twitter, per D6. PLUS body copy carrying a bonding CAPACITY
# FIGURE, which this check did not watch and which was live on 3 pages:
# "Bonding capacity is $3M single / $6M aggregate". D6 obligation 4 says bonding
# capacity is unapproved and questionnaire item 20 is open, so a specific dollar
# figure is exactly the claim it was written to stop.
#
# Only ACG self-claims. A blog telling a GC to ask a glazier for bonding capacity
# is advice, not a claim about ACG.
out=$(ggi -E "$pat" | grep -iE 'ld\+json|og:description|twitter:description|"description"|name="description"')
# Capacity figures in body copy. CONFIRMED 2026-09-09: $3M single / $6M aggregate
# is current, which closes questionnaire item 20. So the check no longer objects
# to the figure, it objects to a DIFFERENT one. Surety capacity changes when the
# surety re-underwrites, and a stale bond number on a prequal page is found by the
# GC asking for the capacity letter.
figs=$(ggi -E '(ACG|American Commercial Glass|our|we)[^.<>]{0,80}(bond|surety)[^.<>]{0,60}\$[0-9.]+ ?M|(surety|bonding) capacity[^.<>]{0,20}(is )?\$[0-9.]+ ?M' \
       | grep -vE '\$3M single ?/ ?\$6M aggregate|\$3M single-project and \$6M aggregate')
out=$(printf '%s\n%s\n' "$out" "$figs" | grep -v '^$')
if [ -f "$TECH" ]; then
  tp=$(grep -vE '^#|^$' "$TECH" | paste -sd'|' -)
  out=$(printf '%s\n' "$out" | grep -viE "$tp")
fi
n=$(printf '%s' "$out" | grep -c . )
[ "$n" -eq 0 ] && { say "PASS    bonding (no bonding claim in JSON-LD, OG or Twitter)"; exit 0; }
printf '%s\n' "$out" | cut -c1-150 | sed 's/^/  /' | head -20
say "FAIL    bonding: $n structured/meta occurrences"; exit 1
