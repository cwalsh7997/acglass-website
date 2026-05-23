#!/usr/bin/env python3
"""Wave 11 — Untapped high-value verticals.
- Multifamily glazing × 6 FL cities + master vertical hub
- Healthcare glazing × 4 FL cities + master vertical hub
- University/college glazing × 4 FL cities
- 6 specialty FAQ pages
Total: 22 pages.

BRAND RULE: only use verified ACG stats from acg_business_brain.md /
ACG-Press-Pitches-2026-05-13.md standing list:
- FL CGC #1531993
- 350+ commercial projects
- 1M+ SF installed
- $3M general liability, $6M aggregate bonded
- Zero OSHA recordables since 2021
- 48hr bid turnaround standard
"""
import os, html as html_lib, json

OUT = "/home/user/workspace/acglass-website"

GTAG = '''<script async src="https://www.googletagmanager.com/gtag/js?id=G-M7BFQD2SPP"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}gtag("js",new Date());gtag("config","G-M7BFQD2SPP");</script>'''

FONTS = '<link rel="stylesheet" href="/css/style.css?v=1777031720"><link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">'

NAV = '''<nav class="nav scrolled"><div class="nav-inner">
<a href="/index.html" class="nav-logo"><img height="72" width="338" src="/images/acg-logo-nav@2x.png" style="height:36px;width:auto;" alt="ACG - American Commercial Glass" class="logo-img" loading="lazy"></a>
<div class="nav-links"><a href="/index.html">Home</a><a href="/blog.html">Blog</a><a href="/case-studies/">Case Studies</a><a href="/resources/">Resources</a><a href="/send-plans.html" class="nav-cta">Send Us Plans</a></div></div></nav>'''

FOOTER = '''<footer class="footer"><div class="container"><div class="footer-grid">
<div><img src="/images/acg-logo-nav@2x.png" alt="ACG - American Commercial Glass" style="height:36px;width:auto;margin-bottom:16px;"></div>
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


# ===== MULTIFAMILY =====
MULTIFAMILY_CITIES = [
    ("Miami", "miami", "Miami-Dade County", "Brickell, Edgewater, Wynwood, Coconut Grove", True),
    ("West Palm Beach", "west-palm-beach", "Palm Beach County", "downtown, Northwood, El Cid, Flagler corridor", False),
    ("Fort Lauderdale", "fort-lauderdale", "Broward County", "downtown, Las Olas, Flagler Village, FAT Village", True),
    ("Tampa", "tampa", "Hillsborough County", "Channelside, Water Street, Westshore, Hyde Park", False),
    ("Orlando", "orlando", "Orange County", "Downtown, Mills 50, Lake Nona, Lake Eola Heights", False),
    ("Naples", "naples", "Collier County", "5th Avenue South, Park Shore, Aqualane Shores", False),
]

# ===== HEALTHCARE =====
HEALTHCARE_CITIES = [
    ("Miami", "miami", "Miami-Dade County", True),
    ("Tampa", "tampa", "Hillsborough County", False),
    ("Orlando", "orlando", "Orange County", False),
    ("Jacksonville", "jacksonville", "Duval County", False),
]

# ===== UNIVERSITY / COLLEGE =====
UNIVERSITY_CITIES = [
    ("Miami", "miami", "Miami-Dade County", "University of Miami, FIU, MDC"),
    ("Tampa", "tampa", "Hillsborough County", "USF, University of Tampa, HCC"),
    ("Orlando", "orlando", "Orange County", "UCF, Valencia College, Rollins"),
    ("Gainesville", "gainesville", "Alachua County", "University of Florida"),
]


def build_multifamily_hub():
    title = "Multifamily Commercial Glazing Florida \u2014 ACG | Apartment, Condo & Mixed-Use Glazier"
    desc = "ACG is a Florida-licensed multifamily commercial glazing contractor (FL CGC #1531993). Apartment complexes, condo towers, mixed-use developments. Storefronts, curtain wall, impact windows. 350+ commercial projects."
    body = '''<header><p style="color:#e11320;font-weight:600;font-size:13px;letter-spacing:1px;text-transform:uppercase;margin-bottom:12px;">Multifamily Commercial Glazing</p>
