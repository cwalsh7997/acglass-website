# -*- coding: utf-8 -*-
import json

NAV = '''<nav class="nav scrolled"><div class="nav-inner">
  <a href="/" class="nav-logo"><img src="/images/acg-logo-nav@2x.png" alt="ACG — American Commercial Glass" width="338" height="72" fetchpriority="high" decoding="async" loading="eager" style="height:36px;width:auto;"></a>
  <div class="nav-links">
    <a href="/portfolio.html">Portfolio</a>
    <a href="/services.html">Services</a>
    <a href="/blog/">Blog</a>
    <a href="/about.html">About</a>
    <a href="/send-plans.html" class="nav-cta" style="background:#e11320;color:#fff;padding:10px 18px;border-radius:6px;font-weight:600;">Send Plans</a>
  </div>
</div></nav>'''

STYLE = '''  <style>
    body { background: #050a12; color: rgba(255,255,255,.85); margin: 0; }
    .author-hero { padding: 96px 24px 56px; background: linear-gradient(180deg, #0e284f 0%, #050a12 100%); color: #fff; }
    .author-hero-inner { max-width: 980px; margin: 0 auto; display: grid; grid-template-columns: 220px 1fr; gap: 48px; align-items: center; }
    @media (max-width: 720px) { .author-hero-inner { grid-template-columns: 1fr; gap: 24px; } }
    .author-photo { width: 220px; height: 220px; border-radius: 50%; object-fit: cover; border: 4px solid #e11320; display:block; }
    .author-eyebrow { font-family: 'JetBrains Mono', monospace; font-size: 11px; letter-spacing: .15em; text-transform: uppercase; color: #e11320; margin-bottom: 14px; }
    .author-hero h1 { font-size: clamp(34px, 5vw, 52px); line-height: 1.05; letter-spacing: -.02em; font-weight: 800; margin: 0 0 12px; }
    .author-role { font-size: 18px; color: rgba(255,255,255,.7); margin: 0 0 24px; }
    .author-meta { display: flex; flex-wrap: wrap; gap: 18px; font-size: 14px; color: rgba(255,255,255,.6); }
    .author-meta a { color: #fff; text-decoration: none; border-bottom: 1px solid rgba(225,19,32,.6); }
    .author-meta a:hover { color: #e11320; }
    .author-body { padding: 64px 24px 96px; }
    .author-body .container { max-width: 720px; margin: 0 auto; font-size: 17px; line-height: 1.7; }
    .author-body h2 { font-size: 22px; color: #fff; margin: 48px 0 16px; font-weight: 700; letter-spacing: -.01em; }
    .author-body h2:first-of-type { margin-top: 0; }
    .author-body p { margin: 0 0 18px; }
    .author-body a { color: #e11320; text-decoration: none; border-bottom: 1px solid rgba(225,19,32,.4); }
    .author-body a:hover { border-bottom-color: #e11320; }
    .author-body ul { padding-left: 22px; margin: 0 0 22px; }
    .author-body li { margin-bottom: 8px; }
    .author-fact-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 16px; margin: 32px 0; }
    .author-fact { background: rgba(225,19,32,.08); border-left: 2px solid #e11320; padding: 16px 18px; border-radius: 4px; }
    .author-fact-label { font-family: 'JetBrains Mono', monospace; font-size: 10px; letter-spacing: .12em; text-transform: uppercase; color: rgba(255,255,255,.55); margin-bottom: 4px; }
    .author-fact-value { font-size: 18px; font-weight: 700; color: #fff; line-height: 1.2; }
  </style>'''

FOOTER = open("/home/user/workspace/acglass-website/_footer_root_frag.html").read()

