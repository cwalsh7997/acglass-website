# CHANGELOG — acglass.com web operations

Per-sprint log. Newest first. Evidence + scorecard delta + next item per the operator brief §8.

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