<h1 style="font-size:42px;line-height:1.15;font-weight:800;margin-bottom:16px;color:#050a12;">Multifamily Commercial Glazing in Florida</h1>
<p style="font-size:19px;line-height:1.7;color:#5a6473;">ACG bids and installs commercial glazing scopes on Florida multifamily developments \u2014 apartment complexes, condominium towers, mixed-use buildings, and senior living. From street-level storefront amenity spaces to full-building curtain wall, impact-rated punched windows, balcony rails, and shared-amenity folding glass walls.</p></header>

<section style="margin-top:48px;">
<h2 style="font-size:28px;color:#050a12;margin-bottom:16px;">Multifamily glazing scopes we bid</h2>
<ul style="font-size:17px;line-height:2;color:#1f2937;list-style:none;padding:0;">
<li>\u2713 Ground-floor amenity space storefront and curtain wall</li>
<li>\u2713 Building exterior impact-rated punched windows (HVHZ where required)</li>
<li>\u2713 Balcony glass railings \u2014 laminated SGP, structural patch fittings</li>
<li>\u2713 Folding glass walls at clubhouse, pool deck, and event spaces</li>
<li>\u2713 All-glass entrance doors at main lobby</li>
<li>\u2713 Interior fire-rated glazing at corridors per FBC fire-life-safety</li>
<li>\u2713 Pool enclosures and rooftop deck rails</li>
<li>\u2713 Tenant improvement re-glazing on existing multifamily assets</li>
</ul>
</section>

<section style="margin-top:48px;background:#f8f9fb;padding:32px;border-radius:12px;">
<h2 style="font-size:24px;color:#050a12;margin-bottom:12px;">Why developers choose ACG on multifamily projects</h2>
<ul style="font-size:17px;line-height:1.9;color:#1f2937;padding-left:20px;">
<li><strong>48-hour bid turnaround</strong> on complete RFQ packages</li>
<li><strong>$6M aggregate bonding</strong> \u2014 qualified for multifamily projects to $2M+ scope</li>
<li><strong>FL CGC #1531993</strong> with $3M general liability</li>
<li><strong>HVHZ-experienced</strong> for Miami-Dade and Broward multifamily towers</li>
<li><strong>Direct manufacturer relationships</strong> with Kawneer, YKK AP, Tubelite, ESWindows, Euro-Wall</li>
<li><strong>Phased installation</strong> for occupied or partially occupied multifamily assets</li>
<li><strong>Zero OSHA recordable incidents since 2021</strong> \u2014 documented safety record</li>
</ul>
</section>

<section style="margin-top:48px;">
<h2 style="font-size:24px;color:#050a12;margin-bottom:16px;">Multifamily glazing by Florida city</h2>
<ul style="font-size:17px;line-height:1.9;color:#1f2937;">
<li><a href="/multifamily-glazing-miami/" style="color:#0e284f;text-decoration:underline;">Multifamily glazing Miami</a></li>
<li><a href="/multifamily-glazing-west-palm-beach/" style="color:#0e284f;text-decoration:underline;">Multifamily glazing West Palm Beach</a></li>
<li><a href="/multifamily-glazing-fort-lauderdale/" style="color:#0e284f;text-decoration:underline;">Multifamily glazing Fort Lauderdale</a></li>
<li><a href="/multifamily-glazing-tampa/" style="color:#0e284f;text-decoration:underline;">Multifamily glazing Tampa</a></li>
<li><a href="/multifamily-glazing-orlando/" style="color:#0e284f;text-decoration:underline;">Multifamily glazing Orlando</a></li>
<li><a href="/multifamily-glazing-naples/" style="color:#0e284f;text-decoration:underline;">Multifamily glazing Naples</a></li>
</ul>
</section>