def page(d):
    person = json.dumps(d["person"], indent=2, ensure_ascii=False)
    crumb = {
      "@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[
        {"@type":"ListItem","position":1,"name":"Home","item":"https://acglass.com/"},
        {"@type":"ListItem","position":2,"name":"About","item":"https://acglass.com/about.html"},
        {"@type":"ListItem","position":3,"name":d["name"],"item":d["url"]}
      ]}
    crumbj=json.dumps(crumb,indent=2,ensure_ascii=False)
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<script async src="https://www.googletagmanager.com/gtag/js?id=G-M7BFQD2SPP"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag("js",new Date());gtag("config","G-M7BFQD2SPP");</script>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="theme-color" content="#0e284f">
  <title>{d["title"]}</title>
  <meta name="description" content="{d["desc"]}">
  <meta name="author" content="{d["name"]}">
  <link rel="canonical" href="{d["url"]}">
  <meta property="og:title" content="{d["ogtitle"]}">
  <meta property="og:description" content="{d["desc"]}">
  <meta property="og:type" content="profile">
  <meta property="og:url" content="{d["url"]}">
  <meta property="og:image" content="{d["img"]}">
  <meta property="og:site_name" content="American Commercial Glass">
  <meta property="profile:first_name" content="{d["first"]}">
  <meta property="profile:last_name" content="Walsh">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{d["ogtitle"]}">
  <meta name="twitter:description" content="{d["desc"]}">
  <meta name="twitter:image" content="{d["img"]}">
  <link rel="icon" type="image/png" href="/images/favicon-32.png">
  <link rel="preload" as="font" type="font/woff2" href="/fonts/inter-variable-latin.woff2" crossorigin>
  <link rel="stylesheet" href="/css/style.css">
  <script type="application/ld+json">
{person}
</script>
  <script type="application/ld+json">
{crumbj}
</script>
{STYLE}
</head>
<body>

{NAV}

<header class="author-hero">
  <div class="author-hero-inner">
    <picture>
      <source type="image/webp" srcset="{d["imgweb"]}">
      <img class="author-photo" src="{d["img"]}" width="220" height="220" alt="{d["name"]}, {d["roleshort"]} of American Commercial Glass" loading="eager" decoding="async">
    </picture>
    <div>
      <div class="author-eyebrow">Author Profile</div>
      <h1>{d["name"]}</h1>
      <p class="author-role">{d["role"]} &middot; American Commercial Glass, Inc.</p>
      <div class="author-meta">
        <span><a href="mailto:{d["email"]}">{d["email"]}</a></span>
        <span><a href="tel:+17724867711">(772) 486-7711</a></span>
        <span><a href="{d["linkedin"]}" rel="noopener" target="_blank">LinkedIn</a></span>
        <span><a href="/blog/">Read posts</a></span>
      </div>
    </div>
  </div>
</header>

<section class="author-body">
  <div class="container">
{d["body"]}
  </div>
</section>

{FOOTER}

