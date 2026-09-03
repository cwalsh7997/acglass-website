# Blog overlap cluster map

For Connor Walsh. Cleanup pass only. No pages were deleted. No redirects were added. No article bodies were rewritten.

**Published post count used on the index and in both sitemaps: 226.**

That is every `blog/*.html` file that is self-canonical and indexable. Excluded from the count (still on disk):

- 2 meta-refresh stubs that canonical to `/about.html` (`ai-first-construction-operations-glazier-perspective.html`, `ai-project-management-commercial-glazing.html`)
- 5 noindex Tennessee posts (held, not listed on the index grid)
- 7 pages that already `rel=canonical` to a keeper or hub (listed under Existing canonicals)

This PR added **no new canonicals**. The seven existing ones stay. Everything below is a recommendation for Connor to approve before any delete, 301, or noindex.

Hubs to prefer when consolidating (already live):

- `/services.html`
- `/commercial-storefront-systems.html`
- `/curtainwall-systems.html`
- `/florida-hvhz-glazing-requirements.html`
- `/at-fp-blast-rated-glazing-florida.html`
- `/government-glazing-contractor-florida.html`
- `/glazing-submittal-package.html`
- `/eswindows-installer-florida.html`
- `/euro-wall-installer-florida.html`
- `/approvals/`
- metro hubs: `/tampa/`, `/miami/`, `/orlando/`, `/naples/`, `/west-palm-beach-commercial-glazing.html`, plus the storefront-glazier city URLs

---

## Existing canonicals (already on disk, not added in this PR)

These are already near-duplicate aliases. They stay live. They are omitted from both sitemaps because crawl-check requires sitemap URLs to be self-canonical.

| Source (alias) | Target (keeper / hub) | Recommended next step |
| --- | --- | --- |
| `/blog/curtainwall-vs-storefront-florida.html` | `/blog/storefront-vs-curtainwall.html` | Keep alias until GSC review, then 301 |
| `/blog/commercial-storefront-installation-process.html` | `/blog/commercial-storefront-installation-guide.html` | Keep, then 301 |
| `/blog/how-much-does-commercial-storefront-glass-cost-florida.html` | `/blog/how-much-does-commercial-storefront-glass-cost.html` | Keep, then 301 |
| `/blog/how-much-does-curtainwall-cost-per-square-foot.html` | `/blog/curtainwall-vs-storefront-cost-guide.html` | Keep, then 301 |
| `/blog/what-is-a-curtainwall-system.html` | `/blog/curtainwall-systems-explained-commercial-construction.html` | Keep, then 301 |
| `/blog/what-is-division-08-glazing-construction.html` | `/blog/what-is-division-08-construction.html` | Keep, then 301 |
| `/blog/best-commercial-storefront-systems-florida.html` | `/commercial-storefront-systems.html` | Already points at the service hub. Keep |

This PR removed those seven alias cards from the index grid so the 226 count matches published posts. The files still resolve.

---

## 1. Storefront vs curtainwall vs window wall

GC question: which envelope system do I spec?

| URL | Role | Action |
| --- | --- | --- |
| `/blog/storefront-vs-curtainwall-vs-window-wall-difference.html` | **Keeper.** Three-way comparison, most complete intent | Keep. Already links up to `/services.html`, `/curtainwall-systems.html`, `/commercial-storefront-systems.html`, `/eswindows-installer-florida.html` |
| `/blog/storefront-vs-curtainwall.html` | Strong two-way comparison. Already the target of an existing canonical | Keep as secondary keeper until GSC says otherwise. Then fold into the three-way or keep if it ranks |
| `/blog/storefront-vs-curtainwall-when-to-use-which.html` | Decision-rule variant (height / span) | Consolidate into the three-way keeper after approval |
| `/blog/curtainwall-vs-storefront-florida.html` | Already canonical to `storefront-vs-curtainwall.html` | Point at keeper (done). Later 301 |
| `/blog/curtainwall-vs-storefront-cost-guide.html` | Cost angle, also the target of the $/SF alias | Keep as the cost sibling. Link up to the system hubs, not sideways into the when-to-use clone |
| `/blog/what-is-a-curtainwall-system.html` | Already canonical to the curtainwall explainer | Later 301 |
| `/blog/curtainwall-systems-explained-commercial-construction.html` | Curtainwall explainer keeper | Keep. Point at `/curtainwall-systems.html` |
| `/blog/what-is-a-window-wall-system.html` | Window-wall explainer | Keep. Point at `/window-wall-systems.html` if that hub is the service page |
| `/blog/window-wall-systems-florida-guide.html` | Florida window-wall guide | Consolidate into the window-wall explainer or the three-way keeper |
| `/blog/window-wall-multifamily-guide.html` | Multifamily-specific | Keep. Distinct occupancy, not a clone |

