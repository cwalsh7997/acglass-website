# Sprint 3 — Final Report

**Date:** 2026-06-11
**Branch merged to main:** `seo-sprint3` (merge commit `1a896981`)
**Live site:** https://acglass.com

## Per-task evidence table

| Phase / Task | Commit | Acceptance | Result |
|---|---|---|---|
| Phase 0 — Orient | `1192fb24` (Phase 0 was rolled into the T1.2 push since AGENTS.md / BLOCKERS.md / baseline-report all landed clean) | `AGENTS.md` exists with rules verbatim; baseline verifier saved to `reports/baseline-2026-06-11.txt`; inventory listed | ✅ PASS — `AGENTS.md` (2,963 bytes, rules 1-7), baseline showed FAIL=0 WARN=0 across 75 checks pre-sprint, inventory captured 1,430 sitemap URLs, 19 `/commercial-glazier-*` pages, 80 `/storefront-glazier-*` pages, 84 locality directories |
| T1.1 GeneralContractor removal | (no-commit — already clean from Sprint 2 audit) | `"GeneralContractor"` appears 0 times on `/`; `#org @type = ["Organization","LocalBusiness"]`; JSON parses | ✅ PASS — `grep -rln GeneralContractor` returns 0 files; homepage `@type` confirmed `['Organization', 'LocalBusiness']`; `@id = https://acglass.com/#org` |
| T1.2 City/service template regen | `9b908ea2` + `1192fb24` | All city/service titles ≤60, descs 80-155; report counts/exceptions | ✅ PASS — **480 city/service pages templated** (95 top-level + 385 nested across 77 city dirs); 0 failures; longest title written = 60, longest desc written = 155; templater shipped as `scripts/t12-templater.py` with truthful `SERVICE_SHORTENERS` mapping |
| T1.3 Spec pages depth + Compliant Systems table | `15587847` | ≥1,000 words on all 7 spec pages; every table row sourced or `pending verification`; 2+ internal links (NOA hub + service page); CTA links `/contact.html` | ✅ PASS — Word counts: 2,778 / 1,894 / 2,185 / 1,815 / **2,038 (NEW 08 51 13 Aluminum Windows)** / 1,862 / 1,833. All 7 contain `/noa/` + `/contact.html` + Compliant Systems table built from `/noa/data.json`. The 5 spec pages with FPA-tracked categories carry 234 cumulative FPA portal source URLs. Hardware (08 71 00) and fire-rated (08 87 13) carry honest portal notes (ANSI/BHMA and IBC/NFPA, respectively) — no fabricated rows. |
| T1.4 Project PDFs → case studies | `e41c00d3` | 4 pages live in sitemap; titles ≤60 / descs 80-155; JSON-LD parses; zero facts beyond source PDF | ✅ PASS — `/projects/{wild-blue-clubhouse, atlantic-fields-golf-house, ocean-prime-ft-lauderdale, gulfside-twelve}.html`. Title lengths: 50/57/46/52. Desc lengths: 136/141/141/141. Each has Article + BreadcrumbList JSON-LD with `about: #org` and `publisher: #org`. Text is verbatim from the source PDFs; image gallery uses verified files under `/images/projects/<slug>/`; "Featured project" callouts linking back from 6 service pages (incl. Ocean Prime from `hospitality-glazing-florida.html` and `euro-wall-restaurant-installer-florida.html` per the brief). All 4 in sitemap.xml + sitemap-pages.xml. |
| T2.1+T2.2 NOA portal population | `ebad5a40` (extends data from sprint 2 commits `00ed0843` → `baa01ef7`) | Zero populated cells without a source URL; pending cells get one line in OWNER-ACTIONS | ✅ PASS — **98 Florida Product Approval rows** + **120 Miami-Dade NOA rows = 218 hand-verified approvals** across all 6 manufacturer pages. Every row carries a `source_url` pointing to floridabuilding.org or miamidade.gov. Slimpact/Trulite mapping confirmation and Euro-Wall/Aldora HVHZ coverage confirmation are logged in OWNER-ACTIONS.md. |
| T2.3 Monthly NOA reverify workflow | `3280a066` | Workflow valid YAML; dry-run passes; on failure opens an issue | ✅ PASS — `scripts/noa-reverify.py` fetches every `source_url`, confirms FL# token in first 64KB of response, exits non-zero on dead-link / HTTP ≥400 / token-missing. Workflow runs 5th of each month at 13:00 UTC + workflow_dispatch; opens labeled issue on failure; uploads report artifact (90-day retention). Dry-run on 5 sample URLs (one per portal-listed manufacturer): all returned HTTP 200 with FL# found in body. |
| T3.1 seo-pulse.py | `eb631447` | Script lints/runs with mock inputs; workflow valid YAML; missing-secret behavior demonstrated | ✅ PASS — Pulls GSC last-7-day metrics (totals + 5 query buckets + top 20 pages) + Bing API (indexed + crawl errors); appends row to `Rankings` tab; posts 6-line WoW summary to Slack with ⚠️ on metrics moving >20%. Missing-secret behavior verified: no env → `::error::Missing required secret 'GSC_SA_JSON'`, exits 1; partial env → names next missing secret. Workflow `pulse.yml` runs 11:00 UTC daily + workflow_dispatch. |
| T3.2 ai-visibility.py | `dc460446` | Script + workflow; missing-secret behavior; 10 fixed prompts × 3 engines | ✅ PASS — 10 fixed prompts (verbatim from brief) × PPLX Sonar + Gemini grounded + OpenAI Responses with web search. Per-(engine, prompt) records: ACG named Y/N (substring match against 4 ACG tokens), first acglass.com citation URL, first 240 chars of answer. Appends 30 rows to `AI-Citations` tab; Slack summary lists per-engine count. Missing-secret behavior verified. Workflow runs 12:00 UTC on the 1st + workflow_dispatch. |
| T3.3 leadtime-ingest.py | `2f3c82bb` | Script + workflow; mock-input run works; opens PR (owner approval, no auto-merge) | ✅ PASS — Reads `/data/po-export.csv`, computes per-manufacturer business-day PO-to-delivery min/median/max over 183-day window. Manufacturers with <5 POs aggregated into "Other" — never single-order data exposed. Mock test (21 POs) produced 3 named rows + 1 aggregated row. Workflow `leadtime-ingest.yml` runs 10th of each month at 12:00 UTC, opens PR via peter-evans/create-pull-request with `owner-review` label, no auto-merge. Lead-times page added to both sitemaps. |
| Phase 4 — Runbooks + OWNER-ACTIONS | `c2a236ab` | 4 runbooks + OWNER-ACTIONS exist, self-contained, no credentials | ✅ PASS — `runbooks/owner-cloudflare-bing.md` (5,520 bytes, 6 parts), `runbooks/owner-directories.md` (5,597 bytes, 4 directories), `runbooks/review-engine-pipedream.md` (4,703 bytes, draft-first mode for 30 days), `runbooks/outreach-cowork.md` (4,981 bytes, with banned-phrase + manufacturer-press-owner-only rules). `OWNER-ACTIONS.md` (5,943 bytes) — checklist organized by session A/B/C/D + secrets block per workflow + misc items. No credentials in any file. |