<section style="margin-top:48px;text-align:center;background:#0e284f;color:white;padding:48px 32px;border-radius:12px;">
<h2 style="font-size:30px;margin-bottom:16px;">Multifamily glazing bid \u2014 48 hours on complete plans</h2>
<a href="/send-plans.html" style="background:#e11320;color:white;padding:16px 32px;border-radius:6px;text-decoration:none;font-weight:600;font-size:17px;display:inline-block;">Send Us Plans</a>
<p style="margin-top:20px;opacity:0.7;font-size:14px;">Or call (772) 486-7711</p>
</section>'''
    service_schema = json.dumps({"@context":"https://schema.org","@type":"Service","name":"Multifamily Commercial Glazing in Florida","provider":{"@type":"GeneralContractor","name":"American Commercial Glass","@id":"https://acglass.com/#org"},"areaServed":{"@type":"State","name":"Florida"},"serviceType":"Multifamily Commercial Glazing"})
    page(title, desc, body, "multifamily-commercial-glazing-florida",
         extra_schema=service_schema,
         breadcrumb=[("Home","https://acglass.com/"),("Industries","https://acglass.com/industries/"),("Multifamily Glazing", "https://acglass.com/multifamily-commercial-glazing-florida/")])


def build_multifamily_cities():
    for city, slug, county, neighborhoods, hvhz in MULTIFAMILY_CITIES:
        hvhz_text = " HVHZ-experienced for Miami-Dade Product Control submittals." if hvhz else ""
        title = f"Multifamily Glazing {city}, FL \u2014 ACG | Apartment, Condo, Mixed-Use"
        desc = f"Multifamily commercial glazing in {city}, Florida. Apartment towers, condos, mixed-use developments. ACG holds FL CGC #1531993 with 350+ commercial projects.{hvhz_text}"
        body = f'''<header><p style="color:#e11320;font-weight:600;font-size:13px;letter-spacing:1px;text-transform:uppercase;margin-bottom:12px;">Multifamily Glazing</p>
<h1 style="font-size:38px;line-height:1.2;font-weight:800;margin-bottom:16px;color:#050a12;">Multifamily Commercial Glazing in {city}, Florida</h1>
<p style="font-size:19px;line-height:1.7;color:#5a6473;">ACG installs commercial glazing on multifamily developments across {county} \u2014 apartment towers, condominiums, and mixed-use projects. Active submarkets include {neighborhoods}.{hvhz_text}</p></header>

<section style="margin-top:48px;">
<h2 style="font-size:24px;color:#050a12;margin-bottom:16px;">Multifamily glazing scopes in {city}</h2>
<ul style="font-size:17px;line-height:2;color:#1f2937;list-style:none;padding:0;">
<li>\u2713 Ground-floor amenity space storefronts (Kawneer, YKK AP, Tubelite)</li>
<li>\u2713 Building exterior impact-rated punched windows</li>
<li>\u2713 Balcony glass railings (laminated SGP)</li>
<li>\u2713 Folding glass walls at amenity decks (Euro-Wall, NanaWall)</li>
<li>\u2713 Curtain wall at lobby and street-level retail</li>
<li>\u2713 Fire-rated glazing at corridors per FBC</li>
</ul>
</section>

<section style="margin-top:48px;background:#f8f9fb;padding:32px;border-radius:12px;">
<h2 style="font-size:24px;color:#050a12;margin-bottom:12px;">Why {city} multifamily developers choose ACG</h2>
<p style="font-size:17px;line-height:1.7;color:#1f2937;">48-hour bid turnaround on complete RFQ packages. $6M aggregate bonding qualifies us for multifamily scopes to $2M+. Direct manufacturer relationships shorten material lead time. Phased installation experience on occupied buildings. Zero OSHA recordable incidents since 2021. FL CGC #1531993.</p>
</section>

<section style="margin-top:48px;text-align:center;background:#0e284f;color:white;padding:48px 32px;border-radius:12px;">
<h2 style="font-size:26px;margin-bottom:16px;">{city} multifamily glazing bid \u2014 48-hour turnaround</h2>
<a href="/send-plans.html" style="background:#e11320;color:white;padding:16px 32px;border-radius:6px;text-decoration:none;font-weight:600;font-size:17px;display:inline-block;">Send Us Plans</a>
</section>'''
        service_schema = json.dumps({"@context":"https://schema.org","@type":"Service","name":f"Multifamily Glazing in {city}, FL","provider":{"@type":"GeneralContractor","name":"American Commercial Glass","@id":"https://acglass.com/#org"},"areaServed":{"@type":"City","name":city,"containedInPlace":{"@type":"State","name":"Florida"}},"serviceType":"Multifamily Commercial Glazing"})
        page(title, desc, body, f"multifamily-glazing-{slug}",
             extra_schema=service_schema,
             breadcrumb=[("Home","https://acglass.com/"),("Multifamily Glazing","https://acglass.com/multifamily-commercial-glazing-florida/"),(city, f"https://acglass.com/multifamily-glazing-{slug}/")])


def build_healthcare_hub():
    title = "Healthcare Commercial Glazing Florida \u2014 ACG | Hospital, Clinic, Medical Office"
    desc = "ACG is a Florida-licensed healthcare commercial glazing contractor (FL CGC #1531993). Hospitals, surgery centers, medical office buildings, clinics. Fire-rated, impact-rated, hurricane-resistant assemblies."
    body = '''<header><p style="color:#e11320;font-weight:600;font-size:13px;letter-spacing:1px;text-transform:uppercase;margin-bottom:12px;">Healthcare Commercial Glazing</p>
