# ACG Website — Project Operating Manual

This file is read automatically by Claude Code and by Connor's Perplexity Computer agent. **Both AI agents share this context.** Update this file when you change something material so the other agent doesn't have to relearn.

---

## 1. What this site is

**American Commercial Glass, Inc.** — commercial glazing contractor, FL CGC #1531993.
HQ 700 S Rosemary Ave Suite 204, West Palm Beach FL 33401 · (772) 486-7711 · connor@acglass.com.
350+ projects · 1M+ SF installed · $3M/$6M bonded · zero OSHA recordables since 2021.
**Authorized installer:** ESWindows, Euro-Wall, TGP, Allegion, PGT, Slimpact.
**NOT installers of:** Kawneer, YKK, Tubelite. Do not mention these brands anywhere on the site.

Nashville TN expansion launches Q3 2026 (page `/commercial-glazing-nashville-tn.html` is live; don't add TN to ad targeting until then).

---

## 2. Tech stack & deploy chain

| Component | What it is |
|---|---|
| **Hosting** | GitHub Pages (NOT Vercel, despite `vercel.json` existing) |
| **DNS** | Cloudflare in front of GitHub Pages |
| **Repo** | `cwalsh7997/acglass-website`, default branch `main` |
| **CNAME** | `acglass.com` (apex) — `www.acglass.com` 301-redirects to apex |
| **Deploy** | `git push origin main` → GitHub Pages auto-deploys in 60–90 sec |
| **Forms backend** | formsubmit.co/ajax/connor@acglass.com (verified) |
| **Analytics** | GA4 measurement ID `G-M7BFQD2SPP`, property `395101505` |
| **Paid ads** | Google Ads account `7840228411`, PMax campaign "American Commercial Glass" |

There is **no build step** — every `.html` file in the repo is served verbatim. CSS is mostly inline `<style>` in `<head>` per page (legacy of the original generator). Avoid introducing build tooling unless a real need arises.

`vercel.json` exists with `redirects` entries — these are dormant. Real redirects use **meta-refresh stub `index.html`** files (e.g. `/kawneer-installer-florida/index.html` exists as a stub redirecting to a working page).

---

## 3. Brand standards (enforce in every change)

| Element | Value |
|---|---|
| Primary navy | `#0e284f` (also `#050a12` used as dark hero background) |
| Accent red | `#e11320` (hover `#c10f1c`) |
| Body font | Inter (Google Fonts), weights 400–900 |
| Mono font | JetBrains Mono, used for technical/metadata callouts |
| Tagline | "Precision glazing. AI-managed. Delivered." |
| Aesthetic target | National-tier — Skanska, Lendlease, Apple-grade editorial. NOT homebuilder/contractor template |

**Banned words anywhere on the site or in any agent output:** delve, leverage (verb), synergy, ecosystem, world-class, best-in-class, cheap, game-changing, elevate, cutting-edge, state-of-the-art, revolutionize, competitive pricing, affordable, low cost.

**Banned brand mentions:** Kawneer, YKK, YKK AP, Tubelite, Vistawall. (Site was purged of these May 26, 2026 — 293 files. Do not reintroduce.)

**Voice:** Direct, confident, owner-tone (Connor, President). No fluff, no AI-sounding phrasing. Lead with answer. Sign client-facing emails "Connor."

---

## 4. Forms — how they work (don't break this)

Three forms exist, all POST to `https://formsubmit.co/ajax/connor@acglass.com`:

1. **`/contact.html`** — main contact form, fires `gtag('event','generate_lead',{value:500})`
2. **`/bid.html`** — bid request with file upload, fires `gtag('event','bid_submitted',{value:1000})`
3. **`/commercial-glazing-nashville-tn.html`** — Nashville intake, fires `gtag('event','generate_lead',{value:1000})`
4. **`/send-plans.html`** — mailto-based (file attachments required), fires `gtag('event','generate_lead',{value:750})` alongside the mailto open

**Required form fields when adding/changing:**
- `name`, `email` (with valid type), `company` (recommended)
- Hidden honeypot: `<input type="text" name="_honey" style="display:none">`
- `_subject` MUST start with `[ACG LEAD]` — Outlook auto-classifies anything else as Promotions
- `_template=basic` (not `table` — plain text is less Promotion-detectable)
- `_replyto` set to submitter's email so Reply goes to lead, not formsubmit
- `_captcha=false`

**GA4 Key Events (already registered on property 395101505):**
- `generate_lead` (id 14944799037)
- `bid_submitted` (id 14944884023)

Both events map to Google Ads "Contact Us" conversion via GA4 import.

---

## 5. SEO conventions

- City landing pages live at `/storefront-glazier-{city}-florida/index.html`
- 79 city pages share a common systems-grid block (ESWindows + Euro-Wall + TGP + Allegion) — if rewriting the systems block, do it across all 79 pages, not one
- Service hub pages at root: `/curtainwall-systems.html`, `/impact-windows-doors-florida.html`, `/eswindows-installer-florida.html`, etc.
- Sitemap: `/sitemap.xml` (currently 1,279 URLs)
- Top ad landing page: `/storefront-glazier-west-palm-beach-florida/` — has a sticky bottom CTA and `cta_click` event tracking; treat as conversion-critical
- Robots: site is indexable; thin pages can be NOINDEX'd via `<meta name="robots" content="noindex,follow">`
- Schema.org JSON-LD on most pages (Organization, LocalBusiness, BreadcrumbList, FAQPage where applicable). Update the `@id` and `sameAs` fields when adding new social/directory profiles.

---

## 6. Coordination between Claude Code and Computer

Both agents share this repo. To avoid conflicts:

- **Pull before any edit**: `git pull origin main` first, always
- **Commit small, push immediately** — don't sit on uncommitted changes
- **Don't rebase or force-push `main`** — straight merges only
- **Write commit messages in the format** Computer has been using:
  ```
  Short imperative subject

  - Bullet of what changed and why
  - Bullet
  - Bullet
  ```
- **If you change something material (forms backend, GA4 setup, deploy flow, brand)**, update this CLAUDE.md in the same commit so the other agent learns it next pull
- **High-risk changes** (mass file rewrites, deletion of pages, sitemap restructure): batch them in one commit with a description of scope and reversibility

If there's a merge conflict, default to the most recent commit unless context says otherwise. When in doubt, ask Connor.

---

## 7. Recent material changes (May 2026)

| Date | Change | Why |
|---|---|---|
| May 25 | `/contact` form rewritten: mailto → fetch POST to formsubmit + `generate_lead` event + honeypot | Was broken — never fired conversion event, never POSTed anywhere |
| May 25 | GA4 `generate_lead` + `bid_submitted` marked as Key Events | So Google Ads can import them as conversions |
| May 26 | 293-file Kawneer/YKK/Tubelite purge — replaced with ESWindows product equivalents | We're NOT authorized installers for those brands |
| May 26 | 10 manufacturer URL pages deleted + meta-refresh redirect stubs created | Same reason |
| May 26 | Glossary entries for Kawneer/YKK consolidated to single ESWindows entry | Same |
| May 26 | Google Ads campaign cleaned: Nashville removed from geo, Final URL Expansion OFF, 31 negatives added, In-market Construction + Commercial RE + ACG Bid Platforms audience signals added | Burning budget on hotel-searchers |
| May 27 | Sticky bottom CTA added to `/storefront-glazier-west-palm-beach-florida/`, nav CTA rewritten to "Get a 48-Hour Bid" → `/bid.html` | 99.7% drop-off between ad-landing and contact form |
| May 30 | All 3 forms: subject changed to `[ACG LEAD] ...`, template→basic, Reply-To→submitter | Outlook was filing submissions in Promotions folder |
| May 30 | Shipped Dealer Portal Phase 1 (cherry-pick 58b0e4a7 from acg-dealer-portal): become-a-dealer.html, dealer/* admin + login + thanks pages, dealer.css/js, workers/dealer-portal-api/* (Cloudflare Worker, NOT deployed) | Connor's April work, no conflicts |
| May 30 | Phase 1 audit cherry-picks: dedupe og:* tags on 117 pages (318 dups removed), Florida\'s literal-backslash fix on 295 pages, humans.txt founding year 2020→2021, Service schema added to curtainwall/impact/multi-slide pages | Real SEO + share-card quality wins, no risk |
| May 30 | Phase 2 + 3 audit ships (Claude Code, e7f25c66 → 50037259): 404 robots dedupe, noindex 9 out-of-state pages + sitemap prune, theme-color #0e284f on every page, self-hosted Inter/JBM/Playfair (165 KB fonts/), width+height on 1,326 imgs (99% CLS coverage), loading=lazy + decoding=async on 100% of eligible imgs, Privacy + Terms surfaced in footer of 965 pages | 8 audit-branch reworks shipped clean, 2 near-miss bugs caught in pre-push diff (gawk \\1 backref, blank-line nuke, RS=\\0 ordering, Google verification \\r) |
| May 30 | LCP collision fix (Computer, 8c6b5a74): 674 imgs had BOTH fetchpriority="high" AND loading="lazy" — flip lazy→eager. Phase 3.3 awk's skip condition only checked loading=eager, missed fetchpriority=high preservation signal. | Real LCP regression on every page (nav logo affected) — caught and fixed within minutes of deploy verification |
| May 30 (late) | Grok-recommendation execution batch (Computer, 81e3ec99 → 91ed34d6): (1a) legal name LLC → Inc. corrected on 89 mentions across 81 files + Org schema enriched with 3-office location[], hasCredential[] (CGC#1531993 + WBE + SBE), award[], numberOfEmployees. (1b) FAQPage schema injected on 4 blog posts that had FAQ HTML but lacked schema. (1c) Project schema added to 10 verified case-study pages (panther-national-clubhouse, atlantic-fields, wild-blue-clubhouse, gulf-harbour-country-club, siena-lakes-naples, baron-shoppes-tradition, tradewinds-hobe-sound, gulfside-twelve, cudjoe-key-fire-station, martin-county/) — SKIPPED Haines City, Ocean Prime, Eau Palm Beach per unverified-flag list. (2) Surgical meta title + description rewrites on top 15 pages from Search Console (all titles ≤58c, all descriptions ≤155c, og/twitter equivalents synced). (4) Related Resources internal-linking block added to same 15 pages, 4 cluster-tagged links each across PRODUCT / COMPLIANCE / COSTS / PROJECTS / BRAND clusters | Grok audit (82/100) execution items 1a, 1b, 1c, 2, 4. Item 3 (image audit) already shipped earlier today; item 5 (homepage SSR) rejected as misdiagnosis (site is static HTML, no JS render layer) |
| May 30 | Phase 2 audit #5: declared `--font-mono` and `--text-muted` CSS vars in `:root` of `css/style.css` (alias for `--mono` and `--white-50`) | ~1,500 inline `style="..."` instances reference these var names; without the declarations, byline + caption text was silently falling back to defaults |
| May 30 | Phase 2 audit #8: deduped `<meta name="robots">` in `404.html` (had two conflicting tags: `noindex,follow` and `noindex, nofollow`) — kept `noindex, nofollow` | Conservative for an error page: don't waste crawl budget on links from a 404 |
| May 30 | Phase 2 audit #6: added `<meta name="robots" content="noindex,follow">` to 9 out-of-state pages (commercial-glazing-{alabama,georgia,louisiana,tennessee,texas,north-carolina,south-carolina,southeast}.html + national-commercial-glazing-contractor.html); pruned the same 9 URLs from `sitemap.xml` (1371→1362 entries) | ACG is FL-licensed only. Pages were attracting leads ACG can't fulfill + risking HCU demotion for templated localized content. `noindex,follow` preserves any inbound-link equity while removing the pages from Google's index over the next 4-8 weeks. |
| May 30 | Phase 2 audit #7: added `<meta name="theme-color" content="#0e284f">` after the viewport meta on every eligible HTML page (1,417 inserts + 4 wrong-color `#0D1E36` corrections); 12 files skipped (redirect stubs + Google verification stub — no viewport meta) | Mobile browser chrome (Chrome address bar on Android, status bar on iOS, Edge) tints to match the page color. Brand navy `#0e284f` per CLAUDE.md §3 |
| May 30 | Phase 3 audit: self-hosted Inter, JetBrains Mono, Playfair Display (Latin-subset variable woff2 in `fonts/`). Added 4 `@font-face` blocks at top of `css/style.css` with `font-display: swap`. Stripped `fonts.googleapis.com` `<link>` + both `fonts.gstatic.com`/`fonts.googleapis.com` preconnects + Inter `@import url(...)` from 1,275 pages. Inserted `<link rel="preload" as="font" type="font/woff2" href="/fonts/inter-variable-latin.woff2" crossorigin>` before each page's `css/style.css` link. Bumped css cache-buster to new epoch on all touched pages including the 4 dealer-portal pages (so cached pre-self-host CSS gets refetched on next visit). 7 pages skipped — 6 `concepts/*` (use Fraunces, not self-hosted) and 1 `multifamily-commercial-glazing-florida/index.html` (uses Manrope `@import`, not self-hosted). | Kills 3 third-party requests + 2 DNS lookups + 1 TLS handshake per page load (~200-400ms LCP improvement on mobile). Variable fonts give all weights in one file each (Inter 100–900, JBM 100–800, Playfair Display 400–900 upright + italic). Latin subset only — site is English. font-display:swap matches Google Fonts' prior behavior so visitors still see web fonts even on slow connections (vs `optional` which would never load web fonts on slow first visits). |
| May 30 | Phase 3 audit #2: added `width` and `height` attributes to 1,326 `<img>` tags across 455 HTML files. Coverage 70% → 99% (4,516 of 4,528 imgs declare intrinsic dims). 12 holdouts skipped by design — 8 empty `src=""` (dynamic JS lightbox placeholders), 1 `${study.img}` (template literal in scope-engine), 3 SVG logos on press.html (SVGs scale, not in dim map). | Cumulative Layout Shift (CLS) is one of three Core Web Vitals — a Google ranking signal. Without intrinsic dimensions browsers don't know an image's aspect ratio until it downloads, so the page reflows as imgs arrive. With width/height declared, the browser reserves the right-sized box up front. Dim map built by parsing `file <img>` output for every jpg/png/webp/jpeg on disk. The injector is multi-line aware (some `<img>` tags span 4-5 lines). Skips imgs that already have width, empty src, external/data URLs, JS template literals, and srcs not in the dim map. |
| May 30 | Phase 3 audit #3: added `loading="lazy"` to 576 imgs and `decoding="async"` to 1,685 imgs across 455 HTML files. Both attrs now at 100% coverage (4,528/4,528). 978 LCP-protected imgs (those with `fetchpriority="high"` or pre-existing `loading="eager"`) deliberately left with eager loading. | Lazy loading defers below-fold image fetches until the visitor scrolls near them — cuts initial network requests. Async decoding lets the browser decode imgs off the main thread, so layout + interactivity aren't blocked while a big image decodes. Together these are a low-risk perf improvement that doesn't change LCP (the eager-marked imgs are left alone — the visitor's first viewport renders as fast as before). |
| May 30 | Phase 3 audit #4: injected `Privacy` and `Terms` links into the `<div class="footer-bottom">` block on 963 pages + 1 hand-edit on `partners.html` (which uses `lp-footer-bottom` variant). Privacy + Terms link coverage went from 2 pages → 965. Multi-line aware awk with depth-tracking handles both single-line `<div class="footer-bottom">...</div>` and multi-line variants including WPB landing's nested-div children. Idempotency check: re-running the awk on already-injected files produces zero diff. | Legal/compliance hygiene: most jurisdictions (GDPR, CCPA, Florida AG enforcement) require Privacy + Terms to be reasonably discoverable. Before this commit they existed but were orphan pages (only the dealer-portal page and self-references linked to them). Now they're discoverable from any footer on the site. |
| Jun 4 | FL city coverage sweep + scope correction (Computer, 95c53b15 → da2bd990): Connor flagged that GSC showed ZERO clicks from any city query in 28 days despite 30+ existing city pages, AND that the site over-emphasized impact glass / HVHZ while the company does the full Division 08 scope. Three parallel ships: (a) Full-scope + Nashville Q3 2026 sweep on 298 existing FL city/service pages — idempotent injectable blocks (`data-acg-block` markers) added two sections before footer: 'Full Commercial Glass Scope' (12 service categories: storefront, curtain wall, impact, sliding/folding doors, interior glass, glass railings, mirrors, fire-rated glazing, automatic entrances, decorative/specialty, skylights, service/retrofit) and 'Nashville Q3 2026 expansion' linking to commercial-glazing-nashville-tn.html. (b) 26 new substantive city landing pages built for previously-missing major FL markets: Miramar, Coral Springs, Plantation, Sunrise, Homestead, Palm Bay, Melbourne, Miami Gardens, Lehigh Acres, Spring Hill, Riverview, Brandon, North Port, Sunny Isles Beach, Largo, Sanford, Tamarac, Lauderhill, Royal Palm Beach, Key West, Coconut Creek, Margate, Apopka, Pinellas Park, St. Cloud, Greenacres. Each page is NOT a template clone — includes city-specific market intro, population, county, metro, HVHZ status with correct code zone framing (Key West 190 mph; Pembroke Pines/Miramar HVHZ NOA; Brandon/Riverview non-HVHZ FBC Ch 16; etc.), nearest ACG office + drive distance, 5 named real-market project types, LocalBusiness JSON-LD with real geo coords, BreadcrumbList schema, canonical-tagged. (c) All 26 added to sitemap.xml at priority 0.7. (d) IndexNow ping submitted 28 URLs to Bing/Yandex/Yep/Naver. (e) Banned-brand audit confirmed clean: all 10 Kawneer/YKK/Tubelite paths from before the May 26 purge are 14-line noindex/canonical redirect stubs. Zero non-redirect references. (f) Form-tracking fix from earlier in day verified live: gtag('generate_lead') now fires only on response.ok=true, with new form_submission_failed event for diagnostic. Scripts persisted: workspace/city_sweep.py (idempotent injector), workspace/build_missing_city_pages.py (template), workspace/build_missing_city_pages_batch2.py. | The 30 existing city pages weren't ranking because they were near-duplicate templates emphasizing impact-only services. The sweep + 26 new pages fix three problems at once: (1) accurate code framing per city (no Miami-Dade NOA references on Pensacola; 190 mph design wind on Key West), (2) full Division 08 scope visible on every page (not just impact), (3) Nashville Q3 2026 surfaced on every FL page so future Tennessee searches find ACG. Total city footprint: 56+ FL cities. |
| Jun 2 | KG Perfection + LLM Ranking sprint (Computer, 1f5ff617 → e7ca8f42): comprehensive Knowledge Graph + AI-engine ranking upgrade. (a) Org schema v2: ImageObject logo with width/height (200x200 acg-mark.png), geo {lat,lng} on Org + each of 3 office LocalBusinesses (26.70716/-80.05707 WPB, 26.20528/-81.79975 Naples, 27.96863/-82.56867 Tampa), priceRange '$$$', knowsLanguage en/es, serviceArea GeoCircle (500km radius), hasOfferCatalog with 7 nested categories and 16 concrete Service offerings (ESWindows ES-9500/ES-8000, curtain wall stick+unitized, PGT/Slimpact impact, Euro-Wall folding/multi-slide, Allegion auto entrances, TGP fire-rated, Division 08 single-source), makesOffer for 48-hour bid turnaround, currenciesAccepted, paymentAccepted. (b) Person schemas v2: ImageObject images with dimensions (Connor 1072x1072, Rielly 800x1000) and captions, spouse + colleague cross-links between #connor-walsh and #rielly-walsh, memberOf + workLocation cross-links to #organization and #hq-west-palm-beach, nationality, mainEntityOfPage, hasOccupation with estimatedSalary band. Rielly canonical URL changed to /author/rielly-walsh/ (purpose-built bio page). (c) Author page consolidation: /author/connor-walsh/index.html and /author/rielly-walsh/index.html now both use canonical @ids #connor-walsh and #rielly-walsh respectively (was disconnected stubs before). (d) Blog post author/publisher canonicalization on all 238 posts: every Article/NewsArticle/BlogPosting/TechArticle uses canonical Person @id #connor-walsh for author and canonical Org @id #organization for publisher (with name/url/logo fallbacks for non-graph-aware parsers). Visible byline added to 14 posts that were missing it. (e) Org @id canonicalization site-wide: 665 additional pages now reference @id 'https://acglass.com/#organization' (1,073 pages total, up from 616) — normalizes alias IDs (#org, #localbusiness, etc.) and adds canonical @id where missing. Extended regex handles JSON-LD arrays [{...},{...}] used on architect-specs and city pages. (f) New /facts.html: citation-ready knowledge page for AI engines with FactCheck schema, WebPage + SpeakableSpecification, BreadcrumbList. Plain-text verifiable claims about ACG (identity, leadership, offices with geo coords, track record, manufacturer authorizations, certifications, disambiguation, external identity graph, contact). Added to sitemap.xml at priority 0.8. (g) New /wikipedia-draft.html: noindex,follow staging article in Wikipedia infobox style — ready for AfC submission and Wikidata Q139858578 enrichment by the EthicalWiki hire (pending). (h) llms.txt updated: facts.html surfaced at top of Identity section, canonical Person @ids documented next to each leader, Rielly URL corrected to /author/rielly-walsh/. (i) All 3 original KG pages re-validated post-changes via validator.schema.org and Google Rich Results Test: 0 errors / 0 warnings on all 3 URLs, eligible for rich results. | Knowledge Graph entity graph is now tightly connected: 1,073 pages tell Google these all describe the same ACG entity, 238 blog posts tell Google Connor wrote them, Connor + Rielly are cross-linked as spouses + colleagues + co-founders + co-employees, ACG founder[]/employee[] arrays reference both via @id. Geo coords + service catalog + price range complete the LocalBusiness signal Google uses for map pack ranking. The new /facts.html and /wikipedia-draft.html give AI engines (ChatGPT, Claude, Perplexity, Gemini) clean structured fact sources they can cite verbatim. The Wikipedia draft, once published, will seed Wikidata which feeds directly into Google KG and LLM training/RAG. |
| Jun 2 | Knowledge Graph schema ship (Computer, d0684c7a → 0f1139a1): (a) NAP unification site-wide — Naples moved from 1415 Panther Lane (34109) to 4850 Tamiami Trail N Ste 301 (34103) on Connor's confirmation; corrected stale Tampa references from '400 N Ashley Drive Suite 2600 (33602)' to the real '3031 N Rocky Point Dr W Ste 600 (33607)' per press release / Tampa landing page. 20 files, 32 Naples + 40 Tampa street swaps, 36 zip swaps. Byte-for-byte consistent across display copy, JSON-LD postal addresses, Google Maps iframes, and meta tags. (b) Canonical entity graph for Google Knowledge Graph: merged homepage Org schema into single canonical #organization block (was 3 competing Org-type blocks before — deleted duplicate @graph Org + anonymous LocalBusiness at line 108437). Added founder[]/employee[] cross-links via @id to #connor-walsh + #rielly-walsh. Logo updated to /images/acg-mark.png (200x200 square, KG-compliant). Replaced /author-connor-walsh.html Person schema with canonical @id #connor-walsh (was author-connor-walsh.html#person). Replaced ai-overview.html Org schema with merged canonical + appended Rielly Person @id #rielly-walsh (alumniOf MTSU w/ Wikipedia sameAs). Headshots: /images/team/connor-walsh-portrait.jpg + /images/team/rielly-walsh-portrait.jpg (both live since May). (c) Validator clean-up pass: removed Person.founder (not a valid Schema.org property on Person — inverse is declared via Org.founder[] cross-link), fixed homepage WebPage.speakable.cssSelector (dropped non-matching .section-intro + p[data-reveal][data-delay=200] selectors), stripped misplaced Organization-level props (alternateName, disambiguatingDescription, naics, iso6523Code) from FAQPage Q0 on ai-overview.html, cleaned WebSite block (removed naics/iso6523Code, simplified publisher to plain @id ref). Final: all 3 URLs pass validator.schema.org with 0 errors / 0 warnings AND Google Rich Results Test eligible (homepage 9 valid items, ai-overview 10 valid items, author page 1 valid item). | Tells Google these 3 entities are connected: ACG → founded by + employs Connor + Rielly; Connor + Rielly → worksFor ACG. Cross-page @id linking is the foundation for Knowledge Graph recognition. NAP unification fixes a real factual error (stale Tampa Ashley Drive on 20 SEO pages) and aligns site copy with Connor's Naples office move. |
| Jun 2 | SEO Ship batch (Computer, d1938f16 → e3edf3ae): (1) Related Resources cluster-link block rolled out to 231 blog posts (7 already had it) — each post gets 4 contextually relevant links via 2 baseline pillars + 2 topic-detected from slug keywords (topic dist: DEFAULT 136, GC 30, IMPACT 22, COSTS 12, PROCESS 11, STOREFRONT 10, CURTAINWALL 6, EUROWALL 3, AI 1). Script persisted at workspace/blog_cluster_linking.py. (2) New `/author-connor-walsh.html` with full Person JSON-LD: @id, jobTitle, knowsAbout (12 topics), hasCredential (CGC1531993), worksFor → @organization reference, sameAs LinkedIn, ProfilePage wrapper, BreadcrumbList. Hero with CW letter avatar, 6 fact cards, 4-link Related Resources block. Closes the 404 from blog post #1's byline link. Already in sitemap at priority 0.7. (6) Stripped last 7 pages off Google Fonts CDN — 6 concepts/* pages (Fraunces) + multifamily page (Manrope) all swapped to self-hosted Inter variable woff2 with inline @font-face. Zero remaining fonts.googleapis.com refs site-wide. | Items 1+2 build E-E-A-T author authority signals (named glazing expert) + internal link equity distribution. Item 6 closes the open-issue line about 7 pages still hitting Google Fonts — site now 100% self-hosted typography. |
| May 30 | Persisted the Phase 2/3 awk tooling into `scripts/`: `lazy-async-inject.awk`, `dim-inject.awk`, `strip-google-fonts.awk`, `inject-legal-footer.awk` (alongside the earlier `sitemap-prune.awk`). Each script's header documents the near-miss bugs caught during the audit pass — gawk `\1` backref non-expansion, aggressive blank-line deletion, `RS="\0"`-before-`getline` ordering, Google-verification-stub byte sanctity, lazy/`fetchpriority="high"` skip-condition gap, and depth-tracking for nested-div footer-bottom. | Next session (human or AI) running these tools inherits the documented failure modes instead of rediscovering them. Caveat for whoever picks up `scripts/add-lazy-loading.py`: that Python script has the same skip-condition gap that produced the LCP collision (commit `8c6b5a74`'s fix). Worth applying the same defensive update — skip on `fetchpriority="high"` regardless of `is_first` index. |

---

## 8. Open / known issues

- **`/eau-palm-beach-resort.html`** — Connor decided to leave it for now (May 30). Page still draws 1 click / 38 impressions per 14 days. Flagged on the unverified-project list.
- **Sticky CTA only on WPB landing page** — could roll out to other 78 city pages. Hasn't been requested yet.
- **Dealer Portal Cloudflare Worker NOT deployed** — `workers/dealer-portal-api/` is in the repo but Connor needs to `wrangler deploy` it. Until then, become-a-dealer.html falls back to mailto.
- **Audit branch Phase 3 (REWORKS) partially complete** — see `AUDIT-TRIAGE.md` on origin/audit/dedupe-og-tags. Shipped May 30: Phase 2 (CSS var aliases, 404 robots dedupe, noindex out-of-state, theme-color) + Phase 3 first item (self-host fonts). Still queued: image dimensions for CLS (~30 min), privacy/terms in footer (~20 min), `loading="lazy"` + `decoding="async"` (~15 min), city-pill + other inline-style → CSS class extractions (~1-2 hrs), broken-link re-audit. Each needs re-extraction against current main due to file drift, not a verbatim cherry-pick.
- **Google Ads "Fix it" call-only banner** — Claude Browser couldn't click through due to an ad blocker in Connor's session. Open question: which legacy call asset is being flagged for Feb 2027 deprecation.
- **AI visibility on commercial queries: 0%** — long-term work, not a today issue.
- **Verification flags still open**: Eau Palm Beach Resort, Ocean Prime at Pier Sixty-Six, Gulf Harbour EOC (vs. verified Gulf Harbour Y&CC), Haines City (Public Safety Complex with Aldora glass NOT Euro-Wall EOC), ESWindows "flagship installer" claim (use "Authorized installer" only). Skipped these in May 30 late-night Project schema pass.

---

## 9. First-time setup for Claude Code (Connor: run these once)

```bash
# 1. Clone the repo (if not already)
gh repo clone cwalsh7997/acglass-website ~/acglass-website
cd ~/acglass-website

# 2. Verify you can push (you should be authenticated via gh)
git config user.email "connor@acglass.com"
git config user.name "Connor Walsh"
git push origin main --dry-run

# 3. Start Claude Code from this directory
claude
```

Then in Claude Code, your first prompt:

> Read `CLAUDE.md`. That is your operating context. Then list every file in the repo root, summarize what each landing-page type does, and tell me what you're ready to work on.

That's it — Claude Code will read this file automatically on every session if you start it from this directory.

---

*Last updated: May 30, 2026 by Computer (Connor's Perplexity agent)*
