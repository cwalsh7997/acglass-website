#!/usr/bin/env python3
"""Build /noa/ hub pages from /noa/data.json.

Zero fabrication: every cell that hasn't been hand-verified shows 'pending verification'
with a link to the source portal. Each system row carries a Dataset JSON-LD block.

Run from repo root:
    python3 scripts/noa-hub-build.py
"""
import json
import os
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).resolve().parent.parent
DATA_PATH = ROOT / "noa" / "data.json"
OUT_DIR = ROOT / "noa"

with DATA_PATH.open() as f:
    data = json.load(f)

NAV = '''  <header role="banner">
    <nav class="acg-nav" aria-label="Primary">
      <a class="acg-nav-logo" href="/" aria-label="ACG home"><img src="/images/acg-logo-mark-2026.svg" alt="ACG" width="36" height="36" loading="eager" decoding="async"></a>
      <ul class="acg-nav-list">
        <li><a href="/services.html">Services</a></li>
        <li><a href="/portfolio.html">Portfolio</a></li>
        <li><a href="/manufacturers.html">Manufacturers</a></li>
        <li><a href="/approvals/">Approvals</a></li>
        <li><a href="/about.html">About</a></li>
        <li><a href="/contact.html">Contact</a></li>
      </ul>
    </nav>
  </header>
'''

FOOTER = '''  <footer role="contentinfo" style="background:#0e284f;color:#fff;padding:48px 24px 24px;margin-top:64px;">
    <div style="max-width:1200px;margin:0 auto;">
      <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:32px;margin-bottom:32px;">
        <div>
          <div style="font-weight:700;font-size:14px;margin-bottom:12px;color:#e11320;letter-spacing:0.08em;text-transform:uppercase;">ACG</div>
          <p style="font-size:14px;line-height:1.6;margin:0 0 8px;">American Commercial Glass, Inc.</p>
          <p style="font-size:13px;line-height:1.6;color:rgba(255,255,255,0.7);margin:0;">FL CGC #1531993 · Founded 2/18/2021</p>
        </div>
        <div>
          <div style="font-weight:700;font-size:14px;margin-bottom:12px;color:#e11320;letter-spacing:0.08em;text-transform:uppercase;">Approvals</div>
          <ul style="list-style:none;padding:0;margin:0;font-size:14px;line-height:1.8;">
            <li><a href="/noa/" style="color:#fff;text-decoration:none;">NOA Hub</a></li>
            <li><a href="/approvals/" style="color:#fff;text-decoration:none;">FL PA &amp; NOA Index</a></li>
            <li><a href="https://www.floridabuilding.org/pr/pr_app_lst.aspx" style="color:#fff;text-decoration:none;" rel="noopener">Florida Product Approval Portal</a></li>
            <li><a href="https://www.miamidade.gov/building/pc-search.asp" style="color:#fff;text-decoration:none;" rel="noopener">Miami-Dade NOA Portal</a></li>
          </ul>
        </div>
        <div>
          <div style="font-weight:700;font-size:14px;margin-bottom:12px;color:#e11320;letter-spacing:0.08em;text-transform:uppercase;">Contact</div>
          <p style="font-size:14px;line-height:1.6;margin:0;">specs@acglass.com<br>+1-772-486-7711</p>
        </div>
      </div>
      <p style="font-size:12px;color:rgba(255,255,255,0.5);margin:24px 0 0;border-top:1px solid rgba(255,255,255,0.1);padding-top:16px;">&copy; 2026 American Commercial Glass, Inc. All rights reserved.</p>
    </div>
  </footer>
'''