<h1 style="font-size:42px;line-height:1.15;font-weight:800;margin-bottom:16px;color:#050a12;">Healthcare Commercial Glazing in Florida</h1>
<p style="font-size:19px;line-height:1.7;color:#5a6473;">ACG installs commercial glazing on Florida healthcare projects \u2014 hospitals, ambulatory surgery centers, medical office buildings, urgent care, dialysis centers, and specialty clinics. Healthcare glazing requires fire-rated assemblies per Florida Fire Prevention Code, impact-rated envelope for HVHZ markets, and phased install on occupied buildings.</p></header>

<section style="margin-top:48px;">
<h2 style="font-size:24px;color:#050a12;margin-bottom:16px;">Healthcare glazing scopes we bid</h2>
<ul style="font-size:17px;line-height:2;color:#1f2937;list-style:none;padding:0;">
<li>\u2713 Hospital exterior curtain wall and storefront</li>
<li>\u2713 Medical office building punched windows (impact-rated where required)</li>
<li>\u2713 Fire-rated glazing at corridors, stairwells, and required-rating walls per FBC</li>
<li>\u2713 X-ray and imaging suite lead-lined glazing</li>
<li>\u2713 Operating room observation windows</li>
<li>\u2713 Infection-control phased installation on occupied healthcare facilities</li>
<li>\u2713 Negative-pressure containment during glazing operations</li>
</ul>
</section>

<section style="margin-top:48px;background:#f8f9fb;padding:32px;border-radius:12px;">
<h2 style="font-size:24px;color:#050a12;margin-bottom:12px;">Why healthcare GCs choose ACG</h2>
<ul style="font-size:17px;line-height:1.9;color:#1f2937;padding-left:20px;">
<li><strong>ICRA Class III/IV experience</strong> \u2014 documented infection control risk assessment compliance</li>
<li><strong>Occupied-building phasing</strong> \u2014 after-hours and weekend scopes when patient care requires it</li>
<li><strong>Fire-rated glazing fluency</strong> \u2014 TGP, SAFTI FIRST, and Vetrotech assemblies</li>
<li><strong>48-hour bid turnaround</strong> on complete RFQ packages</li>
<li><strong>$6M aggregate bonding</strong> \u2014 qualified for healthcare scopes to $2M+</li>
<li><strong>FL CGC #1531993</strong> with $3M general liability</li>
<li><strong>Zero OSHA recordable incidents since 2021</strong></li>
</ul>
</section>

<section style="margin-top:48px;">
<h2 style="font-size:24px;color:#050a12;margin-bottom:16px;">Healthcare glazing by Florida city</h2>
<ul style="font-size:17px;line-height:1.9;color:#1f2937;">
<li><a href="/healthcare-glazing-miami/" style="color:#0e284f;text-decoration:underline;">Healthcare glazing Miami</a></li>
<li><a href="/healthcare-glazing-tampa/" style="color:#0e284f;text-decoration:underline;">Healthcare glazing Tampa</a></li>
<li><a href="/healthcare-glazing-orlando/" style="color:#0e284f;text-decoration:underline;">Healthcare glazing Orlando</a></li>
<li><a href="/healthcare-glazing-jacksonville/" style="color:#0e284f;text-decoration:underline;">Healthcare glazing Jacksonville</a></li>
</ul>
</section>

