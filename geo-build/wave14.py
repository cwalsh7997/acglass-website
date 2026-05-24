#!/usr/bin/env python3
"""Wave 14 — High-intent gap-fill queries.
- 5 brand comparison pages (Kawneer vs YKK AP, Solarban vs Viracon, etc.)
- 5 emergency/specialty service pages
- 5 material spec deep-dives
- 4 industry buyer pages (REIT, hospitality dev, GC, owner-direct)
- 5 service modifier x city
Total: 24 pages. All claims from verified ACG standing list."""
import os, html as html_lib, json

OUT = "/home/user/workspace/acglass-website"

GTAG = '''<script async src="https://www.googletagmanager.com/gtag/js?id=G-M7BFQD2SPP"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}gtag("js",new Date());gtag("config","G-M7BFQD2SPP");</script>'''

FONTS = '<link rel="stylesheet" href="/css/style.css?v=1777031720"><link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">'

NAV = '''<nav class="nav scrolled"><div class="nav-inner">
<a href="/index.html" class="nav-logo"><img height="72" width="338" src="/images/acg-logo-nav@2x.png" style="height:36px;width:auto;" alt="ACG - American Commercial Glass" class="logo-img" loading="lazy"></a>
<div class="nav-links"><a href="/index.html">Home</a><a href="/blog.html">Blog</a><a href="/case-studies/">Case Studies</a><a href="/resources/">Resources</a><a href="/send-plans.html" class="nav-cta">Send Us Plans</a></div></div></nav>'''

FOOTER = '''<footer class="footer"><div class="container"><div class="footer-grid">
<div><img src="/images/acg-logo-nav@2x.png" alt="ACG" style="height:36px;width:auto;margin-bottom:16px;"></div>
<div><h4>Services</h4><ul><li><a href="/folding-glass-walls-florida/">Folding Glass Walls</a></li><li><a href="/multi-slide-doors-florida/">Multi-Slide Doors</a></li><li><a href="/curtainwall-installation.html">Curtain Wall</a></li></ul></div>
<div><h4>Resources</h4><ul><li><a href="/resources/">Glossary &amp; FAQ</a></li><li><a href="/tools/">Free Tools</a></li></ul></div>
<div><h4>Contact</h4><p style="color:rgba(255,255,255,0.6);font-size:14px;line-height:1.8;">(772) 486-7711<br>info@acglass.com</p></div>
</div></div></footer>'''

LOCALBIZ = '''{"@context":"https://schema.org","@type":"GeneralContractor","@id":"https://acglass.com/#org","name":"American Commercial Glass","url":"https://acglass.com","telephone":"+1-772-486-7711","email":"info@acglass.com","address":{"@type":"PostalAddress","streetAddress":"1601 N Flagler Dr Ste 100","addressLocality":"West Palm Beach","addressRegion":"FL","postalCode":"33401","addressCountry":"US"},"areaServed":[{"@type":"State","name":"Florida"},{"@type":"State","name":"Tennessee"}]}'''


