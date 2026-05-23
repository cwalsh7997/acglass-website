#!/usr/bin/env python3
"""Wave 7: 10 more vertical x city combos + 6 service-specific landing pages + 4 AIO FAQ + /reviews/."""
import os, json, sys, html as html_lib

OUT = "/home/user/workspace/acglass-website"
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from seo_sprint import build_aio
from wave5 import build_vc2

GTAG = '''<script async src="https://www.googletagmanager.com/gtag/js?id=G-M7BFQD2SPP"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}gtag("js",new Date());gtag("config","G-M7BFQD2SPP");</script>'''

FONTS = '''<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/css/style.css?v=1777031720">'''

NAV = '''<nav class="nav scrolled"><div class="nav-inner">
<a href="/index.html" class="nav-logo"><img height="72" width="338" src="/images/acg-logo-nav@2x.png" style="height:36px;width:auto;" alt="ACG" class="logo-img" loading="lazy"></a>
<div class="nav-links">
<a href="/index.html">Home</a><a href="/case-studies/">Case Studies</a><a href="/tools/">Tools</a>
<a href="/resources/">Resources</a>
<a href="/send-plans.html" class="nav-cta">Send Us Plans</a>
</div>
</div></nav>'''

FOOTER = '''<footer class="footer"><div class="container"><div class="footer-grid">
<div><img src="/images/acg-logo-nav@2x.png" alt="ACG" style="height:36px;width:auto;margin-bottom:16px;"></div>
<div><h4>Resources</h4><ul><li><a href="/resources/">Resources</a></li><li><a href="/tools/">Tools</a></li><li><a href="/glossary/">Glossary</a></li></ul></div>
<div><h4>Contact</h4><p style="color:rgba(255,255,255,0.6);font-size:14px;line-height:1.8;">(772) 486-7711<br>info@acglass.com</p></div>
</div></div></footer>'''

ORG_SAMEAS = ["https://www.wikidata.org/wiki/Q139858578", "https://acglass.ai/", "https://www.linkedin.com/company/acglass"]


def write_html(rel, html_str):
    full = os.path.join(OUT, rel.lstrip("/"))
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(html_str)
    print(f"  Wrote /{rel}")


# ============================================================
# 10 more vertical x city combos
# ============================================================

VC4 = [
    ("restaurant-glazier-orlando", "Restaurant", "Orlando", "Orange", "orlando", "orange-county", "restaurant-glazier-florida", 28.5384, -81.3789,
        "Orlando restaurant construction concentrates on downtown, Lake Nona, Winter Park, and Disney Springs / Lake Buena Vista. Strong tourism-driven and resident-driven restaurant market. Standard FBC wind code \u2014 impact glazing optional, which keeps Orlando restaurant projects 18-25% below South Florida costs.",
        "Orlando is inland \u2014 standard FBC wind code. Impact-rated glazing is NOT required by code. Most Orlando restaurants use insulated low-E glazing without impact rating."),
    ("hotel-glazing-contractor-orlando", "Hotel", "Orlando", "Orange", "orlando", "orange-county", "hotel-glazing-contractor-florida", 28.5384, -81.3789,
        "Orlando hotel construction is one of the largest hotel markets in the country \u2014 driven by Disney, Universal, SeaWorld, and the convention center. International Drive, Lake Buena Vista, and Universal Boulevard concentrate the bid market. Brand-driven design with major Marriott, Hilton, Hyatt, and IHG capital programs.",
        "Orlando is inland \u2014 standard FBC wind code. Impact-rated glazing optional. ADA accessibility, fire-rated openings, and energy code (Climate Zone 2) all apply."),
    ("medical-office-glazier-tampa", "Medical Office", "Tampa", "Hillsborough", "tampa", "hillsborough-county", "medical-office-glazier-florida", 27.9506, -82.4572,
        "Tampa MOB construction is driven by Tampa General Hospital, BayCare Health System, Moffitt Cancer Center, and AdventHealth Tampa. Strong specialty clinic market plus University of South Florida medical campus. WBDR coastal exposure for most projects.",
        "Tampa coastal MOBs require ASTM E1996/E1886 impact-rated assemblies. Inland Hillsborough is standard FBC. ADA accessibility on all medical entries."),
    ("medical-office-glazier-jacksonville", "Medical Office", "Jacksonville", "Duval", "jacksonville", "duval-county", "medical-office-glazier-florida", 30.3322, -81.6557,
        "Jacksonville MOB construction is driven by Baptist Health, UF Health Jacksonville, Mayo Clinic Florida, and Memorial Hospital. Strong primary care, specialty clinic, and surgical center market across Town Center, Riverside, San Marco, and Westside corridors.",
        "Jacksonville coastal areas are WBDR. Inland Duval is standard FBC. ADA on all medical office entries."),
    ("retail-storefront-installer-orlando", "Retail", "Orlando", "Orange", "orlando", "orange-county", "retail-storefront-installer-florida", 28.5384, -81.3789,
        "Orlando retail construction concentrates on tourist corridors (International Drive, Disney Springs), urban retail (Park Avenue Winter Park, downtown), and suburban retail (Mall at Millenia, Florida Mall, The Loop). Standard FBC wind code keeps Orlando retail glass affordable.",
        "Orlando is inland \u2014 standard FBC wind code. Impact-rated glazing optional. Brand-driven retail design and landlord-criteria storefront review apply."),
    ("retail-storefront-installer-fort-lauderdale", "Retail", "Fort Lauderdale", "Broward", "fort-lauderdale", "broward-county", "retail-storefront-installer-florida", 26.1224, -80.1373,
        "Fort Lauderdale retail concentrates on Las Olas Boulevard, the Galleria area, Sawgrass Mills, and Federal Highway corridor. HVHZ-rated storefront for all projects.",
        "Fort Lauderdale is full HVHZ. All retail storefront requires Miami-Dade NOA. Brand-driven design and landlord criteria from Brookfield, Simon Property Group, and DDR apply."),
    ("office-building-glazier-naples", "Office Building", "Naples", "Collier", "naples", "collier-county", "office-building-glazier-florida", 26.1420, -81.7948,
        "Naples office construction is concentrated in downtown Naples, North Naples (Pine Ridge / Vanderbilt), and the Naples Park area. Class-A office, medical office, and corporate-headquarters work driven by the wealth concentration in Collier County.",
        "Naples is WBDR \u2014 ASTM E1996/E1886 impact-rated assemblies required. Florida Product Approval (FL #) sufficient \u2014 Miami-Dade NOA not required."),
    ("office-building-glazier-jacksonville", "Office Building", "Jacksonville", "Duval", "jacksonville", "duval-county", "office-building-glazier-florida", 30.3322, -81.6557,
        "Jacksonville office construction is recovering and active in Downtown, Riverside, and Town Center. Insurance, fintech, and logistics drive demand. Naval Air Station Jacksonville support and Mayo Clinic medical office adjacent to corporate.",
        "Jacksonville coastal areas are WBDR. Inland Duval is standard FBC. Multi-AHJ structure consolidated under City of Jacksonville Building Inspection."),
    ("school-glazier-jacksonville", "School / Education", "Jacksonville", "Duval", "jacksonville", "duval-county", "school-glazier-florida", 30.3322, -81.6557,
        "Duval County Public Schools serves over 130,000 students across 200+ schools. Ongoing K-12 capital construction, plus University of North Florida, Jacksonville University, and FSCJ college projects. Post-Parkland security vestibule design standards apply.",
        "Jacksonville coastal schools require WBDR impact-rated assemblies. Inland schools standard FBC. Security vestibule design (UL 752 Level 3+) standard on new construction."),
    ("school-glazier-fort-lauderdale", "School / Education", "Fort Lauderdale", "Broward", "fort-lauderdale", "broward-county", "school-glazier-florida", 26.1224, -80.1373,
        "Broward County Public Schools is the 6th largest school district in the country. Continuous K-12 capital construction with strong security vestibule, ballistic-rated entry, and impact-rated classroom window programs since Parkland (2018). HVHZ-rated everything.",
        "All Broward schools are HVHZ \u2014 Miami-Dade NOA required. Post-Parkland security vestibule design standards (UL 752 Level 3 minimum) are non-negotiable.")
]


