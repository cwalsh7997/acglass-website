#!/usr/bin/env python3
"""Wave 6: more sub-city pages, more AIO, vertical x city wave 3, master pillar."""
import os, json, html as html_lib

OUT = "/home/user/workspace/acglass-website"

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
# More sub-city / neighborhood pages
# ============================================================

SUBCITY = [
    ("westshore-tampa", "Westshore", "tampa", "Tampa", 27.9595, -82.5085, "Hillsborough",
        "Westshore is Tampa's primary office and hospitality submarket \u2014 Westshore Plaza, International Plaza, and corporate office towers along Cypress Street and Westshore Boulevard. Strong Class-A office and ground-floor retail commercial market."),
    ("channelside-tampa", "Channelside", "tampa", "Tampa", 27.9477, -82.4470, "Hillsborough",
        "Channelside is downtown Tampa's waterfront entertainment and mixed-use district adjacent to Water Street. Strong restaurant, retail, and ground-floor commercial market with brand-driven storefront work."),
    ("davis-islands-tampa", "Davis Islands", "tampa", "Tampa", 27.9295, -82.4607, "Hillsborough",
        "Davis Islands is Tampa's island community south of downtown \u2014 mix of residential, marina, and small commercial. Boutique retail and restaurant storefront work."),
    ("coral-gables-miracle-mile", "Miracle Mile", "coral-gables", "Coral Gables", 25.7506, -80.2592, "Miami-Dade",
        "Miracle Mile is Coral Gables' historic main retail and dining street \u2014 boutique retail, restaurants, and ground-floor commercial in landmark mediterranean-revival buildings. Sensitive City of Coral Gables design review."),
    ("aventura-mall-area", "Aventura Mall Area", "aventura", "Aventura", 25.9576, -80.1432, "Miami-Dade",
        "Aventura Mall is one of Florida's largest luxury malls. Surrounding commercial (Williams Island, Aventura Hospital, office) drives ongoing storefront, curtain wall, and impact-rated work. HVHZ."),
    ("coconut-grove-miami", "Coconut Grove", "miami", "Miami", 25.7282, -80.2434, "Miami-Dade",
        "Coconut Grove is Miami's historic waterfront village \u2014 CocoWalk, Mayfair in the Grove, ground-floor restaurant and boutique retail. Sensitive design review and HVHZ NOA required."),
    ("lake-nona-orlando", "Lake Nona", "orlando", "Orlando", 28.3989, -81.2378, "Orange",
        "Lake Nona is southeast Orlando's medical city and innovation district \u2014 Nemours Children's Hospital, VA Medical Center, USTA National Campus, and rapid commercial buildout. Strong medical office and ground-floor retail."),
    ("winter-park-park-ave", "Park Avenue Winter Park", "winter-park", "Winter Park", 28.5949, -81.3530, "Orange",
        "Park Avenue is Winter Park's upscale retail and restaurant boulevard \u2014 Tiffany, Pottery Barn, boutique fashion, fine dining. Park Avenue Area Association design review. Sensitive historic district context."),
    ("downtown-doral", "Downtown Doral", "doral", "Doral", 25.8195, -80.3553, "Miami-Dade",
        "Downtown Doral is the master-planned commercial center of Doral \u2014 office, retail, hotel, and ground-floor restaurant. HVHZ requirements. Brand-driven national chain rollouts."),
    ("brickell-key-miami", "Brickell Key", "miami", "Miami", 25.7677, -80.1854, "Miami-Dade",
        "Brickell Key is the island-condominium and resort community adjacent to Brickell \u2014 Mandarin Oriental hotel and luxury residential ground-floor commercial. HVHZ severe.")
]

def schema_subcity(canonical, name, lat, lng, parent, county):
    return [
        {
            "@context": "https://schema.org",
            "@type": ["Organization", "LocalBusiness"],
            "@id": canonical + "#org",
            "name": "American Commercial Glass",
            "url": "https://acglass.com",
            "telephone": "+17724867711",
            "logo": "https://acglass.com/images/acg-logo-nav@2x.png",
            "address": {"@type": "PostalAddress", "streetAddress": "700 S Rosemary Ave Suite 204", "addressLocality": "West Palm Beach", "addressRegion": "FL", "postalCode": "33401", "addressCountry": "US"},
            "sameAs": ORG_SAMEAS,
            "areaServed": {"@type": "Place", "name": f"{name}, {parent}, FL", "geo": {"@type": "GeoCoordinates", "latitude": lat, "longitude": lng}}
        },
        {
            "@context": "https://schema.org",
            "@type": "Service",
            "name": f"Commercial Storefront Glazier \u2014 {name}",
            "serviceType": "Commercial Glazing",
            "areaServed": f"{name}, FL",
            "provider": {"@id": canonical + "#org"}
        }
    ]

