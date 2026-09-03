# Sitemap coverage findings (TASK 1a / 1b)

Window: 2026-05-30 to 2026-08-25, `sc-domain:acglass.com`, `dataState=final`,
dimension `page`, `aggregationType=byPage`. Source: `gsc_full/pages_90d_full.csv`
(1,030 rows, complete/paginated). Sitemap universe: 1,276 unique page URLs across
`sitemap.xml` plus the seven child sitemaps referenced by `sitemap-index.xml`.

## Headline result

**No URLs were added to any sitemap, and no sitemap `<loc>` values were changed.**
Both tasks were reproduced exactly as stated in `gsc_full/ANALYSIS.md`, and in both
cases the correct action under the stated acceptance criteria turned out to be no
edit. The reasoning is below, per URL.

## 1a. The 157 URLs receiving impressions but absent from every sitemap

Reproduced: diffing the 1,024 unique GSC page paths against the 1,276 sitemap `<loc>`
paths yields exactly **157** paths present in GSC and absent from every sitemap.

Each of the 157 was then tested against the three acceptance criteria: (1) resolves to a
real file in the repo, (2) declares itself canonical, (3) is not `noindex`.

| Outcome | Count |
|---|---|
| File does not exist in repo | 0 |
| **Fails (2): rel=canonical points at a different URL** | **105** |
| **Fails (3): meta robots `noindex,follow`** | **46** |
| **Not an HTML page (PDF / JPG), criteria (2) and (3) not expressible** | **6** |
| **Qualifies for addition** | **0** |

All 157 exist as files; not one of them satisfies all three criteria. The 157 are not a
coverage gap -- they are the site's alias/legacy URL layer plus its deliberately
suppressed out-of-market pages. Sitemap coverage of the *indexable, self-canonical* site
is complete.

### Excluded URLs and why
#### Group A -- alias URLs whose rel=canonical points at a different page (105)

Adding these to a sitemap would submit URLs that explicitly disclaim themselves. The
impressions they earn are already being consolidated onto the declared target.