Not near-identical enough for a new canonical in this PR.

---

## 2. How to hire a glazier

GC question: who do I put on the bid list?

| URL | Role | Action |
| --- | --- | --- |
| `/blog/how-to-choose-commercial-glass-contractor-florida.html` | **Statewide keeper** | Keep. This PR added upward chips to `/florida-hvhz-glazing-requirements.html` and `/glazing-submittal-package.html` |
| `/blog/how-to-choose-glazing-contractor.html` | Generic twin | Consolidate into the Florida keeper |
| `/blog/how-to-choose-glazing-subcontractor.html` | Subcontractor-scope variant | Keep. Distinct "sub vs contractor" intent |
| `/blog/how-to-choose-commercial-glazier-tampa-bay.html` | Tampa hire clone | Point at `/tampa/` and `/storefront-glazier-tampa-florida/`. Do not canonical to the statewide keeper (city intent is real) |
| `/blog/how-to-choose-commercial-glazing-contractor-west-palm-beach.html` | West Palm hire clone | Point at the West Palm hub. Same rule: city intent, not a statewide canonical |
| `/blog/commercial-glazing-contractors-tampa-fl.html` | Another Tampa hire page | Consolidate into the Tampa hire keeper or the Tampa hub |
| `/blog/questions-to-ask-before-hiring-commercial-glazing-contractor.html` | Vetting questions | Keep as a sibling, or merge into the statewide keeper later |
| `/blog/questions-to-ask-glazing-subcontractor-before-hiring.html` | Subcontractor questions | Keep or merge with the subcontractor chooser |
| `/blog/why-hire-licensed-commercial-glazier-florida.html` | License argument | Consolidate into the statewide keeper |
| `/blog/why-hire-local-commercial-glazier-florida.html` | Thin local-hire page (965 words) | Consolidate into the statewide keeper |
| `/blog/reliable-commercial-glass-company-florida.html` | Reliability / vetting | Consolidate into the statewide keeper |
| `/blog/selecting-curtainwall-contractor-florida.html` | Curtainwall-specific hire | Point at `/curtainwall-systems.html`. Keep if it stays curtainwall-only |
| `/blog/commercial-glazing-contractor-nashville-how-to-choose.html` | Noindex TN hire page | Leave noindex. Do not list. Do not canonical to Florida |

No new canonical here. City pages are not near-identical to the statewide page.

---

## 3. Per-metro contractor clones

GC question: who covers this city?

**Tampa Bay**

| URL | Role | Action |
| --- | --- | --- |
| `/blog/commercial-glazing-tampa-bay-market-2026.html` | **Market keeper** | Keep. Already links to `/storefront-glazier-tampa-florida/` |
| `/blog/commercial-glazing-tampa-bay-what-gcs-need-to-know.html` | Near-same GC Tampa briefing | Consolidate into the market keeper |
| `/blog/tampa-commercial-construction-boom-glazing.html` | Boom / pipeline angle | Keep or fold a short section into the market keeper |
| `/blog/why-acg-opened-tampa-office.html` | Office announcement | Keep as history. Point at `/tampa/` |
| `/blog/commercial-glazing-contractors-tampa-fl.html` | Hire clone (also in cluster 2) | Point at Tampa hub |
| `/blog/storefront-glass-installation-tampa.html` | Storefront install | Point at `/storefront-glazier-tampa-florida/` |
| `/blog/how-to-choose-commercial-glazier-tampa-bay.html` | Hire clone | Point at Tampa hub |