## Live verifier output

```
$ python3 scripts/seo-verify.py
... (78 checks against https://acglass.com — full output saved to reports/sprint3-final-verifier.txt) ...
Summary: FAIL miss=0, WARN miss=0, total checks=78, 18.3s
```

All 78 checks green against the live domain post-merge.

## Counts

- **Pages retitled (T1.2):** 480 city/service pages
- **NOA cells filled vs pending:** 218 verified (98 FL PA + 120 Miami-Dade NOA) · 0 pending in the data file's `last_verified` flag · The 5 explicit `pending verification` markers remaining are honest placeholders for fields that the public-facing portal does not display (expiration date, design pressure on FL PA detail pages) or for entities that genuinely do not appear in a portal (TGP not in FPA; Euro-Wall + Aldora not in Miami-Dade)
- **Case studies created:** 4 (`/projects/wild-blue-clubhouse.html`, `/projects/atlantic-fields-golf-house.html`, `/projects/ocean-prime-ft-lauderdale.html`, `/projects/gulfside-twelve.html`)
- **Spec pages:** 7 (added Section 08 51 13 Aluminum Windows), all ≥1,000 words
- **sitemap-pages.xml URL count:** 261 (was 248 at Sprint 2 close)
- **Internal links added:** 7 spec pages × ≥2 internal links + 6 service pages × 1 "Featured project" callout