</body>
</html>'''

# ---- Connor ----
connor_person = {
  "@context":"https://schema.org","@type":"Person","@id":"https://acglass.com/#connor-walsh",
  "name":"Connor Walsh","givenName":"Connor","familyName":"Walsh",
  "jobTitle":"President & Co-founder",
  "description":"Connor Walsh is the President and co-founder of American Commercial Glass (ACG), a Florida-licensed commercial glazing contractor. He is the qualifier for Florida Certified General Contractor license CGC #1531993, a former pilot, and previously founded and scaled a Florida glazing business from $400K to $10M in revenue.",
  "url":"https://acglass.com/authors/connor-walsh.html",
  "mainEntityOfPage":"https://acglass.com/authors/connor-walsh.html",
  "image":"https://acglass.com/images/team/connor-walsh-portrait.jpg",
  "email":"connor@acglass.com","telephone":"+1-772-486-7711",
  "worksFor":{"@id":"https://acglass.com/#organization"},
  "colleague":{"@id":"https://acglass.com/#rielly-walsh"},
  "knowsAbout":["Commercial Glazing","Florida Building Code","Hurricane Impact Glazing","AI in Construction","Construction Operations","HVHZ Compliance","Miami-Dade NOA","Curtain Wall","Storefront Systems","Division 08 Coordination"],
  "hasCredential":{"@type":"EducationalOccupationalCredential","credentialCategory":"license","name":"Florida Certified General Contractor (Qualifier)","identifier":"CGC #1531993","recognizedBy":{"@type":"GovernmentOrganization","name":"Florida Department of Business and Professional Regulation"}},
  "sameAs":["https://www.linkedin.com/in/connorwalsh1997"]
}
connor_body = '''    <h2>About</h2>
    <p>I'm Connor Walsh, President and co-founder of <a href="/">American Commercial Glass, Inc.</a> — a Florida-licensed commercial glazing contractor headquartered in West Palm Beach, with offices in Naples and Tampa and a Nashville, TN office opening Q3 2026. I'm the qualifier for our Florida Certified General Contractor license, CGC #1531993, and I run the company day-to-day with my co-founder and CEO, Rielly Walsh.</p>
    <p>Before ACG, I founded and scaled a Florida glazing business from $400K to $10M in revenue, and I'm a former pilot — a background that shaped how I think about checklists, preparation, and zero-defect execution. ACG is a commercial-only Division 08 subcontractor. We self-perform commercial storefront, curtain wall, impact-rated window, multi-slide door, and fire-rated glass installations. We're the authorized commercial installer for <a href="/eswindows-installer-florida.html">ESWindows</a> and Euro-Wall, and we work with PGT, Allegion, TGP, Slimpact, and Aldora.</p>

    <div class="author-fact-grid">
      <div class="author-fact"><div class="author-fact-label">License</div><div class="author-fact-value">FL CGC #1531993 (Qualifier)</div></div>
      <div class="author-fact"><div class="author-fact-label">Projects</div><div class="author-fact-value">350+</div></div>
      <div class="author-fact"><div class="author-fact-label">SF Installed</div><div class="author-fact-value">1M+</div></div>
      <div class="author-fact"><div class="author-fact-label">Bonded</div><div class="author-fact-value">$3M / $6M</div></div>
      <div class="author-fact"><div class="author-fact-label">Safety</div><div class="author-fact-value">0 OSHA recordables since 2021</div></div>
      <div class="author-fact"><div class="author-fact-label">Background</div><div class="author-fact-value">Former pilot</div></div>
    </div>

    <h2>What I write about</h2>
    <p>I write about commercial glazing as a working subcontractor — not as a pundit or a brochure. My focus areas:</p>
    <ul>
      <li><strong>AI-managed construction operations</strong> — we run custom AI agents (Sub.ai, jobcost.ai, and a CFO Agent) in production; what's working, what's hype, and what comes next</li>
      <li><strong>Florida Building Code &amp; HVHZ compliance</strong> — design pressure, Miami-Dade Notice of Acceptance, and Florida Product Approval</li>
      <li><strong>Hurricane impact glazing</strong> — impact-resistant systems, missile testing, and what owners actually need in a Florida envelope</li>
      <li><strong>Division 08 economics for GCs</strong> — bid clarity, scope coordination, and schedule predictability</li>
    </ul>

    <h2>Background &amp; credentials</h2>
    <p>I hold the company's FL CGC qualifier license (#1531993). ACG is $3M/$6M bonded through Arch Insurance and is WBE- and SBE-certified. We compete on speed, reliability, and AI-augmented operations — not price.</p>
    <p>If you're an editor or producer covering construction, AI in the trades, hurricane resilience, or Florida commercial real estate, reach me at <a href="mailto:connor@acglass.com">connor@acglass.com</a>. More on our standing is on the <a href="/press/">press page</a>.</p>

    <h2>Contact</h2>
    <p><strong>Direct:</strong> <a href="mailto:connor@acglass.com">connor@acglass.com</a><br>
    <strong>Phone:</strong> <a href="tel:+17724867711">(772) 486-7711</a><br>
    <strong>HQ:</strong> 700 S Rosemary Ave Suite 204, West Palm Beach, FL 33401<br>
    <strong>Other offices:</strong> Naples, FL &middot; Tampa, FL &middot; Nashville, TN (Q3 2026)</p>'''

connor = {
  "name":"Connor Walsh","first":"Connor","title":"Connor Walsh | President, ACG | Author Bio",
  "ogtitle":"Connor Walsh | President, American Commercial Glass",
  "desc":"Connor Walsh, President & co-founder of American Commercial Glass. FL CGC #1531993 qualifier, former pilot. Writes on glazing, Florida code, and AI in construction.",
  "role":"President &amp; Co-founder","roleshort":"President","email":"connor@acglass.com",
  "linkedin":"https://www.linkedin.com/in/connorwalsh1997",
  "img":"https://acglass.com/images/team/connor-walsh-portrait.jpg",
  "imgweb":"/images/team/connor-walsh-portrait.webp",
  "url":"https://acglass.com/authors/connor-walsh.html",
  "person":connor_person,"body":connor_body
}

# ---- Rielly ----
rielly_person = {
  "@context":"https://schema.org","@type":"Person","@id":"https://acglass.com/#rielly-walsh",
  "name":"Rielly Walsh","givenName":"Rielly","familyName":"Walsh",
  "jobTitle":"CEO & Co-founder",
  "description":"Rielly Walsh is the CEO and co-founder of American Commercial Glass (ACG), a Florida-licensed commercial glazing contractor. She holds a degree in Concrete Industry Management from Middle Tennessee State University and previously ran stoneworks operations at Aqualina.",
  "url":"https://acglass.com/authors/rielly-walsh.html",
  "mainEntityOfPage":"https://acglass.com/authors/rielly-walsh.html",
  "image":"https://acglass.com/images/team/rielly-walsh-portrait.jpg",
  "email":"rielly@acglass.com","telephone":"+1-772-486-7711",
  "worksFor":{"@id":"https://acglass.com/#organization"},
  "colleague":{"@id":"https://acglass.com/#connor-walsh"},
  "alumniOf":{"@type":"CollegeOrUniversity","name":"Middle Tennessee State University"},
  "knowsAbout":["Commercial Construction Management","Commercial Glazing","Project Delivery","Construction Operations","Concrete Industry Management","Field Coordination","Schedule Management"],
  "sameAs":["https://www.linkedin.com/company/american-commercial-glass-inc"]
}
rielly_body = '''    <h2>About</h2>
    <p>I'm Rielly Walsh, CEO and co-founder of <a href="/">American Commercial Glass, Inc.</a> I run ACG alongside my co-founder and President, Connor Walsh. ACG is a Florida-licensed, commercial-only Division 08 glazing contractor — storefront, curtain wall, impact glazing, multi-slide and folding doors, fire-rated glass, and aluminum entrances — headquartered in West Palm Beach, with offices in Naples and Tampa and a Nashville, TN office opening Q3 2026.</p>
    <p>I hold a degree in Concrete Industry Management from Middle Tennessee State University, and before ACG I ran stoneworks operations at Aqualina. That construction-operations background is what I bring to ACG: disciplined field coordination, schedule management, and the operational rigor that keeps 350+ projects and 1M+ square feet of installed work moving without OSHA recordables.</p>

    <div class="author-fact-grid">
      <div class="author-fact"><div class="author-fact-label">Role</div><div class="author-fact-value">CEO &amp; Co-founder</div></div>
      <div class="author-fact"><div class="author-fact-label">Education</div><div class="author-fact-value">MTSU — Concrete Industry Management</div></div>
      <div class="author-fact"><div class="author-fact-label">Projects</div><div class="author-fact-value">350+</div></div>
      <div class="author-fact"><div class="author-fact-label">SF Installed</div><div class="author-fact-value">1M+</div></div>
      <div class="author-fact"><div class="author-fact-label">Safety</div><div class="author-fact-value">0 OSHA recordables since 2021</div></div>
      <div class="author-fact"><div class="author-fact-label">Certifications</div><div class="author-fact-value">WBE &middot; SBE</div></div>
    </div>

    <h2>What I write about</h2>
    <p>I write about the operations side of commercial glazing — how a Division 08 scope actually gets built and turned over:</p>
    <ul>
      <li><strong>Project delivery &amp; field coordination</strong> — sequencing glazing scope to the GC's schedule and keeping it off the critical path</li>
      <li><strong>Construction operations</strong> — submittals, RFIs, and the discipline behind first-pass inspection clearance</li>
      <li><strong>ACG project case studies</strong> — what specific Florida builds taught us about execution at any scale</li>
    </ul>

    <h2>Contact</h2>
    <p><strong>Direct:</strong> <a href="mailto:rielly@acglass.com">rielly@acglass.com</a><br>
    <strong>Phone:</strong> <a href="tel:+17724867711">(772) 486-7711</a><br>
    <strong>HQ:</strong> 700 S Rosemary Ave Suite 204, West Palm Beach, FL 33401<br>
    <strong>Other offices:</strong> Naples, FL &middot; Tampa, FL &middot; Nashville, TN (Q3 2026)</p>'''

rielly = {
  "name":"Rielly Walsh","first":"Rielly","title":"Rielly Walsh | CEO, ACG | Author Bio",
  "ogtitle":"Rielly Walsh | CEO, American Commercial Glass",
  "desc":"Rielly Walsh, CEO & co-founder of American Commercial Glass. MTSU Concrete Industry Management. Writes on commercial construction operations and project delivery.",
  "role":"CEO &amp; Co-founder","roleshort":"CEO","email":"rielly@acglass.com",
  "linkedin":"https://www.linkedin.com/company/american-commercial-glass-inc",
  "img":"https://acglass.com/images/team/rielly-walsh-portrait.jpg",
  "imgweb":"/images/team/rielly-walsh-portrait.webp",
  "url":"https://acglass.com/authors/rielly-walsh.html",
  "person":rielly_person,"body":rielly_body
}

import os
os.makedirs("/home/user/workspace/acglass-website/authors",exist_ok=True)
open("/home/user/workspace/acglass-website/authors/connor-walsh.html","w").write(page(connor))
open("/home/user/workspace/acglass-website/authors/rielly-walsh.html","w").write(page(rielly))
print("authors written")
