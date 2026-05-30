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
| May 30 | Phase 2 audit #5: declared `--font-mono` and `--text-muted` CSS vars in `:root` of `css/style.css` (alias for `--mono` and `--white-50`) | ~1,500 inline `style="..."` instances reference these var names; without the declarations, byline + caption text was silently falling back to defaults |
| May 30 | Phase 2 audit #8: deduped `<meta name="robots">` in `404.html` (had two conflicting tags: `noindex,follow` and `noindex, nofollow`) — kept `noindex, nofollow` | Conservative for an error page: don't waste crawl budget on links from a 404 |
| May 30 | Phase 2 audit #6: added `<meta name="robots" content="noindex,follow">` to 9 out-of-state pages (commercial-glazing-{alabama,georgia,louisiana,tennessee,texas,north-carolina,south-carolina,southeast}.html + national-commercial-glazing-contractor.html); pruned the same 9 URLs from `sitemap.xml` (1371→1362 entries) | ACG is FL-licensed only. Pages were attracting leads ACG can't fulfill + risking HCU demotion for templated localized content. `noindex,follow` preserves any inbound-link equity while removing the pages from Google's index over the next 4-8 weeks. |
| May 30 | Phase 2 audit #7: added `<meta name="theme-color" content="#0e284f">` after the viewport meta on every eligible HTML page (1,417 inserts + 4 wrong-color `#0D1E36` corrections); 12 files skipped (redirect stubs + Google verification stub — no viewport meta) | Mobile browser chrome (Chrome address bar on Android, status bar on iOS, Edge) tints to match the page color. Brand navy `#0e284f` per CLAUDE.md §3 |
| May 30 | Phase 3 audit: self-hosted Inter, JetBrains Mono, Playfair Display (Latin-subset variable woff2 in `fonts/`). Added 4 `@font-face` blocks at top of `css/style.css` with `font-display: swap`. Stripped `fonts.googleapis.com` `<link>` + both `fonts.gstatic.com`/`fonts.googleapis.com` preconnects + Inter `@import url(...)` from 1,275 pages. Inserted `<link rel="preload" as="font" type="font/woff2" href="/fonts/inter-variable-latin.woff2" crossorigin>` before each page's `css/style.css` link. Bumped css cache-buster to new epoch on all touched pages including the 4 dealer-portal pages (so cached pre-self-host CSS gets refetched on next visit). 7 pages skipped — 6 `concepts/*` (use Fraunces, not self-hosted) and 1 `multifamily-commercial-glazing-florida/index.html` (uses Manrope `@import`, not self-hosted). | Kills 3 third-party requests + 2 DNS lookups + 1 TLS handshake per page load (~200-400ms LCP improvement on mobile). Variable fonts give all weights in one file each (Inter 100–900, JBM 100–800, Playfair Display 400–900 upright + italic). Latin subset only — site is English. font-display:swap matches Google Fonts' prior behavior so visitors still see web fonts even on slow connections (vs `optional` which would never load web fonts on slow first visits). |
| May 30 | Phase 3 audit #2: added `width` and `height` attributes to 1,326 `<img>` tags across 455 HTML files. Coverage 70% → 99% (4,516 of 4,528 imgs declare intrinsic dims). 12 holdouts skipped by design — 8 empty `src=""` (dynamic JS lightbox placeholders), 1 `${study.img}` (template literal in scope-engine), 3 SVG logos on press.html (SVGs scale, not in dim map). | Cumulative Layout Shift (CLS) is one of three Core Web Vitals — a Google ranking signal. Without intrinsic dimensions browsers don't know an image's aspect ratio until it downloads, so the page reflows as imgs arrive. With width/height declared, the browser reserves the right-sized box up front. Dim map built by parsing `file <img>` output for every jpg/png/webp/jpeg on disk. The injector is multi-line aware (some `<img>` tags span 4-5 lines). Skips imgs that already have width, empty src, external/data URLs, JS template literals, and srcs not in the dim map. |
| May 30 | Phase 3 audit #3: added `loading="lazy"` to 576 imgs and `decoding="async"` to 1,685 imgs across 455 HTML files. Both attrs now at 100% coverage (4,528/4,528). 978 LCP-protected imgs (those with `fetchpriority="high"` or pre-existing `loading="eager"`) deliberately left with eager loading. | Lazy loading defers below-fold image fetches until the visitor scrolls near them — cuts initial network requests. Async decoding lets the browser decode imgs off the main thread, so layout + interactivity aren't blocked while a big image decodes. Together these are a low-risk perf improvement that doesn't change LCP (the eager-marked imgs are left alone — the visitor's first viewport renders as fast as before). |
| May 30 | Phase 3 audit #4: injected `Privacy` and `Terms` links into the `<div class="footer-bottom">` block on 963 pages + 1 hand-edit on `partners.html` (which uses `lp-footer-bottom` variant). Privacy + Terms link coverage went from 2 pages → 965. Multi-line aware awk with depth-tracking handles both single-line `<div class="footer-bottom">...</div>` and multi-line variants including WPB landing's nested-div children. Idempotency check: re-running the awk on already-injected files produces zero diff. | Legal/compliance hygiene: most jurisdictions (GDPR, CCPA, Florida AG enforcement) require Privacy + Terms to be reasonably discoverable. Before this commit they existed but were orphan pages (only the dealer-portal page and self-references linked to them). Now they're discoverable from any footer on the site. |

---

## 8. Open / known issues

- **`/eau-palm-beach-resort.html`** — Connor decided to leave it for now (May 30). Page still draws 1 click / 38 impressions per 14 days. Flagged on the unverified-project list.
- **Sticky CTA only on WPB landing page** — could roll out to other 78 city pages. Hasn't been requested yet.
- **Dealer Portal Cloudflare Worker NOT deployed** — `workers/dealer-portal-api/` is in the repo but Connor needs to `wrangler deploy` it. Until then, become-a-dealer.html falls back to mailto.
- **Audit branch Phase 3 (REWORKS) partially complete** — see `AUDIT-TRIAGE.md` on origin/audit/dedupe-og-tags. Shipped May 30: Phase 2 (CSS var aliases, 404 robots dedupe, noindex out-of-state, theme-color) + Phase 3 first item (self-host fonts). Still queued: image dimensions for CLS (~30 min), privacy/terms in footer (~20 min), `loading="lazy"` + `decoding="async"` (~15 min), city-pill + other inline-style → CSS class extractions (~1-2 hrs), broken-link re-audit. Each needs re-extraction against current main due to file drift, not a verbatim cherry-pick.
- **7 pages still load fonts from Google** — 6 `concepts/*` pages use Fraunces (a font ACG isn't otherwise using; the pages aren't in sitemap so not high-traffic), and `multifamily-commercial-glazing-florida/index.html` uses Manrope. To fully eliminate the Google Fonts dependency: either self-host Fraunces + Manrope, or convert those pages' typography to Inter. Not urgent.
- **Google Ads "Fix it" call-only banner** — Claude Browser couldn't click through due to an ad blocker in Connor's session. Open question: which legacy call asset is being flagged for Feb 2027 deprecation.
- **AI visibility on commercial queries: 0%** — long-term work, not a today issue.

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