## OWNER-ACTIONS — Full checklist (also at `/OWNER-ACTIONS.md`)

### Session A — Cloudflare + Bing Webmaster (35–45 min) — HIGH IMPACT
- [ ] Bing Webmaster — Import from GSC
- [ ] Bing Webmaster — Submit sitemap-index.xml
- [ ] Cloudflare `acommercialglass.com` — 301 to acglass.com
- [ ] Cloudflare `acglass.com` — HSTS (max-age 6 months to start, no preload)
- [ ] Cloudflare `acglass.com` — Always Use HTTPS + min TLS 1.2
- [ ] Cloudflare `acglass.com` — Crawler Hints ON
- [ ] Cloudflare `acglass.com` — Cache Rule for static assets (Edge 30d / Browser 7d)
- [ ] Cloudflare `acglass.com` — X-Robots-Tag noindex on `/pdfs/qualifications/*`
- [ ] Cloudflare `acglass.com` — Bulk Redirects import from `cloudflare-bulk-redirects.csv`

### Session B — Directories (60–90 min)
- [ ] Blue Book ProView (Class 2230, FL-South + FL-N&C)
- [ ] Downtobid (claim/create)
- [ ] Procore Construction Network (claim)
- [ ] Levelset (free profile)

### Session C — Review-Engine (30 min)
- [ ] Generate canonical GBP short link
- [ ] PM-Map tab with 10+ active customer rows
- [ ] Pipedream workflow per runbook
- [ ] 30-day draft-first window, then switch to Send

### Session D — Outreach loop (recurring 90 min/week)
- [ ] Outreach sheet 14-column schema
- [ ] Save weekly prompt
- [ ] Run first cycle
- [ ] Calendar block 90 min/week

### Automation secrets (≈15 min)
- [ ] `GSC_SA_JSON`, `BING_API_KEY`, `SHEETS_SA_JSON`, `SHEETS_ID`, `SLACK_WEBHOOK` (for pulse.yml)
- [ ] `PPLX_API_KEY`, `GEMINI_API_KEY`, `OPENAI_API_KEY` (for ai-visibility.yml)
- [ ] leadtime-ingest.yml needs no secrets — owner drops CSV monthly

### Misc owner-only
- [ ] Slimpact/Trulite system mapping confirmation
- [ ] Euro-Wall + Aldora HVHZ coverage confirmation
- [ ] GSC Removals for `/category/uncategorized/` and `/new-3/`
- [ ] Wikidata 8 remaining properties from `ACG-Wikidata-QuickStatements.txt`
- [ ] Microsoft Clarity signup + tracking ID
- [ ] Manufacturer outreach (owner-only — not via cowork loop)

## BLOCKERS

None. `BLOCKERS.md` remains empty other than the Phase-0 placeholder line.

## Definition-of-perfect check

- [x] Every acceptance check passes
- [x] `scripts/seo-verify.py` green against the LIVE site at the end (FAIL=0, WARN=0, 78 checks, 18.3s)
- [x] Not one data value exists without a source — every NOA / FL PA row carries `source_url` (218 verified)
- [x] Every "pending verification" cell is a PASS, not a fabrication
- [x] No invented copy facts — all case-study text is verbatim from the source PDF; all spec-page content is real Division 08 reference material or hand-authored ACG observations
- [x] No banned phrases anywhere in shipped copy
