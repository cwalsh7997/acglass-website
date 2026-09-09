#!/usr/bin/env bash
# Secondary-office claims are pinned until someone confirms the offices exist.
#
# ACG's headquarters at 700 S Rosemary Ave, West Palm Beach is asserted on 1,020
# schema nodes and is not in question. Two OTHER addresses are also published as
# ACG regional offices, in body text and in machine-readable LocalBusiness schema:
#
#   4850 Tamiami Trail N, Suite 301, Naples FL 34103
#   3031 N Rocky Point Dr W, Suite 600, Tampa FL 33607
#
# A structured-data office claim is stronger than a sentence. Google may use it
# for local pack eligibility, so if an office is not real it is not a wording
# problem, it is a false business location submitted to a search engine. If the
# offices ARE real, deleting them would throw away legitimate local presence.
#
# I cannot tell which from inside the repo, so this check does not decide. It
# pins the page counts so the claim cannot quietly spread to more pages while
# unresolved, and fails to keep it visible. Logged as PC-19.
#
# To clear: confirm or deny each office, record it in decisions.md, then either
# raise the expected counts here or remove the claim sitewide.
source "$(dirname "$0")/_lib.sh"

check() { # label, needle, expected
  local n; n=$(git -C "$ROOT" grep -lIF "$2" -- '*.html' | grep -vc '^\.github/')
  if [ "$n" -ne "$3" ]; then
    printf '  %s: on %s pages, pinned at %s. The claim moved.\n' "$1" "$n" "$3"; return 1
  fi
  printf '  %s: %s pages (pinned, unresolved)\n' "$1" "$n"; return 0
}
drift=0
check "Naples office" "4850 Tamiami Trail" 17 || drift=1
check "Tampa office"  "3031 N Rocky Point" 17 || drift=1
[ "$drift" -eq 1 ] && { say "FAIL    office-claims: a pinned claim changed page count"; exit 1; }
say "FAIL    office-claims: 2 unconfirmed office addresses published in schema"
exit 1
