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

## PC-01 UPDATE. The licence sweep is 11,319 occurrences, not a handful
**Measured 2026-09-08 after defect 1 was fixed. This changes the question.**

`1531993` renders **11,319 times across 1,550 of 1,593 pages**. It is not confined to
the licence page. The four dominant forms:

| Count | Form |
|---:|---|
| 1,509 | `...certification in progress. FL CGC #1531993. UEI QTQYMLLL9PS4.` (footer compliance line) |
| 1,504 | `American Commercial Glass, Inc. · FL CGC #1531993 · Woman-owned business` |
| 933 + 366 | `"isoNCode": "FL:CGC1531993"` inside JSON-LD `hasCredential` |
| 421 | `<div class="stat-label">#1531993</div>` in a stat block |

The PC-01 default was set on the assumption this was a small sweep. It is a
sitewide change touching almost every page, and the footer and JSON-LD forms are
SEO-visible.

**I did not execute it.** Removing the number from 1,550 pages on an unconfirmed
premise, in one pass, is the kind of change that should be made once and correctly.

**Three options, and the middle one is my recommendation:**

1. **Remove sitewide.** Follows the stated PC-01 default literally. Largest diff,
   loses a genuine trust signal from every footer and every JSON-LD credential node.
2. **Confirm the number first, then attribute at the two places a human reads it**
   (the licence page and the footer compliance line), and leave the JSON-LD
   `hasCredential` node as the machine-readable credential it already is.
   `hasCredential` is structured data, not a rendered claim, and Schema.org's
   `EducationalOccupationalCredential` has no qualifying-agent field to carry an
   attribution sentence anyway.
3. **Remove from the 421 stat-block instances only**, where the number is displayed
   as a decorative statistic with no context at all, and hold the rest.

**Default if unanswered: option 3.** It removes the number from the one place it
renders with no explanatory context, is a small reversible diff, and leaves the
compliance and structured-data uses intact pending your answer on the number itself.

_2026-09-08_

## PC-09. Stock imagery is live on an indexable page
**Phase 4 · Hard stop 3 · rules/01 s.10 calls this an instant rejection**

`multifamily-commercial-glazing-florida/index.html` returns 200, carries no noindex,
and renders **five images from `/images/stock/`**:
`multifamily-1.jpg`, `multifamily-2.jpg`, `multifamily-3.jpg`, `glass-detail-1.jpg`,
`curtainwall-1.jpg`.

rules/01 section 10 bans "stock or AI-generated imagery of glass, buildings, workers,
or hard hats" as an instant rejection. D10 routes any image with unverified rights to
the `TypographicPlate` fallback, which is component 18 and is already built.

The other 31 files in `images/stock/` are referenced by nothing.

**Default if unanswered: swap the five for `TypographicPlate`, which keeps the page's
layout, section count and component count rather than shrinking around the gap, then
delete all 36 unreferenced stock files.** I did not execute it because it is a
visible design change on a live page and I cannot screenshot-verify it here.

## PC-10. Image rights are unverified on 1,007 of 1,428 files
**Phase 4 · Hard stop 3 · `check-image-rights.sh` now FAILS, correctly**

The CSV is populated from the real tree. Source category was inferred from path,
which is evidence of location, not of rights:

| rights_status | files |
|---|---:|
| owned (`/infographics/`, `/brand/`: ACG-authored artwork) | 421 |
| **unverified** | **1,007** |

935 are `unknown` category, dominated by `images/projects/` at 849 files.

The check moved from CONFIG to FAIL and that is progress, not regression: CONFIG meant
"cannot validate", FAIL means "validated, and 1,007 files have no recorded rights".

**Default if unanswered: nothing publishes from an unverified path in later phases;
`TypographicPlate` is used instead.** One batched answer per project, not per file,
is all that is needed. See the existing `image-source-categories` request.