| URL | Imp | Clicks | Declared canonical | Target in sitemap |
|---|---|---|---|---|
| `/blog/what-is-division-08-glazing-construction.html` | 864 | 2 | `/blog/what-is-division-08-construction.html` | yes |
| `/blog/best-commercial-storefront-systems-florida.html` | 485 | 4 | `/commercial-storefront-systems.html` | yes |
| `/commercial-glazing-miami.html` | 451 | 1 | `/storefront-glazier-miami-florida/` | yes |
| `/division-08-scope.html` | 372 | 0 | `/division-08-subcontractor-florida.html` | yes |
| `/commercial-glazing-orlando.html` | 282 | 2 | `/storefront-glazier-orlando-florida/` | yes |
| `/fort-myers/` | 253 | 0 | `/storefront-glazier-fort-myers-florida/` | yes |
| `/case-study-atlantic-fields.html` | 249 | 4 | `/atlantic-fields.html` | yes |
| `/orlando/` | 236 | 2 | `/storefront-glazier-orlando-florida/` | yes |
| `/blog/commercial-storefront-installation-process.html` | 232 | 3 | `/blog/commercial-storefront-installation-guide.html` | yes |
| `/blog/how-much-does-curtainwall-cost-per-square-foot.html` | 215 | 1 | `/blog/curtainwall-vs-storefront-cost-guide.html` | yes |
| `/commercial-glazing-palm-beach.html` | 151 | 1 | `/storefront-glazier-palm-beach-florida/` | yes |
| `/duval-county/` | 146 | 0 | `/commercial-glazing-jacksonville.html` | yes |
| `/deerfield-beach/` | 144 | 0 | `/storefront-glazier-deerfield-beach-florida/` | yes |
| `/commercial-glazing-fort-lauderdale.html` | 140 | 1 | `/storefront-glazier-fort-lauderdale-florida/` | yes |
| `/commercial-glazing-north-palm-beach.html` | 131 | 0 | `/storefront-glazier-north-palm-beach-florida/` | yes |
| `/storefront-vs-curtainwall.html` | 119 | 3 | `/blog/storefront-vs-curtainwall.html` | yes |
| `/north-palm-beach/` | 115 | 0 | `/storefront-glazier-north-palm-beach-florida/` | yes |
| `/commercial-glazing-naples.html` | 114 | 0 | `/storefront-glazier-naples-florida/` | yes |
| `/palm-harbor/` | 96 | 2 | `/storefront-glazier-palm-harbor-florida/` | yes |
| `/blog/what-is-a-curtainwall-system.html` | 95 | 1 | `/blog/curtainwall-systems-explained-commercial-construction.html` | yes |
| `/commercial-glazing-boca-raton.html` | 91 | 0 | `/storefront-glazier-boca-raton-florida/` | yes |
| `/jacksonville/` | 90 | 0 | `/commercial-glazing-jacksonville.html` | yes |
| `/commercial-glazing-fort-myers.html` | 75 | 1 | `/storefront-glazier-fort-myers-florida/` | yes |
| `/commercial-glazing-pompano-beach.html` | 67 | 0 | `/storefront-glazier-pompano-beach-florida/` | yes |
| `/index.html` | 57 | 0 | `/` | yes |
| `/storefront-installer-florida.html` | 55 | 0 | `/commercial-storefront-installer-florida.html` | yes |
| `/naples/` | 54 | 1 | `/storefront-glazier-naples-florida/` | yes |
| `/davie/` | 49 | 0 | `/storefront-glazier-davie-florida/` | yes |
| `/commercial-glazing-aventura.html` | 47 | 0 | `/storefront-glazier-aventura-florida/` | yes |
| `/boca-raton/` | 46 | 1 | `/storefront-glazier-boca-raton-florida/` | yes |
| `/miami-beach/` | 45 | 0 | `/storefront-glazier-miami-beach-florida/` | yes |
| `/tampa/` | 44 | 0 | `/storefront-glazier-tampa-florida/` | yes |
| `/clearwater/` | 40 | 1 | `/storefront-glazier-clearwater-florida/` | yes |
| `/commercial-glazing-west-palm-beach.html` | 33 | 0 | `/storefront-glazier-west-palm-beach-florida/` | yes |
| `/commercial-glazing-kissimmee.html` | 32 | 1 | `/storefront-glazier-kissimmee-florida/` | yes |
| `/fort-lauderdale/` | 30 | 0 | `/storefront-glazier-fort-lauderdale-florida/` | yes |
| `/pompano-beach/` | 28 | 0 | `/storefront-glazier-pompano-beach-florida/` | yes |
| `/commercial-glazing-port-st-lucie.html` | 27 | 1 | `/port-saint-lucie/` | **NO** |
| `/commercial-glazing-sarasota.html` | 27 | 1 | `/storefront-glazier-sarasota-florida/` | yes |
| `/commercial-glazing-weston.html` | 27 | 0 | `/storefront-glazier-weston-florida/` | yes |
| `/blog/curtainwall-vs-storefront-florida.html` | 25 | 2 | `/blog/storefront-vs-curtainwall.html` | yes |
| `/commercial-glazing-lakeland.html` | 23 | 0 | `/storefront-glazier-lakeland-florida/` | yes |
| `/lakeland/` | 22 | 0 | `/storefront-glazier-lakeland-florida/` | yes |
| `/commercial-glazing-st-petersburg.html` | 21 | 0 | `/st-petersburg/` | **NO** |
| `/commercial-glazing-stuart.html` | 21 | 0 | `/storefront-glazier-stuart-florida/` | yes |
| `/stuart/` | 21 | 1 | `/storefront-glazier-stuart-florida/` | yes |
| `/commercial-glazing-tallahassee.html` | 19 | 0 | `/storefront-glazier-tallahassee-florida/` | yes |
| `/commercial-glazing-tampa.html` | 18 | 0 | `/storefront-glazier-tampa-florida/` | yes |
| `/kissimmee/` | 18 | 0 | `/storefront-glazier-kissimmee-florida/` | yes |
| `/commercial-glazing-boynton-beach.html` | 17 | 0 | `/storefront-glazier-boynton-beach-florida/` | yes |
| `/commercial-glazing-tequesta.html` | 17 | 0 | `/storefront-glazier-tequesta-florida/` | yes |
| `/aventura/` | 16 | 0 | `/storefront-glazier-aventura-florida/` | yes |
| `/bradenton/` | 16 | 0 | `/storefront-glazier-bradenton-florida/` | yes |
| `/case-study-atlantic-fields-golf-house.html` | 16 | 0 | `/atlantic-fields-golf-house.html` | yes |
| `/commercial-glazing-panama-city.html` | 16 | 0 | `/storefront-glazier-panama-city-florida/` | yes |
| `/weston/` | 16 | 0 | `/storefront-glazier-weston-florida/` | yes |
| `/blog/how-much-does-commercial-storefront-glass-cost-florida.html` | 15 | 0 | `/blog/how-much-does-commercial-storefront-glass-cost.html` | yes |
| `/palm-beach-gardens/` | 14 | 0 | `/storefront-glazier-palm-beach-gardens-florida/` | yes |
| `/miami/` | 13 | 0 | `/storefront-glazier-miami-florida/` | yes |
| `/palm-beach/` | 13 | 0 | `/storefront-glazier-palm-beach-florida/` | yes |
| `/sarasota/` | 13 | 0 | `/storefront-glazier-sarasota-florida/` | yes |
| `/delray-beach/` | 12 | 0 | `/storefront-glazier-delray-beach-florida/` | yes |
| `/juno-beach/` | 11 | 0 | `/storefront-glazier-juno-beach-florida/` | yes |
| `/commercial-glazing-cape-coral.html` | 10 | 0 | `/storefront-glazier-cape-coral-florida/` | yes |
| `/commercial-glazing-hobe-sound.html` | 10 | 0 | `/storefront-glazier-hobe-sound-florida/` | yes |
| `/commercial-glazing-palm-beach-gardens.html` | 10 | 0 | `/storefront-glazier-palm-beach-gardens-florida/` | yes |
| `/st-petersburg/` | 10 | 0 | `/storefront-glazier-saint-petersburg-florida/` | yes |
| `/bay-harbor-islands/` | 9 | 0 | `/storefront-glazier-bay-harbor-islands-florida/` | yes |
| `/commercial-glazing-pensacola.html` | 9 | 0 | `/storefront-glazier-pensacola-florida/` | yes |
| `/hobe-sound/` | 9 | 0 | `/storefront-glazier-hobe-sound-florida/` | yes |
| `/boynton-beach/` | 8 | 0 | `/storefront-glazier-boynton-beach-florida/` | yes |
| `/case-study-atlantic-fields-performance-center.html` | 8 | 1 | `/atlantic-fields-performance-center.html` | yes |
| `/commercial-glazing-bonita-springs.html` | 8 | 0 | `/storefront-glazier-bonita-springs-florida/` | yes |
| `/commercial-glazing-clearwater.html` | 8 | 0 | `/storefront-glazier-clearwater-florida/` | yes |
| `/cutler-bay/` | 8 | 0 | `/storefront-glazier-cutler-bay-florida/` | yes |
| `/fort-myers-beach/` | 8 | 0 | `/storefront-glazier-fort-myers-beach-florida/` | yes |
| `/projects/atlantic-fields-golf-house.html` | 8 | 1 | `/atlantic-fields-golf-house.html` | yes |
| `/tequesta/` | 8 | 0 | `/storefront-glazier-tequesta-florida/` | yes |
| `/winter-heaven/` | 8 | 0 | `/storefront-glazier-winter-haven-florida/` | yes |
| `/case-study-atlantic-fields-sales-center.html` | 6 | 0 | `/atlantic-fields-sales-center.html` | yes |
| `/port-saint-lucie/` | 6 | 0 | `/storefront-glazier-port-saint-lucie-florida/` | yes |
| `/marco-island/` | 5 | 0 | `/storefront-glazier-marco-island-florida/` | yes |
| `/vero-beach/` | 5 | 0 | `/storefront-glazier-vero-beach-florida/` | yes |
| `/bonita-springs/` | 4 | 0 | `/storefront-glazier-bonita-springs-florida/` | yes |
| `/commercial-glazing-davie.html` | 4 | 0 | `/storefront-glazier-davie-florida/` | yes |
| `/commercial-glazing-vero-beach.html` | 4 | 0 | `/storefront-glazier-vero-beach-florida/` | yes |
| `/englewood/` | 4 | 0 | `/storefront-glazier-englewood-florida/` | yes |
| `/fort-pierce/` | 4 | 0 | `/storefront-glazier-fort-pierce-florida/` | yes |
| `/jupiter/` | 4 | 0 | `/storefront-glazier-jupiter-florida/` | yes |
| `/pinecrest/` | 4 | 0 | `/storefront-glazier-pinecrest-florida/` | yes |
| `/south-miami/` | 4 | 0 | `/storefront-glazier-south-miami-florida/` | yes |
| `/commercial-glazing-jupiter.html` | 3 | 0 | `/storefront-glazier-jupiter-florida/` | yes |
| `/commercial-glazing-marco-island.html` | 3 | 0 | `/storefront-glazier-marco-island-florida/` | yes |
| `/west-palm-beach/` | 3 | 0 | `/storefront-glazier-west-palm-beach-florida/` | yes |
| `/commercial-glazing-bradenton.html` | 2 | 0 | `/storefront-glazier-bradenton-florida/` | yes |
| `/commercial-glazing-deerfield-beach.html` | 2 | 0 | `/storefront-glazier-deerfield-beach-florida/` | yes |
| `/commercial-glazing-estero.html` | 2 | 0 | `/storefront-glazier-estero-florida/` | yes |
| `/pensacola/` | 2 | 0 | `/storefront-glazier-pensacola-florida/` | yes |
| `/sebastian/` | 2 | 0 | `/storefront-glazier-sebastian-florida/` | yes |
| `/commercial-glazing-miami-beach.html` | 1 | 0 | `/storefront-glazier-miami-beach-florida/` | yes |
| `/commercial-glazing-wellington.html` | 1 | 0 | `/storefront-glazier-wellington-florida/` | yes |
| `/estero/` | 1 | 0 | `/storefront-glazier-estero-florida/` | yes |
| `/jensen-beach/` | 1 | 0 | `/storefront-glazier-jensen-beach-florida/` | yes |
| `/north-miami-beach/` | 1 | 0 | `/storefront-glazier-north-miami-beach-florida/` | yes |
| `/tallahassee/` | 1 | 0 | `/storefront-glazier-tallahassee-florida/` | yes |

