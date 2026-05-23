#!/usr/bin/env python3
"""ACG geo-page generator — beats AP Glazing.
Generates /{city}/index.html (76 hubs) and /{city}/{service}/index.html (304 service pages).
Each page: full schema, 1200+ words, real project anchors where available, HVHZ-aware content."""
import os, json, html as html_lib
from cities import CITIES, SERVICES, COUNTIES

OUT_BASE = "/home/user/workspace/acglass-website"

# ---------- shared building blocks ----------

NAV_HTML = '''<nav class="nav scrolled">
    <div class="nav-inner">
      <a href="/index.html" class="nav-logo"><img height="72" width="338" src="/images/acg-logo-nav@2x.png" style="height:36px;width:auto;" alt="ACG" class="logo-img" loading="lazy" decoding="async" fetchpriority="high"></a>
      <div class="nav-links">
        <a href="/index.html">Home</a><a href="/portfolio.html">Portfolio</a><a href="/services.html">Services</a>
        <a href="/about.html">About</a><a href="/manufacturers.html">Partners</a>
        <a href="/send-plans.html" class="nav-cta">Send Us Plans</a>
      </div>
      <button class="nav-toggle" aria-label="Menu"><span></span><span></span><span></span></button>
    </div>
  </nav>'''

DISAMBIG_FOOTER = '''<div class="acg-disambig-footer" style="border-top:1px solid rgba(255,255,255,0.06);padding:14px 0 6px;margin-top:8px;font-family:'JetBrains Mono',monospace;font-size:11px;letter-spacing:0.04em;color:rgba(255,255,255,0.55);text-align:left;">
        <a href="/acg.html" style="color:#E11320;text-decoration:none;font-weight:600;letter-spacing:0.06em;text-transform:uppercase;">ACG | American Commercial Glass</a> &nbsp;&middot;&nbsp; Florida commercial glazing contractor &nbsp;&middot;&nbsp; CGC1531993 &nbsp;&middot;&nbsp; <span style="color:rgba(255,255,255,0.4);">Not affiliated with ACG Glass &amp; Metals or AGC Inc.</span>
      </div>'''

FOOTER_HTML = lambda relative_root: f'''<footer class="footer">
    <div class="container">
      <div class="footer-grid">
        <div class="footer-brand"><a href="/index.html" class="nav-logo" style="margin-bottom:0;"><img height="72" width="338" src="/images/acg-logo-nav@2x.png" style="height:36px;width:auto;" alt="ACG" class="logo-img" loading="lazy" decoding="async"></a><p>Elite commercial glazing for Florida's most demanding projects.</p></div>
        <div><h5>Company</h5><div class="footer-links"><a href="/about.html">About</a><a href="/portfolio.html">Portfolio</a><a href="/services.html">Services</a><a href="/blog.html">Blog</a><a href="/manufacturers.html">Partners</a><a href="/capabilities.html">Capabilities</a><a href="/contact.html">Contact</a></div></div>
        <div><h5>Service Areas</h5><div class="footer-links"><a href="/service-areas.html">All Florida</a><a href="/west-palm-beach/">West Palm Beach</a><a href="/miami/">Miami</a><a href="/fort-lauderdale/">Fort Lauderdale</a><a href="/naples/">Naples</a><a href="/tampa/">Tampa</a></div></div>
        <div><h5>Contact</h5><div class="footer-contact"><p>connor@acglass.com</p><p>(772) 486-7711</p><p>West Palm Beach &bull; Naples &bull; Tampa</p></div></div>
      </div>
      {DISAMBIG_FOOTER}
      <div class="footer-bottom"><span>&copy; 2026 American Commercial Glass, Inc.</span><span>CGC #1531993 &bull; NAICS 238150</span></div>
    </div>
  </footer>'''

ORG_SAMEAS = [
    "https://www.wikidata.org/wiki/Q139858578",
    "https://www.linkedin.com/company/acglass",
    "https://www.facebook.com/acommercialglass",
    "https://www.instagram.com/acglass.co",
    "https://network.procore.com/p/american-commercial-glass-west-palm-beach",
    "https://www.bbb.org/us/fl/west-palm-beach/profile/window-installation/american-commercial-glass-inc-0633-92045708",
    "https://downtobid.com/company/american-commercial-glass",
    "https://www.yelp.com/biz/american-commercial-glass-west-palm-beach",
    "https://www.buildzoom.com/contractor/american-commercial-glass-inc",
    "https://www.esourcebook.net/west-palm-beach/glass-industry-supplier/american-commercial-glass",
]

# ---------- HVHZ-aware answer fragments ----------

def hvhz_storefront_answer(city, hvhz):
    if hvhz:
        return f"Yes — {city} is in Florida's High-Velocity Hurricane Zone (HVHZ). Every commercial storefront installation requires Miami-Dade Notice of Acceptance (NOA) documentation, installation per the NOA install instructions, and an inspection log. ACG's submittal packages include all NOA documentation current at submittal so the storefront passes inspection without back-and-forth."
    return f"{city} is outside the HVHZ envelope but still requires Florida Product Approval (FL#) documentation on every commercial system under Florida Building Code Section 1709. ACG includes FL# documentation in every submittal package."

def hvhz_entrance_answer(city, hvhz):
    if hvhz:
        return f"Yes — {city} is in Florida's HVHZ envelope. All-glass entrance doors must meet Miami-Dade NOA requirements for the configuration installed. Automatic openers must be tested and approved as part of the assembly. ACG submits NOA documentation and hardware spec together for {city} commercial openings."
    return f"All-glass entrances in {city} must meet Florida Building Code Section 2406 (safety glazing) and CPSC 16 CFR 1201 Category II. ACG's submittal documentation covers FL# approvals, glass make-up, and hardware spec in one package."

def hvhz_impact_answer(city, hvhz, county):
    if hvhz:
        return f"Yes — {city} ({county} County) is in Florida's HVHZ envelope. Commercial impact windows must carry Miami-Dade NOA documentation for the configuration. Exposure D ratings apply to direct ocean and Gulf-front sites. ACG carries NOA documentation current for ESWindows, PGT, and Slimpact configurations specified for {city} commercial work."
    if county in ("Indian River", "Brevard", "Martin", "St. Lucie", "Lee", "Collier", "Sarasota", "Charlotte", "Monroe", "Pinellas", "Manatee"):
        return f"{city} ({county} County) is outside HVHZ but in a coastal wind-borne debris region. Commercial impact windows require Florida Product Approval (FL#) with design pressure ratings appropriate for the exposure category — typically Exposure C for inland and Exposure D for direct coastal. ACG sources FL#-approved configurations from ESWindows, PGT, and Slimpact."
    return f"{city} ({county} County) is outside HVHZ. Commercial impact windows are recommended for storm protection and may be required by lender or insurer. ACG installs FL#-approved configurations with the appropriate design pressure rating for the project's exposure category."

# ---------- city hub page (one per city) ----------

