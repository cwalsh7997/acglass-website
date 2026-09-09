#!/usr/bin/env bash
# Who is the qualifier of record on CGC #1531993?
#
# The site answers this on 5 pages, by name, and invites verification:
#
#   "Connor Walsh is the President of American Commercial Glass and the qualifier
#    of record for Florida Certified General Contractor license CGC #1531993"
#   "publicly verifiable at the Florida DBPR public license search"
#
# The repo's own config disagrees. .github/agent-state/config/license.txt carries
# ATTRIBUTION=Jeff Walsh and marks the whole thing UNCONFIRMED. Jeff Walsh appears
# on zero served pages. So two different people are recorded as qualifier for one
# license number, and only one of them can be right.
#
# WHY THIS IS WORSE THAN A NORMAL WORDING ERROR. Qualifier of record is a legal
# designation under F.S. 489, not a job title. The site publishes it on
# prequalification pages, tells the reader it is verifiable on DBPR, and elsewhere
# actively coaches general contractors to check whether a glazier's qualifier
# recently changed and to treat that as a yellow flag. If DBPR shows a different
# name, the GC most likely to look is the one being asked to award work, on the
# page written to win it.
#
# I cannot read DBPR from here and will not guess between two named people on a
# licensing question. This pins the count and fails until someone confirms the
# name on the actual DBPR record. Logged as PC-21.
source "$(dirname "$0")/_lib.sh"
n=$(git -C "$ROOT" grep -lI "qualifier of record" -- '*.html' | grep -vc '^\.github/')
printf '  %s page(s) name a qualifier of record for CGC #1531993\n' "$n"
printf '  config/license.txt says the attribution is "Jeff Walsh", status UNCONFIRMED\n'
printf '  "Jeff Walsh" appears on 0 served pages\n'
[ "$n" -ne 5 ] && { say "FAIL    qualifier-claim: count moved from 5 to $n while unresolved"; exit 1; }
say "FAIL    qualifier-claim: unconfirmed qualifier named on $n page(s)"
exit 1
