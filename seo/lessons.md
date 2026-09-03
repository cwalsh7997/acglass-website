# SEO lessons (living record)

Working notes for acglass.com. Not a marketing page. Do not invent ranks, traffic, or citations. If a measurement is missing, write `unknown`.

Last updated: 2026-09-03
Source: live page checks + repo audit on branch `seo-auto`. `_internal/CLAUDE.md` was not present in this environment.

## Architecture

- Repo root is the GitHub Pages deploy root. Every tracked file is publicly served.
- Homepage title (live 2026-09-03): `Commercial Glazing Contractor Florida | ACG`. Homepage is the federal lead. Do not rewrite it in the week-1 PR beyond one internal link.
- Target Florida hub: `/florida-commercial-glazing/` (was live 404). Long-form sibling already exists: `/florida-commercial-glazing-complete-guide/`.
- Real services URL is `/services.html`. `/services/` is a noindex JS + meta-refresh stub.
- Real author URL is `/authors/connor-walsh.html`. `/author-connor-walsh.html` is a noindex stub. `/about/connor-walsh/` is a live 404.
- `/products/` is a live 404. Do not create it until manufacturer spec sourcing is ready.
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
- Nashville office is Q3 2026, not live coverage (`facts.html`). Do not treat TN pages as a live office.

## Redirects

- GitHub Pages static hosting has no native HTTP 301. This repo has no Jekyll `_config.yml` and no `.nojekyll` is required for static serve, but there is also no `jekyll-redirect-from` pipeline.
- Existing stubs (`/services/`, `/contact/`, `/author-connor-walsh.html`) already use `rel=canonical` + `noindex,follow` + meta-refresh + JS `location.replace`. That is the GitHub Pages-safe pattern.
- Live 301s observed on host/www are Cloudflare edge rules. Do not invent a new Cloudflare rule from this repo.

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
