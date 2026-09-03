# SEO wave-3 audit

Counted on branch `cursor/seo-wave3-audit-f25c`, 2026-09-03, after PRs 81 (wave-2 noindex of 324 city templates) and 83 (directory/locator ledger). Live host `https://acglass.com` compared to repo. `_internal/CLAUDE.md` was not present. Search Console, Bing Webmaster, and GA4 are not connected in this environment. Do not treat any row below as a traffic measurement.

GBP was not touched. `/products/eswindows/` was not created. No pages were deleted. The 324 wave-2 URLs stay `noindex,follow`.

## Headline counts

| Universe | Count | Evidence |
| --- | --- | --- |
| HTML files on disk | 1,583 | repo walk, skip `.git` / `.github` / `_internal` |
| `noindex` pages | 479 | meta robots |
| Meta-refresh stubs | 57 | `http-equiv=refresh` |
| Indexable, non-refresh pages | 1,104 | remainder |
| Unique page URLs in sitemaps | **909** | `sitemap.xml` union of non-image children |
| Live unique page URLs | **909** | fetched 2026-09-03; live == repo, 0 drift |
| Wave-2 prune URLs on disk | **324** | 77+77+77 city-service + 93 storefront-glazier |
| Wave-2 still in any sitemap | **0** | |
| Wave-2 missing `noindex` | **0** | |
| Sitemap URLs that 404 / lack a file | **0** | |
| Noindex or refresh URLs still in sitemaps | **0** | |
| JSON-LD parse failures | **0** | all `application/ld+json` blocks parse |

Child sitemap sizes (repo = live): pages 448, cities 193, services 16, blog 228, projects 25, llm 28. Master == child union (0 master-only, 0 child-only). `sitemap-index.xml` lists the seven children and does **not** list `sitemap.xml` (avoids double-listing). `robots.txt` still lists both the index and the master.

## 1. Sitemap / indexation after the 324-URL prune

**Severity: clean. No Tier 1 sitemap defect.**

Wave-2 apply held:

| Set | On disk | `noindex,follow` | In sitemaps |
| --- | --- | --- | --- |
| `/{city}/commercial-storefronts/` | 77 | 77 | 0 |
| `/{city}/glass-railings/` | 77 | 77 | 0 |
| `/{city}/impact-windows-hurricane/` | 77 | 77 | 0 |
| `/storefront-glazier-{city}-florida/` except 8 keepers | 93 | 93 | 0 |

Live spot-check 2026-09-03: `/aventura/commercial-storefronts/` and `/storefront-glazier-boca-raton-florida/` return HTTP 200, `noindex,follow`, self-canonical. Files were not deleted.

Eight keepers are live 200, indexable, self-canonical, in sitemaps:

| URL | Inbound pages (pre-fix) | Title |
| --- | --- | --- |
| `/storefront-glazier-west-palm-beach-florida/` | 45 | Storefront Glazier in West Palm Beach, FL \| ACG - 48-Hr Bids (live title uses an em dash) |
| `/storefront-glazier-naples-florida/` | 47 | Commercial Storefront Glazier Naples, FL for GCs \| ACG |
| `/storefront-glazier-tampa-florida/` | 59 | Commercial Storefront Glazier Tampa, FL for GCs \| ACG |
| `/storefront-glazier-miami-florida/` | 66 | Storefront Glazier in Miami, FL \| ACG - 48-Hr Bids |
| `/storefront-glazier-orlando-florida/` | 37 | Commercial Storefront Glazier Orlando, FL for GCs \| ACG |
| `/storefront-glazier-fort-lauderdale-florida/` | 30 | Storefront Glazier in Fort Lauderdale, FL \| ACG - 48-Hr Bids |
| `/storefront-glazier-fort-myers-florida/` | 15 | Storefront Glazier in Fort Myers, FL \| ACG - 48-Hr Bids |
| `/storefront-glazier-sarasota-florida/` | 10 | Storefront Glazier in Sarasota, FL \| ACG - 48-Hr Bids |

`/storefront-glazier-florida/` (statewide guide) stays indexable and in the sitemap. `/boca-raton/` city root stays self-canonical and in sitemaps. `url-primaries.json` Boca storefront primary remains gsc-gated on the now-noindex storefront-glazier URL. Do not flip that row without GSC.