#### Group B -- pages carrying meta robots noindex (46)

| URL | Imp | Clicks | Declared canonical | Self-canonical |
|---|---|---|---|---|
| `/ai-overview.html` | 223 | 1 | `/about.html` | no |
| `/commercial-glazing-louisiana.html` | 140 | 1 | `/commercial-glazing-louisiana.html` | yes |
| `/commercial-glazing-texas.html` | 114 | 1 | `/commercial-glazing-texas.html` | yes |
| `/blog.html` | 88 | 0 | `/blog/` | no |
| `/atlanta-commercial-glazing.html` | 78 | 0 | `/atlanta-commercial-glazing.html` | yes |
| `/commercial-glazing-north-carolina.html` | 73 | 0 | `/commercial-glazing-north-carolina.html` | yes |
| `/euro-wall-installer-national.html` | 66 | 0 | `/euro-wall-installer-national.html` | yes |
| `/author-connor-walsh.html` | 62 | 1 | `/authors/connor-walsh.html` | no |
| `/commercial-glazing-tn.html` | 55 | 2 | `/commercial-glazing-tn.html` | yes |
| `/blog/ai-project-management-commercial-glazing.html` | 53 | 0 | `/about.html` | no |
| `/commercial-glazing-chattanooga-tn.html` | 51 | 0 | `/commercial-glazing-chattanooga-tn.html` | yes |
| `/commercial-glazing-georgia.html` | 50 | 1 | `/commercial-glazing-ga.html` | no |
| `/commercial-glazing-memphis-tn.html` | 30 | 1 | `/commercial-glazing-memphis-tn.html` | yes |
| `/commercial-glazing-atlanta-ga.html` | 29 | 1 | `/commercial-glazing-atlanta-ga.html` | yes |
| `/past-performance.html` | 25 | 0 | `/portfolio.html` | no |
| `/ai-managed-glazing-contractor.html` | 24 | 0 | `/about.html` | no |
| `/federal-glazing-contractor-tennessee.html` | 20 | 0 | `/federal-glazing-contractor-tennessee.html` | yes |
| `/federal-government-glazing-subcontractor.html` | 18 | 0 | `/government-public-sector-glazing.html` | no |
| `/author-rielly-walsh.html` | 17 | 0 | `/authors/rielly-walsh.html` | no |
| `/commercial-glazing-huntsville-al.html` | 17 | 0 | `/commercial-glazing-huntsville-al.html` | yes |
| `/national-commercial-glazing-contractor.html` | 17 | 0 | `/national-commercial-glazing-contractor.html` | yes |
| `/commercial-glazing-nashville-tn.html` | 14 | 0 | `/commercial-glazing-nashville-tn.html` | yes |
| `/eurowall-installer-florida.html` | 12 | 1 | `/euro-wall-installer-florida.html` | no |
| `/preglazed-systems-tennessee.html` | 11 | 0 | `/preglazed-systems-tennessee.html` | yes |
| `/commercial-glazing-louisville-ky.html` | 9 | 0 | `/commercial-glazing-louisville-ky.html` | yes |
| `/tennessee-commercial-glazing/` | 8 | 1 | `/tennessee-commercial-glazing/` | yes |
| `/chattanooga/downtown-chattanooga/` | 6 | 0 | `/chattanooga/downtown-chattanooga/` | yes |
| `/commercial-glazing-ga.html` | 6 | 0 | `/commercial-glazing-ga.html` | yes |
| `/cool-springs-tn/` | 6 | 0 | `/cool-springs-tn/` | yes |
| `/blog/tennessee-vs-florida-commercial-glazing-differences.html` | 4 | 0 | `/blog/tennessee-vs-florida-commercial-glazing-differences.html` | yes |
| `/commercial-glazing-al.html` | 4 | 0 | `/commercial-glazing-al.html` | yes |
| `/commercial-glazing-alabama.html` | 4 | 0 | `/commercial-glazing-al.html` | no |
| `/blog/nashville-commercial-construction-glazing-market.html` | 3 | 0 | `/blog/nashville-commercial-construction-glazing-market.html` | yes |
| `/blog/tennessee-commercial-glazing-code-guide.html` | 3 | 0 | `/blog/tennessee-commercial-glazing-code-guide.html` | yes |
| `/blog/tornado-rated-glazing-tennessee-commercial.html` | 3 | 0 | `/blog/tornado-rated-glazing-tennessee-commercial.html` | yes |
| `/knoxville/` | 3 | 0 | `/knoxville/` | yes |
| `/memphis/` | 3 | 0 | `/memphis/` | yes |
| `/murfreesboro-tn/` | 3 | 0 | `/murfreesboro-tn/` | yes |
| `/blog/commercial-glazing-contractor-nashville-how-to-choose.html` | 2 | 0 | `/blog/commercial-glazing-contractor-nashville-how-to-choose.html` | yes |
| `/chattanooga/` | 2 | 0 | `/chattanooga/` | yes |
| `/franklin-tn/` | 2 | 0 | `/franklin-tn/` | yes |
| `/laminated-glass-tennessee.html` | 2 | 0 | `/laminated-glass-tennessee.html` | yes |
| `/memphis/downtown-memphis/` | 2 | 0 | `/memphis/downtown-memphis/` | yes |
| `/brentwood-tn/maryland-farms-brentwood/` | 1 | 0 | `/brentwood-tn/maryland-farms-brentwood/` | yes |
| `/commercial-glazing-birmingham-al.html` | 1 | 0 | `/commercial-glazing-birmingham-al.html` | yes |
| `/storefront-installer-nashville.html` | 1 | 0 | `/storefront-installer-nashville.html` | yes |

