# ACG Scope Engine v2 — README

This document covers `scope-engine.html` and the linked `send-plans.html`. Both are static, single-file HTML pages — no build step, no framework, no server.

---

## 1. What changed (vs. v1)

| Area | v1 | v2 |
|---|---|---|
| Lead capture | None — every input was discarded | Full payload (contact + scope + estimate + meta) sent to `connor@acglass.com` on submit |
| send-plans form action | `formspree.io/f/formspree-pending` (broken placeholder) | `https://formsubmit.co/connor@acglass.com` (proven endpoint) |
| Data carryover | None — user re-entered everything on send-plans | URL params carry the scope across; send-plans pre-fills + shows a banner |
| Impact / HVHZ pricing | Did nothing | Real multipliers (`location` + `requirements` config) |
| Coastal non-HVHZ + impact | Priced like inland | `wbd` flag + coastal multipliers |
| Openings bug | `openings × hard-coded 30` | `openings × per-type avg SF` (config-driven) |
| Building height | Not asked | New Step 2 — drives system + cost |
| Glass makeup | Not asked | New Step 6 (optional) — drives cost |
| False precision | 7-digit count-up | Rounded to sensible increments + confidence band |
| Pricing constants | Scattered through code | One `ACG_CONFIG` object at top of `<script>` |
| GA4 events | Single mailto event | Full funnel (`scope_started`, `scope_step_completed`, `scope_result_generated`, `scope_lead_captured`, `cta_send_plans_click`, `cta_call_click`, `form_submission_failed`) |
| Refresh behavior | Wiped progress | sessionStorage persists state |
| Print | Not styled | `@media print` styles → "Save as PDF" |
| Accessibility | divs as radios with no roles | `role="radio"` / `role="checkbox"` + keyboard handlers + aria-checked + focus rings |
| Reduced motion | Ignored | Respected on count-up + scan animation |
| Banned brands | Mentioned Kawneer, YKK, Tubelite | Removed entirely (only ESWindows, Euro-Wall, PGT, Allegion, TGP, Slimpact) |

---

## 2. The lead path (what ACG receives)

Every submit fires `POST https://formsubmit.co/ajax/connor@acglass.com` with:

**Contact**
`name · email · company · role · phone · project_name · needed_by_date · consent (TCPA)`

**Scope inputs**
`scope_project_type · scope_height · scope_size_method · scope_system_sf · scope_size_raw (JSON) · scope_location · scope_location_label · scope_hvhz · scope_requirements · scope_glass_makeup · scope_recommended_system · scope_system_name`

**Computed estimate**
`estimate_low · estimate_high · estimate_low_fmt · estimate_high_fmt · estimate_psf_low · estimate_psf_high · estimate_confidence · timeline_total_weeks`

**Meta**
`lead_id (ACG-{timestamp}-{nonce}) · timestamp_iso · page_url · referrer · utm_* (if present)`

**formsubmit fields**
`_subject ([ACG LEAD] prefix) · _template (basic) · _captcha (false) · _replyto · _autoresponse (full report sent to visitor) · _gotcha (honeypot)`

The visitor automatically gets the autoresponse email with the full report summary.

**The send-plans form** posts natively (multipart/form-data so file uploads work). After successful submit, formsubmit redirects to `/send-plans.html?submitted=1` which displays a green confirmation banner.

---

## 3. The config object — where to calibrate

All tunable values live in `ACG_CONFIG` at the top of the inline `<script>` in `scope-engine.html`. Hit **Ctrl+F** for `ACG_CONFIG` to find it.

### 3.1 Base $/SF (the most important thing to calibrate)
```js
basePsf: {
  storefront:           { low: 55,  high: 110 },
  curtainwall_stick:    { low: 90,  high: 200 },
  curtainwall_unitized: { low: 150, high: 350 },
  ...
}
```
**TODO**: pull your last 20–30 actual bids per system. Compute installed $/system SF (framing + glass area, not vision-glass only). Update the `low` and `high` per system. This is the #1 driver of accuracy.