Approved hubs live 200, self-canonical, in sitemaps: `/florida-commercial-glazing/`, `/products/`, `/products/euro-wall/`, `/services.html`, `/contact.html`, `/send-plans.html`. Live `/products/eswindows/` is HTTP 404 (intentional; manufacturer HTML still unavailable).

**Recommended next action:** none on the 324. Do not undo. A later 301 of the 93 onto keepers still needs Cloudflare + GSC equity. [NEED: GSC clicks/impressions on the 93 and on the 231 city-service URLs.]

## 2. Remaining template families (GSC-gated; do not noindex in this wave)

Do not noindex another broad family without Search Console evidence.

### A. `/{city}/all-glass-entrances/` - 77 indexable, 28 in sitemaps

Same city-swap shape as the wave-2 triples. Avg ~848 words. Titles are `All-Glass Entrance Installation in {City}…`. Statewide hub `/all-glass-entrances/` already exists (PR 71 consolidated a doorway set into that hub). 49 of the 77 city URLs are indexable and **absent** from sitemaps. Adding them would enlarge a thin family. Noindexing them would repeat wave-2 without GSC.

Examples: `/aventura/all-glass-entrances/`, `/boca-raton/all-glass-entrances/`, `/winter-heaven/all-glass-entrances/` (folder typo; title says Winter Haven).

**Next:** [NEED: GSC page report for `/*/all-glass-entrances/`.] If impressions are near zero, same treatment as wave-2 (noindex,follow + sitemap drop, no delete). If any city has clicks, keep that URL.

### B. `/{vertical}-glazing-{city}/` - 10 indexable, all in sitemaps, avg 386 words

`/assisted-living-glazing-{naples,orlando,west-palm-beach}/`, `/automotive-showroom-glazing-{fort-lauderdale,orlando,tampa,west-palm-beach}/`, `/bar-brewery-glazing-{miami,orlando,tampa}/`. Thin and templated. Keeper-market overlap only.

**Next:** GSC-gated. Do not noindex on word count alone.

### C. `/commercial-glazier-{place}/` - 18 files, 17 indexable, 17 in sitemaps, avg 597 words

City clones plus `/commercial-glazier-bid-process-florida/`. Title bank includes `Commercial Glazier in {City}, FL | ACG - 48-Hr Bids`.

**Next:** GSC-gated.

### D. `/commercial-glazing-*.html` - 131 files, 97 indexable, 49 in sitemaps

Mix of real hubs, aliases, and out-of-Florida pages. Not one family. Do not treat as a single noindex set.

### E. Out-of-Florida state pages still indexable

`llms.txt` says Florida only. These eight remain indexable (lessons.md already named them): `commercial-glazing-al.html`, `-ga.html`, `-louisiana.html`, `-north-carolina.html`, `-south-carolina.html`, `-southeast.html`, `-texas.html`, `-tn.html`. Longer siblings `/commercial-glazing-alabama.html`, `-georgia.html`, `-tennessee.html` are indexable, self-canonical, **not** in sitemaps.

Week-1 note was "noindex + self-canonical + drop from sitemaps." That was not applied. Do not apply without GSC. Homepage still links to `/commercial-glazing-tn.html` and `/commercial-glazing-nashville-tn.html` (homepage is byte-frozen).

**Next:** [NEED: GSC on the 8 + 3 longer state URLs.] Containment is noindex + sitemap drop, not deletion.

### F. `/storefront-installer-*.html` - 9 files, 8 indexable, 7 in sitemaps, avg 2,307 words

Deeper than city templates. Jacksonville's declared storefront primary in wave-2 notes is `/storefront-installer-jacksonville.html` (no `storefront-glazier-jacksonville-florida/` file). Leave until GSC.

## 3. Links, canonicals, orphans, titles, JSON-LD

### Broken internal links

Repo graph found **1** unresolved href: `/search.html` → `/${i.u}` (JS template artifact, not a real URL). Crawl-check still pins pre-existing missing-link debt (baseline 9 distinct / 70 refs). That debt was not expanded here.

**Next:** no public-page fix. JS artifact is not a crawler URL.

### Meta-refresh / canonical

57 refresh stubs. Almost all are the GitHub Pages pattern: `noindex,follow` + canonical **away** + meta-refresh + JS `location.replace`. None of those stubs are in sitemaps.