#### Group C -- non-HTML assets (6)

| URL | Imp | Clicks | Type |
|---|---|---|---|
| `/downloads/ACG-AI-Operations-WhitePaper.pdf` | 307 | 1 | .pdf |
| `/ACG-Capability-Statement.pdf` | 173 | 0 | .pdf |
| `/pdfs/projects/acg-atlantic-fields-golf-house.pdf` | 13 | 0 | .pdf |
| `/pdfs/ACG-Capabilities-Statement.pdf` | 12 | 0 | .pdf |
| `/images/projects/ocean-prime-ft-lauderdale.jpg` | 1 | 0 | .jpg |
| `/images/projects/turbine-technologies/entrance.jpg` | 1 | 0 | .jpg |

### Notes on the exclusion groups

**Group A (105).** These are two consistent families. The larger is the
`/<city>/` and `/commercial-glazing-<city>.html` alias layer, every member of which
canonicalises to `/storefront-glazier-<city>-florida/`. The smaller is a set of retitled
blog posts and case studies (`/blog/what-is-division-08-glazing-construction.html` ->
`/blog/what-is-division-08-construction.html`, `/case-study-atlantic-fields.html` ->
`/atlantic-fields.html`) plus `/index.html` -> `/`. Submitting any of them in a sitemap
would ask Google to index a URL that the page itself disclaims.

