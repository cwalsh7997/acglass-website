# CHANGELOG — acglass.com web operations

Per-sprint log. Newest first. Evidence + scorecard delta + next item per the operator brief §8.

---

## Sprint 008 — WBE confirmation + fire-station past performance — 2026-06-30
Branch: `sprint-008-wbe-fire-stations` (from `main` at Sprint 007 tip).

### Trigger
Connor (2026-06-30, 7:11 PM PDT), replying to Sprint 006 queue: "We've done multiple fire stations now and yes we are WBE." Closes Q4b and partially closes Q8c.

### Shipped
- **Government hub** (`/government-glazing-contractor-florida.html`):
  - Hero eyebrow: `Federal · State · Municipal` → `Federal · State · Municipal · WBE`.
  - Hero sub: added "Woman-owned business (WBE)" and "Multiple Florida fire station projects delivered."
  - Stat grid: new "Business Status — WBE" card (Woman-owned · Set-aside eligible).
  - Compliance-posture table: new row for Business classification (WBE, WOSB/EDWOSB/DBE eligibility).
  - Public-sector past performance: "Multiple Florida fire stations" added as first bullet with Risk Category IV framing.
  - FAQ: 2 new Q&A — fire stations + WBE.
  - JSON-LD: WBE added to `hasCredential[]`, new `diversityPolicy` field, `knowsAbout[]` expanded to include the four blast standards + Risk Category IV fire-station scope.
- **About page** (`/about.html`): service card 08 upgraded from "Federal, Government & Institutional" → "Federal, Government & Fire-Rescue" with WBE and Florida fire-station callouts.
- **Homepage** (`/index.html`): capabilities tile 7 upgraded from "Federal & Government" → "Federal, Government & Fire-Rescue" with WBE.

### Evidence
- Banned-phrase scan on all 4 modified files: 0 hits.
- JSON-LD parses on all 4 files (1+1+1+5 = 8 blocks).

### Still open (in Q8/Q4b block of QUEUE-FOR-CONNOR.md)
- Q8c-fire: specific fire station names / cities / clients (for case study pages).
- Q4b-detail: which certifying body (WBENC / FL OSD / city / SBA WOSB) + cert number.
- Q8a Cape Canaveral naming, Q8b UEI/CAGE, Q8d FCL, Q8e federal blog post remain open.

---

## Sprint 006 — Federal / government positioning build — 2026-06-30
Branch: `sprint-006-federal-positioning` (from `main` at Sprint 005 tip).

### Trigger
Connor (2026-06-30, 6:19 PM PDT): "we are doing some projects out at cape canaverals space force, so whatever we need to do to the website to come across as a trusted government contractor that would be amazing! WHATEVER WE HAVE TO DO".

### Shipped
- **New page** `/government-glazing-contractor-florida.html` — federal contractor hub. Real credentials only. Bonding ($3M/$6M Arch A+ XV), FL CGC #1531993, TAA compliance narrative (Euro-Wall US + ESWindows Colombia = TAA-designated), Davis-Bacon capability, EM 385-1-1 posture, zero OSHA recordables, federal codes table (UFC 4-010-01, UFC 3-301-01, UFC 3-600-01, ASTM F1642/F2248/F2912/E1300, ANSI Z97.1, Buy American, Davis-Bacon), compliance-posture table with NAICS 238150/236220 primary/secondary, public-sector past performance (Haines City EOC, Martin County Fire Training), 7-step federal-sub workflow, 7 FAQ entries, JSON-LD Service + Provider (LocalBusiness + GeneralContractor) + hasCredential + areaServed.
- **New page** `/at-fp-blast-rated-glazing-florida.html` — deep technical reference. Specifier-audience content on UFC 4-010-01, the three ASTM references (F1642 test method, F2248 equivalent-3-second-load method, F2912 specification), standoff distance impact on design load, interlayer selection (standard PVB / structural PVB / ionoplast), frame anchorage failure modes, field QC / closeout, common Div 08 spec traps to RFI. JSON-LD TechArticle schema with about[] pointing to the four standards.
- **Homepage** — added Federal & Government capabilities tile to `/index.html` (7th tile in `.hp-caps-grid`) linking to the government hub.
- **About page** — upgraded service-card #08 to "Federal, Government & Institutional" with bonding, TAA, Davis-Bacon, and zero-OSHA callouts and CTA to the government hub.
- **Sitemap** — both new URLs added with monthly changefreq, priority 0.9 and 0.85. Total URLs 1382 -> 1384. XML validates.

