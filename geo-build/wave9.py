#!/usr/bin/env python3
"""Wave 9 — 4 long-form blog articles + 12 more vertical×city pages + 6 more AIO FAQ.
Final massive build to push toward 1,200 URL sitemap."""
import os, html as html_lib, json

OUT = "/home/user/workspace/acglass-website"

GTAG = '''<script async src="https://www.googletagmanager.com/gtag/js?id=G-M7BFQD2SPP"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}gtag("js",new Date());gtag("config","G-M7BFQD2SPP");</script>'''

FONTS = '<link rel="stylesheet" href="/css/style.css?v=1777031720"><link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">'

NAV = '''<nav class="nav scrolled"><div class="nav-inner">
<a href="/index.html" class="nav-logo"><img height="72" width="338" src="/images/acg-logo-nav@2x.png" style="height:36px;width:auto;" alt="ACG" class="logo-img" loading="lazy"></a>
<div class="nav-links"><a href="/index.html">Home</a><a href="/blog.html">Blog</a><a href="/case-studies/">Case Studies</a><a href="/resources/">Resources</a><a href="/send-plans.html" class="nav-cta">Send Us Plans</a></div></div></nav>'''

FOOTER = '''<footer class="footer"><div class="container"><div class="footer-grid">
<div><img src="/images/acg-logo-nav@2x.png" alt="ACG" style="height:36px;width:auto;margin-bottom:16px;"></div>
<div><h4>Services</h4><ul><li><a href="/folding-glass-walls-florida/">Folding Glass Walls</a></li><li><a href="/multi-slide-doors-florida/">Multi-Slide Doors</a></li><li><a href="/curtainwall-installation.html">Curtain Wall</a></li></ul></div>
<div><h4>Resources</h4><ul><li><a href="/resources/">Glossary &amp; FAQ</a></li><li><a href="/tools/">Free Tools</a></li></ul></div>
<div><h4>Contact</h4><p style="color:rgba(255,255,255,0.6);font-size:14px;line-height:1.8;">(772) 486-7711<br>info@acglass.com</p></div>
</div></div></footer>'''

LOCALBIZ_SCHEMA = '''{"@context":"https://schema.org","@type":"GeneralContractor","@id":"https://acglass.com/#org","name":"American Commercial Glass","url":"https://acglass.com","telephone":"+1-772-486-7711","email":"info@acglass.com","address":{"@type":"PostalAddress","streetAddress":"1601 N Flagler Dr Ste 100","addressLocality":"West Palm Beach","addressRegion":"FL","postalCode":"33401","addressCountry":"US"},"geo":{"@type":"GeoCoordinates","latitude":26.7153,"longitude":-80.0534},"areaServed":[{"@type":"State","name":"Florida"},{"@type":"State","name":"Tennessee"}]}'''