### 3.2 Location multipliers
```js
location: {
  hvhz_se:    { mult: { low: 1.10, high: 1.25 }, hvhz: true,  wbd: true,  ... },
  hvhz_keys:  { mult: { low: 1.18, high: 1.30 }, ... },
  palm_beach: { mult: { low: 1.05, high: 1.12 }, ... },
  ...
}
```
The `hvhz` and `wbd` flags drive code framing in the results page AND affect glass makeup auto-selection. If you observe larger HVHZ premiums in your real bids, raise these.

### 3.3 Requirement multipliers
```js
requirements: {
  impact:  { mult: { low: 1.15, high: 1.35 }, ... },
  energy:  { mult: { low: 1.05, high: 1.12 }, ... },
  sound:   { mult: { low: 1.08, high: 1.18 }, ... },
  fire:    { mult: { low: 1.40, high: 1.60 }, ... },
  blast:   { mult: { low: 1.25, high: 1.40 }, ... },
  bird:    { mult: { low: 1.05, high: 1.10 }, ... },
}
```
Note on **double-counting**: if `location.hvhz === true`, the `impact` requirement multiplier is skipped because the location base already prices for impact. If your HVHZ base assumes impact but a non-HVHZ + impact scope arrives, the multiplier applies.

### 3.4 Building height
```js
height: {
  low_rise:  { mult: { low: 1.00, high: 1.00 }, ... },
  mid_rise:  { mult: { low: 1.10, high: 1.20 }, ... },
  high_rise: { mult: { low: 1.25, high: 1.60 }, ... },
}
```
Height drives both the cost factor and the system recommendation (in `recommendSystem()`).

### 3.5 Project-type overhead
```js
projectMult: {
  healthcare: { low: 1.10, high: 1.15 },
  government: { low: 1.10, high: 1.15 },
}
```
Only applied to healthcare + government scopes. Note prevailing wage on public work.

### 3.6 Scale
```js
scale: {
  small_threshold: 1500,  small_mult: { low: 1.10, high: 1.25 },
  large_threshold: 30000, large_mult: { low: 0.92, high: 0.97 },
}
```
Small jobs (<1,500 SF) get a mobilization premium. Very large jobs (>30,000 SF) get a small economy-of-scale discount.

### 3.7 Glass makeup tier
```js
glassMakeup: {
  standard:         { mult: { low: 0.95, high: 1.00 }, ... },
  laminated_impact: { mult: { low: 1.00, high: 1.00 }, ... },  // assumed baseline for FL exterior
  high_performance: { mult: { low: 1.10, high: 1.25 }, ... },
}
```
`auto` tier: engine picks `laminated_impact` for FL exterior with HVHZ or WBD, `standard` otherwise.

### 3.8 Glass-to-floor ratios (for `building_sf` size method)
```js
glassToFloor: {
  storefront: 0.30, office: 0.35, multifamily: 0.18,
  hospitality: 0.28, healthcare: 0.22, government: 0.22,
  interior: 0.40, industrial: 0.10,
}
```
Used when the user enters gross building SF instead of glass SF. Computed system SF = gross × ratio.

### 3.9 Avg SF per opening (fixes the v1 bug)
```js
avgSfPerOpening: {
  storefront: 60, office: 40, multifamily: 35,
  hospitality: 55, healthcare: 38, government: 42,
  interior: 45, industrial: 55,
}
```
Used when the user enters opening count instead of SF. Computed system SF = openings × avg.

### 3.10 System metadata (manufacturers, U-value, etc.)
```js
systems: {
  storefront: { name: ..., manufacturers: 'ESWindows ES-9500 / ES-8000 series, ...', uvalue: ..., ... },
  ...
}
```
Shown on the results page. Edit this to control what's displayed for "Recommended system."

---

## 4. Backend swap (when ready)

The form endpoint is set in one place:

```js
const ACG_CONFIG = {
  endpoint: 'https://formsubmit.co/ajax/connor@acglass.com',
  ...
}
```

To switch to **Formspree**:
1. Create the form on formspree.io, get the form ID
2. Change `endpoint` to `'https://formspree.io/f/YOUR_FORM_ID'`
3. Remove the `_template` and `_captcha` fields from `buildLeadPayload()` (formspree ignores them)
4. Update the analogous `<form action="...">` in `send-plans.html`

To switch to a **serverless function** (Cloudflare Worker, Netlify Function, Vercel Function):
1. Stand up your function URL
2. Change `endpoint` to your function's URL
3. Confirm your function accepts `multipart/form-data`
4. Have the function send the visitor an autoresponse (Resend/SendGrid/Postmark) and notify connor@acglass.com

