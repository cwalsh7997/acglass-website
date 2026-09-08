#!/usr/bin/env bash
# D9a: every rendered occurrence of the number carries the attribution in the same
# block. Five hits on one page cannot pass on one match.
source "$(dirname "$0")/_lib.sh"
NUM=$(grep '^NUMBER=' "$CFG/license.txt" | cut -d= -f2)
ATTR=$(grep '^ATTRIBUTION=' "$CFG/license.txt" | cut -d= -f2)
out=$(gg -F "$NUM"); total=$(printf '%s' "$out" | grep -c . )
unattr=0
if [ "$total" -gt 0 ]; then
  while IFS=: read -r f ln _; do
    lo=$((ln>3?ln-3:1)); hi=$((ln+3))
    sed -n "${lo},${hi}p" "$ROOT/$f" 2>/dev/null | grep -qF "$ATTR" || {
      printf '  %s:%s: license number without "%s" in the same block\n' "$f" "$ln" "$ATTR"
      unattr=$((unattr+1)); }
  done <<< "$out"
fi
if cfg_incomplete "$CFG/license.txt"; then
  say "CONFIG  license-attribution: number UNCONFIRMED, policy is remove-everywhere."
  say "        occurrences: $total, unattributed: $unattr"
  [ "$total" -gt 0 ] && exit 3 || exit 0
fi
[ "$unattr" -eq 0 ] && { say "PASS    license-attribution ($total occurrences, all attributed)"; exit 0; }
say "FAIL    license-attribution: $unattr of $total unattributed"; exit 1