**Miami / HVHZ**

| URL | Role | Action |
| --- | --- | --- |
| `/blog/commercial-glazing-miami-dade-guide.html` | **Code / NOA keeper** | Keep. This PR added `/storefront-glazier-miami-florida/` and `/florida-hvhz-glazing-requirements.html` (the old "Finding an HVHZ Contractor" chip pointed at `/services.html`). `/miami/` is an alias of the storefront-glazier URL, so it is not used as a link target. |
| `/blog/commercial-glazing-miami-florida.html` | Contractor-in-Miami twin | Point at `/miami/` and `/storefront-glazier-miami-florida/` |

**Orlando**

| URL | Role | Action |
| --- | --- | --- |
| `/blog/commercial-glazing-orlando-fl.html` | **Orlando keeper** | Keep. Already links `/storefront-glazier-orlando-florida/`. `/orlando/` is an alias of that URL, so it is not used as a link target. |
| (no second Orlando essay of the same length) | | Further Orlando clones live on service/city URLs, not in `/blog/` |

**West Palm / Naples / others**

City hire pages belong on the metro hubs, not as more blog clones. Project stubs in those cities stay as project pages (cluster 7).

Do not canonical a Tampa page to a Miami page or to the statewide hire keeper.

---

## 4. Commercial glass cost

GC question: what does Division 08 cost?

| URL | Role | Action |
| --- | --- | --- |
| `/blog/how-much-does-commercial-storefront-glass-cost.html` | **Storefront cost keeper.** Already the target of the `-florida` alias | Keep. Already links up to storefront, curtainwall, impact, and `/services.html` |
| `/blog/how-much-does-commercial-storefront-glass-cost-florida.html` | Already canonical to the keeper | Later 301 |
| `/blog/how-much-does-commercial-glazing-cost-florida.html` | Broader glazing cost | Keep or merge into `commercial-glazing-cost-florida.html` |
| `/blog/commercial-glazing-cost-florida.html` | Broader cost | Pair with the how-much page. Pick one keeper after GSC |
| `/blog/curtainwall-vs-storefront-cost-guide.html` | System cost comparison keeper | Keep |
| `/blog/how-much-does-curtainwall-cost-per-square-foot.html` | Already canonical to the cost comparison | Later 301 |
| `/blog/commercial-glass-repair-costs-florida.html` | Repair, not new work | Keep |
| `/blog/commercial-glass-replacement-cost-business-florida.html` | Thin replacement-cost stub (768 words) | Consolidate into repair/replacement |
| `/blog/budget-commercial-glass-replacement-florida.html` | Budget framing (1004 words) | Consolidate into repair/replacement |
| `/blog/cost-of-impact-windows-commercial-florida.html` | Impact cost | Point at `/impact-windows-doors.html` |
| `/blog/how-much-does-impact-glass-cost-commercial-buildings-florida.html` | Impact cost twin | Consolidate into the impact-cost keeper |
| `/blog/commercial-glazier-hourly-rate-florida-2026.html` | Thin hourly-rate stub (839 words) | Drop the number from the title if it cannot be sourced. Consolidate or noindex after approval |

No new cost canonicals. The two that were already aliases stay aliases.

---

## 5. Glass types

GC question: what glass do I put in the opening?

| URL | Role | Action |
| --- | --- | --- |
| `/blog/commercial-glass-types-guide-florida.html` | **Keeper.** Longest Florida types guide | Keep. Footer already hits storefront and impact hubs |
| `/blog/commercial-glass-types-explained.html` | Shorter contractor explainer | Consolidate into the keeper |
| `/blog/best-glass-types-florida-commercial-climate.html` | Climate / performance angle | Keep as a climate sibling, or merge |
| `/blog/best-glass-options-florida-storefronts.html` | Storefront-specific | Point at `/commercial-storefront-systems.html` |
| `/blog/what-is-low-e-glass-commercial.html` | Low-E primer | Keep |
| `/blog/single-vs-double-glazing-commercial-florida.html` | IGU vs monolithic | Keep |
| `/blog/how-to-choose-glass-options-storefront.html` | Thin chooser (1068 words) | Consolidate into the storefront glass-options page |
| `/blog/energy-efficient-glass-options-florida-businesses.html` | Energy options | Point at the energy-code post and `/services.html` |