The shape of the payload is the same regardless of backend.

---

## 5. Branded PDF report

The visitor's autoresponse email summarizes the report in plain text. To download a branded PDF, the visitor uses **"Save this report as PDF"** button which calls `window.print()`. The page's `@media print` CSS:
- Hides nav, footer, wizard, refinement chips, capture form, CTAs
- Shows the print-only header with ACG branding + generated date
- Forces light-on-dark to dark-on-light for legibility on white paper
- Avoids page-break-inside on result sections

For a true server-generated PDF (different layout, controlled by us not the browser), add a Cloudflare Worker that takes the lead payload + renders a PDF via Puppeteer-in-Worker or via a third-party PDF service (DocRaptor, PDFShift, etc.) and emails it. This was deferred in v2 — see Section 4 in the rebuild prompt.

---

## 6. GA4 funnel events

| Event | Fires when | Params |
|---|---|---|
| `scope_started` | First visit to /scope-engine.html in session | `source_page` |
| `scope_step_completed` | User leaves a step (continues forward) | `step` (the step number they just left) |
| `scope_result_generated` | Engine renders the result | `project_type, height, location, system, system_sf, estimate_low, estimate_high` |
| `scope_lead_captured` | Lead form POST returns 200 OK | `project_type, height, location, system, system_sf, estimate_low, estimate_high, currency, value` |
| `generate_lead` | Lead form POST returns 200 OK (matches site-wide pattern) | `form_id, source_page, currency, value` |
| `form_submission_failed` | Lead form POST returns non-200 | `form_id, http_status` (or `error_type: 'network'`) |
| `cta_send_plans_click` | "Send us your plans" link clicked from results | `source: 'scope-engine'` |
| `cta_call_click` | "Call Connor" link clicked from results | `source: 'scope-engine'` |
| `scope_pdf_print` | "Save this report as PDF" button clicked | (none) |
| `bid_form_start` | First field focused on send-plans | (none) |
| `bid_form_submit` | send-plans form submit triggered | `project_type, bid_type, source_page` |
| `bid_form_confirmed` | User lands on `?submitted=1` | (none) |

**Important**: `generate_lead` only fires on confirmed `response.ok === true` — fixed in v2 (v1 fired on click before fetch, which caused phantom conversions). Same pattern as the site-wide contact form fix from June 3.

---

## 7. Accessibility

- All wizard cards use `role="radio"` (single-select) or `role="checkbox"` (multi-select) with proper `aria-checked` state and visible focus rings
- Keyboard: Tab to focus, Enter or Space to toggle, arrow keys not yet wired (TODO: full ARIA radiogroup keyboard pattern)
- `aria-live="polite"` on validation messages, analyzing region, and form status
- `prefers-reduced-motion` respected on count-up + scan animations
- Color contrast: red `#E11320` on dark `#0C1525` exceeds WCAG AA (4.5:1)
- Form labels properly associated via `for=`
- Tap targets ≥ 44px on mobile (validated in CSS by padding values)

---

## 8. Things to do next (deferred from rebuild prompt)

- **Real PDF generation** via Cloudflare Worker (Section 4 in the rebuild prompt). Current v2 uses browser-print.
- **Full keyboard ARIA radiogroup pattern** (arrow keys). Currently Tab + Enter/Space works.
- **CRM / Zapier webhook** as a second receiver alongside formsubmit. Easy to add: after `response.ok`, send a second POST to the webhook URL.
- **A/B test the value-first vs gated flow** via the `SHOW_FULL_BEFORE_CAPTURE` toggle (currently always value-first — results show before form).
- **Calibrate `basePsf` against ACG's last 20–30 actual bids.** This is the single highest-leverage accuracy improvement.

---

## 9. Files in this rebuild

| Path | Role |
|---|---|
| `scope-engine.html` | The estimator + lead capture |
| `send-plans.html` | The plans-submission form (fixed backend + scope-engine carryover) |
| `SCOPE-ENGINE-README.md` | This file |

Both HTML files are self-contained. No new dependencies, no build, no CI changes.

— Connor / Computer · June 4, 2026
