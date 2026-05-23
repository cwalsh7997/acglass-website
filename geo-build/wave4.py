#!/usr/bin/env python3
"""Wave 4: product-line capture pages + more AIO FAQ + press release.

Note: ACG must position carefully here \u2014 "installer" or "qualified specifier"
not "official dealer/distributor" unless we're actually authorized. We are
authorized for ESWindows/Tecnoglass, Eurowall, Allegion. For Kawneer/YKK AP/Tubelite/
EFCO we are an experienced installer (not an exclusive distributor).
"""
import os, json, sys, html as html_lib

OUT = "/home/user/workspace/acglass-website"
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from seo_sprint import build_aio

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
<div><h4>Manufacturers</h4><ul><li><a href="/eswindows-installer-florida.html">ESWindows</a></li><li><a href="/euro-wall.html">Euro-Wall</a></li><li><a href="/allegion-installer-florida.html">Allegion</a></li></ul></div>
<div><h4>Resources</h4><ul><li><a href="/resources/">Resources</a></li><li><a href="/tools/">Tools</a></li><li><a href="/glossary/">Glossary</a></li></ul></div>
<div><h4>Contact</h4><p style="color:rgba(255,255,255,0.6);font-size:14px;line-height:1.8;">(772) 486-7711<br>info@acglass.com</p></div>
</div></div></footer>'''

ORG_SAMEAS = ["https://www.wikidata.org/wiki/Q139858578", "https://acglass.ai/", "https://www.linkedin.com/company/acglass"]

# ============================================================
# Product-line capture pages
# ============================================================

PRODUCT_PAGES = [
    {
        "slug": "kawneer-installer-florida",
        "h1": "Kawneer Storefront Installer — Florida Commercial",
        "title": "Kawneer Installer Florida | Series 451T/501T/601T Commercial Storefront | ACG",
        "description": "ACG installs Kawneer Series 451T, 501T, 601T, and 701T aluminum storefront systems on Florida commercial projects. CGC #1531993, 350+ commercial installs.",
        "manufacturer": "Kawneer",
        "products": "Series 451T, 501T, 601T, 701T storefront; Trifab\u00ae and 1600 SS curtain wall; OptiQ\u00ae window wall; entrance systems; sun-control screens.",
        "blurb": "Kawneer is the most-specified commercial aluminum framing manufacturer in Florida. ACG is an experienced Florida installer with documented Kawneer projects spanning Series 451T storefront through 1600 SS curtain wall. We do not represent Kawneer exclusively \u2014 we install Kawneer when the spec calls for it or when 'or approved equal' allows us to bid it competitively.",
        "specialty": [
            "Kawneer Series 451T storefront (1-3/4\" face) for tenant improvement and budget commercial",
            "Kawneer Series 501T (2\" face) thermally-broken storefront with HVHZ NOA",
            "Kawneer Series 601T / 701T heavy-duty storefront for high-wind exposure",
            "Kawneer Trifab\u00ae 451T and 451UT curtain wall integration",
            "Kawneer 1600 SS structural silicone glazing",
            "Kawneer entrance systems with continuous hinge and panic hardware"
        ]
    },
    {
        "slug": "ykk-ap-installer-florida",
        "h1": "YKK AP Storefront Installer — Florida Commercial",
        "title": "YKK AP Installer Florida | YHS 50/60 TU Storefront, YKK Curtain Wall | ACG",
        "description": "ACG installs YKK AP YHS 50 TU, YHS 60 TU storefront systems and YKK AP unitized curtain wall on Florida commercial projects. Approved equal to Kawneer specs.",
        "manufacturer": "YKK AP",
        "products": "YHS 50 TU and YHS 60 TU storefront; YCW 750 and YCW 850 unitized curtain wall; YKK AP entrance systems; HVHZ-rated assemblies with Miami-Dade NOAs.",
        "blurb": "YKK AP is the U.S. arm of YKK Corporation. Strong in commercial storefront, window wall, and unitized curtain wall, with aggressive pricing and competitive lead times in Florida. ACG installs YKK AP systems on Florida commercial projects, frequently qualifying as approved equal to Kawneer specs.",
        "specialty": [
            "YKK AP YHS 50 TU storefront (1-3/4\" face) thermally-broken",
            "YKK AP YHS 60 TU (2-1/4\" face) thermally-broken with HVHZ NOA",
            "YKK AP YCW 750 unitized curtain wall (heavy-rise office and hotel)",
            "YKK AP YCW 850 (deeper, higher-performance unitized)",
            "YKK AP HVHZ-rated impact storefront and curtain wall",
            "Approved equal substitution coordination with architect-of-record"
        ]
    },
    {
        "slug": "solarban-installer-florida",
        "h1": "Solarban Low-E Glass Installer — Florida Commercial",
        "title": "Solarban 60, 70XL, 90 Installer Florida | Vitro Low-E Glass | ACG",
        "description": "ACG installs Solarban 60, Solarban 70XL, and Solarban 90 low-E glass by Vitro on Florida commercial projects. Class I performance for FBC Energy Code compliance.",
        "manufacturer": "Vitro (Solarban)",
        "products": "Solarban 60, Solarban 70XL, Solarban R100, Solarban 90 low-E coated glass. Class I performance products commonly specified on Florida Class-A office, hotel, hospital, and high-end commercial.",
        "blurb": "Solarban (by Vitro) is one of the dominant low-E glass coating lines specified on Florida commercial buildings. SHGC values from 0.23 down to 0.20 meet FBC Energy Conservation requirements with margin to spare. ACG sources and installs Solarban glass through approved Florida fabricators.",
        "specialty": [
            "Solarban 60 (SHGC 0.39, VLT 70%) for moderate-tint vision glass",
            "Solarban 70XL (SHGC 0.27, VLT 64%) high-performance neutral",
            "Solarban R100 silver-reflective for premium architectural appearance",
            "Solarban 90 (SHGC 0.23, VLT 51%) maximum performance Class I",
            "Insulated assemblies with surface #2 coating (Florida hot-climate position)",
            "Coordination with Vitro fabricators for HVHZ-laminated impact assemblies"
        ]
    },
    {
        "slug": "sentryglas-plus-installer-florida",
        "h1": "SentryGlas Plus Installer — Florida HVHZ Commercial",
        "title": "SentryGlas Plus Installer Florida | SGP Laminated Impact Glass | ACG",
        "description": "ACG installs laminated impact glass with SentryGlas Plus (SGP) ionoplast interlayer for HVHZ Florida commercial projects. 100x stiffer than standard PVB.",
        "manufacturer": "Kuraray (SentryGlas Plus / SGP)",
        "products": "Laminated impact-rated assemblies with SentryGlas Plus (SGP) interlayer for HVHZ Miami-Dade NOA work, high-security commercial, structural glass, and overhead glazing.",
        "blurb": "SentryGlas Plus (SGP) by Kuraray is a high-performance ionoplast interlayer used in laminated glass. 100 times stiffer than standard PVB. Used on Florida HVHZ work where post-breakage performance matters: hurricane impact glazing, security entries, structural glass railings, and overhead skylights. ACG installs SGP-laminated assemblies routinely.",
        "specialty": [
            "SGP-laminated HVHZ impact glass with Miami-Dade NOA",
            "SGP railings and balustrades (post-breakage retention required)",
            "SGP overhead and skylight glazing per FBC structural requirements",
            "SGP security glass for high-value retail (jewelry, banking, electronics)",
            "Insulated assemblies pairing SGP impact lite with low-E lite",
            "Specification consultation on PVB vs SGP interlayer trade-offs"
        ]
    },
    {
        "slug": "tubelite-installer-florida",
        "h1": "Tubelite Storefront Installer — Florida Commercial",
        "title": "Tubelite Installer Florida | T14000 Storefront, 400 Curtain Wall | ACG",
        "description": "ACG installs Tubelite T14000 storefront, 400/450 curtain wall, and Tubelite entrance systems on Florida commercial projects.",
        "manufacturer": "Tubelite",
        "products": "Tubelite T14000 storefront, T14651 thermally-broken storefront, 400 and 450 curtain wall, entrance systems. Apogee-family manufacturer with Florida fabrication.",
        "blurb": "Tubelite is an Apogee Enterprises manufacturer offering competitive commercial aluminum framing. Strong Florida presence through fabrication relationships, and frequently spec'd as 'approved equal' alternative to Kawneer. ACG installs Tubelite on Florida commercial projects.",
        "specialty": [
            "Tubelite T14000 storefront (1-3/4\" face, basic)",
            "Tubelite T14651 thermally-broken storefront with HVHZ NOA options",
            "Tubelite 400 and 450 curtain wall for mid-rise commercial",
            "Tubelite TU24650 unitized curtain wall",
            "Approved equal qualification coordination",
            "Apogee fabrication coordination for custom finishes"
        ]
    },
    {
        "slug": "efco-installer-florida",
        "h1": "EFCO Storefront Installer — Florida Commercial",
        "title": "EFCO Installer Florida | 403 Storefront, 5600 Curtain Wall | ACG",
        "description": "ACG installs EFCO 403 storefront, 5600 series curtain wall, and EFCO entrance systems on Florida commercial projects.",
        "manufacturer": "EFCO (Pella subsidiary)",
        "products": "EFCO 403 storefront, 433 thermally-broken storefront, 5600 series stick-built curtain wall, S-9000 series unitized curtain wall, EFCO entrance systems.",
        "blurb": "EFCO (a Pella subsidiary) is a long-established commercial aluminum framing manufacturer. Strong tradition in storefront and curtain wall, including HVHZ-rated assemblies. ACG installs EFCO on Florida commercial projects where the spec calls for it.",
        "specialty": [
            "EFCO 403 storefront (1-3/4\" face)",
            "EFCO 433 thermally-broken storefront",
            "EFCO 5600 stick-built curtain wall",
            "EFCO S-9000 unitized curtain wall",
            "EFCO entrance systems with continuous hinge",
            "HVHZ-rated EFCO assemblies with Miami-Dade NOAs"
        ]
    },
    {
        "slug": "viracon-installer-florida",
        "h1": "Viracon Glass Installer — Florida Commercial",
        "title": "Viracon Installer Florida | VRE Low-E, Spandrel, Laminated | ACG",
        "description": "ACG installs Viracon glass on Florida commercial projects: VRE-46, VRE-67 low-E vision glass, Viracon spandrel glass, and Viracon laminated impact assemblies.",
        "manufacturer": "Viracon (Apogee fabricator)",
        "products": "Viracon VRE-46, VRE-67, and high-performance low-E vision glass; Viracon ceramic-frit spandrel; Viracon laminated impact glass; custom-frit and digital-print glass.",
        "blurb": "Viracon is one of the largest commercial glass fabricators in North America (Apogee Enterprises). Florida architects routinely specify Viracon for Class-A office curtain wall, hotel envelopes, and high-performance commercial. ACG sources Viracon glass through approved fabrication and installs on Florida commercial work.",
        "specialty": [
            "Viracon VRE-46 (high VLT, balanced solar control)",
            "Viracon VRE-67 (premium low-E neutral appearance)",
            "Viracon ceramic-frit spandrel and shadow box",
            "Viracon laminated impact-rated assemblies for HVHZ",
            "Custom-frit digital ceramic patterns",
            "Coordination with Viracon factory tours for architect/owner mock-ups"
        ]
    },
    {
        "slug": "pilkington-installer-florida",
        "h1": "Pilkington Glass Installer — Florida Commercial",
        "title": "Pilkington Installer Florida | Pyrostop, FireLite, Energy-Efficient Glass | ACG",
        "description": "ACG installs Pilkington fire-rated glass (Pyrostop, FireLite), Pilkington Sun energy-efficient glass, and Pilkington architectural glass on Florida commercial projects.",
        "manufacturer": "Pilkington (NSG Group)",
        "products": "Pilkington Pyrostop fire-rated insulation glass; Pilkington FireLite ceramic fire-rated; Pilkington Sun and OptiTherm low-E coated glass; Pilkington Optiwhite low-iron.",
        "blurb": "Pilkington (NSG Group) is one of the world's largest architectural glass manufacturers. Known for fire-rated glazing (Pyrostop, FireLite), energy-efficient low-E (Sun, OptiTherm), and low-iron Optiwhite for high-end commercial applications. ACG installs Pilkington products on Florida commercial projects.",
        "specialty": [
            "Pilkington Pyrostop EI-rated fire-rated glazing (60-120 min)",
            "Pilkington FireLite integrity-only fire-rated (20-90 min)",
            "Pilkington Sun and OptiTherm low-E coatings",
            "Pilkington Optiwhite low-iron glass for premium clarity",
            "Pilkington Suncool reflective performance coatings",
            "Coordination with Pilkington fabricator network for Florida supply"
        ]
    },
]

def build_product_page(p):
    canonical = f"https://acglass.com/{p['slug']}/"
    spec_html = "".join(f'<li>{html_lib.escape(s)}</li>' for s in p['specialty'])
    body = f'''<section style="background:linear-gradient(180deg,#050A12 0%,#0e284f 100%);padding:100px 0 60px;">
