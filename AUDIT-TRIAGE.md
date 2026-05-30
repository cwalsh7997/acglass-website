# Audit-branch triage — `origin/audit/dedupe-og-tags`

**Author:** Claude Code (Opus 4.7, 1M context)
**Reviewed against:** `origin/main` @ `fdd9dc0d`
**Audit branch tip:** `04058482`
**Lag:** audit branch is 33 commits ahead of, **117 commits behind** main. A flat merge is dead.

This document classifies every commit on the audit branch into one of three
buckets: **SHIP** (clean cherry-pick), **MOOT** (already done on main, or
docs-only), or **REWORK** (still valuable but underlying files have drifted —
needs fresh extraction against current main).

**No cherry-picks performed.** Computer + Connor decide which SHIP commits
land on main; REWORK gets re-implemented if/when prioritized.

---

## TL;DR

| Bucket | Count | What it means |
|---|---|---|
| **SHIP** | 4 | Pure data fixes, safe verbatim cherry-pick |
| **MOOT** | 11 | Already addressed on main, or docs-only artifacts |
| **REWORK** | 18 | Real bugs/wins still on main, but file drift means re-extraction needed |

State verified on main: og:title/og:type still duplicated on 83 city pages (Miami sample shows 2 each); `Florida\'s` literal-backslash escape still in 297+ instances; humans.txt still says 2020; 9 out-of-state pages have zero noindex meta; `index.html` still pulls fonts.googleapis.com; only 19 imgs on `index.html` declare width/height; footer of `index.html` has zero privacy-policy link; Miami's city-pill list still has 75 inline onmouseover handlers. Conversely: forms (May 25 rewrite to formsubmit.co fetch), GTM-XXXXXXX removal, GA4 on best-commercial-glazing, partners.html in sitemap, 5-GC-page WebP sources, location-template-snippet noindex, and ifly broken-source removal are all **already on main**.

---

## SHIP (4)

| SHA | What it did | Why it's SHIP |
|---|---|---|
| `4ab2221d` | Dedupe duplicate `<meta property="og:*">` tags on 83 city/service pages (300+ tags removed) | Miami sample on main still has 2 og:title + 2 og:type. Bug persists across the 83 affected pages. Awk keeps the last occurrence per property — data-driven, not line-position-dependent. Clean cherry-pick. |
| `bc44120e` | Replace literal `\'` with `'` in `Florida\'s` (og:image:alt + body) across 301 pages | 297 instances still present on main. Pure literal-string substitution using hex escapes (`\x5c\x27` → `\x27`), safe. |
| `1b4365a8` | humans.txt: `Established: 2020` → `Established: 2021` | main still says 2020; schema + llms.txt + Sunbiz corp record (P21000018259) all say 2021. Single-line, single-file fix. |
| `cdc950c2` | Add `Service` schema JSON-LD to 6 product/system pages | Re-fingerprinted: 3 of 6 already have it on main (commercial-storefront-systems, window-wall-systems, fire-rated-glass-systems). **Cherry-pick only the 3 still-missing**: curtainwall-systems.html, impact-windows-doors.html, multi-slide-bifold-doors.html. Direct cherry-pick of `cdc950c2` would create cosmetic duplicates on the 3 already-done pages. |

---

## MOOT (11)