def page(title, description, body_html, slug, faq=None, extra_schema=None, breadcrumb=None):
    bc_json = ""
    if breadcrumb:
        items = [{"@type":"ListItem","position":i+1,"name":n,"item":u} for i,(n,u) in enumerate(breadcrumb)]
        bc_json = ',\n' + json.dumps({"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":items})
    faq_json = ""
    if faq:
        faq_json = ',\n' + json.dumps({"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in faq]})
    extra = ',\n' + extra_schema if extra_schema else ""
    speakable_block = '<script type="application/ld+json">' + json.dumps({"@context":"https://schema.org","@type":"WebPage","speakable":{"@type":"SpeakableSpecification","cssSelector":["h1","h2","p"]},"url":f"https://acglass.com/{slug}/"}) + '</script>'

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
{FONTS}
{GTAG}
<script type="application/ld+json">
[
{LOCALBIZ}{extra}{bc_json}{faq_json}
]
</script>
{speakable_block}
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


# === 5 BRAND COMPARISONS ===
COMPARISONS = [
    ("kawneer-vs-ykk-ap-storefront-systems", "Kawneer vs YKK AP storefront systems \u2014 which is right for Florida commercial?",
     "Both Kawneer and YKK AP are tier-one commercial aluminum storefront manufacturers. Kawneer Trifab VG 451 is the architect-default in Florida commercial spec. YKK AP YES 45 IG often qualifies as approved-equal and saves 8-15% on the storefront line item. Both carry full HVHZ NOAs.",
     [
       ("What's the practical difference between Kawneer and YKK AP?", "Kawneer has the broadest part library and the deepest project history. YKK AP qualifies as approved-equal on most architect specs and saves 8-15% on bid pricing. Performance, finish, and warranty are functionally equivalent on the comparable product lines."),
       ("Which carries more Florida HVHZ approvals?", "Kawneer carries the most extensive Miami-Dade NOA portfolio (Trifab VG 451, Trifab 451UT, 1600 SS Series). YKK AP YES 45 IG and YHC 300 OG carry full HVHZ approval. Both are HVHZ-qualified for typical commercial scopes."),
       ("Does ACG install both?", "Yes. Direct manufacturer relationships with both. ACG bids the spec on the drawing and qualifies approved-equal where the architect's spec allows. Pricing decision typically goes to the lower-cost qualified alternate.")
     ]),
    ("solarban-vs-viracon-low-e-glass", "Solarban vs Viracon low-E glass \u2014 commercial spec comparison",
     "Solarban (Vitro) and Viracon are the dominant tier-one low-E coated glass manufacturers used in Florida commercial glazing. Solarban 70XL is the Florida default for hospitality and office. Viracon VRE-67 is the alternative \u2014 slightly higher VLT. Performance is comparable; spec selection depends on architect preference and project-specific SHGC/VLT/U-factor requirements.",
     [
       ("What's the performance difference between Solarban 70XL and Viracon VRE-67?", "Solarban 70XL: SHGC 0.27, VLT 0.64, U-factor 0.29 in 1\" IGU. Viracon VRE-67: SHGC 0.27, VLT 0.67, U-factor 0.29 in 1\" IGU. Functionally equivalent. The 3-point VLT difference is below the threshold most architects optimize against."),
       ("Are both warranted the same way?", "Yes. Both carry 10-year IGU edge seal warranty and 5-year low-E coating warranty under typical commercial specifications. Warranty transfers with documentation."),
       ("How much do they cost?", "Roughly comparable per square foot. The bid spread between Solarban 70XL and Viracon VRE-67 is typically less than 3% on the glass line item.")
     ]),
    ("pvb-vs-sgp-interlayer-comparison", "PVB vs SGP interlayer \u2014 when to specify each on Florida commercial glazing",
     "PVB (polyvinyl butyral) at 0.090 inch is the Florida commercial default for laminated impact glass and meets FBC 1626 for typical storefront and curtain wall scopes. SGP (SentryGlas Plus) is the structural-grade upgrade for balcony rails, all-glass entrances, hurricane shutter assemblies, and point-supported glass. SGP is roughly 100x stiffer than PVB.",
     [
       ("When do I need SGP instead of PVB?", "Structural applications. Balcony glass rails (where the glass acts as guardrail). All-glass entrance doors with structural patch fittings. Point-supported glass. Hurricane shutter assemblies. Any application where the interlayer's post-impact strength matters."),
       ("How much more does SGP cost than PVB?", "25-35% premium on the glass line item, depending on glass thickness and overall scope size. On a typical commercial storefront where PVB at 0.090 inch meets code, SGP is rarely the right value."),
       ("Does ACG install both?", "Yes. ACG installs both PVB-laminated and SGP-laminated assemblies daily. SGP specifically on balcony rail and all-glass entrance scopes.")
     ]),
    ("eswindows-vs-pgt-impact-windows", "ESWindows vs PGT impact windows \u2014 commercial Florida comparison",
     "ESWindows and PGT (PGT Industries) are both Florida-Product-Approval and Miami-Dade NOA qualified impact window manufacturers. ESWindows is the choice for architectural commercial (multifamily, hospitality, office) with premium aluminum profiles. PGT WinGuard line is broader residential-commercial-blend coverage with deeper distribution.",
     [
       ("Which is the better choice for commercial Florida projects?", "ESWindows for architectural commercial \u2014 multifamily, hospitality, office, healthcare \u2014 where premium aluminum profile, custom finish, and tighter sightlines matter. PGT for commercial-residential-blend projects where the project benefits from PGT's broader distribution network and faster lead-time on stock profiles."),
       ("What's the price difference?", "ESWindows typically commands a 5-12% premium over comparable PGT WinGuard products on commercial scopes. Worth it for architectural projects; not always worth it for tenant-improvement or commercial-residential-hybrid scopes."),
       ("Does ACG install both?", "Yes. ACG carries direct manufacturer relationships with ESWindows. PGT is sourced through distribution. We bid the spec and recommend the right product for the project type.")
     ]),
    ("kawneer-1600-vs-ykk-yhc-300-curtain-wall", "Kawneer 1600 SS vs YKK AP YHC 300 OG \u2014 commercial curtain wall comparison",
     "Both are tier-one aluminum stick-built curtain wall systems for Florida commercial projects. Kawneer 1600 SS is the broadest-deployed system with the deepest Miami-Dade NOA portfolio. YKK AP YHC 300 OG often qualifies as approved-equal and reduces curtain-wall line-item cost by 8-15% with equivalent performance.",
     [
       ("What's the practical specification difference?", "Both are 2.5\" deep stick-built curtain wall systems with thermal break, captured-glazing or structural-silicone glazing options, and full Miami-Dade NOA approval. Sightline, finish options, and accessory parts are functionally equivalent on the comparable product lines."),
       ("Which has the broader HVHZ approval?", "Kawneer 1600 SS Series has the most extensive Miami-Dade NOA portfolio. YKK AP YHC 300 OG carries full HVHZ approval on the standard configurations \u2014 sufficient for typical commercial curtain wall scopes."),
       ("Does ACG install both?", "Yes. ACG has installed both Kawneer 1600 SS and YKK AP YHC 300 OG curtain wall systems on Florida commercial projects. Direct manufacturer relationships with both.")
     ]),
]

# === 5 EMERGENCY/SPECIALTY SERVICE ===
EMERGENCY = [
    ("emergency-commercial-glass-repair-florida", "Emergency commercial glass repair Florida \u2014 24-hour response",
     "ACG provides emergency commercial glass repair across Florida \u2014 storefront breakage, IGU failure, vandalism, hurricane damage, and impact incidents. Response targets: 24 hours to site, 48 hours to permanent re-glaze. Florida-licensed (FL CGC #1531993), insured ($3M general liability), bonded ($6M aggregate).",
     [
       ("How fast does ACG respond to emergency commercial glass calls?", "24 hours to site with temporary board-up if required. 48 hours to permanent re-glaze on most commercial storefront scopes. Faster on simple IGU swaps; longer on custom curtain wall or HVHZ assemblies that require NOA-matched replacement glass."),
       ("Does ACG handle hurricane storm damage commercial glass?", "Yes. Post-storm commercial glass replacement across Florida HVHZ markets (Miami-Dade, Broward) and statewide. Insurance claims documentation included on request. Direct relationships with glass manufacturers shorten replacement lead times."),
       ("What's the cost of emergency commercial glass repair?", "Depends on scope. Temporary board-up: $400-$1,200 per opening. IGU replacement: $45-$95 per square foot installed for in-stock glass. Full storefront replacement: $95-$145 per square foot installed. After-hours premium typically adds 15-30% to labor.")
     ]),
    ("after-hours-commercial-glazing-installation-florida", "After-hours commercial glazing installation Florida \u2014 weekend and night work",
     "ACG performs after-hours, weekend, and overnight commercial glazing installation across Florida \u2014 retail tenant improvement during off-hours, hotel re-glaze during low-occupancy windows, hospital ICRA-compliant work, restaurant storefront replacement after dinner service. Premium labor typically adds 15-30% to line item; planned and bid up-front.",
     [
       ("What commercial scopes typically require after-hours install?", "Retail mall tenant improvement (after-hours per lease). Hotel re-glaze during low occupancy. Hospital and medical office (ICRA Class III/IV phased install). Restaurant storefront replacement after dinner service. Office building re-glaze (weekend work)."),
       ("How does after-hours pricing work?", "Premium time labor rates (1.5x-2x standard) add 15-30% to the labor line item. Temporary protection (Visqueen, plywood, scaffold weather screen) adds $4-$12 per square foot. Crew break-down and re-setup nightly adds 5-10% to labor productivity loss. Net premium: 20-40% over standard new-construction install pricing."),
       ("Can ACG do 24/7 commercial glazing?", "Continuous shift work on critical scopes \u2014 e.g., hospital occupied-facility re-glaze, school summer-break compressed schedule, retail mall blackout install. Bid with shift premium and supervision overhead. Typically used on scopes where schedule compression is the owner's priority.")
     ]),
    ("commercial-glass-replacement-hurricane-damage-florida", "Commercial glass replacement after hurricane damage Florida",
     "Post-hurricane commercial glass replacement across Florida. ACG handles insurance documentation, AHJ permit pathway, NOA-matched replacement glass, structural assessment, and full envelope re-glaze on commercial scopes from $50K to $2M+. Florida-licensed (FL CGC #1531993), $6M bonded.",
     [
       ("How does insurance documentation work on hurricane glass claims?", "ACG provides scope-of-work documentation, photo evidence, structural assessment, and pricing-detail breakdown formatted for commercial insurance claims. Most carriers accept ACG bid documentation directly. We coordinate with the adjuster as needed."),
       ("Does the replacement glass need to match the original NOA?", "In HVHZ markets (Miami-Dade, Broward), yes \u2014 replacement glass must match the original NOA-approved assembly or carry a current NOA-equivalent assembly. ACG sources NOA-matched replacement glass directly from manufacturers."),
       ("What's the typical hurricane glass replacement timeline?", "30-90 days for in-stock glass packages. 90-180 days for custom architectural or oversized lites. Lead time often exceeds the insurance carrier's deadline \u2014 we document the manufacturer's confirmed delivery date on the bid to support claim extension requests.")
     ]),
    ("commercial-glass-board-up-emergency-florida", "Commercial glass board-up emergency Florida",
     "Commercial glass board-up emergency response across Florida \u2014 temporary plywood or polycarbonate replacement following breakage, vandalism, storm damage, or impact. ACG provides 24-hour site response with permanent re-glaze scheduled within 48 hours.",
     [
       ("What's included in a commercial board-up?", "Temporary 1/2\" or 3/4\" plywood (or 1/4\" polycarbonate for higher-security scopes) cut to opening, anchored to frame, weather-sealed perimeter. Includes site cleanup of broken glass per OSHA waste handling protocol."),
       ("How much does commercial board-up cost?", "$400-$1,200 per opening depending on size, height, and security level. Higher cost for above-grade openings requiring lift access or 24-hour security board-ups."),
       ("Does the board-up cost roll into the permanent re-glaze?", "On most ACG commercial board-up jobs that proceed to permanent re-glaze, the board-up cost is credited against the permanent re-glaze contract \u2014 effectively making the temporary work free.")
     ]),
    ("occupied-building-glazing-installation-florida", "Occupied building glazing installation Florida \u2014 retrofit and re-glaze",
     "ACG performs commercial glazing installation on occupied Florida buildings \u2014 hotel partial-occupancy re-glaze, office building floor-by-floor IGU replacement, medical office occupied-facility re-glaze, restaurant after-hours storefront swap, school summer-break re-glaze. Phased install, weather protection, dust mitigation, egress maintenance, ICRA where required.",
     [
       ("What occupied-building scopes does ACG handle?", "Hotel curtain wall reskin during partial occupancy. Office building IGU replacement floor-by-floor. Restaurant storefront after-hours. Medical office punched-opening replacement room-by-room. School re-glaze during summer break. Each scope phased to maintain occupancy."),
       ("What protections do tenants need during occupied-building glazing?", "Negative-pressure containment for indoor air quality. Weather protection during open-frame periods (rain, wind, salt-air exposure). Acoustic dampening on chiseling and rebar cutting. Dust mitigation for HVAC return air. Egress maintained per Florida Fire Prevention Code. Documented in pre-construction occupied-building plan."),
       ("How does occupied-building pricing differ from new construction?", "20-40% premium over equivalent new-construction line item. Drivers: after-hours labor, temporary protection, productivity loss from break-down/re-setup, scope-by-scope phasing.")
     ]),
]

# === 5 MATERIAL SPEC DEEP-DIVE ===
SPEC = [
    ("aluminum-extrusion-grades-commercial-glazing", "Aluminum extrusion grades for commercial glazing \u2014 6063-T5 vs 6061-T6",
     "Commercial glazing aluminum is typically 6063-T5 alloy \u2014 the architectural extrusion alloy with good extrudability, mid-range strength, and excellent surface finish. 6061-T6 is the structural aluminum alloy used for high-load components (anchors, structural mullions, premium curtain wall verticals) where 6063's strength is insufficient.",
     [
       ("Why is 6063-T5 standard for commercial storefront?", "6063-T5 extrudes cleanly into complex architectural profiles, accepts PVDF/anodized finishes with consistent surface quality, and has yield strength (~145 MPa) sufficient for typical storefront wind loads. It's the architectural extrusion alloy."),
       ("When does aluminum need to be 6061-T6?", "Structural anchorage components, high-load curtain wall verticals, oversized openings under high wind pressure, and specialty structural applications. 6061-T6 yield strength (~276 MPa) is roughly 2x 6063-T5."),
       ("Does the finish look different between 6063 and 6061?", "Both alloys accept PVDF Kynar 70/30 and Class I/II anodized finishes. Surface quality at the extrusion stage is slightly higher on 6063-T5 \u2014 the architectural reason it's preferred when structural performance allows.")
     ]),
    ("low-e-glass-coatings-commercial-explained", "Low-E glass coatings explained \u2014 hard-coat vs soft-coat for commercial",
     "Low-E (low-emissivity) coatings reduce heat transfer and UV penetration on commercial glass. Two coating types: hard-coat (pyrolytic, applied during glass manufacture) and soft-coat (magnetron sputter vacuum deposition, applied to cooled glass). Soft-coat dominates commercial Florida \u2014 better performance, must be encapsulated in IGU.",
     [
       ("Why does soft-coat dominate commercial Florida?", "Soft-coat low-E (Solarban, Viracon, Guardian SunGuard) has lower emissivity (better thermal performance), lower SHGC (better solar control), and better aesthetic clarity than hard-coat. Must be on surface 2 or 3 of an insulating glass unit \u2014 cannot be exposed to weather."),
       ("Is hard-coat ever used in commercial?", "Hard-coat low-E (Pilkington Energy Advantage, AGC EnergySelect) is used on single-pane commercial assemblies (rare), monolithic exterior storefronts in dry climates, and specialty applications where the coating must be on the exterior surface. Rarely the right choice for Florida commercial."),
       ("How do I spec the right coating?", "Specify performance criteria (SHGC, VLT, U-factor) rather than coating type. The glazier and glass manufacturer will recommend the right coating to hit your performance target. For Florida hospitality and office: typically Solarban 70XL or Viracon VRE-67 (soft-coat) in 1\" IGU.")
     ]),
    ("structural-silicone-glazing-commercial-explained", "Structural silicone glazing explained \u2014 when commercial spec requires SSG",
     "Structural silicone glazing (SSG) bonds glass to aluminum mullion using structural-grade silicone sealant \u2014 the silicone is the structural fastener, not a captured glazing channel. Creates frameless aesthetic. Common on premium commercial curtain wall, automotive showrooms, hospitality, and luxury retail.",
     [
       ("When does the architect spec SSG?", "When the aesthetic requirement is frameless or flush glazing \u2014 luxury showroom, hospitality lobby, premium office. SSG eliminates the captured-glazing channel that visually breaks the glass field."),
       ("What sealants qualify for structural silicone glazing?", "Dow Corning 995 Silicone Structural Sealant and Sika SikaSil WS-305 are the two dominant tier-one structural silicones in commercial Florida. Both carry 10-20 year warranty when applied per spec by an approved applicator."),
       ("Is ACG an approved structural silicone applicator?", "Yes. ACG is an approved applicator for Dow Corning and Sika commercial sealant lines. Applicator certification on file for project documentation.")
     ]),
    ("igu-construction-commercial-explained", "IGU construction explained \u2014 commercial insulating glass unit anatomy",
     "An IGU (insulating glass unit) is a multi-pane glass assembly with sealed air space between lites. Standard Florida commercial: 1\" overall IGU = 1/4\" outboard low-E + 1/2\" argon air space + 1/4\" laminated impact inboard. Spacer (Super Spacer, Intercept, TPS) seals the perimeter; sealant seals the edge.",
     [
       ("Why argon gas in the air space?", "Argon is denser than air, reduces convective heat transfer across the air space, and improves U-factor by 5-15%. Standard on commercial IGUs unless cost-engineered out."),
       ("What's the typical IGU edge-seal warranty?", "10 years on commercial IGUs from tier-one manufacturers (Vitro Architectural Glass, Viracon, Guardian). Failure mode is moisture intrusion past the perimeter sealant, visible as condensation between the panes. Replacement requires IGU swap, not full opening replacement."),
       ("When do I need a 1-1/4 inch or 1-1/2 inch IGU?", "Specialty applications. Cold storage commercial. Acoustic-priority projects (recording studios, performance halls, hospital ICUs). High-wind-load assemblies that require thicker glass for structural reasons. Standard commercial Florida is 1 inch IGU.")
     ]),
    ("commercial-aluminum-finishes-pvdf-anodize-powder", "Commercial aluminum finishes \u2014 PVDF vs anodize vs powder coat",
     "Commercial aluminum storefront and curtain wall accept three finish types: PVDF Kynar 70/30 (paint-based), Class I/II anodize (electrolytic oxide layer), and powder coat (electrostatic resin). PVDF dominates commercial Florida \u2014 widest color range, best warranty, premium aesthetic.",
     [
       ("What's the difference between PVDF and powder coat?", "PVDF Kynar 70/30 (e.g., AAMA 2605) is a baked fluoropolymer paint applied at the extruder. Industry-standard commercial finish in Florida with 20-30 year service life. Powder coat is electrostatic resin baked on \u2014 lower cost, shorter service life (10-15 years), narrower color range."),
       ("When is anodize the right finish?", "When the architectural spec calls for a metallic finish (Class II anodize = 0.4 mil oxide, Class I = 0.7 mil). Anodize is durable and integrates the metallic appearance into the substrate. Color range is limited (champagne, dark bronze, light bronze, black). Used on premium curtain wall and architectural storefront."),
       ("What's the typical warranty on commercial aluminum finish?", "PVDF Kynar 70/30: 20-30 year warranty against fade, chalk, peel, adhesion failure (manufacturer warranty + AAMA 2605 spec). Class I anodize: 20 year. Class II anodize: 10 year. Powder coat: 5-10 year. PVDF is the warranty leader.")
     ]),
]

# === 4 INDUSTRY BUYER PAGES ===
BUYER = [
    ("commercial-glazing-for-reits-florida", "Commercial glazing for REITs \u2014 Florida portfolio capabilities",
     "ACG works directly with Real Estate Investment Trusts (REITs) on Florida commercial portfolio glazing scopes \u2014 tenant improvement, re-glaze, post-storm replacement, capital improvement programs. Florida-licensed (FL CGC #1531993), $6M aggregate bonded, AIA G702/G703 pay applications, lien-waiver discipline.",
     [
       ("What REIT portfolio scopes does ACG handle?", "Tenant improvement glass scopes on mall in-line stores. Office building re-glaze and capital improvement programs. Multifamily envelope on owned-operated apartment portfolios. Hospitality property re-glaze during planned renovation cycles. Retail strip center storefront refresh."),
       ("Does ACG accept AIA pay applications?", "Yes. Standard AIA G702/G703 progress billing. Conditional and unconditional lien waivers with each pay application. Sworn statements on request. Tier-1 GC, asset manager, and property manager workflow compatibility."),
       ("How does ACG handle multi-property REIT programs?", "Master service agreement structure. Dedicated project manager for the REIT account. Standardized scope, pricing, and documentation across the portfolio. Quarterly business review with the asset management team.")
     ]),
    ("commercial-glazing-for-hospitality-developers-florida", "Commercial glazing for hospitality developers \u2014 Florida hotel and resort",
     "ACG bids commercial glazing scopes for Florida hospitality developers \u2014 limited service, select service, full service, resort, and luxury. Tower curtain wall, balcony glass rails, hotel-room punched windows, lobby all-glass entries, restaurant folding walls, rooftop bar enclosures. Florida-licensed, $6M bonded, 48-hour bid.",
     [
       ("What hospitality glazing scopes does ACG handle?", "Full hotel envelope (tower curtain wall, balcony rails, hotel-room windows, lobby entrance, conference center storefront). Restaurant indoor-outdoor (folding glass walls, all-glass entries). Pool deck and amenity (folding walls, glass railings). Rooftop bar enclosures."),
       ("What's the typical bid window for hospitality glazing?", "ACG bids in 48 hours on complete RFQ packages. Florida hospitality projects often arrive with incomplete spec on the first round \u2014 we follow up with clarification questions inside 24 hours and bid on the second round. Schedule typically compresses against the hotel opening date."),
       ("Does ACG have HVHZ hospitality experience?", "Yes. Active HVHZ commercial glazing project history in Miami-Dade and Broward hospitality. Miami-Dade NOA documentation on every HVHZ scope.")
     ]),
    ("commercial-glazing-for-general-contractors-florida", "Commercial glazing for general contractors \u2014 ACG GC partnership profile",
     "ACG is a Florida-licensed Division 08 (Openings) commercial glazing subcontractor. We bid GC scopes from $50K to $2M+, deliver complete submittals on first round, hit schedule, communicate, finish punch. The standard for a GC repeat bid list.",
     [
       ("Why do GCs put ACG on the next bid list?", "48-hour bid response (Florida average is 7-15 business days). Submittal package complete on first submission. RFI response inside 24 hours. Weekly Friday look-ahead. Punch list closure inside 5 business days at substantial completion. Schedule discipline."),
       ("What scope size does ACG bid?", "$50K to $2M+ commercial glazing scopes. Smaller tenant-improvement scopes (under $50K) we triage by project type. Larger scopes are our specialty."),
       ("What payment terms does ACG accept?", "Standard AIA G702/G703 progress billing. Conditional and unconditional lien waivers with each pay application. Sworn statements on request. Net 30 terms standard. Retention per contract \u2014 standard Florida commercial.")
     ]),
    ("commercial-glazing-owner-direct-restaurant-florida", "Commercial glazing for owner-direct restaurants \u2014 Florida",
     "ACG works owner-direct with Florida restaurant operators \u2014 single-unit and small-chain restaurant owners specifying commercial glazing on new build, tenant improvement, and re-glaze. Folding glass walls, all-glass entries, full-height storefront, HVHZ-rated where the AHJ requires.",
     [
       ("Does ACG work directly with restaurant owners, not through a GC?", "Yes. Many restaurant operators source the glazing scope directly when the GC is acting as construction manager or when the scope is a tenant improvement. ACG bids owner-direct and coordinates with the GC for site logistics."),
       ("What restaurant glazing scopes are common owner-direct?", "Folding glass walls (Euro-Wall, NanaWall) for indoor-outdoor dining. All-glass entrance doors. Patio and rooftop enclosures. Bar storefront. Restaurant storefront replacement after lease build-out completion."),
       ("How fast can ACG bid an owner-direct restaurant glazing scope?", "48 hours on a complete plan package. Restaurant scopes typically include floor plans, elevations, MEP for door operators, and brand spec for hardware finish. Bid response includes scope description, line-item pricing, and schedule.")
     ]),
]

# === 5 SERVICE MODIFIER × CITY ===
SERVICE_CITY = [
    ("emergency-commercial-glass-repair-miami", "Emergency commercial glass repair Miami", "Emergency commercial glass repair in Miami, Florida. 24-hour site response, 48-hour permanent re-glaze on most commercial storefront scopes. Miami-Dade NOA-matched replacement glass. FL CGC #1531993."),
    ("emergency-commercial-glass-repair-tampa", "Emergency commercial glass repair Tampa", "Emergency commercial glass repair in Tampa, Florida. 24-hour site response, 48-hour permanent re-glaze. Florida Product Approval-matched replacement glass. FL CGC #1531993."),
    ("emergency-commercial-glass-repair-orlando", "Emergency commercial glass repair Orlando", "Emergency commercial glass repair in Orlando, Florida. 24-hour site response, 48-hour permanent re-glaze. FL CGC #1531993, $6M bonded."),
    ("after-hours-storefront-installation-miami", "After-hours commercial storefront installation Miami", "After-hours commercial storefront installation in Miami, Florida. Retail mall tenant improvement, hotel re-glaze, restaurant storefront swap after dinner service. Premium labor pricing transparent up-front. FL CGC #1531993."),
    ("hurricane-glass-replacement-fort-lauderdale", "Post-hurricane commercial glass replacement Fort Lauderdale", "Post-hurricane commercial glass replacement in Fort Lauderdale, Florida. Insurance documentation, AHJ permit pathway, Miami-Dade NOA-matched replacement glass. FL CGC #1531993, $6M bonded."),
]


def build_comparisons():
    for slug, title_q, intro, faq in COMPARISONS:
        title = f"{title_q} \u2014 ACG"
        body = f'<header><p style="color:#e11320;font-weight:600;font-size:13px;letter-spacing:1px;text-transform:uppercase;margin-bottom:12px;">Florida Commercial Glazing Spec</p><h1 style="font-size:36px;line-height:1.2;font-weight:800;margin-bottom:20px;color:#050a12;">{html_lib.escape(title_q)}</h1><p style="font-size:19px;line-height:1.7;color:#1f2937;font-weight:500;">{html_lib.escape(intro)}</p></header><section style="margin-top:48px;">'
        for q, a in faq:
            body += f'<h2 style="font-size:24px;color:#050a12;margin-top:32px;margin-bottom:12px;font-weight:700;">{html_lib.escape(q)}</h2><p style="font-size:17px;line-height:1.75;color:#1f2937;">{html_lib.escape(a)}</p>'
        body += '</section><div style="background:#0e284f;color:white;padding:32px;border-radius:12px;margin-top:48px;text-align:center;"><h3 style="font-size:24px;margin-bottom:12px;">Send us drawings \u2014 48-hour bid</h3><a href="/send-plans.html" style="background:#e11320;color:white;padding:14px 28px;border-radius:6px;text-decoration:none;font-weight:600;display:inline-block;">Send Us Plans</a></div>'
        page(title, intro, body, slug, faq=faq,
             breadcrumb=[("Home","https://acglass.com/"),("Resources","https://acglass.com/resources/"),(title_q, f"https://acglass.com/{slug}/")])


def build_emergency():
    for slug, title_q, intro, faq in EMERGENCY:
        title = f"{title_q} \u2014 ACG"
        body = f'<header><p style="color:#e11320;font-weight:600;font-size:13px;letter-spacing:1px;text-transform:uppercase;margin-bottom:12px;">Florida Commercial Glazing Service</p><h1 style="font-size:36px;line-height:1.2;font-weight:800;margin-bottom:20px;color:#050a12;">{html_lib.escape(title_q)}</h1><p style="font-size:19px;line-height:1.7;color:#1f2937;font-weight:500;">{html_lib.escape(intro)}</p></header><section style="margin-top:48px;">'
        for q, a in faq:
            body += f'<h2 style="font-size:24px;color:#050a12;margin-top:32px;margin-bottom:12px;font-weight:700;">{html_lib.escape(q)}</h2><p style="font-size:17px;line-height:1.75;color:#1f2937;">{html_lib.escape(a)}</p>'
        body += '</section><div style="background:#0e284f;color:white;padding:32px;border-radius:12px;margin-top:48px;text-align:center;"><h3 style="font-size:24px;margin-bottom:12px;">Need emergency commercial glass response?</h3><a href="tel:7724867711" style="background:#e11320;color:white;padding:14px 28px;border-radius:6px;text-decoration:none;font-weight:600;display:inline-block;">Call (772) 486-7711</a></div>'
        page(title, intro, body, slug, faq=faq,
             breadcrumb=[("Home","https://acglass.com/"),("Services","https://acglass.com/"),(title_q, f"https://acglass.com/{slug}/")])


def build_spec():
    for slug, title_q, intro, faq in SPEC:
        title = f"{title_q} \u2014 ACG"
        body = f'<header><p style="color:#e11320;font-weight:600;font-size:13px;letter-spacing:1px;text-transform:uppercase;margin-bottom:12px;">Commercial Glazing Material Spec</p><h1 style="font-size:36px;line-height:1.2;font-weight:800;margin-bottom:20px;color:#050a12;">{html_lib.escape(title_q)}</h1><p style="font-size:19px;line-height:1.7;color:#1f2937;font-weight:500;">{html_lib.escape(intro)}</p></header><section style="margin-top:48px;">'
        for q, a in faq:
            body += f'<h2 style="font-size:24px;color:#050a12;margin-top:32px;margin-bottom:12px;font-weight:700;">{html_lib.escape(q)}</h2><p style="font-size:17px;line-height:1.75;color:#1f2937;">{html_lib.escape(a)}</p>'
        body += '</section><div style="background:#0e284f;color:white;padding:32px;border-radius:12px;margin-top:48px;text-align:center;"><h3 style="font-size:24px;margin-bottom:12px;">Need spec help on a Florida commercial project?</h3><a href="/send-plans.html" style="background:#e11320;color:white;padding:14px 28px;border-radius:6px;text-decoration:none;font-weight:600;display:inline-block;">Send Us Plans</a></div>'
        page(title, intro, body, slug, faq=faq,
             breadcrumb=[("Home","https://acglass.com/"),("Resources","https://acglass.com/resources/"),(title_q, f"https://acglass.com/{slug}/")])


def build_buyer():
    for slug, title_q, intro, faq in BUYER:
        title = f"{title_q} \u2014 ACG"
        body = f'<header><p style="color:#e11320;font-weight:600;font-size:13px;letter-spacing:1px;text-transform:uppercase;margin-bottom:12px;">For Buyers</p><h1 style="font-size:36px;line-height:1.2;font-weight:800;margin-bottom:20px;color:#050a12;">{html_lib.escape(title_q)}</h1><p style="font-size:19px;line-height:1.7;color:#1f2937;font-weight:500;">{html_lib.escape(intro)}</p></header><section style="margin-top:48px;">'
        for q, a in faq:
            body += f'<h2 style="font-size:24px;color:#050a12;margin-top:32px;margin-bottom:12px;font-weight:700;">{html_lib.escape(q)}</h2><p style="font-size:17px;line-height:1.75;color:#1f2937;">{html_lib.escape(a)}</p>'
        body += '</section><div style="background:#0e284f;color:white;padding:32px;border-radius:12px;margin-top:48px;text-align:center;"><h3 style="font-size:24px;margin-bottom:12px;">Send us drawings \u2014 48-hour bid</h3><a href="/send-plans.html" style="background:#e11320;color:white;padding:14px 28px;border-radius:6px;text-decoration:none;font-weight:600;display:inline-block;">Send Us Plans</a></div>'
        page(title, intro, body, slug, faq=faq,
             breadcrumb=[("Home","https://acglass.com/"),("For Buyers","https://acglass.com/"),(title_q, f"https://acglass.com/{slug}/")])


def build_service_city():
    for slug, title_q, desc in SERVICE_CITY:
        title = f"{title_q} \u2014 ACG"
        body = f'''<header><p style="color:#e11320;font-weight:600;font-size:13px;letter-spacing:1px;text-transform:uppercase;margin-bottom:12px;">Emergency Commercial Glazing</p>
<h1 style="font-size:38px;line-height:1.2;font-weight:800;margin-bottom:16px;color:#050a12;">{html_lib.escape(title_q)}</h1>
<p style="font-size:19px;line-height:1.7;color:#1f2937;">{html_lib.escape(desc)}</p></header>

<section style="margin-top:48px;">
<h2 style="font-size:24px;color:#050a12;margin-bottom:16px;">Emergency commercial glazing services</h2>
<ul style="font-size:17px;line-height:2;color:#1f2937;list-style:none;padding:0;">
<li>\u2713 24-hour site response with board-up if required</li>
<li>\u2713 48-hour permanent re-glaze on most commercial storefront scopes</li>
<li>\u2713 Insurance documentation for commercial claims</li>
<li>\u2713 Miami-Dade NOA-matched replacement glass in HVHZ markets</li>
<li>\u2713 OSHA-compliant broken glass cleanup and disposal</li>
<li>\u2713 Coordinated AHJ permit pathway for permanent re-glaze</li>
</ul>
</section>

<section style="margin-top:48px;background:#f8f9fb;padding:32px;border-radius:12px;">
<h2 style="font-size:24px;color:#050a12;margin-bottom:12px;">Why ACG for commercial glass emergencies</h2>
<p style="font-size:17px;line-height:1.7;color:#1f2937;">24-hour site response. Florida-licensed (FL CGC #1531993) with $3M general liability and $6M aggregate bonding. Direct manufacturer relationships shorten replacement lead time. Documented zero OSHA recordable incidents since 2021. Commercial scope only.</p>
</section>

<section style="margin-top:48px;text-align:center;background:#0e284f;color:white;padding:48px 32px;border-radius:12px;">
<h2 style="font-size:26px;margin-bottom:16px;">Call now for emergency commercial glass response</h2>
<a href="tel:7724867711" style="background:#e11320;color:white;padding:16px 32px;border-radius:6px;text-decoration:none;font-weight:600;font-size:17px;display:inline-block;">Call (772) 486-7711</a>
</section>'''
        page(title, desc, body, slug,
             breadcrumb=[("Home","https://acglass.com/"),(title_q, f"https://acglass.com/{slug}/")])


if __name__ == "__main__":
    print("Wave 14 \u2014 high-intent gap-fill")
    build_comparisons()
    print(f"  {len(COMPARISONS)} brand comparisons")
    build_emergency()
    print(f"  {len(EMERGENCY)} emergency/specialty services")
    build_spec()
    print(f"  {len(SPEC)} material spec deep-dives")
    build_buyer()
    print(f"  {len(BUYER)} industry buyer pages")
    build_service_city()
    print(f"  {len(SERVICE_CITY)} service-modifier x city")
    total = len(COMPARISONS)+len(EMERGENCY)+len(SPEC)+len(BUYER)+len(SERVICE_CITY)
    print(f"\nWave 14 total: {total}")