def build_subcity(slug, name, parent_slug, parent, lat, lng, county, blurb):
    canonical = f"https://acglass.com/{parent_slug}/{slug}/"
    body = f'''<section style="background:linear-gradient(180deg,#050A12 0%,#0e284f 100%);padding:100px 0 60px;">
<div class="container">
<div class="eyebrow" style="color:#E11320;font-family:'JetBrains Mono',monospace;font-size:13px;letter-spacing:0.1em;text-transform:uppercase;margin-bottom:16px;">Neighborhood &middot; {html_lib.escape(parent)}, FL</div>
<h1 style="color:#fff;font-size:clamp(32px,5vw,52px);line-height:1.1;margin:0 0 24px;">Storefront Glazier \u2014 {html_lib.escape(name)}</h1>
<p style="color:rgba(255,255,255,0.85);font-size:19px;line-height:1.6;max-width:900px;">{html_lib.escape(blurb)}</p>
<div style="margin-top:32px;display:flex;gap:14px;flex-wrap:wrap;">
<a href="/send-plans.html" style="background:#E11320;color:#fff;padding:14px 28px;text-decoration:none;font-weight:600;border-radius:4px;">Send Us Plans</a>
<a href="tel:+17724867711" style="border:1px solid rgba(255,255,255,0.2);color:#fff;padding:14px 28px;text-decoration:none;font-weight:600;border-radius:4px;">(772) 486-7711</a>
</div>
</div>
</section>

<section style="background:#050A12;padding:60px 0;">
<div class="container" style="max-width:900px;">
<h2 style="color:#fff;font-size:26px;margin-bottom:18px;">Services in {html_lib.escape(name)}</h2>
<ul style="color:rgba(255,255,255,0.85);font-size:16px;line-height:1.9;list-style:disc;padding-left:24px;margin-bottom:32px;">
<li>Aluminum commercial storefront (Kawneer, YKK AP, Tubelite, EFCO)</li>
<li>Curtain wall and window wall systems</li>
<li>Impact-rated windows</li>
<li>All-glass entrances</li>
<li>Folding glass walls and multi-slide doors (restaurant indoor-outdoor)</li>
<li>Glass railings for terraces and stairs</li>
</ul>

<h2 style="color:#fff;font-size:26px;margin-bottom:18px;">Permit context</h2>
<p style="color:rgba(255,255,255,0.85);font-size:16px;line-height:1.7;margin-bottom:24px;">{html_lib.escape(name)} is in {html_lib.escape(parent)}, {html_lib.escape(county)} County, FL. See our <a href="/{parent_slug}/" style="color:#E11320;">{html_lib.escape(parent)} commercial storefront page</a> for full code and AHJ context.</p>

<h2 style="color:#fff;font-size:26px;margin-bottom:18px;">Why ACG</h2>
<ul style="color:rgba(255,255,255,0.85);font-size:16px;line-height:1.9;list-style:disc;padding-left:24px;">
<li>Florida-licensed CGC #1531993 with 350+ commercial projects.</li>
<li>48-hour bid turnaround on standard commercial plans.</li>
<li>Documented HVHZ/WBDR submittal experience.</li>
<li>AI-first operations stack: <a href="https://acglass.ai" style="color:#E11320;">acglass.ai</a></li>
</ul>
</div>
</section>'''
    schemas = schema_subcity(canonical, name, lat, lng, parent, county)
    bc = [("Home", "https://acglass.com/"), (parent, f"https://acglass.com/{parent_slug}/"), (name, canonical)]
    schemas.append({"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": i+1, "name": n, "item": u} for i, (n, u) in enumerate(bc)]})
    sblocks = "\n".join(f'<script type="application/ld+json">{json.dumps(s, ensure_ascii=False)}</script>' for s in schemas)
    title = f"Storefront Glazier {name} \u2014 {parent}, FL | ACG"
    description = f"Commercial storefront glazing in {name}, {parent}, FL. ACG is Florida-licensed CGC #1531993 with 350+ commercial projects and 48-hour bid turnaround."
    html = f'''<!DOCTYPE html>
<html lang="en">
<head>{GTAG}
<meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{html_lib.escape(title)}</title>
<meta name="description" content="{html_lib.escape(description)}">
<link rel="canonical" href="{canonical}">
<link rel="icon" type="image/png" href="/images/favicon-32.png">
<meta name="geo.position" content="{lat};{lng}">
<meta name="geo.placename" content="{html_lib.escape(name)}, {html_lib.escape(parent)}, FL">
<meta name="geo.region" content="US-FL">
<meta name="ICBM" content="{lat}, {lng}">
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
    write_html(f"{parent_slug}/{slug}/index.html", html)


# ============================================================
# Wave 4 AIO FAQs
# ============================================================

import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from seo_sprint import build_aio

AIO4 = [
    {
        "slug": "aluminum-vs-vinyl-windows-commercial",
        "title": "Aluminum vs Vinyl Windows for Commercial Buildings (Florida 2026)",
        "description": "Commercial buildings use aluminum windows, not vinyl. ACG explains why and when vinyl shows up on commercial projects (rarely \u2014 mostly low-rise residential or hospitality).",
        "h1": "Aluminum vs Vinyl Windows for Commercial Buildings",
        "summary": "Aluminum is the standard for commercial windows in Florida; vinyl is used almost exclusively in low-rise residential and entry-level hospitality. Aluminum supports higher wind loads, larger openings, structural-silicone glazing, and the thermal-break performance Florida Energy Code requires. Vinyl is cheaper but limited to smaller openings and lower wind exposures.",
        "sections": [
            ("Why commercial defaults to aluminum", "Commercial buildings need larger openings, higher wind capacity, and code-rated structural performance. Aluminum extrusions can be machined to 1-3/4\" through 6\" face dimensions with steel reinforcement where needed. Vinyl is a polymer \u2014 it has lower stiffness and is typically limited to opening sizes under 60 inches and design pressures below 60 PSF."),
            ("Where vinyl shows up on commercial projects", "Low-rise multi-family (3 stories or less), entry-level hospitality where budget is tight, and ground-floor residential conversion projects. Even there, most commercial GCs prefer aluminum because it has consistent service-life expectations across the trades."),
            ("Energy performance comparison", "Modern aluminum thermally-broken windows hit U-factor 0.30-0.45 and SHGC 0.25 \u2014 well within FL Energy Code limits. Vinyl windows can hit U-factor 0.25-0.32 (slightly better insulator) but at the cost of structural performance limits."),
            ("Cost comparison on commercial work", "Aluminum thermally-broken IG: $66-$142/SF installed (storefront) or $30-$60/SF (punch windows). Commercial-grade vinyl: $40-$85/SF installed for punch windows. Vinyl saves money on the line item but loses on opening flexibility, hardware quality, and resale value."),
            ("HVHZ and vinyl windows", "HVHZ-rated vinyl windows exist (several manufacturers have current NOAs) but the certified opening sizes are smaller than aluminum equivalents. For most commercial Florida applications, aluminum HVHZ-rated windows are the practical answer.")
        ],
        "faqs": [
            ("Do commercial buildings use aluminum or vinyl windows?", "Commercial buildings overwhelmingly use aluminum windows. Vinyl is reserved for low-rise residential, entry-level hospitality, and small-opening applications. Aluminum supports larger openings, higher wind loads, and more sophisticated hardware."),
            ("Are vinyl windows allowed in HVHZ Florida?", "Yes, several manufacturers offer HVHZ-rated vinyl windows with current Miami-Dade NOAs. But certified opening sizes are smaller than aluminum equivalents, limiting their use on commercial projects."),
            ("Is aluminum more expensive than vinyl?", "Yes \u2014 commercial aluminum windows typically cost 50-80% more than equivalent vinyl windows. The premium covers structural capacity, opening flexibility, and longer service life."),
            ("Which has better thermal performance?", "Vinyl is technically a better insulator (U-factor 0.25-0.32) than thermally-broken aluminum (0.30-0.45). But both meet FL Energy Code, and the difference is rarely decisive on commercial buildings."),
            ("Can vinyl windows be used in curtain wall?", "No \u2014 curtain wall systems are aluminum-framed by definition. Vinyl doesn't have the structural stiffness for multi-story curtain wall applications.")
        ]
    },
    {
        "slug": "skylights-overhead-glazing-commercial-florida",
        "title": "Commercial Skylights & Overhead Glazing in Florida (Code, Cost, Systems)",
        "description": "Commercial skylights and overhead glazing in Florida require laminated glass per IBC, structural calculations, and water management detailing. ACG explains the requirements.",
        "h1": "Commercial Skylights and Overhead Glazing in Florida",
        "summary": "Commercial skylights and overhead glazing in Florida must use laminated glass per IBC 2407 and FBC, support live and dead loads per ASCE 7, manage water with proper slope and curb detailing, and meet HVHZ impact requirements in Miami-Dade, Broward, and HVHZ Palm Beach. Common products: Wasco Skylights, Velux Commercial, Major Industries Guardian 275, Kalwall translucent panels.",
        "sections": [
            ("Why overhead glazing is structurally different", "Overhead glazing sees gravity loads (dead load + live load) that wall glazing doesn't. IBC 2407 requires laminated glass for any glazing at greater than 15 degrees from vertical. The laminated structure prevents falling glass shards in the event of breakage \u2014 a critical safety requirement."),
            ("Common system types", "Translucent panel systems (Kalwall, Major Industries Guardian 275) for diffuse daylight, dome and pyramid skylights (Wasco, Velux Commercial), structural glass skylights with stick-built aluminum framing, and operable smoke-vent skylights for commercial code compliance."),
            ("Water management and detailing", "Florida rain enters overhead openings differently than wall openings. Specify 1/4\" per foot minimum slope (1.2 degrees) on flat skylights. Continuous curb flashing. Integral gutters at panel-edge details. Drainage paths that prevent water collection in framing."),
            ("HVHZ overhead glazing", "Miami-Dade NOAs for skylights are specific. Approved products include Wasco, Velux Commercial, Major Industries, and specialty fabricators. Confirm the specific NOA is current AND that the design pressure matches your project before specification."),
            ("Cost benchmarks", "Standard translucent panel skylight (10x10 ft): $4,800-$8,400 installed. Custom structural glass skylight (200 SF): $35,000-$72,000 installed. Operable smoke-vent skylight: $6,500-$14,000 installed. HVHZ-rated assemblies: add 20-35%."),
            ("Daylighting and energy considerations", "Skylights add free daylight \u2014 reducing artificial lighting load. But they also add solar heat gain that needs to be managed via Low-E coatings or frit patterns. Specify low-E surface #2 on insulated skylight assemblies for Florida.")
        ],
        "faqs": [
            ("What kind of glass is used in commercial skylights?", "Commercial skylights use laminated glass per IBC 2407 \u2014 any glazing more than 15 degrees from vertical must be laminated for safety. Insulated laminated assemblies are standard for energy code compliance."),
            ("Do skylights need impact-rated glass in HVHZ?", "Yes, skylights in HVHZ counties (Miami-Dade, Broward, parts of Palm Beach) must be impact-rated and have a current Miami-Dade NOA. The same TAS 201/202/203 testing applies to overhead glazing."),
            ("How much do commercial skylights cost?", "Translucent panel skylights (10x10 ft): $4,800-$8,400 installed. Custom structural glass skylights (200 SF): $35,000-$72,000 installed. HVHZ-rated adds 20-35%."),
            ("What's the slope requirement for skylights?", "Minimum 1/4\" per foot slope (1.2 degrees) for flat or low-slope skylights. Steeper slopes shed water more reliably."),
            ("Can skylights be operable?", "Yes \u2014 operable skylights, smoke-vent skylights, and motorized hatch skylights are all available for commercial applications. Smoke-vent skylights serve code-required smoke evacuation in some occupancies.")
        ]
    },
    {
        "slug": "decorative-glass-commercial-florida",
        "title": "Decorative Glass for Florida Commercial: Frit, Etch, Digital Print, Switchable",
        "description": "Decorative glass on Florida commercial projects: ceramic frit, acid etch, digital print, switchable smart glass, and custom interlayer films. ACG explains options and cost.",
        "h1": "Decorative Glass for Florida Commercial",
        "summary": "Decorative commercial glass includes ceramic frit (baked-on patterns), acid etch (sandblast-style frosted effects), digital ceramic print (full-color custom imagery), switchable smart glass (PDLC privacy on demand), and custom interlayer films (color, image, branding). Cost ranges from $15-$200/SF premium over clear vision glass depending on technology and customization.",
        "sections": [
            ("Ceramic frit \u2014 the standard decorative technique", "Ceramic frit is opaque ceramic ink fired onto the back surface of a glass lite at 1,200\u00b0F. Permanent, fade-proof, and architecturally versatile. Available in solid coverage (spandrel), dot patterns, gradient, stripes, and custom geometries. Common on Florida Class-A office curtain wall, hotel facades, and retail storefront. Cost: $15-$45/SF premium."),
            ("Acid etch and sandblast", "Acid etch and sandblast both create a frosted appearance on the glass surface. Acid etch (chemical) is permanent and uniform. Sandblast (mechanical) can be patterned by masking. Both used for privacy applications: conference rooms, executive offices, restroom partitions, restaurant divider walls. Cost: $25-$60/SF premium."),
            ("Digital ceramic print", "Digital ceramic print uses inkjet technology to apply ceramic inks in custom imagery. Photographic-quality reproduction. Used for branding, art glass installations, and architectural feature walls. Common on hotel lobby walls, retail brand-presence installations, healthcare wayfinding. Cost: $80-$200/SF premium depending on coverage and color count."),
            ("Switchable smart glass", "PDLC (polymer-dispersed liquid crystal) switches between transparent and opaque (frosted) electronically. Used for executive office privacy, conference room walls, hospital exam rooms, hotel suite bathrooms. Cost: $90-$180/SF premium."),
            ("Custom interlayer films", "Laminated glass can use custom interlayer films \u2014 colored (red, blue, gradient), image-printed (logos, art), or solar-control film. Used for restaurant branding, retail color identity, and architectural feature glazing. Cost: $30-$90/SF premium."),
            ("How to choose the right decorative technique", "Privacy with daylight = acid etch or PDLC. Solar control = frit or low-E. Branding/imagery = digital ceramic print. Architecture feature = laminated with custom interlayer. The choice depends on the design objective and budget.")
        ],
        "faqs": [
            ("What's ceramic frit glass?", "Ceramic frit glass has opaque ceramic ink fired onto the back surface in patterns or solid coverage. Used for spandrel, solar control, and architectural pattern work. Permanent and fade-proof. Common on Florida commercial curtain wall."),
            ("Is acid etch glass permanent?", "Yes \u2014 acid etch creates a permanent frosted surface that won't wear off. Sandblast is also permanent but can be patterned with masking. Both are common for privacy applications."),
            ("What's digital ceramic print glass?", "Digital ceramic print uses inkjet ceramic inks to apply custom imagery on glass. Photographic-quality reproduction. Used for branding, art glass, and architectural features. Cost premium $80-$200/SF."),
            ("Can smart glass switch from clear to opaque?", "Yes \u2014 PDLC smart glass switches between transparent and opaque (frosted) electronically. Used for executive privacy, conference rooms, healthcare, and hospitality. Cost premium $90-$180/SF."),
            ("Which decorative technique is best for privacy with daylight?", "Acid etch and PDLC smart glass both provide privacy while allowing daylight through. Acid etch is permanent and cheaper; PDLC is switchable and more expensive but offers flexibility.")
        ]
    },
    {
        "slug": "energy-code-compliance-florida-commercial-glass",
        "title": "Energy Code Compliance for Florida Commercial Glass (FBC 2023)",
        "description": "FBC Energy Conservation requires Florida commercial glass to meet U-factor and SHGC limits. ACG explains compliance paths, climate zones, and product selection.",
        "h1": "Energy Code Compliance for Florida Commercial Glass",
        "summary": "Florida Building Code Energy Conservation chapter (based on IECC) sets U-factor and SHGC limits for commercial fenestration. Climate Zone 1 (South Florida) requires U-factor \u2264 0.50 and SHGC \u2264 0.25 for most vertical glazing. Climate Zone 2 (rest of Florida) is slightly less strict. Compliance paths include prescriptive (component-by-component limits), performance (whole-building modeling), and trade-off (area-weighted average).",
        "sections": [
            ("Florida climate zones", "Climate Zone 1 (South Florida, including Miami-Dade, Broward, Palm Beach, Collier, Lee, Hendry, Monroe, Glades): strictest energy code. Climate Zone 2 (rest of Florida): slightly less strict. Boundaries follow county lines."),
            ("U-factor limits for commercial vertical fenestration", "Climate Zone 1: U-factor \u2264 0.50. Climate Zone 2: U-factor \u2264 0.55. Most commercial low-E insulated glass easily achieves U-factor 0.30-0.45, providing significant margin to the code minimum."),
            ("SHGC limits", "Climate Zone 1: SHGC \u2264 0.25 for most projects (slightly higher for north-facing only). Climate Zone 2: SHGC \u2264 0.27. SHGC compliance is the binding constraint in South Florida \u2014 it drives low-E specification."),
            ("Visible Light Transmittance (VLT) considerations", "Florida energy code doesn't require minimum VLT, but most architects target VLT 35-70% for daylight quality. High-performance low-E products (Solarban 70XL, SunGuard SN 68, VRE-46) deliver this VLT while meeting SHGC \u2264 0.25."),
            ("Compliance paths", "Prescriptive: each component must meet the table limits. Performance: whole-building energy modeling demonstrates equivalent or better performance. Trade-off: area-weighted average across all fenestration meets the limit. Most commercial projects use prescriptive."),
            ("Common compliance failures", "1) Specifying clear vision glass without low-E coating (SHGC 0.55-0.70, fails Zone 1). 2) Single-pane glass (U-factor 1.10, fails everywhere). 3) Glass at building corners (higher wind load) sometimes incorrectly specced from interior wall sections. 4) Skylights treated as vertical fenestration (different limits apply)."),
            ("Verification at permit submittal", "AHJs verify energy compliance via REScheck (residential) or COMcheck (commercial) reports submitted with the permit application. Glaziers don't directly produce these reports, but they provide the U-factor and SHGC values that the energy consultant inputs.")
        ],
        "faqs": [
            ("What are Florida energy code limits for commercial glass?", "FBC Energy Conservation chapter requires Climate Zone 1 (South Florida) commercial vertical fenestration to meet U-factor \u2264 0.50 and SHGC \u2264 0.25. Climate Zone 2 is slightly less strict."),
            ("What's the SHGC for low-E commercial glass?", "Typical high-performance low-E commercial glass has SHGC 0.20-0.27 \u2014 well within Florida Climate Zone 1 requirement of \u2264 0.25. Products like Solarban 70XL, SunGuard SN 68, and Viracon VRE-46 are commonly specified."),
            ("Does single-pane glass meet Florida energy code?", "No \u2014 single-pane clear glass has U-factor around 1.10, far above the 0.50 limit. Commercial buildings require insulated (double-pane minimum) glass to comply."),
            ("Who verifies energy code compliance at permit?", "Energy code compliance is verified via COMcheck reports submitted with the permit application. An energy consultant or design professional prepares these. The glazier provides the U-factor and SHGC values."),
            ("Is impact glass automatically energy-compliant?", "Not automatically \u2014 impact glass can be specified with or without low-E coating. Most modern impact assemblies include low-E to meet energy code, but verify the specific product specification.")
        ]
    },
    {
        "slug": "leed-points-from-glass-florida-commercial",
        "title": "LEED Points from Glass on Florida Commercial Buildings",
        "description": "Florida commercial buildings can earn LEED points from glass selection: daylight, views, solar control, energy performance, and recycled content. ACG explains the math.",
        "h1": "LEED Points from Glass on Florida Commercial Buildings",
        "summary": "Florida commercial buildings can earn LEED points through glass selection in several categories: Energy & Atmosphere (energy performance, optimized envelope), Indoor Environmental Quality (daylight, views, low-emitting materials), Materials & Resources (recycled content, sourcing), and Innovation (advanced glazing technologies). A typical Florida commercial building can capture 8-15 LEED points from glazing decisions alone.",
        "sections": [
            ("Energy & Atmosphere (EA): up to 6+ points", "EA Credit 1 (Optimize Energy Performance): high-performance low-E insulated glass with SHGC \u2264 0.22 and U-factor \u2264 0.35 contributes to whole-building energy modeling that earns 1-18 points (typical commercial earns 4-8). The glazing's contribution to envelope performance is a major driver."),
            ("Indoor Environmental Quality (IEQ): up to 4 points", "IEQ Credit 7.1 (Daylight): glazing with VLT \u2265 50% in occupied areas earns 1-2 points. IEQ Credit 7.2 (Views): direct line-of-sight glass to outdoor view at 75% of occupied floor area earns 1 point. IEQ Credit 4.2 (Low-Emitting Materials, sealants): low-VOC sealants earn 1 point."),
            ("Materials & Resources (MR): up to 2 points", "MR Credit 4 (Recycled Content): post-consumer recycled content in glass and aluminum framing. Most modern glass is 20-30% recycled cullet. Aluminum extrusions are typically 30-50% recycled. Combined, this contributes to 1-2 points."),
            ("Innovation (IN): 1-2 points", "Advanced glazing technologies (electrochromic, photovoltaic, building-integrated solar) can earn Innovation points. Florida projects pursuing dynamic glass or BIPV typically capture 1-2 Innovation credits."),
            ("Florida-specific LEED considerations", "Florida's hot climate makes solar control (SHGC) the dominant factor. Building orientation, glass-to-wall ratio, and shading device coordination all interact with the glass spec for whole-building energy modeling. Coordinate the glass package with the energy consultant early to maximize credits."),
            ("LEED v4 vs v4.1 differences", "LEED v4.1 (current) credits envelope performance via the Optimize Energy Performance credit, integrated into the whole-building model. Older LEED v4 had separate envelope credits. Either way, glass spec is one of the biggest envelope levers.")
        ],
        "faqs": [
            ("How many LEED points can a Florida commercial building earn from glass?", "A typical Florida commercial building can earn 8-15 LEED points from glazing decisions \u2014 across Energy & Atmosphere, Indoor Environmental Quality, Materials & Resources, and Innovation categories."),
            ("Does low-E glass help with LEED certification?", "Yes \u2014 low-E glass with SHGC \u2264 0.22 contributes significantly to the Optimize Energy Performance credit (up to 18 points) through whole-building energy modeling."),
            ("What VLT do I need for LEED daylight credits?", "Daylight credits require VLT \u2265 50% in regularly occupied areas. Most low-E commercial glass provides VLT 50-70% \u2014 well within the requirement."),
            ("Can recycled-content glass earn LEED points?", "Yes \u2014 most modern commercial glass contains 20-30% recycled cullet, contributing to the Materials & Resources Recycled Content credit. Aluminum framing typically contains 30-50% recycled content."),
            ("Does smart glass (electrochromic) earn Innovation credits?", "Yes \u2014 dynamic glazing (electrochromic, photovoltaic, BIPV) typically earns 1-2 Innovation credits on LEED projects.")
        ]
    },
    {
        "slug": "glass-types-comparison-commercial-florida",
        "title": "Commercial Glass Types Compared: Float, Tempered, Laminated, Heat-Strengthened, Insulated",
        "description": "Commercial glass comes in five base types: float (annealed), tempered, heat-strengthened, laminated, and insulated. ACG explains what each is for and Florida code requirements.",
        "h1": "Commercial Glass Types Compared",
        "summary": "Commercial glass comes in five base types: annealed (float), tempered, heat-strengthened, laminated, and insulated. Each has specific uses, performance characteristics, and Florida code applications. Most commercial buildings use combinations \u2014 e.g., insulated laminated impact-rated tempered (4 of the 5 types in one assembly).",
        "sections": [
            ("Annealed (float) glass \u2014 the base material", "All commercial glass starts as annealed float glass. Manufactured on a bath of molten tin to produce a flat, polished sheet. Annealed glass is not safety glass and breaks into sharp shards. Used directly in non-hazardous locations (above 60\" from floor, away from doors). Cost basis for all other types."),
            ("Tempered glass \u2014 the safety standard", "Tempered glass is heat-treated to 1,200\u00b0F and rapidly cooled. The result: 4-5x stronger than annealed, and a safe break pattern (small granular pieces). Required in 'hazardous locations' per FBC: doors, sidelights, glass within 24\" of doors, glass within 18\" of floor, shower/tub enclosures, stairs."),
            ("Heat-strengthened glass \u2014 the spandrel/curtain wall workhorse", "Heat-strengthened glass is heat-treated like tempered but cooled more slowly, resulting in 2x annealed strength (vs 4-5x for tempered). NOT safety glazing. Used in spandrel, curtain wall vision lites (often as outboard of laminated assemblies), and applications where higher strength than annealed is needed but the safety break pattern of tempered is not required."),
            ("Laminated glass \u2014 the impact and security workhorse", "Laminated glass is two layers of glass bonded to a tough plastic interlayer (PVB or SGP). When broken, the interlayer holds the assembly together. Required for HVHZ impact-rated openings (TAS 201/202/203), structural glass railings, overhead glazing, and security applications. The dominant safety/structural glass type on Florida commercial work."),
            ("Insulated glass units (IGU) \u2014 the energy code answer", "Insulated glass units are two or more glass lites separated by a sealed cavity (typically 1/2\" with argon or air). The sealed cavity reduces heat transfer. Required by FL Energy Code to meet U-factor \u2264 0.50 for most commercial vertical fenestration. Standard IGU: 1/4\" outboard + 1/2\" airspace + 1/4\" inboard = 1\" nominal thickness."),
            ("Real-world combinations on Florida commercial", "Typical Florida storefront IGU: 1/4\" laminated impact (laminated outboard) + 1/2\" air + 1/4\" tempered inboard. This combines: laminated (HVHZ impact), tempered (safety break pattern), insulated (energy code), and low-E coating (energy code SHGC). Four glass types in one assembly.")
        ],
        "faqs": [
            ("What are the main types of commercial glass?", "Five base types: annealed (float) glass, tempered glass, heat-strengthened glass, laminated glass, and insulated glass units (IGU). Most commercial assemblies combine 2-3 of these types."),
            ("What's the difference between tempered and heat-strengthened?", "Tempered is heat-treated and rapidly cooled, achieving 4-5x annealed strength and a safe granular break. Heat-strengthened is treated more slowly, achieving 2x annealed strength but NOT a safety break pattern. Heat-strengthened is used in spandrel and curtain wall vision lites; tempered is used at safety-glazing locations."),
            ("Is laminated glass required for HVHZ?", "Yes \u2014 HVHZ impact-rated assemblies require laminated glass (typically tempered laminated with PVB or SGP interlayer). The laminated structure maintains integrity after impact, which is what passes the TAS 201/202/203 testing."),
            ("Why use insulated glass units instead of single-pane?", "Insulated glass units reduce heat transfer dramatically (U-factor 0.30-0.45 vs 1.10 for single pane). Required by Florida Energy Code for all conditioned commercial space."),
            ("Can one glass lite be multiple types?", "Yes \u2014 a single lite can be heat-treated (tempered or heat-strengthened), laminated (with another lite via interlayer), and coated (low-E). A typical Florida HVHZ storefront IGU combines 4 attributes in one assembly: laminated + tempered + insulated + low-E coated.")
        ]
    },
]


# ============================================================
# 5 more vertical x city
# ============================================================

VC3 = [
    ("medical-office-glazier-naples", "Medical Office", "Naples", "Collier", "naples", "collier-county", "medical-office-glazier-florida", 26.1420, -81.7948,
        "Naples medical office construction is driven by NCH Healthcare System, Physicians Regional, and a deep specialty clinic market. WBDR coastal impact glazing required. Brand-quality finish standards.",
        "Naples is WBDR \u2014 ASTM E1996/E1886 impact-rated assemblies required. Not HVHZ \u2014 FL Product Approval (FL #) sufficient. City of Naples design review on Fifth Avenue corridor."),
    ("hotel-glazing-contractor-fort-lauderdale", "Hotel", "Fort Lauderdale", "Broward", "fort-lauderdale", "broward-county", "hotel-glazing-contractor-florida", 26.1224, -80.1373,
        "Fort Lauderdale hotel construction concentrates on downtown, Las Olas, beachfront (A1A), and the Galleria area. Conrad, Four Seasons, AC Hotel, and brand-driven Marriott/Hilton/IHG projects driving demand.",
        "Fort Lauderdale is full HVHZ. All hotel envelope work requires Miami-Dade NOA. Unitized curtain wall standard above 8 stories."),
    ("retail-storefront-installer-naples", "Retail", "Naples", "Collier", "naples", "collier-county", "retail-storefront-installer-florida", 26.1420, -81.7948,
        "Naples retail construction is concentrated on Fifth Avenue South, Third Street South, Mercato, and Coconut Point. Upscale boutique retail and brand-driven national chain rollouts.",
        "Naples is WBDR \u2014 ASTM E1996/E1886 impact-rated assemblies required. City of Naples design review on Fifth Avenue corridor."),
    ("office-building-glazier-miami", "Office Building", "Miami", "Miami-Dade", "miami", "miami-dade-county", "office-building-glazier-florida", 25.7617, -80.1918,
        "Miami office construction concentrates on Brickell, downtown, Wynwood, the Design District, and Coral Gables. Class-A office, mixed-use ground floor, and tenant improvement work. HVHZ required.",
        "All Miami office envelope work requires Miami-Dade NOA. Unitized curtain wall typical above 8 stories. Structural silicone glazing (factory-bonded) for SSG applications."),
    ("school-glazier-miami", "School / Education", "Miami", "Miami-Dade", "miami", "miami-dade-county", "school-glazier-florida", 25.7617, -80.1918,
        "Miami-Dade County Public Schools is one of the nation's largest school districts. Constant capital construction. Plus charter networks, private schools, University of Miami, FIU, and MDC capital projects. HVHZ required.",
        "All Miami school construction is HVHZ. Vestibule design, ballistic-rated entries (UL 752 Level 3+), and impact-rated classroom windows are standard.")
]


def build_vc3(slug, vertical, city, county, city_slug, county_slug, vert_slug, lat, lng, blurb, hvhz_note):
    canonical = f"https://acglass.com/{slug}/"
    faqs = [
        (f"Does ACG do {vertical.lower()} glazing in {city}?", f"Yes. ACG installs commercial glazing for {vertical.lower()} projects in {city}, {county} County. Florida-licensed CGC #1531993 with 350+ commercial projects."),
        (f"What wind code applies?", hvhz_note),
        (f"How fast can ACG bid?", "48 hours on standard commercial plans; 5-7 business days on complex assemblies with structural engineering."),
        (f"What's typical cost?", f"FL commercial in 2026 ranges $66-$142/SF (storefront) or $95-$240/SF (curtain wall). {city} HVHZ sits at the upper end.")
    ]
    body = f'''<section style="background:linear-gradient(180deg,#050A12 0%,#0e284f 100%);padding:100px 0 60px;">
