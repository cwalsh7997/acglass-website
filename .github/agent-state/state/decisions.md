# Decisions

## 2026-09-08. Bonding vocabulary excludes bare "bonding" and "surety"
First pass matched 165 occurrences, nearly all false: pages discussing how to vet a
glazier ("license verification, bonding, NOA review"). Narrowed to assertive
self-claims only. Recorded because the narrowing is a judgment call a human should
be able to second-guess.

## 2026-09-08. Defect 4 is NOT closed. Correcting my own earlier finding
I previously reported defect 4 as not reproducing, from the homepage and
/qualifications.html. `check-safety-claims.sh` found a live EMR figure I had missed:
`blog/how-to-prequalify-a-florida-commercial-glazier.html` publishes **"Ours is 0.81"**
and **"EMR: 0.81"**. D2 withholds every safety statistic. The defect is real, it is on a
blog post, and my earlier scope was too narrow. Verify-and-close was the right
instruction; my verification was incomplete.

## 2026-09-08. Recon supersedes the bundle audit
Live measurement wins per the standing directive. 15 stylesheet sets (largest 887),
492 near-duplicate pairs at ≥0.60 with only 21 above 0.81, 364 orphans, 10 broken
links, **zero** canonicals resolving to 404, 58 meta-refresh stubs split out of every
count. The canonical repair task is dropped: it does not reproduce.

## 2026-09-08. Redirect stubs excluded from content analysis
58 pages are meta-refresh stubs, ~690 bytes, noindex,follow, canonical to the
replacement. Correctly built. Counting them as content inflates duplicates and orphans.

## 2026-09-08. Kit staged, not installed to the deploy root
The bundle is 21 markdown files. Extracting them to the repo root would recreate the
exposure closed in 44d9a7e0a. Staged under `_internal/` instead, which is git-ignored.
