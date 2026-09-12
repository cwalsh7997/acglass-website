# Launch tripwire log

Phase 6 artifact. Required alongside the runbook and never written.

Baseline frozen at `.github/agent-state/state/baseline-frozen-2026-09-09/`, made
read-only. Structural counts, the 23-check result, and the live response headers.

## Thresholds

From the phase-6 spec. HALT means stop the rollout and diagnose. ROLLBACK means
revert the deploy. These are not negotiable downward after launch, which is the
entire point of fixing them beforehand.

| metric | HALT | ROLLBACK |
|---|---|---|
| Organic clicks | -20% sustained 7 days | -35% sustained 5 days |
| Indexed pages | -20% |, |
| Form submissions | -25% sustained 14 days | -40% sustained 7 days |

## Monitoring cadence

    days 0-3     every 4 hours
    days 4-14    daily
    days 15-45   weekly
    days 46-90   weekly, then biweekly
    day 90       written closeout, baseline vs current, each consolidation
                 phase's effect isolated

## Structural baseline, 2026-09-09

Measured, not estimated.

| metric | value |
|---|---:|
| Tracked HTML files | 1,593 |
| Sitemap URLs | 901 |
| Indexable pages | 1,103 |
| Redirect stubs | 58 |
| Orphans not in sitemap | 108 |
| Sitemapped orphans | 4 |
| Broken internal links | 0 |
| Checks passing | 14 of 23 |

## What I cannot baseline, and it is the half that matters

**Organic clicks, indexed page count and form submissions are all unmeasurable from
here.** Two of the three headline thresholds are traffic metrics and I have no Search
Console or GA4 access. A percentage threshold against a baseline nobody recorded is
not a tripwire, it is a number in a document.

Before any launch window, someone with Search Console and GA4 access has to record:

    organic clicks        trailing 28 days, and the same 28 days last year
    indexed pages         Coverage report, valid count
    form submissions      trailing 28 days, per form
    top 20 queries        clicks and average position
    top 20 landing pages  clicks

Paste those into this file under a dated heading. Until then the rollout has no
tripwire, whatever this document says.

## Rollback path

Every phase branch is intact and pushed: `refresh/p0` through `refresh/p6-seo-launch`,
stacked, PRs #111 to #117. Rollback is `git revert` of the merge commit, not a force
push and not a history rewrite.

The one thing revert does NOT undo is anything applied at Cloudflare, because that
configuration lives outside this repo. If the three security headers or a Transform
Rule go in, record them here with the date so a rollback knows to remove them.

## Launch window

Google's site-move guidance: split the move into chunks, change one thing at a time,
move during a low traffic period, and expect Search to take "a few weeks or more" to
reflect it.

For ACG that is a weekend or a weekday evening. Never the Monday of a bid week.

## Entries

_None. Nothing has launched._
