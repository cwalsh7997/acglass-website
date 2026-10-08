#!/usr/bin/env bash
# D8: Buy American pages are never-touch. Fails if one appears in the diff.
#
# AUTHORISED EXCEPTIONS, added 2026-09-09. The deny list exists to stop
# UNAUTHORISED edits, and an edit Connor explicitly asked for is not one. But
# "Connor said it was fine" is not a mechanism and would rot into a loophole, so an
# authorisation is pinned to the exact file content in
# deny-list-authorized-edits.txt. If an authorised page changes again by one byte
# the hash stops matching and this fails, which is the behaviour that matters: the
# exception covers one specific reviewed change, not the file forever.
#
# I violated this deny list three times in one session by reasoning past it. The
# lesson was not "be more careful", it was that the rule needed a legitimate way to
# say yes so there was never a reason to route around it.
source "$(dirname "$0")/_lib.sh"
DENY="$ROOT/.github/agent-state/state/deny-list-buy-american.txt"
AUTH="$ROOT/.github/agent-state/state/deny-list-authorized-edits.txt"
[ -f "$DENY" ] || { say "CONFIG  deny-list: not yet generated"; exit 3; }
BASE="${1:-origin/main}"
changed=$(git -C "$ROOT" diff --name-only "$BASE"...HEAD 2>/dev/null)
fail=0; allowed=0
while IFS= read -r p; do
  case "$p" in ''|\#*) continue;; esac
  echo "$changed" | grep -qxF "$p" || continue
  want=""
  [ -f "$AUTH" ] && want=$(awk -v f="$p" '$1==f{print $2}' "$AUTH" | head -1)
  if [ -n "$want" ]; then
    have=$(shasum -a 256 "$ROOT/$p" 2>/dev/null | cut -d' ' -f1)
    if [ "$have" = "$want" ]; then
      printf '  %s: changed, and it matches an authorised edit on file\n' "$p"
      allowed=$((allowed+1)); continue
    fi
    hit "$p" "-" "changed BEYOND its authorised edit. Hash does not match."
    fail=$((fail+1)); continue
  fi
  hit "$p" "-" "never-touch Buy American page in diff"
  fail=$((fail+1))
done < "$DENY"
if [ "$fail" -eq 0 ]; then
  say "PASS    deny-list (no unauthorised Buy American page touched, $allowed authorised)"
  exit 0
fi
say "FAIL    deny-list: $fail"; exit 1