<div class="container">
<div class="eyebrow" style="color:#E11320;font-family:'JetBrains Mono',monospace;font-size:13px;letter-spacing:0.1em;text-transform:uppercase;margin-bottom:16px;">{html_lib.escape(vertical)} &middot; {html_lib.escape(city)}, FL</div>
<h1 style="color:#fff;font-size:clamp(36px,5vw,56px);line-height:1.1;margin:0 0 24px;">{html_lib.escape(vertical)} Glazier in {html_lib.escape(city)}</h1>
<p style="color:rgba(255,255,255,0.85);font-size:19px;line-height:1.6;max-width:900px;">{html_lib.escape(blurb)}</p>
<div style="margin-top:32px;display:flex;gap:14px;flex-wrap:wrap;">
<a href="/send-plans.html" style="background:#E11320;color:#fff;padding:14px 28px;text-decoration:none;font-weight:600;border-radius:4px;">Send Us Plans</a>
<a href="tel:+17724867711" style="border:1px solid rgba(255,255,255,0.2);color:#fff;padding:14px 28px;text-decoration:none;font-weight:600;border-radius:4px;">(772) 486-7711</a>
</div>
</div>
</section>

<section style="background:#050A12;padding:60px 0;">
<div class="container" style="max-width:900px;">
<h2 style="color:#fff;font-size:26px;margin-bottom:18px;">Code context</h2>
<p style="color:rgba(255,255,255,0.85);font-size:16px;line-height:1.8;margin-bottom:32px;">{html_lib.escape(hvhz_note)}</p>