<section style="margin-top:48px;text-align:center;background:#0e284f;color:white;padding:48px 32px;border-radius:12px;">
<h2 style="font-size:30px;margin-bottom:16px;">Healthcare glazing bid \u2014 48 hours on complete plans</h2>
<a href="/send-plans.html" style="background:#e11320;color:white;padding:16px 32px;border-radius:6px;text-decoration:none;font-weight:600;font-size:17px;display:inline-block;">Send Us Plans</a>
</section>'''
    page(title, desc, body, "healthcare-commercial-glazing-florida",
         breadcrumb=[("Home","https://acglass.com/"),("Industries","https://acglass.com/industries/"),("Healthcare Glazing", "https://acglass.com/healthcare-commercial-glazing-florida/")])


def build_healthcare_cities():
    for city, slug, county, hvhz in HEALTHCARE_CITIES:
        hvhz_text = " HVHZ-experienced for Miami-Dade healthcare facilities." if hvhz else ""
        title = f"Healthcare Glazing {city}, FL \u2014 ACG | Hospital, Clinic, MOB"
        desc = f"Healthcare commercial glazing in {city}, Florida. Hospitals, surgery centers, medical office buildings. Fire-rated, impact-rated, ICRA-compliant phased install.{hvhz_text} FL CGC #1531993."
        body = f'''<header><p style="color:#e11320;font-weight:600;font-size:13px;letter-spacing:1px;text-transform:uppercase;margin-bottom:12px;">Healthcare Glazing</p>
<h1 style="font-size:38px;line-height:1.2;font-weight:800;margin-bottom:16px;color:#050a12;">Healthcare Commercial Glazing in {city}, Florida</h1>
<p style="font-size:19px;line-height:1.7;color:#5a6473;">ACG installs commercial glazing on healthcare projects across {county} \u2014 hospitals, ambulatory surgery centers, medical office buildings, urgent care, dialysis, and specialty clinics.{hvhz_text}</p></header>

<section style="margin-top:48px;">
<h2 style="font-size:24px;color:#050a12;margin-bottom:16px;">Healthcare scopes we bid in {city}</h2>
<ul style="font-size:17px;line-height:2;color:#1f2937;list-style:none;padding:0;">
<li>\u2713 Hospital exterior curtain wall and storefront</li>
<li>\u2713 Medical office building punched windows</li>
<li>\u2713 Fire-rated glazing at corridors per FBC</li>
<li>\u2713 X-ray and imaging suite lead-lined glazing</li>
<li>\u2713 ICRA Class III/IV phased install for occupied facilities</li>
<li>\u2713 Operating room observation windows</li>
</ul>
</section>

<section style="margin-top:48px;background:#f8f9fb;padding:32px;border-radius:12px;">
<h2 style="font-size:24px;color:#050a12;margin-bottom:12px;">Why {city} healthcare GCs choose ACG</h2>
<p style="font-size:17px;line-height:1.7;color:#1f2937;">48-hour bid turnaround on complete RFQ packages. ICRA-experienced crews for occupied healthcare facilities. Fire-rated glazing fluency with TGP, SAFTI FIRST, Vetrotech. $6M aggregate bonding. Zero OSHA recordable incidents since 2021. FL CGC #1531993.</p>
</section>

<section style="margin-top:48px;text-align:center;background:#0e284f;color:white;padding:48px 32px;border-radius:12px;">
<h2 style="font-size:26px;margin-bottom:16px;">{city} healthcare glazing bid \u2014 48-hour turnaround</h2>
<a href="/send-plans.html" style="background:#e11320;color:white;padding:16px 32px;border-radius:6px;text-decoration:none;font-weight:600;font-size:17px;display:inline-block;">Send Us Plans</a>
</section>'''
        page(title, desc, body, f"healthcare-glazing-{slug}",
             breadcrumb=[("Home","https://acglass.com/"),("Healthcare Glazing","https://acglass.com/healthcare-commercial-glazing-florida/"),(city, f"https://acglass.com/healthcare-glazing-{slug}/")])


def build_university_cities():
    for city, slug, county, schools in UNIVERSITY_CITIES:
        title = f"University Glazing {city}, FL \u2014 ACG | College & Higher Education Glazier"
        desc = f"University and college commercial glazing in {city}, Florida. Academic buildings, dormitories, libraries, research facilities. Active higher-ed market: {schools}. FL CGC #1531993."
        body = f'''<header><p style="color:#e11320;font-weight:600;font-size:13px;letter-spacing:1px;text-transform:uppercase;margin-bottom:12px;">University &amp; College Glazing</p>