Related but separate: `/blog/commercial-glass-adds-property-value-florida.html` and `/blog/commercial-glass-property-value-florida.html` are value twins. Keep the longer one (`property-value`, 3153 words) and consolidate the shorter (`adds-property-value`, 1696 words) after approval. Not canonicalized here; they are similar, not near-identical.

---

## 6. HVHZ / hurricane / NOA repeats

GC question: what approval and impact path does this county need?

| URL | Role | Action |
| --- | --- | --- |
| `/blog/hvhz-glazing-requirements-florida.html` | **Blog keeper for HVHZ rules** | Keep. This PR added a chip to `/florida-hvhz-glazing-requirements.html` |
| `/florida-hvhz-glazing-requirements.html` | Service / hub | The page the blog should lose to, long term |
| `/blog/florida-product-approval-glazing-guide.html` | **FPA keeper** | Keep. Already links `/approvals/`, Miami, impact, services |
| `/blog/what-is-a-product-approval-florida.html` | Primer | Keep as series item 01. Do not canonical to the GC guide (different depth) |
| `/blog/commercial-glazing-miami-dade-guide.html` | Miami-Dade / NOA | Keep (also a metro keeper) |
| `/blog/hvhz-certified-glazing-contractor-florida.html` | Hire-in-HVHZ | Point at the HVHZ hub and the statewide hire keeper |
| `/blog/florida-building-code-9th-edition-december-31-2026.html` | **Code cutover flagship. Do not edit.** | Keep |
| `/blog/florida-building-code-commercial-glazing-guide.html` | FBC handbook | Keep as series item 03 |
| `/blog/florida-building-codes-commercial-glazing-2026.html` | 2026 code roundup | Keep as series item 02, or merge into the handbook after the 9th Edition ships |
| `/blog/florida-building-code-commercial-windows-2026.html` | Windows-only FBC | Consolidate into the handbook |
| `/blog/south-florida-building-code-glazing.html` | South Florida code | Consolidate into HVHZ keeper or Miami-Dade guide |
| `/blog/florida-commercial-glazing-hurricane-code.html` | Hurricane code | Consolidate into HVHZ keeper |
| `/blog/ufc-glazing-vs-florida-noa.html` | **Federal overlay flagship. Do not edit.** | Keep. Already links AT/FP, government, submittal, HVHZ |
| Impact vs shutters / impact vs laminated / impact vs hurricane-windows cluster (about a dozen URLs) | Same GC question, many slugs | Pick `/blog/hurricane-impact-windows-vs-shutters-commercial.html` or `/blog/what-are-impact-windows-commercial-guide.html` as the impact primer. Fold the rest after GSC. No canonicals in this PR; they overlap but are not byte-level twins |

The HVHZ repeat problem is real. Do not 301 any of these until Search Console shows which URL holds the query.

---

## 7. Thin project stubs

About fifty `*-glazing.html` posts are the same press-release chassis: "ACG delivered the glazing envelope at [project]..." at roughly 1,760 to 1,880 words.

**Keeper for the pattern:** none. Each URL is a different job. Do not canonical one project to another.

**Recommended next step (needs approval):**

- Keep every stub live
- Point each one up to `/portfolio.html` and the matching project page at the repo root when that page exists
- Where two stubs cover the same job, consolidate later:
  - `lucie-at-tradition-glazing.html` (press-release chassis) and `lucie-at-tradition-clubhouse-glazing.html` (longer spotlight). Same clubhouse. Keeper: the clubhouse spotlight
  - `bradley-daytona-glazing.html` (chassis) and `bradley-daytona-multifamily-glazing.html` (longer 300-unit piece). Same community. Keeper: the multifamily piece
  - `wave-haven-cocoa-beach-glazing.html` and `wave-food-hall-cocoa-beach-glazing.html`. Confirm whether these are one job or two before touching
  - `waxins-west-palm-beach-glazing.html` and `waxins-eurowall-clematis-street.html`. Confirm before touching
