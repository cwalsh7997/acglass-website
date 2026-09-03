# Citations (living record)

Primary sources already used on acglass.com. This is a ledger, not a new public claim. Re-check the live URL before quoting. Do not invent ranks or third-party review totals.

Last updated: 2026-09-03
Seeded from live `llms.txt`, `facts.html`, and homepage JSON-LD.

## Euro-Wall locator request (sent)

Email sent 2026-09-02 from connor@acglass.com to info@euro-wall.com to distinguish American Commercial Glass (acglass.com, West Palm Beach / Naples / Tampa) from A-Christian Glass (ACG) in Delray Beach, which the official Euro-Wall locator currently lists. Status: **sent**. Do not treat this as a completed listing change. [NEED: Euro-Wall reply and a date-stamped locator capture.]

## Entity and license

| Claim | Source | URL | Last live check |
| --- | --- | --- | --- |
| Legal name American Commercial Glass, Inc. | Florida Division of Corporations (Sunbiz) P21000018259 | https://search.sunbiz.org/Inquiry/CorporationSearch/SearchResults?inquiryType=EntityName&searchTerm=american+commercial+glass | 2026-09-03 (cited on live `facts.html` / `llms.txt`; registry page not re-fetched this run) |
| FL CGC #1531993 | Florida DBPR | https://www.myfloridalicense.com | 2026-09-03 (present on live homepage JSON-LD, `facts.html`, `llms.txt`) |
| Founded February 18, 2021 | `facts.html` ID-02 | https://acglass.com/facts.html | 2026-09-03 |
| Wikidata Q139858578 | Wikidata | https://www.wikidata.org/wiki/Q139858578 | 2026-09-03 (linked from live `llms.txt` / `facts.html`) |
| NAICS 238150 | `facts.html` ID-05 | https://acglass.com/facts.html | 2026-09-03 |
| President Connor Walsh | `authors/connor-walsh.html` Person schema | https://acglass.com/authors/connor-walsh.html | 2026-09-03 |
| CEO / 51% owner Rielly Walsh | `facts.html` leadership block | https://acglass.com/facts.html | 2026-09-03 |

## Offices

| Office | Address (from live `locations.html` / `facts.html`) | Last live check |
| --- | --- | --- |
| HQ West Palm Beach | 700 S Rosemary Ave Ste 204, West Palm Beach, FL 33401 | 2026-09-03 |
| Naples | 4850 Tamiami Trail N Ste 301, Naples, FL 34103 | 2026-09-03 |
| Tampa | 3031 N Rocky Point Dr W Ste 600, Tampa, FL 33607 | 2026-09-03 |
| Nashville | Q3 2026, not live coverage | 2026-09-03 (`facts.html`) |

## Manufacturer posture (do not upgrade these)

| Manufacturer | Stated relationship on live `facts.html` | On-site page | Last live check |
| --- | --- | --- | --- |
| ESWindows / Tecnoglass | Commercial installer | https://acglass.com/eswindows-installer-florida.html | 2026-09-03 |
| Euro-Wall | Installer; factory certified. Official Euro-Wall locator does **not** list American Commercial Glass. | https://acglass.com/euro-wall.html | 2026-09-03 |

## Manufacturer HTML fetches (2026-09-03)

Used to source `/products/euro-wall/`. Do not upgrade installer status from these rows.

