#!/usr/bin/env bash
# Out-of-state service claims must be noindexed.
#
# ACG is a Florida contractor. Pages asserting "licensed contractor serving
# <another state>" make a licensure claim ACG has not evidenced to me, so they
# must not be served to search engines. Seven such pages were already noindexed
# in an earlier pass; three long-slug twins were missed and stayed indexable,
# their ONLY difference from the handled twin being the robots tag. This check
# exists so that gap cannot reopen.
#
# ALLOWLIST, not a denylist: it matches one assertive ACG self-claim shape and
# leaves every other mention of another state alone. A page may discuss Georgia
# all day. It may not claim ACG is a licensed contractor serving Georgia while
# indexable.
source "$(dirname "$0")/_lib.sh"

STATES='Alabama|Georgia|Tennessee|Mississippi|South Carolina|North Carolina|Louisiana|Texas|Virginia|Kentucky|Arkansas|Missouri|Ohio|New York|California'
fail=0
while IFS= read -r p; do
  [ -z "$p" ] && continue
  case "$p" in .github/*) continue;; esac
  grep -qi 'name="robots"[^>]*noindex' "$ROOT/$p" || {
    printf '  %s :: claims service in another state and is indexable\n' "$p"
    fail=$((fail+1))
  }
done <<< "$(git -C "$ROOT" grep -lIiE "(licensed|certified)[^<.]{0,40}contractor serving ($STATES)" -- '*.html')"

[ "$fail" -eq 0 ] && { say "PASS    out-of-state-claims (every out-of-state claim page is noindexed)"; exit 0; }
say "FAIL    out-of-state-claims: $fail indexable page(s)"
exit 1