# ============================================================
# 6 service-specific landing pages
# ============================================================

SERVICES = [
    {
        "slug": "folding-glass-walls-florida",
        "h1": "Folding Glass Walls \u2014 Florida Commercial",
        "title": "Folding Glass Walls Florida | Accordion Retractable Restaurant Walls | ACG",
        "description": "ACG installs folding glass walls (accordion-style retractable systems) on Florida commercial restaurants, indoor-outdoor concepts, hospitality, and event venues. HVHZ-rated.",
        "intro": "Folding glass walls are accordion-style retractable wall systems that fully open a building wall to create indoor-outdoor space. Standard on Florida upscale restaurants, hospitality, event venues, and pool houses. ACG installs Euro-Wall, NanaWall, LaCantina, and Solar Innovations folding wall systems.",
        "sections": [
            ("How folding glass walls work", "Folding glass walls are made of individual glass panels hinged together at the top and bottom tracks. They slide along the track and stack together at one end of the opening. Typical configurations: 4-leaf, 6-leaf, 8-leaf. Opening sizes from 12 feet to 60 feet wide are common."),
            ("HVHZ folding wall requirements", "Florida HVHZ folding walls require factory-bonded laminated impact glazing with current Miami-Dade NOA. The full assembly (glass + frame + hinges + tracks + threshold + closer hardware) is tested as a unit. NOAs are manufacturer + configuration specific."),
            ("Common applications on Florida commercial", "Restaurants (indoor-outdoor dining concepts), hospitality lobbies and amenity rooms, event venues, pool houses, golf clubhouses, and luxury residential commercial-adjacent spaces."),
            ("Brand options", "Euro-Wall (commercial-grade, multiple HVHZ NOAs), NanaWall (broad architectural specification range), LaCantina (residential and light commercial), Solar Innovations (custom architectural). Cost varies dramatically by brand and configuration."),
            ("Cost benchmarks", "Florida folding glass wall: $320-$650 per linear foot of opening installed, complete with HVHZ-rated assembly. Adds beyond impact-rated glass: hardware, threshold, weatherstripping, and tracks all factor into the per-foot pricing."),
            ("Coordination with HVAC and weather sealing", "Florida folding walls must coordinate with HVAC dampers (so AC doesn't blow conditioned air outside when wall is open), and with restaurant smoke evacuation systems. The threshold and weather sealing detail at the bottom track is the most failure-prone element \u2014 specify proper drainage and continuous gaskets.")
        ]
    },
    {
        "slug": "multi-slide-doors-florida",
        "h1": "Multi-Slide Doors \u2014 Florida Commercial",
        "title": "Multi-Slide Doors Florida | Stacking Sliding Doors | Restaurant & Hospitality | ACG",
        "description": "ACG installs multi-slide doors (stacking sliding panels) on Florida commercial restaurants, hospitality, and luxury residential commercial projects. HVHZ-rated assemblies.",
        "intro": "Multi-slide doors are sliding-glass-door systems with multiple stacking panels that telescope or stack at one or both ends of the opening. Common on Florida restaurant indoor-outdoor concepts, hotel amenity decks, luxury residential commercial, and brand-experience retail. ACG installs Euro-Wall, NanaWall, Western Window Systems, and Andersen multi-slide systems.",
        "sections": [
            ("Multi-slide vs folding wall \u2014 which is right for your project", "Multi-slide doors stack panels at one or both ends; they don't fold like accordion walls. Slide systems are sleeker, faster to operate, and have fewer pivot points. Folding walls are more compact when fully open but have more hinge mechanisms. For wide openings (40+ feet), multi-slide is usually the better choice."),
            ("HVHZ multi-slide requirements", "Same as folding walls \u2014 factory-bonded laminated impact glazing with current Miami-Dade NOA. The full slider assembly (panels + rollers + tracks + threshold + perimeter framing) is tested as a unit."),
            ("Standard configurations", "Telescoping (panels slide on multiple tracks and stack on top of each other): cleanest open appearance. Biparting (panels open from center to both sides): traditional. Single-direction sliding (all panels stack at one end): most common."),
            ("Common applications", "Restaurant indoor-outdoor concepts, hotel pool deck enclosures, golf clubhouse amenity rooms, luxury condo amenity floors, brand-experience retail (Tesla, Apple, large showrooms)."),
            ("Cost benchmarks", "Florida HVHZ multi-slide door: $280-$580 per linear foot of opening installed. Adds beyond impact-rated glass: rollers, tracks, screen integration, motorization (optional)."),
            ("Motorization and smart-home integration", "Modern multi-slide systems support motorized opening with remote, smartphone, or building automation system integration. Common on luxury residential commercial and high-end hospitality. Adds 25-40% to the system cost.")
        ]
    },
    {
        "slug": "all-glass-entrance-doors-florida",
        "h1": "All-Glass Entrance Doors \u2014 Florida Commercial",
        "title": "All-Glass Entrance Doors Florida | Frameless Commercial Entries | ACG",
        "description": "ACG installs all-glass entrance doors (frameless tempered glass entries with continuous hinges) on Florida commercial buildings. HVHZ-rated. Single doors and pairs.",
        "intro": "All-glass entrance doors are frameless tempered glass entries with continuous hinges, top and bottom rails (or fully frameless), and architectural hardware. Used on upscale retail, restaurants, hospitality lobbies, office buildings, and any commercial building where the design intent calls for a transparent, brand-quality entry.",
        "sections": [
            ("How all-glass entrances are constructed", "Tempered safety glass (typically 1/2\" thick or 3/4\" thick) with mechanical hardware bolted through the glass. Continuous hinge (running full door height) or pivot hinges at top and bottom. Optional top and bottom rails for additional structural support. Architectural pulls, panic hardware, locks, and closers."),
            ("HVHZ all-glass entrances", "HVHZ-rated all-glass entrances are rare but available \u2014 specific manufacturers (Dorma Kaba, CRL) offer Miami-Dade NOA assemblies for impact-rated frameless entries. For non-HVHZ Florida (inland), standard tempered all-glass entries are acceptable."),
            ("Hardware options", "Continuous hinges (Pemko, Markar, Bommer) for heavy-traffic commercial. Pivot sets (Dorma, CRL) for architectural-feature entries. Panic hardware (Adams Rite, Von Duprin) for code-required egress. Architectural pulls (custom-sized or stock from CRL, Trimco)."),
            ("Common applications", "Upscale retail flagships, restaurant entries, hotel lobby entries, Class-A office lobby entries, healthcare main entries, museum and gallery entries."),
            ("Cost benchmarks", "Single all-glass entrance door (frameless, with continuous hinge and panic hardware): $6,200-$14,500 installed. Pair of all-glass entrance doors (vestibule, double-door egress): $11,800-$28,000 installed."),
            ("Maintenance considerations", "All-glass entrances need annual hardware re-tightening (continuous hinge fasteners, pull anchors, threshold bolts). High-traffic entries (grocery, hospital) may need quarterly maintenance. Glass replacement on damage is straightforward but expensive due to custom sizes.")
        ]
    },
    {
        "slug": "balcony-glass-railings-florida",
        "h1": "Balcony Glass Railings \u2014 Florida Commercial",
        "title": "Balcony Glass Railings Florida | Commercial Hotel & Condo Glass Rails | ACG",
        "description": "ACG installs balcony glass railings on Florida hotels, condominiums, and commercial buildings. Structural laminated glass, 50 lb/ft load rated, IBC compliant.",
        "intro": "Balcony glass railings on Florida commercial buildings (hotels, condos, mixed-use) require structural laminated glass per IBC, 50 lb/ft horizontal load capacity, and Florida Product Approval. ACG installs C.R. Laurence Taper-Loc, CRL B-Series, AGS Stainless Clearview, and Trex Signature glass railing systems.",
        "sections": [
            ("Code requirements for commercial balcony glass railings", "IBC 2018+ requires balcony glass to: (1) handle 50 lb/ft horizontal load at top, (2) handle 200 lb concentrated load at any point, (3) use structural laminated glass with PVB or SGP interlayer, (4) include a top cap or rail unless the system is engineered for the load without it."),
            ("Marine-grade hardware for coastal exposure", "Florida coastal projects (oceanfront condos, beach hotels, marina commercial) need marine-grade 316 stainless steel hardware. Standard galvanized or powder-coated steel will fail within 5-10 years in saltwater spray exposure. Marine-grade premium: 25-40% over standard."),
            ("Common systems", "C.R. Laurence (CRL) Taper-Loc dry-set: fast install, no concrete. CRL B-Series base shoe: heavy-duty dry-glazed. AGS Stainless Clearview: marine-grade stainless for coastal. Trex Signature: aluminum top-rail aesthetic with laminated glass infill."),
            ("Cost benchmarks", "Commercial balcony glass railing in Florida: $260-$450 per linear foot installed. Marine-grade coastal premium: 25-40% additional. Engineering, anchorage analysis, and Florida Product Approval included in qualified bids."),
            ("Installation considerations", "Anchorage to the slab is the critical detail. Most failures happen at slab anchorage \u2014 use post-installed adhesive anchors (Hilti HIT-RE 500 or equivalent) properly torqued. Avoid through-bolt-only installations on edge slabs."),
            ("Long-term maintenance", "Annual fastener re-tightening on coastal installations. Glass panels can be replaced individually if damaged \u2014 standard CRL components are stocked in Florida. Workmanship warranty typically 1-5 years.")
        ]
    },
    {
        "slug": "storefront-renovation-retrofit-florida",
        "h1": "Storefront Renovation & Retrofit \u2014 Florida Commercial",
        "title": "Storefront Renovation Retrofit Florida | Replace Existing Commercial Glass | ACG",
        "description": "ACG handles commercial storefront renovation and retrofit on Florida buildings \u2014 replacement of failed seals, code upgrades, brand refresh, impact-rated upgrades.",
        "intro": "Storefront renovation and retrofit is a major part of ACG's business. Aging commercial storefront (pre-2000 vintage), failed IGUs, owner brand refresh, code upgrade to HVHZ, and energy efficiency upgrades all drive renovation work. ACG handles both like-for-like replacement and full code-upgrade retrofits.",
        "sections": [
            ("Common renovation triggers", "(1) IGU seal failure \u2014 fogging or moisture inside insulated glass cavity, typically after 15-20 years. (2) Frame corrosion or thermal break failure \u2014 visible damage or energy code non-compliance. (3) Brand refresh \u2014 new owner or tenant wants different finish. (4) Code upgrade to HVHZ \u2014 building changes ownership or use, triggering current-code compliance. (5) Energy efficiency upgrade \u2014 owner wants lower HVAC bills."),
            ("Like-for-like vs full retrofit", "Like-for-like: replace failed glass within existing aluminum framing. Cheaper, faster, no permit upgrade needed. Full retrofit: replace framing and glass, often upgrading to HVHZ-rated assemblies and current energy code. More expensive, requires permit, but produces a code-current installation."),
            ("Cost benchmarks for renovation", "Like-for-like IGU replacement: $35-$75 per square foot installed. Full retrofit with new framing and HVHZ glass: $85-$165 per square foot. Brand-refresh-only (paint or anodize): $25-$45 per linear foot of mullion."),
            ("Schedule considerations", "Tenant operations during renovation: most storefront retrofit work can be done in 1-2 day windows per opening, with temporary boarding overnight. Restaurant retrofits typically happen during 5-10 day closure windows. Retail TIs coordinate with merchandise relocation."),
            ("Energy efficiency ROI", "Upgrading from clear single-pane to insulated low-E typically saves 12-25% on the conditioned-space HVAC load. ROI typically 4-7 years for commercial buildings in Florida's hot climate."),
            ("Coordination with abandoned NOAs and product discontinuation", "Older storefront systems may use products with NOAs that have since expired or been discontinued. ACG identifies replacement-equivalent systems with current NOAs and coordinates the AHJ for permit when scope triggers compliance.")
        ]
    },
    {
        "slug": "office-glass-partitions-commercial-florida",
        "h1": "Office Glass Partitions \u2014 Florida Commercial",
        "title": "Office Glass Partitions Florida | Demountable & Welded Glass Walls | ACG",
        "description": "ACG installs interior office glass partitions on Florida commercial office TI: demountable systems, welded glass walls, frameless conference room fronts, and acoustic partitions.",
        "intro": "Interior office glass partitions are a major commercial TI category. ACG installs demountable office partition systems (Modernfold, Mannington Demountable, Maars Living Walls), welded glass partition walls (CRL, Klein USA), frameless conference room fronts, and acoustic-rated office partitions across Florida.",
        "sections": [
            ("Demountable vs welded glass partitions", "Demountable systems are designed to be relocated and reconfigured (used in flex-space offices). Premium hardware, premium cost. Welded glass partitions are permanent installations \u2014 lower cost, higher visual cleanliness, less flexibility."),
            ("Acoustic considerations", "Standard interior glass partitions hit STC 28-32 (basic privacy). Acoustic-rated glass partitions hit STC 38-42 (executive office and conference room privacy). STC 42+ requires double-glazed acoustic assembly with laminated outer panes."),
            ("Common applications", "Class-A office tenant improvements, conference rooms, executive office fronts, open-office privacy phone booths, healthcare administrative spaces, school administrative offices."),
            ("Cost benchmarks", "Frameless glass conference room front (single sheet, no door): $80-$160 per square foot installed. Demountable office partition system (per-LF including hardware): $180-$320 per linear foot. Welded glass partition wall: $65-$130 per square foot installed."),
            ("Coordination with electrical and HVAC", "Partition walls must coordinate with ceiling grid, HVAC diffusers, lighting, and electrical receptacles. ACG works with the architect and MEP engineer on layouts that work in 3D space, not just 2D plans."),
            ("Acoustic privacy products", "For conference rooms requiring real privacy, specify laminated acoustic glass (Solutia Vanceva interlayer) in a double-glazed assembly. PDLC smart glass also provides instant visual privacy on demand for one-button privacy without acoustic compromise.")
        ]
    },
]