- After approval, the chassis stubs can 301 to the spotlight or to the root project page

`ocean-prime-ft-lauderdale-glazing.html` was a published post with no index card. It is now on the grid. Still a stub. Keep.

---

## 8. Fire-rated

| URL | Role | Action |
| --- | --- | --- |
| `/blog/fire-rated-glass-requirements-commercial-buildings.html` | **Keeper** | Keep. Point at `/fire-rated-glass-systems.html` |
| `/blog/fire-rated-glass-requirements-florida.html` | Florida variant | Consolidate into the keeper or keep if Florida-only code stays distinct |
| `/blog/fire-rated-glass-code-compliance.html` | Code-compliance twin | Consolidate into the keeper |

---

## 9. Division 08 / submittals

| URL | Role | Action |
| --- | --- | --- |
| `/blog/what-is-division-08-construction.html` | **Explainer keeper.** Already the target of the glazing-construction alias | Keep |
| `/blog/what-is-division-08-glazing-construction.html` | Already canonical | Later 301 |
| `/blog/division-08-specifications-guide.html` | Spec writing | Keep. Point at `/division-08-scope.html` |
| `/blog/commercial-glazing-submittal-process-guide.html` | **Submittal keeper** | Keep. This PR added `/glazing-submittal-package.html` |
| `/glazing-submittal-package.html` | Hub | The page the blog should lose to for "what goes in the package" |

---

## 10. Held / unpublished

Leave these off the index and out of the sitemaps until Connor says otherwise:

- 5 noindex Tennessee posts
- 2 about.html stubs

Do not delete them in a later IA pass without a redirect plan. The TN claim-guard inventory still fingerprints those files.

---

## Internal links

### Fixes in this PR (upward only)

- Hire keeper: chips to HVHZ hub and submittal package
- HVHZ blog keeper: chip to `/florida-hvhz-glazing-requirements.html`
- Submittal keeper: chip to `/glazing-submittal-package.html`
- Miami-Dade keeper: chips to `/storefront-glazier-miami-florida/` and the HVHZ hub. Removed a mislabeled chip that said "Finding an HVHZ Contractor" and went to `/services.html`
- Orlando keeper: already linked the Orlando storefront-glazier primary. Left that in place.
- Tampa market keeper: already had `/storefront-glazier-tampa-florida/`. Left alone (also a TN-inventory fingerprint)

Flagships `/blog/ufc-glazing-vs-florida-noa.html` and `/blog/florida-building-code-9th-edition-december-31-2026.html` were not edited. UFC already links AT/FP, government, submittal, and HVHZ.

### Broken internal page links

A pass over every `href` in `blog/*.html` that looks like a site page (not an asset) found **zero missing targets**.

Known leftover quality issues, not 404s:

- Several related-resource chips still point at sibling blog posts instead of hubs. Left in place. Rewriting those is a second pass.
- Share URLs on some older posts omit `/blog/` (`/hvhz-glazing-requirements-florida.html` in the LinkedIn share on the HVHZ post). The file lives at `/blog/hvhz-glazing-requirements-florida.html`. The share is a dead social URL, not an on-site 404. Fix on approval.
- Project stubs often link `../images/infographics/infographic-*.webp`. Those assets were not audited here.

---

## What this PR did not do (needs Connor)

1. No deletes, no Cloudflare/GitHub 301s, no new `rel=canonical` tags
2. No body rewrites, no new articles
3. No change to the five noindex TN posts
4. No merge of the Lucie, Bradley, Wave, or Waxin's project pairs
5. No GSC-based keeper changes on the impact-vs-shutters pile
6. Flagship HTML for UFC, FBC 9th Edition, and the bid-day tool was not touched
7. `docs/blog-cluster-map.md` is a working note. It will be publicly served because repo root is the deploy root. Move it under `_internal/` after review if it should not stay live
