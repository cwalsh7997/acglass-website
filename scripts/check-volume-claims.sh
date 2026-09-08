#!/usr/bin/env bash
# D6: 350+ and 1,000,000+ SF are APPROVED and must stay. One value, one format.
source "$(dirname "$0")/_lib.sh"
v1=$(gg -oE '[0-9,]+\+ (commercial )?projects' | sed 's/.*://' | sort | uniq -c | sort -rn)
v2=$(gg -oE '[0-9,]+\+ ?(SF|sq\.? ?ft|square feet)' | sed 's/.*://' | sort | uniq -c | sort -rn)
say "        project-count variants:";  printf '%s\n' "$v1" | sed 's/^/          /' | head -6
say "        square-footage variants:"; printf '%s\n' "$v2" | sed 's/^/          /' | head -6
p=$(gg -lF '350+' | wc -l | tr -d ' ')
[ "$p" -eq 0 ] && { say "FAIL    volume-claims: approved '350+' claim has disappeared"; exit 1; }
say "PASS    volume-claims (350+ on $p pages; variants above for review)"; exit 0
