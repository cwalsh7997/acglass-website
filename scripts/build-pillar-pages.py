#!/usr/bin/env python3
"""Build the 5 phantom pillar pages flagged in the audit.

Each is linked 24-25x sitewide. They must exist with proper content + schema.
"""
import json, os
from pathlib import Path

ROOT = Path('/home/user/workspace/acglass-website')

# Brand tokens copied from existing pages (navy/red/paper, Inter/Fraunces/JetBrains)
HEAD_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title}</title>
  <meta name="description" content="{description}">
  <meta name="keywords" content="{keywords}">
  <link rel="canonical" href="https://acglass.com/{slug}.html">
  <meta property="og:title" content="{og_title}">
  <meta property="og:description" content="{og_description}">
  <meta property="og:type" content="website">
  <meta property="og:url" content="https://acglass.com/{slug}.html">
  <meta property="og:image" content="{og_image}">
  <link rel="stylesheet" href="css/style.css">
  <link rel="icon" href="images/acg-favicon.svg" type="image/svg+xml">

{schema_blocks}

  <style>
    .hero {{ padding: 100px 0 40px; max-width: 1080px; margin: 0 auto; padding-left: 28px; padding-right: 28px; }}
    .hero .eyebrow {{ font-family: 'JetBrains Mono', monospace; font-size: 0.72rem; letter-spacing: 0.18em; text-transform: uppercase; color: var(--accent, #E11320); margin-bottom: 14px; font-weight: 700; }}
    .hero h1 {{ font-size: clamp(2rem, 4.5vw, 3.6rem); line-height: 1.04; letter-spacing: -0.02em; margin: 0 0 22px; }}
    .hero .lead {{ font-size: 1.06rem; line-height: 1.65; color: rgba(255,255,255,0.84); max-width: 780px; }}
    .byline {{ font-family: 'JetBrains Mono', monospace; font-size: 0.74rem; letter-spacing: 0.14em; text-transform: uppercase; color: rgba(255,255,255,0.55); margin-top: 18px; }}
    #answer-box {{ background: rgba(225,19,32,0.06); border-left: 3px solid var(--accent, #E11320); padding: 22px 26px; max-width: 1024px; margin: 40px auto; border-radius: 6px; }}
    #answer-box h2 {{ font-family: 'JetBrains Mono', monospace; font-size: 0.72rem; letter-spacing: 0.16em; text-transform: uppercase; color: var(--accent); margin: 0 0 12px; font-weight: 700; }}
    #answer-box p {{ font-size: 1.05rem; line-height: 1.6; color: rgba(255,255,255,0.92); margin: 0; }}
    main.content {{ max-width: 1024px; margin: 60px auto 100px; padding: 0 28px; }}
    main.content h2 {{ font-size: 1.7rem; letter-spacing: -0.01em; margin: 50px 0 18px; }}
    main.content h3 {{ font-size: 1.2rem; margin: 32px 0 12px; color: rgba(255,255,255,0.95); }}
    main.content p {{ color: rgba(255,255,255,0.85); line-height: 1.75; font-size: 1.02rem; margin-bottom: 18px; }}
    main.content ul {{ color: rgba(255,255,255,0.85); line-height: 1.85; padding-left: 24px; }}
    main.content table {{ width: 100%; border-collapse: collapse; margin: 22px 0 32px; font-size: 0.94rem; }}
    main.content th {{ text-align: left; padding: 14px 14px; border-bottom: 1px solid rgba(255,255,255,0.18); font-family: 'JetBrains Mono', monospace; font-size: 0.72rem; letter-spacing: 0.12em; text-transform: uppercase; color: var(--accent); font-weight: 700; }}
    main.content td {{ padding: 14px 14px; border-bottom: 1px solid rgba(255,255,255,0.06); color: rgba(255,255,255,0.88); vertical-align: top; }}
    main.content td:first-child {{ color: #fff; font-weight: 600; }}
    .pill-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(160px, 1fr)); gap: 10px; margin: 24px 0; }}
    .pill-grid a {{ padding: 10px 14px; background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.1); border-radius: 6px; color: rgba(255,255,255,0.85); text-decoration: none; font-size: 13px; text-align: center; }}
    .pill-grid a:hover {{ border-color: var(--accent); color: #fff; }}
    .stat-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 18px; margin: 30px 0; }}
    .stat-card {{ padding: 22px; background: rgba(0,0,0,0.25); border: 1px solid rgba(225,19,32,0.2); border-radius: 10px; }}
    .stat-card .label {{ font-family: 'JetBrains Mono', monospace; font-size: 10px; text-transform: uppercase; letter-spacing: 0.14em; color: var(--accent); margin-bottom: 8px; }}
    .stat-card .value {{ font-size: 22px; font-weight: 800; color: #fff; line-height: 1.15; }}
    .stat-card .note {{ font-size: 12px; color: rgba(255,255,255,0.6); margin-top: 6px; }}
    .cta-box {{ background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.1); padding: 28px; margin: 50px 0; border-radius: 8px; }}
    .cta-box a {{ color: var(--accent); font-weight: 700; text-decoration: none; }}
  </style>
</head>
<body>

  <header class="site-nav">
    <div style="max-width:1200px;margin:0 auto;padding:18px 28px;display:flex;justify-content:space-between;align-items:center;">
      <a href="/" style="color:#fff;font-weight:700;text-decoration:none;font-size:1.05rem;">ACG</a>
      <nav style="display:flex;gap:24px;font-size:0.92rem;">
        <a href="/services.html" style="color:rgba(255,255,255,0.85);text-decoration:none;">Services</a>
        <a href="/portfolio.html" style="color:rgba(255,255,255,0.85);text-decoration:none;">Portfolio</a>
        <a href="/ask.html" style="color:rgba(255,255,255,0.85);text-decoration:none;">Resources</a>
        <a href="/contact.html" style="color:rgba(255,255,255,0.85);text-decoration:none;">Contact</a>
      </nav>
    </div>
  </header>
"""

FOOTER = """
  <footer style="background:#050a12;padding:40px 28px;text-align:center;border-top:1px solid rgba(255,255,255,0.08);">
    <div style="max-width:1200px;margin:0 auto;color:rgba(255,255,255,0.6);font-size:0.9rem;">
      <p>&copy; 2026 American Commercial Glass &middot; FL CGC #1531993 &middot; West Palm Beach &middot; Naples &middot; Tampa &middot; Nashville (2026)</p>
      <p style="margin-top:12px;"><a href="/services.html" style="color:rgba(255,255,255,0.7);margin:0 12px;">Services</a> <a href="/ask.html" style="color:rgba(255,255,255,0.7);margin:0 12px;">Direct Answers</a> <a href="/glossary.html" style="color:rgba(255,255,255,0.7);margin:0 12px;">Glossary</a> <a href="/contact.html" style="color:rgba(255,255,255,0.7);margin:0 12px;">Contact</a></p>
    </div>
  </footer>
</body>
</html>
"""

ACG_ORG = {
    "@type": ["GeneralContractor", "LocalBusiness"],
    "@id": "https://acglass.com/#organization",
    "name": "American Commercial Glass, Inc.",
    "alternateName": "ACG",
    "url": "https://acglass.com",
    "telephone": "+1-772-486-7711",
    "hasCredential": {"@type": "EducationalOccupationalCredential", "credentialCategory": "license", "name": "Florida CGC #1531993"}
}

CONNOR = {
    "@type": "Person",
    "name": "Connor Walsh",
    "jobTitle": "President, American Commercial Glass",
    "url": "https://acglass.com/author/connor-walsh.html",
    "hasCredential": {"@type": "EducationalOccupationalCredential", "credentialCategory": "license", "name": "Florida CGC #1531993"}
}

def trust_signals_block():
    return """
    <div class="stat-grid">
      <div class="stat-card"><div class="label">License</div><div class="value">FL CGC<br>#1531993</div><div class="note">Certified General Contractor</div></div>
      <div class="stat-card"><div class="label">Projects</div><div class="value">350+<br>Installed</div><div class="note">Commercial, 2021–2026</div></div>
      <div class="stat-card"><div class="label">Volume</div><div class="value">1M+ SF<br>Installed</div><div class="note">FL &amp; Southeast</div></div>
      <div class="stat-card"><div class="label">Bonding</div><div class="value">$3M / $6M<br>Aggregate</div><div class="note">Single / aggregate capacity</div></div>
      <div class="stat-card"><div class="label">Safety</div><div class="value">Zero<br>OSHA</div><div class="note">5+ year clean record</div></div>
      <div class="stat-card"><div class="label">Coverage</div><div class="value">WPB · Naples<br>· Tampa</div><div class="note">Nashville 2026</div></div>
    </div>"""

# ────────── Page 1: /curtainwall-installation.html ──────────
P1 = dict(
    slug='curtainwall-installation',
    title='Commercial Curtainwall Installation — Florida CGC | ACG',
    description="Commercial curtainwall installer — stick-built, unitized, structural silicone glazing (SSG), pressure-cap. 350+ projects, FL CGC #1531993. ESWindows ES8000T, Kawneer 1600UT, Vista pressure-cap. HVHZ NOA assemblies.",
    keywords='commercial curtainwall installer, curtainwall contractor Florida, stick-built curtainwall, unitized curtainwall, structural silicone glazing, SSG, pressure-cap curtainwall, ES8000T curtainwall',
    og_title='Commercial Curtainwall Installation',
    og_description='Florida-licensed commercial curtainwall installer. 350+ projects. Stick-built, unitized, SSG. ES8000T, Kawneer 1600UT.',
    og_image='https://acglass.com/images/projects/ocean-prime-ft-lauderdale/ocean-prime-ftl-twilight-exterior.jpg',
    h1='Commercial curtainwall installation',
    eyebrow='Curtainwall Pillar &middot; Florida CGC',
    lead='Stick-built, unitized, structural silicone, pressure-cap — curtainwall is the most engineered wall system on a commercial project. We install all four configurations across Florida and the Southeast on AIA-format contracts, with HVHZ NOA assemblies, signed/sealed engineering, and AAMA 502 field testing as standard scope.',
    answer='ACG is a Florida-licensed commercial curtainwall installer (FL CGC #1531993) with 350+ projects across stick-built, unitized, structural silicone glazing (SSG), and pressure-cap configurations. We install ESWindows ES8000T, Kawneer 1600UT, Vista pressure-cap, and equivalent commercial systems. HVHZ NOA assemblies, AAMA 502 field testing, and signed/sealed engineering are standard scope.',
    children=[
        ('/storefront-vs-curtainwall.html', 'Storefront vs curtainwall — when to use'),
        ('/curtainwall-vs-window-wall.html', 'Curtainwall vs window wall'),
        ('/commercial-glass-cost-data.html', 'Curtainwall cost per SF — 2026 data'),
        ('/florida-hvhz-glazing-contractor.html', 'Florida HVHZ glazing'),
        ('/miami-hvhz-glazing-contractor.html', 'Miami HVHZ glazing'),
        ('/eswindows-installer-florida.html', 'ESWindows commercial installer'),
        ('/euro-wall.html', 'Euro-Wall systems'),
        ('/approvals/', 'FPA &amp; NOA index'),
        ('/architect-specs/', 'CSI Division 08 specs'),
    ],
    sections=[
        ('What curtainwall is', """<p>Curtainwall is a non-load-bearing exterior wall system that hangs off the building structure rather than sitting on the floor. It attaches at slab edges and transfers wind load horizontally to the structure. Curtainwall framing is deeper than storefront (typically 4½"–7½") to span longer distances and resist higher design pressures.</p>
<p>Three families of curtainwall, by fabrication method:</p>
<ul>
<li><strong>Stick-built</strong> — assembled member-by-member on site. Most common in Florida commercial work. Lower factory cost, higher field labor.</li>
<li><strong>Unitized</strong> — pre-glazed factory panels shipped to site and hung on the structure. Used on high-rise where field labor cost and schedule compression matter.</li>
<li><strong>Ladder / pre-assembled</strong> — intermediate approach. Vertical mullions pre-assembled in shop, horizontals and glass installed in field.</li>
</ul>
<p>Three families of curtainwall, by glazing method:</p>
<ul>
<li><strong>Captured (pressure-cap)</strong> — glass held by aluminum cap and gasket. Most economical. Visible cap line on exterior.</li>
<li><strong>Structural silicone glazing (SSG)</strong> — glass bonded to frame with structural silicone. Flush exterior — no visible mullion cap. Premium aesthetic.</li>
<li><strong>Point-supported / spider</strong> — glass held by stainless-steel fittings without conventional framing. Used in lobbies, atriums, signature entrances.</li>
</ul>"""),
        ('Systems we install', """<p>ACG installs the full commercial curtainwall line from our authorized manufacturer partners:</p>
<table>
<thead><tr><th>System</th><th>Manufacturer</th><th>Family</th><th>Max DP</th><th>Common use</th></tr></thead>
<tbody>
<tr><td>ES8000T</td><td>ESWindows (Tecnoglass)</td><td>Thermal stick-built / SSG</td><td>+90 / &minus;120 PSF</td><td>Energy-targeted office, mid-rise</td></tr>
<tr><td>ES7000 (LMI)</td><td>ESWindows</td><td>Pre-glazed window wall / CW hybrid</td><td>+125 / &minus;150 PSF</td><td>High-rise envelope</td></tr>
<tr><td>Euro-Wall Pressure-Cap</td><td>Euro-Wall</td><td>Stick-built pressure-cap</td><td>Project-engineered</td><td>Hospitality, clubhouse, luxury</td></tr>
<tr><td>Kawneer 1600UT</td><td>Kawneer</td><td>Unitized thermal</td><td>Per NOA</td><td>High-rise tower, Class A office</td></tr>
</tbody>
</table>
<p style="font-size:0.85rem;color:rgba(255,255,255,0.6);font-style:italic;">Design pressures are tested-assembly maximums. Actual project DPs depend on glass make-up, anchor spacing, and assembly configuration. Send drawings for project-specific verification.</p>"""),
        ('How we work', """<h3>1. Drawing review &amp; system selection</h3>
<p>Send architectural drawings to <a href="/bid.html" style="color:var(--accent);">bid@acglass.com</a>. We review for system applicability, identify NOA-listed assemblies that match the wind load and aesthetic intent, and flag spec conflicts before submittal.</p>
<h3>2. NOA &amp; FPA documentation</h3>
<p>For HVHZ projects we deliver Miami-Dade NOA cover sheets, installation instructions, configuration limits, and a glazing schedule keyed to the architect&rsquo;s elevations.</p>
<h3>3. Signed/sealed engineering</h3>
<p>Florida-licensed engineer reviews anchor calculations and confirms the assembly falls inside the NOA limits for the project wind zone.</p>
<h3>4. Fabrication &amp; field installation</h3>
<p>Crews from our WPB, Naples, and Tampa offices, supported by manufacturer-trained installers. Unitized projects coordinate with the factory ship schedule.</p>
<h3>5. AAMA 502 testing &amp; close-out</h3>
<p>Field water testing scheduled per AHJ requirement and witnessed by ACG and the GC. Warranty package, NOA close-out, and maintenance schedule delivered.</p>"""),
        ('Frequently asked questions', """<h3>What&rsquo;s the difference between stick-built and unitized curtainwall?</h3>
<p>Stick-built is assembled member-by-member on site; unitized is pre-glazed at the factory and hung on the structure as panels. Unitized has higher factory cost but faster field installation and tighter QC — typically used on high-rise above ~8 stories.</p>
<h3>How much does commercial curtainwall cost in Florida in 2026?</h3>
<p>Installed cost runs $95&ndash;$180 per square foot. HVHZ NOA assemblies add ~20%. <a href="/commercial-glass-cost-data.html" style="color:var(--accent);">See full pricing data.</a></p>
<h3>When is curtainwall required over storefront?</h3>
<p>When the assembly spans floor-to-floor or multi-story, exceeds ~10 ft height, requires deflection &le; L/240, or specifies structural silicone glazing for a flush aesthetic. <a href="/storefront-vs-curtainwall.html" style="color:var(--accent);">See the full decision framework.</a></p>
<h3>Is SSG (structural silicone glazing) more expensive?</h3>
<p>SSG runs 8&ndash;15% more than pressure-cap curtainwall. The premium buys a flush exterior, deeper thermal break, and tighter water performance.</p>"""),
    ],
)

# ────────── Page 2: /commercial-storefront-systems.html ──────────
P2 = dict(
    slug='commercial-storefront-systems',
    title='Commercial Storefront Systems Installation | ACG',
    description='Commercial storefront installation — impact-rated, non-impact, butt-glazed, all-glass entrances. Florida CGC #1531993. Authorized Euro-Wall DirectSet, ESWindows, Kawneer 451T-IR. 350+ commercial projects.',
    keywords='commercial storefront installer, storefront contractor Florida, impact-rated storefront, butt-glazed storefront, all-glass entrance, Kawneer 451T, Euro-Wall DirectSet',
    og_title='Commercial Storefront Systems',
    og_description='Florida commercial storefront installer. 350+ projects. Impact-rated, HVHZ NOA, butt-glazed, all-glass entries.',
    og_image='https://acglass.com/images/projects/atlantic-fields/atlantic-fields-golden-hour.jpg',
    h1='Commercial storefront systems',
    eyebrow='Storefront Pillar &middot; Florida CGC',
    lead='Storefront is the workhorse of commercial glazing — center-set aluminum framing for retail, restaurant, lobby, and ground-floor commercial. We install impact-rated and non-impact configurations across Florida, with HVHZ NOA assemblies in Miami-Dade and Broward, and butt-glazed / all-glass entry variants for signature applications.',
    answer='ACG is a Florida-licensed commercial storefront installer (FL CGC #1531993) installing center-set aluminum storefront systems for retail, restaurant, lobby, and commercial ground-floor projects. Impact-rated and non-impact configurations. Authorized installer for Euro-Wall DirectSet, ESWindows ES-50/ES-80, and Kawneer 451T-IR. HVHZ Miami-Dade NOA assemblies for South Florida.',
    children=[
        ('/storefront-vs-curtainwall.html', 'Storefront vs curtainwall'),
        ('/curtainwall-installation.html', 'Curtainwall installation'),
        ('/window-wall-systems.html', 'Window wall systems'),
        ('/impact-windows-doors-florida.html', 'Impact-rated assemblies'),
        ('/commercial-glass-cost-data.html', 'Storefront cost per SF'),
        ('/euro-wall.html', 'Euro-Wall DirectSet'),
        ('/eswindows-installer-florida.html', 'ESWindows commercial'),
        ('/approvals/', 'NOA &amp; FPA index'),
    ],
    sections=[
        ('What commercial storefront is', """<p>Storefront is a center-set aluminum glazing system &mdash; typically 1¾&Prime; or 2&Prime; deep &mdash; that sits on the floor and transfers wind load downward through its sill. Glass is held by gaskets and snap-on stops. Height limit is approximately 10 ft single-story; above that, you generally move to curtainwall.</p>
<p>Common applications:</p>
<ul>
<li>Retail strip centers and shopping plazas</li>
<li>Restaurant fronts and ground-floor commercial</li>
<li>Bank branches and credit unions</li>
<li>Office tower lobbies and vestibules</li>
<li>Small office buildings and medical offices</li>
<li>Auto dealership showrooms</li>
</ul>
<p>Variants:</p>
<ul>
<li><strong>Centerline (standard)</strong> &mdash; glass set in the center of the framing. The most economical configuration.</li>
<li><strong>Front-set / back-set</strong> &mdash; glass offset to the exterior or interior face for aesthetic reasons.</li>
<li><strong>Butt-glazed</strong> &mdash; vertical mullions replaced with structural silicone joints between lites. Frameless look.</li>
<li><strong>All-glass entrance</strong> &mdash; tempered glass doors with full-height stiles. Premium retail and hospitality.</li>
<li><strong>Impact-rated</strong> &mdash; NOA-listed assembly with laminated glass and reinforced framing.</li>
</ul>"""),
        ('Systems we install', """<table>
<thead><tr><th>System</th><th>Manufacturer</th><th>Configuration</th><th>Max DP</th><th>Use</th></tr></thead>
<tbody>
<tr><td>Euro-Wall DirectSet</td><td>Euro-Wall</td><td>Impact-rated storefront</td><td>+90 / &minus;100 PSF</td><td>Restaurant, retail HVHZ</td></tr>
<tr><td>Kawneer 451T-IR</td><td>Kawneer</td><td>Thermal impact</td><td>Per NOA</td><td>Mid-rise commercial</td></tr>
<tr><td>ESWindows ES-50</td><td>ESWindows</td><td>Standard storefront</td><td>Project-engineered</td><td>Light commercial</td></tr>
<tr><td>ESWindows ES-80</td><td>ESWindows</td><td>Heavy-commercial storefront</td><td>Per NOA</td><td>Hospitality, retail</td></tr>
</tbody>
</table>
<p style="font-size:0.85rem;color:rgba(255,255,255,0.6);font-style:italic;">DPs are tested maximums. Project-specific verification required.</p>"""),
        ('Storefront vs curtainwall — when storefront is correct', """<p>Use storefront when:</p>
<ul>
<li>Assembly is one story and &le; 10 ft height</li>
<li>Wind load is moderate (deflection L/175 achievable)</li>
<li>Budget matters &mdash; storefront installed cost is $55&ndash;$110/SF vs curtainwall $95&ndash;$180/SF</li>
<li>Standard centerline aesthetic is acceptable</li>
</ul>
<p>Use curtainwall when assembly spans floor-to-floor, exceeds 10 ft, or requires flush SSG aesthetic. <a href="/storefront-vs-curtainwall.html" style="color:var(--accent);">Full decision framework.</a></p>"""),
        ('Frequently asked questions', """<h3>How much does commercial storefront cost in Florida in 2026?</h3>
<p>Non-impact: $55&ndash;$80/SF installed. Impact-rated: $80&ndash;$110/SF. HVHZ NOA adds ~20%.</p>
<h3>What&rsquo;s the lead time for commercial storefront in 2026?</h3>
<p>6&ndash;10 weeks material lead time. Installation 2&ndash;4 weeks for a typical 5,000&ndash;8,000 SF assembly.</p>
<h3>Can storefront be impact-rated for HVHZ?</h3>
<p>Yes. ACG installs Miami-Dade NOA-listed impact storefront from Euro-Wall, ESWindows, and Kawneer.</p>
<h3>What&rsquo;s the difference between butt-glazed and standard storefront?</h3>
<p>Butt-glazed replaces vertical mullions with structural silicone joints between lites &mdash; the look is frameless. Cost premium 15&ndash;25% over standard centerline.</p>"""),
    ],
)

# ────────── Page 3: /window-wall-systems.html ──────────
P3 = dict(
    slug='window-wall-systems',
    title='Commercial Window Wall Systems Installation | ACG',
    description='Window wall installer — slab-to-slab commercial glazing for multifamily, hotel, condo. Florida CGC #1531993. ESWindows ES7000, YKK YHC 300, HVHZ NOA assemblies. 350+ projects.',
    keywords='commercial window wall installer, slab-to-slab glazing, multifamily window wall, condo window wall, ESWindows ES7000, YKK YHC 300, hotel envelope',
    og_title='Commercial Window Wall Systems',
    og_description='Florida window wall installer for multifamily, condo, hotel. Slab-to-slab HVHZ NOA assemblies.',
    og_image='https://acglass.com/images/projects/wild-blue-clubhouse/wild-blue-clubhouse-exterior.jpg',
    h1='Commercial window wall systems',
    eyebrow='Window Wall Pillar &middot; Florida CGC',
    lead='Window wall is slab-to-slab glazing &mdash; the cost-efficient middle path between storefront and curtainwall. Common in multifamily, condo, and mid-rise hospitality. We install ESWindows ES7000, YKK YHC 300, and equivalent commercial systems with HVHZ NOA configurations across Florida.',
    answer='ACG is a Florida-licensed commercial window wall installer (FL CGC #1531993). We install slab-to-slab window wall systems for multifamily, condo, mid-rise hotel, and mixed-use projects. Authorized installer for ESWindows ES7000 / ES7100, YKK YHC 300, and equivalent commercial lines. HVHZ Miami-Dade NOA assemblies available.',
    children=[
        ('/curtainwall-vs-window-wall.html', 'Curtainwall vs window wall'),
        ('/storefront-vs-curtainwall.html', 'Storefront vs curtainwall'),
        ('/curtainwall-installation.html', 'Curtainwall installation'),
        ('/commercial-storefront-systems.html', 'Storefront systems'),
        ('/commercial-glass-cost-data.html', 'Window wall cost per SF'),
        ('/eswindows-installer-florida.html', 'ESWindows ES7000'),
        ('/florida-hvhz-glazing-contractor.html', 'Florida HVHZ'),
        ('/miami-hvhz-glazing-contractor.html', 'Miami HVHZ'),
    ],
    sections=[
        ('What window wall is', """<p>Window wall is a non-load-bearing exterior glazing system installed <strong>between slabs</strong> &mdash; the bottom of each story&rsquo;s window wall rests on (or anchors to) the slab below, and the top tucks under the slab above. Window wall is stacked floor by floor.</p>
<p>This is different from curtainwall, which hangs <strong>outside</strong> the slab edges as one continuous skin. Window wall is more economical, sequences naturally with concrete construction, but typically caps out at ~10 stories.</p>
<p>Common applications:</p>
<ul>
<li>Multifamily &mdash; podium and stick-built up to 8 stories</li>
<li>Mid-rise condo</li>
<li>Select-service hotels (4&ndash;10 stories)</li>
<li>Mixed-use ground-floor retail + upper-floor residential</li>
<li>Senior living and assisted-living</li>
</ul>"""),
        ('Systems we install', """<table>
<thead><tr><th>System</th><th>Manufacturer</th><th>Design Pressure</th><th>NOA</th><th>Use</th></tr></thead>
<tbody>
<tr><td>ES7000 (LMI)</td><td>ESWindows</td><td>+125 / &minus;150 PSF</td><td>23-0724.09</td><td>HVHZ multifamily, condo</td></tr>
<tr><td>ES7100 (SMI)</td><td>ESWindows</td><td>+125 / &minus;150 PSF</td><td>23-0724.10</td><td>Non-HVHZ multifamily</td></tr>
<tr><td>YKK YHC 300</td><td>YKK AP</td><td>Per NOA</td><td>Multiple</td><td>Mid-rise commercial</td></tr>
</tbody>
</table>
<p style="font-size:0.85rem;color:rgba(255,255,255,0.6);font-style:italic;">Source: ESWindows technical datasheets and Miami-Dade Product Control NOA database.</p>"""),
        ('Window wall vs curtainwall — when window wall wins', """<p>Use window wall when:</p>
<ul>
<li>Multifamily, condo, or mid-rise hotel up to ~10 stories</li>
<li>Cost matters &mdash; window wall runs $70&ndash;$110/SF vs curtainwall $95&ndash;$180/SF</li>
<li>Construction sequence is slab-then-glaze-then-slab</li>
<li>Visible horizontal slab bands are acceptable aesthetically</li>
</ul>
<p>Use curtainwall when assembly is Class A office, hotel tower, or requires flush SSG aesthetic. <a href="/curtainwall-vs-window-wall.html" style="color:var(--accent);">Full decision framework.</a></p>"""),
        ('Frequently asked questions', """<h3>How much does window wall cost in Florida in 2026?</h3>
<p>$70&ndash;$110/SF installed. HVHZ NOA adds ~20%. 30&ndash;40% cheaper than curtainwall on equivalent assemblies.</p>
<h3>Can window wall be impact-rated for HVHZ?</h3>
<p>Yes. ESWindows ES7000 holds a Miami-Dade NOA (23-0724.09) with design pressures to +125/&minus;150 PSF.</p>
<h3>What&rsquo;s the height limit on window wall?</h3>
<p>~10 stories is the practical limit. Above that, wind load and anchor capacity push you to curtainwall.</p>
<h3>How is window wall waterproofed?</h3>
<p>Sloped slab edge with back-dam, self-adhering flashing turn-down, and a sealed perimeter at head and jamb. AAMA 502 field water testing typically required on HVHZ.</p>"""),
    ],
)

# ────────── Page 4: /impact-windows-doors-florida.html ──────────
P4 = dict(
    slug='impact-windows-doors-florida',
    title='Commercial Impact Windows & Doors — Florida HVHZ | ACG',
    description='Commercial impact-rated window and door installer for Florida HVHZ projects. Miami-Dade NOA assemblies, Florida Product Approvals, AAMA 502 field testing. FL CGC #1531993. 350+ projects.',
    keywords='commercial impact windows Florida, commercial impact doors Florida, HVHZ impact glazing, Miami-Dade NOA, Florida Product Approval, large missile impact, hurricane impact commercial',
    og_title='Commercial Impact Windows & Doors — Florida HVHZ',
    og_description='Florida commercial impact-rated glazing. Miami-Dade NOA assemblies. 350+ commercial projects.',
    og_image='https://acglass.com/images/projects/ocean-prime-ft-lauderdale/ocean-prime-ftl-twilight-exterior.jpg',
    h1='Commercial impact windows &amp; doors &mdash; Florida',
    eyebrow='Hurricane Impact &middot; Florida CGC',
    lead='Florida&rsquo;s commercial market runs on impact-rated assemblies &mdash; HVHZ in Miami-Dade and Broward, Florida Product Approval (FPA) statewide. We install impact-rated commercial storefront, curtainwall, window wall, sliding doors, and entrance assemblies from Miami-Dade NOA-listed manufacturers across the state.',
    answer='ACG is a Florida-licensed commercial installer (FL CGC #1531993) of impact-rated windows, doors, storefronts, curtainwalls, and window walls. We install Miami-Dade NOA assemblies in HVHZ zones (Miami-Dade, Broward) and Florida Product Approval (FPA) assemblies statewide. Authorized installer for ESWindows, Euro-Wall, PGT, Allegion, and TGP commercial impact-rated systems.',
    children=[
        ('/florida-hvhz-glazing-contractor.html', 'Florida HVHZ glazing contractor'),
        ('/miami-hvhz-glazing-contractor.html', 'Miami HVHZ glazing'),
        ('/approvals/', 'FPA &amp; NOA index'),
        ('/commercial-storefront-systems.html', 'Impact storefront'),
        ('/curtainwall-installation.html', 'Impact curtainwall'),
        ('/window-wall-systems.html', 'Impact window wall'),
        ('/eswindows-installer-florida.html', 'ESWindows impact'),
        ('/euro-wall.html', 'Euro-Wall impact systems'),
        ('/commercial-glass-cost-data.html', 'Impact assembly cost'),
    ],
    sections=[
        ('Florida&rsquo;s two impact-code paths', """<p>Florida uses two distinct compliance paths for impact-rated assemblies:</p>
<h3>HVHZ (Miami-Dade &amp; Broward)</h3>
<p>The High-Velocity Hurricane Zone &mdash; the highest level of code in the United States. Every assembly must hold a Miami-Dade Notice of Acceptance (NOA), proving it passed Large Missile Impact, cyclic-pressure testing, and water resistance per ASTM E331/E547. NOAs are assembly-specific &mdash; frame + glass + anchorage must be tested together.</p>
<h3>Florida Product Approval (FPA) &mdash; rest of state</h3>
<p>Outside HVHZ, Florida uses statewide product approval. The testing protocol is similar but less restrictive. FPA-listed assemblies are searchable in the Florida Building Commission database. Wind zones range from 130&ndash;180 mph design wind speed depending on AHJ.</p>
<h3>When impact rating is required</h3>
<p>Required by code for any opening in the building envelope within HVHZ, and in wind-borne debris regions across the rest of FL (typically within 1 mile of coast or specific permit areas). Most commercial work in coastal Florida specifies impact-rated assemblies whether code-required or not.</p>"""),
        ('Manufacturer authority', """<table>
<thead><tr><th>Manufacturer</th><th>Commercial line</th><th>Specialization</th></tr></thead>
<tbody>
<tr><td>ESWindows / Tecnoglass</td><td>ES7000, ES8000T, ES-6500, ES-9000</td><td>Curtainwall, window wall, sliding doors, entries</td></tr>
<tr><td>Euro-Wall</td><td>Vista Multi Slide, Vista Fold, Vista Pivot, DirectSet</td><td>Folding, sliding, pivot doors, storefront</td></tr>
<tr><td>PGT</td><td>WinGuard Aluminum</td><td>Light commercial, mixed-use, multifamily</td></tr>
<tr><td>Allegion</td><td>Commercial impact hardware</td><td>Egress, panic, locking</td></tr>
<tr><td>TGP</td><td>Fire-rated HVHZ assemblies</td><td>UL-listed HVHZ + fire-rated combo</td></tr>
</tbody>
</table>"""),
        ('Frequently asked questions', """<h3>What&rsquo;s the difference between impact glass and laminated glass?</h3>
<p>All impact glass is laminated, but not all laminated glass is impact-rated. Impact-rated glass uses a thicker interlayer (typically 0.090&Prime; PVB or 0.060&Prime; SentryGlas) and must pass Large Missile Impact testing in a specific frame.</p>
<h3>How much does commercial impact glazing cost vs non-impact?</h3>
<p>Impact-rated commercial assemblies cost 20&ndash;30% more than non-impact equivalents. HVHZ adds another ~20% on top of that. <a href="/commercial-glass-cost-data.html" style="color:var(--accent);">Full pricing data.</a></p>
<h3>What&rsquo;s the difference between Large Missile Impact (LMI) and Small Missile Impact (SMI)?</h3>
<p>LMI = 9-pound 2x4 fired at 50 ft/sec; required below 30 ft elevation. SMI = 30 steel balls fired at 130 ft/sec; required above 30 ft. NOAs are typically listed for one or the other.</p>
<h3>Do I need impact glazing for a commercial project in Florida?</h3>
<p>Yes if you are inside HVHZ or in a wind-borne debris region. The AHJ determines applicability based on parcel location and wind zone. Send drawings and we&rsquo;ll confirm code path.</p>"""),
    ],
)

# ────────── Page 5: /fire-rated-glass-systems.html ──────────
P5 = dict(
    slug='fire-rated-glass-systems',
    title='Fire-Rated Glass Systems Installation — TGP Authorized | ACG',
    description='Fire-rated glass installer — UL-listed assemblies from 20-minute to 120-minute ratings, including HVHZ + fire-rated combo. Florida CGC #1531993. Authorized TGP, Vetrotech, and Pyrobel installer.',
    keywords='fire-rated glass installer, TGP fire-rated, UL fire glazing, 60 minute fire glass, 90 minute fire-rated, fire-rated curtainwall, fire-rated storefront, fire door commercial',
    og_title='Fire-Rated Glass Systems',
    og_description='TGP-authorized fire-rated glass installer. UL-listed assemblies, 20-min to 120-min ratings.',
    og_image='https://acglass.com/images/projects/martin-county-fire-training/martin-county-fire-training-exterior.jpg',
    h1='Fire-rated glass systems',
    eyebrow='Fire-Rated Pillar &middot; Florida CGC',
    lead='Fire-rated glazing protects egress paths, separates fire areas, and meets IBC Chapter 7 / Florida Building Code requirements. We install UL-listed assemblies from 20-minute to 120-minute ratings, including HVHZ + fire-rated combos, with TGP, Vetrotech, and Pyrobel product lines.',
    answer='ACG is a Florida-licensed installer (FL CGC #1531993) of UL-listed fire-rated glass systems. We install 20-minute, 45-minute, 60-minute, 90-minute, and 120-minute rated assemblies including fire-protective and fire-resistive glazing. Authorized TGP installer with experience on hospital, school, multifamily, and federal projects across Florida. HVHZ + fire-rated combinations available.',
    children=[
        ('/architect-specs/', 'CSI Division 08 specs'),
        ('/commercial-storefront-systems.html', 'Storefront systems'),
        ('/curtainwall-installation.html', 'Curtainwall installation'),
        ('/approvals/', 'FPA &amp; NOA index'),
        ('/glossary.html', 'Glazing glossary'),
        ('/commercial-glass-cost-data.html', 'Commercial glazing cost'),
    ],
    sections=[
        ('Fire-rated glazing — two categories', """<h3>Fire-Protective Glazing</h3>
<p>Limits the passage of flames and smoke but transmits radiant heat. Rated up to 45 minutes for &le; 100 SF and 20 minutes for unlimited size. Common applications: corridor windows, door vision panels, transoms.</p>
<h3>Fire-Resistive Glazing</h3>
<p>Limits flames, smoke, AND radiant heat. Rated 60, 90, or 120 minutes. Treated as a wall assembly under the building code. Common applications: stairwell separations, exit access corridors, area separations.</p>
<h3>Which is required?</h3>
<p>IBC Chapter 7 / FBC dictates rating by occupancy, building type, and location within the structure. Fire-resistive is required where the assembly substitutes for a fire-rated wall. Fire-protective covers most door and small-opening applications.</p>"""),
        ('Systems we install', """<table>
<thead><tr><th>Product</th><th>Manufacturer</th><th>Rating</th><th>Type</th><th>Use</th></tr></thead>
<tbody>
<tr><td>FireLite Plus</td><td>TGP</td><td>20&ndash;90 min</td><td>Fire-protective</td><td>Doors, sidelites, transoms</td></tr>
<tr><td>Pilkington Pyrostop</td><td>TGP</td><td>20&ndash;120 min</td><td>Fire-resistive</td><td>Stairwell, area separation</td></tr>
<tr><td>FireSeal</td><td>TGP</td><td>20&ndash;90 min</td><td>Fire-protective</td><td>Curtain wall, ribbon window</td></tr>
<tr><td>Vetrotech Contraflam</td><td>Vetrotech</td><td>30&ndash;120 min</td><td>Fire-resistive</td><td>High-spec fire walls</td></tr>
<tr><td>HVHZ + fire-rated combos</td><td>TGP custom</td><td>Per NOA + UL</td><td>Combined</td><td>Florida HVHZ + fire-rated</td></tr>
</tbody>
</table>"""),
        ('Where we install fire-rated', """<ul>
<li><strong>Healthcare</strong> &mdash; hospital corridors, ED separations, OR area boundaries</li>
<li><strong>Education</strong> &mdash; school stairwells, corridor separations, gymnasium walls</li>
<li><strong>Multifamily</strong> &mdash; unit-to-corridor doors, stairwell vision panels</li>
<li><strong>Federal / military</strong> &mdash; specified rated separations</li>
<li><strong>Office &amp; mixed-use</strong> &mdash; high-rise stair enclosures, area separations between tenancies</li>
<li><strong>Hospitality</strong> &mdash; back-of-house separations, kitchen exhausts</li>
</ul>
<p>Example project: <a href="/martin-county-fire-training-exterior.html" style="color:var(--accent);">Martin County Fire Training Facility</a> &mdash; fire-rated assemblies installed by ACG.</p>"""),
        ('Frequently asked questions', """<h3>How much does fire-rated glass cost?</h3>
<p>Fire-protective: $50&ndash;$120/SF installed. Fire-resistive (60+ min): $180&ndash;$320/SF installed. Custom HVHZ + fire-rated combos: project-specific.</p>
<h3>What&rsquo;s the difference between wired glass and modern fire-rated?</h3>
<p>Wired glass is largely obsolete in new commercial construction &mdash; banned in many applications by IBC since 2003 due to safety glazing requirements (CPSC 16 CFR 1201). Modern fire-rated uses ceramic, intumescent, or filmed/laminated assemblies.</p>
<h3>Can fire-rated glass be impact-rated for HVHZ?</h3>
<p>Yes &mdash; TGP and Vetrotech both make combined fire-rated and impact-rated assemblies. Rare but possible. Send drawings for spec confirmation.</p>
<h3>What standards govern fire-rated glazing?</h3>
<p>UL 9 (positive-pressure testing), UL 10B (neutral-pressure), NFPA 252 (door assemblies), NFPA 257 (window assemblies), and IBC Chapter 7. Florida adopts these by reference.</p>"""),
    ],
)

ALL_PAGES = [P1, P2, P3, P4, P5]

def faq_schema_from_sections(sections, page_url):
    """Extract a FAQPage schema from any section titled 'Frequently asked questions'."""
    qs = []
    for title, html in sections:
        if 'questions' not in title.lower():
            continue
        # naive parse: <h3>Q?</h3><p>A.</p> pairs
        import re
        h3s = re.findall(r'<h3>(.*?)</h3>\s*<p>(.*?)</p>', html, re.DOTALL)
        for q, a in h3s:
            # strip inline tags for the answer text
            clean_a = re.sub(r'<[^>]+>', '', a).strip()
            clean_q = re.sub(r'<[^>]+>', '', q).strip()
            qs.append({
                "@type": "Question",
                "name": clean_q.replace('&rsquo;', "'").replace('&amp;', '&'),
                "acceptedAnswer": {"@type": "Answer", "text": clean_a.replace('&rsquo;', "'").replace('&amp;', '&').replace('&ndash;','-')}
            })
    if not qs:
        return None
    return {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": qs
    }

def build_page(p):
    page_url = f"https://acglass.com/{p['slug']}.html"
    # Service schema
    service_schema = {
        "@context": "https://schema.org",
        "@type": "Service",
        "@id": page_url + "#service",
        "name": p['h1'].replace('&amp;', '&').replace('&mdash;', '—').replace('&middot;', '·'),
        "description": p['description'],
        "url": page_url,
        "provider": ACG_ORG,
        "areaServed": [
            {"@type": "State", "name": "Florida"},
            {"@type": "State", "name": "Tennessee"},
            {"@type": "State", "name": "Georgia"},
            {"@type": "State", "name": "Alabama"}
        ],
        "serviceType": p['h1'].replace('&amp;', '&').replace('&mdash;', '—'),
        "audience": {"@type": "BusinessAudience", "audienceType": "Architects, General Contractors, Owners, Developers"}
    }
    # Article schema (for E-E-A-T)
    article_schema = {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": p['h1'].replace('&amp;', '&').replace('&mdash;', '—').replace('&middot;', '·'),
        "description": p['description'],
        "author": CONNOR,
        "publisher": {"@type": "Organization", "name": "American Commercial Glass", "logo": {"@type": "ImageObject", "url": "https://acglass.com/images/acg-logo-nav@2x.png"}},
        "datePublished": "2026-05-13",
        "dateModified": "2026-05-13",
        "mainEntityOfPage": page_url,
        "image": p['og_image'],
        "speakable": {"@type": "SpeakableSpecification", "cssSelector": ["h1", "#answer-box", "table"]}
    }
    # Breadcrumb
    breadcrumb_schema = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://acglass.com/"},
            {"@type": "ListItem", "position": 2, "name": "Services", "item": "https://acglass.com/services.html"},
            {"@type": "ListItem", "position": 3, "name": p['h1'].replace('&amp;', '&').replace('&mdash;', '—').replace('&middot;', '·'), "item": page_url}
        ]
    }

    faq_schema = faq_schema_from_sections(p['sections'], page_url)

    schema_parts = [service_schema, article_schema, breadcrumb_schema]
    if faq_schema: schema_parts.append(faq_schema)

    schema_blocks = '\n'.join(
        f'  <script type="application/ld+json">\n{json.dumps(s, indent=2)}\n  </script>'
        for s in schema_parts
    )

    head = HEAD_TEMPLATE.format(
        title=p['title'], description=p['description'], keywords=p['keywords'],
        slug=p['slug'], og_title=p['og_title'], og_description=p['og_description'],
        og_image=p['og_image'], schema_blocks=schema_blocks
    )

    # Hero + answer
    hero = f"""
  <section class="hero">
    <div class="eyebrow">{p['eyebrow']}</div>
    <h1>{p['h1']}</h1>
    <p class="lead">{p['lead']}</p>
    <div class="byline">By Connor Walsh &middot; President, American Commercial Glass &middot; FL CGC #1531993 &middot; Published May 13, 2026</div>
  </section>

  <div id="answer-box">
    <h2>Direct answer</h2>
    <p>{p['answer']}</p>
  </div>

  <main class="content">
"""
    # Trust signals
    main_content = trust_signals_block()

    # Sections
    for section_title, section_html in p['sections']:
        main_content += f"\n    <h2>{section_title}</h2>\n    {section_html}\n"

    # Children grid
    children_grid = '\n      '.join(
        f'<a href="{href}">{label}</a>' for href, label in p['children']
    )
    main_content += f"""
    <h2>Related ACG resources</h2>
    <div class="pill-grid">
      {children_grid}
    </div>

    <div class="cta-box">
      <h3 style="margin-top:0;">Have a project?</h3>
      <p style="margin-bottom:14px;">Send drawings to ACG. We&rsquo;ll review system selection, code path, and budget &mdash; no charge. Florida CGC #1531993. 350+ projects.</p>
      <p><a href="/bid.html">Submit plans &rarr;</a> &nbsp;|&nbsp; <a href="/commercial-glass-cost-data.html">See pricing data &rarr;</a> &nbsp;|&nbsp; <a href="/contact.html">Contact ACG &rarr;</a></p>
    </div>
  </main>
"""
    return head + hero + main_content + FOOTER


def main():
    written = 0
    for p in ALL_PAGES:
        out_path = ROOT / f"{p['slug']}.html"
        out_path.write_text(build_page(p))
        size_k = out_path.stat().st_size // 1024
        print(f"OK  {p['slug']}.html ({size_k}K)")
        written += 1
    print(f"\nWrote {written}/{len(ALL_PAGES)} pillar pages.")

if __name__ == '__main__':
    main()