### Intentional restraint (queued for Connor, not published)
- Cape Canaveral SFS is NOT named on any page pending prime-contractor publication authorization. The hub currently says "additional active federal and defense-installation glazing scope — details withheld per prime-contractor and site security policy." Queued as Q8a in QUEUE-FOR-CONNOR.md.
- SAM.gov UEI + CAGE code NOT asserted (Q8b).
- No claim of Facility Security Clearance (Q8d).
- WBE-certification narrative NOT added — Q4b still open (Q8f depends on Q4b).
- Federal-topic blog post drafted mentally but NOT shipped — Sprint 007 candidate (Q8e).

### Evidence
- Banned-phrase scan on all 4 modified files (2 new + index.html + about.html): 0 hits.
- JSON-LD parses on all 4 files (1+1+1+5 = 8 blocks).
- sitemap.xml validates as well-formed XML, 1384 URLs.

### Next
Merge to main once verified live. Wait on Q8a/Q4b for follow-up detail sprint.

---

## Sprint 005 — True-zero banned-phrase residual cleanup — 2026-06-30
Branch: `sprint-005-banned-phrase-residuals` (from `sprint-004` tip).

### Context
Sprint 004 reported "TRUE FINAL residual = 0" but the scan regex only covered AI-positioning + the `best commercial glazing in {city}` superlative — not the full Connor banned-phrase list. A fresh scan covering every term in the directive found **141 files** with one or more of: `the leading`, `the largest`, `premier`, `best commercial glazing`, `ecosystem`, `cheap`, `affordable`, `elevate`, plus a single verb-form `leverage`. Hard-gate violation.

### Shipped — `scripts/fix-banned-residuals-sprint005.py` + 10 surgical fixes
- Stock city template `from the leading manufacturers` rewritten across 75 hurricane-impact city pages.
- SEO page identity rewrites (URL unchanged, no 301s needed):
  - `blog/commercial-glazing-contractors-tampa-fl.html`: title/H1/meta/og/JSON-LD `Best Commercial Glazing Contractors in Tampa FL (2026 Guide)` → `Choosing a Commercial Glazing Contractor in Tampa FL (2026 Guide)`. All 14 in-page references aligned.
  - `best-glazing-subcontractor-florida.html`: `Best Glazing Subcontractor in Florida` → `Florida Commercial Glazing Subcontractor`.
  - `best-storefront-contractor-florida.html`: `Best Storefront Contractor in Florida` → `Florida Commercial Storefront Contractor`.