CITY_HUB_TEMPLATE = '''<!DOCTYPE html>
<html lang="en">
<head>
<script async src="https://www.googletagmanager.com/gtag/js?id=G-M7BFQD2SPP"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag("js",new Date());gtag("config","G-M7BFQD2SPP");</script>
<meta charset="UTF-8">
<meta name="referrer" content="strict-origin-when-cross-origin">
<meta http-equiv="X-Content-Type-Options" content="nosniff">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Storefront Glazier {city} | Commercial Windows & Doors | ACG</title>
<link rel="icon" type="image/png" href="/images/favicon-32.png">
<meta name="description" content="Storefront glazier in {city}, FL. ACG does all things commercial storefront, commercial windows, and commercial doors. Hurricane impact, all-glass entrances, glass railings. Florida-licensed contractor CGC #1531993. 350+ commercial projects.{project_meta_suffix}">
<meta name="keywords" content="storefront glazier {city_lower}, commercial storefront {city_lower}, commercial windows {city_lower}, commercial doors {city_lower}, impact windows {city_lower}, glazier near {city_lower} fl, glass contractor {city_lower}">
<link rel="canonical" href="https://acglass.com/{slug}/">
<meta name="geo.position" content="{lat};{lon}">
<meta name="geo.placename" content="{city}, FL">
<meta name="geo.region" content="US-FL">
<meta name="ICBM" content="{lat}, {lon}">
<meta property="og:type" content="website">
<meta property="og:title" content="Storefront Glazier &mdash; {city}, FL | ACG">
<meta property="og:description" content="ACG is a Florida storefront glazing company serving {city}. All things commercial storefront, commercial windows, and commercial doors. CGC #1531993.">
<meta property="og:url" content="https://acglass.com/{slug}/">
<meta property="og:image" content="https://acglass.com/images/projects/ocean-prime-marina-aerial.jpg">
<meta property="og:site_name" content="American Commercial Glass">
<meta name="twitter:card" content="summary_large_image">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/css/style.css?v=1777031720">

<script type="application/ld+json">
{schema}
</script>

<style>
.loc-hero {{ padding: clamp(100px, 14vw, 180px) 0 clamp(48px, 6vw, 96px); border-bottom: 1px solid rgba(255,255,255,0.08); }}
.loc-label {{ font-family:'JetBrains Mono',monospace; font-size:11px; letter-spacing:0.15em; text-transform:uppercase; color: var(--accent); margin-bottom: 16px; }}
.chip {{ display: inline-block; padding: 8px 14px; background: rgba(255,255,255,0.04); border: 1px solid rgba(255,255,255,0.08); border-radius: 100px; font-size: 13px; color: rgba(255,255,255,0.75); margin: 4px 4px 4px 0; font-family: 'JetBrains Mono',monospace; }}
.stat-row {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(160px, 1fr)); gap: clamp(24px, 3vw, 48px); padding: clamp(28px, 4vw, 48px) 0; border-top: 1px solid rgba(255,255,255,0.06); border-bottom: 1px solid rgba(255,255,255,0.06); }}
.stat-num {{ font-family:'Inter',sans-serif; font-size: clamp(30px, 4vw, 48px); font-weight: 900; line-height: 1; margin-bottom: 8px; }}
.stat-num.accent {{ color: var(--accent); }}
.stat-label {{ font-family:'JetBrains Mono',monospace; font-size:11px; letter-spacing:0.08em; text-transform:uppercase; color: rgba(255,255,255,0.55); }}
.section-h {{ font-size: clamp(28px, 3.5vw, 42px); font-weight: 900; line-height: 1.1; margin-bottom: 22px; }}
.body-p {{ font-size: clamp(15px, 1.15vw, 17px); line-height: 1.75; color: rgba(255,255,255,0.72); margin-bottom: 16px; }}
.body-p strong {{ color: white; font-weight: 700; }}
.card-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: clamp(14px, 2vw, 24px); }}
.card {{ background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08); border-radius: var(--radius); padding: clamp(20px, 2.5vw, 30px); text-decoration: none; color: inherit; display: block; transition: border-color 0.2s; }}
.card:hover {{ border-color: rgba(225,19,32,0.4); }}
.card h4 {{ font-size: 17px; font-weight: 700; margin-bottom: 8px; line-height: 1.3; color: white; }}
.card p {{ font-size: 13px; color: rgba(255,255,255,0.65); line-height: 1.55; margin: 0; }}
.card-num {{ font-family:'JetBrains Mono',monospace; font-size:10px; color: var(--accent); margin-bottom: 10px; letter-spacing: 0.12em; }}
</style>
</head>
<body>
<a class="skip-link" href="#main-content">Skip to main content</a>
<div class="grain"></div>
{nav}

<main id="main-content">
  <section class="loc-hero">
    <div class="container">
      <div class="loc-label">Storefront Glazier &mdash; {city}, FL</div>
      <h1 style="font-size:clamp(38px,5.5vw,72px);font-weight:900;line-height:1.05;max-width:1000px;margin-bottom:22px;">Storefront glazier <span class="accent">in {city}.</span></h1>
      <p style="font-size:clamp(16px,1.35vw,19px);color:rgba(255,255,255,0.7);max-width:820px;line-height:1.6;margin-bottom:22px;">{hero_intro}</p>
      <div style="display:flex;gap:14px;margin-top:32px;flex-wrap:wrap;">
        <a href="/send-plans.html" class="btn btn-primary">Send Us Plans</a>
        <a href="tel:+17724867711" class="btn btn-secondary">Call (772) 486-7711</a>
      </div>
    </div>
  </section>

  <section class="container">
    <div class="stat-row">
      <div><div class="stat-num accent">{city_count}</div><div class="stat-label">{region}</div></div>
      <div><div class="stat-num">350+</div><div class="stat-label">FL Commercial Projects</div></div>
      <div><div class="stat-num">CGC</div><div class="stat-label">#1531993</div></div>
      <div><div class="stat-num">48 hr</div><div class="stat-label">Bid Turnaround</div></div>
    </div>
  </section>

  <section class="section">
    <div class="container">
      <div class="loc-label">Services in {city}</div>
      <h2 class="section-h">Commercial storefront, window, and door services <span class="accent">in {city}.</span></h2>
      <div class="card-grid">
        <a href="/{slug}/commercial-storefronts/" class="card">
          <div class="card-num">01 &mdash; Storefronts</div>
          <h4>Commercial Storefronts &mdash; {city}</h4>
          <p>Ground-floor retail, restaurant, and commercial storefronts. Aluminum framing, single-source glazing. $66-$142/SF installed.</p>
        </a>
        <a href="/{slug}/all-glass-entrances/" class="card">
          <div class="card-num">02 &mdash; Entrances</div>
          <h4>All-Glass Entrances &mdash; {city}</h4>
          <p>Frameless and minimally framed entrance doors. Pivot, herculite, automatic sliders. $4,500-$18,000 per opening.</p>
        </a>
        <a href="/{slug}/impact-windows-hurricane/" class="card">
          <div class="card-num">03 &mdash; Impact</div>
          <h4>Hurricane Impact Windows &mdash; {city}</h4>
          <p>Commercial impact windows and doors. ESWindows, PGT, Slimpact authorized. $78-$195/SF installed.</p>
        </a>
        <a href="/{slug}/glass-railings/" class="card">
          <div class="card-num">04 &mdash; Railings</div>
          <h4>Glass Railings &mdash; {city}</h4>
          <p>Balcony, terrace, and stair glass railings. Tempered or laminated, top-rail or frameless. $145-$385/LF.</p>
        </a>
      </div>
    </div>
  </section>

  <section class="section" style="padding-top:0;">
    <div class="container">
      <div class="loc-label">{city} Context</div>
      <h2 class="section-h">Commercial glazing in {city}, <span class="accent">{county} County.</span></h2>
      <div style="max-width:860px;">
        {context_body}
      </div>
    </div>
  </section>

  {projects_section}

  <section class="section" style="padding-top:0;">
    <div class="container">
      <div class="loc-label">Why GCs Choose ACG in {city}</div>
      <h2 class="section-h">{why_choose_h2}</h2>
      <div class="card-grid">
        <div class="card" style="cursor:default;">
          <div class="card-num">Licensed</div>
          <h4>CGC #1531993</h4>
          <p>Florida Certified General Contractor. Connor Walsh qualifier. Full GL, Workers Comp, and Auto with Additional Insured language standard. $3M single / $6M aggregate bonding.</p>
        </div>
        <div class="card" style="cursor:default;">
          <div class="card-num">Authorized</div>
          <h4>6 Manufacturer Partnerships</h4>
          <p>Authorized installer for ESWindows (Tecnoglass), Euro-Wall, PGT Innovations, Allegion, TGP, and Slimpact. Direct factory engineering support for {city} commercial scopes.</p>
        </div>
        <div class="card" style="cursor:default;">
          <div class="card-num">Bid Speed</div>
          <h4>48-Hour Turnaround</h4>
          <p>{city} commercial scope bids return within 48 hours. Send plans, BuildingConnected invite, or scope description. Schedule and budget back in your inbox in two days.</p>
        </div>
        <div class="card" style="cursor:default;">
          <div class="card-num">{hvhz_label}</div>
          <h4>{hvhz_card_h4}</h4>
          <p>{hvhz_card_body}</p>
        </div>
        <div class="card" style="cursor:default;">
          <div class="card-num">GC-Direct</div>
          <h4>GC-Direct, Not Retail</h4>
          <p>ACG bids directly to general contractors and commercial owners. Active on Procore and BuildingConnected. {city} GC relationships across the commercial market.</p>
        </div>
        <div class="card" style="cursor:default;">
          <div class="card-num">3 Offices</div>
          <h4>{office_proximity}</h4>
          <p>ACG operates from West Palm Beach (HQ), Naples, and Tampa. Nashville Q3 2026. Daily {city} project management with crews staged for the {region} market.</p>
        </div>
      </div>
    </div>
  </section>

  <section class="section" style="padding-top:0;">
    <div class="container">
      <div class="loc-label">Nearby Coverage</div>
      <h2 class="section-h">Also serving <span class="accent">{region}.</span></h2>
      <div class="card-grid">
        {neighbor_cards}
      </div>
    </div>
  </section>

  <section class="cta-section">
    <div class="container">
      <h2>{city} project?<br><span class="accent">Bid in 48 hours.</span></h2>
      <p>ACG is a Florida-licensed commercial glazing contractor (CGC #1531993) serving {city}, {county} County, and all of Florida. Send plans, a BuildingConnected invite, or a scope description and our team will have a commercial glazing bid back within 48 hours.</p>
      <a href="/send-plans.html" class="btn btn-primary btn-lg">Send Us Plans <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14M12 5l7 7-7 7"/></svg></a>
    </div>
  </section>
</main>

{footer}
<script src="/js/main.js"></script>
</body>
</html>
'''

