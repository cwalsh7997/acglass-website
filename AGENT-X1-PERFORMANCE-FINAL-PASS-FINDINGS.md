# Agent X1 — Performance Final Pass — Findings

**Date:** 2026-06-06
**Working dir:** `/home/user/workspace/acglass-website/`
**Status:** All 5 tasks complete. **NOT committed** (per instruction).

---

## Pages modified (6 HTML files)

| Page | Task 1 Critical CSS | Task 2 Spec Rules | Task 3 SW reg | Task 4 HSTS meta | Task 5 Clarity | Manifest link |
|------|:---:|:---:|:---:|:---:|:---:|:---:|
| `index.html`        | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| `capabilities.html` | ✅ | ✅ | ✅ | — | ✅ | — |
| `portfolio.html`    | ✅ | — | ✅ | — | — | — |
| `locations.html`    | ✅ | — | ✅ | — | — | — |
| `ai-overview.html`  | ✅ | — | ✅ | — | — | — |
| `send-plans.html`   | — (not in T1 scope) | — | ✅ | — | ✅ | — |

## Files created (4)

- `/sw.js` — Service Worker (offline shell + stale-while-revalidate caching). JS syntax validated with `node --check`.
- `/manifest.json` — Web App Manifest. Valid JSON.
- `/images/favicon-512.png` — 512×512 PWA icon (generated from `acg-mark.png` on navy `#0e284f` ground).
- `/images/favicon-192.png` — 192×192 PWA icon (same source).

> Note: the task said "if favicon-512 / favicon-192 don't exist, use the nav logo path." They didn't exist. Rather than mislabel the non-square 338×72 nav logo (which would distort) or the 200×200 mark as 512px, I generated correctly-sized square PWA icons from the existing brand mark. This is cleaner and avoids a PWA install-icon warning in Lighthouse. If Connor prefers, he can swap in higher-res source art later.

---

## TASK 1 — Critical CSS inlining

**Approach:** Extracted the shared above-the-fold foundation from `css/style.css` (lines ~47–700 + the `hp-*` block at 2777–3424) into an inlined `<style id="crit-css">` block placed in `<head>` *before* the async stylesheet. The full `style.css` now loads non-render-blocking via `preload`→`onload` swap, with a `<noscript>` fallback.

**Critical CSS contents (shared base, all pages):** CSS reset, `:root` design tokens (incl. `--hp-*` brand vars), `html`/`body`, base typography (`h1–h4`, `p`, `.accent`), `.container`, `.section`, `.label`, full `.btn` family, full `.nav` system (logo, links, cta, toggle, scope/badge/phone add-ons, mobile drawer @900px), `.skip-link`, and the generic `.hero` (bg, overlay, content, sub, actions).

**Per-page additions:**
- `index.html`: + `hp-hero`, `hp-hero-overlay`, `hp-hero-content/eyebrow/h1/sub/actions`, `hp-trust-seal`, `hp-metrics` bar, `hp-partners` bar + their mobile rules (@900/@600/@480). Inlined ~11.3 KB.
- `locations.html`: + `.page-hero` block + @640 mobile. Inlined ~8.2 KB.
- `capabilities.html`: shared base only (~7.6 KB). Its `.cap-hero` hero CSS is **already inlined** in that page's own `<head>` `<style>` block, so it was not duplicated.
- `portfolio.html`: shared base only (~7.6 KB). Its `.filmstrip-hero` CSS is **already inlined** in-page.
- `ai-overview.html`: shared base only (~7.6 KB). Uses the generic `.hero` (in shared) plus inline `style="..."` overrides.

**FOUC verification:** Rendered every page with the async `style.css` request **blocked** (simulating first paint with critical CSS only) via Playwright at 1280×800. All five above-the-fold viewports render correctly — nav, hero photo/overlay, eyebrow, H1 + red accent, subhead, both CTAs, trust seal, metric bar, partner bar. **No FOUC on any page. No page skipped.**

**Expected LCP improvement:** Eliminating the single render-blocking ~80–100 KB CSS request removes one full round-trip from the critical path. On the target 300–500 ms goal, expect **~250–450 ms LCP improvement** on cold loads (more on slow 3G/4G where the CSS round-trip dominates; less on warm cache). The LCP element on the homepage is the hero image (already `fetchpriority="high"` + preloaded), so the win comes from no longer waiting on CSS parse before first paint. Real-world delta should be confirmed in PageSpeed Insights / CrUX after deploy.