Two entries reveal a two-step canonical chain worth flagging to the owner separately:
`/commercial-glazing-port-st-lucie.html` -> `/port-saint-lucie/` ->
`/storefront-glazier-port-saint-lucie-florida/`, and
`/commercial-glazing-st-petersburg.html` -> `/st-petersburg/` ->
`/storefront-glazier-saint-petersburg-florida/`. The intermediate hop is itself
non-self-canonical, which is why its "target in sitemap" cell reads NO. Collapsing these
chains to a single hop requires editing a page's `rel=canonical` target, which this
change set is explicitly forbidden from doing.

**Group B (46).** All carry `<meta name="robots" content="noindex,follow">`. The bulk are
the Tennessee / Georgia / Alabama / Texas / Louisiana / Kentucky / North Carolina
out-of-market pages, which are noindexed on purpose (see `tn-claim-guard.py` and the
Tennessee governance in this repo). 35 of the 46 are self-canonical but still noindex,
so criterion (3) fails on its own; the other 11 fail (2) as well. Adding a noindexed URL
to a sitemap is a direct conflict signal -- the sitemap says "index this", the page says
"do not" -- and would be a regression, not a fix.

**Group C (6).** Four PDFs and two JPGs. The PDFs earn real traffic
(`/downloads/ACG-AI-Operations-WhitePaper.pdf` 307 impressions,
`/ACG-Capability-Statement.pdf` 173) and are live `200 application/pdf` with no
`X-Robots-Tag` header, so they are genuinely indexable. They were still excluded, for two
reasons: a PDF cannot declare `rel=canonical` or `meta robots`, so criteria (2) and (3)
cannot be verified as the task requires; and there is **no precedent** for PDF entries
anywhere in the existing sitemaps (`grep -c "<loc>[^<]*\.pdf</loc>" sitemap*.xml` = 0),
so adding them is a policy change rather than a gap fix. Recommend the owner decide
explicitly; if they want PDFs submitted, `sitemap-pages.xml` is the right home and
`X-Robots-Tag: noindex` should be confirmed absent first (it is, as of this check).
The two JPGs belong in `sitemap-images.xml` as `<image:loc>` children of the page that
displays them, not as standalone `<url><loc>` page entries -- that file's existing
structure already does exactly that, and neither image is currently referenced there.

