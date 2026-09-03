# SEO lessons (living record)

Working notes for acglass.com. Not a marketing page. Do not invent ranks, traffic, or citations. If a measurement is missing, write `unknown`.

Last updated: 2026-09-03 (products index + Euro-Wall specs; ESWindows product page skipped)
Source: live page checks + repo audit on branch `seo-auto`. `_internal/CLAUDE.md` was not present in this environment.

## Architecture

- Repo root is the GitHub Pages deploy root. Every tracked file is publicly served.
- Homepage title (live 2026-09-03): `Commercial Glazing Contractor Florida | ACG`. Homepage is the federal lead. Do not rewrite it in the week-1 PR beyond one internal link.
- Target Florida hub: `/florida-commercial-glazing/` (was live 404). Long-form sibling already exists: `/florida-commercial-glazing-complete-guide/`.
- Real services URL is `/services.html`. `/services/` is a noindex JS + meta-refresh stub.
- Real author URL is `/authors/connor-walsh.html`. `/author-connor-walsh.html` is a noindex stub. `/about/connor-walsh/` is now the same stub pattern (noindex + canonical + meta-refresh + JS). Not a second bio. Not an HTTP 301. `/about/index.html` is a matching parent stub to `/about.html` so creating the `about/` directory does not leave `/about/` as a 404 parent.
- `/products/` is an installer index. `/products/euro-wall/` is sourced. `/products/eswindows/` was not created (manufacturer site blocked).
- `/projects/` and `/resources/` exist and are self-canonical.
- Office metros `/west-palm-beach/`, `/naples/`, `/tampa/` were live-canonicalized off to `/storefront-glazier-{city}-florida/` clones. Do not bulk-fix the rest of the storefront-glazier set in a week-1 PR.

## Sitemap

- `robots.txt` points at `sitemap-index.xml` and also at `sitemap.xml` (master). Listing the master inside the index duplicates every URL for index-following crawlers.
- Master-only URLs (not in any child sitemap) were the 8 out-of-Florida state pages.
- Child-only URL: `/florida-federal-glazing-reference.html` (in `sitemap-services.xml`, missing from master).
- `services-schema-block.html` is a JSON-LD include fragment, not a page. It was in `sitemap.xml` and `sitemap-services.xml`. Live 200, no canonical.
- Filesystem resolve of all sitemap `<loc>` values (except image URLs) found 0 missing files on 2026-09-03. Live 404s that were not in sitemaps: `/florida-commercial-glazing/`, `/products/`, `/about/connor-walsh/`.

## Indexation conflicts

- `llms.txt` states Florida only. Eight indexable out-of-Florida pages still exist (`commercial-glazing-al.html`, `-ga.html`, `-louisiana.html`, `-north-carolina.html`, `-south-carolina.html`, `-southeast.html`, `-texas.html`, `-tn.html`). Do not delete them. noindex + self-canonical + drop from sitemaps is the containment move.
- Duplicate title pattern on office metros: `Storefront Glazier in {City}, FL | ACG - 48-Hr Bids` (WPB variant added "Service Area" and em dashes). Storefront-clone titles for Naples and Tampa were already rewritten; WPB clone still matches the old pattern.
- ACG holds no Nashville or Tennessee office. Live offices are West Palm Beach, Naples, and Tampa only. Tennessee pages are furnish-and-consult geography, not a live office.

## Redirects

- GitHub Pages static hosting has no native HTTP 301. This repo has no Jekyll `_config.yml` and no `jekyll-redirect-from` pipeline.
- `vercel.json` is an observed mirror of Cloudflare edge rules. Editing it does not deploy redirects on GitHub Pages (see `.github/cloudflare/RUNBOOK.md`). Do not invent a Cloudflare rule from this repo.
- Existing stubs (`/services/`, `/contact/`, `/author-connor-walsh.html`) already use `rel=canonical` + `noindex,follow` + meta-refresh + JS `location.replace`. That is the GitHub Pages-safe pattern. Same pattern applied to `services-schema-block.html` (snippet, not a page). JSON-LD body of that file was kept below the stub so the snippet was not deleted.
- Live 301s observed on host/www are Cloudflare edge rules.

## Claims discipline

- Never publish unverified quantitative claims, certifications, NOAs, lead times, prices, or manufacturer relationships.
- Verified manufacturer posture (from `facts.html`, re-checked 2026-09-03): ESWindows = commercial installer; Euro-Wall = installer / factory certified; PGT, Allegion, TGP, Slimpact, Aldora = installed to spec, not authorized-dealer relationships.
- Euro-Wall official locator does not list American Commercial Glass. It lists A-Christian Glass (ACG) in Delray Beach. That is a name-collision risk, not a dealer listing for this company.
- Positioning line: `Precision glazing. AI-managed. Delivered.` Do not compete on price.

## Week-1 decisions

- Unique-ify titles/descriptions on the 3 office metros only.
- Self-canonical on those 3 office metros is optional and is Tier 2 (creates a second indexable URL next to each storefront clone).
- Add `/florida-commercial-glazing/` as the state hub. Link only to URLs that exist.
- Do not bulk-generate city or service pages. Do not noindex the blog set.
- Wave-2 inventory (counts only): `seo/prune-wave2.md`. 77 city storefront + 77 railing + 77 impact + 101 storefront-glazier URLs. Recommendation is noindex+sitemap drop, not 301 onto the 3 offices + 6 satellites. Not applied.

## Products pass (2026-09-03)

- `/products/` created as an installer index. Links Euro-Wall to the new sourced page. ESWindows stays on `/eswindows-installer-florida.html`.
- `/products/euro-wall/` sourced from euro-wall.com HTML (home, products, commercial-products, Vista Multi Slide, Vista Fold, Vista Pivot, Vista DS) plus re-fetched ACG pages (`euro-wall.html`, `euro-wall-installer-florida.html`, `facts.html`). Numeric DPs, NOA numbers, FL PA numbers, and lead times omitted. SGD2020 / Vistafold named only as ACG-page labels, not factory SKUs.
- `/products/eswindows/` skipped. `https://eswindows.com/` returned a Cloudflare "Performing security verification" challenge on 2026-09-03. Product URLs timed out. Do not copy the ACG installer or `/noa/eswindows.html` tables onto a new URL until the manufacturer HTML can be fetched. Existing ACG ESWindows NOA/DP figures also conflict across those two on-site pages.
- `/about/connor-walsh/` noindex stub added. `/about/index.html` parent stub added so the new `about/` directory does not 404 `/about/`. Neither stub is in sitemaps. Neither is a second bio. Do not call either an HTTP 301.
- 77×3 city folders were not noindexed in this pass.
- One-line link from `/services.html` technical references to `/products/`. No services rewrite.
