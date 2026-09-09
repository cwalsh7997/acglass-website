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


## D9 superseded by owner confirmation, 2026-09-09

**D9 stated:** the contractor licence is held by Jeff Walsh, ACG's qualifying agent,
and "it is not Connor's licence and it is not a corporate credential belonging to
Connor personally."

**Connor confirms:** he is the qualifier of record on Florida CGC #1531993.

D9 was written on a wrong premise. Its obligation 3 anticipated exactly this and
required confirmation before publishing the attributed sentence; the confirmation
was sought and returned negative, so this is D9's own escape path rather than a
re-litigation of a locked decision.

**Effect.** D9's attribution requirement dissolves. Its whole rationale was that a
bare number sitting next to Connor's name misattributes a credential belonging to
someone else. The credential is Connor's, so a bare number is accurate.

- The 5 pages naming Connor as qualifier of record are CORRECT and stay as written.
- The 1,550 pages carrying CGC 1531993 need no attribution sentence.
- D9a item 5's sitewide removal is REVOKED. Its trigger condition, "if Connor has
  not confirmed", is now false. `scripts/apply-d9a-license-sweep.sh` is removed so
  it cannot be run against a premise that no longer holds.
- Jeff Walsh is not added to any page. D9 obligation 4 forbade describing his role
  beyond "qualifying agent", and he is not the qualifying agent.

## D2 obligation 4 resolved, 2026-09-09

Connor answered questionnaire items 25 and 26.

**Item 25, OSHA 30: every field employee holds current OSHA 30.** The claim is
accurate. All 201 occurrences across 125 pages stay exactly as written. D2 froze it
pending an answer and the answer unfreezes it. No copy changed.

**Item 26, AAMA InstallationMasters: ACG does not hold a current certification.**
All 6 assertive ACG self-claims removed across 3 files.

Two classes, and only one was a false claim. My first count said 8 occurrences on 5
pages and treated them as one thing. Left in place deliberately:

- `architect-specs/*` state what an INSTALLER must hold. ACG writes these sections
  for architects. A requirement is not a claim about ACG.
- Blog pages advising GCs what to look for when vetting a glazier.
- `glossary.html`, explaining what the programme is.

**Worth knowing.** The storefront spec section requires the installer to be
"AAMA InstallationMasters certified or equivalent". ACG does not hold it. The
"or equivalent" clause covers this, so it is not a contradiction, but if an
architect issues that spec and ACG bids it, ACG is answering its own qualification
requirement under the equivalency clause. Not a defect. Worth being aware of before
someone asks.

## Office locations confirmed, 2026-09-09

Connor confirmed both regional offices are real leased space:

    HQ       700 S Rosemary Ave Suite 204, West Palm Beach FL 33401
    Naples   4850 Tamiami Trail N Ste 301, Naples FL 34103
    Tampa    3031 N Rocky Point Dr W Ste 600, Tampa FL 33607

Nothing removed. Both stay in body copy and in LocalBusiness schema on all 17
pages each. Recorded in `config/offices.txt`.

`check-office-claims.sh` now guards the opposite direction. It used to pin two
unconfirmed addresses so they could not spread; it now fails if any street address
appears in ACG's own Organization or LocalBusiness schema that is not in the config,
which is the case that actually matters: a new location entering machine-readable
form without anyone confirming it exists.

**One consequence.** `press-release-tampa.html` was parked as PC-13 solely because
it asserted a Tampa office. The claim is true, so the park is void. It turned out to
be a duplicate of `news/acg-tampa-office-expansion.html`, which is linked from the
news index and carries more inbound links, so it now canonicals there and is out of
the sitemap. Same treatment as `gc.html`. Not deleted, not unlinked.

**Correction worth recording.** My first version of the check flagged
"2645 Southeast Bridge Road" and "100 S Ocean Blvd" as unconfirmed ACG offices.
They are Atlantic Fields and Eau Palm Beach Resort, both `Place` nodes, both project
sites. It matched them because their `@id` is under acglass.com, which is true of
every page-scoped fragment id on our own domain and says nothing about who the
entity is. The check now requires an Organization-like `@type` AND an ACG name.

## Third-party GC approvals, 2026-09-09

Connor's decisions on the six GC names in the approval ledger.

    APPROVED      Proctor Construction    33 pages, stays as published
    APPROVED      Rycon Construction      24 pages, stays as published
    NOT APPROVED  Suffolk                 32 pages, awaiting descriptor decision
    NOT APPROVED  Kaufman Lynn             3 pages, awaiting descriptor decision
    NOT APPROVED  Coastal Construction     1 page,  awaiting descriptor decision
    REMOVED       Verdex                  was 48 pages, now 0

### Verdex

**Connor directed the replacement, with the counsel caveat visible in the question
he answered.** Recording that plainly because it is a content change touching an
active dispute, and the charter routes Panther and Verdex to counsel.

118 replacements across 48 pages. Two shapes, handled differently:

- **In lists** the name was dropped rather than substituted. "DeAngelis Diamond,
  Verdex, Proctor, Curran Young, Rycon, and Suffolk" became the same list without
  it. Substituting a descriptor mid-list produces broken English.
- **Standalone** references took D3 obligation 5's accurate generic descriptor,
  "the general contractor". No invented size, sector or relationship.

Two identifying URLs survived the name replacement on
`panther-national-clubhouse.html`: Organization nodes renamed to "the general
contractor" while still carrying `url: verdexconstruction.com`. That both identifies
the party and is incoherent schema. URLs removed.

**Counsel should be told this was done and when.** Nothing is destroyed: every prior
version is in git history, and this is ACG's own marketing copy rather than a record
of the dispute. But counsel deciding the Panther question should know the site
changed underneath them on 2026-09-09.

### The ledger was incomplete and that is my error

The six names came from a hardcoded list in my own script, not from the site.
Working through the Verdex contexts surfaced five more GCs named as partners:

    DeAngelis Diamond    Curran Young    Pirtle    Hooks    Ahrens

They are still UNAPPROVED and still published. D3 obligation 3 applies to them
exactly as it did to the six.