| URL | Result | Facts used |
| --- | --- | --- |
| https://eswindows.com/ | Blocked twice on 2026-09-03. HTTP 403 + Cloudflare "Just a moment..." challenge. | None. `/products/eswindows/` skipped again. |
| https://euro-wall.com/ | 200. HQ 2200 Murphy Court, North Port, FL 34289. 888.989.EURO. info@euro-wall.com. FOR YOU Crew. Locator exists. | HQ, phone, email, support program name. |
| https://euro-wall.com/products/ | 200. Crafted in the USA. Sliding / Folding / Pivot / Windows. | USA manufacture claim. |
| https://euro-wall.com/products/commercial-products/ | 200. Commercial families listed, including thermally broken fold and window lines. | Family names only where dedicated HTML was not fetched. |
| https://euro-wall.com/products/sliding-door-systems/vista-multi-slide/ | 200. Impact/non-impact. Interlock &lt; 1 in. Up to 8 panels in one stack. ASTM/TAS/AAMA list. 10-year warranty from purchase. Kynar or powder coat. DP charts present, no numbers in HTML. | Copied onto `/products/euro-wall/`. DPs omitted. |
| https://euro-wall.com/products/folding-door-systems/vista-fold-impact-rated/ | 200. 14 ft / 52 in panels. Config list. ASTM/TAS list. 10-year warranty. DP charts, no numbers. | Copied. DPs omitted. |
| https://euro-wall.com/products/vista-pivot/ | 200. 168 in H x 100 in W. AAMA 2605 standard finish. ASTM/TAS/AAMA list. 10-year warranty. | Copied. DPs omitted. |
| https://euro-wall.com/products/vista-ds/ | 200. 1-1/4 in profile. Up to 14 ft x 9 ft. ASTM/TAS list. 10-year warranty. FL PA resource link, number not in HTML. | Copied. FL PA number omitted. |
| https://acglass.com/euro-wall.html | 200. Installer page. Publishes a DP table and DirectSet / Vista Windows names. | Relationship + named jobs. DP table not copied. |
| https://acglass.com/euro-wall-installer-florida.html | 200. Names SGD2020 and Vistafold. Lead times 14-20 weeks. Named jobs. | Named jobs only. Lead times and SGD2020-as-SKU omitted. |
| https://acglass.com/noa/euro-wall.html | Timed out this run. | None. |
| https://acglass.com/eswindows-installer-florida.html | 200. Installer page with NOA/DP table. | Linked from `/products/` only. Table not copied. |
| https://acglass.com/noa/eswindows.html | 200. NOA table; several pending verification. ES-8000 figures conflict with the installer page. | Not copied. |
| PGT, Allegion, TGP, Slimpact, Aldora | Installed and coordinated to spec. Not authorized-dealer relationships. | https://acglass.com/manufacturers.html | 2026-09-03 |

## SameAs already published (do not add new ones here)

From live organization JSON-LD / `llms.txt`. Presence on this list is not a rank.

- https://www.wikidata.org/wiki/Q139858578
- https://www.linkedin.com/company/acglass
- https://www.facebook.com/acommercialglass
- https://www.instagram.com/acglass.co
- https://network.procore.com/p/american-commercial-glass-west-palm-beach
- https://www.bbb.org/us/fl/west-palm-beach/profile/window-installation/american-commercial-glass-inc-0633-92045708
- https://downtobid.com/company/american-commercial-glass
- https://www.yelp.com/biz/american-commercial-glass-west-palm-beach
- https://www.buildzoom.com/contractor/american-commercial-glass-inc
- https://www.esourcebook.net/west-palm-beach/glass-industry-supplier/american-commercial-glass

## Open citations

- [NEED: current DBPR license snapshot URL with date]
- [NEED: Euro-Wall official locator URL + date-stamped capture that ACG is absent and A-Christian Glass is listed]
- Euro-Wall locator request: sent 2026-09-02 from connor@acglass.com to info@euro-wall.com. Distinguishes A-Christian Glass Delray. [NEED: reply and locator recapture]
- Naples Google Business Profile: case 2-8095000041141. [NEED: case status and what the listing currently shows]
- Tampa Google Business Profile: suspended. [NEED: suspension reason and restore date]
- West Palm Beach Google Business Profile: Bobcat post. [NEED: post URL, date, and whether it is still live]
- [NEED: live Google rank for `commercial glazing contractor Florida` (homepage vs new hub)]
- [NEED: manufacturer letters (ESWindows, Euro-Wall) if they will be quoted on `/products/`]
- [NEED: successful fetch of eswindows.com product HTML before creating `/products/eswindows/`]
- [NEED: Euro-Wall dedicated pages for thermally broken fold, thin-line, casement, fixed, and multi-directional fold if those SKUs will be specified by number]
- [NEED: Euro-Wall Florida Product Approval / NOA numbers from a fetched manufacturer page or PDF, not from ACG-only tables]
