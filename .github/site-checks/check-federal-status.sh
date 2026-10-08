#!/usr/bin/env bash
# D1: SAM.gov status identical across copy, JSON-LD, OG, Twitter, llms.txt.
#
# D1 is a LOCKED decision and it carried an explicit obligation: qualifications.html
# read "Federal registration in process", D1 calls that false, and says it "must be
# corrected in phase 0". It was not. It sat wrong through six phases while this
# check reported CONFIG instead of FAIL, because of a WARN-ONLY escape hatch that
# was conditioned on llms.txt shipping.
#
# llms.txt has shipped. The escape hatch is removed. ACG is registered and current
# through 2027-07-17, UEI QTQYMLLL9PS4, CAGE 234B0, and saying otherwise understates
# federal readiness on the page GCs and agencies actually read.
source "$(dirname "$0")/_lib.sh"
out=$(ggi -E 'registration in process|not yet registered|pending SAM')
n=$(printf '%s' "$out" | grep -c . )
if [ "$n" -gt 0 ]; then
  printf '%s\n' "$out" | cut -c1-140 | sed 's/^/  /'
  say "FAIL    federal-status: $n contradiction(s) with D1"; exit 1
fi
say "PASS    federal-status (UEI QTQYMLLL9PS4, CAGE 234B0, no contradictions)"; exit 0