<h2 style="color:#fff;font-size:26px;margin-bottom:18px;">Why ACG</h2>
<ul style="color:rgba(255,255,255,0.85);font-size:16px;line-height:1.9;list-style:disc;padding-left:24px;margin-bottom:32px;">
<li>FL-licensed CGC #1531993 with 350+ commercial projects.</li>
<li>Specialized in <a href="/{vert_slug}/" style="color:#E11320;">{vertical.lower()}</a> across <a href="/{city_slug}/" style="color:#E11320;">{html_lib.escape(city)}</a> and <a href="/{county_slug}/" style="color:#E11320;">{county} County</a>.</li>
<li>48-hour bid turnaround. AI-first operations: <a href="https://acglass.ai" style="color:#E11320;">acglass.ai</a></li>
</ul>

<h2 style="color:#fff;font-size:26px;margin-bottom:18px;">Frequently asked</h2>
<div>{"".join(f'<details style="background:#0e284f;padding:20px 24px;margin-bottom:10px;border-radius:6px;border-left:3px solid #E11320;"><summary style="color:#fff;font-size:17px;font-weight:600;cursor:pointer;">{html_lib.escape(q)}</summary><p style="color:rgba(255,255,255,0.8);font-size:15px;line-height:1.7;margin-top:14px;">{html_lib.escape(a)}</p></details>' for q, a in faqs)}</div>
</div>
</section>

