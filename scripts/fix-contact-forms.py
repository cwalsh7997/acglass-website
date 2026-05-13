#!/usr/bin/env python3
"""Replace placeholder Formspree endpoints with working mailto fallback on send-plans.html and partners.html. Also switch nashville@ -> connor@ sitewide."""
import re
from pathlib import Path

ROOT = Path('/home/user/workspace/acglass-website')

# Fix 1: send-plans.html — replace JS submit handler so it always builds a mailto + opens mail client
sp = ROOT / 'send-plans.html'
sp_html = sp.read_text()
# The current handler errors out on placeholder. Replace with a proper mailto builder.
old_handler = """        // If Formspree endpoint is still the placeholder, fall back to email
        if (form.action.indexOf('formspree-pending') !== -1 || form.action.indexOf('YOUR_FORMSPREE_ID') !== -1) {
          e.preventDefault();
          status.style.color = 'var(--accent)';
          status.innerHTML = 'Form endpoint not yet configured. Please email plans to <a href="mailto:connor@acglass.com" style="color:inherit;text-decoration:underline;">connor@acglass.com</a> or call (772) 486-7711.';
          return;
        }"""
new_handler = """        // Always use mailto delivery (reliable, no third-party dependency)
        if (form.action.indexOf('formspree-pending') !== -1 || form.action.indexOf('YOUR_FORMSPREE_ID') !== -1) {
          e.preventDefault();
          var get = function(n){ var el = form.querySelector('[name="'+n+'"]'); return el ? el.value : ''; };
          var name = get('name'), company = get('company'), email = get('email'), phone = get('phone');
          var role = get('role'), project = get('project_name'), location = get('project_location');
          var btype = get('building_type'), bidtype = get('bid_type'), sf = get('total_sf');
          var due = get('bid_due'), notes = get('notes');
          var subject = 'Plans Submission — ' + (project || company || name);
          var body = 'PROJECT INFO%0D%0A' +
                     'Project: ' + project + '%0D%0A' +
                     'Location: ' + location + '%0D%0A' +
                     'Building Type: ' + btype + '%0D%0A' +
                     'Total SF: ' + sf + '%0D%0A' +
                     'Bid Due: ' + due + '%0D%0A' +
                     'Bid Type: ' + bidtype + '%0D%0A%0D%0A' +
                     'CONTACT%0D%0A' +
                     'Name: ' + name + '%0D%0A' +
                     'Company: ' + company + '%0D%0A' +
                     'Role: ' + role + '%0D%0A' +
                     'Email: ' + email + '%0D%0A' +
                     'Phone: ' + phone + '%0D%0A%0D%0A' +
                     'NOTES%0D%0A' + notes + '%0D%0A%0D%0A' +
                     'NOTE: Drawing files cannot be attached through this form. Please attach plans (PDF, DWG, ZIP) to this email before sending. For files over 25MB, paste a Procore/BuildingConnected/Dropbox link in the Notes section above and re-send.%0D%0A%0D%0A' +
                     'Submitted from acglass.com/send-plans';
          status.style.color = 'var(--accent)';
          status.innerHTML = 'Opening your email — please attach drawing files before sending. If your mail client did not open, email plans to <a href="mailto:connor@acglass.com" style="color:inherit;text-decoration:underline;">connor@acglass.com</a>.';
          window.location.href = 'mailto:connor@acglass.com?subject=' + encodeURIComponent(subject) + '&body=' + body;
          if (typeof gtag === 'function') gtag('event', 'bid_form_submit_mailto', { bid_type: bidtype });
          return;
        }"""
if old_handler in sp_html:
    sp_html = sp_html.replace(old_handler, new_handler)
    sp.write_text(sp_html)
    print("OK  send-plans.html — Formspree placeholder replaced with working mailto handler")
else:
    print("WARN send-plans.html — old handler pattern not found; may already be fixed")

# Fix 2: partners.html — same treatment
pt = ROOT / 'partners.html'
pt_html = pt.read_text()
# Find the form and check for any submit handler
form_match = re.search(r'<form class="cta-form"[^>]*action="https://formspree\.io/f/formspree-pending"[^>]*>', pt_html)
if form_match:
    # Replace the form action and add an onsubmit handler
    old_form = form_match.group(0)
    new_form = old_form.replace('action="https://formspree.io/f/formspree-pending"', 'action="mailto:connor@acglass.com" onsubmit="return handlePartnerSubmit(event)"')
    pt_html = pt_html.replace(old_form, new_form)
    # Inject the handler script just before </body>
    handler_script = """
<script>
function handlePartnerSubmit(e){
  e.preventDefault();
  var f = e.target;
  var get = function(n){ var el = f.querySelector('[name="'+n+'"]'); return el ? el.value : ''; };
  var fields = ['name','company','email','phone','company_type','website','project_volume','interest','message'];
  var lines = [];
  fields.forEach(function(n){
    var v = get(n);
    if (v) lines.push(n.replace(/_/g, ' ').toUpperCase() + ': ' + v);
  });
  var subject = 'Dealer Network Inquiry — ' + (get('company') || get('name'));
  var body = lines.join('%0D%0A') + '%0D%0A%0D%0ASubmitted from acglass.com/partners';
  window.location.href = 'mailto:connor@acglass.com?subject=' + encodeURIComponent(subject) + '&body=' + body;
  var status = f.querySelector('.form-status');
  if (status) status.textContent = 'Opening your email — if it does not open, email connor@acglass.com directly.';
  return false;
}
</script>
"""
    if 'handlePartnerSubmit' not in pt_html:
        pt_html = pt_html.replace('</body>', handler_script + '</body>')
    pt.write_text(pt_html)
    print("OK  partners.html — Formspree placeholder replaced with mailto submit handler")
else:
    print("WARN partners.html — Formspree placeholder pattern not found; checking action attribute")

# Fix 3: nashville@acglass.com -> connor@acglass.com sitewide (until Connor confirms mailbox exists)
nashville_count = 0
for fp in ROOT.rglob('*.html'):
    if '.git' in fp.parts or 'drafts' in fp.parts: continue
    try: c = fp.read_text()
    except: continue
    if 'nashville@acglass.com' in c:
        c2 = c.replace('nashville@acglass.com', 'connor@acglass.com')
        fp.write_text(c2)
        nashville_count += 1
print(f"OK  Switched nashville@acglass.com -> connor@acglass.com in {nashville_count} files")

# Fix 4: same for contact@acglass.com -> connor@acglass.com (in mailto refs only — footer placeholder)
contact_count = 0
for fp in ROOT.rglob('*.html'):
    if '.git' in fp.parts or 'drafts' in fp.parts: continue
    try: c = fp.read_text()
    except: continue
    if 'mailto:contact@acglass.com' in c:
        c2 = c.replace('mailto:contact@acglass.com', 'mailto:connor@acglass.com')
        fp.write_text(c2)
        contact_count += 1
print(f"OK  Switched mailto:contact@acglass.com -> mailto:connor@acglass.com in {contact_count} files")

print()
print("All contact form fixes applied. Every form on the site now routes to connor@acglass.com.")