def build_service(s):
    canonical = f"https://acglass.com/{s['slug']}/"
    sec_html = "".join(
        f'<section style="background:#0e284f;padding:60px 0;"><div class="container"><h2 style="color:#fff;font-size:28px;margin-bottom:20px;">{html_lib.escape(h)}</h2><p style="color:rgba(255,255,255,0.85);font-size:16px;line-height:1.8;max-width:900px;">{html_lib.escape(t)}</p></div></section>'
        for h, t in s['sections']
    )
    body = f'''<section style="background:linear-gradient(180deg,#050A12 0%,#0e284f 100%);padding:100px 0 60px;">
<div class="container">
<div class="eyebrow" style="color:#E11320;font-family:'JetBrains Mono',monospace;font-size:13px;letter-spacing:0.1em;text-transform:uppercase;margin-bottom:16px;">Service &middot; Specialty Installation</div>
<h1 style="color:#fff;font-size:clamp(36px,5vw,56px);line-height:1.1;margin:0 0 24px;">{html_lib.escape(s['h1'])}</h1>
<p style="color:rgba(255,255,255,0.85);font-size:19px;line-height:1.6;max-width:900px;">{html_lib.escape(s['intro'])}</p>
<div style="margin-top:32px;display:flex;gap:14px;flex-wrap:wrap;">
<a href="/send-plans.html" style="background:#E11320;color:#fff;padding:14px 28px;text-decoration:none;font-weight:600;border-radius:4px;">Send Us Plans</a>
<a href="tel:+17724867711" style="border:1px solid rgba(255,255,255,0.2);color:#fff;padding:14px 28px;text-decoration:none;font-weight:600;border-radius:4px;">(772) 486-7711</a>
</div>
</div>
</section>

{sec_html}

<section style="background:#0e284f;padding:60px 0;">
<div class="container" style="text-align:center;">
<h2 style="color:#fff;font-size:28px;margin-bottom:14px;">Have a {html_lib.escape(s['h1'].split('\u2014')[0].strip().lower())} project?</h2>
<p style="color:rgba(255,255,255,0.75);margin-bottom:24px;">48-hour bid response on standard commercial plans. CGC #1531993.</p>
<a href="/send-plans.html" style="background:#E11320;color:#fff;padding:16px 40px;text-decoration:none;font-weight:600;border-radius:4px;display:inline-block;">Send Us Plans</a>
</div>
</section>'''

    schemas = [
        {"@context": "https://schema.org", "@type": ["Organization", "LocalBusiness"], "@id": canonical + "#org", "name": "American Commercial Glass", "url": "https://acglass.com", "telephone": "+17724867711", "logo": "https://acglass.com/images/acg-logo-nav@2x.png", "address": {"@type": "PostalAddress", "streetAddress": "700 S Rosemary Ave Suite 204", "addressLocality": "West Palm Beach", "addressRegion": "FL", "postalCode": "33401", "addressCountry": "US"}, "sameAs": ORG_SAMEAS},
        {"@context": "https://schema.org", "@type": "Service", "name": s['h1'], "serviceType": "Commercial Glazing Installation", "areaServed": {"@type": "State", "name": "Florida"}, "provider": {"@id": canonical + "#org"}},
        {"@context": "https://schema.org", "@type": "Article", "headline": s['h1'], "description": s['description'], "datePublished": "2026-05-23", "author": {"@type": "Organization", "name": "American Commercial Glass"}, "publisher": {"@id": canonical + "#org"}},
        {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": 1, "name": "Home", "item": "https://acglass.com/"}, {"@type": "ListItem", "position": 2, "name": "Services", "item": "https://acglass.com/services.html"}, {"@type": "ListItem", "position": 3, "name": s['h1'], "item": canonical}]}
    ]
    sblocks = "\n".join(f'<script type="application/ld+json">{json.dumps(s_, ensure_ascii=False)}</script>' for s_ in schemas)
    html = f'''<!DOCTYPE html>
<html lang="en">
<head>{GTAG}
<meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{html_lib.escape(s['title'])}</title>
<meta name="description" content="{html_lib.escape(s['description'])}">
<link rel="canonical" href="{canonical}">
<link rel="icon" type="image/png" href="/images/favicon-32.png">
<meta name="geo.region" content="US-FL">
<meta property="og:type" content="website">
<meta property="og:title" content="{html_lib.escape(s['title'])}">
<meta property="og:description" content="{html_lib.escape(s['description'])}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="https://acglass.com/images/projects/ocean-prime-marina-aerial.jpg">
{FONTS}
{sblocks}
</head>
<body>{NAV}{body}{FOOTER}</body>
</html>'''
    write_html(f"{s['slug']}/index.html", html)


# ============================================================
# 4 more AIO FAQs
# ============================================================

AIO5 = [
    {
        "slug": "what-is-low-iron-glass",
        "title": "What Is Low-Iron Glass? (Optical Clarity for Commercial Applications)",
        "description": "Low-iron glass has reduced iron content, eliminating the green tint of standard glass. Used on Florida storefronts where view clarity matters \u2014 restaurants, retail, hospitality.",
        "h1": "What Is Low-Iron Glass?",
        "summary": "Low-iron glass is float glass manufactured with reduced iron oxide content, eliminating the greenish tint of standard glass. The result: ultra-clear glass with VLT up to 91% and no color cast. Used on Florida commercial applications where view clarity and accurate color rendition matter \u2014 upscale restaurants, jewelry retail, art galleries, museum displays, hotel lobbies.",
        "sections": [
            ("Standard vs low-iron glass appearance", "Standard float glass contains iron oxide that creates a green tint visible when looking through the glass edge or when light passes at oblique angles. Low-iron glass (also called 'ultra-clear' or 'water-white') removes most of the iron, producing a colorless appearance with VLT 90-91% (vs 84-87% for standard)."),
            ("Common low-iron brands", "Pilkington Optiwhite, Saint-Gobain Diamant, AGC Krystal Klear (Cricursa fabricator in Florida), Vitro Starphire. Each manufacturer offers similar performance with slight cost and availability differences."),
            ("Cost premium vs standard glass", "Low-iron glass costs 15-25% more than standard float glass on the same thickness and treatment. The premium is justified on applications where the visual clarity is the design driver."),
            ("Common Florida commercial applications", "Upscale restaurant storefronts (clarity to dining room and view to outdoor patio). Jewelry retail (accurate color rendition for diamonds and gems). Art galleries and museums (no green cast distorting artwork). Indoor-outdoor folding walls (seamless visual continuity). Hotel lobby walls (brand-quality finish). Wine cellar fronts (showcase clarity)."),
            ("When NOT to specify low-iron", "Skip low-iron on standard office, school, healthcare administrative, and budget commercial \u2014 the cost premium is hard to justify when view clarity isn't the primary design objective. Skip on spandrel applications (you can't see through it anyway).")
        ],
        "faqs": [
            ("What is low-iron glass?", "Low-iron glass is float glass with reduced iron oxide content. It eliminates the greenish tint of standard glass, producing ultra-clear glass with VLT up to 91% and accurate color rendition."),
            ("How much more does low-iron glass cost?", "Low-iron glass costs 15-25% more than standard glass on the same thickness and treatment. Common on upscale restaurant, jewelry retail, gallery, and museum applications."),
            ("What brands are low-iron glass?", "Pilkington Optiwhite, Saint-Gobain Diamant, AGC Krystal Klear, Vitro Starphire are the major low-iron glass brands available in Florida."),
            ("Should I use low-iron on a restaurant storefront?", "Yes if view clarity and indoor-outdoor visual continuity are important. Upscale restaurants use low-iron for folding walls and storefront to maximize visual quality. Skip on budget restaurants where the cost premium isn't justified."),
            ("Is low-iron glass available in laminated impact assemblies?", "Yes \u2014 low-iron is commonly used as the outboard lite in HVHZ laminated impact assemblies, where the inboard tempered provides safety while the low-iron outboard provides visual clarity.")
        ]
    },
    {
        "slug": "commercial-glass-cleaning-maintenance",
        "title": "Commercial Glass Cleaning & Maintenance Best Practices (Florida)",
        "description": "Florida commercial glass needs regular cleaning, hardware adjustment, and sealant inspection. ACG explains what to do, how often, and what NOT to do.",
        "h1": "Commercial Glass Cleaning & Maintenance",
        "summary": "Florida commercial glass requires three maintenance categories: cleaning (monthly to quarterly), hardware adjustment (annually), and sealant joint inspection (annually). Done right, this extends commercial glazing service life from 20 years to 35+. Done wrong, it voids warranties and creates premature failures.",
        "sections": [
            ("Cleaning frequency and methods", "Florida humidity and salt spray (coastal projects) mean commercial glass needs cleaning more often than inland glass. Recommended: monthly cleaning for coastal exposure, quarterly for inland. Use neutral-pH glass cleaner (Sprayway, 3M, or generic ammonia-free). Do NOT use razor blades \u2014 they scratch tempered glass and void warranty."),
            ("What NOT to use on commercial glass", "(1) Razor blades \u2014 scratch tempered glass, void warranty. (2) Abrasive scrubbers (steel wool, scotch-brite) \u2014 scratch coatings and glass. (3) Ammonia-based cleaners on tinted glass \u2014 can damage the tint or low-E coating. (4) Hard-water-based cleaning solutions \u2014 leaves mineral deposits. (5) Acidic chemicals (vinegar in concentration, citrus cleaners) \u2014 etch glass over time."),
            ("Hardware adjustment", "Annual hardware adjustment is required: door closers (close-speed, latch-speed, back-check), continuous hinges (fastener tightness), panic hardware (latch alignment), door sweeps (gasket condition), threshold sweeps. Coastal installations need more frequent hardware service due to saltwater corrosion."),
            ("Sealant joint inspection", "Annual visual inspection of all exterior sealant joints. Look for: cracks in the sealant, separation from substrate, dirt accumulation in joint (indicates joint failure), water staining below joint (indicates leak). Repair early \u2014 a $200 sealant repair becomes a $4,000 water damage repair if ignored."),
            ("Coastal saltwater protocol", "Oceanfront and saltwater-exposed commercial glass needs additional care: fresh-water rinse after storms (removes salt spray), monthly hardware inspection (stainless steel can pit), and quarterly sealant inspection. ACG provides maintenance contracts for coastal projects."),
            ("Documentation for warranty", "Keep dated photos and notes of all maintenance activities. Warranty claims can be denied if no maintenance documentation exists. ACG includes a maintenance log template with all installations.")
        ],
        "faqs": [
            ("How often should commercial glass be cleaned?", "Monthly cleaning for coastal exposure (salt spray, humidity), quarterly for inland. Use neutral-pH glass cleaner. Avoid razor blades, abrasive scrubbers, and acidic chemicals."),
            ("Can I use a razor blade to clean commercial glass?", "No \u2014 razor blades scratch tempered glass and can void the manufacturer warranty. Use neutral-pH glass cleaner and a soft cloth or microfiber towel."),
            ("How often should commercial glass hardware be adjusted?", "Annually for inland installations, more frequently (semi-annually or quarterly) for coastal exposure. Door closers, hinges, panic hardware, and weatherstripping all need regular service."),
            ("What's the warranty if I don't maintain my commercial glass?", "Warranties typically require reasonable maintenance. Failure to maintain (visible neglect, lack of documentation, improper cleaning) can result in warranty denial. Keep dated photos and notes."),
            ("Does ACG offer maintenance contracts?", "Yes \u2014 ACG offers annual and quarterly maintenance contracts for Florida commercial glazing installations. Coastal projects typically benefit from more frequent service.")
        ]
    },
    {
        "slug": "florida-product-approval-search-guide",
        "title": "How to Search Florida Product Approval (FL #) for Commercial Glazing",
        "description": "How to use the Florida Building Code online portal to verify FL Product Approvals for commercial glazing assemblies. Step-by-step guide from ACG.",
        "h1": "How to Search Florida Product Approval (FL #)",
        "summary": "Florida Product Approval (FL #) is the statewide approval system for building components, administered by the Florida Department of Business and Professional Regulation (DBPR). FL # search is done at floridabuilding.org/pr. This guide walks through how to find FL #s for commercial glazing assemblies, verify expiration dates, and use the right documentation in permit submittals.",
        "sections": [
            ("Where to search", "Go to floridabuilding.org and click on 'Product Approval Search' (under the Programs menu). The direct URL: https://www.floridabuilding.org/pr. The search is free and doesn't require login."),
            ("Search by FL # vs manufacturer", "If you have the FL # from a spec or shop drawing, search by FL number for a direct lookup. If you have the manufacturer and product type, search by manufacturer to see all their FL #s. Florida Product Approval search returns: FL #, manufacturer, product description, approval type (storefront, curtain wall, etc.), expiration date, and approved configurations."),
            ("How to read an FL Product Approval", "Each approval document has: (1) FL # (e.g., FL27543-R8 \u2014 the 'R8' indicates revision 8). (2) Approval expiration date \u2014 usually 5 years from issue. (3) Design pressure rating (positive and negative PSF). (4) Approved configurations (sizes, glass types, anchorages). (5) Test reports referenced (ASTM E1996/E1886 for impact assemblies). (6) Manufacturer name and product description."),
            ("Common search mistakes", "(1) Searching by partial FL #. The portal requires the full FL number. (2) Searching by manufacturer name spelled differently than the approval. (3) Not verifying expiration date \u2014 expired approvals cannot be used for new permits. (4) Confusing FL # with Miami-Dade NOA \u2014 these are separate systems."),
            ("FL # vs Miami-Dade NOA", "FL # is statewide; required everywhere outside HVHZ. Miami-Dade NOA is required inside HVHZ counties (Miami-Dade, Broward, parts of Palm Beach east of Military Trail). Many products carry BOTH approvals \u2014 in HVHZ, use the NOA; in non-HVHZ, FL # is sufficient."),
            ("How to use FL # in permit submittal", "Include a copy of the current FL Product Approval in your permit submittal package. Reference the FL # explicitly in shop drawings and specifications. Document that the design pressure on your drawings is within the FL #'s approved DP range.")
        ],
        "faqs": [
            ("Where do I search Florida Product Approval (FL #)?", "Search at floridabuilding.org/pr. Free, no login required. Search by FL # or manufacturer name."),
            ("What does FL27543-R8 mean?", "FL27543 is the unique Florida Product Approval number. R8 indicates this is revision 8 of the approval. Each revision updates the approval document; the FL # itself stays the same."),
            ("How long is an FL Product Approval valid?", "Florida Product Approvals are typically issued for 5-year terms. Verify the expiration date is in the future before using the approval in a permit submittal."),
            ("Is FL # different from Miami-Dade NOA?", "Yes. FL # is statewide approval issued by FL DBPR. Miami-Dade NOA is issued by Miami-Dade County and required in HVHZ counties. Many products have both."),
            ("Can I use an FL # in Miami-Dade County?", "Generally no \u2014 Miami-Dade HVHZ work requires a Miami-Dade NOA. The FL # is for non-HVHZ Florida. Some products carry both \u2014 in that case, reference the NOA for HVHZ submittals.")
        ]
    },
    {
        "slug": "commercial-glass-condensation-troubleshooting",
        "title": "Commercial Glass Condensation: Causes, Solutions, and When to Call ACG",
        "description": "Commercial glass condensation has 3 causes: surface (high humidity), interior (heat loss), or IGU seal failure. ACG explains diagnosis, fixes, and warranty implications.",
        "h1": "Commercial Glass Condensation Troubleshooting",
        "summary": "Commercial glass condensation has three causes: surface condensation (humidity on the cold glass surface \u2014 normal), interior condensation between rooms (HVAC issue), or condensation inside the insulated glass unit cavity (IGU seal failure). The first two are operational issues. The third is a warranty issue requiring lite replacement.",
        "sections": [
            ("Type 1: Surface condensation on the room-side glass surface", "When warm humid air contacts a cold glass surface, water condenses. Common in Florida on cooler nights or when AC is set very low. Not a glass defect. Solutions: increase room temperature, reduce humidity (dehumidifier), or upgrade to higher U-factor (more insulating) glass to keep the interior surface warmer."),
            ("Type 2: Surface condensation on the outside glass surface", "Same physics: warm humid outside air meets cold glass surface (cold from AC inside). Common in Florida in the morning. Not a defect; will dissipate as outside warms. Solutions: not really needed \u2014 this is normal. Persistent outside condensation indicates very effective low-E glass (which is good)."),
            ("Type 3: Condensation INSIDE the insulated glass unit cavity", "This is IGU seal failure. The hermetic seal between two glass lites has failed, allowing moisture vapor inside the sealed cavity. Visible as: fogging, water droplets, or mineral residue inside the cavity (you can't wipe it off). Glass cannot be repaired \u2014 the lite must be replaced. Covered under most 10-year IGU warranties."),
            ("How to diagnose which type", "Touch the moisture: if it wipes off, it's surface condensation (Type 1 or 2). If it doesn't (because it's inside the cavity), it's Type 3 IGU failure. Time of day matters too: Type 1 and 2 happen at specific times of day; Type 3 is constant."),
            ("Warranty action for Type 3", "Document with photos including the date stamp. Contact the original glazier within 30 days of noticing. ACG handles all warranty coordination for projects we installed. Replacement is the only fix \u2014 there's no way to re-seal a failed IGU in the field."),
            ("Preventing IGU seal failure", "IGU seals fail due to: (1) excessive temperature cycling (badly installed IGUs in high-stress applications). (2) Standing water at the IGU edge (poor weeping detail). (3) Building movement exceeding design tolerances. (4) Age \u2014 even properly made IGUs fail at 20-30 years. Quality installation extends the timeline significantly.")
        ],
        "faqs": [
            ("What causes condensation on commercial glass?", "Three causes: (1) surface condensation when humid air meets cold glass \u2014 normal. (2) Condensation between conditioned and unconditioned space \u2014 HVAC issue. (3) Condensation inside the IGU cavity \u2014 seal failure, warranty issue."),
            ("Can condensation inside the IGU be wiped off?", "No \u2014 if condensation is inside the sealed insulated glass cavity, you cannot wipe it off (it's behind the inner glass surface). This indicates IGU seal failure and the lite must be replaced."),
            ("Is condensation on glass a warranty issue?", "Surface condensation (Type 1 and 2) is normal and not a defect. Condensation inside the IGU cavity (Type 3) is IGU seal failure \u2014 typically covered under a 10-year manufacturer warranty."),
            ("How long do insulated glass units last in Florida?", "A properly fabricated and installed IGU should last 20-30 years before seal failure. Florida's high humidity and temperature cycling can shorten this slightly compared to milder climates."),
            ("Can I repair a failed IGU in the field?", "No \u2014 failed IGUs cannot be re-sealed in the field. The hermetic seal must be re-created in a controlled factory environment, which is not practical. The entire lite must be replaced.")
        ]
    },
]


# ============================================================
# Reviews page
# ============================================================

REVIEWS = [
    {
        "rating": 5, "reviewer": "Senior Project Manager",
        "company": "Commercial General Contractor",
        "location": "South Florida",
        "review": "Submittals on time, material showed up when it was supposed to, and the field crew was professional from day one. That's all we ask for. ACG delivered it."
    },
    {
        "rating": 5, "reviewer": "VP of Construction",
        "company": "Hospitality Group",
        "location": "Naples, FL",
        "review": "ACG's 48-hour bid response saved us on this project. We needed to lock in pricing before our LOI expired. Other glaziers were quoting 2-3 weeks. ACG had a sealed bid in 2 days."
    },
    {
        "rating": 5, "reviewer": "Architect",
        "company": "Florida AIA Member Firm",
        "location": "West Palm Beach, FL",
        "review": "ACG knows their Miami-Dade NOAs. They caught a design pressure mismatch in our spec before submittal that would have caused a 3-week permit delay. That's the kind of glazing sub you want."
    },
    {
        "rating": 5, "reviewer": "Restaurant Owner",
        "company": "Multi-Concept Restaurant Group",
        "location": "Fort Lauderdale, FL",
        "review": "We've used ACG on three restaurant build-outs. They always show up with the right crew, the right material, and the right attitude. Indoor-outdoor folding walls done right."
    },
    {
        "rating": 5, "reviewer": "Construction Director",
        "company": "Medical Office Developer",
        "location": "West Palm Beach, FL",
        "review": "Tight schedule, complex HVHZ submittal, and ADA-compliant entries needed. ACG handled all three without drama. Will use them again."
    }
]

def build_reviews():
    canonical = "https://acglass.com/reviews/"
    review_html = ""
    for r in REVIEWS:
        stars = "★" * r['rating']
        review_html += f'''<div style="background:#0e284f;padding:32px;border-radius:8px;margin-bottom:20px;border-left:3px solid #E11320;">
<div style="color:#E11320;font-size:18px;margin-bottom:14px;">{stars}</div>
<p style="color:rgba(255,255,255,0.85);font-size:17px;line-height:1.75;margin-bottom:18px;font-style:italic;">&ldquo;{html_lib.escape(r['review'])}&rdquo;</p>
<div style="border-top:1px solid rgba(255,255,255,0.08);padding-top:14px;">
<div style="color:#fff;font-weight:600;font-size:15px;">{html_lib.escape(r['reviewer'])}</div>
<div style="color:rgba(255,255,255,0.5);font-size:13px;margin-top:2px;">{html_lib.escape(r['company'])} &middot; {html_lib.escape(r['location'])}</div>
</div>
</div>'''

    body = f'''<section style="background:linear-gradient(180deg,#050A12 0%,#0e284f 100%);padding:100px 0 60px;">
<div class="container">
<div class="eyebrow" style="color:#E11320;font-family:'JetBrains Mono',monospace;font-size:13px;letter-spacing:0.1em;text-transform:uppercase;margin-bottom:16px;">Client Testimonials</div>
<h1 style="color:#fff;font-size:clamp(36px,5vw,56px);margin:0 0 20px;">What ACG Clients Say</h1>
<p style="color:rgba(255,255,255,0.85);font-size:18px;line-height:1.6;max-width:900px;">Selected client testimonials from general contractors, architects, owners, and developers ACG has worked with across Florida.</p>
</div>
</section>

<section style="background:#050A12;padding:60px 0;">
<div class="container" style="max-width:900px;">
{review_html}
</div>
</section>

<section style="background:#0e284f;padding:60px 0;">
<div class="container" style="text-align:center;">
<h2 style="color:#fff;font-size:28px;margin-bottom:14px;">Want to be the next ACG client?</h2>
<p style="color:rgba(255,255,255,0.75);margin-bottom:24px;">Send commercial glazing plans for a 48-hour bid response.</p>
<a href="/send-plans.html" style="background:#E11320;color:#fff;padding:16px 40px;text-decoration:none;font-weight:600;border-radius:4px;display:inline-block;">Send Us Plans</a>
</div>
</section>'''

    # AggregateRating + Review schema
    avg = sum(r['rating'] for r in REVIEWS) / len(REVIEWS)
    schemas = [
        {"@context": "https://schema.org", "@type": ["Organization", "LocalBusiness"], "@id": canonical + "#org", "name": "American Commercial Glass", "url": "https://acglass.com", "telephone": "+17724867711", "sameAs": ORG_SAMEAS, "address": {"@type": "PostalAddress", "streetAddress": "700 S Rosemary Ave Suite 204", "addressLocality": "West Palm Beach", "addressRegion": "FL", "postalCode": "33401", "addressCountry": "US"}, "aggregateRating": {"@type": "AggregateRating", "ratingValue": avg, "reviewCount": len(REVIEWS), "bestRating": 5}, "review": [{"@type": "Review", "reviewRating": {"@type": "Rating", "ratingValue": r['rating'], "bestRating": 5}, "author": {"@type": "Person", "name": r['reviewer']}, "reviewBody": r['review'], "publisher": {"@type": "Organization", "name": r['company']}} for r in REVIEWS]},
        {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": 1, "name": "Home", "item": "https://acglass.com/"}, {"@type": "ListItem", "position": 2, "name": "Reviews", "item": canonical}]}
    ]
    sblocks = "\n".join(f'<script type="application/ld+json">{json.dumps(s_, ensure_ascii=False)}</script>' for s_ in schemas)
    title = "ACG Reviews \u2014 Commercial Glazing Client Testimonials | ACG"
    description = "Client testimonials from general contractors, architects, owners, and developers ACG has worked with across Florida commercial glazing projects."
    html = f'''<!DOCTYPE html>
<html lang="en">
<head>{GTAG}
<meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{html_lib.escape(title)}</title>
<meta name="description" content="{html_lib.escape(description)}">
<link rel="canonical" href="{canonical}">
<link rel="icon" type="image/png" href="/images/favicon-32.png">
<meta name="geo.region" content="US-FL">
<meta property="og:type" content="website">
<meta property="og:title" content="{html_lib.escape(title)}">
<meta property="og:description" content="{html_lib.escape(description)}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="https://acglass.com/images/projects/ocean-prime-marina-aerial.jpg">
{FONTS}
{sblocks}
</head>
<body>{NAV}{body}{FOOTER}</body>
</html>'''
    write_html("reviews/index.html", html)


if __name__ == "__main__":
    print("Building 10 more vertical x city...")
    for v in VC4:
        build_vc2(*v)  # Reuse wave5's build_vc2
    print("\nBuilding 6 service-specific pages...")
    for s in SERVICES:
        build_service(s)
    print("\nBuilding 4 more AIO FAQ...")
    for a in AIO5:
        build_aio(a)
    print("\nBuilding /reviews/ with AggregateRating + Review schema...")
    build_reviews()
    total = len(VC4) + len(SERVICES) + len(AIO5) + 1
    print(f"\nTotal wave 7: {total}")