CSS = '''
    :root { --navy: #0e284f; --red: #e11320; --bg: #0a1628; --text: #fff; }
    * { box-sizing: border-box; }
    body { font-family: 'Inter', system-ui, -apple-system, sans-serif; background: var(--bg); color: var(--text); margin: 0; line-height: 1.6; }
    .noa-hero { padding: 80px 24px 48px; max-width: 1200px; margin: 0 auto; }
    .noa-hero h1 { font-size: clamp(2rem, 5vw, 3.5rem); margin: 0 0 16px; letter-spacing: -0.02em; line-height: 1.1; }
    .noa-hero .lead { font-size: 18px; color: rgba(255,255,255,0.75); max-width: 720px; margin: 0; }
    .noa-eyebrow { font-size: 12px; letter-spacing: 0.12em; text-transform: uppercase; color: var(--red); font-weight: 600; margin-bottom: 16px; }
    .noa-content { padding: 0 24px 64px; max-width: 1200px; margin: 0 auto; }
    .noa-callout { background: rgba(225,19,32,0.08); border-left: 3px solid var(--red); padding: 16px 20px; margin: 32px 0; border-radius: 4px; font-size: 14px; }
    .noa-callout strong { color: var(--red); }
    .noa-table-wrap { overflow-x: auto; margin: 32px 0; border-radius: 8px; background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08); }
    .noa-table { width: 100%; min-width: 900px; border-collapse: collapse; font-size: 13px; }
    .noa-table th { background: rgba(14,40,79,0.6); color: var(--red); text-transform: uppercase; letter-spacing: 0.05em; font-size: 11px; padding: 14px 16px; text-align: left; border-bottom: 2px solid var(--red); }
    .noa-table td { padding: 14px 16px; border-bottom: 1px solid rgba(255,255,255,0.06); vertical-align: top; }
    .noa-table tr:last-child td { border-bottom: none; }
    .noa-table tr:nth-child(even) { background: rgba(255,255,255,0.02); }
    .noa-pending { color: rgba(255,193,7,0.85); font-style: italic; }
    .noa-na { color: rgba(255,255,255,0.4); }
    .noa-source { font-size: 11px; }
    .noa-source a { color: var(--red); text-decoration: none; }
    .noa-source a:hover { text-decoration: underline; }
    .noa-partners { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 16px; margin: 32px 0; }
    .noa-partner-card { background: rgba(255,255,255,0.04); border: 1px solid rgba(255,255,255,0.08); border-radius: 8px; padding: 20px; text-decoration: none; color: var(--text); transition: all 0.2s; }
    .noa-partner-card:hover { background: rgba(225,19,32,0.08); border-color: var(--red); }
    .noa-partner-card h3 { margin: 0 0 8px; font-size: 18px; }
    .noa-partner-card .count { font-size: 13px; color: rgba(255,255,255,0.6); }
    h2 { font-size: 28px; margin: 48px 0 16px; letter-spacing: -0.01em; }
    a { color: var(--red); }
'''


def cell_html(value, source_url=None):
    if isinstance(value, str) and value.lower().startswith("pending"):
        if source_url:
            return f'<span class="noa-pending">pending verification</span>'
        return '<span class="noa-pending">pending verification</span>'
    if isinstance(value, str) and value.lower().startswith("n/a"):
        return f'<span class="noa-na">{value}</span>'
    if value is None:
        return '<span class="noa-na">—</span>'
    return str(value)


def source_link(url):
    if not url:
        return '<span class="noa-na">—</span>'
    return f'<a href="{url}" rel="noopener" target="_blank">portal</a>'


def page_head(title, description, canonical):
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title}</title>
  <meta name="description" content="{description}">
  <link rel="canonical" href="{canonical}">
  <meta name="robots" content="index,follow,max-image-preview:large,max-snippet:-1">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{description}">
  <meta property="og:url" content="{canonical}">
  <meta property="og:type" content="website">
  <meta name="theme-color" content="#0e284f">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap">
  <link rel="icon" href="/images/acg-favicon.svg" type="image/svg+xml">
  <style>{CSS}</style>
