# QUEUE FOR CONNOR — open decisions blocking the loop

Items requiring your input. Each has my recommended answer. Reply inline or in a session; I'll execute on the next sprint.

_Opened 2026-06-30 (Sprint 001, Phase 1 — "Stop the Bleeding"). Ordered by impact._

---

## Q1 — The two operating docs conflict. Which wins? (HIGH — coordination hazard)
There are **two** CLAUDE.md files driving this repo and they now contradict each other:

- **Operator brief** (my brief, in `~/.claude` — reflects your 2026-06-22/23 decisions): AI-managed positioning **killed**; only **Euro-Wall + ESWindows** are authorized-installer relationships; WBE/SBE **not** confirmed.
- **In-repo `/CLAUDE.md`** (last edited May 30 by "Computer", your Perplexity agent): still lists tagline **"Precision glazing. AI-managed. Delivered."**, lists **TGP/Allegion/PGT/Slimpact** as "authorized installer", and bakes **WBE + SBE** into Org schema.

The two AI agents share this repo. **If Computer pulls and re-reads the stale in-repo doc, it will re-add the AI positioning I just removed.** This sprint I updated the in-repo `/CLAUDE.md` (tagline retired, banned-positioning list added, manufacturer line corrected) to stop that — but you should confirm the in-repo doc is now subordinate to the operator brief, and ideally tell Computer the AI positioning is dead.

**Recommended:** Confirm operator brief is source of truth; I keep the in-repo `/CLAUDE.md` synced to it each sprint.

---

## Q2 — Final homepage tagline / what replaces the AI positioning? (HIGH)
I removed the AI-managed positioning from the homepage (hero, why-card #02, the "four AI agents" white-paper section, two FAQ entries) and the About section. I used **Ledger-only interim copy**:
- Why-card #02 → "Single-source Division 08" (self-perform storefront/curtain wall/impact/Euro-Wall).
- Interim tagline placeholder in the in-repo doc → "Precision glazing. Owner-run. Delivered."

I did **not** invent a permanent brand tagline (that's your call, not mine).

**Recommended:** Approve the interim copy, or give me the tagline + the positioning line you want and I'll roll it across the homepage + meta.

---

## Q3 — Disposition of the 6 other AI-premised pages + the white-paper page (HIGH)
These pages exist and are built around the now-retired AI positioning:
- `/ai-operations-whitepaper.html` (the white paper itself)
- `/ai-overview.html` (already noindex)
- `/blog/ai-project-management-commercial-glazing.html`
- `/blog/future-of-commercial-glazing.html`
- `/blog/ai-first-construction-operations-glazier-perspective.html`
- `/acg-vs-competitors.html` and `/national-commercial-glazing-contractor.html` (link to the retired pages; national page is also out-of-state/already noindex)

I did **not** touch these this sprint — deleting/rewriting whole pages is a bigger call than the directed banned-phrase strip.

**Recommended:** noindex + redirect-stub `/ai-operations-whitepaper.html` and the 3 AI blog posts to `/about.html` (same treatment as the two hard-gate pages), OR tell me to rewrite them as non-AI process/authority content. Your call per page.

---

## Q4b — WBE/SBE: are you actually certified, or woman-owned-but-not-yet-certified? (HIGH — only you know)
**This is now the main open factual question.** In Sprint 002 I removed the unverified **manufacturer** "authorized installer" claims (see Q4 below — done) and neutralized the **WBE/SBE certification** assertions in machine-read schema. But "WBE/SBE" still appears in **visible prose on ~1,484 pages**, and one press release says ACG is "certified as a WBE." I did **not** mass-edit that prose because [[acg-people-and-structure]] notes Rielly Walsh holds 51% on a WBE basis — so "woman-owned" may be literally true even if a formal **certification** isn't held yet.
**I need one answer:** Is ACG **formally WBE-certified and SBE-certified** (by which body — WBENC / state / SBA WOSB), or **majority woman-owned but not yet certified**?
- If certified → I restore the certification wording (and you send me the cert for the file).
- If not yet → I sweep "WBE/SBE certified" → "woman-owned" (truthful, Rielly 51%) across the ~1,484 pages.
**Recommended:** Tell me the status; I'll run the matching sweep.

## Q7 — Site-wide AI/superlative sweep (DONE in Sprint 003; ~33 bespoke files remain for Sprint 004)
Sprint 003 swept the templated AI positioning site-wide (~700 file-changes): AI-managed **343 → 5**, AI-augmented **351 → 0**, acglass.ai sameAs removed from 213 files, superlative self-claims **27 → 0**, and retired 4 AI pages (whitepaper + 2 blog posts + acglass.ai-launch press release) to noindex redirect stubs.
**Still open (Sprint 004 — no decision needed, just per-page rewrite work):** ~33 pages where AI was woven into narrative and needs rewriting rather than deletion — the `acg-vs-{giroux,harmon,permasteelisa}.html` comparison pages, Connor's author-bio pages, several Nashville/TN neighborhood pages, `facts.html`, `press.html`, `capabilities.html`, `how-it-works.html`, `procore-integrated-glazing-subcontractor.html`, `concepts/*`, and `security-policy.html`. ~19 still name Sub.ai/jobcost.ai/CFO Agent in prose. I'll handle these as careful per-page edits next.

## Q4 — Unverified manufacturer "authorized installer" claims (DONE in Sprint 002) + WBE/SBE schema (DONE)
Per the operator Ledger, these are **not** verified, but Computer's June schema work baked them site-wide:
- "Authorized installer" for **TGP, Allegion, PGT, Slimpact** (Org `hasOfferCatalog` / homepage Organization nodes)
- **WBE** and **SBE** credentials in Org `hasCredential[]`
- Homepage voice-search FAQ still says ACG works "with partners including ESWindows, **PGT**, and **Slimpact**" (left in place — softer "works with" wording, not an authorized-installer claim, but flag it)

This is a large remediation (regex sweep across ~1,073 pages) and touches manufacturer-relationship + certification language — **§2.6/§7 say STOP and ask you first.**

**Recommended:** Confirm which of {TGP, Allegion, PGT, Slimpact} we can legitimately call "authorized installer" (Ledger says none), and whether WBE/SBE are actually certified. Then I'll do one controlled sweep to correct the schema.

---

## Q5 — GSC URL removals + Cloudflare 410 (MED — needs your access)
Phase 1.1 acceptance wants the two retired pages removed from Google's index and ideally served as 410 Gone. I can't do either without your credentials:
- **Google Search Console:** submit URL-removal requests for `/ai-managed-glazing-contractor.html` and `/best-commercial-glazing-contractor.html`.
- **Cloudflare:** optionally serve those two as **410 Gone** (preferred long-term) instead of the meta-refresh stubs I shipped.

**Recommended:** I keep the noindex+redirect stubs (already shipped, works now); you submit the two GSC removals when convenient. 410 is optional polish.

---

## Q6 — Sister-agent write coordination (LOW, but real)
The in-repo `/CLAUDE.md` §6 says "pull before any edit." This sprint's work is on branch `sprint-001-phase-1-bleeding`, not yet merged. If Computer pushes to `main` before you merge this PR, there could be drift on `index.html` / `about.html` / `sitemap.xml` / `CLAUDE.md`. Low risk (Computer mostly touches city/blog pages), but worth a heads-up to Computer to stay off those four files until merge.
