# Consolidation plan

Phase 1. Documents only, nothing shipped. Written 2026-09-08 against `origin/main` @ `48dfa14c9` plus the phase-0 branch.

**Every number here is my own live measurement.** The bundle's audit figures are superseded per the standing directive, and where they differ the discrepancy is stated.

`reviews/06_current_site_urls.csv`, the 1,352-row baseline this phase was supposed to read, **does not exist in this repository and never has**. The inventory was rebuilt from the tracked tree, the live sitemap (899 URLs, curl-fetched) and `_internal/recon/`.

---

## The shape of the problem

**1,593 tracked pages. 899 in the sitemap. 15 stylesheet sets.**

This is not a dated site. On-page hygiene is strong: 1,587 of 1,593 pages carry a canonical, **zero** resolve to a 404, and the redirect stubs are correctly built. The problem is consolidation, consistency and claim discipline, exactly as the phase brief says.

| Disposition | Pages | What it means |
|---|---:|---|
| KEEP | 873 | Content with inbound links, not duplicated, indexable |
| REVIEW-PHASE-4 | 432 | Noindexed and absent from the sitemap. Deliberately parked content |
| **LINK-OR-RETIRE** | **178** | **In the sitemap, but nothing on the site links to them** |
| REVIEW | 108 | Near-duplicates above 0.81, or orphans outside the sitemap |
| CONSOLIDATE | 2 | Byte-identical |

---

## 1. Templates. The real work, and bigger than scoped

The audit says five competing templates with 1,152 on one. **Measured: 15 distinct stylesheet sets**, and 20 clusters once nav structure is included.

| Cluster | Pages | Share |
|---|---:|---:|
| T01 | 808 | 50.7% |
| T02 | 252 | 15.8% |
| T03 | 204 | 12.8% |
| T04 | 79 | 5.0% |
| T05 | 74 | 4.6% |
| T06 | 58 | 3.6% |
| T07 to T15 | 118 | 7.4% |

The audit's "5" captures the top five, which cover 1,417 pages. It misses ten further sets covering 176 pages, three of them singletons. **Consolidation is a 15-to-N problem, not 5-to-1.**

Sequencing: T01 through T03 are 1,264 pages and 79% of the site. Land those three on one token layer first. T04 through T06 are structurally distinct enough to need their own reads. T07 to T15 are the tail and should be evaluated for retirement before migration, because migrating a singleton is more expensive than deleting it.

Per-page mapping: `url-inventory.csv`, `template` column. Cluster detail: `_internal/recon/templates-summary.md`.

## 2. Orphans. 178 of them are actively advertised

**364 real content pages have zero inbound internal links.** Not 219.

The number that matters is the subset: **178 orphans are in the sitemap.** Google is being told to index pages that nothing on the site links to. That is a crawl-budget and internal-link-equity problem, and it is self-inflicted.

Examples: `acg-glass.html`, `aventura/aventura-mall-area/`, `bar-brewery-glazing-orlando/`, `best-glazing-subcontractor-florida.html`, `best-storefront-contractor-florida.html`.

Each needs one of two decisions, and hard stop 6 applies to the second:

- **LINK** — earn its place with real inbound links from relevant hubs, or
- **RETIRE** — remove from the sitemap, and 301 only after a traffic check

**No page with organic traffic or inbound links gets retired without a disposition row.** I have no Search Console access, so traffic cannot be checked from here. That gate is real and it is Connor's.

## 3. Duplicates. Smaller at the top than claimed, larger in the middle

The audit says 187 pairs, worst 0.81. **Measured: 492 pairs at Jaccard ≥ 0.60, worst 1.000, and only 21 above 0.81.**

- **2 pairs are byte-identical**: `commercial-glazing-ga.html` = `commercial-glazing-georgia.html`, and the same for `-al`/`-alabama`. Abbreviation twins. Redirect map written.
- **19 pairs sit between 0.81 and 0.89**, mostly adjacent Palm Beach city pages.
- **404 pairs sit between 0.70 and 0.80.** This is the `storefront-glazier-{city}-florida` cluster and it is expected for templated local pages. Treating it as duplication would gut the local footprint.

**Recommendation: act on the 21 above 0.81 and leave the 0.70 band alone.** Differentiate those pages with real local content in a later phase rather than consolidating them.

The GA and AL twins are also parked as PC-03, because the disposition depends on whether ACG works those states at all. If the answer is neither, the whole out-of-state cluster gets the TN treatment and the redirect map is moot.

## 4. Canonicals. Task dropped

The audit claims canonical targets that are themselves 404s. **Zero reproduce.** 1,587 of 1,593 pages carry a canonical and every one resolves. Six pages have no canonical at all, which is a separate and much smaller item.

**This repair task is removed from the plan.**

## 5. Broken links. Task dropped

The audit says 10. So did I, and we were both wrong. **52 of 53 occurrences are draft pages cross-linking each other at root paths they were never published to.** The 53rd is `${i.u}` in `search.html`, a JavaScript template literal my own recon misparsed as an href.

**Zero real broken internal links on live pages.** The draft cross-links resolve themselves when phase 4 decides where those pages live; fixing them first would likely be wrong twice.

## 6. Carried from phase 0

Every phase-0 defect appears in the inventory dispositions:

- The 11 noindexed drafts are `REVIEW-PHASE-4`, still blocked by the pinned TN governance digests in `tn-claim-guard.py`.
- The 219-page bonding sweep is 72 pages done, the remainder technique vocabulary that must stay.
- `license-attribution`, `geography`, `deny-list` and `image-rights` all report CONFIG until their lists are populated.

---

## Order of work

1. **178 sitemapped orphans.** Highest value, and it needs Connor's traffic check first.
2. **T01 to T03 onto one token layer.** 1,264 pages, 79% of the site.
3. **The 21 duplicate pairs above 0.81.**
4. **T07 to T15 tail.** Retire before migrating.
5. **T04 to T06.** Separate reads.

Nothing in this plan ships in phase 1.
