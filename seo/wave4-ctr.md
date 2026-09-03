# SEO wave-4: CTR on ranking RFQ pages

Counted on branch `cursor/seo-wave4-ctr-b764`, 2026-09-03, rebased onto `main` after PR 95 (`e6bd1066`). `_internal/CLAUDE.md` was not present.

Source of truth for traffic: operator GSC export, Web, last 28 days, pulled 2026-09-03. Headline 119 clicks / 13,237 impressions vs 265 / 28,673 prior. Almost all query-attributed clicks are branded (`american commercial glass` 25 clicks, position 1.26 → 6.17). Unbranded: 1 click across 1,528 query rows.

No pages were deleted. No city templates added. Keepers stay indexable. `/products/eswindows/` was not created. Homepage was not redesigned. Homepage title, description, H1, and NAP stay. Nashville stays cancelled. Tennessee stays furnish/consult, no field labor, no opening date. The only Tennessee file edited is `federal-glazing-contractor-tennessee.html`, and only to soften one unsupported authorization string. No DNS change. No extra www/http redirect. Sitemap advertising left apex-only (`robots.txt` still lists only `https://acglass.com/sitemap.xml`).

## What changed

Titles and meta descriptions on pages already on page 1-2 for buyer queries. Each new title uses a differentiator already on that page (48-hour bid, FL CGC #1531993, metro, HVHZ, or founded 2021). Each edited page now has a visible body text link to `/florida-commercial-glazing/` and to `/send-plans.html` or `/contact.html`.

`/west-palm-beach-commercial-glazing.html` was lifted from the byte freeze so title/meta/hub-link edits could ship. Canonical, H1, and NAP schema on that file were not rewritten. Homepage freeze stays.

## Old vs new title and description

Lengths are characters. CI allows titles 30-60 and descriptions 80-155.

| URL | GSC 28d (clk / impr / pos) | Old title (len) | New title (len) | Old description (len) | New description (len) |
| --- | --- | --- | --- | --- | --- |
| `/west-palm-beach-commercial-glazing.html` | 1 / 274 / 6.28 | Commercial Glazing West Palm Beach, FL \| ACG - 48-Hour Bids (59; live used a long dash) | Palm Beach Commercial Glass Contractor \| 48-Hr Bid (50) | ACG is Palm Beach County's commercial glazing subcontractor. Division 08 full scope, 48-hour bid turnaround. Licensed CGC1531993. (129) | West Palm Beach commercial glass contractor for Palm Beach County GCs. FL CGC #1531993. Bid in 48 hours. Send drawings. Call (772) 486-7711. (140) |
| `/portfolio.html` | 0 / 143 / 5.52 | American Commercial Glass Portfolio and Projects \| ACG (54) | Florida Commercial Glazing Portfolio \| CGC 1531993 (50) | Review commercial glazing project examples from American Commercial Glass, including storefront and curtain wall work. Send drawings. (133) | Florida commercial glazing projects for GCs: storefront, curtain wall, impact. FL CGC #1531993. Bid in 48 hours. Send drawings. (772) 486-7711. (143) |
| `/blog/what-is-division-08-construction.html` | 1 / 305 / 8.67 | What Is Division 08 in Construction? Guide for GCs \| ACG (56) | Division 08 Construction for Florida GCs \| 48-Hr Bid (52) | Understand Division 08 construction scope, common sections and how openings work is coordinated for a commercial project. Send drawings. (136) | Division 08 is openings: storefront, curtain wall, doors. Florida commercial glazing contractor, FL CGC #1531993. Bid in 48 hours. (772) 486-7711. (146) |
| `/miami-dade-noa-explained/` | 1 / 141 / 8.74 | Miami-Dade NOA: Notice of Acceptance Guide for GCs \| ACG (56) | Miami-Dade NOA Explained for HVHZ GCs \| CGC 1531993 (51) | Learn what a Miami-Dade NOA covers, how to read approval data and where it matters in glazing submittals. Use it before bid day. Send drawings. (143) | Miami-Dade NOA for HVHZ glazing submittals. Florida commercial glazing contractor, FL CGC #1531993. Bid in 48 hours. Send drawings. (772) 486-7711. (147) |
| `/blog/commercial-glazing-warranties-florida.html` | 0 / 128 / 6.19 | Commercial Glazing Warranties Florida Guide for GCs \| ACG (57) | Florida Glazing Warranties for GCs \| Bid in 48 Hours (52) | Learn what commercial glazing warranties typically address, what documents to review and how to track closeout. Send drawings. (126) | Florida commercial glazing warranties for GCs: labor, glass, aluminum, sealant. FL CGC #1531993. Bid in 48 hours. Send drawings. (772) 486-7711. (144) |
| `/about.html` | 0 / 110 / 10.61 | American Commercial Glass: Florida Glazing Team \| ACG (53) | ACG Florida Glazing Contractor \| Founded 2021, CGC (50) | Meet American Commercial Glass, a West Palm Beach commercial glazing subcontractor with Florida CGC license #1531993. Send drawings. (132) | West Palm Beach commercial glazing contractor, founded 2021. FL CGC #1531993. Offices in WPB, Naples, Tampa. Bid in 48 hours. (772) 486-7711. (141) |
| `/contact.html` | 0 / 81 / 56 | Contact ACG \| American Commercial Glass (39) | Florida Glazing Bid Desk \| Send Plans, 48-Hr Reply (50) | Contact American Commercial Glass about a commercial glazing project. West Palm Beach HQ. For drawings, use the send-plans page. (772) 486-7711. (144) | Send plans for a Florida commercial glazing bid today. West Palm Beach HQ, FL CGC #1531993. Scope letter back in 48 hours. Call (772) 486-7711. (143) |
| `/blog/what-does-a-glazing-contractor-do.html` | 1 / 69 / 7.58 | What Does a Glazing Contractor Do? Guide for GCs \| ACG (54) | Glazing Contractor Meaning \| Florida GCs, 48-Hr Bid (51) | Learn what a glazing contractor does, from scope review and submittals to installation coordination and closeout. Plan ahead. Send drawings. (140) | Glazing contractor meaning for GCs: scope, submittals, install, closeout. Florida CGC #1531993. Bid in 48 hours. Send drawings. (772) 486-7711. (143) |
| `/blog/florida-building-codes-commercial-glazing-2026.html` | 0 / 60 / 8.12 | Florida Building Codes for Commercial Glazing \| ACG (51) | 2026 Florida Glazing Codes for GCs \| HVHZ, 48-Hr Bid (52) | Use this guide to review Florida commercial glazing code topics, approvals and document coordination steps. Use it before bid day. Send drawings. (145) | 2026 Florida building codes for commercial glazing, including HVHZ and NOA. FL CGC #1531993. Bid in 48 hours. Send drawings. (772) 486-7711. (140) |
| `/blog/commercial-glazing-project-turnaround-time-florida.html` | 0 / 59 / 6.76 | Commercial Glazing Project Turnaround Time Guide \| ACG (54) | Commercial Glazing Turnaround in Florida \| 48-Hr Bid (52) | Learn what drives commercial glazing turnaround, from scope review and submittals to procurement and field readiness. Send drawings. (132) | Florida commercial glazing turnaround: takeoff, submittals, fabrication, install. FL CGC #1531993. Bid in 48 hours. Send drawings. (772) 486-7711. (146) |
| `/blog/commercial-glazing-submittal-process-guide.html` | 0 / 67 / 9.87 | Commercial Glazing Submittal Process Guide for GCs \| ACG (56) | Glazing Submittals for GCs \| Florida, CGC #1531993 (50) | Follow a commercial glazing submittal process that helps GCs track approvals, questions and release decisions. Send drawings. (125) | Glazing submittals for GCs: shop drawings, NOA, approvals, and delay causes. FL CGC #1531993. Bid in 48 hours. Send drawings. (772) 486-7711. (141) |
| `/florida-commercial-glazing/` | not in 28-day page table | Commercial Glazing Contractor Florida \| ACG (43) | Commercial Glazing Contractor Florida \| Bid in 48 Hrs (53) | American Commercial Glass is a Florida commercial glazing contractor. Division 08 storefront, curtain wall, impact, operable walls. FL CGC #1531993. (148) | Florida commercial glazing contractor for South Florida GCs. WPB, Naples, Tampa. FL CGC #1531993. Bid in 48 hours. Send drawings. (772) 486-7711. (145) |
| `/` | branded / hash URLs | Commercial Glazing Contractor Florida \| ACG (43) | unchanged | Florida's commercial glazing contractor for storefront, curtainwall, and impact glass - 350+ projects, FL CGC #1531993, bonded $3M/$6M. Get a scope in 48 hrs. (158, held; live uses a long dash) | unchanged |

Homepage title already says commercial glazing contractor Florida. Homepage description already says get a scope in 48 hrs. Frozen. Not edited.

## Hub title (live-verify collision)

Live HTTP verify 2026-09-03 ~9:40 AM PT: homepage and `/florida-commercial-glazing/` shared the exact title `Commercial Glazing Contractor Florida | ACG`. Homepage keeps that company/home title. Hub title is now unique and aimed at Florida GC queries: `Commercial Glazing Contractor Florida | Bid in 48 Hrs` (53). og/twitter/JSON-LD `name` match. Description from the earlier pass stays.

## Canonicals (live verify 2026-09-03)

Pages were not deleted. og:url follows each new canonical.

| URL | Old canonical | New canonical |
| --- | --- | --- |
| `/west-palm-beach/` | `https://acglass.com/west-palm-beach/` (self) | `https://acglass.com/storefront-glazier-west-palm-beach-florida/` |
| `/naples/` | `https://acglass.com/naples/` (self) | `https://acglass.com/storefront-glazier-naples-florida/` |
| `/tampa/` | `https://acglass.com/tampa/` (self) | `https://acglass.com/storefront-glazier-tampa-florida/` |
| `/florida-commercial-glazing-complete-guide/` | `https://acglass.com/florida-commercial-glazing-complete-guide/` (self) | `https://acglass.com/florida-commercial-glazing/` |

Complete-guide breadcrumb item now names the hub. File stays on disk, stays 200. Hub office cards now link the three keeper glazier URLs so the office-metro aliases do not create new cross-canonical edges.

Those four URLs were dropped from `sitemap.xml` and the matching child urlset (`sitemap-cities.xml` for the three office metros, `sitemap-pages.xml` for the complete guide) because crawl-check requires sitemap locs to be self-canonical. Keepers stay listed. This is not sitemap-advertising expansion. `robots.txt` still advertises only the apex sitemap. Unique `sitemap.xml` locs after the drop: 901.

## Inbound (live verify 2026-09-03)

Specified main-page inbound to `/florida-commercial-glazing/` was 14, not 23. Missing from about, portfolio, glossary, and most `/storefront-*` and `/curtainwall-*` URLs. About and portfolio already gained hub links in the title pass. This pass adds crawlable text links on `glossary.html`, `storefront-glossary.html`, and the remaining storefront/curtainwall service pages. `storefront-installer-nashville.html` was not edited.

Specified main-page inbound to `/products/euro-wall/` was 0. Crawlable text links added from homepage (body only; title/desc/H1/NAP untouched), about, portfolio, contact, glossary, storefront-glossary, the three office metros, the eight keeper glazier pages, and the storefront/curtainwall service pages. Anchor text is installer/specifier ("Euro-Wall Vista page", "sourced operable-wall specs"). No authorization invented.

## Claims softened (live verify 2026-09-03)

| URL | Old string | New string |
| --- | --- | --- |
| `/products/euro-wall/` | Factory certified installer per facts.html. | Installer and specifier language only. |
| `/products/euro-wall/` | facts.html lists Euro-Wall as installer, factory certified. | facts.html lists Euro-Wall as installer. |
| `/federal-glazing-contractor-tennessee.html` | manufacturer- / authorized install (SVG) | installer and / specifier |

Tennessee page still says no Tennessee office or field labor. No Nashville opening language restored.

Website Agent owns jsPDF / scope-engine, architect-resources 404s, Ocean Prime 301s, and google verify files. Those files were not edited here.

## Sitemap / host variants

Repo sitemaps list `https://acglass.com/...` only. No `http://` and no `www` locs. `robots.txt` sitemap lines are the same apex HTTPS set.

Live 2026-09-03: `http://www.acglass.com/` → 301 → `https://www.acglass.com/` → 301 → `https://acglass.com/`. www does not serve 200. No extra redirect layer added.

## Homepage hash URLs

GSC shows 52 impressions each on `/#capability`, `/#discipline`, `/#prequal`. Homepage already has a fragment-free canonical (`https://acglass.com/`). Those hashes are in-page nav, not separate files. No simple extra canonical without a redesign. Left alone.

## Left alone

- Homepage title, description, H1, NAP schema
- Keepers stay indexable (WPB, Naples, Tampa, Miami, Orlando, Fort Lauderdale, Fort Myers, Sarasota storefront-glazier pages)
- `/products/eswindows/` (still absent; manufacturer HTML still blocked as of wave-3)
- DNS, nav, logo, brand tokens
- GBP
- Sitemap advertising (apex-only from PR 95)
- 324 wave-2 `noindex,follow` pages and the 8 keepers
- `storefront-installer-nashville.html` (no hub or euro-wall link added)
- jsPDF / scope-engine, architect-resources, Ocean Prime, google verify files