<section style="background:#0e284f;padding:60px 0;">
<div class="container" style="text-align:center;">
<h2 style="color:#fff;font-size:28px;margin-bottom:14px;">Have a {html_lib.escape(city)} {vertical.lower()} project?</h2>
<a href="/send-plans.html" style="background:#E11320;color:#fff;padding:16px 40px;text-decoration:none;font-weight:600;border-radius:4px;display:inline-block;">Send Us Plans</a>
</div>
</section>'''
    schemas = [
        {"@context": "https://schema.org", "@type": ["Organization", "LocalBusiness"], "@id": canonical + "#org", "name": "American Commercial Glass", "url": "https://acglass.com", "telephone": "+17724867711", "logo": "https://acglass.com/images/acg-logo-nav@2x.png", "address": {"@type": "PostalAddress", "streetAddress": "700 S Rosemary Ave Suite 204", "addressLocality": "West Palm Beach", "addressRegion": "FL", "postalCode": "33401", "addressCountry": "US"}, "sameAs": ORG_SAMEAS, "areaServed": {"@type": "Place", "name": f"{city}, {county} County, FL", "geo": {"@type": "GeoCoordinates", "latitude": lat, "longitude": lng}}},
        {"@context": "https://schema.org", "@type": "Service", "name": f"{vertical} Glazier \u2014 {city}", "serviceType": vertical + " Glazing", "areaServed": f"{city}, FL", "provider": {"@id": canonical + "#org"}},
        {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faqs]},
        {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": 1, "name": "Home", "item": "https://acglass.com/"}, {"@type": "ListItem", "position": 2, "name": vertical, "item": f"https://acglass.com/{vert_slug}/"}, {"@type": "ListItem", "position": 3, "name": city, "item": canonical}]}
    ]
    sblocks = "\n".join(f'<script type="application/ld+json">{json.dumps(s, ensure_ascii=False)}</script>' for s in schemas)
    title = f"{vertical} Glazier {city}, FL | Commercial Storefront | ACG"
    description = f"ACG installs {vertical.lower()} commercial glazing in {city}, {county} County, FL. 350+ projects, CGC #1531993, 48-hour bid turnaround."
    html = f'''<!DOCTYPE html>
