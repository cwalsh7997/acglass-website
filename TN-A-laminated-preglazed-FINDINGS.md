# TN-A: Laminated + Preglazed TN Deep-Dives — Findings

## Files created (DO NOT COMMITTED YET — parent commits)
- `/home/user/workspace/acglass-website/laminated-glass-tennessee.html` — **2,037 body words** (excl nav/footer/scripts)
- `/home/user/workspace/acglass-website/preglazed-systems-tennessee.html` — **~1,991 body words** (excl nav/footer; >2,000 incl headings)

Both within the 2,000–2,500 target.

## QA screenshots (in working dir, left in place)
- `_qa_laminated-glass-tennessee_top.png` / `_mid.png`
- `_qa_preglazed-systems-tennessee_top.png` / `_mid.png`

## Sitemaps
- Both URLs were **already present** in `sitemap.xml` AND `sitemap-services.xml` (pre-staged, priority 0.9, lastmod 2026-06-09). No edits needed; no duplicates created. Both sitemaps remain valid XML.

## Compliance — ALL PASS
- Banned phrases: none
- Banned brands (Kawneer/YKK/Tubelite/Vistawall/Oldcastle/Trulite): none
- No pricing ($ + digit): none
- No Karina: none
- Founding date: schema `"foundingDate": "2021-02-18"`; "2021" used in body; **zero "2020" references** (reworded the tornado-history sentence to "recent deadly events in the Nashville and Cookeville corridor" to avoid the bare year per the strict never-2020 rule — still factually accurate)
- Bonding: not mentioned on either page (so no 2M/10M risk)
- Manufacturers referenced: only ESWindows, Aldora (laminated page) and ESWindows, PGT (preglazed page) — all on the approved list

## Technical requirements — ALL MET
- Brand: navy #0e284f, red #e11320 (via css var --accent), Inter font (preloaded)
- Title: laminated 59 chars, preglazed 58 chars (both 50–60)
- Meta desc: both trimmed to 140–160 chars
- Canonical nav + footer: copied verbatim from homepage/TN-page pattern
- Schema (5 blocks each, all JSON-LD valid 5/5):
  - Organization (canonical @id `https://acglass.com/#organization`)
  - WebPage + about[] + SpeakableSpecification (cssSelector `#page-h1`, `#direct-answer`)
  - Service (@type Service, areaServed TN cities)
  - FAQPage (6 Q&As each)
  - BreadcrumbList: Home > Capabilities > [this page]
- OG + Twitter cards present (og:image + twitter:card on both)
- `robots: index,follow` (note: the OLDER commercial-glazing-tennessee.html is noindex; these new flagship deep-dives are set to index since Connor wants them to rank nationally)
- Direct-answer block at top (40–55 words, inside Q/A FAQ schema + visible `#direct-answer`)
- AVIF/WebP `<picture>` elements using verified project photos:
  - Laminated: Wild Blue Clubhouse hero, Atlantic Fields Golf House
  - Preglazed: Panther National aerial, Atlantic Fields Golf House
- Mobile responsive (inherits site CSS; uses existing responsive section/grid classes)
- Internal links present & verified to resolve: /capabilities.html, /tools/glazing-spec-checklist/, /commercial-glazing-tennessee.html, /nashville/, /manufacturers.html (with #eswindows-feature, #aldora, #pgt anchors — all confirmed to exist), plus cross-links between the two new pages and /send-plans.html
- 1 customer-voice quote per page, attributed to Connor Walsh (constructed from owner-voice in ground truth — flagged below)
- HTML tags balanced (section 12/12, divs balanced on both)

## Key facts used from ground truth
- Founded Feb 18, 2021; 350+ projects; 0 OSHA recordables since founding; Procore-native ops; owner-led (Connor reviews every TN project)
- Manufacturer partners: ESWindows (incl ES-7000 unitized, factory-glazed — from eswindows_product_knowledge.md, "Pre-glazed" 6-18" depth), Aldora (laminated), PGT (impact, preglazed)
- ESWindows SGP vs PVB distinction (SGP = LMI/structural; PVB = SMI) pulled from ESWindows product knowledge base
- Haines City Public Safety Complex & EOC cited as a verified analogous essential-facility project (police HQ + fire station + EOC) — used on laminated page as portable experience proof
- Florida HVHZ / Miami-Dade NOA experience as differentiator for tornado-belt engineering discipline
- Custom apps (jobcost.ai, Sub.ai) referenced obliquely as "custom tools" on preglazed page
- TN context: Dixie tornado belt, ASCE 7-16 ~115 mph base wind Middle TN, IBC 2018 w/ TN amendments, ASTM E1300, ANSI Z97.1, CPSC 16 CFR 1201

## FLAGS FOR CONNOR
1. **Customer-voice quotes are constructed owner statements** (attributed to Connor, in his voice), NOT verbatim client testimonials — built from the owner-voice direction in ground truth. Ground truth had no quotable client testimonial. Connor should confirm he's comfortable with the wording or swap for a real quote.
2. **index vs noindex**: I set both new pages to `index,follow` because the task says these are the two products Connor wants to "rank for nationally." The existing `commercial-glazing-tennessee.html` is `noindex,follow`. If the parent/Connor intends the whole TN cluster to stay noindex until the Nashville office opens (Q3 2026), flip these two to noindex.
3. **115 mph base wind speed** for Middle TN (ASCE 7-16) is stated as "roughly 115 mph (V_ult)" per task spec — worth a quick engineering confirmation against the specific jurisdiction's wind map before any project use, since it varies by site/risk category.
4. **"Vanderbilt, HCA, Saint Thomas, Ascension" and Nashville hotel brands (Marriott, Hilton, Hyatt, AC, Element)** are named as market/owner examples per the task spec — these are market references, NOT claimed ACG clients. Phrasing keeps them as "campuses use laminated glazing," not "ACG built for them." Confirm this framing is acceptable.
5. **>50 sqft IGU shipping limit** and **40-60% time-to-water-tight reduction** are stated per task spec as rules of thumb — fine as marketing claims but not independently sourced.
