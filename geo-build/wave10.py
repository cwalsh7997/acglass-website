#!/usr/bin/env python3
"""Wave 10 — High-intent commercial conversion pages.
Focus: capture queries that BUY, not just queries that read.
12 "commercial glazier near me" type pages by city
8 specialty product+city pages
6 buyer-intent FAQ pages
Total: 26 pages targeting purchase-intent search terms."""
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

LOCALBIZ = '''{"@context":"https://schema.org","@type":"GeneralContractor","@id":"https://acglass.com/#org","name":"American Commercial Glass","url":"https://acglass.com","telephone":"+1-772-486-7711","email":"info@acglass.com","address":{"@type":"PostalAddress","streetAddress":"1601 N Flagler Dr Ste 100","addressLocality":"West Palm Beach","addressRegion":"FL","postalCode":"33401","addressCountry":"US"},"geo":{"@type":"GeoCoordinates","latitude":26.7153,"longitude":-80.0534},"areaServed":[{"@type":"State","name":"Florida"},{"@type":"State","name":"Tennessee"}]}'''


def page(title, description, body_html, slug, extra_schema=None, breadcrumb=None, faq=None):
    bc_json = ""
    if breadcrumb:
        items = [{"@type":"ListItem","position":i+1,"name":n,"item":u} for i,(n,u) in enumerate(breadcrumb)]
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
<meta property="og:type" content="website">
{FONTS}
{GTAG}
<script type="application/ld+json">
[
{LOCALBIZ}{extra}{bc_json}{faq_json}
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


# 12 "commercial glazier near me" / "best commercial glazier in X" pages
NEAR_ME = [
    ("Boca Raton", "boca-raton", "South Palm Beach County", 26.3683, -80.1289),
    ("Delray Beach", "delray-beach", "South Palm Beach County", 26.4615, -80.0728),
    ("Jupiter", "jupiter", "North Palm Beach County", 26.9342, -80.0942),
    ("Wellington", "wellington", "West Palm Beach County", 26.6618, -80.2417),
    ("Coral Springs", "coral-springs", "Broward County", 26.2712, -80.2706),
    ("Pembroke Pines", "pembroke-pines", "Broward County", 26.0078, -80.2962),
    ("Hollywood", "hollywood-fl", "Broward County", 26.0112, -80.1495),
    ("Doral", "doral-fl", "Miami-Dade County", 25.8195, -80.3553),
    ("Hialeah", "hialeah", "Miami-Dade County", 25.8576, -80.2781),
    ("Pinecrest", "pinecrest", "Miami-Dade County", 25.6692, -80.3081),
    ("Lakeland", "lakeland", "Polk County", 28.0395, -81.9498),
    ("Vero Beach", "vero-beach", "Indian River County", 27.6386, -80.3973),
]

# 8 specialty product + city pages
PRODUCT_CITY = [
    ("Euro-Wall folding door installer", "euro-wall-folding-door-installer", "Miami", "miami", "Miami-Dade NOA-approved Euro-Wall folding door installation"),
    ("Euro-Wall folding door installer", "euro-wall-folding-door-installer", "Naples", "naples", "Naples and Marco Island Euro-Wall folding door installation"),
    ("ESWindows impact window installer", "eswindows-impact-window-installer", "Palm Beach", "palm-beach", "ESWindows architectural impact window installation across Palm Beach County"),
    ("ESWindows impact window installer", "eswindows-impact-window-installer", "Boca Raton", "boca-raton", "ESWindows architectural impact window installation in Boca Raton commercial buildings"),
    ("Kawneer storefront installer", "kawneer-storefront-installer", "Tampa", "tampa", "Kawneer Trifab VG 451 and 1600 SS storefront installation in Tampa Bay"),
    ("Kawneer storefront installer", "kawneer-storefront-installer", "Orlando", "orlando", "Kawneer Trifab VG 451 and 1600 SS storefront installation in Orlando"),
    ("YKK AP storefront installer", "ykk-ap-storefront-installer", "Jacksonville", "jacksonville", "YKK AP YES 45 IG and YHC 300 OG storefront installation in Jacksonville"),
    ("Tubelite storefront installer", "tubelite-storefront-installer", "Miami", "miami", "Tubelite T14000 storefront installation in Miami-Dade HVHZ"),
]

# 6 buyer-intent FAQ pages
BUYER_FAQ = [
    ("how-to-hire-commercial-glazier-florida", "How to hire a commercial glazier in Florida (2026 buyer's guide)",
     "Hiring a Florida commercial glazier comes down to 6 verifications: license (FL CGC), bonding capacity, insurance, NOA experience for HVHZ, response time, and project portfolio depth in your specific vertical. Skip any of these and you risk schedule slip, lien exposure, or warranty gaps.",
     [
       ("What license should a Florida commercial glazier carry?", "Florida CGC (Certified General Contractor) or CGB (Certified Building Contractor) for full commercial scope. CC-C (Certified Glazing Contractor) is the dedicated glazing credential. Verify the license at MyFloridaLicense.com before signing a contract. ACG holds FL CGC #1531993."),
       ("What insurance and bonding does a Florida commercial glazier need?", "Minimum $2M general liability and $1M workers comp for commercial scopes. On projects over $250K, ask for bonding capacity verification \u2014 most reputable Florida commercial glaziers carry $3M-10M bonding. ACG carries $3M general liability and $6M aggregate bonding."),
       ("How do I verify Miami-Dade NOA experience?", "Ask for NOA numbers on three recent HVHZ projects. Verify each NOA at miamidade.gov/permits/online-services.asp. A glazier who can't produce three NOAs by manufacturer (Kawneer, YKK AP, ESWindows) hasn't done meaningful HVHZ work."),
       ("How fast should a commercial glazier respond to my bid request?", "48 hours on a complete RFQ package is fast and serious. 7 business days is the Florida average. Longer than 10 days, they're not prioritizing the bid \u2014 expect the same response speed during the project."),
       ("Should I ask for portfolio depth in my specific vertical?", "Yes. Restaurant glazier and curtain wall glazier are different specialties. Ask for 3 completed projects in your vertical (restaurant, hospital, school, hotel, office) inside the last 24 months. If they can't produce three, they don't have the field experience to manage your specific build."),
       ("What contract red flags should I watch for?", "No mention of NOA documentation. Vague warranty language. No structural calc submission commitment. No specific glass package (no Solarban, Viracon, or ESWindows model number). Lump-sum bid with no line-item breakdown. Schedule promises without material lead time language. Any of these and you're heading for a change-order war.")
     ]),
    ("commercial-glazing-bid-comparison-florida", "How to compare 3 Florida commercial glazing bids without getting fleeced",
     "Apples-to-apples bid comparison in Florida commercial glazing requires forcing every bidder to spec the same glass, same aluminum, same NOA, and same warranty term. Without those four standardizations, you can't compare bids \u2014 you can only guess which one is closer to the truth.",
     [
       ("How do I force apples-to-apples glass spec across 3 bids?", "Include the specific glass product (Solarban 70XL, Viracon VRE-67) or specific performance criteria (SHGC \u2264 0.27, VLT \u2265 0.55, U-factor \u2264 0.32, laminated impact-rated per FBC 1626) in the RFQ. If you don't, each bidder will guess what you mean and your bids will be 20-40% apart for reasons that have nothing to do with installer quality."),
       ("How do I force apples-to-apples aluminum across bids?", "Specify either the exact system (Kawneer Trifab VG 451) or call for 'aluminum thermal storefront system, 2.25 inch sightline mullion, kynar finish, approved equal acceptable.' The approved-equal language opens YKK AP, Tubelite, and EFCO as bid-comparable. Without it, one bidder may be on $25/sq ft cheaper aluminum and you can't tell."),
       ("What if one bid is dramatically lower?", "Ask hard questions in writing. Anchor density (number per linear foot). Glass thickness. Specific NOA being carried (if HVHZ). Submittal package scope. Warranty term and what's covered. A bid 25% below the others is either missing scope (most common), substituting cheaper material (second most common), or proposing crew quality that won't perform (third most common). Real low bids from quality glaziers are rare in Florida commercial."),
       ("What if the bids are very close \u2014 how do I pick?", "Response time on the bid itself. Submittal package preview (ask for a sample shop drawing set from a similar prior project). Reference calls to 3 GCs from completed projects in the last 12 months. The glazier whose GC references say 'they finished on schedule, they communicated, and we'd hire them again' is the right pick \u2014 even at the upper end of the bid range."),
       ("How do I evaluate warranty terms across bids?", "Standard Florida commercial installer warranty is 1-2 years labor. ACG offers 2-year standard, 5-year extended. Sealant warranty 5-20 years depending on type. Glass manufacturer warranty 10 years on IGU. Aluminum manufacturer 5-10 years on finish. Get all four in writing on every bid. A bid that doesn't break warranty out by layer is hiding something."),
       ("Should I require performance bonds on commercial glazing bids?", "On scopes over $250K, yes. On scopes over $1M, absolutely. Florida lien law gives subs strong recovery rights, but performance bonds protect you against schedule slip and abandonment. Bond cost runs 1-3% of contract value and is a line item in the bid \u2014 transparent and worth the cost on six-figure scopes.")
     ]),
    ("what-to-look-for-in-commercial-glazing-warranty", "What to look for in a commercial glazing warranty (Florida 2026)",
     "Florida commercial glazing warranty is a 4-layer stack: glass manufacturer, aluminum manufacturer, sealant, and installer labor. Each layer has different terms, different coverage scopes, and different enforcement pathways. Owners who don't get all four documented at substantial completion enforce warranty 3x slower when issues come up.",
     [
       ("What should the installer labor warranty cover?", "Anchor performance, sealant joint integrity, flashing, weatherstripping integration, hardware function, glass alignment, and field workmanship defects. Should NOT cover acts of God, building structural movement beyond design tolerance, owner-caused damage, or modifications by other trades after installation. ACG installer warranty is 2 years standard, 5 years extended on commercial."),
       ("What does the glass manufacturer warranty cover?", "IGU edge seal failure (typically 10 years), low-E coating defects (5-10 years), lamination delamination (5 years on PVB, 10 years on SGP). Does NOT cover breakage, owner-caused damage, post-installation tinted film application, or chemical exposure beyond manufacturer-approved cleaning agents."),
       ("What does the aluminum manufacturer warranty cover?", "Extrusion finish (PVDF Kynar, anodized, powder coat) against fade, chalk, peel, adhesion failure \u2014 typically 5-10 years. Aluminum substrate is generally lifetime on structural extrusion. Hardware (operators, locks, hinges) typically 1-3 years. Specialty finishes (custom colors, two-tone) may carry shorter terms."),
       ("How long should sealant warranty be?", "Structural sealant (Dow 995, Sika SikaSil WS-305): 10-20 years when applied per spec by an approved applicator. Weatherseal sealants: typically 5 years. Critical: get the applicator's manufacturer certification on file. ACG is approved applicator for Dow Corning and Sika commercial sealant lines."),
       ("What voids commercial glazing warranty most often?", "Owner-side power washing with non-approved chemicals (citrus-based, ammoniated). HVAC overspray. Tinted film applied after installation (voids low-E coating warranty almost universally). Modification of frame for tenant signage without manufacturer approval. Building settlement beyond design tolerance."),
       ("Is the warranty transferable to a new building owner?", "On commercial glazing, yes. ACG installer warranty transfers with documentation. Manufacturer warranties on glass (Vitro, Viracon, Guardian), aluminum (Kawneer, YKK AP), and sealant (Dow, Sika) also transferable. Documentation file at substantial completion makes future transfers fast.")
     ]),
    ("when-to-replace-commercial-glass-vs-repair", "When to replace commercial glass vs repair it (Florida 2026)",
     "Repair vs replace decisions on Florida commercial glass depend on glass type, IGU age, frame integrity, and NOA implications. The rule of thumb: replace at 12+ year IGU age, replace at any structural sealant failure, replace at any HVHZ frame anchor compromise, repair (re-glaze) at single-pane defects or minor sealant joint issues.",
     [
       ("How long does commercial IGU last in Florida?", "Insulating glass unit edge seal warranty is typically 10 years. Actual service life in Florida is 12-18 years depending on installation quality, exposure, and weather cycles. After year 10, expect to start seeing failed IGUs (visible condensation between panes) on 5-15% of units annually."),
       ("Should I repair a failed IGU or replace the whole opening?", "On a failed IGU within 10 years and frame is sound: repair (re-glaze same opening, replace just the glass unit). On a failed IGU at 12+ years AND the building has multiple failures: budget a full re-glaze \u2014 once you're in there, sealant joints, gaskets, and weatherstripping should be addressed together. Lifetime cost is lower with a phased re-glaze than one-off IGU swaps over 5 years."),
       ("When does a curtain wall need full reskin vs repair?", "Full reskin when: structural sealant has failed at multiple bays (Florida structural sealant past 15-18 years), frame anchors are compromised, NOA has expired and current code requires upgrade, or aluminum finish has failed system-wide. Repair when: scattered IGU failures, hardware-only issues, isolated sealant joints, or minor finish touch-up."),
       ("Can I repair an HVHZ-rated storefront after impact damage?", "Partial repair is possible if the manufacturer's NOA covers field-replacement of individual lites and the original NOA documentation is on file. Without those, the AHJ will likely require full replacement of the affected bays. Hurricane impact damage typically requires submittal of repair scope to the AHJ for review before work proceeds."),
       ("What does a commercial re-glaze typically cost in Florida?", "Re-glaze (same frame, new glass): $45-95/sq ft installed depending on glass package. Full storefront replacement: $95-145/sq ft installed. Full curtain wall replacement: $135-225/sq ft installed. Owners typically save 35-55% by re-glazing vs full replacement when the frame is still serviceable."),
       ("How do I know if my frame is still serviceable?", "Get a glazier inspection. Specific things they check: anchor pullout test on sample bays, sealant durometer reading, aluminum corrosion at fasteners and joints, gasket compression, frame deflection under simulated wind load. ACG offers commercial frame inspections at $1,500-3,500 depending on building size \u2014 fee credited toward contract if scope proceeds.")
     ]),
    ("how-to-spec-commercial-impact-glass", "How to spec commercial impact glass for Florida projects (architect guide)",
     "Specifying commercial impact glass for Florida projects requires four decisions: interlayer (PVB vs SGP), tested assembly path (FBC Product Approval vs Miami-Dade NOA), glass package (low-E coating, IGU configuration), and aluminum framing system (Kawneer, YKK AP, Tubelite). Get these four right and the rest of the spec writes itself.",
     [
       ("Should I spec PVB or SGP interlayer?", "PVB at 0.090 inch is the Florida commercial default and meets FBC 1626 for typical storefront and curtain wall scopes. SGP (SentryGlas Plus) is the upgrade for: structural applications (point-supported glass, all-glass entrances), balcony rails, hurricane shutter assemblies, and high-impact-energy projects. SGP is 100x stiffer than PVB and retains structural integrity after impact. Cost premium 25-35% on the glass line item."),
       ("FBC Product Approval or Miami-Dade NOA \u2014 which applies?", "Miami-Dade County and Broward County (the HVHZ markets) require Miami-Dade NOA approval. The rest of Florida accepts FBC Product Approval (FBC PA). NOA documentation is more rigorous and the assemblies are tested to higher cyclic pressure and large missile impact criteria. Always specify the path explicitly in the RFQ \u2014 ambiguity here loses 8-15% of bids to unnecessary HVHZ-spec premiums."),
       ("What low-E coating should I spec for Florida commercial?", "Solarban 70XL is the Florida default for hospitality and office (SHGC 0.27, VLT 0.64, U-factor 0.29 in 1\" IGU). Viracon VRE-67 is the alternative (slightly higher VLT). Solarban 90 is the high-performance upgrade for harsh exposure (SHGC 0.23). For schools and healthcare, often Solarban 60 (SHGC 0.39, VLT 0.70) for natural light priority. Specify the actual product or the SHGC/VLT/U-factor performance criteria."),
       ("What's the right IGU configuration?", "1 inch overall IGU is the Florida commercial standard: 1/4 inch outboard low-E + 1/2 inch argon air space + 1/4 inch laminated impact inboard. 1 inch IGU meets FBC Energy Code and FBC 1626 impact in most commercial scopes. Specialty applications (cold storage, sound attenuation) may require 1-1/4 inch or 1-1/2 inch IGU configurations \u2014 spec accordingly."),
       ("Kawneer, YKK AP, or Tubelite \u2014 which aluminum system?", "Kawneer is the architect-default. YKK AP often qualifies as approved-equal and saves 8-15% on the storefront line item. Tubelite is competitive on stock profiles but sometimes longer lead time on custom dies. All three carry HVHZ NOAs. Default to Kawneer with approved-equal language opening YKK AP and Tubelite."),
       ("What anchorage do I spec for commercial impact glass?", "Engineer-of-record sealed structural calcs are required for all commercial impact glass in Florida. Anchorage type depends on substrate (concrete vs CMU vs steel), wind pressure (ASCE 7-22 calculation), and assembly NOA/FBC PA requirements. Specify 'anchorage per engineer-of-record sealed calculations meeting ASCE 7-22 wind pressure and FBC 1626 impact criteria.' The glazier handles the specific anchor selection.")
     ]),
    ("commercial-glazier-questions-to-ask-before-hiring", "10 questions to ask a Florida commercial glazier before signing a contract",
     "Most commercial glazing project failures in Florida trace back to questions the owner didn't ask before signing. Asking these 10 questions at bid stage filters out 60-80% of unreliable bidders before they get to contract.",
     [
       ("What's your FL CGC license number and current standing?", "Verify at MyFloridaLicense.com. License must be active and the company name must match. ACG holds FL CGC #1531993, active and current. A glazier who hesitates or can't produce the number on the spot is not commercial-grade in Florida."),
       ("Show me three NOAs you carried on recent HVHZ projects.", "If you're in Miami-Dade or Broward, the glazier must produce three Miami-Dade NOA numbers from projects completed in the last 24 months. Verify each at miamidade.gov/permits/online-services.asp. A glazier who can't produce three has not done meaningful HVHZ work recently."),
       ("What's your bonding capacity?", "On contracts over $250K, ask for current bonding letter from their surety. Most Florida commercial glaziers carry $3M-10M bonding. ACG carries $6M aggregate. A glazier without bonding capacity is undercapitalized for commercial work."),
       ("Who are your three most recent GC references?", "Ask for GCs from completed projects in the last 12 months. Call them. The question to ask: 'Would you hire this glazier again? Why or why not?' GCs who hesitate on the 'would you hire again' question are flagging something."),
       ("What's your average bid response time and submittal turnaround?", "48 hours on bid is fast. 7 business days is Florida average. Submittal turnaround should be 10-15 business days from contract award. A glazier who can't quote turnaround numbers has not measured their own operation \u2014 they will be slower."),
       ("Show me a sample shop drawing set from a similar project.", "Quality of shop drawings predicts quality of installation. Look for: clear elevations, detailed sections, hardware schedule, glass type call-outs, sealant joint sections, anchor details. Sloppy shop drawings mean sloppy field installation."),
       ("What's your warranty term and what specifically does it cover?", "Get warranty terms by layer (installer labor, glass manufacturer, aluminum manufacturer, sealant). In writing. Vague warranty language is the single biggest source of post-project dispute."),
       ("What's your safety record?", "Ask for current OSHA EMR (Experience Modification Rate). Industry average is 1.0 \u2014 lower is better. ACG carries an OSHA EMR below 1.0 with zero recordable incidents since 2021. A glazier without current EMR documentation hasn't built a safety culture."),
       ("Who specifically will run my project from your team?", "Get the project manager and field superintendent names. Verify they're on staff, not contract. Ask how many active projects they're each running concurrently. PM running 10+ active commercial projects is overloaded \u2014 quality drops."),
       ("Can you commit to the schedule in writing with material lead times itemized?", "Schedule commitments without itemized material lead times are guesses. Make the glazier identify the longest lead-time item (typically custom aluminum extrusions or specialty glass packages) and commit to ordering on signed contract, not on permit issuance. This saves 2-3 weeks on every commercial project.")
     ])
]


def build_near_me():
    for city, slug, region, lat, lon in NEAR_ME:
        page_slug = f"commercial-glazier-{slug}"
        title = f"Commercial Glazier {city}, FL \u2014 ACG | Storefronts, Curtain Wall, Impact Glass"
        desc = f"Looking for a commercial glazier in {city}? ACG handles storefronts, curtain wall, impact windows, folding glass walls for commercial buildings across {region}. 48-hour bid turnaround."
        body = f'''<header><p style="color:#e11320;font-weight:600;font-size:13px;letter-spacing:1px;text-transform:uppercase;margin-bottom:12px;">Commercial Glazier {city}, FL</p>
<h1 style="font-size:42px;line-height:1.15;font-weight:800;margin-bottom:16px;color:#050a12;">Commercial Glazier in {city}, Florida</h1>
<p style="font-size:19px;line-height:1.7;color:#5a6473;">ACG is a licensed Florida commercial glazing contractor (FL CGC #1531993) serving {city} and the surrounding {region}. We bid commercial scopes from $50K to $2M+ across storefronts, curtain wall, impact windows, folding glass walls, and architectural glazing.</p></header>

<section style="margin-top:48px;">
<h2 style="font-size:28px;color:#050a12;margin-bottom:16px;">Commercial glazing services in {city}</h2>
<ul style="font-size:17px;line-height:2;color:#1f2937;list-style:none;padding:0;">
<li>\u2713 Commercial storefront installation (Kawneer, YKK AP, Tubelite)</li>
<li>\u2713 Curtain wall installation (Kawneer 1600 SS, YKK AP YHC 300 OG)</li>
<li>\u2713 Impact-rated windows and doors (HVHZ where required, FBC elsewhere)</li>
<li>\u2713 Folding glass walls and multi-slide doors (Euro-Wall, NanaWall)</li>
<li>\u2713 All-glass entrance doors with structural patch fittings</li>
<li>\u2713 Balcony glass railings (laminated SGP)</li>
<li>\u2713 Architectural glazing and full-height curtain wall</li>
<li>\u2713 Commercial glass repair, re-glaze, and IGU replacement</li>
</ul>
</section>

<section style="margin-top:48px;background:#f8f9fb;padding:32px;border-radius:12px;">
<h2 style="font-size:24px;color:#050a12;margin-bottom:12px;">Why {city} buyers choose ACG</h2>
<ul style="font-size:17px;line-height:1.9;color:#1f2937;padding-left:20px;">
<li><strong>48-hour bid turnaround</strong> on complete commercial RFQ packages (vs Florida average of 7-15 business days)</li>
<li><strong>FL CGC #1531993</strong> \u2014 licensed Florida commercial general contractor, $3M general liability, $6M aggregate bonding</li>
<li><strong>350+ commercial projects</strong> completed across Florida</li>
<li><strong>0 OSHA recordable incidents since 2021</strong> \u2014 documented safety record</li>
<li><strong>Direct manufacturer relationships</strong> with Kawneer, YKK AP, Tubelite, ESWindows, Euro-Wall</li>
<li><strong>2-year installer warranty</strong> standard, 5-year extended available on commercial scopes</li>
</ul>
</section>

<section style="margin-top:48px;">
<h2 style="font-size:24px;color:#050a12;margin-bottom:12px;">Project types we handle in {city}</h2>
<p style="font-size:17px;line-height:1.7;color:#1f2937;">Restaurants, hotels, medical office buildings, schools, retail centers, country clubs, government buildings, office towers, multifamily developments. Commercial scope only \u2014 we do not do residential window installation.</p>
</section>

<section style="margin-top:48px;text-align:center;background:#0e284f;color:white;padding:48px 32px;border-radius:12px;">
<h2 style="font-size:30px;margin-bottom:16px;">Send us drawings \u2014 48-hour bid on your {city} project</h2>
<p style="font-size:17px;opacity:0.9;margin-bottom:24px;">Real number, fast. No filler. No "we'll get back to you."</p>
<a href="/send-plans.html" style="background:#e11320;color:white;padding:16px 32px;border-radius:6px;text-decoration:none;font-weight:600;font-size:17px;display:inline-block;">Send Us Plans</a>
<p style="margin-top:20px;opacity:0.7;font-size:14px;">Or call (772) 486-7711</p>
</section>'''

        service_schema = json.dumps({"@context":"https://schema.org","@type":"Service","name":f"Commercial Glazing in {city}, FL","provider":{"@type":"GeneralContractor","name":"American Commercial Glass","@id":"https://acglass.com/#org"},"areaServed":{"@type":"City","name":city,"containedInPlace":{"@type":"State","name":"Florida"},"geo":{"@type":"GeoCoordinates","latitude":lat,"longitude":lon}},"serviceType":"Commercial Glazing"})

        page(title, desc, body, page_slug,
             extra_schema=service_schema,
             breadcrumb=[("Home","https://acglass.com/"),("Service Areas","https://acglass.com/service-areas-map/"),(city, f"https://acglass.com/{page_slug}/")])


def build_product_city():
    for product, prod_slug, city, city_slug, intent in PRODUCT_CITY:
        slug = f"{prod_slug}-{city_slug}"
        title = f"{product} in {city}, Florida \u2014 ACG"
        desc = f"ACG is a Florida-licensed installer for {product.lower()} in {city}. {intent}. FL CGC #1531993, 350+ commercial projects."
        body = f'''<header><p style="color:#e11320;font-weight:600;font-size:13px;letter-spacing:1px;text-transform:uppercase;margin-bottom:12px;">{product}</p>
<h1 style="font-size:38px;line-height:1.2;font-weight:800;margin-bottom:16px;color:#050a12;">{product} in {city}, Florida</h1>
<p style="font-size:19px;line-height:1.7;color:#5a6473;">{intent}. ACG holds FL CGC #1531993 and carries direct manufacturer relationships for accurate spec, faster lead times, and warranty-supported installation.</p></header>

<section style="margin-top:48px;">
<h2 style="font-size:28px;color:#050a12;margin-bottom:16px;">Why {city} buyers choose ACG for this product</h2>
<ul style="font-size:17px;line-height:1.9;color:#1f2937;padding-left:20px;">
<li>Direct manufacturer relationship \u2014 we order direct, not through a distributor</li>
<li>Florida-licensed (FL CGC #1531993) with $3M general liability and $6M bonding</li>
<li>48-hour bid turnaround on complete RFQ packages</li>
<li>HVHZ-experienced installation crews where {city} requires Miami-Dade NOA</li>
<li>Engineer-of-record sealed structural calculations included on every commercial scope</li>
<li>Manufacturer warranty + 2-year ACG installer warranty standard, 5-year extended available</li>
</ul>
</section>

<section style="margin-top:48px;background:#f8f9fb;padding:32px;border-radius:12px;">
<h2 style="font-size:24px;color:#050a12;margin-bottom:12px;">What we install for {city} commercial buildings</h2>
<p style="font-size:17px;line-height:1.7;color:#1f2937;">Restaurants, hotels, retail, office buildings, medical office, schools, country clubs, and architectural residential projects in {city} and surrounding markets. Commercial scope only.</p>
</section>

<section style="margin-top:48px;text-align:center;background:#0e284f;color:white;padding:48px 32px;border-radius:12px;">
<h2 style="font-size:28px;margin-bottom:16px;">Get a {product.lower()} bid for your {city} project</h2>
<a href="/send-plans.html" style="background:#e11320;color:white;padding:16px 32px;border-radius:6px;text-decoration:none;font-weight:600;font-size:17px;display:inline-block;">Send Us Plans</a>
<p style="margin-top:20px;opacity:0.7;font-size:14px;">Or call (772) 486-7711</p>
</section>'''

        page(title, desc, body, slug,
             breadcrumb=[("Home","https://acglass.com/"),(product, f"https://acglass.com/{prod_slug}/"),(city, f"https://acglass.com/{slug}/")])


def build_buyer_faq():
    for slug, q, intro, faq in BUYER_FAQ:
        title = f"{q} \u2014 ACG"
        body = f'<header><p style="color:#e11320;font-weight:600;font-size:13px;letter-spacing:1px;text-transform:uppercase;margin-bottom:12px;">Florida Commercial Glazing Buyer Guide</p><h1 style="font-size:36px;line-height:1.2;font-weight:800;margin-bottom:20px;color:#050a12;">{html_lib.escape(q)}</h1><p style="font-size:19px;line-height:1.7;color:#1f2937;font-weight:500;">{html_lib.escape(intro)}</p></header><section style="margin-top:48px;">'
        for qq, aa in faq:
            body += f'<h2 style="font-size:24px;color:#050a12;margin-top:32px;margin-bottom:12px;font-weight:700;">{html_lib.escape(qq)}</h2><p style="font-size:17px;line-height:1.75;color:#1f2937;">{html_lib.escape(aa)}</p>'
        body += '</section><div style="background:#0e284f;color:white;padding:32px;border-radius:12px;margin-top:48px;text-align:center;"><h3 style="font-size:24px;margin-bottom:12px;">Ready for a Florida commercial glazing bid?</h3><a href="/send-plans.html" style="background:#e11320;color:white;padding:14px 28px;border-radius:6px;text-decoration:none;font-weight:600;display:inline-block;">Send Us Plans</a></div>'

        speakable = json.dumps({"@context":"https://schema.org","@type":"WebPage","speakable":{"@type":"SpeakableSpecification","cssSelector":["h1","h2","p"]},"url":f"https://acglass.com/{slug}/"})

        page(title, intro, body, slug,
             extra_schema=speakable,
             breadcrumb=[("Home","https://acglass.com/"),("FAQ","https://acglass.com/florida-glazing-faq/"),(q, f"https://acglass.com/{slug}/")],
             faq=faq)


if __name__ == "__main__":
    print("Wave 10 \u2014 high-intent buyer pages")
    print(f"Building {len(NEAR_ME)} 'commercial glazier in X' city pages...")
    build_near_me()
    print(f"Building {len(PRODUCT_CITY)} product+city pages...")
    build_product_city()
    print(f"Building {len(BUYER_FAQ)} buyer-intent FAQ pages...")
    build_buyer_faq()
    print(f"\nTotal: {len(NEAR_ME)+len(PRODUCT_CITY)+len(BUYER_FAQ)} pages")
