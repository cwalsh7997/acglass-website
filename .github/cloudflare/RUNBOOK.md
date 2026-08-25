# Cloudflare redirect deployment runbook - money-market canonicalization

**Status: NOT ACTIVATED.** Nothing in this directory has been applied. Merging the
pull request that adds it changes no routing. Applying it is a manual act in the
Cloudflare dashboard, performed by someone with zone access, following the steps
below.

## Why this is not a code change

`acglass.com` is served by GitHub Pages behind Cloudflare.

- GitHub Pages serves the repository tree. It does not read `vercel.json`, so
  editing `vercel.json` deploys nothing. The superseded plan on branch
  `fix/canonical-cannibalization-money-markets` rewrote `vercel.json` from 69 to
  80 rules; that change would have shipped **zero** redirects.
- Every 301 observed on the live site executes at the Cloudflare edge, which is
  configured outside this repository.
- `.github/` is not served by Pages (verified: `acglass.com/.github/workflows/pulse.yml`
  returns 404 while `/.gitignore` returns 200), so this runbook and its manifest
  are not public. They live here rather than in `_internal/` for the same reason
  the CI scripts do - `_internal/` is git-ignored, so Actions cannot read it and
  nothing there can be reviewed in a pull request.

`vercel.json` is therefore best understood as an **observed mirror** of the edge
configuration. On 2026-07-29 all 69 rules in it were HEAD-probed against the live
site with redirect-following disabled: 69/69 matched exactly, there were no live
301s absent from the file, and `server: cloudflare` was returned on every
response. The mirror is currently accurate. Keep it that way (step 8).

## What is being changed and why

Two rules. Both fix the same defect.

A visitor or crawler requesting a broad commercial-glazing URL currently lands on
a storefront page:

```
/commercial-glazing-miami.html
  --301 (Cloudflare)-->  /miami/                              <- title: "Storefront Glazier in Miami, FL - Service Area"
  --rel=canonical-->     /storefront-glazier-miami-florida/   <- storefront primary
```

That is two hops, and it ends on the primary for a *different* head intent.
"Commercial glazing contractor {city}" and "storefront {city}" are separate
intents with separate primaries; a `storefront-glazier-*` page must never be the
primary for the broad intent.

Note carefully what is **not** wrong here. `/miami/` is titled, H1'd and
meta-described as storefront copy, so its `rel=canonical` to
`/storefront-glazier-miami-florida/` is *correct*. Repointing that canonical
would be the wrong fix and would make the mismatch worse. The defect is the
redirect destination, and the redirect lives at the edge. This is why the work
splits into an in-repo part and this part.

| # | Source | From | To |
|---|---|---|---|
| 1 | `/commercial-glazing-miami.html` | `/miami/` | `/miami-hvhz-glazing-contractor.html` |
| 2 | `/commercial-glazing-tampa.html` | `/tampa/` | `/tampa-commercial-glazing.html` |

Both destinations already exist on disk, are self-canonical, and are named as the
market's commercial-glazing primary by both
`acglass_topical_authority_research_20260728.md` §4.3 and
`.github/seo/seo-targets.json`. Neither destination is a URL that is known to
rank, so neither rule moves a ranking URL - the sources are 301s today and are
already not indexable.

Five further cities carry the identical two-hop and are **deliberately excluded**.
West Palm Beach is frozen; Orlando, Naples, Fort Lauderdale and Boca Raton have
no commercial-glazing hub to redirect *to*, and inventing one by pointing them at
their `storefront-glazier-*` page is the exact error being reversed. See
`deliberately_not_requested` in `redirects.manifest.json` for the full list with
reasons, including roughly 27 non-money-market cities in the same state.

## Preconditions

1. The in-repo half of this work is merged to `main` and deployed. Check that
   `https://acglass.com/nashville/` returns a `rel=canonical` of
   `https://acglass.com/commercial-glazing-nashville-tn.html`.
2. Both destinations return HTTP 200:
   ```
   curl -sI https://acglass.com/miami-hvhz-glazing-contractor.html | head -1
   curl -sI https://acglass.com/tampa-commercial-glazing.html      | head -1
   ```
