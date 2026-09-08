#!/usr/bin/env bash
# D8: Buy American pages are never-touch. Fails if one appears in the diff.
source "$(dirname "$0")/_lib.sh"
DENY="$ROOT/.github/agent-state/state/deny-list-buy-american.txt"
[ -f "$DENY" ] || { say "CONFIG  deny-list: not yet generated"; exit 3; }
BASE="${1:-origin/main}"
changed=$(git -C "$ROOT" diff --name-only "$BASE"...HEAD 2>/dev/null)
fail=0
while IFS= read -r p; do
  case "$p" in ''|\#*) continue;; esac
  echo "$changed" | grep -qxF "$p" && { hit "$p" "-" "never-touch Buy American page in diff"; fail=$((fail+1)); }
done < "$DENY"
[ "$fail" -eq 0 ] && { say "PASS    deny-list (no Buy American page touched)"; exit 0; }
say "FAIL    deny-list: $fail"; exit 1