'''


def build_dataset_schema(partner_key, partner):
    """Return Dataset JSON-LD for a partner page."""
    return {
        "@context": "https://schema.org",
        "@type": "Dataset",
        "name": f"ACG NOA & Florida Product Approval Reference — {partner['label']}",
        "description": (
            f"Reference table of {partner['label']} commercial glazing systems that ACG installs, "
            "showing Florida Product Approval numbers, Miami-Dade NOA numbers, design pressures, "
            "and expiration dates. Cells marked 'pending verification' are populated only after "
            "manual cross-reference against the Florida Product Approval portal "
            "(floridabuilding.org) or Miami-Dade NOA portal."
        ),
        "url": f"https://acglass.com/noa/{partner_key}.html",
        "creator": {"@id": "https://acglass.com/#org"},
        "license": "https://acglass.com/legal/terms.html",
        "isAccessibleForFree": True,
        "keywords": [partner['label'], "Florida Product Approval", "Miami-Dade NOA", "commercial glazing", "HVHZ"],
        "variableMeasured": [
            "Florida Product Approval number",
            "Miami-Dade NOA number",
            "Expiration date",
            "Design pressure rating"
        ]
    }


def build_partner_page(key, partner):
    title = f"{partner['label']} — Florida Product Approvals & Miami-Dade NOAs | ACG"
    if len(title) > 60:
        title = f"{partner['label']} — FL PA + Miami-Dade NOA | ACG"
    description = (
        f"Reference table of {partner['label']} commercial glazing systems "
        f"ACG installs. FL PA numbers, Miami-Dade NOAs, design pressures."
    )
    canonical = f"https://acglass.com/noa/{key}.html"
    
    dataset_jsonld = json.dumps(build_dataset_schema(key, partner), indent=2, ensure_ascii=False)
    
    rows_html = []
    for s in partner["systems"]:
        rows_html.append(f'''        <tr>
          <td><strong>{s['series']}</strong></td>
          <td>{cell_html(s['fl_pa'])}</td>
          <td>{cell_html(s['miami_dade_noa'])}</td>
          <td>{cell_html(s['expiration'])}</td>
          <td>{cell_html(s['design_pressure'])}</td>
          <td class="noa-source">{source_link(s['source_url'])}</td>
          <td>{s.get('last_verified') or '<span class="noa-na">not yet</span>'}</td>
          <td>{s.get('last_attempted') or '<span class="noa-na">—</span>'}</td>
        </tr>''')
    
    body = f'''{page_head(title, description, canonical)}  <script type="application/ld+json">
{dataset_jsonld}
  </script>
</head>
<body>
{NAV}
  <main role="main">
    <section class="noa-hero">
      <div class="noa-eyebrow">NOA Reference</div>
      <h1>{partner['label']} — Florida Product Approvals & Miami-Dade NOAs</h1>
      <p class="lead">Reference table of {partner['label']} commercial glazing systems that ACG is authorized to install. Cells marked &lsquo;pending verification&rsquo; have not been hand-confirmed against the manufacturer&rsquo;s current portal listing &mdash; ACG verifies every approval on every project bid.</p>
    </section>

    <section class="noa-content">
      <div class="noa-callout">
        <strong>Verification policy.</strong> Every cell on this page that is not &lsquo;pending verification&rsquo; has been hand-confirmed against the Florida Product Approval portal or Miami-Dade NOA portal on the &lsquo;last verified&rsquo; date shown. Approval numbers change. For binding bid use, always cross-reference with the source portal before submittal. ACG does not certify the contents of this page for permit submission &mdash; we certify only the project-specific sealed engineering we deliver with each bid.
      </div>

      <div class="noa-table-wrap">
        <table class="noa-table">
          <thead>
            <tr>
              <th>System / Series</th>
              <th>FL PA #</th>
              <th>Miami-Dade NOA #</th>
              <th>Expiration</th>
              <th>Design Pressure</th>
              <th>Source</th>
              <th>Last Verified</th>
              <th>Last Attempted</th>
            </tr>
          </thead>
          <tbody>
{chr(10).join(rows_html)}
          </tbody>
        </table>
      </div>

      <h2>Verify against the source</h2>
      <p>For the {partner['label']} systems listed above, use the official source portals:</p>
      <ul>
        <li><a href="https://www.floridabuilding.org/pr/pr_app_lst.aspx" rel="noopener" target="_blank">Florida Product Approval portal</a> &mdash; search by manufacturer name &lsquo;{partner['label']}&rsquo;.</li>
        <li><a href="https://www.miamidade.gov/building/pc-search.asp" rel="noopener" target="_blank">Miami-Dade NOA portal</a> &mdash; search by manufacturer for HVHZ-listed assemblies.</li>
        <li><a href="{partner['manufacturer_url']}" rel="noopener" target="_blank">{partner['label']} manufacturer site</a> &mdash; for current spec sheets and installation guides.</li>
      </ul>

      <h2>Need a project-specific approval verification?</h2>
      <p>Email <a href="mailto:specs@acglass.com">specs@acglass.com</a> with the system, framing, glass make-up, and design pressure required. ACG will confirm approval coverage and submit a sealed bid.</p>

      <p style="margin-top:32px;"><a href="/noa/">&larr; Back to NOA hub</a></p>
    </section>
  </main>
{FOOTER}
</body>
</html>
'''
    return body


def build_index_page():
    title = "NOA & FL PA Hub — ESWindows, Euro-Wall, PGT, TGP, Aldora, Slimpact | ACG"
    if len(title) > 60:
        title = "NOA & FL PA Hub — Manufacturer Reference | ACG"
    description = "Reference hub for Florida Product Approvals and Miami-Dade NOAs covering ESWindows, Euro-Wall, PGT, TGP, Aldora, and Slimpact systems ACG installs."
    canonical = "https://acglass.com/noa/"
    
    partner_cards = []
    for key, p in data["partners"].items():
        partner_cards.append(f'''        <a href="/noa/{key}.html" class="noa-partner-card">
          <h3>{p['label']}</h3>
          <div class="count">{len(p['systems'])} system{'s' if len(p['systems']) != 1 else ''}</div>
        </a>''')
    
    last_full = data["_meta"]["last_full_pass_attempt"]
    
    index_jsonld = {
        "@context": "https://schema.org",
        "@type": "CollectionPage",
        "name": "NOA & Florida Product Approval Hub",
        "description": description,
        "url": canonical,
        "isPartOf": {"@id": "https://acglass.com/#website"},
        "publisher": {"@id": "https://acglass.com/#org"},
        "hasPart": [
            {"@type": "Dataset", "name": f"ACG NOA Reference — {p['label']}", "url": f"https://acglass.com/noa/{k}.html"}
            for k, p in data["partners"].items()
        ]
    }
    body = f'''{page_head(title, description, canonical)}  <script type="application/ld+json">
{json.dumps(index_jsonld, indent=2, ensure_ascii=False)}
  </script>