<div class="container">
<div class="eyebrow" style="color:#E11320;font-family:'JetBrains Mono',monospace;font-size:13px;letter-spacing:0.1em;text-transform:uppercase;margin-bottom:16px;">Manufacturer &middot; Installation</div>
<h1 style="color:#fff;font-size:clamp(36px,5vw,56px);line-height:1.1;margin:0 0 24px;">{html_lib.escape(p['h1'])}</h1>
<p style="color:rgba(255,255,255,0.85);font-size:19px;line-height:1.6;max-width:900px;">{html_lib.escape(p['blurb'])}</p>
<div style="margin-top:32px;display:flex;gap:14px;flex-wrap:wrap;">
<a href="/send-plans.html" style="background:#E11320;color:#fff;padding:14px 28px;text-decoration:none;font-weight:600;border-radius:4px;">Send Us Plans</a>
<a href="tel:+17724867711" style="border:1px solid rgba(255,255,255,0.2);color:#fff;padding:14px 28px;text-decoration:none;font-weight:600;border-radius:4px;">(772) 486-7711</a>
</div>
</div>
</section>

<section style="background:#050A12;padding:60px 0;">
<div class="container" style="max-width:900px;">

<h2 style="color:#fff;font-size:26px;margin-bottom:18px;">Product lines we install</h2>
<p style="color:rgba(255,255,255,0.85);font-size:16px;line-height:1.7;margin-bottom:24px;">{html_lib.escape(p['products'])}</p>

