# -*- coding: utf-8 -*-
import re, glob, os, json

POSTS = [p for p in glob.glob("/home/user/workspace/acglass-website/blog/*.html")
         if not p.endswith("/index.html")]

# Rich Person JSON-LD objects (as a string injected into the author: position).
# Keep the same indentation context; we replace the whole author object.
def person_obj(author, indent):
    pad = " " * indent
    if author == "rielly":
        d = {
            "@type":"Person",
            "@id":"https://acglass.com/#rielly-walsh",
            "name":"Rielly Walsh",
            "jobTitle":"CEO & Co-founder",
            "worksFor":{"@id":"https://acglass.com/#organization"},
            "url":"https://acglass.com/authors/rielly-walsh.html",
            "image":"https://acglass.com/images/team/rielly-walsh-portrait.jpg",
            "sameAs":["https://www.linkedin.com/company/american-commercial-glass-inc"],
            "knowsAbout":["Commercial Construction Management","Commercial Glazing","Project Delivery","Construction Operations","Field Coordination"]
        }
    else:
        d = {
            "@type":"Person",
            "@id":"https://acglass.com/#connor-walsh",
            "name":"Connor Walsh",
            "jobTitle":"President & Co-founder",
            "worksFor":{"@id":"https://acglass.com/#organization"},
            "url":"https://acglass.com/authors/connor-walsh.html",
            "image":"https://acglass.com/images/team/connor-walsh-portrait.jpg",
            "sameAs":["https://www.linkedin.com/in/connorwalsh1997"],
            "knowsAbout":["Commercial Glazing","Florida Building Code","Hurricane Impact Glazing","AI in Construction","Construction Operations"]
        }
    raw = json.dumps(d, indent=2, ensure_ascii=False)
    # re-indent every line (except first) by `indent`
    lines = raw.split("\n")
    out = lines[0]  # "{"
    for ln in lines[1:]:
        out += "\n" + pad + ln
    return out

BIO = {
 "connor": {
   "name":"Connor Walsh","role":"President &amp; Co-founder",
   "img":"../images/team/connor-walsh-portrait",
   "href":"../authors/connor-walsh.html",
   "bio":"Connor Walsh is the President and co-founder of American Commercial Glass. He is the qualifier for the company's Florida Certified General Contractor license (CGC #1531993) and a former pilot who previously founded and scaled a Florida glazing business from $400K to $10M. He leads ACG's commercial glazing and AI-managed operations across Florida.",
   "creds":"FL CGC #1531993 (Qualifier) &middot; Former pilot &middot; 350+ commercial projects",
   "linkedin":"https://www.linkedin.com/in/connorwalsh1997"
 },
 "rielly": {
   "name":"Rielly Walsh","role":"CEO &amp; Co-founder",
   "img":"../images/team/rielly-walsh-portrait",
   "href":"../authors/rielly-walsh.html",
   "bio":"Rielly Walsh is the CEO and co-founder of American Commercial Glass. She holds a degree in Concrete Industry Management from Middle Tennessee State University and previously ran stoneworks operations at Aqualina. She leads ACG's construction operations and project delivery across Florida.",
   "creds":"MTSU Concrete Industry Management &middot; Construction operations &middot; 350+ projects",
   "linkedin":"https://www.linkedin.com/company/american-commercial-glass-inc"
 }
}

def bio_card(author):
    b = BIO[author]
    return f'''
  <aside aria-label="About the author" style="background:#0e284f;padding:40px 24px;margin:0;border-top:1px solid rgba(255,255,255,.08);">
    <div style="max-width:840px;margin:0 auto;display:flex;gap:28px;align-items:flex-start;flex-wrap:wrap;">
      <picture>
        <source type="image/webp" srcset="{b['img']}.webp">
        <img src="{b['img']}.jpg" width="96" height="96" alt="{b['name']}, {b['role'].replace('&amp;','and')} of American Commercial Glass" style="width:96px;height:96px;border-radius:50%;object-fit:cover;border:3px solid #e11320;flex-shrink:0;" loading="lazy" decoding="async">
      </picture>
      <div style="flex:1;min-width:240px;">
        <div style="font-family:'JetBrains Mono',monospace;font-size:11px;letter-spacing:.14em;text-transform:uppercase;color:#e11320;margin-bottom:6px;">About the author</div>
        <h2 style="font-size:20px;font-weight:800;color:#fff;margin:0 0 2px;letter-spacing:-.01em;"><a href="{b['href']}" rel="author" style="color:#fff;text-decoration:none;">{b['name']}</a></h2>
        <div style="font-size:14px;color:rgba(255,255,255,.7);margin-bottom:12px;">{b['role']} &middot; American Commercial Glass</div>
        <p style="font-size:15px;line-height:1.65;color:rgba(255,255,255,.82);margin:0 0 12px;">{b['bio']}</p>
        <div style="font-family:'JetBrains Mono',monospace;font-size:11px;letter-spacing:.06em;color:rgba(255,255,255,.55);margin-bottom:12px;">{b['creds']}</div>
        <a href="{b['href']}" rel="author" style="font-family:'JetBrains Mono',monospace;font-size:12px;letter-spacing:.06em;text-transform:uppercase;font-weight:700;color:#fff;border-bottom:1px solid #e11320;text-decoration:none;">Full bio &amp; profile &rarr;</a>
      </div>
    </div>
  </aside>
'''