| SHA | What it did | Why it's MOOT |
|---|---|---|
| `d3dd2fef` | Add canonical to `press-release-tampa.html` | Main now has it. |
| `2793ec60` | mailto fallback for `contact.html` + `send-plans.html` forms | Contact form rewritten May 25 to fetch-POST `formsubmit.co/ajax/connor@acglass.com` (CLAUDE.md §4) — strictly superior to the mailto fallback. Send-plans already uses mailto. **CAVEAT:** this commit also contains noindex-out-of-state + theme-color + font-preload bits that are NOT moot — see REWORK notes; don't pull this commit verbatim. |
| `99a23d55` | Add `<source type="image/webp">` to 5 GC partner-page picture blocks | All 5 (curran-young, hooks, made-in-rio, proctor, rycon) already have webp source on main. |
| `503f063f` | Remove broken `<source>` referencing non-existent `ifly-miami-exterior.webp` | Already removed on main. |
| `a63e35d3` | Add `noindex,nofollow` to `location-template-snippet.html` | Already noindex'd on main. |
| `3d8aa6e8` | Add missing GA4 snippet to `best-commercial-glazing-contractor.html` | Already has GA4 (`G-M7BFQD2SPP`) on main. |
| `04058482` | Remove broken `GTM-XXXXXXX` placeholder from tampa + west-palm-beach city pages | Already removed on main. |
| `f432e93c` | docs: add HANDOFF.md (initial 12-commit summary) | Obsolete artifact of abandoned branch. Recommend deleting both HANDOFF.md and PLAN.md from main as part of triage cleanup. |
| `9184c726` | docs: note known minor issues in HANDOFF | Same — obsolete docs. |
| `d3f77f0b` | docs: refresh HANDOFF with all 18 commits + perf savings numbers | Same. |
| `60cac1cd` | docs: refresh HANDOFF with full commit list + class reference (29 commits) | Same. Superseded by this AUDIT-TRIAGE.md. |

---

## REWORK (18)

All address real, still-present bugs or wins, but files have drifted across 117 commits. Verbatim cherry-pick will either conflict or apply against an outdated structure. Each needs fresh extraction against current main.