<h2 style="color:#fff;font-size:26px;margin-bottom:18px;">Specialty applications</h2>
<ul style="color:rgba(255,255,255,0.85);font-size:16px;line-height:1.9;list-style:disc;padding-left:24px;margin-bottom:32px;">{spec_html}</ul>

<h2 style="color:#fff;font-size:26px;margin-bottom:18px;">Why specify ACG for {html_lib.escape(p['manufacturer'])} installation</h2>
<ul style="color:rgba(255,255,255,0.85);font-size:16px;line-height:1.9;list-style:disc;padding-left:24px;">
<li>Florida-licensed CGC #1531993 with documented installation experience.</li>
<li>350+ commercial projects executed across Florida.</li>
<li>48-hour bid turnaround on standard commercial plans.</li>
<li>HVHZ Miami-Dade NOA submittal experience for impact-rated assemblies.</li>
<li>Coordination with manufacturer factory tours, mock-ups, and approved-equal qualification.</li>
<li>AI-first operations: <a href="https://acglass.ai" style="color:#E11320;">acglass.ai</a></li>
</ul>

<p style="color:rgba(255,255,255,0.6);font-size:13px;line-height:1.7;margin-top:32px;font-style:italic;">Note: ACG is an experienced Florida commercial installer of {html_lib.escape(p['manufacturer'])} products. Where ACG is an exclusive authorized dealer or distributor (e.g., ESWindows/Tecnoglass, Euro-Wall, Allegion), this relationship is explicitly stated on the relevant dealer pages. For other manufacturers, ACG installs their products when specified by architect or when 'approved equal' allows competitive bid.</p>

