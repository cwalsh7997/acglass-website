# Sitemap zero-impression report

Sitemap URLs that received **exactly zero impressions** in Google Search Console over
the 90-day window **2026-05-30 to 2026-08-25** (`sc-domain:acglass.com`, dataState=final,
searchType=web). Source data: `gsc_full/pages_90d_full.csv` (1,030 rows, complete and
paginated; GSC returns only URLs with at least one impression, so zero-impression status
is derived by set subtraction of the GSC page set from the sitemap `<loc>` set).

**NOTHING HAS BEEN REMOVED.** This file is a decision aid only. The removal / noindex /
consolidate decision is the owner's.

## Summary

| Metric | Count |
|---|---|
| Unique sitemap page URLs | 1276 |
| With at least 1 impression | 867 (67.9%) |
| **With exactly zero impressions** | **409** (32.1%) |

### By child sitemap

| Child sitemap | Zero / total | Zero rate |
|---|---|---|
| `sitemap-cities.xml` | 231 / 562 | 41.1% |
| `sitemap-pages.xml` | 152 / 448 | 33.9% |
| `sitemap-blog.xml` | 19 / 225 | 8.4% |
| `sitemap-llm.xml` | 6 / 29 | 20.7% |
| `sitemap-projects.xml` | 4 / 25 | 16.0% |
| `sitemap-services.xml` | 3 / 16 | 18.8% |
| `sitemap-images.xml` | 1 / 35 | 2.9% |

A URL listed under more than one child sitemap appears once per sitemap below, so the
per-sitemap counts sum to more than the unique total.

### Known URL-form duplicates inside this list

Five of the zero-impression entries are not invisible pages. Each is one half of a
`.html` / trailing-slash pair where **both files exist, both are self-canonical, and both
are already in `sitemap-pages.xml`**. Google picked the sibling form, so the entry below
shows zero while its twin gets traffic. These need a canonical decision, not removal:

| Zero-impression sitemap entry | Sibling form receiving impressions |
|---|---|
| `/industries.html` | `/industries/` (46 imp) |
| `/press.html` | `/press/` (14 imp) |
| `/for-general-contractors.html` | `/for-general-contractors/` (23 imp) |
| `/resources.html` | `/resources/` (114 imp) |
| `/reviews/` | `/reviews.html` (390 imp) |

### Repo status of the 409 zero-impression URLs

| Repo status | Count |
|---|---|
| self-canonical | 407 |
| no-canonical | 2 |

None of the 409 are `noindex` and none point their canonical elsewhere, so there is no
sitemap-hygiene bug to fix here: every one of these URLs is a live, self-canonical,
indexable page that Google simply never showed. Two exceptions are not content pages at
all and are safe to drop whenever the owner wants:

- `/google9d45280643313cec.html` -- Google Search Console verification file.
- `/services-schema-block.html` -- JSON-LD include fragment, not a reader-facing page.

## Full listing by child sitemap

`status` is read from the repo file for that URL: `self-canonical` (the page declares
itself canonical and is indexable), `noindex` (meta robots noindex), or
`canonical->/other` (the page points its canonical at a different URL, so it can never
accrue impressions as itself and is a sitemap-inclusion bug independent of content).

### `sitemap-cities.xml` (231 zero-impression URLs)