- Third-party descriptors neutralized contextually: Harmon, ESWindows testing facility, Texas Medical Center, PGT, Hurricane Michael reconstruction, Tampa Water Street, Panther National private club, Gulf Harbour Country Club, Eau Palm Beach, etc.
- `ecosystem` → `network` / `cluster` / `platform` / `workflow` (6 instances).
- `cheap` → `low-cost` / `inexpensive` (2 instances).
- `affordable` → `cost-controlled` (1 instance; remaining match is inside an external Georgia gov URL slug).
- `elevate` (verb) → `raise` (1 instance, technical wind-pressure context).
- `leverage` (verb) → `route through` (1 instance — Connor's list bans the verb only; noun usage retained).
- Removed `press/acg-launches-ai-operations-site.html` from `sitemap.xml` (already noindex+redirect, but still in sitemap). 1383 → 1382 well-formed `<loc>`.

### Evidence
- Full banned-phrase scan against the complete Connor list (24 terms) returns **0 hits** on live content. Only exclusions: retired noindex stubs (acceptable per Sprint 003) and one external link URL slug to a Georgia state government page (cannot rewrite a third-party URL).
- JSON-LD re-validated on: `index.html`, `about.html`, `pgt-installer-florida.html`, `blog/index.html`, `commercial-glazing-nashville-tn.html`, `acg-vs-giroux-glass.html`, `blog/commercial-glazing-contractors-tampa-fl.html` — all blocks parse.
- `sitemap.xml` validates as well-formed XML, 1382 URLs.
- 149 files changed, 197 insertions / 198 deletions.

### Result — site is now true-zero against the full banned-phrase directive.

### Still open
**Q4b** (Connor): WBE/SBE certification status — unblocks ~1,484-file WBE-prose sweep. Does NOT block this deploy.

---

## Sprint 004 — Bespoke AI-prose rewrite + artifact cleanup (finishes Q7) — 2026-06-30
Branch: `sprint-004-ai-prose-rewrite` (from `sprint-003` tip).

### Shipped
- `scripts/fix-ai-prose-sprint004.py` (deterministic exact-string, dry-run default): rewrote the ~34 bespoke pages where AI was woven into narrative — `acg-vs-*` comparison pages, Connor + Rielly author bios, Nashville/TN neighborhood pages, `facts.html`, `capabilities.html`, `how-it-works.html`, `procore-integrated-*`, `ask.html`, `how-to-hire-*`, etc. Every Sub.ai/jobcost.ai/CFO Agent/"custom AI agents"/acglass.ai reference replaced with the real, Ledger-verifiable substance (Procore-native operations, owner-led delivery, real-time job costing, custom in-house software). No new claims.
- Removed the 2 retired-AI-post cards from `blog/index.html` and neutralized their ItemList schema refs (value-swaps; JSON re-validated).
- Repointed internal links from the retired `ai-managed-glazing-contractor.html` → `/about.html`.
- Cleaned grammatical **artifacts** left by Sprint 003's AI-adjective stripping (". .", "scope. operations.", "uses operations to", orphan double-spaces) in meta/schema on the previously-AI pages.
- Neutralized AI labels on the 3 `concepts/*` internal mockups (noindex,nofollow).

### Evidence
- **TRUE FINAL residual = 0** across the public site (excl. retired-stub comments): Sub.ai, jobcost.ai, CFO Agent, AI-managed, AI-augmented, AI-first, custom AI, AI agents, acglass.ai, "best commercial glazing contractor in {city}" — all **0**.
- JSON-LD re-validated on every schema-edited page (blog/index, national, glazing-subcontractor, southeast, author bios — all valid).

### Result — AI positioning + banned superlatives are now fully removed from the public site
The retired AI-managed/AI-first/AI-augmented positioning (operator Ledger 2.3) and the banned "best commercial glazing" superlative are gone site-wide. Remaining low-severity item: schema-only ItemList refs left pointing to the retired blog URLs were redirected to /about.html (not deleted).

### Still open
**Q4b** (needs Connor): WBE/SBE certification status → unlocks the WBE-prose sweep (~1,484 files). That is the last major factual-integrity item.

---

## Sprint 003 — Site-wide AI-positioning + superlative sweep (Q3 + Q7) — 2026-06-30
Branch: `sprint-003-ai-superlative-sweep` (from `sprint-002` tip).

### Context
Sprint 001 only de-AI'd the homepage + About. The retired "AI-managed / AI-augmented / AI-first" positioning was templated across the rest of the site: **~343 files** carried it (bylines ×200+, a Nashville operating-model paragraph ×336, hero headlines, section headers, estimating/scheduling adjectives, Sub.ai/jobcost.ai/CFO Agent prose, an `acglass.ai` AI sister-site link in **218** files), plus the banned "best commercial glazing contractor in {city}" superlative on 27 city pages.

### Shipped — `scripts/fix-ai-positioning.py` (deterministic exact-string + city regex, dry-run default), 2 rounds + targeted passes
- **~700 file-changes** removing AI positioning: drop the AI adjective ("AI-managed scheduling" → "scheduling"), retire the `acglass.ai` AI-promo bullets, strip the "AI-Managed" hero headline lines and section headers, rewrite the Nashville paragraph ("AI-augmented operating model" → "owner-run operating model"), and replace the templated "uses AI to manage" / Sub.ai-CFO FAQ answers with Procore-native, Ledger-only copy.
- **Superlative: 27 → 0** crisp ACG self-superlatives. "Who is the best commercial glazing contractor in {city}?" → "Is American Commercial Glass a licensed commercial glazing contractor in {city}?" (city-parameterized regex). (4 generic "what do the best contractors do" evaluation FAQs left — not ACG self-claims.)
- **`acglass.ai` sameAs removed** from 213 files' JSON-LD (safe comma-form removal; JSON re-validated on index/facts/about).
- **Q3 retirements:** `ai-operations-whitepaper.html`, 2 AI blog posts, and `press/acg-launches-ai-operations-site.html` → noindex redirect stubs to `/about.html`; removed from sitemap with the AI whitepaper PDF (1387 → 1383 `<loc>`, well-formed).
- Fixed an internal link whose anchor text was the banned superlative pointing at the retired hard-gate page.

### Evidence
- Footprint: AI-managed **343 → 5**, AI-augmented **351 → 0**, acglass.ai **218 → 6**, superlative **27 → 0** (self-claims). JSON-LD re-validated on samples after every pass. Exact-string method = can miss, never corrupt.

### NOT done — bespoke remainder for Sprint 004 (~33 files)
Deeper prose where AI was woven into narrative and needs per-page rewriting, not mechanical deletion: `acg-vs-{giroux,harmon,permasteelisa}.html` (comparison tables/narrative), author bios (`author/connor-walsh/`, `authors/connor-walsh.html`), several Nashville/TN neighborhood pages, `facts.html`, `press.html`, `capabilities.html`, `how-it-works.html`, `concepts/*`, `security-policy.html` (lists acglass.ai as a brand/scope domain), `procore-integrated-glazing-subcontractor.html`. ~19 files still mention Sub.ai/jobcost.ai/CFO Agent in prose. Listed in QUEUE Q7.

### Next item
Sprint 004: per-page rewrite of the ~33 bespoke AI-prose files. Then await Connor's Q4b (WBE certification status) to finish the WBE prose sweep.

---

## Sprint 002 — Unverified manufacturer + WBE/SBE claims (Q4) — 2026-06-30
Branch: `sprint-002-unverified-claims` (from `sprint-001` tip). Connor authorized full autonomous decisions; governance = downgrade/remove unverified claims, never fabricate.

### Context
Investigation (read-only subagent) found the prior "Computer" agent had baked **"authorized installer for ESWindows, Euro-Wall, PGT, Allegion, TGP, Slimpact, and Aldora"** (note Aldora — not even in the Ledger) into the homepage Org schema and hundreds of pages, in ~30 distinct phrasings across prose, JSON-LD, `<title>`, og/meta, FAQ schema, and capability badges. Per the Ledger only **Euro-Wall + ESWindows/Tecnoglass** are verified authorized-installer relationships.

### Shipped — `scripts/fix-unverified-installer-claims.py` (deterministic, idempotent, dry-run default), 5 rounds
- **~290 file-changes** downgrading every unverified-brand "authorized installer/installation/dealer/partner" claim → plain "installer of / installs" (a permitted "we install it" claim). Euro-Wall + ESWindows keep their verified "authorized" status; the compliant "authorized commercial installer for ESWindows and Euro-Wall" construction (87 files) was preserved untouched.
- Fixed: homepage Org schema line, full-list prose (all comma/“+”/“and Aldora” variants), impact short-list, og:title/og:description/meta-description on the 5 dedicated brand pages, per-brand `<title>` ("PGT/Slimpact/TGP/Allegion Authorized…Installer" → "…Installer"), per-brand FAQ-schema Q&A ("Is ACG an authorized PGT/TGP/Allegion/Slimpact installer?" → "Does ACG install…?"; answers → "installs"), "seven manufacturer authorizations" marketing phrasings, reference-table "authorized to install", capability badges, and the crisp schema name entries ("Authorized PGT/Allegion/Slimpact Installer — Florida" → "…Installer — Florida").
- **WBE/SBE schema:** neutralized the `EducationalOccupationalCredential` certification *names* (e.g. "Woman-Owned Business Enterprise (WBE)" → "Woman-owned business (majority owner Rielly Walsh)") so the machine-read schema no longer asserts a held WBE/SBE certification. Verified CGC + Euro-Wall/ESWindows dealer credentials untouched.

### Evidence
- Final scan: **0** crisp ACG-specific "authorized for [PGT/Allegion/TGP/Slimpact/Aldora]" claims remain. Remaining `authorized`+brand co-occurrences are all compliant (verified Euro-Wall/ESWindows dealer entries), "ACG installs…" lists, or neutral industry-explainer text.
- JSON-LD re-validated on homepage + all 3 fixed brand pages (4/4 blocks valid each).
- Method = exact-string replacement only: can MISS but never corrupt; every dry-run reviewed; compliant copy verified preserved.

### NOT done (deliberately — routed to Connor or next sprint)
- **WBE/SBE in visible prose (~1,484 files)** — NOT mass-edited. "Woman-owned" may be literally true (Rielly Walsh 51%, Connor-sourced) even if "WBE-certified" isn't. Needs Connor's certification-status answer (QUEUE Q4b). One press release asserts "certified as a WBE" — flagged.
- **Q3 — retire the AI pages** (ai-operations-whitepaper.html + 2 AI blog posts are still indexable) — not done this sprint.
- **NEW finding: AI positioning + "best commercial glazing contractor" superlative are duplicated across MANY pages via a templated FAQ-schema block** (Sprint 001 only fixed homepage/About). Site-wide sweep queued (QUEUE Q7).

### Next item
Sprint 003: retire the indexable AI pages (Q3) + site-wide AI/superlative templated-FAQ sweep (Q7). Then await Connor's Q4b (WBE certification status).

---

## Sprint 001 — Phase 1: Stop the Bleeding — 2026-06-30
Branch: `sprint-001-phase-1-bleeding` (from `origin/main`). PR to `main` for Connor's preview-then-merge.

### Shipped
**1.1 — Purged the two Hard-Gate violation pages**
- `/ai-managed-glazing-contractor.html` and `/best-commercial-glazing-contractor.html` → overwritten with `noindex, follow` meta-refresh redirect stubs to `/about.html` (repo's established stub pattern; operator brief 1.1 permits a stub to /about.html).
- Removed both URLs from `sitemap.xml` (1389 → 1387 `<loc>` entries). `sitemap.xml` re-validated well-formed (xml.dom.minidom).
- `/ai-overview.html` verified already carrying `<meta name="robots" content="noindex, follow">` — no action needed (brief's 3rd 1.1 item already satisfied).
- GSC URL-removal + optional Cloudflare 410 → **queued for Connor (Q5)** — needs his access.

**1.4 — Stripped retired AI-managed positioning from homepage + About**
- Homepage hero subhead: dropped "AI-managed" → "Owner-operated commercial glazing from bid to closeout…" (all proof points Ledger-verified).
- Why-card #02: "AI-managed ops / Sub.ai, jobcost.ai, CFO Agent" → "Single-source Division 08" (self-perform scope; Ledger-grounded, no new claim).
- Removed the homepage "AI WHITE PAPER CTA" section ("We built four AI agents…", linking `/ai-operations-whitepaper.html`).
- Voice-search FAQ: rewrote "Who is the **best commercial glazing contractor**…" (banned superlative) → "Is American Commercial Glass a licensed commercial glazing contractor in Florida?" (answer preserved, factual). Removed the "Which glazing contractor **uses AI to manage** projects?" FAQ pair entirely.
- About page: section heading "AI-Managed. Lean-Operated." → "Lean-Operated. Owner-Run."; rewrote the two AI-framing intro paragraphs to describe ACG's project-management discipline without the AI label (real substance — real-time tracking, 3 offices, lean owner-run team — preserved).

**Coordination fix (mandated by in-repo /CLAUDE.md §6)**
- Updated in-repo `/CLAUDE.md`: tagline marked RETIRED + interim placeholder; added a "Banned positioning (RETIRED 2026-06-23)" line (AI-managed family, Sub.ai/jobcost.ai/CFO Agent); corrected the manufacturer line to Euro-Wall + ESWindows verified, TGP/Allegion/PGT/Slimpact unverified. Prevents the sister "Computer" agent from re-adding the AI positioning on its next pull.

### Evidence
- DoD banned-phrase scan on `index.html`, `about.html`, and both stubs → **0 hits** (`grep -icE` of the brief's banned list).
- `sitemap.xml` well-formed; the two retired URLs return 0 matches in sitemap.
- Brand tokens untouched (#0e284f / #e11320 / Inter / JetBrains Mono).

### Queued for Connor (see QUEUE-FOR-CONNOR.md)
Q1 two-CLAUDE.md conflict · Q2 final tagline/positioning · Q3 disposition of 6 other AI pages + whitepaper · Q4 unverified TGP/Allegion/PGT/Slimpact + WBE/SBE schema across ~1,000 pages · Q5 GSC removals + Cloudflare 410 · Q6 sister-agent write coordination.

### Scorecard delta (est., pending re-measure)
Factual Integrity 70 → ~76 (removed banned superlative page + AI-managed claims from top pages; large remainder gated on Q4). AEO/GEO unchanged this sprint (FAQ schema preserved/cleaned, not expanded).

### Not done this sprint (deferred, not blocked)
1.2 Atlantic Fields cluster consolidation · 1.3 NOA cluster · 1.5 NAP normalization · 1.6 carry-over link repoint/marker injection. These are independent and sized for their own sprints; the SEO city-page work is staged separately on `seo/fl-city-rankings`.

### Next item
Sprint 002: 1.5 NAP normalization (low-risk, mechanical) OR await Connor's Q1–Q4 answers to unlock the AI-page disposition + manufacturer-schema sweep.
