#!/usr/bin/env python3
"""T1.3 — Spec page augmentation.

For each spec page:
 (a) Plain estimator language summary — already present in spec-hero summary.
 (b) Compliant Systems table built from /noa/data.json (system/category, FL PA #, NOA #, expiration, source).
 (c) Submittal checklist — already present in the 1.4 SUBMITTALS subsection of the pre block.
 (d) Coordination/lead-time paragraph (no specific weeks unless sourced).
 (e) CTA: 'Send us the spec section — scope letter in 48 hours' linking /contact.html.
 (f) 2+ internal links: /noa/ + matching service page.
 (g) Word count ≥ 1,000.
"""
import json
import re
from pathlib import Path

ROOT = Path('/home/user/workspace/acglass-website')
SPECS = ROOT / 'architect-specs'
DATA = json.loads((ROOT / 'noa' / 'data.json').read_text())

# Section → service page mapping (must be 2nd internal link)
SECTION_SERVICE = {
    'section-08-41-13-aluminum-storefront.html': ('/commercial-storefront-systems.html', 'Commercial Storefront Systems', ['eswindows','euro-wall','aldora','slimpact','pgt']),
    'section-08-43-29-folding-glass-walls.html': ('/multi-slide-bifold-doors.html', 'Multi-Slide & Bi-Fold Doors', ['euro-wall']),
    'section-08-44-13-aluminum-curtainwall.html': ('/curtainwall-systems.html', 'Curtain Wall Systems', ['eswindows','aldora','slimpact']),
    'section-08-44-23-multi-slide-doors.html': ('/multi-slide-bifold-doors.html', 'Multi-Slide & Bi-Fold Doors', ['euro-wall','eswindows']),
    'section-08-51-13-aluminum-windows.html': ('/impact-windows-doors.html', 'Impact Windows & Doors', ['eswindows','pgt','aldora']),
    'section-08-71-00-automatic-entrance-door-hardware.html': ('/automatic-entrance-systems.html', 'Automatic Entrance Systems', []),
    'section-08-87-13-fire-rated-glazing.html': ('/fire-rated-glass-systems.html', 'Fire-Rated Glass Systems', ['tgp','slimpact']),
}

# Filter NOA data to relevant categories per section
SECTION_CATEGORY_FILTER = {
    'section-08-41-13-aluminum-storefront.html': lambda cat: 'Storefronts' in cat or 'Windows' in cat,
    'section-08-43-29-folding-glass-walls.html': lambda cat: 'Swinging' in cat or 'Sliding' in cat,
    'section-08-44-13-aluminum-curtainwall.html': lambda cat: 'Curtain Walls' in cat,
    'section-08-44-23-multi-slide-doors.html': lambda cat: 'Sliding' in cat,
    'section-08-51-13-aluminum-windows.html': lambda cat: 'Windows' in cat,
    'section-08-71-00-automatic-entrance-door-hardware.html': lambda cat: False,  # hardware section — no FPA data
    'section-08-87-13-fire-rated-glazing.html': lambda cat: False,  # fire-rated — no FPA data, TGP not in portal
}


