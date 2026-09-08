# Pending Connor

Every item states a default. Say nothing and I take the default.

## PC-01. License number
**Phase 0 · Hard stop 2 · Blocked: the D9a sitewide attribution sweep**
Is CGC 1531993 Jeff Walsh's certification number, or a business certificate of authority?
**Default if unanswered: the number stays removed sitewide rather than shipping bare.**
Recommendation: take the default. Removing is always safe; shipping it bare is not.
Shipped instead: `check-license-attribution.sh` enforces per-occurrence attribution.
Also blocked: the footer credential block, /licensed-glazing-contractor-florida.html.
_2026-09-08_

## PC-02. County list
**Phase 0 · Hard stop 8 · Blocked: check-geography.sh, which reports CONFIG not PASS**
Which Florida counties does ACG self-perform in? `.agent/config/geography-counties.txt` is empty.
**Default if unanswered: no geography claim validates, and the check never passes.**
Recommendation: list the counties. Until then every location page is unverifiable.
_2026-09-08_

## PC-03. Georgia and Alabama
**Phase 1 · Hard stop 8 · Blocked: disposition of the out-of-state cluster**
ACG carries live Georgia and Alabama geography pages, including byte-identical
abbreviation twins (`commercial-glazing-ga.html` = `commercial-glazing-georgia.html`,
same for `-al`/`-alabama`, both measured at Jaccard 1.00).
Does ACG self-perform, furnish-only, or neither in GA and AL?
**Default if unanswered: neither, and they get the same treatment as the TN cluster.**
_2026-09-08_

## PC-04. Bonding is sitewide, not one node
**Phase 0 · Not a hard stop, a scope correction that needs your eyes before I sweep**
Defect 3 scopes "bonded" to the homepage Organization JSON-LD plus OG and Twitter.
Measured today: **219 pages**, six distinct forms, 118 of them inside city-page meta
descriptions reading "impact-rated, bonded, 48-hour scope letters".
One form is NOT a bonding claim: **"structurally bonded silicone"** (6 pages) is a
glazing technique. A naive strip would corrupt technical copy.
**Default if unanswered: strip the assertive forms on all 219, preserve "structurally
bonded silicone" verbatim, and leave pages that merely discuss bonding as a topic.**
_2026-09-08_