<html lang="en">
<head>{GTAG}
<meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{html_lib.escape(title)}</title>
<meta name="description" content="{html_lib.escape(description)}">
<link rel="canonical" href="{canonical}">
<link rel="icon" type="image/png" href="/images/favicon-32.png">
<meta name="geo.position" content="{lat};{lng}">
<meta name="geo.placename" content="{html_lib.escape(city)}, FL">
<meta name="geo.region" content="US-FL">
<meta name="ICBM" content="{lat}, {lng}">
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
    write_html(f"{slug}/index.html", html)


# ============================================================
# Master pillar page
# ============================================================

def build_pillar():
    canonical = "https://acglass.com/florida-commercial-glazing-complete-guide/"
    body = '''<section style="background:linear-gradient(180deg,#050A12 0%,#0e284f 100%);padding:100px 0 60px;">
<div class="container">
<div class="eyebrow" style="color:#E11320;font-family:'JetBrains Mono',monospace;font-size:13px;letter-spacing:0.1em;text-transform:uppercase;margin-bottom:16px;">Pillar &middot; Master Guide</div>
<h1 style="color:#fff;font-size:clamp(36px,5vw,56px);margin:0 0 20px;">Florida Commercial Glazing: The Complete Guide (2026)</h1>
<p style="color:rgba(255,255,255,0.85);font-size:18px;line-height:1.6;max-width:900px;">Everything an architect, GC, owner, or developer needs to specify, bid, install, and warranty commercial glazing in Florida \u2014 2026 edition. Links to every detailed guide, calculator, and reference on this site.</p>
</div>
</section>

<section style="background:#050A12;padding:60px 0;">
<div class="container" style="max-width:1000px;">

<h2 style="color:#fff;font-size:30px;margin:0 0 24px;">Code &amp; compliance</h2>
<ul style="color:rgba(255,255,255,0.85);font-size:16px;line-height:2;list-style:disc;padding-left:24px;margin-bottom:32px;">
<li><a href="/florida-building-code-glass-requirements/" style="color:#E11320;">Florida Building Code glass requirements (2026)</a></li>
<li><a href="/what-is-hvhz-rated-glass/" style="color:#E11320;">HVHZ-rated glass explained</a></li>
<li><a href="/miami-dade-noa-explained/" style="color:#E11320;">Miami-Dade NOA explained</a></li>
<li><a href="/florida-product-approval-vs-noa/" style="color:#E11320;">FL Product Approval vs Miami-Dade NOA</a></li>
<li><a href="/energy-code-compliance-florida-commercial-glass/" style="color:#E11320;">Energy Code compliance (FBC 2023)</a></li>
<li><a href="/ada-storefront-door-requirements-florida/" style="color:#E11320;">ADA storefront door requirements</a></li>
<li><a href="/fire-rated-glazing-explained/" style="color:#E11320;">Fire-rated glazing explained (20-120 min)</a></li>
</ul>

<h2 style="color:#fff;font-size:30px;margin:0 0 24px;">System types</h2>
<ul style="color:rgba(255,255,255,0.85);font-size:16px;line-height:2;list-style:disc;padding-left:24px;margin-bottom:32px;">
<li><a href="/storefront-vs-curtain-wall/" style="color:#E11320;">Storefront vs curtain wall (when to choose each)</a></li>
<li><a href="/what-is-window-wall-system/" style="color:#E11320;">What is a window wall system</a></li>
<li><a href="/aluminum-storefront-systems-compared/" style="color:#E11320;">Aluminum storefront systems compared (Series 451T, 501T, 601T, 701T)</a></li>
<li><a href="/structural-silicone-glazing-explained/" style="color:#E11320;">Structural silicone glazing explained</a></li>
<li><a href="/what-is-spandrel-glass/" style="color:#E11320;">Spandrel glass explained</a></li>
<li><a href="/glass-railing-systems-florida/" style="color:#E11320;">Glass railing systems</a></li>
<li><a href="/skylights-overhead-glazing-commercial-florida/" style="color:#E11320;">Commercial skylights and overhead glazing</a></li>
</ul>

<h2 style="color:#fff;font-size:30px;margin:0 0 24px;">Glass types</h2>
<ul style="color:rgba(255,255,255,0.85);font-size:16px;line-height:2;list-style:disc;padding-left:24px;margin-bottom:32px;">
<li><a href="/glass-types-comparison-commercial-florida/" style="color:#E11320;">Commercial glass types compared (5 base types)</a></li>
<li><a href="/tempered-vs-laminated-glass/" style="color:#E11320;">Tempered vs laminated glass</a></li>
<li><a href="/impact-glass-vs-hurricane-shutters/" style="color:#E11320;">Impact glass vs hurricane shutters</a></li>
<li><a href="/low-e-glass-explained-florida/" style="color:#E11320;">Low-E glass explained for Florida</a></li>
<li><a href="/smart-glass-explained-florida-commercial/" style="color:#E11320;">Smart glass explained (SPD, PDLC, electrochromic)</a></li>
<li><a href="/decorative-glass-commercial-florida/" style="color:#E11320;">Decorative glass: frit, etch, digital print, switchable</a></li>
<li><a href="/aluminum-vs-vinyl-windows-commercial/" style="color:#E11320;">Aluminum vs vinyl windows for commercial</a></li>
<li><a href="/blast-resistant-glazing-florida/" style="color:#E11320;">Blast-resistant glazing</a></li>
</ul>

<h2 style="color:#fff;font-size:30px;margin:0 0 24px;">Cost &amp; pricing</h2>
<ul style="color:rgba(255,255,255,0.85);font-size:16px;line-height:2;list-style:disc;padding-left:24px;margin-bottom:32px;">
<li><a href="/how-much-does-commercial-storefront-cost-florida/" style="color:#E11320;">Commercial storefront cost in Florida (2026)</a></li>
<li><a href="/curtain-wall-cost-florida/" style="color:#E11320;">Curtain wall cost in Florida (2026)</a></li>
<li><a href="/glazier-cost-by-city-florida/" style="color:#E11320;">Cost by city (12 FL markets compared)</a></li>
<li><a href="/florida-commercial-glass-statistics-2026/" style="color:#E11320;">Florida commercial glass statistics 2026</a></li>
<li><a href="/tools/storefront-cost-estimator/" style="color:#E11320;">Storefront cost estimator (free tool)</a></li>
</ul>

<h2 style="color:#fff;font-size:30px;margin:0 0 24px;">Process &amp; schedule</h2>
<ul style="color:rgba(255,255,255,0.85);font-size:16px;line-height:2;list-style:disc;padding-left:24px;margin-bottom:32px;">
<li><a href="/commercial-glass-installation-timeline/" style="color:#E11320;">Commercial glass installation timeline (6-16 weeks)</a></li>
<li><a href="/florida-glazing-permit-timeline-by-county/" style="color:#E11320;">Permit timeline by Florida county</a></li>
<li><a href="/commercial-glass-warranty-explained/" style="color:#E11320;">Commercial glass warranty explained</a></li>
<li><a href="/commercial-glass-replacement-vs-repair/" style="color:#E11320;">Replacement vs repair</a></li>
<li><a href="/automatic-door-operators-commercial-florida/" style="color:#E11320;">Automatic door operators</a></li>
</ul>

<h2 style="color:#fff;font-size:30px;margin:0 0 24px;">Manufacturers we install</h2>
<ul style="color:rgba(255,255,255,0.85);font-size:16px;line-height:2;list-style:disc;padding-left:24px;margin-bottom:32px;">
<li><a href="/kawneer-installer-florida/" style="color:#E11320;">Kawneer storefront installer</a></li>
<li><a href="/ykk-ap-installer-florida/" style="color:#E11320;">YKK AP storefront installer</a></li>
<li><a href="/kawneer-vs-ykk-ap-storefront/" style="color:#E11320;">Kawneer vs YKK AP compared</a></li>
<li><a href="/solarban-installer-florida/" style="color:#E11320;">Solarban (Vitro) low-E installer</a></li>
<li><a href="/sentryglas-plus-installer-florida/" style="color:#E11320;">SentryGlas Plus (Kuraray) installer</a></li>
<li><a href="/viracon-installer-florida/" style="color:#E11320;">Viracon glass installer</a></li>
<li><a href="/pilkington-installer-florida/" style="color:#E11320;">Pilkington glass installer</a></li>
<li><a href="/tubelite-installer-florida/" style="color:#E11320;">Tubelite installer</a></li>
<li><a href="/efco-installer-florida/" style="color:#E11320;">EFCO installer</a></li>
</ul>

<h2 style="color:#fff;font-size:30px;margin:0 0 24px;">By industry</h2>
<ul style="color:rgba(255,255,255,0.85);font-size:16px;line-height:2;list-style:disc;padding-left:24px;margin-bottom:32px;">
<li><a href="/restaurant-glazier-florida/" style="color:#E11320;">Restaurant storefront</a></li>
<li><a href="/hotel-glazing-contractor-florida/" style="color:#E11320;">Hotel glazing</a></li>
<li><a href="/medical-office-glazier-florida/" style="color:#E11320;">Medical office</a></li>
<li><a href="/school-glazier-florida/" style="color:#E11320;">Schools and education</a></li>
<li><a href="/retail-storefront-installer-florida/" style="color:#E11320;">Retail</a></li>
<li><a href="/office-building-glazier-florida/" style="color:#E11320;">Office buildings</a></li>
<li><a href="/best-glass-for-restaurant-storefronts-florida/" style="color:#E11320;">Best glass for FL restaurants</a></li>
</ul>

<h2 style="color:#fff;font-size:30px;margin:0 0 24px;">By county / market</h2>
<p style="color:rgba(255,255,255,0.85);font-size:16px;line-height:1.8;margin-bottom:24px;">25 Florida county hub pages plus 90+ city pages. <a href="/florida-counties/" style="color:#E11320;">Browse all counties</a>.</p>

<h2 style="color:#fff;font-size:30px;margin:0 0 24px;">For specific audiences</h2>
<ul style="color:rgba(255,255,255,0.85);font-size:16px;line-height:2;list-style:disc;padding-left:24px;margin-bottom:32px;">
<li><a href="/for-general-contractors/" style="color:#E11320;">For general contractors (prequal, bid, scope)</a></li>
<li><a href="/architect-resources/" style="color:#E11320;">For architects (specs, code, calculators)</a></li>
<li><a href="/florida-commercial-glaziers-compared/" style="color:#E11320;">For owners (how to evaluate glaziers)</a></li>
<li><a href="/best-glaziers-south-florida/" style="color:#E11320;">Best glaziers in South Florida (eval criteria)</a></li>
</ul>

<h2 style="color:#fff;font-size:30px;margin:0 0 24px;">Reference</h2>
<ul style="color:rgba(255,255,255,0.85);font-size:16px;line-height:2;list-style:disc;padding-left:24px;margin-bottom:32px;">
<li><a href="/glossary/" style="color:#E11320;">Glossary (44 terms)</a></li>
<li><a href="/florida-glazing-faq/" style="color:#E11320;">Master FAQ (28 questions)</a></li>
<li><a href="/tools/" style="color:#E11320;">Free tools (4 calculators)</a></li>
<li><a href="/case-studies/" style="color:#E11320;">Case studies (25 projects)</a></li>
<li><a href="/leed-points-from-glass-florida-commercial/" style="color:#E11320;">LEED points from glass</a></li>
</ul>

</div>
</section>'''
    schemas = [
        {"@context": "https://schema.org", "@type": ["Organization", "LocalBusiness"], "@id": canonical + "#org", "name": "American Commercial Glass", "url": "https://acglass.com", "telephone": "+17724867711", "sameAs": ORG_SAMEAS, "address": {"@type": "PostalAddress", "streetAddress": "700 S Rosemary Ave Suite 204", "addressLocality": "West Palm Beach", "addressRegion": "FL", "postalCode": "33401", "addressCountry": "US"}},
        {"@context": "https://schema.org", "@type": "Article", "headline": "Florida Commercial Glazing: The Complete Guide (2026)", "description": "Master pillar guide to Florida commercial glazing \u2014 code, systems, glass types, cost, process, manufacturers, industries, counties, and resources.", "datePublished": "2026-05-23", "dateModified": "2026-05-23", "author": {"@type": "Organization", "name": "American Commercial Glass"}, "publisher": {"@id": canonical + "#org"}},
        {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": 1, "name": "Home", "item": "https://acglass.com/"}, {"@type": "ListItem", "position": 2, "name": "Complete Guide", "item": canonical}]}
    ]
    sblocks = "\n".join(f'<script type="application/ld+json">{json.dumps(s, ensure_ascii=False)}</script>' for s in schemas)
    title = "Florida Commercial Glazing: The Complete Guide (2026) | ACG"
    description = "Master pillar guide to Florida commercial glazing in 2026: code, systems, glass types, cost, process, manufacturers, industries, counties. From ACG (CGC #1531993)."
    html = f'''<!DOCTYPE html>
<html lang="en">
<head>{GTAG}
<meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{html_lib.escape(title)}</title>
<meta name="description" content="{html_lib.escape(description)}">
<link rel="canonical" href="{canonical}">
<link rel="icon" type="image/png" href="/images/favicon-32.png">
<meta name="geo.region" content="US-FL">
<meta property="og:type" content="article">
<meta property="og:title" content="{html_lib.escape(title)}">
<meta property="og:description" content="{html_lib.escape(description)}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="https://acglass.com/images/projects/ocean-prime-marina-aerial.jpg">
{FONTS}
{sblocks}
</head>
<body>{NAV}{body}{FOOTER}</body>
</html>'''
    write_html("florida-commercial-glazing-complete-guide/index.html", html)


if __name__ == "__main__":
    print("Building sub-city pages...")
    for s in SUBCITY:
        build_subcity(*s)
    print("\nBuilding AIO wave 4...")
    for a in AIO4:
        build_aio(a)
    print("\nBuilding vertical x city wave 3...")
    for v in VC3:
        build_vc3(*v)
    print("\nBuilding master pillar...")
    build_pillar()
    total = len(SUBCITY) + len(AIO4) + len(VC3) + 1
    print(f"\nTotal wave 6: {total} pages.")