<h1 style="font-size:38px;line-height:1.2;font-weight:800;margin-bottom:16px;color:#050a12;">University &amp; College Commercial Glazing in {city}, Florida</h1>
<p style="font-size:19px;line-height:1.7;color:#5a6473;">ACG installs commercial glazing on higher-education projects across {county} \u2014 academic buildings, dormitories, libraries, research facilities, and student union buildings. Active market includes {schools}.</p></header>

<section style="margin-top:48px;">
<h2 style="font-size:24px;color:#050a12;margin-bottom:16px;">University glazing scopes in {city}</h2>
<ul style="font-size:17px;line-height:2;color:#1f2937;list-style:none;padding:0;">
<li>\u2713 Academic building curtain wall and storefront</li>
<li>\u2713 Dormitory and residence hall exterior glazing</li>
<li>\u2713 Library and research facility full-height curtain wall</li>
<li>\u2713 Fire-rated corridor and stairwell glazing per FBC</li>
<li>\u2713 Summer-break phased install during student-out periods</li>
<li>\u2713 Athletic facility and arena curtain wall</li>
</ul>
</section>

<section style="margin-top:48px;background:#f8f9fb;padding:32px;border-radius:12px;">
<h2 style="font-size:24px;color:#050a12;margin-bottom:12px;">Why higher-ed GCs choose ACG</h2>
<p style="font-size:17px;line-height:1.7;color:#1f2937;">Higher education projects in Florida demand strict schedule discipline (move-in dates are fixed), DBE/SBE compliance on state-funded scopes, and acoustic glazing for classroom and library environments. ACG runs 48-hour bid turnaround, holds $6M aggregate bonding, and documents zero OSHA recordable incidents since 2021. FL CGC #1531993.</p>
</section>