| SHA | What it did | Why REWORK (not SHIP, not MOOT) |
|---|---|---|
| `2b692128` | Self-host Inter, JetBrains Mono, Playfair Display (replaces 3 Google Fonts requests/page with 8 self-hosted woff2 files using `unicode-range` subsetting) | Main still references `fonts.googleapis.com` on `index.html`. High-value perf win still on the table. But: (a) needs re-strip of Google Fonts links across the now-1929-file set, (b) fresh `@font-face` block against current `css/style.css`, (c) cache-buster bump, (d) any new pages added since May may use different font weights/styles needing re-subsetting. |
| `a7a04e12` | Repair 437 broken internal links + add `noindex,follow` to 9 out-of-state pages + prune those 9 from sitemap | On current main: **0 of 9 out-of-state pages have noindex meta**; sitemap still lists them; broken-link count needs full re-audit (293 files purged May 26 may have removed some broken refs and introduced others). Cherry-picking this verbatim would conflict on dozens of files; safer to re-run the directory-aware crawl on current main to get a fresh broken-link list, then noindex + sitemap-prune as a clean micro-commit. |
| `6d924612` | Repoint final 35 still-broken anchors to `/locations.html` or `/blog.html` band-aids | After `a7a04e12` rework is done on current main, this might not even be needed — re-audit first. |
| `7d18e384` | Dedupe duplicate `<meta name="robots">` in `404.html` + add `partners.html` to sitemap | `partners.html` already in main's sitemap (MOOT half). 404.html still has 2 robots metas on main (SHIP half). Rework as a 1-file 1-line commit just for the 404 dedupe. |
| `ad7f2768` | Add `width`+`height` to ~1024 `<img>` tags (CLS fix) + repair 13 broken image refs | On current main: only 19 `<img>` tags on `index.html` declare width. Big CLS win still available. Needs: re-run dimension-map build (`file <img>` against current `images/` tree, which has changed), then re-run multi-line aware injector against current 1929 HTML files. Broken-image-ref list needs fresh audit too. |
| `82769a27` | Add `decoding="async"` to 784 imgs that lacked it | Main is probably still ~50% coverage. Re-run injector against current files. |
| `888e636e` | Add `loading="lazy"` to 425 below-fold imgs (skipping `fetchpriority="high"` LCPs) | Same situation — re-run injector. |
| `4a3c4de6` | Inject Privacy + Terms links into single-line footer-bottom (135 pages) | Main `index.html` footer has 0 references to privacy-policy.html. Real bug — orphan legal pages. Footer markup may have drifted in 117 commits; re-extract the literal pattern from current main before mass injection. |
| `b15a3cc4` | Same as above for multi-line footer-bottom (304 pages) | Same — re-extract pattern. |
| `ebfd8d81` | Extract repeated `.city-pill` inline style + onmouseover (~5,329 instances on 95 location pages) into one CSS class | Miami sample still has 75 instances on main. Big payload-reduction win. Computer must verify the literal byte pattern is still identical on current main pages before mass-running the awk substitution. |
| `3b6ec923` | Extract 2 more inline-style anchor patterns (`see-also-link`, `service-pill`, `blog-card-link`) | Pattern-dependent — same verification needed. |
| `f3c72b51` | Extract bullet-row pattern (red dot + flex container, ~700 instances) into `.bullet-row` + `.bullet-dot` | Pattern-dependent. |
| `5bca45b6` | Extract FAQ accordion `<details>`/`<summary>` styles into `.faq-item` / `.faq-question` / `.faq-marker` / `.faq-answer` + add `details[open] .faq-marker { transform: rotate(45deg) }` for visual close-state | Pattern-dependent. UX bonus of marker rotation is independent of HTML drift. |
| `02507e88` | Define missing CSS vars `--font-mono` (alias for `--mono`) + `--text-muted` (alias for `--white-50`) + extract byline/eyebrow inline styles | **CSS var declaration is a real-bug SHIP-able micro-commit** — ~1500 inline `style="font-family:var(--font-mono);...color:var(--text-muted);..."` instances on the site silently fall back to defaults because the vars are undefined. Worth splitting out. Class extraction part is REWORK. |
| `2c898c20` | Extract 5 more class patterns (`feature-label`, `feature-value`, `content-card`, `accent-link`, `body-sm`) | Pattern-dependent. |
| `9aa0a582` | Extract 7 more class patterns (`label-sm`, `label-tag`, `section-h2`, `link-card`, `body-sm-tight`, `card-title`, `card-meta`) | Pattern-dependent. |
| `31a53ea9` | Extract 3 share-button classes (generic / LinkedIn / Facebook) — 447 instances | Pattern-dependent. |
| `3a023865` | Extract 6 more class patterns (`label-tag-mb`, `share-row`, `divider-faint`, `heading-md`, `bullet-dot-md`, `share-row-bare`) | Pattern-dependent. |

---

## Important context for Computer

1. **`2793ec60` is split-class** (MOOT bucket above with caveat): the commit's headline change (mailto fallback for forms) is MOOT, but it ALSO contains:
   - `noindex,follow` on 9 out-of-state pages — still SHIP-able (and folded into the `a7a04e12` rework)
   - `theme-color` meta on every page — still SHIP-able **BUT WITH `#0e284f` NOT `#0D1E36`** (audit branch used wrong color; CLAUDE.md §3 brand standards say primary navy is `#0e284f`)
   - Font preload hint — depends on whether font self-host (`2b692128`) is REWORK'd first
   - Cache-buster bump on `?v=` query string for blog pages — pre-purge era, may not apply cleanly
   
   Don't cherry-pick `2793ec60` verbatim. If implementing its still-relevant bits, do so as fresh micro-commits.

2. **`02507e88` is split-class**: the CSS var alias definition (`--font-mono: var(--mono); --text-muted: var(--white-50);` in `:root`) is a small, safe, real-bug SHIP-able micro-commit. The class extraction (.byline-meta, .eyebrow-tag) is pattern-dependent REWORK.

3. **Theme-color color is wrong on audit branch.** Any commit/rework that introduces `<meta name="theme-color">` MUST use `#0e284f` per CLAUDE.md §3, NOT `#0D1E36` from the audit branch.