# ---------- service page (one per city × service) ----------

SERVICE_PAGE_TEMPLATE = '''<!DOCTYPE html>
<html lang="en">
<head>
<script async src="https://www.googletagmanager.com/gtag/js?id=G-M7BFQD2SPP"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag("js",new Date());gtag("config","G-M7BFQD2SPP");</script>
<meta charset="UTF-8">
<meta name="referrer" content="strict-origin-when-cross-origin">
<meta http-equiv="X-Content-Type-Options" content="nosniff">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{service_name} {city} | {h1_short} | ACG</title>
<link rel="icon" type="image/png" href="/images/favicon-32.png">
<meta name="description" content="{service_name} in {city}, FL. ${price_low}-${price_high}/{price_unit}. ACG is a Florida-licensed commercial glazing contractor (CGC #1531993) with 350+ commercial projects. 48-hour bid turnaround.">
<meta name="keywords" content="{intent_keyword} {city_lower}, {service_slug_kw} {city_lower} fl, {city_lower} {intent_keyword}, glazier {city_lower}">
<link rel="canonical" href="https://acglass.com/{city_slug}/{service_slug}/">
<meta name="geo.position" content="{lat};{lon}">
<meta name="geo.placename" content="{city}, FL">
<meta name="geo.region" content="US-FL">
<meta name="ICBM" content="{lat}, {lon}">
<meta property="og:type" content="website">
<meta property="og:title" content="{service_name} &mdash; {city}, FL | ACG">
<meta property="og:description" content="ACG installs {intent_keyword} in {city}, FL. CGC #1531993. ${price_low}-${price_high}/{price_unit}. 48-hour bid turnaround.">
<meta property="og:url" content="https://acglass.com/{city_slug}/{service_slug}/">
<meta property="og:image" content="https://acglass.com/images/projects/ocean-prime-marina-aerial.jpg">
<meta name="twitter:card" content="summary_large_image">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/css/style.css?v=1777031720">

<script type="application/ld+json">
{schema}
</script>

<style>
.loc-hero {{ padding: clamp(100px, 14vw, 180px) 0 clamp(48px, 6vw, 96px); border-bottom: 1px solid rgba(255,255,255,0.08); }}
.loc-label {{ font-family:'JetBrains Mono',monospace; font-size:11px; letter-spacing:0.15em; text-transform:uppercase; color: var(--accent); margin-bottom: 16px; }}
.stat-row {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(160px, 1fr)); gap: clamp(24px, 3vw, 48px); padding: clamp(28px, 4vw, 48px) 0; border-top: 1px solid rgba(255,255,255,0.06); border-bottom: 1px solid rgba(255,255,255,0.06); }}
.stat-num {{ font-family:'Inter',sans-serif; font-size: clamp(28px, 4vw, 44px); font-weight: 900; line-height: 1; margin-bottom: 8px; }}
.stat-num.accent {{ color: var(--accent); }}
.stat-label {{ font-family:'JetBrains Mono',monospace; font-size:11px; letter-spacing:0.08em; text-transform:uppercase; color: rgba(255,255,255,0.55); }}
.section-h {{ font-size: clamp(28px, 3.5vw, 42px); font-weight: 900; line-height: 1.1; margin-bottom: 22px; }}
.body-p {{ font-size: clamp(15px, 1.15vw, 17px); line-height: 1.75; color: rgba(255,255,255,0.72); margin-bottom: 16px; }}
.body-p strong {{ color: white; font-weight: 700; }}
.faq-item {{ border-top: 1px solid rgba(255,255,255,0.08); padding: 24px 0; }}
.faq-item:last-child {{ border-bottom: 1px solid rgba(255,255,255,0.08); }}
.faq-q {{ font-size: 18px; font-weight: 700; margin-bottom: 10px; color: white; }}
.card-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: clamp(14px, 2vw, 24px); }}
.card {{ background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08); border-radius: var(--radius); padding: clamp(20px, 2.5vw, 28px); text-decoration: none; color: inherit; display: block; transition: border-color 0.2s; }}
.card:hover {{ border-color: rgba(225,19,32,0.4); }}
.card h4 {{ font-size: 16px; font-weight: 700; margin-bottom: 8px; line-height: 1.3; color: white; }}
.card p {{ font-size: 13px; color: rgba(255,255,255,0.65); line-height: 1.55; margin: 0; }}
.card-num {{ font-family:'JetBrains Mono',monospace; font-size:10px; color: var(--accent); margin-bottom: 10px; letter-spacing: 0.12em; }}
</style>
</head>
<body>
<a class="skip-link" href="#main-content">Skip to main content</a>
<div class="grain"></div>
{nav}

<main id="main-content">
  <section class="loc-hero">
    <div class="container">
      <nav aria-label="Breadcrumb" style="margin-bottom:14px;font-family:'JetBrains Mono',monospace;font-size:11px;letter-spacing:0.12em;text-transform:uppercase;color:rgba(255,255,255,0.45);">
        <a href="/" style="color:rgba(255,255,255,0.55);text-decoration:none;">Home</a> &nbsp;/&nbsp;
        <a href="/service-areas.html" style="color:rgba(255,255,255,0.55);text-decoration:none;">Service Areas</a> &nbsp;/&nbsp;
        <a href="/{city_slug}/" style="color:rgba(255,255,255,0.55);text-decoration:none;">{city}</a> &nbsp;/&nbsp;
        <span style="color:#E11320;">{service_name}</span>
      </nav>
      <div class="loc-label">{service_name} &mdash; {city}, FL</div>
      <h1 style="font-size:clamp(34px,5vw,64px);font-weight:900;line-height:1.05;max-width:1000px;margin-bottom:22px;">{h1_text} <span class="accent">in {city}.</span></h1>
      <p style="font-size:clamp(16px,1.35vw,19px);color:rgba(255,255,255,0.7);max-width:820px;line-height:1.6;margin-bottom:22px;">{lead_paragraph}</p>
      <div style="display:flex;gap:14px;margin-top:32px;flex-wrap:wrap;">
        <a href="/send-plans.html" class="btn btn-primary">Get a {city} Bid in 48 Hours</a>
        <a href="tel:+17724867711" class="btn btn-secondary">Call (772) 486-7711</a>
      </div>
    </div>
  </section>

  <section class="container">
    <div class="stat-row">
      <div><div class="stat-num accent">${price_low}-${price_high}</div><div class="stat-label">Per {price_unit} ({city})</div></div>
      <div><div class="stat-num">48 hr</div><div class="stat-label">Bid Turnaround</div></div>
      <div><div class="stat-num">{hvhz_short}</div><div class="stat-label">{hvhz_short_label}</div></div>
      <div><div class="stat-num">CGC</div><div class="stat-label">#1531993</div></div>
    </div>
  </section>

  <section class="section">
    <div class="container">
      <div class="loc-label">{service_name} in {city}</div>
      <h2 class="section-h">{section1_h2}</h2>
      <div style="max-width:860px;">
        {section1_body}
      </div>
    </div>
  </section>

  <section class="section" style="padding-top:0;">
    <div class="container">
      <div class="loc-label">Standards &amp; Documentation</div>
      <h2 class="section-h">{section2_h2}</h2>
      <div style="max-width:860px;">
        {section2_body}
      </div>
    </div>
  </section>

  {projects_section}

  <section class="section" style="padding-top:0;">
    <div class="container">
      <div class="loc-label">{city} {service_name} FAQ</div>
      <h2 class="section-h">Common questions, <span class="accent">answered.</span></h2>
      <div style="max-width:820px;">
        {faqs_html}
      </div>
    </div>
  </section>

  <section class="section" style="padding-top:0;">
    <div class="container">
      <div class="loc-label">Other Services in {city}</div>
      <h2 class="section-h">Full Division 08 scope <span class="accent">in {city}.</span></h2>
      <div class="card-grid">
        {other_services_cards}
      </div>
    </div>
  </section>

  <section class="cta-section">
    <div class="container">
      <h2>{city} {service_name_lower}?<br><span class="accent">48-hour bid response.</span></h2>
      <p>ACG installs {intent_keyword} for general contractors, restaurant operators, hospitality groups, and developers across {city} and the rest of {region}. Send plans, a BuildingConnected invite, or a scope description and our team will have a bid back within 48 hours. CGC #1531993. $3M/$6M bonding.</p>
      <a href="/send-plans.html" class="btn btn-primary btn-lg">Send Us Plans</a>
    </div>
  </section>
</main>

{footer}
<script src="/js/main.js"></script>
</body>
</html>
'''