| URL | status | note |
|---|---|---|
| `/alachua-county/` | self-canonical |  |
| `/bal-harbour-village/all-glass-entrances/` | self-canonical |  |
| `/bal-harbour-village/commercial-storefronts/` | self-canonical |  |
| `/bal-harbour-village/glass-railings/` | self-canonical |  |
| `/bal-harbour-village/impact-windows-hurricane/` | self-canonical |  |
| `/bay-harbor-islands/all-glass-entrances/` | self-canonical |  |
| `/bay-harbor-islands/commercial-storefronts/` | self-canonical |  |
| `/bay-harbor-islands/glass-railings/` | self-canonical |  |
| `/bonita-springs/all-glass-entrances/` | self-canonical |  |
| `/bonita-springs/commercial-storefronts/` | self-canonical |  |
| `/bonita-springs/glass-railings/` | self-canonical |  |
| `/boynton-beach/all-glass-entrances/` | self-canonical |  |
| `/boynton-beach/commercial-storefronts/` | self-canonical |  |
| `/boynton-beach/glass-railings/` | self-canonical |  |
| `/clearwater/all-glass-entrances/` | self-canonical |  |
| `/commercial-glazier-bid-process-florida/` | self-canonical |  |
| `/commercial-glazier-boca-raton/` | self-canonical |  |
| `/commercial-glazier-coral-springs/` | self-canonical |  |
| `/commercial-glazier-doral-fl/` | self-canonical |  |
| `/commercial-glazier-hialeah/` | self-canonical |  |
| `/commercial-glazier-hollywood-fl/` | self-canonical |  |
| `/commercial-glazier-jupiter/` | self-canonical |  |
| `/commercial-glazier-lakeland/` | self-canonical |  |
| `/commercial-glazier-near-me-miami/` | self-canonical |  |
| `/commercial-glazier-near-me-tampa/` | self-canonical |  |
| `/commercial-glazier-pembroke-pines/` | self-canonical |  |
| `/commercial-glazier-pinecrest/` | self-canonical |  |
| `/commercial-glazier-vero-beach/` | self-canonical |  |
| `/commercial-glazier-wellington/` | self-canonical |  |
| `/commercial-glazing-brandon.html` | self-canonical |  |
| `/commercial-glazing-brickell.html` | self-canonical |  |
| `/commercial-glazing-coconut-creek.html` | self-canonical |  |
| `/commercial-glazing-coral-springs.html` | self-canonical |  |
| `/commercial-glazing-for-hospitality-developers-florida/` | self-canonical |  |
| `/commercial-glazing-homestead.html` | self-canonical |  |
| `/commercial-glazing-joint-check.html` | self-canonical |  |
| `/commercial-glazing-lehigh-acres.html` | self-canonical |  |
| `/commercial-glazing-margate.html` | self-canonical |  |
| `/commercial-glazing-miami-gardens.html` | self-canonical |  |
| `/commercial-glazing-north-port.html` | self-canonical |  |
| `/commercial-glazing-owner-direct-restaurant-florida/` | self-canonical |  |
| `/commercial-glazing-payment-terms-florida/` | self-canonical |  |
| `/commercial-glazing-pinellas-park.html` | self-canonical |  |
| `/commercial-glazing-riverview.html` | self-canonical |  |
| `/commercial-glazing-sanford.html` | self-canonical |  |
| `/commercial-glazing-submittal-process.html` | self-canonical |  |
| `/commercial-glazing-tamarac.html` | self-canonical |  |
| `/commercial-glazing-treasure-coast.html` | self-canonical |  |
| `/commercial-glazing-warranty-florida-acg/` | self-canonical |  |
| `/coral-gables/all-glass-entrances/` | self-canonical |  |
| `/cutler-bay/commercial-storefronts/` | self-canonical |  |
| `/cutler-bay/glass-railings/` | self-canonical |  |
| `/dania-beach/all-glass-entrances/` | self-canonical |  |
| `/dania-beach/commercial-storefronts/` | self-canonical |  |
| `/dania-beach/glass-railings/` | self-canonical |  |
| `/davie/all-glass-entrances/` | self-canonical |  |
| `/davie/commercial-storefronts/` | self-canonical |  |
| `/davie/glass-railings/` | self-canonical |  |
| `/deerfield-beach/commercial-storefronts/` | self-canonical |  |
| `/delray-beach/all-glass-entrances/` | self-canonical |  |
| `/delray-beach/commercial-storefronts/` | self-canonical |  |
| `/delray-beach/glass-railings/` | self-canonical |  |
| `/delray-beach/impact-windows-hurricane/` | self-canonical |  |
| `/englewood/all-glass-entrances/` | self-canonical |  |
| `/englewood/commercial-storefronts/` | self-canonical |  |
| `/englewood/glass-railings/` | self-canonical |  |
| `/englewood/impact-windows-hurricane/` | self-canonical |  |
| `/florida-keys/all-glass-entrances/` | self-canonical |  |
| `/florida-keys/commercial-storefronts/` | self-canonical |  |
| `/florida-keys/glass-railings/` | self-canonical |  |
| `/fort-myers-beach/all-glass-entrances/` | self-canonical |  |
| `/fort-myers-beach/commercial-storefronts/` | self-canonical |  |
| `/fort-myers-beach/glass-railings/` | self-canonical |  |
| `/fort-myers/glass-railings/` | self-canonical |  |
| `/fort-myers/impact-windows-hurricane/` | self-canonical |  |
| `/fort-pierce/all-glass-entrances/` | self-canonical |  |
| `/fort-pierce/commercial-storefronts/` | self-canonical |  |
| `/golden-beach/all-glass-entrances/` | self-canonical |  |
| `/golden-beach/commercial-storefronts/` | self-canonical |  |
| `/golden-beach/glass-railings/` | self-canonical |  |
| `/golden-beach/impact-windows-hurricane/` | self-canonical |  |
| `/gulfstream/all-glass-entrances/` | self-canonical |  |
| `/gulfstream/glass-railings/` | self-canonical |  |
| `/gulfstream/impact-windows-hurricane/` | self-canonical |  |
| `/hallandale-beach/all-glass-entrances/` | self-canonical |  |
| `/hallandale-beach/commercial-storefronts/` | self-canonical |  |
| `/hallandale-beach/glass-railings/` | self-canonical |  |
| `/highland-beach/all-glass-entrances/` | self-canonical |  |
| `/highland-beach/commercial-storefronts/` | self-canonical |  |
| `/highland-beach/impact-windows-hurricane/` | self-canonical |  |
| `/hillsboro-beach/all-glass-entrances/` | self-canonical |  |
| `/hillsboro-beach/commercial-storefronts/` | self-canonical |  |
| `/hillsboro-beach/glass-railings/` | self-canonical |  |
| `/hillsboro-beach/impact-windows-hurricane/` | self-canonical |  |
| `/hobe-sound/all-glass-entrances/` | self-canonical |  |
| `/hollywood-florida/all-glass-entrances/` | self-canonical |  |
| `/hollywood-florida/glass-railings/` | self-canonical |  |
| `/islamorada/all-glass-entrances/` | self-canonical |  |
| `/islamorada/commercial-storefronts/` | self-canonical |  |
| `/islamorada/glass-railings/` | self-canonical |  |
| `/islamorada/impact-windows-hurricane/` | self-canonical |  |
| `/jensen-beach/all-glass-entrances/` | self-canonical |  |
| `/jensen-beach/commercial-storefronts/` | self-canonical |  |
| `/jensen-beach/glass-railings/` | self-canonical |  |
| `/jensen-beach/impact-windows-hurricane/` | self-canonical |  |
| `/juno-beach/all-glass-entrances/` | self-canonical |  |
| `/juno-beach/glass-railings/` | self-canonical |  |
| `/juno-beach/impact-windows-hurricane/` | self-canonical |  |
| `/jupiter/all-glass-entrances/` | self-canonical |  |
| `/jupiter/glass-railings/` | self-canonical |  |
| `/key-biscayne-village/all-glass-entrances/` | self-canonical |  |
| `/key-biscayne-village/commercial-storefronts/` | self-canonical |  |
| `/key-biscayne-village/glass-railings/` | self-canonical |  |
| `/key-biscayne-village/impact-windows-hurricane/` | self-canonical |  |
| `/key-largo/all-glass-entrances/` | self-canonical |  |
| `/key-largo/commercial-storefronts/` | self-canonical |  |
| `/key-largo/glass-railings/` | self-canonical |  |
| `/key-largo/impact-windows-hurricane/` | self-canonical |  |
| `/key-west/all-glass-entrances/` | self-canonical |  |
| `/key-west/commercial-storefronts/` | self-canonical |  |
| `/key-west/glass-railings/` | self-canonical |  |
| `/key-west/impact-windows-hurricane/` | self-canonical |  |
| `/kissimmee/all-glass-entrances/` | self-canonical |  |
| `/lantana/all-glass-entrances/` | self-canonical |  |
| `/lantana/commercial-storefronts/` | self-canonical |  |
| `/lantana/glass-railings/` | self-canonical |  |
| `/lantana/impact-windows-hurricane/` | self-canonical |  |
| `/lauderdale-by-the-sea/commercial-storefronts/` | self-canonical |  |
| `/lauderdale-by-the-sea/glass-railings/` | self-canonical |  |
| `/leon-county/` | self-canonical |  |
| `/lighthouse-point/commercial-storefronts/` | self-canonical |  |
| `/manalapan/all-glass-entrances/` | self-canonical |  |
| `/manalapan/glass-railings/` | self-canonical |  |
| `/manalapan/impact-windows-hurricane/` | self-canonical |  |
| `/manatee-county/` | self-canonical |  |
| `/marathon/commercial-storefronts/` | self-canonical |  |
| `/marathon/glass-railings/` | self-canonical |  |
| `/marco-island/all-glass-entrances/` | self-canonical |  |
| `/marco-island/commercial-storefronts/` | self-canonical |  |
| `/marco-island/glass-railings/` | self-canonical |  |
| `/marion-county/` | self-canonical |  |
| `/miami-beach/all-glass-entrances/` | self-canonical |  |
| `/miami-beach/glass-railings/` | self-canonical |  |
| `/miami-beach/impact-windows-hurricane/` | self-canonical |  |
| `/miami-shores-village/all-glass-entrances/` | self-canonical |  |
| `/miami-shores-village/commercial-storefronts/` | self-canonical |  |
| `/miami-shores-village/glass-railings/` | self-canonical |  |
| `/miami-shores-village/impact-windows-hurricane/` | self-canonical |  |
| `/miami/all-glass-entrances/` | self-canonical |  |
| `/miami/glass-railings/` | self-canonical |  |
| `/naples/all-glass-entrances/` | self-canonical |  |
| `/north-bay-village/glass-railings/` | self-canonical |  |
| `/north-bay-village/impact-windows-hurricane/` | self-canonical |  |
| `/north-miami-beach/all-glass-entrances/` | self-canonical |  |
| `/north-miami-beach/commercial-storefronts/` | self-canonical |  |
| `/north-miami-beach/glass-railings/` | self-canonical |  |
| `/north-miami-beach/impact-windows-hurricane/` | self-canonical |  |
| `/north-palm-beach/impact-windows-hurricane/` | self-canonical |  |
| `/oakland-park/commercial-storefronts/` | self-canonical |  |
| `/oakland-park/impact-windows-hurricane/` | self-canonical |  |
| `/okaloosa-county/` | self-canonical |  |
| `/orlando/glass-railings/` | self-canonical |  |
| `/orlando/impact-windows-hurricane/` | self-canonical |  |
| `/osceola-county/` | self-canonical |  |
| `/palm-bay/all-glass-entrances/` | self-canonical |  |
| `/palm-bay/commercial-storefronts/` | self-canonical |  |
| `/palm-bay/glass-railings/` | self-canonical |  |
| `/palm-bay/impact-windows-hurricane/` | self-canonical |  |
| `/palm-beach-gardens/glass-railings/` | self-canonical |  |
| `/palm-city/all-glass-entrances/` | self-canonical |  |
| `/palm-city/commercial-storefronts/` | self-canonical |  |
| `/palm-city/glass-railings/` | self-canonical |  |
| `/palm-harbor/all-glass-entrances/` | self-canonical |  |
| `/palm-harbor/glass-railings/` | self-canonical |  |
| `/palmetto-bay-village/all-glass-entrances/` | self-canonical |  |
| `/palmetto-bay-village/commercial-storefronts/` | self-canonical |  |
| `/palmetto-bay-village/glass-railings/` | self-canonical |  |
| `/parkland/commercial-storefronts/` | self-canonical |  |
| `/parkland/glass-railings/` | self-canonical |  |
| `/pinecrest/commercial-storefronts/` | self-canonical |  |
| `/pinecrest/glass-railings/` | self-canonical |  |
| `/pinecrest/impact-windows-hurricane/` | self-canonical |  |
| `/pinellas-county/` | self-canonical |  |
| `/pompano-beach/all-glass-entrances/` | self-canonical |  |
| `/port-saint-lucie/commercial-storefronts/` | self-canonical |  |
| `/riviera-beach/commercial-storefronts/` | self-canonical |  |
| `/riviera-beach/glass-railings/` | self-canonical |  |
| `/seminole-county/` | self-canonical |  |
| `/south-miami/commercial-storefronts/` | self-canonical |  |
| `/south-miami/glass-railings/` | self-canonical |  |
| `/st-petersburg/glass-railings/` | self-canonical |  |
| `/storefront-cost-per-square-foot-florida.html` | self-canonical |  |
| `/storefront-glazier-crestview-florida/` | self-canonical |  |
| `/storefront-glazier-englewood-florida/` | self-canonical |  |
| `/storefront-glazier-inlet-beach-florida/` | self-canonical |  |
| `/storefront-glazier-mexico-beach-florida/` | self-canonical |  |
| `/storefront-glazier-miami-shores-florida/` | self-canonical |  |
| `/storefront-glazier-navarre-florida/` | self-canonical |  |
| `/storefront-glazier-palm-city-florida/` | self-canonical |  |
| `/storefront-glazier-sunny-isles-beach-florida/` | self-canonical |  |
| `/storefront-glazier-watercolor-florida/` | self-canonical |  |
| `/storefront-glazier-watersound-florida/` | self-canonical |  |
| `/storefront-installation-mistakes.html` | self-canonical |  |
| `/storefront-installer-jacksonville.html` | self-canonical |  |
| `/storefront-installer-orlando.html` | self-canonical |  |
| `/storefront-maintenance-commercial.html` | self-canonical |  |
| `/storefront-renovation-retrofit-florida/` | self-canonical |  |
| `/storefront-replacement-commercial-florida.html` | self-canonical |  |
| `/storefront-water-intrusion-repair.html` | self-canonical |  |
| `/sunny-isles-beach/all-glass-entrances/` | self-canonical |  |
| `/sunny-isles-beach/commercial-storefronts/` | self-canonical |  |
| `/sunny-isles-beach/glass-railings/` | self-canonical |  |
| `/sunny-isles-beach/impact-windows-hurricane/` | self-canonical |  |
| `/surfside/all-glass-entrances/` | self-canonical |  |
| `/surfside/commercial-storefronts/` | self-canonical |  |
| `/surfside/glass-railings/` | self-canonical |  |
| `/tequesta/all-glass-entrances/` | self-canonical |  |
| `/tequesta/glass-railings/` | self-canonical |  |
| `/venice/all-glass-entrances/` | self-canonical |  |
| `/venice/commercial-storefronts/` | self-canonical |  |
| `/venice/glass-railings/` | self-canonical |  |
| `/vero-beach/glass-railings/` | self-canonical |  |
| `/virginia-gardens/all-glass-entrances/` | self-canonical |  |
| `/virginia-gardens/commercial-storefronts/` | self-canonical |  |
| `/virginia-gardens/glass-railings/` | self-canonical |  |
| `/volusia-county/` | self-canonical |  |
| `/walton-county/` | self-canonical |  |
| `/west-palm-beach/all-glass-entrances/` | self-canonical |  |
| `/weston/all-glass-entrances/` | self-canonical |  |
| `/winter-heaven/all-glass-entrances/` | self-canonical |  |
| `/winter-heaven/glass-railings/` | self-canonical |  |