3. The mirror is still accurate. This must pass **before** you touch anything:
   ```
   python3 .github/scripts/canonical-verify.py --live
   ```
   If it reports divergence, stop. Someone has changed the edge outside this
   process and the analysis above may be stale.
4. Capture the current state of both rules for rollback:
   ```
   curl -sI https://acglass.com/commercial-glazing-miami.html | grep -i '^location'
   curl -sI https://acglass.com/commercial-glazing-tampa.html | grep -i '^location'
   ```
   Expect `/miami/` and `/tampa/`. Record the output.

## Apply

5. Cloudflare dashboard → zone `acglass.com` → **Rules → Redirect Rules → Bulk
   Redirects**. Open the existing list that contains
   `/commercial-glazing-miami.html`.

6. Edit the two rows in place - do **not** add new rows, or you will have two
   rules matching one source and the winner is order-dependent:

   | Source URL | Target URL | Status | Preserve query string | Subpath matching |
   |---|---|---|---|---|
   | `https://acglass.com/commercial-glazing-miami.html` | `https://acglass.com/miami-hvhz-glazing-contractor.html` | 301 | on | off |
   | `https://acglass.com/commercial-glazing-tampa.html` | `https://acglass.com/tampa-commercial-glazing.html` | 301 | on | off |

   Leave every other row untouched. There are 69 rules; 67 of them are not part
   of this change.

## Verify

7. Confirm one hop, correct destination, and that the destination is
   self-canonical:
   ```
   curl -sI https://acglass.com/commercial-glazing-miami.html | grep -iE '^(HTTP|location)'
   curl -sI https://acglass.com/commercial-glazing-tampa.html | grep -iE '^(HTTP|location)'

   curl -s https://acglass.com/miami-hvhz-glazing-contractor.html | grep -o 'rel="canonical"[^>]*'
   curl -s https://acglass.com/tampa-commercial-glazing.html      | grep -o 'rel="canonical"[^>]*'
   ```
   Expect `301` then `Location: https://acglass.com/miami-hvhz-glazing-contractor.html`
   (and the Tampa equivalent), and each canonical pointing at itself. If a second
   hop appears, you added rows instead of editing them.

8. Update the mirror so it stops lying. In a follow-up commit, change the two
   `destination` values in `vercel.json` to match, then confirm:
   ```
   python3 .github/scripts/canonical-verify.py --live
   ```
   This is bookkeeping. It deploys nothing.

9. Set `"activated": true` in `redirects.manifest.json` in that same commit, and
   paste the step 7 output into the commit message. The static gate fails while
   `activated` is `true` **and** the manifest still lists rules whose
   `current_destination` disagrees with the mirror, so steps 8 and 9 belong
   together.

10. In Google Search Console, use URL Inspection on both sources and both
    destinations, then request indexing for the two destinations. Watch
    `/miami-hvhz-glazing-contractor.html` and `/tampa-commercial-glazing.html`
    impressions for four weeks.

## Rollback

Revert the two Target URLs to `https://acglass.com/miami/` and
`https://acglass.com/tampa/`, revert the `vercel.json` follow-up commit, and set
`"activated": false`. Recovery is immediate; 301s are cached by browsers but
Cloudflare serves the new value to every fresh request and Google re-crawls on
its own schedule.

## What this runbook does not do

- It does not touch West Palm Beach. Not one rule, not one canonical, not one
  byte of visible content. WPB is #1 organic and #1 in the map pack, the ranking
  URL is not attributable from the available evidence, and the two research
  documents in the workspace prescribe opposite primaries for it.
- It does not resolve Orlando, Naples, Fort Lauderdale or Boca Raton. Those need
  a commercial-glazing hub page written first.
- It does not promote `/commercial-glazing-near-me-florida.html` to statewide
  primary. `/glazing-contractor-florida.html` holds that intent.
- It does not flatten the ~27 non-money-market city two-hops.
- It does not act on any Search Console data, because no GSC export exists in
  this workspace and the measurement layer merged in PR #20 has never run - it
  needs the `GSC_SA_JSON` secret. Every "gsc-gated" entry in
  `.github/seo/url-primaries.json` is waiting on that.