# ---------- helpers ----------

def get_neighbor_cards(city_slug, region, n=6):
    others = [c for c in CITIES if c[0] != city_slug and c[7] == region]
    out = []
    for c in others[:n]:
        slug, name, county, hvhz, exposure, lat, lon, reg, projects = c
        out.append(f'''<a href="/{slug}/" class="card">
          <div class="card-num">{county} County</div>
          <h4>{name}</h4>
          <p>Commercial glazing services in {name}, {county} County. Storefronts, impact, curtainwall, glass railings.</p>
        </a>''')
    return "\n".join(out)


def build_city_schema(slug, city, county, lat, lon, hvhz):
    address_locality = city
    schema = {
      "@context": "https://schema.org",
      "@graph": [
        {
          "@type": ["LocalBusiness", "HomeAndConstructionBusiness"],
          "@id": f"https://acglass.com/{slug}/#localbusiness",
          "name": f"American Commercial Glass — {city}",
          "alternateName": ["ACG", "ACG Glass", "American Commercial Glass"],
          "image": "https://acglass.com/images/acg-logo-nav@2x.png",
          "url": f"https://acglass.com/{slug}/",
          "telephone": "+17724867711",
          "email": "connor@acglass.com",
          "priceRange": "$$$",
          "address": {
            "@type": "PostalAddress",
            "addressLocality": address_locality,
            "addressRegion": "FL",
            "addressCountry": "US"
          },
          "geo": {"@type": "GeoCoordinates", "latitude": lat, "longitude": lon},
          "areaServed": [{"@type": "City", "name": city}, {"@type": "AdministrativeArea", "name": f"{county} County"}],
          "serviceType": "Commercial Glazing Contractor",
          "sameAs": ORG_SAMEAS
        },
        {
          "@type": "BreadcrumbList",
          "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://acglass.com/"},
            {"@type": "ListItem", "position": 2, "name": "Service Areas", "item": "https://acglass.com/service-areas.html"},
            {"@type": "ListItem", "position": 3, "name": city, "item": f"https://acglass.com/{slug}/"}
          ]
        }
      ]
    }
    return json.dumps(schema, indent=2)