Two self-canonical + noindex + refresh pages: `/press/acg-launches-ai-operations-site.html`, `/tools/storefront-cost-estimator/`. Not in sitemaps. Not a sitemap conflict. Leave unless a later stub-hygiene pass.

`/author/connor-walsh.html` (file) is a noindex stub that canonicalizes and refreshes to `/author/connor-walsh/` (directory). That directory is **indexable**, self-canonical, and **in the sitemap**. So is `/authors/connor-walsh.html` (the bio lessons.md calls canonical). Same pair for Rielly: `/author/rielly-walsh/` and `/authors/rielly-walsh.html` are both sitemap + indexable.

**Severity: medium (duplicate author URLs).** Not a syntax error. Week-1 stubbed `/about/connor-walsh/` to `/authors/connor-walsh.html` and left `/author/connor-walsh/` live.

**Next:** [NEED: GSC on `/author/connor-walsh/` vs `/authors/connor-walsh.html` and the Rielly pair.] If `/author/*/` has no clicks, stub them onto `/authors/*.html` and drop from sitemaps. Do not do that without GSC.

### Orphan keepers / hubs

No keeper or approved hub is orphaned. Pre-fix inbound to `/florida-commercial-glazing/` was **5** (homepage, `/services.html`, `/commercial-storefront-systems.html`, `/curtainwall-systems.html`, `/contact.html`). `/products/` had **2**. `/products/euro-wall/` had **1**. That inbound gap is the wave-3 fix (below).

### Duplicate titles (self-canonical + indexable only)

City-root aliases (`/miami/`, `/fort-lauderdale/`, `/fort-myers/`, `/sarasota/`) share titles with keepers but **canonical away** to those keepers and are **not** in sitemaps. They are not a second indexable title.

True collision:

| Title | URLs | Notes |
| --- | --- | --- |
| `Commercial Glazing Contractor Florida \| ACG` | `/` and `/florida-commercial-glazing/` | Homepage is byte-frozen in `url-primaries.json`. Hub title was copied from the homepage. |

**Next:** unique-ify the **hub** title only (do not edit homepage). Blocked on a copy decision; see blocked decisions.

### Duplicate descriptions

Parser-false "A GC" / "ACG" shorts were apostrophe truncation (`A GC's` → `A GC`). Re-extracted with an HTML parser: **0** sitemap URLs have description length < 80 except `/google9d45280643313cec.html` (empty; verification file). Alias pairs (city root vs keeper) still share descriptions; aliases are not sitemap URLs.

Homepage description (frozen, 155 chars) still carries unverified `350+ projects` and `bonded $3M/$6M`. crawl-check holds that hash. [NEED: lift homepage freeze before that copy can change.]

### JSON-LD

**0 malformed blocks.** Type mix is the existing site graph (FAQPage, LocalBusiness, Organization, BreadcrumbList). No syntax fix to ship.

## 4. Unsupported / leftover claims

Do not invent replacements on public pages. [NEED:] means a fact is unverified here.