def build_compliant_table(section):
    """Build HTML table for Compliant Systems table for this section."""
    allowed_partners = SECTION_SERVICE[section][2]
    cat_filter = SECTION_CATEGORY_FILTER[section]
    
    rows = []
    for pkey in allowed_partners:
        partner = DATA['partners'].get(pkey)
        if not partner:
            continue
        for s in partner['systems']:
            cat = s.get('category', '')
            if not cat_filter(cat):
                continue
            rows.append({
                'manufacturer': partner['label'],
                'system': cat,
                'fl_pa': s['fl_pa'],
                'noa': s.get('miami_dade_noa', 'pending verification'),
                'expiration': s.get('expiration', 'pending verification'),
                'source': s['source_url'],
            })
    
    if not rows:
        # Section has no FPA-tracked systems — explain honestly
        if section == 'section-08-71-00-automatic-entrance-door-hardware.html':
            note = 'Automatic entrance hardware (Allegion, Stanley, Horton, Record) is regulated by ANSI A156.10 / A156.19 — not the Florida Product Approval system. Project-specific UL listings and ANSI/BHMA compliance documents are submitted with each bid.'
        elif section == 'section-08-87-13-fire-rated-glazing.html':
            note = 'Fire-rated glazing (TGP, SCHOTT, Vetrotech, Slimpact) is governed by IBC/NFPA test methods — UL 9, UL 10B, UL 10C, UL 263, NFPA 252, NFPA 257 — not the Florida Product Approval (wind-load) system. Listing report numbers from UL Online Certifications Directory or Intertek Directory of Listed Products are submitted with each bid.'
        else:
            note = 'No Florida Product Approvals on file for this section at this time. ACG verifies approval coverage at bid time against the source portal.'
        return f'''      <div class="compliant-note">
        <strong>Note on this section.</strong> {note}
      </div>'''
    
    # Build table HTML
    body_rows = []
    for r in rows:
        # Render long values gracefully
        fl_pa_html = f'<a href="{r["source"]}" target="_blank" rel="noopener" style="color:#E11320;font-family:monospace;">{r["fl_pa"]}</a>'
        noa_html = r['noa'] if r['noa'] != 'pending verification' else '<span style="color:rgba(255,193,7,0.85);font-style:italic;font-size:11px;">pending verification</span>'
        exp_html = r['expiration'] if 'pending' not in r['expiration'].lower() and 'not in public' not in r['expiration'].lower() else '<span style="color:rgba(255,193,7,0.85);font-style:italic;font-size:11px;">see source PDF</span>'
        body_rows.append(f'''        <tr>
          <td>{r["manufacturer"]}</td>
          <td>{r["system"]}</td>
          <td>{fl_pa_html}</td>
          <td>{noa_html}</td>
          <td>{exp_html}</td>
          <td class="src-link"><a href="{r["source"]}" target="_blank" rel="noopener" style="color:rgba(255,255,255,0.6);font-size:11px;">portal</a></td>
        </tr>''')
    
    return f'''      <div class="compliant-table-wrap" style="overflow-x:auto;margin:24px 0;border:1px solid rgba(255,255,255,0.1);border-radius:6px;">
        <table class="compliant-table" style="width:100%;border-collapse:collapse;font-size:13px;color:rgba(255,255,255,0.85);">
          <thead>
            <tr style="background:rgba(225,19,32,0.08);">
              <th style="text-align:left;padding:10px 12px;font-size:11px;letter-spacing:0.06em;text-transform:uppercase;color:#E11320;border-bottom:1px solid rgba(225,19,32,0.3);">Manufacturer</th>
              <th style="text-align:left;padding:10px 12px;font-size:11px;letter-spacing:0.06em;text-transform:uppercase;color:#E11320;border-bottom:1px solid rgba(225,19,32,0.3);">System / Category</th>
              <th style="text-align:left;padding:10px 12px;font-size:11px;letter-spacing:0.06em;text-transform:uppercase;color:#E11320;border-bottom:1px solid rgba(225,19,32,0.3);">FL PA #</th>
              <th style="text-align:left;padding:10px 12px;font-size:11px;letter-spacing:0.06em;text-transform:uppercase;color:#E11320;border-bottom:1px solid rgba(225,19,32,0.3);">Miami-Dade NOA #</th>
              <th style="text-align:left;padding:10px 12px;font-size:11px;letter-spacing:0.06em;text-transform:uppercase;color:#E11320;border-bottom:1px solid rgba(225,19,32,0.3);">Expiration</th>
              <th style="text-align:left;padding:10px 12px;font-size:11px;letter-spacing:0.06em;text-transform:uppercase;color:#E11320;border-bottom:1px solid rgba(225,19,32,0.3);">Source</th>
            </tr>
          </thead>
          <tbody>
{chr(10).join(body_rows)}
          </tbody>
        </table>
      </div>'''