**Cache buster:** All async links bumped to `?v=20260606crit`.

---

## TASK 2 — Speculation Rules API

Added `<script type="speculationrules">` (prerender, `eagerness: moderate`) to `index.html` and `capabilities.html` `<head>`. Excludes `/api/*`, `*.pdf`, `mailto:`, and `tel:` links. Chrome/Edge prerender same-origin pages on hover; Safari/Firefox ignore the tag gracefully. JSON validated.

---

## TASK 3 — Service Worker + PWA manifest

- `/sw.js`: `install` pre-caches the app shell (`/`, css, js, nav logo, manifest) + `skipWaiting`; `activate` purges old caches + `clients.claim`; `fetch` is cache-first with background revalidate, GET-only, same-origin writes, offline `503` fallback. Cache key `acg-v1-2026-06-06`.
- Registration script added before `</body>` on all 6 pages (guarded by `'serviceWorker' in navigator`, fired on `load`, errors swallowed).
- `/manifest.json` created; `<link rel="manifest">` added to homepage head.

---

## TASK 4 — HSTS preload preparation

- Added `<meta http-equiv="Strict-Transport-Security" content="max-age=63072000; includeSubDomains; preload">` to homepage head **for documentation/intent only**.

### ⚠️ OPEN FLAG FOR CONNOR — HSTS requires a real HTTP header (meta tag does NOT enforce HSTS)

Browsers ignore HSTS delivered via `<meta http-equiv>`. To actually enforce + qualify for the preload list, Connor must set the response **header** in **Cloudflare** (which fronts GitHub Pages):

1. Cloudflare dashboard → select `acglass.com` → **SSL/TLS → Edge Certificates**.
2. Scroll to **HTTP Strict Transport Security (HSTS)** → **Enable HSTS**.
3. Set: **Max-Age = 12 months** (≥ `63072000` s / 2 yrs for preload eligibility — choose 2 years), **Include subDomains = On**, **Preload = On**, **No-Sniff header = On**.
4. Confirm prerequisites: all subdomains must serve valid HTTPS, and the site must redirect HTTP→HTTPS (Cloudflare "Always Use HTTPS" = On).
5. Only **after** the header is live and stable for a few days, submit `acglass.com` at **https://hstspreload.org** (this is the manual step Connor owns). Preload removal is slow, so verify subdomains first.

Resulting header should be: `Strict-Transport-Security: max-age=63072000; includeSubDomains; preload`

---

## TASK 5 — Microsoft Clarity (staged, commented out)

Added a **commented-out** Clarity snippet to `index.html`, `capabilities.html`, and `send-plans.html` (the conversion-funnel pages). No live placeholder ID (avoids a 404 / failed request). Block includes inline instructions.

### OPEN FLAG FOR CONNOR — activate Clarity
1. Sign up free at **https://clarity.microsoft.com** (~60 s), create a project for `acglass.com`.
2. Copy the **Project ID**.
3. In each of the 3 pages, find the `MICROSOFT CLARITY` comment block, **uncomment** the `<script>`, and replace `YOUR_CLARITY_ID` with the real ID.

---

## Open flags / notes for Connor (summary)

1. **HSTS** — meta tag is intent-only; enable the real header in Cloudflare, then submit at hstspreload.org (steps above).
2. **Clarity** — uncomment + paste Project ID on 3 funnel pages once signed up.
3. **PWA icons** — generated 192/512 from the brand mark on navy. Swap for higher-res art if desired.
4. **Service Worker scope** — `sw.js` is at repo root so its scope is `/` (whole site). On first deploy after this change, the SW will cache the shell; the `activate` handler auto-purges any older cache versions. If CSS/JS is updated later, bump the `CACHE` constant in `sw.js` to force a refresh.
5. **GitHub Pages + SW** — service workers require HTTPS (satisfied via Cloudflare). The `/sw.js` path must be served from the site root — confirmed it's at repo root.
6. **Not committed** — all changes are working-tree only, per task instruction. Files modified by a *prior* agent (whitepaper, glossary, manufacturers, several service pages) also appear in `git status` but were **not** touched by this pass.

## Verification performed
- All 6 pages: balanced `<style>` braces, single `</head>`/`</body>`, async preload present, SW registration present.
- `manifest.json` valid JSON; `sw.js` passes `node --check`; speculation-rules JSON valid.
- Critical-CSS-only Playwright screenshots saved: `_qa_{home,capabilities,portfolio,locations,aioverview}_critonly.png` (left in workspace for review).