### `sitemap-pages.xml` (152 zero-impression URLs)

| URL | status | note |
|---|---|---|
| `/acg-vs-giroux-glass.html` | self-canonical |  |
| `/acg-vs-harmon.html` | self-canonical |  |
| `/acg-vs-permasteelisa.html` | self-canonical |  |
| `/after-hours-commercial-glazing-installation-florida/` | self-canonical |  |
| `/after-hours-storefront-installation-miami/` | self-canonical |  |
| `/aia-g702-g703-glazing.html` | self-canonical |  |
| `/architect-specs/section-08-41-13-aluminum-storefront.html` | self-canonical |  |
| `/architect-specs/section-08-71-00-automatic-entrance-door-hardware.html` | self-canonical |  |
| `/assisted-living-glazing-naples/` | self-canonical |  |
| `/assisted-living-glazing-orlando/` | self-canonical |  |
| `/assisted-living-glazing-west-palm-beach/` | self-canonical |  |
| `/atlantic-fields-sales-center.html` | self-canonical |  |
| `/balcony-glass-railings-florida/` | self-canonical |  |
| `/bar-brewery-glazing-miami/` | self-canonical |  |
| `/bar-brewery-glazing-orlando/` | self-canonical |  |
| `/bar-brewery-glazing-tampa/` | self-canonical |  |
| `/best-glass-for-restaurant-storefronts-florida/` | self-canonical |  |
| `/best-glaziers-south-florida/` | self-canonical |  |
| `/best-glazing-subcontractor-florida.html` | self-canonical |  |
| `/best-storefront-contractor-florida.html` | self-canonical |  |
| `/blog-2026/commercial-glazing-rfq-checklist-for-architects/` | self-canonical |  |
| `/can-acg-bid-multifamily-projects-over-2-million/` | self-canonical |  |
| `/can-acg-handle-healthcare-glazing-occupied-facility/` | self-canonical |  |
| `/can-i-finance-commercial-glazing-florida/` | self-canonical |  |
| `/can-you-install-glass-on-occupied-buildings/` | self-canonical |  |
| `/commercial-glass-board-up-emergency-florida/` | self-canonical |  |
| `/commercial-glass-cleaning-maintenance/` | self-canonical |  |
| `/commercial-glass-replacement-hurricane-damage-florida/` | self-canonical |  |
| `/coral-gables/coral-gables-miracle-mile/` | self-canonical |  |
| `/country-club-glazing-boca-raton/` | self-canonical |  |
| `/country-club-glazing-naples/` | self-canonical |  |
| `/country-club-glazing-palm-beach/` | self-canonical |  |
| `/curtain-wall-recladding-reglazing.html` | self-canonical |  |
| `/daytona-beach/` | self-canonical |  |
| `/doral/downtown-doral/` | self-canonical |  |
| `/emergency-commercial-glass-repair-miami/` | self-canonical |  |
| `/eswindows-impact-window-installer-boca-raton/` | self-canonical |  |
| `/eswindows-impact-window-installer-palm-beach/` | self-canonical |  |
| `/eswindows-installer-naples.html` | self-canonical |  |
| `/euro-wall-folding-door-installer-miami/` | self-canonical |  |
| `/euro-wall-folding-door-installer-naples/` | self-canonical |  |
| `/florida-commercial-glazing-report-2026.html` | self-canonical |  |
| `/florida-notice-to-owner-glazing.html` | self-canonical |  |
| `/folding-glass-walls-florida/` | self-canonical |  |
| `/for-general-contractors.html` | self-canonical | URL-form duplicate, sibling gets traffic |
| `/fort-lauderdale/las-olas-fort-lauderdale/` | self-canonical |  |
| `/glazier-cost-by-city-florida/` | self-canonical |  |
| `/glazing-scope-inclusions-exclusions.html` | self-canonical |  |
| `/glazing-value-engineering.html` | self-canonical |  |
| `/google9d45280643313cec.html` | no-canonical |  |
| `/government-municipal-glazing-tallahassee/` | self-canonical |  |
| `/gym-fitness-glazing-miami/` | self-canonical |  |
| `/gym-fitness-glazing-orlando/` | self-canonical |  |
| `/gym-fitness-glazing-tampa/` | self-canonical |  |
| `/hotel-glazing-contractor-fort-lauderdale/` | self-canonical |  |
| `/hotel-glazing-contractor-jacksonville/` | self-canonical |  |
| `/hotel-glazing-contractor-naples/` | self-canonical |  |
| `/hotel-glazing-contractor-orlando/` | self-canonical |  |
| `/hotel-glazing-contractor-sarasota/` | self-canonical |  |
| `/hotel-glazing-contractor-tampa/` | self-canonical |  |
| `/how-far-does-acg-travel-for-projects/` | self-canonical |  |
| `/how-long-does-commercial-glazing-take-to-install/` | self-canonical |  |
| `/how-much-does-curtain-wall-cost-per-square-foot/` | self-canonical |  |
| `/how-to-hire-commercial-glazing-contractor-florida.html` | self-canonical |  |
| `/how-to-spec-commercial-impact-glass/` | self-canonical |  |
| `/hurricane-glass-replacement-fort-lauderdale/` | self-canonical |  |
| `/indiantown-high-school.html` | self-canonical |  |
| `/industries.html` | self-canonical | URL-form duplicate, sibling gets traffic |
| `/industries/healthcare.html` | self-canonical |  |
| `/lucie-at-tradition.html` | self-canonical |  |
| `/marina-glazing-miami-beach/` | self-canonical |  |
| `/medical-office-glazier-fort-lauderdale/` | self-canonical |  |
| `/medical-office-glazier-miami/` | self-canonical |  |
| `/medical-office-glazier-naples/` | self-canonical |  |
| `/medical-office-glazier-orlando/` | self-canonical |  |
| `/medical-office-glazier-tampa/` | self-canonical |  |
| `/medical-office-glazier-west-palm-beach/` | self-canonical |  |
| `/miami-dade-noa-glazing.html` | self-canonical |  |
| `/miami/brickell-key-miami/` | self-canonical |  |
| `/miami/brickell-miami/` | self-canonical |  |
| `/miami/coconut-grove-miami/` | self-canonical |  |
| `/miami/design-district-miami/` | self-canonical |  |
| `/miami/flagler-street-miami/` | self-canonical |  |
| `/miami/wynwood-miami/` | self-canonical |  |
| `/multifamily-glazing-tampa/` | self-canonical |  |
| `/naples/fifth-avenue-naples/` | self-canonical |  |
| `/naples/third-street-naples/` | self-canonical |  |
| `/new-construction-glazing.html` | self-canonical |  |
| `/news/` | self-canonical |  |
| `/noa/eswindows.html` | self-canonical |  |
| `/occupied-building-glazing-installation-florida/` | self-canonical |  |
| `/office-building-glazier-fort-lauderdale/` | self-canonical |  |
| `/office-building-glazier-miami/` | self-canonical |  |
| `/office-building-glazier-naples/` | self-canonical |  |
| `/office-building-glazier-orlando/` | self-canonical |  |
| `/office-building-glazier-sarasota/` | self-canonical |  |
| `/office-building-glazier-tampa/` | self-canonical |  |
| `/orlando/downtown-orlando/` | self-canonical |  |
| `/palm-beach/worth-avenue-palm-beach/` | self-canonical |  |
| `/ponte-vedra-beach/` | self-canonical |  |
| `/port-orange/` | self-canonical |  |
| `/press.html` | self-canonical | URL-form duplicate, sibling gets traffic |
| `/religious-glazing-miami/` | self-canonical |  |
| `/religious-glazing-orlando/` | self-canonical |  |
| `/religious-glazing-tampa/` | self-canonical |  |
| `/resources.html` | self-canonical | URL-form duplicate, sibling gets traffic |
| `/restaurant-glazier-fort-lauderdale/` | self-canonical |  |
| `/restaurant-glazier-miami/` | self-canonical |  |
| `/restaurant-glazier-naples/` | self-canonical |  |
| `/restaurant-glazier-orlando/` | self-canonical |  |
| `/restaurant-glazier-sarasota/` | self-canonical |  |
| `/restaurant-glazier-tampa/` | self-canonical |  |
| `/retail-storefront-installer-fort-lauderdale/` | self-canonical |  |
| `/retail-storefront-installer-miami/` | self-canonical |  |
| `/retail-storefront-installer-naples/` | self-canonical |  |
| `/retail-storefront-installer-sarasota/` | self-canonical |  |
| `/retail-storefront-installer-tampa/` | self-canonical |  |
| `/reviews/` | self-canonical | URL-form duplicate, sibling gets traffic |
| `/sanford/` | self-canonical |  |
| `/sanibel/` | self-canonical |  |
| `/sarasota/sarasota-downtown-main-street/` | self-canonical |  |
| `/school-glazier-fort-lauderdale/` | self-canonical |  |
| `/school-glazier-jacksonville/` | self-canonical |  |
| `/school-glazier-miami/` | self-canonical |  |
| `/school-glazier-naples/` | self-canonical |  |
| `/school-glazier-sarasota/` | self-canonical |  |
| `/school-glazier-tampa/` | self-canonical |  |
| `/security-window-film-retrofit.html` | self-canonical |  |
| `/showroom-glazing-miami/` | self-canonical |  |
| `/showroom-glazing-naples/` | self-canonical |  |
| `/st-augustine/` | self-canonical |  |
| `/st-petersburg/downtown-st-pete/` | self-canonical |  |
| `/tampa/davis-islands-tampa/` | self-canonical |  |
| `/tampa/hyde-park-tampa/` | self-canonical |  |
| `/tampa/water-street-tampa/` | self-canonical |  |
| `/tampa/westshore-tampa/` | self-canonical |  |
| `/temple-terrace/` | self-canonical |  |
| `/university-college-glazing-gainesville/` | self-canonical |  |
| `/university-college-glazing-miami/` | self-canonical |  |
| `/university-college-glazing-tampa/` | self-canonical |  |
| `/west-palm-beach/clematis-street-west-palm-beach/` | self-canonical |  |
| `/west-palm-beach/rosemary-square-west-palm-beach/` | self-canonical |  |
| `/what-is-a-good-bid-acknowledgment-time/` | self-canonical |  |
| `/what-is-iru-insulating-glass-unit/` | self-canonical |  |
| `/what-is-stick-built-curtain-wall/` | self-canonical |  |
| `/what-is-the-best-aluminum-storefront-system/` | self-canonical |  |
| `/what-is-the-warranty-on-commercial-glass/` | self-canonical |  |
| `/what-makes-acg-different-florida-glazier/` | self-canonical |  |
| `/what-to-look-for-in-commercial-glazing-warranty/` | self-canonical |  |
| `/when-to-replace-commercial-glass-vs-repair/` | self-canonical |  |
| `/winter-park/` | self-canonical |  |
| `/winter-park/winter-park-park-ave/` | self-canonical |  |