</div>
</section>

<section style="background:#0e284f;padding:60px 0;">
<div class="container" style="text-align:center;">
<h2 style="color:#fff;font-size:28px;margin-bottom:14px;">Have a {html_lib.escape(p['manufacturer'])}-spec project?</h2>
<p style="color:rgba(255,255,255,0.75);margin-bottom:24px;">Send plans for a 48-hour bid response.</p>
<a href="/send-plans.html" style="background:#E11320;color:#fff;padding:16px 40px;text-decoration:none;font-weight:600;border-radius:4px;display:inline-block;">Send Us Plans</a>
</div>
</section>'''

    schemas = [
        {"@context": "https://schema.org", "@type": ["Organization", "LocalBusiness"], "@id": canonical + "#org", "name": "American Commercial Glass", "url": "https://acglass.com", "telephone": "+17724867711", "sameAs": ORG_SAMEAS, "address": {"@type": "PostalAddress", "streetAddress": "700 S Rosemary Ave Suite 204", "addressLocality": "West Palm Beach", "addressRegion": "FL", "postalCode": "33401", "addressCountry": "US"}},
        {"@context": "https://schema.org", "@type": "Service", "name": p['h1'], "serviceType": "Commercial Glazing Installation", "areaServed": {"@type": "State", "name": "Florida"}, "provider": {"@id": canonical + "#org"}},
        {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": 1, "name": "Home", "item": "https://acglass.com/"}, {"@type": "ListItem", "position": 2, "name": "Manufacturers", "item": "https://acglass.com/manufacturers.html"}, {"@type": "ListItem", "position": 3, "name": p['manufacturer'], "item": canonical}]}
    ]
    sblocks = "\n".join(f'<script type="application/ld+json">{json.dumps(s, ensure_ascii=False)}</script>' for s in schemas)
    html = f'''<!DOCTYPE html>