| Claim | Where | Indexable? | Notes | Next |
| --- | --- | --- | --- | --- |
| `Euro-Wall authorized` CSI label | `/services.html` | yes | First-party leftover. Softened this PR to `Euro-Wall installer` to match `facts.html`. | Done. |
| `Euro-Wall dealer` + `(authorized)` | `/llms.txt` | n/a (txt) | Softened this PR to `Euro-Wall installer` / `(factory certified)`. | Done. |
| First-party `factory authorization` / `factory-authorized` / `direct factory authorization` leftovers | `/blog/reliable-commercial-glass-company-florida.html`, `/blog/professional-installation-commercial-glazing-important.html`, `/blog/decorative-glass-storefront-options-florida.html`, `/blog/how-much-does-impact-glass-cost-commercial-buildings-florida.html`, `/storefront-installer-jacksonville.html`, `/storefront-installer-nashville.html`, `/blog/questions-to-ask-before-hiring-commercial-glazing-contractor.html` | yes | ACG-as-subject leftovers softened to installer / factory-certified / documentation-not-a-bio wording. Review pass also removed Stanley / Horton / Record from "How ACG Answers" and dropped unverified ESWindows installer-program warranty language on Jacksonville. Generic "ask the sub" editorial left alone. | Done. |
| BuildZoom bio "Authorized installer for Euro-Wall, ESWindows (Tecnoglass), PGT, Allegion, TGP, Slimpact" | external https://www.buildzoom.com/contractor/american-commercial-glass-inc | n/a | Unsupported unless manufacturer-proven. Not in this repo. Do not add the claim on-site. Do not edit BuildZoom from this PR. | External cleanup. [NEED: manufacturer proof before any authorized-installer language.] |
| Procore "20 years of experience" | external Procore Construction Network profile | n/a | False. External profile data. Not added anywhere in this repo. | External cleanup. [NEED: live recapture after Procore removes the line.] |
| `authorized dealer` editorial | `/blog/how-to-choose-commercial-glass-contractor-florida.html`, `/blog/questions-to-ask-glazing-subcontractor-before-hiring.html` | yes | Third-party "ask the sub" wording. claim-guard allowlists similar architect-spec uses. | Leave unless a first-party ACG subject is added. |
| `24-hour response` on site visits / emergency | `/commercial-glazier-near-me-miami/`, `-tampa/`, `-west-palm-beach/`, `/emergency-commercial-glass-repair-florida/` | yes | SLA not verified in this environment. | [NEED: whether ACG commits to 24-hour site visits.] Do not tighten or delete without that. |
| `WBENC certification in progress` | 1,085 indexable pages (footer chrome) | yes | Not "WBENC certified". Matches claim-guard (in-progress qualifier). | [NEED: filing date / application ID if the line should stay.] |
| Woman-owned | 1,100 indexable pages | yes | Stated on `facts.html` / `llms.txt` as Rielly Walsh 51%. No WBENC number published. | Do not upgrade to certified. |
| Nashville / Tennessee **office** | indexable pages | yes | Remaining hits are denials (`holds no Tennessee office`) or furnish-and-consult geography. PR 82 retired office-opening claims. `/acg-nashville-office-opening/` is a noindex stub to `/locations.html`. | No further office-claim edit found. |
| License qualifier = Connor Walsh | `/about.html` | yes | Repeated as first-party fact. | [NEED: DBPR qualifier name on CGC #1531993.] Do not "correct" here. |
| `$400K to $10M` prior business | `/authors/connor-walsh.html` | yes | Personal bio, not an ACG revenue claim. | [NEED: whether this stays.] |
| Homepage `350+ projects`, `$3M/$6M` bond | `/` | yes | Frozen. crawl-check documents it. | Lift freeze, then rewrite. |
| NOA / DP tables | `/eswindows-installer-florida.html`, `/noa/eswindows.html` | yes | On-site figures conflict (citations ledger). | Do not copy onto `/products/eswindows/`. [NEED: manufacturer HTML.] |
| Qualifier / WBE language | `/about.html` | yes | "WBE-qualifying owner" is ownership language, not a certification. | Do not add WBENC / WOSB numbers. |

Prices: `$` hits on `/become-a-dealer.html` are form ranges, not published job prices. No new price pages.

## 5. Conversion paths (service + Florida market → RFQ / send-plans)

Every major service and Florida market URL in the audit set already has a `/send-plans.html` link (header chrome and/or body CTA). `/contact.html` is the inquiry form and says it does not accept files; it points at send-plans. `/bid.html` is a separate live Bid Engine (self-canonical, indexable). PR 84 already pointed labeled "Send plans" CTAs at `/send-plans.html`.

This wave does **not** retarget `/bid.html` links. That is a product decision (Bid Engine vs file-upload intake).

Pre-fix gap was **hub discovery**, not the RFQ button: GCs on keepers and office metros could send plans but were not pointed at `/florida-commercial-glazing/` (5 inbound) or `/products/` (2 inbound).

## Tier 1 shipped in this PR

Narrow inbound links to already-approved hubs. One sentence or one list item. No new claims. No title rewrites. No noindex. No sitemap membership change. Homepage not edited.

**Florida hub `/florida-commercial-glazing/`** added on:

- Keepers: west-palm-beach, naples, tampa, miami, orlando, fort-lauderdale, fort-myers, sarasota
- Office metros: `/west-palm-beach/`, `/naples/`, `/tampa/`
- Service / statewide: `/glazing-contractor-florida.html`, `/commercial-storefront-installer-florida.html`, `/curtainwall-contractor-florida.html`, `/impact-windows-doors-florida.html`, `/commercial-glazing-south-florida.html`, `/commercial-glazing-jacksonville.html`, `/florida-commercial-glazing-complete-guide/`

**Products hubs** added on:

- `/florida-commercial-glazing/` → `/products/` and `/products/euro-wall/`
- `/euro-wall.html` → `/products/euro-wall/`
- `/euro-wall-installer-florida.html` → `/products/euro-wall/`
- `/manufacturers.html` → `/products/euro-wall/`

Not added: `/products/eswindows/` (404). ESWindows stays on `/eswindows-installer-florida.html`.

Post-fix inbound (distinct linking pages, self excluded): `/florida-commercial-glazing/` **23** (was 5), `/products/` **3** (was 2), `/products/euro-wall/` **5** (was 1).

## Morning findings (2026-09-03, later)

Owner-verified. This environment could not recapture BBB or Manta HTML (Cloudflare 403). Exact evidence and [NEED:] live in `/seo/citations.md`. No homepage, GBP, or marketing-copy rewrite.

1. **BBB 0633-92045708 live corrected.** Primary phone (772) 486-7711. Visit Website https://acglass.com/. Old (561) 283-8030 is secondary. No public-site content change. Ledger updated.
2. **Manta slug `mtmntvt` removed.** 301 to a generic WPB flat-glass category. Virginia Gardens / 24210 / (276) 466-2743 / Steve Thorogood gone. Recheck 2026-09-10. [NEED: exact pre-301 URL + destination URL.]
3. **`estimating@eswindows.com` bounced 550 5.1.1.** Repo hit was ledger-only. Historical send row kept and marked bounced. No replacement inbox invented. Next route: fetched https://eswindows.com/connect-dealer/ (200, "Connect with an ES Dealer" / Get a Quote). No public ACG page needed that contact language, so the form was not added to a public page.
4. **Procore** still shows false "20 years of experience". External cleanup. Claim not added on-site.
5. **BuildZoom** bio still claims authorized-installer status for Euro-Wall, ESWindows (Tecnoglass), PGT, Allegion, TGP, Slimpact. Unsupported. External only. Matching first-party leftovers on ACG pages were softened (above). BuildZoom was not edited.
6. **Extra/duplicate sends** to FreeListingUSA, Blue Book, and BBB (plus a found Constrafor NAP send) logged in citations Round 3 with UTC times. No other code action.

## Not done (out of allowed Tier 1)

- Unique-ify Florida hub title vs homepage
- Stub `/author/connor-walsh/` and `/author/rielly-walsh/`
- Noindex `/{city}/all-glass-entrances/` or out-of-Florida state pages
- Homepage claim freeze
- Cloudflare 301s, GBP, DNS, nav, logo, design tokens
- Bulk city pages
- External Procore / BuildZoom profile edits
- Inventing an ESWindows replacement inbox or adding `/connect-dealer/` to a public ACG page that did not need contact language

## Blocked decisions (top three)

1. **Unique-ify `/florida-commercial-glazing/` title** so it no longer matches the frozen homepage title `Commercial Glazing Contractor Florida | ACG`. Hub description is already distinct. Copy choice needed; do not touch `/`.
2. **`/{city}/all-glass-entrances/` (77 indexable / 28 in sitemaps).** Same template class as wave-2. Needs GSC before noindex or sitemap add. Statewide hub already exists.
3. **Duplicate author URLs in the sitemap:** `/author/connor-walsh/` vs `/authors/connor-walsh.html`, and the Rielly pair. Lessons.md already named `/authors/connor-walsh.html` as the real bio. Stubbing `/author/*/` needs a GSC equity check.

## Live fetch log (2026-09-03)

All `https://acglass.com{path}`:

| Path | HTTP | robots | canonical |
| --- | --- | --- | --- |
| `/` | 200 | index,follow | self |
| `/florida-commercial-glazing/` | 200 | index,follow | self |
| `/products/` | 200 | index,follow | self |
| `/products/euro-wall/` | 200 | index,follow | self |
| `/products/eswindows/` | 404 | noindex | `/404.html` |
| eight keepers | 200 | index,follow | self |
| `/send-plans.html` | 200 | index,follow | self |
| `/aventura/commercial-storefronts/` | 200 | noindex,follow | self |
| `/storefront-glazier-boca-raton-florida/` | 200 | noindex,follow | self |

Live sitemaps matched repo byte-for-URL-set on master + six page children + index (0 live-only, 0 repo-only).