### `sitemap-blog.xml` (19 zero-impression URLs)

| URL | status | note |
|---|---|---|
| `/blog/736-lagoon-dr-glazing.html` | self-canonical |  |
| `/blog/bobcat-treasure-coast-glazing.html` | self-canonical |  |
| `/blog/commercial-glass-replacement-cost-business-florida.html` | self-canonical |  |
| `/blog/common-commercial-glass-installation-mistakes-avoid.html` | self-canonical |  |
| `/blog/dale-mabry-retail-tampa-glazing.html` | self-canonical |  |
| `/blog/how-glaziers-handle-custom-measurements.html` | self-canonical |  |
| `/blog/how-professional-glaziers-ensure-safe-installation.html` | self-canonical |  |
| `/blog/how-to-choose-glass-options-storefront.html` | self-canonical |  |
| `/blog/how-to-maintain-commercial-storefront-glass.html` | self-canonical |  |
| `/blog/how-to-prepare-for-commercial-glazier-visit.html` | self-canonical |  |
| `/blog/hurricane-proof-windows-commercial-florida.html` | self-canonical |  |
| `/blog/lessons-from-350-florida-commercial-glazing-projects.html` | self-canonical |  |
| `/blog/medley-business-park-glazing.html` | self-canonical |  |
| `/blog/prestige-marble-bonita-springs-glazing.html` | self-canonical |  |
| `/blog/villa-lonz-riviera-beach-glazing.html` | self-canonical |  |
| `/blog/what-are-impact-windows-commercial-guide.html` | self-canonical |  |
| `/blog/whats-included-professional-glass-installation.html` | self-canonical |  |
| `/blog/why-hire-local-commercial-glazier-florida.html` | self-canonical |  |
| `/blog/why-is-my-commercial-storefront-glass-leaking.html` | self-canonical |  |