</head>
<body>
{NAV}
  <main role="main">
    <section class="noa-hero">
      <div class="noa-eyebrow">Approvals Reference</div>
      <h1>NOA &amp; Florida Product Approval Hub</h1>
      <p class="lead">A single reference for the Florida Product Approval (FPA) numbers, Miami-Dade Notices of Acceptance (NOAs), expiration dates, and design pressures of the commercial glazing systems ACG installs. Built for spec writers, GCs, and project managers who need a quick lookup before issuing a bid or submittal.</p>
    </section>

    <section class="noa-content">
      <div class="noa-callout">
        <strong>Zero-fabrication policy.</strong> Approval numbers, expirations, and design pressures on these pages are populated only after manual cross-reference against the Florida Product Approval portal (floridabuilding.org) or Miami-Dade NOA portal (miamidade.gov). Cells marked &lsquo;pending verification&rsquo; have not been hand-confirmed yet. For binding bid use, always verify against the source portal before submittal. Last full-pass attempt: {last_full}.
      </div>

      <h2>Manufacturer pages</h2>
      <div class="noa-partners">
{chr(10).join(partner_cards)}
      </div>

      <h2>How this hub is maintained</h2>
      <p>The page schema (system list, source URLs) is stored in <code>/noa/data.json</code> in the ACG repository. A scheduled GitHub Action runs monthly and writes a status report covering any verification gaps. Verification entries are added by hand when ACG&rsquo;s estimating team confirms an approval against the source portal during normal bid work.</p>

      <h2>Source portals</h2>
      <ul>
        <li><a href="https://www.floridabuilding.org/pr/pr_app_lst.aspx" rel="noopener" target="_blank">Florida Product Approval portal</a> &mdash; the official Florida Department of Business and Professional Regulation database for non-HVHZ commercial systems.</li>
        <li><a href="https://www.miamidade.gov/building/pc-search.asp" rel="noopener" target="_blank">Miami-Dade NOA portal</a> &mdash; the official Miami-Dade County Product Control database for HVHZ-rated commercial systems.</li>
      </ul>

      <p style="margin-top:32px;"><a href="/approvals/">View the legacy approvals index &rarr;</a></p>
    </section>
  </main>
{FOOTER}
</body>
</html>
'''
    return body


# Write index
(OUT_DIR / "index.html").write_text(build_index_page())
print("WROTE: noa/index.html")

# Write partner pages
for key, partner in data["partners"].items():
    (OUT_DIR / f"{key}.html").write_text(build_partner_page(key, partner))
    print(f"WROTE: noa/{key}.html ({len(partner['systems'])} systems)")