def resolve_author(html):
    m = re.search(r'<meta name="author" content="([^"]*)"', html)
    meta = m.group(1) if m else ""
    flag = None
    low = meta.lower()
    if "rielly" in low:
        return "rielly", None
    if "connor" in low:
        return "connor", None
    if "field team" in low:
        return "connor", "ACG Field Team byline -> defaulted to Connor Walsh"
    if not meta:
        return "connor", "No author meta -> defaulted to Connor Walsh"
    return "connor", f"Unrecognized author meta '{meta}' -> defaulted to Connor"

# Regex to match the author JSON-LD object. It starts at `"author": {` and ends at the
# matching closing brace followed by a comma (the simple flat object used here).
# All posts use: "author": {\n ...Person... \n  },
author_obj_re = re.compile(r'("author"\s*:\s*)\{.*?\n(\s*)\}', re.S)

results = {"connor":0, "rielly":0}
flags = []
no_byline = []
skipped_jsonld = []

redirect_stubs = []
for path in POSTS:
    html = open(path, encoding="utf-8").read()
    fn = os.path.basename(path)
    # Skip redirect/noindex stubs (e.g. unverified projects) — not real articles
    if 'http-equiv="refresh"' in html and '<footer class="footer">' not in html:
        redirect_stubs.append(fn)
        continue
    author, flag = resolve_author(html)
    if flag:
        flags.append(f"{fn}: {flag}")

    # 1) Replace JSON-LD author object (first occurrence)
    def repl(m):
        prefix = m.group(1)
        closing_indent = m.group(2)
        indent = len(closing_indent)
        return prefix + person_obj(author, indent)
    new_html, n = author_obj_re.subn(repl, html, count=1)
    if n == 0:
        skipped_jsonld.append(fn)
    else:
        html = new_html

    # 2) Update byline href(s): point both author links to the resolved /authors/ page.
    # Replace any occurrence of ../author-connor-walsh.html or ../author-rielly-walsh.html
    target = f"../authors/{author}-walsh.html"
    html = html.replace("../author-connor-walsh.html", target)
    html = html.replace("../author-rielly-walsh.html", target)
    # also fix the visible byline name if it mismatches resolved author in the hero byline
    # (byline uses rel="author" anchor text). Normalize anchor text to resolved name.
    # We do a light touch: replace ">Connor Walsh<" / ">Rielly Walsh<" inside rel="author" anchors.
    want_name = "Rielly Walsh" if author == "rielly" else "Connor Walsh"
    # Replace anchor text in rel="author" anchors pointing to target
    html = re.sub(r'(<a href="' + re.escape(target) + r'"[^>]*rel="author"[^>]*>)(Connor Walsh|Rielly Walsh)(</a>)',
                  lambda m: m.group(1) + want_name + m.group(3), html)

    # track if there is any visible byline
    if 'rel="author"' not in html:
        no_byline.append(fn)

    # 3) Insert bio card before the first `  <footer class="footer">`
    if "About the author" not in html:
        idx = html.find('<footer class="footer">')
        if idx != -1:
            # find start of that line
            line_start = html.rfind("\n", 0, idx) + 1
            html = html[:line_start] + bio_card(author) + html[line_start:]
        else:
            flags.append(f"{fn}: no footer anchor found for bio card insertion")

    open(path, "w", encoding="utf-8").write(html)
    results[author] += 1

print("Posts processed:", results['connor']+results['rielly'])
print("Redirect stubs skipped:", len(redirect_stubs), redirect_stubs)
print("Connor:", results["connor"], "Rielly:", results["rielly"])
print("JSON-LD author not replaced in:", len(skipped_jsonld), skipped_jsonld[:10])
print("Posts with NO visible byline after update:", len(no_byline), no_byline[:10])
print("FLAGS:")
for f in flags:
    print("  -", f)
open("/home/user/workspace/blog_author_flags.txt","w").write("\n".join(flags))
open("/home/user/workspace/blog_no_byline.txt","w").write("\n".join(no_byline))