### `sitemap-llm.xml` (6 zero-impression URLs)

| URL | status | note |
|---|---|---|
| `/acg-vs-giroux-glass.html` | self-canonical |  |
| `/acg-vs-harmon.html` | self-canonical |  |
| `/acg-vs-permasteelisa.html` | self-canonical |  |
| `/curtain-wall-recladding-reglazing.html` | self-canonical |  |
| `/press.html` | self-canonical | URL-form duplicate, sibling gets traffic |
| `/security-window-film-retrofit.html` | self-canonical |  |

### `sitemap-projects.xml` (4 zero-impression URLs)

| URL | status | note |
|---|---|---|
| `/case-study-bobcat-treasure-coast.html` | self-canonical |  |
| `/case-study-bradley-daytona.html` | self-canonical |  |
| `/case-study-cudjoe-key.html` | self-canonical |  |
| `/case-study-ocean-prime-fort-lauderdale.html` | self-canonical |  |

### `sitemap-services.xml` (3 zero-impression URLs)

| URL | status | note |
|---|---|---|
| `/all-glass-entrance-doors-florida/` | self-canonical |  |
| `/multi-slide-doors-florida/` | self-canonical |  |
| `/services-schema-block.html` | no-canonical |  |

### `sitemap-images.xml` (1 zero-impression URLs)

| URL | status | note |
|---|---|---|
| `/atlantic-fields-sales-center.html` | self-canonical |  |

This file lives at `.github/docs/sitemap-zero-impression-report.md`. GitHub Pages does not
serve `.github/`, so it is not publicly fetchable. Do not move it back under the deploy root.