def page(title, description, body_html, slug, extra_schema=None, breadcrumb=None, faq=None):
    bc = breadcrumb or []
    bc_json = ""
    if bc:
        items = [{"@type":"ListItem","position":i+1,"name":n,"item":u} for i,(n,u) in enumerate(bc)]
        bc_json = ',\n' + json.dumps({"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":items})
    faq_json = ""
    if faq:
        faq_json = ',\n' + json.dumps({"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in faq]})
    extra = ',\n' + extra_schema if extra_schema else ""
    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{html_lib.escape(title)}</title>
<meta name="description" content="{html_lib.escape(description)}">
<link rel="canonical" href="https://acglass.com/{slug}/">
<meta property="og:title" content="{html_lib.escape(title)}">
<meta property="og:description" content="{html_lib.escape(description)}">
<meta property="og:url" content="https://acglass.com/{slug}/">
<meta property="og:type" content="article">
{FONTS}
{GTAG}
<script type="application/ld+json">
[
{LOCALBIZ_SCHEMA}{extra}{bc_json}{faq_json}
]
</script>
</head>
<body>
{NAV}
<main class="page-main" style="padding-top:100px;">
<div class="container" style="max-width:980px;padding:60px 24px 100px;">
{body_html}
</div>
</main>
{FOOTER}
</body></html>'''
    out_dir = os.path.join(OUT, slug)
    os.makedirs(out_dir, exist_ok=True)
    with open(os.path.join(out_dir, "index.html"), "w") as f:
        f.write(html)
    print(f"  Wrote /{slug}/index.html")


# =============== 4 LONG-FORM BLOG ARTICLES (placed as /blog-2026/<slug>/) ===============
LONG_ARTICLES = [
    {
        "slug": "florida-impact-glass-cost-guide-2026",
        "title": "Florida Impact Glass Cost Guide 2026 — Commercial Building Edition",
        "description": "Per-square-foot pricing benchmarks for Florida commercial impact glass: storefront, curtain wall, punched openings, and HVHZ-rated assemblies. Updated for 2026 material costs.",
        "intro": "We get asked one question more than any other: what does commercial impact glass actually cost per square foot in Florida? Here is the 2026 answer, segmented by glass assembly type and AHJ region.",
        "sections": [
            ("What 'impact glass' actually means in Florida commercial context", "Commercial impact glass in Florida means laminated glass tested to Florida Building Code 1626 (cyclic pressure) and ASTM E1996/E1886 (large missile impact). HVHZ markets (Miami-Dade, Broward) additionally require Miami-Dade NOA approval. Outside HVHZ, FL Product Approval (FBC) is sufficient. Standard interlayer is 0.090 inch PVB; SGP (SentryGlas Plus) is the premium upgrade used on hurricane shutters, balcony rails, and structural applications."),
            ("Per-square-foot pricing — storefront impact systems", "Aluminum storefront impact-rated (Kawneer Trifab VG 451, YKK AP YES 45 IG, Tubelite T14000) with 9/16 inch laminated impact glass and standard kynar paint runs $95-145/sq ft installed in 2026. Drivers: HVHZ vs FBC, glass thickness, anchor density, and anodized vs PVDF finish. Bid premium on Miami-Dade Product Control jobs adds 8-15% over Broward / Palm Beach for the same assembly."),
            ("Per-square-foot pricing — curtain wall impact systems", "Aluminum curtain wall impact-rated (Kawneer 1600 SS, YKK AP YHC 300 OG, EFCO 5600) with 1 inch insulating laminated unit runs $135-225/sq ft installed in 2026. Stick-built vs unitized matters: stick-built dominates Florida commercial under 80 feet, unitized for high-rise. Glass package (Solarban 70XL, Viracon VRE-67, low-iron) adds $8-18/sq ft."),
            ("Per-square-foot pricing — punched openings (impact windows)", "Single-hung, casement, fixed, and architectural punched windows in impact-rated aluminum or fiberglass run $85-165/sq ft installed in 2026 for commercial buildings. Wood frame impact windows are not commercial-grade in Florida and we don't quote them. ESWindows architectural series (we install) runs $115-180/sq ft installed for commercial residential."),
            ("What changes the price by 20-40%", "Five things: (1) HVHZ vs FBC — HVHZ adds 8-15%. (2) PVDF Kynar vs anodized vs powder coat — PVDF is +12-20%. (3) SGP vs PVB interlayer — SGP is +25-35% on glass line item. (4) Custom mullion sizes and project-specific extrusions — custom dies add $0.50-2.00/sq ft. (5) Crane required vs hand-set — crane-required scopes add $4-12/sq ft."),
            ("Material vs labor split in 2026", "Material is 60-72% of the line item on commercial impact glass installed cost. Labor is 22-30%. Sealants, anchors, accessories are 4-8%. Material cost has come down 8-12% from 2024 peaks (aluminum + interlayer normalization). Labor cost is up 6-9% YoY as commercial glaziers compete for shrinking commercial glazier headcount."),
            ("How owners and GCs should benchmark a bid", "If a glazier's storefront impact bid is below $90/sq ft installed, ask hard questions about anchor density, glass thickness, and whether they're carrying NOA-approved assembly or substituting. If above $160/sq ft installed, ask what's driving the premium — specialty finish, custom mullion, special glass package. The middle band is where qualified competitive bids should land."),
            ("Get a real 2026 quote", "We bid commercial impact glass scopes across Florida daily. Send us drawings and we'll come back inside 48 hours with a real number, not a per-square-foot estimate. We also flag the spec items that can be value-engineered without losing performance or warranty.")
        ],
        "faq": [
            ("What is the per-square-foot cost of commercial impact glass in Florida in 2026?", "Storefront impact runs $95-145/sq ft installed. Curtain wall impact runs $135-225/sq ft installed. Punched openings run $85-165/sq ft installed. HVHZ markets (Miami-Dade, Broward) add 8-15% over non-HVHZ Florida."),
            ("Why does HVHZ cost more than the rest of Florida?", "Miami-Dade Product Control NOA approval requires more documentation, tighter anchor specifications, and more frequent inspection. Plus the assemblies themselves are tested to higher performance criteria (cyclic pressure, large missile impact at higher energies)."),
            ("Is SGP interlayer worth the upgrade over PVB?", "On structural applications (balcony rails, point-supported glass, all-glass entrances) — yes. SGP is roughly 100x stiffer than PVB and retains more structural integrity after impact. On standard storefront and curtain wall, PVB at 0.090 inch typically meets code at lower cost.")
        ]
    },
    {
        "slug": "commercial-glazing-rfq-checklist-for-architects",
        "title": "The Commercial Glazing RFQ Checklist Every Florida Architect Should Use",
        "description": "What architects should include in a commercial glazing request for quote to get accurate, comparable bids from Florida commercial glaziers. Built from 350+ projects of pattern recognition.",
        "intro": "We bid roughly 200 commercial glazing projects per year. About a third arrive with incomplete RFQ packages that force us to estimate scope, ask follow-up questions, and submit conditional bids. Here's the RFQ checklist that gets architects accurate, comparable, fast bids.",
        "sections": [
            ("Drawings — what we actually need", "Storefront elevations with glass type called out. Door schedule (single, double, automatic operator, hardware). Curtain wall sections (mullion depth, glass thickness, IGU configuration). Detail sections at head, sill, jamb. Anchor conditions (slab edge, concrete masonry, steel). Most architects send elevations and floor plans only. Without sections and details, we estimate anchor labor and miss things."),
            ("Glass spec — call out the actual product or the performance criteria", "Specify Solarban 70XL low-E, Viracon VRE-67, SentryGlas Plus interlayer at 0.090 inch — actual products. Or specify SHGC ≤ 0.27, VLT ≥ 0.55, U-factor ≤ 0.32, laminated impact-rated per FBC 1626 — actual performance criteria. Do not specify 'high-performance low-E' without numbers; we'll have to guess what you mean and our guess might not match the next glazier's guess."),
            ("Aluminum system spec — Kawneer or approved equal", "Spec Kawneer Trifab VG 451 with 9/16 IG and 2.25 inch mullion, OR call for 'aluminum thermal storefront system, 2.25 inch sightline mullion, kynar finish, approved equal acceptable.' The 'approved equal' opens YKK AP YES 45 IG and Tubelite T14000 — both qualify and typically save 8-15% on the storefront line item."),
            ("AHJ and permit pathway", "Tell us the AHJ. 'Miami-Dade NOA required' is different from 'Broward NOA acceptable' is different from 'FL Product Approval.' The submittal package complexity doubles between FBC and HVHZ. Architects who don't tell us the AHJ get bids that may not include the right NOA/Product Approval documentation."),
            ("Schedule — when do you need substantial completion", "If you need substantial completion in 90 days from contract, tell us. We may need to reroute material orders, source from in-stock inventory, or qualify alternate manufacturers. The bid changes. If you need it in 180 days, we can engineer to spec and source the right material. Both are buildable; pricing differs."),
            ("Warranty expectations", "Manufacturer warranty (Solarban 10-year, YKK AP 5-year aluminum) plus installer warranty (we offer 2-year labor standard, 5-year extended on commercial). Tell us if you need 10-year extended installer warranty — it changes the bid price. Architects who don't ask get standard. Architects who ask get a real number."),
            ("Commissioning and field testing requirements", "Field water testing per ASTM E1105? AAMA 502 testing? Air infiltration testing? These add 1-3% to the bid. We need to know in advance to subcontract testing. Architects who add them after award get change orders."),
            ("Send-us-plans pathway", "We accept RFQ packages at info@acglass.com or via our send-plans intake. Standard turnaround is 48 hours for commercial bids on complete packages. Incomplete packages get a clarification-question email within 24 hours. We don't disappear — we either bid or we tell you we're declining inside 48 hours.")
        ],
        "faq": [
            ("How long does a Florida commercial glazier need to return a bid?", "On a complete RFQ package (drawings + spec + AHJ + schedule), 48 hours is fast and 7 business days is typical. Florida market average is 7-15 business days. ACG averages 48 hours for routine commercial scopes."),
            ("What's the most common mistake architects make on commercial glazing RFQs?", "Specifying 'high-performance low-E' without performance numbers. This forces every bidder to guess the glass package and produces non-comparable bids. Always include either the specific product (Solarban 70XL, Viracon VRE-67) or the performance criteria (SHGC, VLT, U-factor)."),
            ("Should the RFQ allow 'approved equal' on aluminum systems?", "Almost always yes. Kawneer is the default spec; YKK AP and Tubelite often qualify as approved equal and save 8-15%. Owners benefit from the cost savings; architects keep design intent intact through the approved-equal review process.")
        ]
    },
    {
        "slug": "what-general-contractors-look-for-in-commercial-glaziers",
        "title": "What General Contractors Actually Look For in a Commercial Glazier (Beyond Price)",
        "description": "Inside view from a commercial glazier on what GCs really evaluate when selecting glazing subcontractors for Florida commercial projects. Response time, submittal completeness, and field performance.",
        "intro": "GCs do not pick the lowest bidder. We win bids at 8-12% above the low bid every week. Here is what GCs actually evaluate when they pick a commercial glazier — and what most glaziers get wrong.",
        "sections": [
            ("Response time on the initial bid", "GCs send drawings to 4-7 glaziers. The first 2 to respond with complete bids set the floor. The next 2 might still be looked at. The last 2-3 are usually ignored. We respond to commercial bid requests inside 48 hours. The Florida commercial glazier average is 7-15 days. That speed alone moves us into the 'serious contender' pile on every bid."),
            ("Submittal completeness on the first round", "After award, the submittal package is the second selection criterion. Complete on first submission means shop drawings + product data + NOA/Product Approval documentation + structural calcs + sealant compatibility letters in one package. Incomplete first submissions cost the GC 2-3 weeks of schedule and prove the glazier is not field-ready."),
            ("Field crew quality and OSHA discipline", "GCs walk the field daily. A glazing crew that wears proper PPE, hot-works permits when required, sets up safety per-section, and doesn't leave debris and cigarette butts is a crew the GC will hire again. The opposite gets debriefed at the post-project review and not invited to bid the next job."),
            ("Communication frequency and quality", "We send weekly look-ahead schedules every Friday. We respond to RFIs inside 24 hours on commercial scopes. We don't go dark for 3-5 days. GCs notice. We've been added to bid lists specifically because of our communication frequency — we make their job easier."),
            ("Punch list responsiveness at substantial completion", "Most glazing punch lists are sealant joints, gasket alignment, hardware adjustment, and minor glass scratches. Address them inside 5 business days. We have crews dedicated to punch turnaround. GCs who finish projects on schedule have glaziers who finish punch on schedule."),
            ("Warranty service after substantial completion", "Year-one warranty calls happen. The question is whether the glazier shows up. We have a documented 5-day response on warranty service. Glaziers who ghost after substantial completion get exactly one project from each GC, then they're out."),
            ("Project-type specialty", "Restaurant glaziers and hospital curtain wall glaziers are different specialties. School punched-opening glazier and luxury residential balcony rail glazier are different specialties. GCs notice when a glazier has done their specific project type 5+ times recently. Specialty matters."),
            ("Financial stability and bonding capacity", "On commercial projects over $250K, GCs check bonding capacity. On projects over $1M, they verify it. On AIA G706 or sworn statement workflows, they verify lien waivers. A glazier who doesn't bond, doesn't carry $2M general liability, and doesn't have a CFO function gets cut from larger bid lists.")
        ],
        "faq": [
            ("How long does a commercial glazier have to return a GC bid request to be competitive?", "48 hours is fast and wins more bids. 7 business days is the Florida market average and lands you in the middle of the pile. Longer than 10 days and most GCs have already selected from earlier bidders."),
            ("Why don't GCs always pick the lowest bidder on commercial glazing?", "Because the lowest bidder often has the worst submittal package, the longest material lead time, the spottiest crew discipline, and the slowest warranty response. GCs have been burned by lowest bidders before. Reliability is worth 8-12% premium on commercial glazing scopes."),
            ("What's the single biggest reason a commercial glazier gets dropped from a GC's bid list?", "Going dark mid-project. Not responding to RFIs for a week. Not showing up to coordination meetings. Not turning around shop drawings on schedule. Once a glazier costs a GC two weeks of schedule on a project, they don't get invited back.")
        ]
    },
    {
        "slug": "florida-commercial-glazing-warranty-explained",
        "title": "Florida Commercial Glazing Warranty Explained — Manufacturer vs Installer Coverage",
        "description": "Manufacturer vs installer warranty on Florida commercial glass: what's covered, what isn't, and how to enforce. Covers Solarban, Viracon, Kawneer, YKK AP, sealant warranties.",
        "intro": "Commercial glazing warranty is a stack — manufacturer + installer + product-specific — and most owners don't know which warranty covers what. This is the practical breakdown.",
        "sections": [
            ("Manufacturer warranty layer 1 — glass", "Glass manufacturer warranty covers the glass itself: edge seal failure on insulating units, low-E coating defects, lamination delamination. Solarban (Vitro) IGU warranty: 10 years on seal failure. Viracon IGU warranty: 10 years. Lamination warranty: 5 years standard, 10 years with SGP upgrade. Glass warranty does NOT cover installation defects, sealant failure, or breakage."),
            ("Manufacturer warranty layer 2 — aluminum system", "Aluminum framing manufacturer warranty (Kawneer, YKK AP, Tubelite, EFCO) covers extrusion finish (PVDF Kynar 70/30 or Kynar 500, anodized class I/II, powder coat) typically 5-10 years against fade, chalk, peel, and adhesion failure. Aluminum substrate warranty is generally lifetime on the structural extrusion itself. Hardware (operators, locks, hinges) is typically 1-3 years."),
            ("Installer warranty — labor and installation defects", "Installer warranty covers installation workmanship: anchor performance, sealant joint, flashing, weatherstripping integration. Florida commercial glazier standard is 1-2 years on labor. ACG standard is 2 years; extended 5-year available on commercial scopes. Installer warranty does NOT cover acts of God, building structural movement beyond design, or owner-caused damage."),
            ("Sealant warranty — the often-forgotten layer", "Structural sealant (Dow Corning 995, Sika SikaSil WS-305) carries manufacturer warranty 10-20 years when applied per spec by a Dow- or Sika-approved applicator. Weatherseal sealants are typically 5-year manufacturer warranty. ACG is an approved applicator for both Dow and Sika commercial sealant lines."),
            ("What voids commercial glazing warranties — most common", "Owner-side power washing with non-approved chemicals (citrus-based, ammoniated). HVAC overspray reaching sealant joints. Building settlement beyond design tolerance. Tinted film applied after installation (voids low-E coating warranty almost universally). Modification of frame for tenant signage without manufacturer approval."),
            ("Enforcement — how owners actually claim warranty", "Document the defect with photos and date. Contact the installer first within 60 days of discovery. Installer triages — installation defect vs material defect. If material defect, installer files claim with manufacturer and coordinates remediation. If installer is non-responsive, owner contacts manufacturer directly with installer's contact info and copy of original purchase. Manufacturer-direct claims work but slower."),
            ("ACG warranty service standard", "5-day response on all warranty calls. 10-day site visit for inspection. Remediation scope and timeline issued within 5 days of inspection. Most warranty issues resolved within 30-45 days of initial call. Documented in our service tracking system; reported to owner monthly until closed."),
            ("Recommended owner warranty file at substantial completion", "Manufacturer certificates (glass, aluminum, sealant, hardware). NOA documentation if HVHZ. Shop drawings as-built. Installer warranty letter on company letterhead with project address and warranty term. Sealant applicator certification. Punch list signoff with dates. Annual cleaning specification document. Owner who has this file enforces warranty 3x faster than owner who has to reconstruct it.")
        ],
        "faq": [
            ("How long is the typical commercial glazing warranty in Florida?", "Glass manufacturer: 10 years on IGU seal failure, 5-10 years on lamination. Aluminum manufacturer: 5-10 years on finish. Installer labor: 1-2 years standard, 5 years on extended commercial. Sealant: 10-20 years on structural, 5 years on weatherseal."),
            ("What's the most common cause of commercial glass warranty claims?", "IGU edge seal failure (typically years 7-12 on standard low-E units) and sealant joint failure (typically years 3-7 if installed poorly, years 10-15 if installed correctly). Glass breakage from impact is not a warranty claim — it's an insurance or owner-replacement event."),
            ("Does the installer warranty travel with the building if ownership changes?", "Yes, on commercial glazing. ACG installer warranty is transferable to subsequent owners within the warranty term with documentation. Manufacturer warranties on glass, aluminum, and sealant are also transferable.")
        ]
    },
]

# =============== 12 MORE VERTICAL × CITY PAGES ===============
VERTICAL_CITY = [
    ("Bar &amp; Brewery", "bar-brewery-glazing", "Miami", "miami", "bar and brewery glazing in Miami, including folding storefronts, sliding glass walls, and impact-rated windows for South Beach, Wynwood, and Brickell venues"),
    ("Bar &amp; Brewery", "bar-brewery-glazing", "Tampa", "tampa", "bar and brewery glazing in Tampa, including folding storefronts, multi-slide doors, and impact windows for Ybor City, Riverwalk, and SoHo venues"),
    ("Bar &amp; Brewery", "bar-brewery-glazing", "Orlando", "orlando", "bar and brewery glazing in Orlando, including folding storefronts and sliding glass walls for Mills 50, Thornton Park, and Winter Park venues"),
    ("Country Club", "country-club-glazing", "Naples", "naples", "country club glazing in Naples, including full-height curtain walls, balcony rails, and folding storefronts for ballrooms, dining rooms, and golf clubhouses"),
    ("Country Club", "country-club-glazing", "Palm Beach", "palm-beach", "country club glazing in Palm Beach, including full-height curtain walls, balcony rails, and folding storefronts for clubhouses across the island"),
    ("Country Club", "country-club-glazing", "Boca Raton", "boca-raton", "country club glazing in Boca Raton, including full-height curtain walls, balcony rails, and folding storefronts for established Boca clubhouses"),
    ("Government &amp; Municipal", "government-municipal-glazing", "Tallahassee", "tallahassee", "government and municipal glazing in Tallahassee, including curtain wall, security glazing, and impact-rated assemblies for state and local government buildings"),
    ("Government &amp; Municipal", "government-municipal-glazing", "Miami", "miami", "government and municipal glazing in Miami, including HVHZ-rated curtain wall and security glazing for Miami-Dade county and city facilities"),
    ("Marina", "marina-glazing", "Miami Beach", "miami-beach", "marina and waterfront restaurant glazing in Miami Beach, including all-glass entrances, folding storefronts, and HVHZ-rated impact assemblies"),
    ("Marina", "marina-glazing", "Naples", "naples", "marina and waterfront restaurant glazing in Naples, including all-glass entrances, folding storefronts, and curtain wall at the bay"),
    ("Showroom", "showroom-glazing", "Miami", "miami", "automotive and luxury showroom glazing in Miami, including full-height curtain walls, structural silicone, and architectural storefronts"),
    ("Showroom", "showroom-glazing", "Naples", "naples", "automotive and luxury showroom glazing in Naples, including full-height curtain walls, structural silicone, and architectural storefronts on Pine Ridge and Tamiami Trail"),
]

# =============== 6 MORE AIO FAQ PAGES ===============
AIO_FAQ = [
    ("how-much-does-curtain-wall-cost-per-square-foot", "How much does curtain wall cost per square foot in Florida 2026?",
     "Aluminum curtain wall installed cost in Florida 2026 averages $135-225 per square foot for impact-rated commercial systems with 1 inch insulating laminated glass. HVHZ markets (Miami-Dade, Broward) add 8-15% over non-HVHZ Florida.",
     [
       ("What's included in $135-225/sq ft curtain wall pricing?", "Aluminum framing (Kawneer 1600 SS, YKK AP YHC 300 OG, or EFCO 5600), 1 inch insulating laminated glass with low-E coating, structural anchors, sealants, weatherstripping, and standard PVDF kynar finish. Installation labor and standard warranty included. Glass package upgrades (Solarban 70XL, Viracon VRE-67) add $8-18/sq ft."),
       ("Why is HVHZ curtain wall more expensive than other Florida regions?", "Miami-Dade NOA approval requires tighter anchor specifications, more frequent inspection, and additional documentation. Plus assemblies are tested to higher cyclic pressure and large missile impact criteria. Net impact: 8-15% premium over the same assembly outside HVHZ."),
       ("What's the difference between stick-built and unitized curtain wall pricing?", "Stick-built dominates Florida commercial under 80 feet and runs at the lower end of the $135-225 band. Unitized curtain wall is panelized off-site and runs at the upper end — $185-260/sq ft installed — but installs 3-5x faster on high-rise construction. Florida hotel and condo high-rises increasingly spec unitized.")
     ]),
    ("how-long-does-commercial-glazing-take-to-install", "How long does commercial glazing take to install on a Florida commercial project?",
     "Commercial glazing install duration runs 8-16 weeks for restaurant and retail, 12-22 weeks for hotel and medical office, 16-32 weeks for office building, and 6-10 months for high-rise. Material lead time is 60-80% of the total timeline; field install is 20-40%.",
     [
       ("What drives the 60-80% material lead time?", "Aluminum extrusions: 3-5 weeks for stock profiles, 8-12 weeks for custom dies. Laminated impact glass: 4-10 weeks depending on coating, interlayer, and tempering. Custom PVDF finishes: 8-12 weeks. Hardware: 2-6 weeks. The longest lead-time item sets the schedule."),
       ("What's the fastest a commercial glazing install can actually move?", "Restaurant tenant improvement with stock storefront and in-stock glass — 6-8 weeks total from contract to substantial completion. Hotel curtain wall with custom mullion, custom finish, custom glass — 10-14 months. Most commercial work falls in the 12-22 week range."),
       ("How do we shorten commercial glazing schedule?", "Order material on signed contract, not on permit issuance — saves 2-3 weeks. Submit complete first-round submittal package — saves 2-3 weeks. Specify stock extrusions and approved-equal aluminum systems — saves 4-6 weeks on custom dies. Lock glass spec early — saves 2-4 weeks of substitution drama.")
     ]),
    ("what-is-the-warranty-on-commercial-glass", "What is the standard warranty on commercial glass and glazing in Florida?",
     "Florida commercial glazing carries layered warranties: glass manufacturer 10 years on IGU seal failure, aluminum manufacturer 5-10 years on finish, installer labor 1-2 years standard (5 years extended), sealant 10-20 years on structural and 5 years on weatherseal.",
     [
       ("What's the typical installer labor warranty in Florida?", "1-2 years is the Florida commercial glazier average. ACG offers 2-year labor standard and 5-year extended on commercial scopes. Some specialty work (all-glass entrances, structural silicone) may carry shorter installer warranty due to higher exposure."),
       ("Does the warranty transfer if the building changes ownership?", "Yes. ACG installer warranty transfers with documentation. Manufacturer warranties on glass (Vitro, Viracon, Guardian), aluminum (Kawneer, YKK AP), and sealant (Dow Corning, Sika) are also transferable to subsequent owners within the warranty term."),
       ("What voids commercial glazing warranty?", "Owner-side power washing with non-approved chemicals (citrus-based, ammoniated). HVAC overspray reaching sealant joints. Tinted film applied after installation (voids low-E coating warranty almost universally). Modification of frame for tenant signage without manufacturer approval. Building settlement beyond design tolerance.")
     ]),
    ("can-you-install-glass-on-occupied-buildings", "Can a commercial glazier install glass on an occupied building in Florida?",
     "Yes — occupied building glazing is a defined commercial glazing specialty in Florida. Scope-by-scope phased install, after-hours and weekend work, temporary weather protection between removal and reinstall, and noise/dust mitigation are standard for retrofit and re-glaze projects.",
     [
       ("What occupied-building glazing scopes are common in Florida?", "Hotel curtain wall reskin during partial occupancy. Office building IGU replacement floor-by-floor. Restaurant storefront replacement during off-hours (10pm-6am). Medical office punched-opening replacement room-by-room. School re-glaze during summer break. Each has its own phasing protocol."),
       ("How does after-hours occupied-building work affect commercial glazing pricing?", "Premium time labor (1.5x-2x standard rates) adds 15-30% to the labor line item. Temporary protection (Visqueen, plywood, scaffold weather screen) adds $4-12/sq ft. Crew break-down and re-setup nightly adds 5-10% to labor productivity loss. Net: 20-40% premium over new-construction install."),
       ("What protections do tenants need during occupied-building glazing?", "Negative-pressure containment for indoor air quality. Weather protection during open-frame periods (rain, wind). Acoustic dampening on chiseling and rebar cutting. Dust mitigation for HVAC return air. Egress maintained at all times per Florida Fire Prevention Code. Documented in pre-construction occupied building plan and submitted to property manager.")
     ]),
    ("what-is-the-best-aluminum-storefront-system", "What is the best aluminum storefront system for Florida commercial buildings in 2026?",
     "The best aluminum storefront for Florida commercial is the one that meets project criteria — HVHZ rating, glass thickness, mullion sightline, finish, schedule, and budget. Kawneer Trifab VG 451, YKK AP YES 45 IG, and Tubelite T14000 are the three dominant commercial-grade impact-rated storefronts in Florida.",
     [
       ("Kawneer vs YKK AP vs Tubelite — what's the practical difference?", "Kawneer is the architect-default spec — broadest part library, deepest project history. YKK AP often qualifies as approved equal and saves 8-15% on the storefront line item with comparable performance. Tubelite is the third major qualifier — competitive on stock profiles, sometimes longer lead time on custom dies. All three carry HVHZ NOAs."),
       ("Which aluminum storefront has the best Florida HVHZ approval breadth?", "Kawneer carries the most extensive Miami-Dade NOA portfolio across Trifab VG 451, Trifab 451UT, and 1600 SS Series. YKK AP YES 45 IG and YHC 300 OG carry full HVHZ approval. Tubelite T14000 carries HVHZ on most assemblies. All three are HVHZ-qualified for typical commercial scopes."),
       ("Does specifying 'approved equal' actually save the owner money?", "Almost always yes. On a $200K storefront line item, approved-equal qualification often saves $15K-30K. The architect maintains design intent through the approved-equal review process. The owner gets the cost savings. The glazier (us, in many cases) brings the qualification.")
     ]),
    ("what-glazing-permit-is-required-in-florida", "What permit is required for commercial glazing work in Florida?",
     "Commercial glazing in Florida requires a building permit (typically from the local AHJ — city or county) plus Florida Product Approval (FBC) documentation, or Miami-Dade NOA documentation in HVHZ markets. The general contractor or specialty glazing contractor pulls the permit.",
     [
       ("What does the AHJ check on a Florida commercial glazing permit?", "Florida Building Code 1626 compliance (impact and cyclic pressure on impact-rated assemblies), Energy Code compliance (U-factor, SHGC), structural anchorage (engineer-of-record sealed calcs), code-required egress and life safety, and ADA compliance on door hardware and reach."),
       ("How long does AHJ permit approval take in Florida?", "Miami-Dade: 15-25 days on complete submittal. Broward: 12-22 days. Palm Beach: 10-18 days. Orange County: 7-12 days. Hillsborough: 10-15 days. Duval (Jacksonville): 8-14 days. Cycle time depends on submittal completeness — incomplete first submissions get bounced and add 2-3 weeks."),
       ("Does residential vs commercial glazing change the permit pathway?", "Yes. Commercial glazing falls under FBC Building (not FBC Residential), requires engineer-of-record sealed shop drawings, and typically requires more documentation. Commercial scopes over certain thresholds also require licensed glazing contractor (CC-C credential) — not all Florida glazing contractors carry it.")
     ])
]


def build_blog_articles():
    for art in LONG_ARTICLES:
        slug = "blog-2026/" + art["slug"]
        body = f'<header style="margin-bottom:40px;"><p style="color:#e11320;font-weight:600;text-transform:uppercase;letter-spacing:1px;font-size:13px;margin-bottom:12px;">ACG Blog</p><h1 style="font-size:42px;line-height:1.15;font-weight:800;margin-bottom:20px;color:#050a12;">{html_lib.escape(art["title"])}</h1><p style="color:#5a6473;font-size:18px;line-height:1.6;margin-bottom:8px;">{html_lib.escape(art["description"])}</p><p style="color:#9099a8;font-size:14px;">By Connor Walsh, President — American Commercial Glass · May 23, 2026 · 8-12 minute read</p></header>'
        body += f'<p style="font-size:19px;line-height:1.7;color:#1f2937;margin-bottom:32px;font-weight:500;">{html_lib.escape(art["intro"])}</p>'
        for h, p in art["sections"]:
            body += f'<h2 style="font-size:28px;margin-top:40px;margin-bottom:16px;color:#050a12;font-weight:700;">{h}</h2>'
            body += f'<p style="font-size:17px;line-height:1.75;color:#1f2937;margin-bottom:24px;">{p}</p>'
        body += '<div style="background:#0e284f;color:white;padding:32px;border-radius:12px;margin-top:48px;text-align:center;"><h3 style="font-size:24px;margin-bottom:12px;">Need a commercial glazing bid?</h3><p style="margin-bottom:20px;opacity:0.9;">Send us drawings and we\'ll come back inside 48 hours with a real number.</p><a href="/send-plans.html" style="background:#e11320;color:white;padding:14px 28px;border-radius:6px;text-decoration:none;font-weight:600;display:inline-block;">Send Us Plans</a></div>'

        article_schema = json.dumps({"@context":"https://schema.org","@type":"BlogPosting","headline":art["title"],"description":art["description"],"author":{"@type":"Person","name":"Connor Walsh","url":"https://acglass.com/author-connor-walsh/"},"datePublished":"2026-05-23","publisher":{"@type":"Organization","name":"American Commercial Glass","logo":{"@type":"ImageObject","url":"https://acglass.com/images/acg-logo-nav@2x.png"}},"mainEntityOfPage":{"@type":"WebPage","@id":f"https://acglass.com/{slug}/"}})

        page(art["title"], art["description"], body, slug,
             extra_schema=article_schema,
             breadcrumb=[("Home","https://acglass.com/"),("Blog","https://acglass.com/blog.html"),(art["title"], f"https://acglass.com/{slug}/")],
             faq=art.get("faq"))


def build_vertical_city():
    for vertical_name, vertical_slug, city_name, city_slug, intent_text in VERTICAL_CITY:
        slug = f"{vertical_slug}-{city_slug}"
        title = f"{vertical_name.replace('&amp;','&')} Glazing {city_name} — ACG Commercial Glazier"
        desc = f"{vertical_name.replace('&amp;','&')} commercial glazing in {city_name}, Florida — ACG installs {intent_text}."
        body = f'''<header><p style="color:#e11320;font-weight:600;font-size:13px;letter-spacing:1px;text-transform:uppercase;margin-bottom:12px;">{vertical_name} Glazing</p><h1 style="font-size:42px;line-height:1.15;font-weight:800;margin-bottom:16px;color:#050a12;">{vertical_name.replace('&amp;','&')} Glazing in {city_name}, Florida</h1><p style="font-size:19px;line-height:1.7;color:#5a6473;">ACG installs {intent_text}.</p></header>
<section style="margin-top:48px;">
<h2 style="font-size:28px;color:#050a12;margin-bottom:16px;">What we install for {vertical_name.replace('&amp;','&').lower()} clients in {city_name}</h2>
<ul style="font-size:17px;line-height:2;color:#1f2937;list-style:none;padding:0;">
<li>✓ Impact-rated storefront aluminum systems (Kawneer Trifab VG 451, YKK AP YES 45 IG, Tubelite T14000)</li>
<li>✓ Folding glass walls and multi-slide doors (Euro-Wall, NanaWall, LaCantina)</li>
<li>✓ Curtain wall and full-height architectural glazing (Kawneer 1600 SS, YKK AP YHC 300 OG)</li>
<li>✓ All-glass entrance doors with structural patch fittings (Dorma, CRL)</li>
<li>✓ Balcony rail and stair rail glass (laminated SGP)</li>
<li>✓ Impact-rated punched windows (ESWindows architectural series)</li>
</ul>
</section>
<section style="margin-top:48px;background:#f8f9fb;padding:32px;border-radius:12px;">
<h2 style="font-size:24px;color:#050a12;margin-bottom:12px;">Why {vertical_name.replace('&amp;','&').lower()} clients choose ACG in {city_name}</h2>
<p style="font-size:17px;line-height:1.7;color:#1f2937;">350+ Florida commercial projects. 48-hour bid turnaround on standard commercial scopes. HVHZ-experienced when {city_name} requires it. Direct manufacturer relationships with Kawneer, YKK AP, Tubelite, ESWindows, and Euro-Wall. Licensed commercial glazing contractor with statewide coverage.</p>
</section>
<section style="margin-top:48px;text-align:center;background:#0e284f;color:white;padding:48px 32px;border-radius:12px;">
<h2 style="font-size:30px;margin-bottom:16px;">Send us drawings — we'll bid your {city_name} project in 48 hours</h2>
<p style="font-size:17px;opacity:0.9;margin-bottom:24px;">{vertical_name.replace('&amp;','&')} glazing in {city_name}, Florida. Real number, fast.</p>
<a href="/send-plans.html" style="background:#e11320;color:white;padding:16px 32px;border-radius:6px;text-decoration:none;font-weight:600;font-size:17px;display:inline-block;">Send Us Plans</a>
</section>'''

        service_schema = json.dumps({"@context":"https://schema.org","@type":"Service","name":f"{vertical_name.replace('&amp;','&')} Glazing in {city_name}, FL","provider":{"@type":"GeneralContractor","name":"American Commercial Glass","@id":"https://acglass.com/#org"},"areaServed":{"@type":"City","name":city_name,"containedInPlace":{"@type":"State","name":"Florida"}},"serviceType":"Commercial Glazing"})

        page(title, desc, body, slug,
             extra_schema=service_schema,
             breadcrumb=[("Home","https://acglass.com/"),("Service Areas","https://acglass.com/service-areas-map/"),(city_name, f"https://acglass.com/{city_slug}/"),(f"{vertical_name.replace('&amp;','&')} Glazing", f"https://acglass.com/{slug}/")])


def build_aio_faq():
    for slug, q, intro, faq in AIO_FAQ:
        title = f"{q} — ACG Commercial Glazier"
        desc = intro
        body = f'<header><p style="color:#e11320;font-weight:600;font-size:13px;letter-spacing:1px;text-transform:uppercase;margin-bottom:12px;">Florida Commercial Glazing FAQ</p><h1 style="font-size:36px;line-height:1.2;font-weight:800;margin-bottom:20px;color:#050a12;">{html_lib.escape(q)}</h1><p style="font-size:19px;line-height:1.7;color:#1f2937;font-weight:500;">{html_lib.escape(intro)}</p></header><section style="margin-top:48px;">'
        for qq, aa in faq:
            body += f'<h2 style="font-size:24px;color:#050a12;margin-top:32px;margin-bottom:12px;font-weight:700;">{html_lib.escape(qq)}</h2><p style="font-size:17px;line-height:1.75;color:#1f2937;">{html_lib.escape(aa)}</p>'
        body += '</section><div style="background:#0e284f;color:white;padding:32px;border-radius:12px;margin-top:48px;text-align:center;"><h3 style="font-size:24px;margin-bottom:12px;">Need a Florida commercial glazing bid?</h3><a href="/send-plans.html" style="background:#e11320;color:white;padding:14px 28px;border-radius:6px;text-decoration:none;font-weight:600;display:inline-block;">Send Us Plans</a></div>'

        # Speakable schema for voice search
        speakable_schema = json.dumps({"@context":"https://schema.org","@type":"WebPage","speakable":{"@type":"SpeakableSpecification","cssSelector":["h1","h2","p"]},"url":f"https://acglass.com/{slug}/"})

        page(title, desc, body, slug,
             extra_schema=speakable_schema,
             breadcrumb=[("Home","https://acglass.com/"),("FAQ","https://acglass.com/florida-glazing-faq/"),(q, f"https://acglass.com/{slug}/")],
             faq=faq)


if __name__ == "__main__":
    print("Building 4 long-form blog articles...")
    build_blog_articles()
    print("\nBuilding 12 vertical x city pages...")
    build_vertical_city()
    print("\nBuilding 6 more AIO FAQ pages...")
    build_aio_faq()
    print(f"\nWave 9 total: {len(LONG_ARTICLES) + len(VERTICAL_CITY) + len(AIO_FAQ)} pages")
