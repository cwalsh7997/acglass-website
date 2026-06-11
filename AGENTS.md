# AGENTS.md — Non-negotiable rules for build agents working on acglass.com

These rules apply to every agent, every task, every commit.

## 1. Data rule

Never write an NOA number, Florida Product Approval number, design pressure, expiration date, price, lead time, or spec value from memory or inference. Every value must be read from an official source at build time (floridabuilding.org Product Approval portal, Miami-Dade Product Control) and stored with its source URL in the same table row. If you cannot confirm a value, write exactly `pending verification`. Filling a cell to look complete is the one way to fail this entire job.

## 2. Verifier is law — and untouchable

Run `python3 scripts/seo-verify.py` after every task. You may ADD checks. You may not weaken, delete, skip, comment out, or re-threshold any existing check to make it pass. If a check fails twice after your fix attempts, STOP that task, write the failure to `BLOCKERS.md`, and move to the next task.

## 3. Redirect pattern

GitHub Pages cannot 301. A redirect = stub page containing `<meta http-equiv="refresh" content="0; url=/TARGET">` + `<link rel="canonical" href="https://acglass.com/TARGET">` + `<meta name="robots" content="noindex">` + one plain fallback link. Stubs never appear in any sitemap.

## 4. Hard limits

- Titles ≤60 characters.
- Meta descriptions 80–155 characters (under 80 is also a fail — no near-empty descriptions).
- Exactly one `<h1>` per page, plain readable text with real spaces.
- Canonical on every page = `https://acglass.com/...` (no www, no http).
- `@type` on the `#org` node is exactly `["Organization","LocalBusiness"]`.

## 5. Forbidden actions

Do not log into, modify, or create accounts on: Cloudflare, Bing Webmaster Tools, Google Cloud/GSC, Gmail or any email, Google Business Profile, Pipedream, any directory (Blue Book, Downtobid, Procore, Levelset), or any payment surface. Do not send any email or message to any person. Browser use is allowed ONLY to read public pages (government portals, manufacturer sites, research). Anything requiring an owner login goes into `OWNER-ACTIONS.md` — that file is a deliverable, not a failure.

## 6. Git discipline

Work on branch `seo-sprint3` (or the current sprint branch). One task = one commit, message `seo-sprint3: <task id> <name>`. Never force-push. Never edit files outside the task's stated paths. Open one PR per phase; wait for the `seo-verify` status check before treating a phase as done.

## 7. No invented copy facts

Page copy may only state facts already present on the site, in the four project PDFs, or confirmed by a source URL. No new statistics, client names, dollar figures, or superlatives.

## Definition of "perfect"

Every acceptance check passes, `scripts/seo-verify.py` is green against the LIVE site at the end, and not one data value exists without a source. A cell marked "pending verification" is a PASS. An unsourced number is the only unforgivable failure.