4. **Banned terms check passes on audit-branch commits.** Spot-checked commit messages and diffs against CLAUDE.md §3 banned-words list — no `leverage`/`world-class`/`cutting-edge`/etc. in audit-branch changes. Kawneer/YKK/Tubelite not reintroduced.

5. **`HANDOFF.md` and `PLAN.md` on the audit branch are obsolete.** Recommend deleting both as part of post-triage cleanup (they'd be confusing artifacts if anyone discovered them via search).

6. **Pattern-extraction REWORK assumes byte-identical inline-style strings on current main.** Cheap sanity-check before re-running any awk extraction: `git show origin/main:commercial-glazing-miami.html | grep -c "<exact pattern from audit branch>"` on 3-5 sample files. If counts match expected, safe to mass-run.

---

## Recommended cherry-pick order (when Computer + Connor decide to ship)

**Phase 1 — pure SHIP-bucket (zero-risk, 10 minutes of cherry-pick + push):**

1. `4ab2221d` — og:* dedupe across 83 pages
2. `bc44120e` — `Florida\'s` literal-backslash fix on 297 instances
3. `1b4365a8` — humans.txt year
4. Hand-craft a fresh micro-commit: Service schema on the 3 still-missing pages (NOT cherry-pick `cdc950c2`)

**Phase 2 — small carve-outs from REWORK-bucket (~20-30 min):**

5. Hand-craft: define `--font-mono` + `--text-muted` aliases in `:root` of `css/style.css` (from `02507e88`)
6. Hand-craft: noindex 9 out-of-state pages + prune from sitemap (from `a7a04e12` and `2793ec60`)
7. Hand-craft: theme-color meta on every page with correct `#0e284f`
8. Hand-craft: dedupe 2nd robots meta in `404.html` (from `7d18e384`)

**Phase 3 — big REWORK (estimate, by descending value-per-effort):**

9. Self-host fonts (`2b692128`) — biggest perf win, ~30 min rework
10. Image dimensions for CLS (`ad7f2768`) — Core Web Vitals signal, ~30 min
11. Privacy + Terms in footer (`4a3c4de6` + `b15a3cc4`) — legal, ~20 min
12. `loading="lazy"` + `decoding="async"` (`82769a27` + `888e636e`) — ~15 min
13. City-pill extraction (`ebfd8d81`) — ~1.5MB payload cut, ~30 min
14. Other inline-style extractions (`3b6ec923`, `f3c72b51`, `5bca45b6`, `02507e88` extraction part, `2c898c20`, `9aa0a582`, `31a53ea9`, `3a023865`) — ~1-2 hours total
15. Broken-link re-audit + repair (`a7a04e12` + `6d924612` link parts) — fresh crawl first, then targeted fixes

**Phase 4 — cleanup:**

16. Delete `HANDOFF.md` and `PLAN.md` from any branch they appear on.
17. Delete the audit branch from origin once triage is complete and ship-able fixes are landed.

---

## Footnote: side observation on 58b0e4a7 (dealer Phase 1) for Computer

You asked whether 58b0e4a7 was tested. I did NOT browser-test, but a static read shows:
- `become-a-dealer.html` has proper title, canonical (self-pointing), meta description, GA4, og tags
- `dealer/admin.html` is correctly `noindex,nofollow` and lacks GA4 (correct for an admin tool)
- `dealer/dealer.js` form-submit logic uses the same `formsubmit.co/ajax/connor@acglass.com` endpoint as the rest of the site (consistent with CLAUDE.md §4)
- `dealer.js` honeypot field is named `_honey` ✓
- One observation: `dealer/admin.html` doesn't have `<meta name="description">` — fine for an admin page that's noindex'd, but worth flagging if the noindex is ever lifted.

No blockers spotted, but recommend a quick browser smoke-test of the application form submission against your test inbox before relying on production volume.