## 1b. The 5 URL-form mismatches

`ANALYSIS.md` describes these as "sitemap entries whose sibling form gets the traffic --
the sitemap declares one form and Google indexed the other". Verified directly, that
description is **not accurate**, and the intended fix ("make the sitemap entry match the
form the page declares") has nothing to change.

For all five pairs, **both files exist**, **both declare themselves canonical**, and
**both forms are already present in `sitemap-pages.xml` and `sitemap.xml`**:

| Pair | `.html` file canonical | `/` file canonical | Both in sitemap-pages.xml | GSC rows |
|---|---|---|---|---|
| industries | `https://acglass.com/industries.html` | `https://acglass.com/industries/` | yes | `/industries/` only (46 imp) |
| press | `https://acglass.com/press.html` | `https://acglass.com/press/` | yes | `/press/` only (14 imp) |
| for-general-contractors | `https://acglass.com/for-general-contractors.html` | `https://acglass.com/for-general-contractors/` | yes | `/for-general-contractors/` only (23 imp) |
| resources | `https://acglass.com/resources.html` | `https://acglass.com/resources/` | yes | `/resources/` only (114 imp) |
| reviews | `https://acglass.com/reviews.html` | `https://acglass.com/reviews/` | yes | `/reviews.html` only (390 imp) |

So the sitemap entry **already matches, byte for byte, the canonical each page declares
for itself.** There is no sitemap-side mismatch to correct. `/press.html` additionally
appears in `sitemap-llm.xml`, again matching its own declared canonical.

The real defect is upstream of the sitemap: these are **five pairs of duplicate pages,
each half self-canonical**, so each pair submits two competing canonicals for one piece of
content and lets Google pick. Google picked the trailing-slash form in four cases and the
`.html` form in one (`reviews`), which is exactly the split the GSC data shows.

Fixing it requires choosing one form per pair and repointing the loser's `rel=canonical`
at the winner (plus a 301 and an internal-link sweep). That is a change to a page's
`rel=canonical` **target**, which this change set is explicitly prohibited from making, so
it is written up here for the owner instead of actioned. Recommended targets based on
measured traffic: keep `/industries/`, `/press/`, `/for-general-contractors/`,
`/resources/`, and `/reviews.html`.

## 1c. Zero-impression report

Delivered as `.github/docs/sitemap-zero-impression-report.md`. 409 of 1,276 sitemap URLs (32.1%) had
exactly zero impressions, worst in `sitemap-cities.xml` at 231/562 (41.1%). Counts
reconcile exactly with `gsc_full/ANALYSIS.md` and the 409 lines of
`gsc_full/zero_impression_urls.txt`. **Nothing was removed.**

## Files changed by this change set

| File | Change |
|---|---|
| `.github/docs/sitemap-zero-impression-report.md` | new -- 409 zero-impression URLs grouped by child sitemap |
| `.github/docs/host-consolidation-findings.md` | new -- www duplicate-host investigation and Cloudflare recommendation |
| `.github/docs/sitemap-coverage-findings.md` | new -- this file |
| `sitemap*.xml` | **unchanged** -- no `<loc>` added, removed or edited; no `<lastmod>` touched |
| all HTML pages | **unchanged** |
| `vercel.json` | **unchanged** -- its one `www.acglass.com` string is a redirect match condition and must stay |

This file lives at `.github/docs/sitemap-coverage-findings.md`. GitHub Pages does not
serve `.github/`, so it is not publicly fetchable. Do not move it back under the deploy root.