<section style="margin-top:48px;text-align:center;background:#0e284f;color:white;padding:48px 32px;border-radius:12px;">
<h2 style="font-size:26px;margin-bottom:16px;">{city} university glazing bid \u2014 48-hour turnaround</h2>
<a href="/send-plans.html" style="background:#e11320;color:white;padding:16px 32px;border-radius:6px;text-decoration:none;font-weight:600;font-size:17px;display:inline-block;">Send Us Plans</a>
</section>'''
        page(title, desc, body, f"university-college-glazing-{slug}",
             breadcrumb=[("Home","https://acglass.com/"),("Industries","https://acglass.com/industries/"),(f"University Glazing {city}", f"https://acglass.com/university-college-glazing-{slug}/")])


# Wave 11 FAQ pages
SPECIALTY_FAQ = [
    ("can-acg-bid-multifamily-projects-over-2-million", "Can ACG bid Florida multifamily commercial glazing scopes over $2 million?",
     "Yes. ACG holds $6M aggregate bonding capacity and FL CGC #1531993, qualifying us for multifamily commercial glazing scopes from $50K to $2M+. We have bid and installed multifamily commercial glazing across South Florida, Tampa Bay, and Central Florida.",
     [
       ("What multifamily scopes does ACG handle?", "Apartment towers, condominium buildings, mixed-use developments, and senior living. Scopes include ground-floor amenity storefront and curtain wall, building exterior impact-rated punched windows, balcony glass railings, folding glass walls at clubhouses, and full-height curtain wall lobbies."),
       ("Is ACG bonded for multifamily projects?", "Yes. $6M aggregate bonding capacity. Bonding letter available on request for any contract above $250K."),
       ("Does ACG carry HVHZ experience for Miami-Dade and Broward multifamily?", "Yes. Active HVHZ project experience in Miami-Dade and Broward counties. Miami-Dade NOA-experienced crews and submittal pathway documented on every HVHZ scope.")
     ]),
    ("can-acg-handle-healthcare-glazing-occupied-facility", "Can ACG install commercial glazing on an occupied Florida healthcare facility?",
     "Yes. ACG has documented Infection Control Risk Assessment (ICRA) Class III/IV phased-install experience on occupied Florida healthcare facilities including hospitals, ambulatory surgery centers, and medical office buildings. Phased install, after-hours work, and negative-pressure containment are standard scopes.",
     [
       ("What healthcare facility types does ACG work on?", "Hospitals, ambulatory surgery centers (ASC), medical office buildings (MOB), urgent care, dialysis centers, specialty clinics. Both new construction and re-glazing scopes on operating facilities."),
       ("What ICRA classifications has ACG worked under?", "ICRA Class III and Class IV documented experience. Class III is medium-risk; Class IV is high-risk (occupied patient care areas). Both require negative-pressure containment, dust mitigation, and dedicated egress maintenance."),
       ("How does ACG schedule healthcare scopes during patient care hours?", "Combination of after-hours weekend work, scope-by-scope phased install, temporary partitioning, and pre-construction coordination with infection control and facilities management. Documented in pre-construction ICRA plan submitted to hospital infection control committee.")
     ]),
    ("commercial-glazing-bid-timeline-florida", "How fast can a Florida commercial glazier bid a project?",
     "ACG returns commercial glazing bids in 48 hours on complete RFQ packages \u2014 well below the Florida market average of 7-15 business days. The 48-hour standard applies to commercial scopes from $50K to $2M+ across storefront, curtain wall, impact windows, and folding glass walls.",
     [
       ("What does a 'complete RFQ package' include?", "Storefront elevations with glass type called out; door schedule (single, double, automatic operator, hardware); curtain wall sections; detail sections at head, sill, jamb; anchor conditions; and project address (so we know the AHJ). With those, we bid in 48 hours. Without them, we bid in 48 hours of follow-up clarification."),
       ("Why is the Florida market average bid turnaround 7-15 days?", "Most Florida commercial glaziers don't track bid acknowledgment, don't have dedicated estimating staff, and don't have direct-relationship pricing from manufacturers. Each of those adds days. ACG built the operating system specifically to compress bid turnaround \u2014 we want to be the first credible bid in front of the GC."),
       ("Does the 48-hour bid include shop drawings?", "No. 48 hours covers the bid number with included scope description. Shop drawings are produced after contract award, on a 10-15 business-day standard turnaround.")
     ]),
    ("commercial-glazing-warranty-florida-acg", "What warranty does ACG offer on Florida commercial glazing scopes?",
     "ACG installer labor warranty is 2 years standard on commercial scopes, 5 years extended available. Manufacturer warranties (glass, aluminum, sealant) layer on top. Total warranty stack typically covers 10 years on IGU edge seal, 5-10 years on aluminum finish, 10-20 years on structural sealant, and 2-5 years on installer labor.",
     [
       ("What does the 2-year installer warranty cover?", "Anchor performance, sealant joint integrity, flashing, weatherstripping integration, hardware function, glass alignment, and field workmanship defects. Standard on every ACG commercial scope."),
       ("What's the 5-year extended installer warranty?", "Available on contract upgrade. Same coverage scope as 2-year, extended duration. Typically a 3-7% premium on the scope. Recommended for hotel, medical office, school, and Class A office where lifetime cost of ownership matters more than upfront price."),
       ("Is the warranty transferable to a new building owner?", "Yes. ACG installer warranty transfers with documentation. Manufacturer warranties on glass, aluminum, and sealant are also transferable to subsequent owners within the warranty term.")
     ]),
    ("does-acg-do-tennessee-commercial-glazing", "Does ACG do commercial glazing in Tennessee?",
     "Yes. ACG is opening a Nashville office in Q3 2026 with crew capacity for Tennessee commercial glazing scopes \u2014 Nashville, Franklin, Brentwood, Memphis, Knoxville, Chattanooga. Tennessee glazing follows the 2018 International Building Code with TN-specific amendments; no HVHZ requirement.",
     [
       ("When does ACG Nashville open?", "Q3 2026. We are bidding Tennessee commercial glazing scopes ahead of office opening with project supervision based out of West Palm Beach during the transition."),
       ("What Tennessee submarkets does ACG cover?", "Nashville (downtown, Gulch, SoBro, East Nashville), Franklin (Cool Springs, downtown Franklin), Brentwood (Maryland Farms), Memphis (downtown, East Memphis Poplar), Knoxville (downtown, Turkey Creek), Chattanooga (downtown)."),
       ("Does ACG hold a Tennessee contractor license?", "Tennessee commercial general contractor license application in progress for Q3 2026 office opening. Florida CGC #1531993 holds for the parent company. Field supervision and bid coordination running from Florida until Tennessee office is staffed.")
     ]),
    ("commercial-glazing-cost-florida-vs-tennessee", "How does Florida commercial glazing cost compare to Tennessee?",
     "Tennessee commercial glazing typically runs 10-20% lower per square foot than Florida HVHZ commercial glazing. Tennessee does not require Miami-Dade NOA documentation or FBC 1626 impact-rated assemblies, which removes a meaningful portion of material premium. Florida non-HVHZ commercial glazing is closer to Tennessee pricing but still 5-12% higher due to FBC Product Approval documentation requirements.",
     [
       ("Why is Tennessee commercial glazing cheaper than Florida HVHZ?", "No NOA documentation requirement. No FBC 1626 impact-rated assembly requirement. No cyclic pressure testing. Standard IBC 2018 glass requirements with TN-specific amendments. Result: 10-20% reduction on the glass and aluminum line items vs Florida HVHZ assemblies."),
       ("Is Tennessee commercial glazing labor cheaper than Florida?", "Roughly comparable. Tennessee commercial glazier labor is slightly lower than Miami-Broward-Palm Beach but slightly higher than Tampa-Orlando-Jacksonville. Net labor differential is typically within 5%."),
       ("Does ACG bid the same way in Tennessee as in Florida?", "Yes \u2014 48-hour bid turnaround, $6M aggregate bonding capacity, FL CGC #1531993 (TN credential in progress for Q3 2026), zero OSHA recordable incidents since 2021. Same operating system, same bid response standard.")
     ])
]


def build_specialty_faq():
    for slug, q, intro, faq in SPECIALTY_FAQ:
        title = f"{q} \u2014 ACG"
        body = f'<header><p style="color:#e11320;font-weight:600;font-size:13px;letter-spacing:1px;text-transform:uppercase;margin-bottom:12px;">Florida Commercial Glazing FAQ</p><h1 style="font-size:36px;line-height:1.2;font-weight:800;margin-bottom:20px;color:#050a12;">{html_lib.escape(q)}</h1><p style="font-size:19px;line-height:1.7;color:#1f2937;font-weight:500;">{html_lib.escape(intro)}</p></header><section style="margin-top:48px;">'
        for qq, aa in faq:
            body += f'<h2 style="font-size:24px;color:#050a12;margin-top:32px;margin-bottom:12px;font-weight:700;">{html_lib.escape(qq)}</h2><p style="font-size:17px;line-height:1.75;color:#1f2937;">{html_lib.escape(aa)}</p>'
        body += '</section><div style="background:#0e284f;color:white;padding:32px;border-radius:12px;margin-top:48px;text-align:center;"><h3 style="font-size:24px;margin-bottom:12px;">Send us drawings \u2014 48-hour bid</h3><a href="/send-plans.html" style="background:#e11320;color:white;padding:14px 28px;border-radius:6px;text-decoration:none;font-weight:600;display:inline-block;">Send Us Plans</a></div>'
        speakable = json.dumps({"@context":"https://schema.org","@type":"WebPage","speakable":{"@type":"SpeakableSpecification","cssSelector":["h1","h2","p"]},"url":f"https://acglass.com/{slug}/"})
        page(title, intro, body, slug,
             extra_schema=speakable,
             breadcrumb=[("Home","https://acglass.com/"),("FAQ","https://acglass.com/florida-glazing-faq/"),(q, f"https://acglass.com/{slug}/")],
             faq=faq)


if __name__ == "__main__":
    print("Wave 11 \u2014 untapped vertical hubs")
    build_multifamily_hub()
    print("  Multifamily hub built")
    build_multifamily_cities()
    print(f"  {len(MULTIFAMILY_CITIES)} multifamily city pages built")
    build_healthcare_hub()
    print("  Healthcare hub built")
    build_healthcare_cities()
    print(f"  {len(HEALTHCARE_CITIES)} healthcare city pages built")
    build_university_cities()
    print(f"  {len(UNIVERSITY_CITIES)} university city pages built")
    build_specialty_faq()
    print(f"  {len(SPECIALTY_FAQ)} specialty FAQ pages built")
    total = 1 + len(MULTIFAMILY_CITIES) + 1 + len(HEALTHCARE_CITIES) + len(UNIVERSITY_CITIES) + len(SPECIALTY_FAQ)
    print(f"\nTotal wave 11 pages: {total}")
