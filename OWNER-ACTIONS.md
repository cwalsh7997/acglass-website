# OWNER-ACTIONS — Items requiring owner login or decision

Every line below requires a login, a credential, a payment surface, or a decision the build agent cannot make. Run them in the order shown — Cloudflare/Bing first because it unlocks the largest measurable SEO gains. Each runbook in `/runbooks/` covers one session end to end.

---

## Session A — Cloudflare + Bing Webmaster (35–45 min) [HIGH IMPACT]

Runbook: [`runbooks/owner-cloudflare-bing.md`](runbooks/owner-cloudflare-bing.md)

- [ ] Bing Webmaster Tools — Import from GSC for `sc-domain:acglass.com`
- [ ] Bing Webmaster Tools — Submit `https://acglass.com/sitemap-index.xml`
- [ ] Cloudflare zone `acommercialglass.com` — Add Redirect Rule → 301 to `acglass.com`
- [ ] Cloudflare zone `acglass.com` — Enable HSTS (max-age 6 months to start, no preload)
- [ ] Cloudflare zone `acglass.com` — Always Use HTTPS ON, min TLS 1.2
- [ ] Cloudflare zone `acglass.com` — Crawler Hints ON
- [ ] Cloudflare zone `acglass.com` — Cache Rule for `*.avif|*.webp|*.jpg|*.png|*.svg|*.woff2|*.ico|/css/*|/js/*|/images/*` → Edge TTL 30d / Browser 7d
- [ ] Cloudflare zone `acglass.com` — Transform Rule: X-Robots-Tag `noindex, nofollow` on `/pdfs/qualifications/*`
- [ ] Cloudflare zone `acglass.com` — Bulk Redirects: create `acglass-legacy-301s` list, import `cloudflare-bulk-redirects.csv` from repo root, attach to a Bulk Redirects rule

---

## Session B — Directories (60–90 min) [MEDIUM-HIGH IMPACT]

Runbook: [`runbooks/owner-directories.md`](runbooks/owner-directories.md)

- [ ] Blue Book — ProView free listing, Class 2230, regions FL-South + FL-N&C, canonical NAP/desc
- [ ] Downtobid — claim or create subcontractor profile, canonical NAP/desc
- [ ] Procore Construction Network — claim profile, canonical NAP/desc, logo upload
- [ ] Levelset — free subcontractor profile

---

## Session C — Review-Engine setup (30 min) [MEDIUM IMPACT]

Runbook: [`runbooks/review-engine-pipedream.md`](runbooks/review-engine-pipedream.md)

- [ ] Generate canonical GBP short link from `business.google.com → Customers → Reviews → Get more reviews`
- [ ] In ACG SEO Ops sheet, create **PM-Map** tab with columns: QBO Customer ID, PM Name, PM Email, GC Primary Name, GC Primary Email, Project Name, Project Address, GBP Short Link
- [ ] Populate PM-Map with at least 10 active customer rows
- [ ] In Pipedream, build the workflow per runbook (QBO trigger → sheet lookup → draft email → 7-day follow-up)
- [ ] Verify the workflow with a test invoice closeout
- [ ] Keep in draft-first mode for 30 days, then switch step 5 to Send Email

---

## Session D — Weekly outreach loop (recurring, 90 min/week)

Runbook: [`runbooks/outreach-cowork.md`](runbooks/outreach-cowork.md)

- [ ] Create **Outreach** tab in ACG SEO Ops sheet with the 14-column schema
- [ ] Save the weekly prompt to your personal prompt library
- [ ] Run the first cycle (3 contacts → 3 Gmail drafts → 3 sheet rows)
- [ ] Calendar block 90 min/week for the loop

---

## Pipedream / GitHub Actions secrets (≈15 min)

Required for the three automation workflows in `.github/workflows/`:

### Workflow: `pulse.yml` (nightly SEO pulse)

- [ ] `GSC_SA_JSON` — Google service-account JSON with GSC Webmasters readonly scope, granted access to `sc-domain:acglass.com`
- [ ] `BING_API_KEY` — From Bing Webmaster Tools → Settings → API access
- [ ] `SHEETS_SA_JSON` — Google service-account JSON with Sheets scope; share the SEO Ops sheet with the service account email
- [ ] `SHEETS_ID` — The spreadsheet ID from the SEO Ops sheet URL
- [ ] `SLACK_WEBHOOK` — Incoming webhook URL for the #seo Slack channel

### Workflow: `ai-visibility.yml` (monthly AI-citation audit)

- [ ] `PPLX_API_KEY` — Perplexity Sonar API key (perplexity.ai/settings/api)
- [ ] `GEMINI_API_KEY` — Google AI Studio API key (aistudio.google.com/apikey)
- [ ] `OPENAI_API_KEY` — OpenAI API key (platform.openai.com/api-keys)
- [ ] Reuses `SHEETS_SA_JSON`, `SHEETS_ID`, `SLACK_WEBHOOK` from above

### Workflow: `leadtime-ingest.yml` (monthly PR from PO export)

- [ ] No secrets required. Owner drops `data/po-export.csv` into the repo by the 9th of each month; workflow opens a PR on the 10th.

To add a secret: GitHub repo → Settings → Secrets and variables → Actions → New repository secret.

---

## Miscellaneous owner-only items

- [ ] **NOA hub — confirm Slimpact/Trulite system mapping with manufacturer rep.** The Florida Product Approval portal does not list "Slimpact" as a standalone applicant; approvals appear under parent Trulite Glass & Aluminum Solutions. Confirm with your Slimpact rep which specific Trulite FL PA / Miami-Dade NOA numbers cover the Slimpact-branded products you actually install. Update `/noa/data.json` once known.
- [ ] **NOA hub — Euro-Wall + Aldora HVHZ coverage.** Both manufacturers carry FL Product Approvals but are NOT registered applicants in the Miami-Dade Product Control HVHZ system. Confirm with each manufacturer's rep how they cover HVHZ projects in Miami-Dade and Broward. Update `/noa/data.json`'s `miami_dade_note` field for each manufacturer with the rep's answer.
- [ ] **GSC removals (separate from Bing import).** In Google Search Console for `sc-domain:acglass.com`, submit Removals for: `/category/uncategorized/`, `/new-3/`. These are legacy WordPress URLs that should not show in search.
- [ ] **Wikidata** — 8 properties remaining per `ACG-Wikidata-QuickStatements.txt` at the repo root. Paste into [quickstatements.toolforge.org](https://quickstatements.toolforge.org) (5-minute manual).
- [ ] **Microsoft Clarity** — Sign up at `clarity.microsoft.com`, paste the Clarity tracking ID into the homepage `<head>` block. Free, gives session recordings + heatmaps.
- [ ] **Manufacturer outreach (owner-only).** Reach out to ESWindows commercial rep, Euro-Wall, and PGT to confirm the "Authorized installer" pages on acglass.com link the way they want. These cannot run through the cowork outreach loop.