def build_service_schema(city_slug, city, county, lat, lon, service, hvhz):
    schema = {
      "@context": "https://schema.org",
      "@graph": [
        {
          "@type": "Service",
          "name": f"{service['name']} — {city}, FL",
          "description": f"ACG installs {service['intent_keyword']} for commercial projects in {city}, {county} County. Florida-licensed CGC #1531993, $3M/$6M bonding, 350+ commercial projects.",
          "provider": {
            "@type": "LocalBusiness",
            "@id": f"https://acglass.com/{city_slug}/{service['slug']}/#provider",
            "name": "American Commercial Glass",
            "telephone": "+17724867711",
            "url": "https://acglass.com",
            "address": {
              "@type": "PostalAddress",
              "streetAddress": "700 S Rosemary Ave Suite 204",
              "addressLocality": "West Palm Beach",
              "addressRegion": "FL",
              "postalCode": "33401",
              "addressCountry": "US"
            },
            "sameAs": ORG_SAMEAS
          },
          "serviceType": service["schema_service"],
          "areaServed": {"@type": "City", "name": city, "containedInPlace": {"@type": "AdministrativeArea", "name": f"{county} County, FL"}},
          "offers": {
            "@type": "Offer",
            "priceCurrency": "USD",
            "priceSpecification": {
              "@type": "PriceSpecification",
              "minPrice": service["price_low"],
              "maxPrice": service["price_high"],
              "priceCurrency": "USD",
              "unitText": service["price_unit"]
            }
          }
        },
        {
          "@type": "BreadcrumbList",
          "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://acglass.com/"},
            {"@type": "ListItem", "position": 2, "name": "Service Areas", "item": "https://acglass.com/service-areas.html"},
            {"@type": "ListItem", "position": 3, "name": city, "item": f"https://acglass.com/{city_slug}/"},
            {"@type": "ListItem", "position": 4, "name": service["name"], "item": f"https://acglass.com/{city_slug}/{service['slug']}/"}
          ]
        },
        {
          "@type": "FAQPage",
          "mainEntity": [
            build_faq_qa(q, a, city, hvhz, county) for q, a in service["faqs"]
          ]
        }
      ]
    }
    return json.dumps(schema, indent=2)


def build_faq_qa(q, a, city, hvhz, county):
    answer_text = a.format(
        city=city,
        hvhz_storefront_answer=hvhz_storefront_answer(city, hvhz),
        hvhz_entrance_answer=hvhz_entrance_answer(city, hvhz),
        hvhz_impact_answer=hvhz_impact_answer(city, hvhz, county),
    )
    return {
        "@type": "Question",
        "name": q.format(city=city),
        "acceptedAnswer": {"@type": "Answer", "text": answer_text}
    }


def render_city_hub(city_data):
    slug, city, county, hvhz, exposure, lat, lon, region, projects = city_data

    # Hero intro
    hvhz_phrase = "in Florida's High-Velocity Hurricane Zone (HVHZ) " if hvhz else ""
    project_meta_suffix = ""
    if projects:
        names = [p.replace("case-study-", "").replace("-", " ").title() for p in projects[:2]]
        project_meta_suffix = f" Notable projects: {', '.join(names)}."

    hvhz_note = (f"Every commercial opening in {city} is in HVHZ and requires Miami-Dade NOA documentation. ACG carries the NOA inventory current."
        if hvhz else f"{city} commercial work requires Florida Product Approval (FL#) documentation, which ACG includes in every submittal package.")
    hero_intro = (
        f"American Commercial Glass (ACG) is a Florida storefront glazing company serving {city}, {county} County, "
        f"and the rest of {region}. We do all things commercial storefront, commercial windows, and commercial doors "
        f"&mdash; storefront systems, entrances, hurricane impact glass, glass railings, and the full Division 08 envelope &mdash; "
        f"for general contractors, restaurant operators, hospitality groups, and developers. {hvhz_note} "
        f"350+ commercial projects, 1M+ SF installed. CGC #1531993. 48-hour bid turnaround."
    )
    # END hero_intro

    # Context body
    hvhz_sentence = (
        "It is in Florida's High-Velocity Hurricane Zone (HVHZ), which means every commercial storefront, window, and door must carry Miami-Dade NOA documentation for the specific configuration installed."
        if hvhz else
        "It is outside HVHZ but commercial storefronts, windows, and doors still require Florida Product Approval (FL#) documentation under FBC Section 1709."
    )
    exposure_suffix = " for direct ocean or Gulf-front sites" if exposure == "D" else ""
    context_parts = [
        f"<p class='body-p'><strong>{city} storefront glazing context.</strong> {city} is in {county} County, in Florida's {region} market. {hvhz_sentence} Exposure category for {city} commercial work is typically <strong>{exposure}</strong>{exposure_suffix}.</p>",
        f"<p class='body-p'><strong>What ACG does in {city}.</strong> We do all things commercial storefront, commercial windows, and commercial doors. Storefront systems for ground-floor retail, restaurants, and commercial buildings. Commercial entrance doors &mdash; aluminum-framed, all-glass, automatic sliders, pivots. Hurricane impact windows and impact-rated commercial doors. Window walls and curtainwall. Glass railings for balconies and terraces. The full Division 08 scope, single-source from the storefront frame to the hardware to the submittal package.</p>",
        f"<p class='body-p'><strong>Who we work with in {city}.</strong> ACG bids directly to general contractors active in the {city} market, restaurant operators, hospitality and hotel ownership groups, healthcare systems, private clubs, multifamily developers, and commercial property owners. We are active on Procore and BuildingConnected for {city} project invites, and the 48-hour bid turnaround that ACG runs on commercial storefront and window work fits the operator and GC timeline at the front of the project.</p>",
        f"<p class='body-p'><strong>Pricing and timeline for {city} storefront and commercial window work.</strong> Commercial storefronts run $66-$142 per square foot installed in {city}, depending on glass make-up and exposure category. Hurricane impact commercial windows run $78-$195/SF. All-glass commercial entrance doors run $4,500-$18,000 per opening. Glass railings run $145-$385/LF. Lead times are 8-16 weeks from approved shop drawings depending on system, plus 2-8 days of field installation. ACG locks rough opening dimensions in pre-construction so the field install runs on schedule.</p>",
    ]
    context_body = "\n        ".join(context_parts)

    # Projects section
    projects_section = ""
    if projects:
        proj_cards = []
        for p in projects:
            display = p.replace("case-study-", "").replace("-", " ").title()
            href = f"/{p}.html"
            proj_cards.append(f'''<a href="{href}" class="card">
              <div class="card-num">{city} delivered</div>
              <h4>{display}</h4>
              <p>ACG commercial glazing project completed in {city}. Photographed in the portfolio.</p>
            </a>''')
        projects_section = f'''<section class="section" style="padding-top:0;">
    <div class="container">
      <div class="loc-label">{city} Projects</div>
      <h2 class="section-h">Delivered in <span class="accent">{city}.</span></h2>
      <div class="card-grid">
        {"".join(proj_cards)}
      </div>
    </div>
  </section>'''

    # HVHZ card
    if hvhz:
        hvhz_label = "HVHZ"
        hvhz_card_h4 = "Miami-Dade NOA Documentation"
        hvhz_card_body = f"{city} is in HVHZ. Every commercial opening requires current Miami-Dade NOA. ACG's submittal package includes NOA, install instructions tied to the approval, and engineer-stamped shop drawings where required."
    else:
        hvhz_label = "FL Product"
        hvhz_card_h4 = "Florida Product Approval"
        hvhz_card_body = f"{city} is outside HVHZ but FBC Section 1709 still requires Florida Product Approval (FL#) on every commercial system. ACG includes FL# documentation in every {city} submittal package."

    # Office proximity
    if region == "South Florida":
        office_proximity = "West Palm Beach HQ"
    elif region == "Treasure Coast":
        office_proximity = "West Palm Beach Office"
    elif region in ("Southwest Florida",):
        office_proximity = "Naples Office"
    elif region == "Tampa Bay" or region == "Central Florida" or region == "Space Coast":
        office_proximity = "Tampa Office"
    else:
        office_proximity = "Florida Coverage"

    # Region city count
    region_count = sum(1 for c in CITIES if c[7] == region)
    why_choose_h2 = f"<span class='accent'>{city}</span> commercial glazing &mdash; <span class='accent'>built to specification.</span>"

    schema = build_city_schema(slug, city, county, lat, lon, hvhz)
    neighbor_cards = get_neighbor_cards(slug, region, 6)

    return CITY_HUB_TEMPLATE.format(
        slug=slug,
        city=city,
        city_lower=city.lower(),
        county=county,
        region=region,
        city_count=region_count,
        lat=lat,
        lon=lon,
        nav=NAV_HTML,
        footer=FOOTER_HTML("../"),
        schema=schema,
        hero_intro=hero_intro,
        context_body=context_body,
        projects_section=projects_section,
        why_choose_h2=why_choose_h2,
        hvhz_label=hvhz_label,
        hvhz_card_h4=hvhz_card_h4,
        hvhz_card_body=hvhz_card_body,
        office_proximity=office_proximity,
        neighbor_cards=neighbor_cards,
        project_meta_suffix=project_meta_suffix,
    )