<html lang="en">
<head>{GTAG}
<meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{html_lib.escape(p['title'])}</title>
<meta name="description" content="{html_lib.escape(p['description'])}">
<link rel="canonical" href="{canonical}">
<link rel="icon" type="image/png" href="/images/favicon-32.png">
<meta name="geo.region" content="US-FL">
<meta property="og:type" content="website">
<meta property="og:title" content="{html_lib.escape(p['title'])}">
<meta property="og:description" content="{html_lib.escape(p['description'])}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="https://acglass.com/images/projects/ocean-prime-marina-aerial.jpg">
{FONTS}
{sblocks}
</head>
<body>{NAV}{body}{FOOTER}</body>
</html>'''
    full = os.path.join(OUT, p['slug'], "index.html")
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"  Wrote /{p['slug']}/")


# ============================================================
# Wave 3 AIO FAQs
# ============================================================

AIO3 = [
    {
        "slug": "what-is-window-wall-system",
        "title": "What Is a Window Wall System? (Window Wall vs Curtain Wall)",
        "description": "Window wall sits on the floor slab; curtain wall hangs from the slab edge. ACG explains the difference, when to spec each, and 2026 cost.",
        "h1": "What Is a Window Wall System?",
        "summary": "Window wall is an aluminum-and-glass framing system that sits on top of the floor slab and runs floor-to-ceiling within a single floor. It looks similar to curtain wall from the exterior, but structurally it's installed floor-by-floor (not hung from the slab edge). Window wall is common on multi-family residential and mixed-use mid-rise, where each unit's facade installs independently and the structural connection is at the floor below.",
        "sections": [
            ("How window wall actually works structurally", "Window wall sits on the floor slab and supports its own weight on that slab. The next floor up has its own independent window wall sitting on its own slab. There's typically a sealant joint at the slab line between floors. Compare to curtain wall, which hangs from the slab edge and spans floor-to-floor as a continuous skin."),
            ("Window wall vs curtain wall: when to choose each", "Window wall: multi-family residential, mixed-use ground floor with units above, mid-rise hotel. Cost-efficient. Simpler structural engineering. Easier punch-out by floor. Curtain wall: Class-A office, luxury hotel, taller commercial. Continuous facade appearance. Higher engineering and cost."),
            ("Window wall cost in Florida", "Window wall typically costs $80-$160/SF installed in Florida \u2014 between standard storefront ($66-$142) and curtain wall ($95-$240). Cost varies with glass type, HVHZ rating, and finish."),
            ("Common window wall systems on Florida projects", "Kawneer 1600 Window Wall, YKK AP YWW 60 T, Tubelite 400, EFCO 8700 \u2014 these are the most-spec'd. All available with HVHZ-rated Miami-Dade NOA assemblies."),
            ("Window wall sealant detailing is critical", "The horizontal joint at each floor slab is where window wall systems can leak. Florida humidity, temperature swings, and storm-driven rain stress this joint. Specify pressure-equalized window wall (not face-sealed) and high-performance sealants (Dow 795 silicone or equivalent).")
        ],
        "faqs": [
            ("What is a window wall system?", "Window wall is an aluminum-and-glass framing system that sits on the floor slab and runs floor-to-ceiling within a single floor. It looks like curtain wall but installs floor-by-floor with independent structural support at each slab."),
            ("What's the difference between window wall and curtain wall?", "Window wall sits on the floor slab and supports its own weight at each floor. Curtain wall hangs from the slab edge and spans multiple floors as a continuous skin. Window wall is cheaper and simpler; curtain wall is more architecturally dramatic and required for taller buildings."),
            ("Is window wall good for hotels?", "Yes, mid-rise hotels (typically 4-12 stories) often use window wall to balance cost and appearance. High-rise hotels (typically 12+ stories) usually use curtain wall for continuous facade appearance."),
            ("Does window wall cost less than curtain wall?", "Yes \u2014 window wall typically costs $80-$160/SF in Florida vs $95-$240/SF for curtain wall. The savings come from simpler structural engineering, smaller mullion depth, and floor-by-floor installation."),
            ("Can window wall be HVHZ-rated?", "Yes \u2014 Kawneer, YKK AP, Tubelite, and EFCO all offer HVHZ-rated window wall systems with Miami-Dade NOAs. Confirm the specific NOA is current and matches the project design pressure before specification.")
        ]
    },
    {
        "slug": "best-glass-for-restaurant-storefronts-florida",
        "title": "Best Glass for Restaurant Storefronts in Florida (2026 Guide)",
        "description": "The best glass for Florida restaurant storefronts is impact-rated laminated low-E in coastal counties, low-iron clear vision glass for indoor-outdoor concepts. ACG breaks down the choices.",
        "h1": "Best Glass for Restaurant Storefronts in Florida",
        "summary": "The best glass for a Florida restaurant storefront depends on three factors: location (HVHZ, WBDR, or inland), concept (indoor-outdoor or sealed envelope), and brand finish standards. For coastal restaurants, laminated impact glass is required by code. For indoor-outdoor concepts, low-iron tempered glass on folding walls maximizes view clarity. For brand-quality urban restaurants, low-E coated laminated impact insulated assemblies deliver code, energy, and finish.",
        "sections": [
            ("Decision factor 1: location and code", "HVHZ counties (Miami-Dade, Broward, parts of Palm Beach): laminated impact glass with Miami-Dade NOA is required. WBDR coastal: laminated impact glass meeting ASTM E1996/E1886 is required. Inland Florida: impact glass is optional; standard tempered or insulated low-E meets code."),
            ("Decision factor 2: concept (indoor-outdoor vs sealed)", "Indoor-outdoor concept (folding walls, multi-slide doors): low-iron clear tempered or laminated. Low-iron eliminates the green tint of standard glass, making the indoor-outdoor visual seamless. Sealed envelope: insulated low-E laminated impact assemblies (standard for high-end restaurants in HVHZ)."),
            ("Decision factor 3: brand finish standards", "Most national restaurant brands have brand-standard glass specifications. Hillstone, Cipriani, Carbone, Major Food Group, Hakkasan \u2014 each has finish requirements that constrain glass selection. ACG translates brand standards into Florida code-compliant assemblies."),
            ("Specific glass recommendations by concept type", "Steakhouse / upscale: low-E laminated impact with low-iron outboard for max clarity. Fast-casual: standard tempered or low-E IG (budget-driven). Outdoor-focused restaurant: low-iron folding walls or multi-slide doors, impact-rated where required. Rooftop / terrace: laminated SGP for railings, laminated impact for storefront-style enclosures."),
            ("Solar control on south- and west-facing restaurant facades", "Florida sun on south and west facades is intense. Specify low-E with SHGC \u2264 0.27 to reduce HVAC load and prevent customer discomfort at window tables. Tinted glass (bronze, gray) is older-style; modern low-E performs better without the dark appearance."),
            ("Anti-smash-grab for urban restaurants", "Urban restaurants with high-value contents (wine, electronics behind bars) benefit from laminated glass with thicker interlayers \u2014 the laminated lite holds together if struck with a hammer or brick. ACG specifies laminated SGP for security-sensitive restaurants.")
        ],
        "faqs": [
            ("What's the best glass for a Florida restaurant storefront?", "For HVHZ and coastal restaurants: laminated impact glass with Miami-Dade NOA. For indoor-outdoor concepts with folding walls: low-iron clear tempered or laminated. For brand-driven urban restaurants: low-E coated laminated impact insulated assemblies."),
            ("Is low-iron glass worth the cost premium for restaurants?", "For indoor-outdoor concepts and high-end restaurants where view clarity matters, low-iron glass is worth the 15-25% cost premium. It eliminates the green tint of standard glass, making patio openings and storefront views noticeably clearer."),
            ("Do Florida restaurants need impact glass?", "In HVHZ counties (Miami-Dade, Broward, parts of Palm Beach) and Wind-Borne Debris Region: yes, impact glass or rated shutters are required by code. Inland Florida: impact glass is optional but still a smart investment for storm protection."),
            ("What glass do upscale steakhouses typically use?", "Upscale steakhouses (Ocean Prime, Eddie V's, Major Food Group concepts) typically use low-E coated laminated impact insulated assemblies with low-iron outboard lite. This delivers code compliance, energy performance, and maximum view clarity."),
            ("How thick should restaurant storefront glass be?", "Typical Florida restaurant storefront uses 1-inch insulated glass units (IG) with 1/4-inch outboard tempered + 1/2-inch air space + 1/4-inch inboard tempered. For HVHZ work, the outboard lite is replaced with laminated impact (typically 1/4\" + .090 PVB + 1/4\").")
        ]
    },
    {
        "slug": "smart-glass-explained-florida-commercial",
        "title": "Smart Glass Explained: SPD, PDLC, Electrochromic for Florida Commercial",
        "description": "Smart glass (SPD, PDLC, electrochromic) electronically tints or switches between clear and opaque. ACG explains the three technologies, cost, and Florida applications.",
        "h1": "Smart Glass for Florida Commercial Buildings",
        "summary": "Smart glass electronically controls light transmission \u2014 either tinting on demand (electrochromic) or switching between transparent and opaque (PDLC, SPD). Three dominant technologies: electrochromic (View, SageGlass), PDLC liquid crystal (Smart Tint, Switchable Glass), and SPD suspended particle device (Research Frontiers, Halio). Costs run $75-$200/SF on top of standard glass costs. Used on Class-A office, healthcare privacy, executive office fronts, and hospitality lounges.",
        "sections": [
            ("Electrochromic glass (View, SageGlass)", "Electrochromic glass tints on demand by passing a low voltage across a thin coating between two glass lites. Tint levels are gradient (clear to dark). The tint persists with low power draw. Used for solar control on south and west facades, replacing manual shades and reducing HVAC load. Cost: $75-$150/SF premium over standard glass."),
            ("PDLC liquid crystal glass (Smart Tint, Switchable Glass)", "PDLC glass switches between transparent and opaque (frosted) by aligning or scattering liquid crystals between two films. Operates in two states: on (clear) or off (opaque). Used for executive office privacy, conference room walls, hospital exam rooms, and hotel bathrooms. Cost: $90-$180/SF premium."),
            ("SPD suspended particle device (Halio, Research Frontiers)", "SPD glass uses suspended microscopic particles that align (clear) or disperse (dark) with voltage. Continuous gradient from clear to dark in 1-3 seconds. Used for high-end office, executive transportation (yachts, jets), and luxury residential. Cost: $120-$200/SF premium."),
            ("When smart glass makes sense on Florida commercial", "Executive office privacy with one switch. Conference room walls that need privacy on demand. Healthcare exam rooms (instant privacy without curtains). Hotel suite bathrooms (frosted when occupied). South-facing Class-A office for solar control. Hospitality private dining."),
            ("Limitations and gotchas", "Smart glass requires power, control wiring, and a switch or building automation interface. Failures (very rare) require lite replacement, not field repair. Long-term reliability is well-documented now (10+ years) but warranty terms vary by manufacturer. HVHZ-rated smart glass requires factory-bonded assemblies that include the smart film/coating.")
        ],
        "faqs": [
            ("What is smart glass?", "Smart glass electronically controls light transmission, either tinting on demand (electrochromic) or switching between transparent and opaque (PDLC, SPD). It eliminates the need for manual shades, curtains, or blinds."),
            ("What's the difference between electrochromic, PDLC, and SPD?", "Electrochromic tints gradient (clear to dark, for solar control). PDLC switches between transparent and opaque (frosted, for privacy). SPD does a fast gradient (1-3 seconds) from clear to dark. Each has different use cases and cost points."),
            ("How much does smart glass cost?", "Smart glass adds $75-$200/SF on top of standard glass costs. Electrochromic: $75-$150/SF. PDLC: $90-$180/SF. SPD: $120-$200/SF. Cost varies with manufacturer, sizes, and integration complexity."),
            ("Can smart glass be installed in HVHZ buildings?", "Yes, but HVHZ-rated smart glass requires factory-bonded assemblies that integrate the smart film or coating with the laminated impact glass. Confirm the manufacturer has a current Miami-Dade NOA before specification."),
            ("Where does smart glass make sense on commercial buildings?", "Executive office privacy, conference room walls, healthcare exam rooms, hotel suite bathrooms, south-facing Class-A office solar control, and high-end hospitality private dining are the most common Florida commercial applications.")
        ]
    },
    {
        "slug": "glass-railing-systems-florida",
        "title": "Glass Railing Systems for Florida Commercial (Code, Cost, Brands)",
        "description": "Glass railings on Florida commercial projects require structural laminated glass, 50 lb/ft load capacity, and approved post-and-shoe systems. ACG explains the options.",
        "h1": "Glass Railing Systems for Florida Commercial",
        "summary": "Florida commercial glass railings must meet two engineering requirements: 50 lb/ft horizontal load capacity per IBC, and structural laminated glass that maintains integrity after breakage per ASTM E2353. Common systems: C.R. Laurence (CRL) Taper-Loc and B-Series, Trex Signature, AGS Stainless Clearview, and Q-railing Easy Glass. Cost typically $200-$450 per linear foot installed.",
        "sections": [
            ("Code requirements for commercial glass railings", "IBC 2018+ and FBC require glass railings to: (1) handle 50 lb/ft horizontal load applied at the top, (2) handle 200 lb concentrated load at any point, (3) use structural laminated glass (typically 1/2\" + .060 PVB + 1/2\" tempered minimum), and (4) include a top cap or rail unless the system is engineered for the load without one."),
            ("Common railing systems on Florida commercial", "C.R. Laurence (CRL) Taper-Loc: fast install, dry-set system, no wet cement, common on Florida residential and commercial. CRL B-Series base shoe: high-performance dry-glazed shoe. Trex Signature: aluminum top-rail aesthetic, structural laminated glass infill. AGS Stainless Clearview: marine-grade stainless steel post and shoe systems for coastal/saltwater exposure. Q-railing Easy Glass: European-style minimal-profile shoe systems."),
            ("Post-mounted vs base-shoe railings", "Post-mounted railings have individual posts every 4-6 feet with glass infill panels. Cheaper and easier to install. Base-shoe railings have continuous floor-mounted shoes holding the glass directly \u2014 cleaner appearance but more expensive and requires precise structural anchorage to substrate."),
            ("Cost benchmarks (per linear foot installed)", "Basic post-and-glass railing: $200-$280/LF. CRL Taper-Loc base shoe with 1/2\" laminated glass: $260-$360/LF. CRL B-Series base shoe: $310-$420/LF. AGS Stainless Clearview (marine grade): $350-$500/LF. Custom top-rail aesthetic systems: $400-$650/LF."),
            ("Saltwater / coastal considerations", "Florida coastal projects (beach hotels, oceanfront condos, marina restaurants) need marine-grade stainless steel hardware. Standard galvanized or powder-coated steel will fail within 5-10 years in saltwater spray exposure. AGS Stainless and CRL marine-grade product lines address this. Cost premium: 25-40% over standard."),
            ("Maintenance and warranty considerations", "Glass railings are low-maintenance but require periodic re-tightening of fasteners (annual on coastal projects, every 3-5 years inland). Glass panels can be replaced individually if damaged. ACG offers 1-year workmanship warranty extending to 5 years with maintenance contract.")
        ],
        "faqs": [
            ("What glass is used for commercial railings?", "Commercial glass railings use structural laminated tempered glass \u2014 typically 1/2\" + .060 PVB + 1/2\" tempered minimum. The laminated structure maintains integrity after breakage, which is critical for life-safety railings."),
            ("How much do glass railings cost in Florida?", "Florida commercial glass railings typically cost $200-$450 per linear foot installed. Marine-grade stainless steel hardware for coastal projects adds 25-40%. Custom architectural systems can exceed $650/LF."),
            ("What's the load requirement for commercial glass railings?", "Commercial glass railings must handle 50 lb/ft horizontal load applied at the top, plus 200 lb concentrated load at any point. The full assembly (glass + posts + base shoe + anchorage) must be engineered to these loads per IBC and FBC."),
            ("What brands of glass railings are common in Florida?", "C.R. Laurence (CRL), Trex Signature, AGS Stainless, and Q-railing are the most commonly specified glass railing systems on Florida commercial projects. CRL Taper-Loc is particularly common for fast-install dry-set applications."),
            ("Are SGP interlayers required for glass railings?", "Standard PVB interlayer is acceptable for most commercial railing applications. SGP (SentryGlas Plus) interlayer is required where the railing is structural (no separate top rail) or where post-breakage retention is critical \u2014 the SGP holds the broken laminate together better than PVB.")
        ]
    },
    {
        "slug": "automatic-door-operators-commercial-florida",
        "title": "Automatic Door Operators for Commercial Storefront (Florida 2026)",
        "description": "Automatic door operators on Florida commercial storefronts deliver ADA compliance, hands-free entry, and accessibility. ACG explains swing vs slide, cost, and code.",
        "h1": "Automatic Door Operators for Commercial Storefront",
        "summary": "Automatic door operators electromechanically open and close storefront doors based on motion sensor, push button, or smart access trigger. Two main types: automatic swing operators (one or two leaves, swing open) and automatic sliding doors (telescoping or biparting). Required at primary entrances on most Florida commercial buildings to meet ADA 5-pound opening force, often easier than manually adjusting closer hardware.",
        "sections": [
            ("Swing operators (Stanley, Besam/ASSA ABLOY, Horton)", "Swing-door operators install above the door header and pivot the door open via push-button or motion sensor. Stanley MagicSwing, ASSA ABLOY Besam SW100, and Horton 7000 series are the dominant brands. Pricing: $1,800-$4,200 per door installed."),
            ("Sliding operators (Stanley, Besam, Horton)", "Sliding operators handle telescoping (sliding panels) or biparting (two panels opening from center) sliders. Used at high-volume entries (grocery, retail, hospital). Stanley StanleyDura-Glide, Besam SL500, Horton ProSlide. Pricing: $4,500-$12,000 per sliding entry installed."),
            ("ADA compliance and operator activation", "Push-button activation must be 36-48 inches above floor, with the button mounted 60 inches from the door's swing arc (so it can be activated from a wheelchair without being in the door path). Motion sensor activation must include sufficient time delay for slower users."),
            ("Florida storm and humidity considerations", "Florida operators need to handle high humidity, salt spray (coastal), and storm-driven wind loads. Specify operators with sealed housings (IP54 minimum) and Florida-rated components. Specify operators with built-in wind detection that pauses operation in high winds (prevents the door from being slammed)."),
            ("Maintenance and warranty", "Auto operators need annual maintenance (motor brush check, sensor calibration, threshold adjustment). Standard warranty: 1-2 years parts and labor. Extended warranties available. Plan for 3-5 year operator replacement on high-traffic entries."),
            ("Integration with access control", "Modern auto operators integrate with electronic access control \u2014 card readers, badge systems, smart phone unlock. Schlage, Allegion, and HID Global all interface with major auto operator brands. Specify the integration interface (Wiegand, RS-485, OSDP) during the design phase.")
        ],
        "faqs": [
            ("What is an automatic door operator?", "An automatic door operator electromechanically opens and closes a storefront door based on motion sensor, push button, or smart access trigger. They're used to meet ADA 5-pound opening force requirements and improve accessibility at commercial entries."),
            ("How much does an automatic door operator cost?", "Automatic swing operators cost $1,800-$4,200 per door installed. Automatic sliding operators cost $4,500-$12,000 per entry. Pricing depends on traffic capacity, ADA compliance level, and operator brand."),
            ("Are automatic door operators required by ADA?", "Not strictly required by ADA, but they are the most reliable way to meet the 5-pound opening force requirement on heavy exterior doors. Many Florida AHJs strongly recommend or effectively require auto operators on primary commercial entries."),
            ("What brands of operators are common in Florida?", "Stanley (now Allegion), ASSA ABLOY Besam, and Horton are the dominant commercial automatic door operator brands. Stanley MagicSwing and Besam SW100 are the most-installed swing operators in Florida."),
            ("How often do auto operators need maintenance?", "Annual maintenance is the standard \u2014 motor brush check, sensor calibration, threshold and gasket inspection. High-traffic entries (grocery, hospital) may need quarterly maintenance.")
        ]
    },
    {
        "slug": "blast-resistant-glazing-florida",
        "title": "Blast-Resistant Glazing for Florida Commercial (GSA Standards)",
        "description": "Blast-resistant glazing protects building occupants from explosion overpressure and debris. ACG explains GSA Level C/D, ASTM F1642 testing, and Florida applications.",
        "h1": "Blast-Resistant Glazing for Florida Commercial",
        "summary": "Blast-resistant glazing is engineered to maintain integrity during explosion events, protecting occupants from overpressure and flying glass debris. Required on federal facilities, courthouses, and some financial/public buildings. Tested to ASTM F1642 and GSA Performance Conditions (Levels A through F). Common in Florida on federal courthouses, military installations, and high-security commercial.",
        "sections": [
            ("How blast-resistant glazing works", "Blast-resistant glass is heavily laminated, typically with multiple PVB or SGP interlayers, and engineered to absorb explosion energy. The framing system is reinforced (steel-back-aluminum or all-steel) and engineered to retain the glass even under extreme overpressure. The full assembly (glass + frame + anchorage) is tested as a unit."),
            ("ASTM F1642 testing", "ASTM F1642 measures glazing performance under blast loading. Test uses an actual explosive charge or air-blast simulator. Results categorize performance from 'no breakage' through 'breakage but retained' through 'failure.' Most commercial blast-rated glazing achieves 'breakage but retained' performance."),
            ("GSA Performance Conditions A-F", "GSA Level A: no glass breakage. Level B: minor breakage, no fragment hazard. Level C: glass breakage, fragments fall within 36 inches of frame (typical office spec). Level D: fragments fall within 36 inches up to 3 feet above floor (common commercial spec). Level E and F: increasing degrees of fragment hazard, used only on legacy non-compliant buildings."),
            ("Common product systems", "Custom laminated assemblies from Viracon, Insulgard Security, Saint-Gobain Glass: 1\" to 2\" thick laminated assemblies with SGP interlayers. Common framing partners: Trussbuilt steel, Architectural Armor, custom-fabricated steel-back-aluminum systems. Cost: 8-20x standard commercial glazing on the same opening size."),
            ("Florida applications", "Federal courthouses in Miami, Orlando, Tampa, Jacksonville. Military installations (Pensacola NAS, MacDill AFB Tampa, Naval Station Mayport). Some financial sector (bank trading floors, federal reserve operations). High-security corporate (research facilities, data centers). Federal embassy buildings."),
            ("Why blast-rated is rarely on commercial work", "Standard commercial doesn't need it. Blast-rated glazing is a specialty product for federal and security-sensitive applications. For typical Florida commercial buildings (retail, office, restaurant, hotel), standard impact-rated glass meets life-safety requirements without the blast-rated premium.")
        ],
        "faqs": [
            ("What is blast-resistant glazing?", "Blast-resistant glazing is heavily laminated glass engineered to maintain integrity during explosion events, protecting building occupants from overpressure and flying glass fragments. Tested to ASTM F1642 and GSA Performance Conditions."),
            ("Where is blast-resistant glazing required?", "Federal courthouses, military installations, high-security commercial, financial trading floors, and certain critical infrastructure. Not required on standard commercial buildings (retail, office, restaurant, hotel)."),
            ("What's the difference between blast-resistant and impact-resistant glass?", "Impact-resistant glass is tested for windborne debris (storm hazard). Blast-resistant glass is tested for explosion overpressure (security hazard). Some blast-rated assemblies also meet impact rating, but the testing standards are different."),
            ("How much does blast-resistant glazing cost?", "Blast-resistant glazing typically costs 8-20x standard commercial glazing on the same opening size, due to thicker laminated assemblies, reinforced framing, and specialty fabrication."),
            ("What are GSA Performance Conditions?", "GSA Performance Conditions A through F classify blast-glazing performance from no breakage (A) through increasing degrees of fragment hazard. Level C and D are typical commercial blast specs.")
        ]
    },
]

if __name__ == "__main__":
    print("Building product-line capture pages...")
    for p in PRODUCT_PAGES:
        build_product_page(p)
    print("\nBuilding wave 3 AIO FAQ pages...")
    for p in AIO3:
        build_aio(p)
    total = len(PRODUCT_PAGES) + len(AIO3)
    print(f"\nTotal wave 4: {total} pages.")