def build_augment_block(section):
    """Build the augmentation HTML block for the given section."""
    service_path, service_label, _ = SECTION_SERVICE[section]
    section_num = section.split('section-')[1].rsplit('.', 1)[0].rsplit('-', 1)[0].replace('-', ' ').upper()
    table_html = build_compliant_table(section)
    
    return f'''
    <section class="spec-augment" style="max-width:880px;margin:40px auto;padding:0 28px;color:rgba(255,255,255,0.9);font-family:'Inter',system-ui,sans-serif;">
      <h2 style="font-size:1.5rem;margin:0 0 12px;color:#fff;">Compliant systems on file</h2>
      <p style="line-height:1.7;color:rgba(255,255,255,0.75);">Every Florida Product Approval (FL PA) number below has been hand-verified against the official source — <a href="https://www.floridabuilding.org/pr/pr_app_lst.aspx" target="_blank" rel="noopener" style="color:#E11320;">floridabuilding.org Product Approval portal</a> — and links to the source URL inline. Miami-Dade NOA cells marked &lsquo;pending verification&rsquo; require a separate portal session that ACG runs at bid time. Expiration and design pressure are not displayed on the public-facing FPA portal; both appear inside the linked approval PDFs.</p>
{table_html}
      <p style="font-size:13px;color:rgba(255,255,255,0.6);margin-top:16px;">Full reference: see the <a href="/noa/" style="color:#E11320;">ACG NOA &amp; FL PA Hub</a> for every authorized manufacturer&rsquo;s approvals in one place.</p>

      <h2 style="font-size:1.5rem;margin:32px 0 12px;color:#fff;">Coordination &amp; lead-time considerations</h2>
      <p style="line-height:1.7;color:rgba(255,255,255,0.75);">Lead time on this section depends on factory backlog, glass make-up, and finish. ACG quotes project-specific lead time in writing on every bid, sourced from the most recent factory acknowledgement on the proposed system &mdash; not from a published average. For complex assemblies (HVHZ + thermal break + custom finish), expect the bid to include a project-specific submittal schedule that runs from issued shop drawings through factory release. Coordination items to confirm with the General Contractor before submittal: rough opening tolerances, perimeter sequence (WRB transition, flashings, structural anchor path), and any sequence-dependent items downstream (interior finishes, MEP rough-in around the opening).</p>

      <h2 style="font-size:1.5rem;margin:32px 0 12px;color:#fff;">Related ACG resource</h2>
      <p style="line-height:1.7;color:rgba(255,255,255,0.75;">For ACG&rsquo;s services page on this scope, including project examples and bid-ready capabilities, see <a href="{service_path}" style="color:#E11320;">{service_label}</a>.</p>

      <div style="background:linear-gradient(135deg,rgba(225,19,32,0.12),rgba(225,19,32,0.04));border:1px solid rgba(225,19,32,0.3);border-radius:8px;padding:28px;margin:40px 0 24px;text-align:center;">
        <h2 style="font-size:1.25rem;margin:0 0 8px;color:#fff;">Send us the spec section &mdash; scope letter in 48 hours</h2>
        <p style="margin:0 0 18px;color:rgba(255,255,255,0.8);font-size:14px;">Drop your Division 08 spec, drawings, and bid package. ACG returns a sealed-engineer-ready scope letter within 48 hours.</p>
        <a href="/contact.html" style="display:inline-block;padding:12px 28px;background:#E11320;color:#fff;text-decoration:none;border-radius:6px;font-weight:600;letter-spacing:0.04em;">Send the spec &rarr;</a>
      </div>
    </section>
'''


def augment_spec(filename):
    path = SPECS / filename
    if not path.exists():
        print(f"MISS: {filename}")
        return
    c = path.read_text()
    
    # Insert augment block AFTER </pre> if present, BEFORE <aside class="spec-notes" or <aside class="noa-hub-callout"
    # Strategy: locate end of <pre class="spec-body" ... </pre> and insert after it,
    # but only if 'spec-augment' is not already present.
    if 'class="spec-augment"' in c:
        print(f"SKIP (already augmented): {filename}")
        return
    
    augment = build_augment_block(filename)
    # Insert right after the </pre> closing tag of spec-body
    pre_end = '</pre>'
    idx = c.find(pre_end)
    if idx < 0:
        print(f"WARN: no </pre> in {filename}")
        return
    insert_at = idx + len(pre_end)
    c = c[:insert_at] + '\n' + augment + c[insert_at:]
    path.write_text(c)
    print(f"OK: augmented {filename}")


# Process each existing spec page
for fname in SECTION_SERVICE:
    if fname == 'section-08-51-13-aluminum-windows.html':
        # Will be created next
        continue
    augment_spec(fname)