def render_service_page(city_data, service):
    slug, city, county, hvhz, exposure, lat, lon, region, projects = city_data
    service_name = service["name"]
    service_slug = service["slug"]

    # Lead paragraph
    if service_slug == "commercial-storefronts":
        lead = f"ACG installs commercial storefront systems for ground-floor retail, restaurants, and commercial buildings in {city}, {county} County. {service['intro']} ${service['price_low']}-${service['price_high']} per {service['price_unit']} installed in {city}. CGC #1531993."
    elif service_slug == "all-glass-entrances":
        lead = f"ACG installs all-glass entrance door systems for commercial buildings in {city}, {county} County. {service['intro']} ${service['price_low']:,}-${service['price_high']:,} per opening in {city}. CGC #1531993."
    elif service_slug == "impact-windows-hurricane":
        lead = f"ACG installs commercial hurricane impact windows and doors in {city}, {county} County. {service['intro']} ${service['price_low']}-${service['price_high']} per {service['price_unit']} installed in {city}. CGC #1531993."
    else:
        lead = f"ACG installs glass railing systems for commercial and multifamily buildings in {city}, {county} County. {service['intro']} ${service['price_low']}-${service['price_high']} per {service['price_unit']} installed in {city}. CGC #1531993."

    # Section 1 / 2 — build conditional fragments first (avoids backslash-in-fstring issues)
    s1_h2 = f"{service_name} in {city}, FL."

    # Pre-compute fragments based on hvhz/exposure/county
    storefront_select_frag = (f"In HVHZ {city}, commercial storefronts require Miami-Dade NOA-approved configurations."
        if hvhz else f"{city} commercial storefronts require Florida Product Approval (FL#) documentation with design pressure ratings appropriate for the exposure category.")
    expo_dp_suffix = " with elevated DP for direct ocean exposure" if exposure == "D" else ""
    dept_phrase = "Miami-Dade" if hvhz else "local"
    storefront_s2_open = (f"In HVHZ {city}, every commercial storefront requires Miami-Dade NOA documentation. The NOA covers the specific framing, glass make-up, and anchorage configuration. ACG submittal packages include the current NOA, installation instructions tied directly to the approval, engineer-stamped shop drawings where the project requires, and a field inspection log the GC can attach to the inspection request."
        if hvhz else f"{city} is outside HVHZ but Florida Building Code Section 1709 still requires Florida Product Approval (FL#) documentation on every commercial storefront. ACG submittal packages include FL# documentation, glass make-up specification, hardware spec, and engineer-stamped shop drawings where the project requires.")

    entrance_select_frag = (f"In HVHZ {city}, impact-rated configurations are required and ACG sources Miami-Dade NOA-approved hardware and glass make-ups."
        if hvhz else f"{city} all-glass entrances must meet FBC Section 2406 safety glazing requirements and CPSC 16 CFR 1201 Category II.")
    entrance_glass_frag = (f"In HVHZ {city}, all-glass entrance glass make-ups must be Miami-Dade NOA-approved laminated configurations meeting the impact requirements for the project exposure."
        if hvhz else f"{city} all-glass entrances use tempered or tempered-laminated configurations meeting safety glazing requirements per FBC Section 2406.")

    impact_s1_open = (f"Every commercial opening in {city} requires impact protection per Florida Building Code, and HVHZ designation means Miami-Dade NOA documentation on every installation."
        if hvhz else f"{city} ({county} County) is outside HVHZ but in a wind-borne debris region. Commercial impact windows are required by FBC where the building site exposure and structural design call for them, and may also be required by lender or insurer.")
    expo_label_frag = " for direct coastal" if exposure == "D" else " for inland"
    impact_invest_frag = ("HVHZ NOA-rated configurations and Exposure D coastal sites run at the upper end."
        if hvhz else "Exposure D direct coastal sites and higher design pressures run at the upper end.")
    impact_doc_frag = (f"Miami-Dade NOA is required on every commercial impact window installation in HVHZ {city}."
        if hvhz else f"{city} commercial impact windows require Florida Product Approval (FL#) documentation under FBC Section 1709.")

    railing_hw_frag = (f"Coastal {city} sites require stainless 316 hardware for corrosion resistance &mdash; anodized aluminum and standard stainless 304 will not survive the salt environment."
        if exposure == "D" else f"{city} sites use anodized aluminum or stainless 304 hardware depending on architectural intent.")

    if service_slug == "commercial-storefronts":
        s1_body = (
            f"<p class='body-p'><strong>{city} storefront work.</strong> {city} commercial storefront projects in 2026 cover ground-floor retail in mixed-use buildings, restaurant entries with operating glass envelopes, and standalone commercial buildings ranging from professional offices to medical and institutional uses. ACG bids storefront systems for {city} general contractors and restaurant operators with the full Division 08 scope: aluminum framing, single-source glazing, hardware coordination, and complete submittal documentation.</p>"
            f"<p class='body-p'><strong>System selection in {city}.</strong> {storefront_select_frag} ACG specifies storefront systems with the design pressure (DP) rating and exposure category appropriate for the {city} site &mdash; typically Exposure {exposure}{expo_dp_suffix}. We source from manufacturers with current Florida documentation and direct factory engineering support.</p>"
            f"<p class='body-p'><strong>Lead time and pricing in {city}.</strong> Commercial storefront lead times run 10-16 weeks from approved shop drawings, with 3-7 days of field installation for a standard 30-foot storefront. Pricing in {city} runs ${service['price_low']}-${service['price_high']} per square foot installed for the all-in scope including material, labor, NOA or FL# documentation, and {dept_phrase} building department submittal package. {city} oceanfront and direct-coastal sites run at the upper end of the range due to elevated design pressure requirements.</p>"
        )
        s2_h2 = "Code, NOA, and submittal discipline."
        s2_body = (
            f"<p class='body-p'>{storefront_s2_open}</p>"
            f"<p class='body-p'><strong>{city} permit and inspection.</strong> ACG handles permit submittal coordination with the GC and the {city} building department. We pull the NOA or FL# documentation current at submittal, align the shop drawings with the approved configuration, and document the field installation against the installation instructions with a photo log. The result: {city} commercial storefront installations close out at certificate of occupancy without surprise items at the building department.</p>"
            f"<p class='body-p'><strong>Manufacturer relationships.</strong> ACG is an authorized installer for the commercial storefront product lines we specify, with direct factory engineering support on configuration selection, design pressure, and NOA or FL# documentation. We do not bid a storefront system and then quietly substitute a less-rated competitor product at fabrication time. The product the architect specified is the product we install.</p>"
        )
    elif service_slug == "all-glass-entrances":
        s1_body = (
            f"<p class='body-p'><strong>{city} all-glass entrance work.</strong> Frameless and minimally framed all-glass entrance systems serve as the architectural moment at retail, hospitality, restaurant, office lobby, and institutional building entries in {city}. ACG installs all-glass entrances with the hardware (top and bottom pivots, side patches, automatic openers) coordinated as a single-source assembly with the glass make-up, the operator, and the floor and head condition. The result: an entrance that operates daily for years without alignment issues or hardware service calls.</p>"
            f"<p class='body-p'><strong>System options in {city}.</strong> Common configurations: single or double frameless pivot doors, herculite-style entrances with header and floor patches, automatic sliding doors with full-glass side panels, and pivot doors with sensor-operated openers. {entrance_select_frag}</p>"
            f"<p class='body-p'><strong>Investment in {city}.</strong> An all-glass entrance in {city} typically runs ${service['price_low']:,}-${service['price_high']:,} per opening depending on configuration, glass thickness, hardware finish, and automatic operator selection. ACG provides material + labor + submittal documentation + operator coordination in the all-in number. Lead time is 6-10 weeks from approved shop drawings, with 1-2 days of field installation.</p>"
        )
        s2_h2 = "Hardware, glass, and operator coordination."
        s2_body = (
            f"<p class='body-p'><strong>Hardware sources.</strong> ACG specifies all-glass entrance hardware from Allegion (Dorma, FSB), CRL, and TGP depending on the project. Pivots are bottom-mounted floor closers or top-pivot offset depending on the floor condition and operating cycle. For high-traffic {city} retail or restaurant entries we specify floor closers rated for daily operation cycles in the 200,000+ range.</p>"
            f"<p class='body-p'><strong>Glass make-up.</strong> {entrance_glass_frag} ACG specifies the appropriate make-up and provides Florida Product Approval (FL#) or NOA documentation as required.</p>"
            f"<p class='body-p'><strong>Operator and access control.</strong> ACG coordinates with the GC electrical and access control contractors on automatic operator installation, sensor placement, and access control integration. We pull operator specs from the manufacturer and verify power and control runs in pre-construction so the entrance commissions on first try.</p>"
        )
    elif service_slug == "impact-windows-hurricane":
        s1_body = (
            f"<p class='body-p'><strong>{city} commercial impact window context.</strong> ACG installs commercial-grade hurricane impact windows and doors in {city}, {county} County. {impact_s1_open} As a commercial storefront and window contractor, we source from the leading manufacturers with current Florida Product Approval and Miami-Dade NOA documentation. We are an authorized installer for major commercial impact glass and impact-rated door product lines.</p>"
            f"<p class='body-p'><strong>System selection in {city}.</strong> ACG specifies impact window configurations based on the {city} site exposure category (typically Exposure {exposure}{expo_label_frag}), design pressure requirements from the project structural engineer, glass make-up (laminate thickness, low-E coating, thermal performance), and frame profile and finish. We source from leading commercial impact storefront, window wall, and sliding door manufacturers with current Florida documentation. The right system for the project is selected together with the architect &mdash; ACG installs the system the architect specified.</p>"
            f"<p class='body-p'><strong>Investment in {city}.</strong> Commercial impact windows in {city} run ${service['price_low']}-${service['price_high']} per square foot installed for the all-in scope. {impact_invest_frag} ACG includes material, labor, NOA or FL# documentation, and the full submittal package.</p>"
        )
        s2_h2 = "NOA, FL#, and Florida Building Code."
        s2_body = (
            f"<p class='body-p'><strong>{city} documentation requirements.</strong> {impact_doc_frag} ACG carries NOA and FL# documentation current and submits it as part of the permit package along with the installation instructions, shop drawings, and engineer stamp where the project requires.</p>"
            f"<p class='body-p'><strong>Manufacturer specifications.</strong> ACG specifies impact window configurations from manufacturers with current Florida documentation and direct factory engineering support. We do not substitute a less-rated product at fabrication time. The architect specifies the system; ACG installs the system specified.</p>"
            f"<p class='body-p'><strong>Inspection and closeout.</strong> ACG documents field installation against the NOA or FL# install instructions with a photo log the GC can attach to inspection requests. The result: {city} commercial impact window installations close out at certificate of occupancy without back-and-forth on documentation.</p>"
        )
    else:  # glass-railings
        s1_body = (
            f"<p class='body-p'><strong>{city} glass railing context.</strong> ACG installs glass railing systems for commercial balconies, terraces, stair guards, and pool deck enclosures in {city}, {county} County. Glass railings replace traditional metal pickets with tempered or laminated glass panels, supported by either a top-rail aluminum or stainless system or a fully frameless (channel-anchored or post-mounted) design. The architectural intent is sightlines &mdash; the glass disappears, the view does not.</p>"
            f"<p class='body-p'><strong>System selection in {city}.</strong> Top-rail glass railing systems with anodized aluminum or stainless top rails are the most common for multifamily balconies and commercial terraces in {city}. Frameless channel-anchored systems are specified for high-end residential, restaurant terrace, and pool deck applications where the railing is the architectural moment. {railing_hw_frag}</p>"
            f"<p class='body-p'><strong>Investment in {city}.</strong> Glass railings in {city} run ${service['price_low']}-${service['price_high']} per linear foot installed. Frameless systems and stainless 316 hardware run at the upper end. ACG provides material, labor, engineer documentation, and full submittal package in the all-in number. Lead time is 6-9 weeks from approved shop drawings, with 2-4 days of field installation for a typical multifamily balcony stack or commercial terrace.</p>"
        )
        s2_h2 = "Code, glass standards, and engineering."
        s2_body = (
            f"<p class='body-p'><strong>Loading and testing.</strong> ACG installs glass railings to Florida Building Code Section 1607.8 (handrail and guard loading), ASTM E2358 (testing standard for guards), and ASTM E1300 (glass strength). The standard guard loading requirement is 50 plf concentrated load + 200 lb concentrated load at any point. Heat-soak-tested glass is available on request to mitigate the rare risk of nickel-sulfide-inclusion spontaneous breakage.</p>"
            f"<p class='body-p'><strong>Glass make-up.</strong> Tempered glass meets CPSC 16 CFR 1201 Category II safety glazing requirements. For commercial guard applications where post-break performance matters (the glass must stay in the opening even if broken), ACG specifies laminated tempered or laminated heat-strengthened make-ups. The decision is project-specific and ACG works with the architect to specify the right configuration.</p>"
            f"<p class='body-p'><strong>Hardware and anchorage in {city}.</strong> ACG specifies hardware appropriate for the {city} exposure: anodized aluminum or stainless 304 for inland sites, stainless 316 for direct coastal exposure. Anchorage details are engineered to the structural substrate (concrete, steel, wood-framed deck) with embed plates or post-installed anchors as required. ACG provides engineer-stamped shop drawings for the anchorage where the project requires.</p>"
        )

    # FAQ rendering
    faqs_html_parts = []
    for q, a in service["faqs"]:
        q_text = q.format(city=city)
        a_text = a.format(
            city=city,
            hvhz_storefront_answer=hvhz_storefront_answer(city, hvhz),
            hvhz_entrance_answer=hvhz_entrance_answer(city, hvhz),
            hvhz_impact_answer=hvhz_impact_answer(city, hvhz, county),
        )
        faqs_html_parts.append(f'''<div class="faq-item">
          <div class="faq-q">{q_text}</div>
          <div class="body-p">{a_text}</div>
        </div>''')
    faqs_html = "\n        ".join(faqs_html_parts)

    # Other services cards
    other_cards = []
    for svc in SERVICES:
        if svc["slug"] == service_slug: continue
        other_cards.append(f'''<a href="/{slug}/{svc['slug']}/" class="card">
          <div class="card-num">{city}</div>
          <h4>{svc['name']} &mdash; {city}</h4>
          <p>${svc['price_low']:,}-${svc['price_high']:,} per {svc['price_unit']}. ACG installer in {city}.</p>
        </a>''')
    other_services_cards = "\n        ".join(other_cards)

    # Projects
    projects_section = ""
    if projects:
        proj_cards = []
        for p in projects:
            display = p.replace("case-study-", "").replace("-", " ").title()
            href = f"/{p}.html"
            proj_cards.append(f'''<a href="{href}" class="card">
              <div class="card-num">{city} delivered</div>
              <h4>{display}</h4>
              <p>ACG commercial glazing project completed in {city}. Photographed in the portfolio.</p>
            </a>''')
        projects_section = f'''<section class="section" style="padding-top:0;">
    <div class="container">
      <div class="loc-label">{city} Projects</div>
      <h2 class="section-h">Delivered in <span class="accent">{city}.</span></h2>
      <div class="card-grid">
        {"".join(proj_cards)}
      </div>
    </div>
  </section>'''

    hvhz_short = "HVHZ" if hvhz else "FL#"
    hvhz_short_label = "Miami-Dade NOA" if hvhz else "FL Product Approval"

    h1_text = service["h1"]
    h1_short = service_name

    schema = build_service_schema(slug, city, county, lat, lon, service, hvhz)

    intent_keyword = service["intent_keyword"]
    service_slug_kw = service["slug"].replace("-", " ")

    return SERVICE_PAGE_TEMPLATE.format(
        slug=slug,
        city_slug=slug,
        city=city,
        city_lower=city.lower(),
        county=county,
        region=region,
        lat=lat,
        lon=lon,
        nav=NAV_HTML,
        footer=FOOTER_HTML("../../"),
        schema=schema,
        service_name=service_name,
        service_name_lower=service_name.lower(),
        service_slug=service["slug"],
        service_slug_kw=service_slug_kw,
        intent_keyword=intent_keyword,
        h1_text=h1_text,
        h1_short=h1_short,
        price_low=service["price_low"],
        price_high=service["price_high"],
        price_unit=service["price_unit"],
        lead_paragraph=lead,
        section1_h2=s1_h2,
        section1_body=s1_body,
        section2_h2=s2_h2,
        section2_body=s2_body,
        faqs_html=faqs_html,
        other_services_cards=other_services_cards,
        projects_section=projects_section,
        hvhz_short=hvhz_short,
        hvhz_short_label=hvhz_short_label,
    )


def main():
    n_hubs, n_services = 0, 0
    for city_data in CITIES:
        slug = city_data[0]
        # City hub
        city_dir = os.path.join(OUT_BASE, slug)
        os.makedirs(city_dir, exist_ok=True)
        with open(os.path.join(city_dir, "index.html"), "w") as f:
            f.write(render_city_hub(city_data))
        n_hubs += 1
        # 4 service pages
        for service in SERVICES:
            svc_dir = os.path.join(city_dir, service["slug"])
            os.makedirs(svc_dir, exist_ok=True)
            with open(os.path.join(svc_dir, "index.html"), "w") as f:
                f.write(render_service_page(city_data, service))
            n_services += 1
    print(f"Generated {n_hubs} city hubs + {n_services} service pages = {n_hubs + n_services} total pages")


if __name__ == "__main__":
    main()
