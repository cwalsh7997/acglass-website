# HANDOFF → Computer (Perplexity agent): review + deploy Claude Code's Sprints 001–004

Claude Code staged a 4-sprint **factual-integrity remediation** across stacked branches/PRs.
Your job: critically review it, then get it live. **Pull `CLAUDE.md` first — the brand rules changed.**

## What changed (and why it matters)
1. **Removed unverified manufacturer claims (liability).** The site claimed "authorized installer for PGT, Allegion, TGP, Slimpact, Aldora" in prose + JSON-LD across ~270 pages. Per the Ledger only **Euro-Wall + ESWindows/Tecnoglass** are verified → downgraded to truthful "installs / installer of." Euro-Wall + ESWindows keep "authorized."
2. **WBE/SBE certification** assertions neutralized in machine-read schema → "woman-owned (Rielly 51%)." (Prose WBE on ~1,484 pages left pending — see Q4b.)
3. **Retired AI-managed/AI-augmented/AI-first positioning** site-wide (Connor killed it 2026-06-23) + the `acglass.ai` sister-site links. 7 AI/hard-gate pages retired to noindex redirect stubs.
4. **Banned "best commercial glazing contractor" superlatives** removed.
5. **`CLAUDE.md` updated** (tagline retired, banned-positioning list added, manufacturer line corrected) so this isn't re-added.

Full detail: `CHANGELOG.md`. Open decisions: `QUEUE-FOR-CONNOR.md`.

## ⚠️ Do NOT re-introduce
AI-managed/AI-augmented/AI-first, Sub.ai, jobcost.ai, CFO Agent, acglass.ai, "authorized installer" for PGT/Allegion/TGP/Slimpact/Aldora, "WBE/SBE certified," "best commercial glazing contractor." Re-read `CLAUDE.md` §3 before any edit.

## The PR stack (each based on the prior sprint)
- #1 `sprint-001-phase-1-bleeding` → main
- #2 `sprint-002-unverified-claims` → sprint-001
- #3 `sprint-003-ai-superlative-sweep` → sprint-002
- #4 `sprint-004-ai-prose-rewrite` → sprint-003  ← **contains the entire stack (7 commits)**

## STEP 1 — Review (don't rubber-stamp)
- `git fetch origin` and confirm `main` hasn't drifted in a way that conflicts (Claude's branches were cut from `main` @ `3c0ec63`). If you pushed to main in parallel, reconcile first.
- Spot-render in a browser: `/`, `/about.html`, `/blog/`, `/commercial-glazing-nashville-tn.html`, `/pgt-installer-florida.html`, `/acg-vs-giroux-glass.html`, one city page. Check layout isn't broken and the rewritten copy reads cleanly (Claude flagged some replacements are blander — improve any that read awkwardly, but **do not re-add killed claims**).
- Validate JSON-LD on `/`, `/pgt-installer-florida.html`, `/blog/index.html` via Google Rich Results Test (Claude only checked it *parses*, not that it's eligible).
- Confirm the 7 retired pages redirect: `ai-managed-glazing-contractor.html`, `best-commercial-glazing-contractor.html`, `ai-operations-whitepaper.html`, the 2 AI blog posts, `press/acg-launches-ai-operations-site.html` → all should `noindex` + redirect to `/about.html`.
- Banned-phrase scan must be clean:
  `grep -rliE 'AI-managed|AI-augmented|AI-first|Sub\.ai|jobcost\.ai|CFO Agent|acglass\.ai|best commercial glazing contractor in|authorized installer for ESWindows, Euro-Wall, PGT' --include='*.html' . | grep -v 'Retired 2026-06-30'` → expect **0**.
- `python3 -c "import xml.dom.minidom; xml.dom.minidom.parse('sitemap.xml')"` → well-formed.

## STEP 2 — Merge to main
Simplest: merge **#4** straight to `main` (it contains all 7 commits) —
`gh pr merge 4 --merge` (after retargeting #4's base to `main` in the PR UI, or merge the branch directly).
Or merge #1→#2→#3→#4 in order (GitHub auto-retargets each as the one below merges).
**Do not force-push main. Straight merge only.**

## STEP 3 — Deploy + verify live
- Push triggers GitHub Pages (~60–90s). Then **purge Cloudflare cache** (or wait out the TTL).
- Verify on the live apex (not a cached copy): hit 3–4 of the changed URLs + 2 of the retired-page redirects with `curl -sIL`. Confirm 200s / redirects, no 5xx, nav intact.
- Re-run the banned-phrase scan against a few live pages.

## STEP 4 — Report back to Connor
- Confirm live + cache purged.
- Flag the one open item: **Q4b — is ACG formally WBE/SBE *certified* (which body), or woman-owned but not certified?** That answer unlocks the final WBE-prose sweep (~1,484 pages). It does **not** block this deploy.
