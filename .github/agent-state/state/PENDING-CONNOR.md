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

## PC-05. "48-hour scope letters" is an unsubstantiated performance promise
**Phase 0 · Hard stop 5 · Blocked: the promise stays live meanwhile**
Surfaced while removing the bonding claim from the same sentence. acglass.com promises
48-hour scope letters on approximately 118 page-occurrences (59 pages, meta description
plus og:description each). Nobody has substantiated it.
**Default if unanswered: remove the promise from all pages and replace with a factual
description of responsiveness that does not commit to a number.**
_2026-09-08_

## PC-06. Affirmative bonding capability on the multifamily FAQ
**Phase 0 · Blocked: one page, `can-acg-bid-multifamily-projects-over-2-million/`**
Reads: "Is ACG bonded for multifamily projects? Yes. ACG provides performance and payment
bonds on multifamily projects that require them, with bond capacity letters available
during prequalification."
D6 removes bonding from JSON-LD, OG and Twitter. This is a page FAQ making an affirmative
capability claim, which D6 does not directly rule on, and defect 3 states the bonding
question is unanswered. The phrasing already uses the withheld-to-prequal posture.
**Default if unanswered: leave the sentence as written, since it defers to the
prequalification packet rather than publishing a bond amount.**
_2026-09-08_

## PC-07. check-bonding flags technique pages in structured data
**Not a content defect. A check refinement, logged so it is not mistaken for one.**
The remaining 2 bonding FAILs are pages where "bonded" appears inside JSON-LD as glazing
technique: `structural-silicone-glazing-explained`, `glazed-aluminum-curtain-wall-contractor`,
`glossary`. The technique exclusion is applied to the visible-copy path but not the
structured-data path.
**Default if unanswered: extend the technique exclusion to structured data, then re-run.**
_2026-09-08_

## PC-08. Cloudflare edge rule for /.agent/* and /_internal/*
**Cross-phase · Hard stop 7 (irreversible outside the repo) · Not blocking**
Defense in depth regardless of what the canary shows. `.nojekyll` is present, so
Jekyll is off and every path is served; only `.github/` is reserved by Pages.
Rule: block or 404 any request to `/.agent/*` and `/_internal/*` at the edge.
**Default if unanswered: proceed without it. The canary at `.agent/canary.txt` is
the control, and the agent tree already lives under `_internal/`.**
_2026-09-08_
