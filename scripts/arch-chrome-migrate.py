#!/usr/bin/env python3
"""arch-chrome-migrate.py - put the architectural-design header, menu and footer on every page.

Replaces the legacy <header class="hd..."> and <footer class="ft"> blocks with the shared
ax- chrome, links css/acg-arch-chrome.css and js/acg-arch-chrome.js, and leaves page content,
head metadata, JSON-LD, forms and tracking untouched. Idempotent: pages that already carry
the ax- chrome are skipped. Byte-frozen pages and the homepage are excluded.

Usage:
  python3 scripts/arch-chrome-migrate.py            # dry run, prints counts
  python3 scripts/arch-chrome-migrate.py --write    # rewrite files
"""
from __future__ import annotations

import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
SKIP_DIRS = ("_internal/", "drafts/", "node_modules/", ".github/", "src/")
EXCLUDE = {
    "index.html",  # homepage carries its own architectural chrome
    "impact-windows-palm-beach.html",  # byte-frozen
    "commercial-glazier-near-me-west-palm-beach/index.html",  # byte-frozen
    "location-template-snippet.html",  # template fragment, not a page
}
CSS_TAG = '<link rel="stylesheet" href="/css/acg-arch-chrome.css?v=20261001">'
JS_TAG = '<script src="/js/acg-arch-chrome.js?v=20261001" defer></script>'

HEADER = (
    '<header class="ax-nav">'
    '<a class="ax-logo" href="/" aria-label="American Commercial Glass home">'
    '<img src="/images/acg-logo-nav@2x.png" alt="ACG" width="169" height="36" decoding="async">'
    '<span>AMERICAN<br>COMMERCIAL GLASS</span></a>'
    '<div class="ax-nav-right">'
    '<a class="ax-btn-plans" href="/send-plans.html">Send Us Plans</a>'
    '<button class="ax-menu-button" type="button" aria-expanded="false" aria-controls="ax-navigation">'
    'Menu<span class="ax-menu-icon" aria-hidden="true"><i></i><i></i></span></button>'
    '</div></header>'
    '<div id="ax-navigation" class="ax-navigation" hidden>'
    '<nav aria-label="Main navigation">'
    '<a href="/portfolio.html"><span>01</span>The work</a>'
    '<a href="/services.html"><span>02</span>The services</a>'
    '<a href="/about.html"><span>03</span>The company</a>'
    '<a href="/qualifications.html"><span>04</span>Qualifications</a>'
    '<a href="/manufacturers.html"><span>05</span>Manufacturers</a>'
    '<a href="/locations.html"><span>06</span>Coverage</a>'
    '<a href="/resources.html"><span>07</span>Resources</a>'
    '<a href="/contact.html"><span>08</span>Your project</a>'
    '</nav>'
    '<div class="ax-menu-footer"><span>Florida / Division 08</span>'
    '<!--email_off--><a href="mailto:connor@acglass.com">connor@acglass.com</a><!--/email_off-->'
    '<a href="tel:+17724867711">(772) 486-7711</a></div>'
    '</div>'
)

FOOTER = (
    '<footer class="ax-footer">'
    '<div class="ax-footer-brand">'
    '<a class="ax-logo" href="/"><img src="/images/acg-logo-nav@2x.png" width="169" height="36" alt="American Commercial Glass" loading="lazy" decoding="async"></a>'
    '\n<p>Owner-operated commercial glazing. Florida HQ in West Palm Beach, offices in Naples and Tampa.</p>\n'
    '<p>700 S Rosemary Ave #204, West Palm Beach, FL 33401</p>'
    '<!--email_off--><a href="mailto:connor@acglass.com">connor@acglass.com</a><!--/email_off-->'
    '<a href="tel:+17724867711">(772) 486-7711</a>'
    '</div>'
    '<div class="ax-footer-col"><h2>Work</h2>'
    '<a href="/atlantic-fields-golf-house.html">Atlantic Fields</a>'
    '<a href="/gulfside-twelve.html">Gulfside Twelve</a>'
    '<a href="/wild-blue-clubhouse.html">Wild Blue Clubhouse</a>'
    '<a href="/eau-palm-beach-resort.html">Eau Palm Beach Resort</a>'
    '<a href="/cudjoe-key-fire-station.html">Cudjoe Key Fire Station</a>'
    '<a href="/case-study-haines-city-eoc.html">Haines City EOC</a>'
    '<a href="/portfolio.html">Full portfolio</a>'
    '</div>'
    '<div class="ax-footer-col"><h2>Services</h2>'
    '<a href="/commercial-storefront-systems.html">Storefront</a>'
    '<a href="/curtainwall-systems.html">Curtainwall</a>'
    '<a href="/window-wall-systems.html">Window wall</a>'
    '<a href="/impact-windows-doors.html">Impact windows &amp; doors</a>'
    '<a href="/multi-slide-bifold-doors.html">Moving glass walls</a>'
    '<a href="/fire-rated-glass-systems.html">Fire-rated glazing</a>'
    '<a href="/automatic-entrance-systems.html">Automatic entrances</a>'
    '<a href="/interior-glass-partitions.html">Interior glass</a>'
    '</div>'
    '<div class="ax-footer-col"><h2>Company</h2>'
    '<a href="/about.html">About ACG</a>'
    '<a href="/leadership.html">Leadership</a>'
    '<a href="/qualifications.html">Qualifications</a>'
    '<a href="/manufacturers.html">Manufacturer partners</a>'
    '<a href="/partners.html">Working with GCs</a>'
    '<a href="/testimonials.html">Testimonials</a>'
    '<a href="/careers.html">Careers</a>'
    '</div>'
    '<div class="ax-footer-col"><h2>Explore</h2>'
    '<a href="/government-public-sector-glazing.html">Government &amp; public sector</a>'
    '<a href="/locations.html">All service areas</a>'
    '<a href="/resources.html">Technical resources</a>'
    '<a href="/blog/">Articles</a>'
    '<a href="/news/">News</a>'
    '<a href="/scope-engine.html">Scope engine</a>'
    '<a href="/contact.html">Contact</a>'
    '<a href="/send-plans.html">Send Us Plans</a>'
    '</div>'
    '<div class="ax-footer-legal">'
    '\n<span>© 2026 American Commercial Glass, Inc. · FL CGC #1531993 · Woman-owned business, WBENC certification in progress</span>\n'
    '<span class="compliance-line" style="display:block;margin-top:6px;font-size:12px;color:#8892a3">Woman-owned business, WBENC certification in progress. FL CGC 1531993. UEI QTQYMLLL9PS4.</span>\n'
    '<span><a href="/privacy-policy.html">Privacy</a> &middot; <a href="/terms-of-use.html">Terms</a> &middot; <a href="/security-policy.html">Security</a> &middot; Not affiliated with AGC Inc or ACG Glass &amp; Metals</span>'
    '</div>'
    '</footer>'
)

HEADER_RE = re.compile(r'<header class="hd(?: [^"]*)?">.*?</header>|<header class="nav" id="siteNav">.*?</header>', re.S)
FOOTER_RE = re.compile(r'<footer class="ft">.*?</footer>|<footer class="footer">.*?</footer>|<footer>.*?</footer>', re.S)
STYLESHEET_RE = re.compile(r'<link[^>]+rel=["\']stylesheet["\'][^>]*>', re.I)


def migrate(text: str) -> tuple[str, str]:
    if 'class="ax-nav"' in text:
        return text, "already"
    if 'http-equiv="refresh' in text.lower():
        return text, "stub"
    h = HEADER_RE.search(text)
    f = FOOTER_RE.search(text)
    if not h:
        return text, "no-legacy-chrome"
    if f:
        text = text[: f.start()] + FOOTER + text[f.end():]
    else:
        # Header but no footer (spec sheets): add the shared footer at the end of the body.
        body_end = text.lower().rfind("</body>")
        text = text[:body_end] + FOOTER + "\n" + text[body_end:]
    h = HEADER_RE.search(text)
    assert h, "header vanished after footer replacement"
    text = text[: h.start()] + HEADER + text[h.end():]
    head_end = text.lower().find("</head>")
    sheets = [m for m in STYLESHEET_RE.finditer(text) if m.start() < head_end]
    at = sheets[-1].end() if sheets else head_end
    text = text[:at] + "\n" + CSS_TAG + text[at:]
    body_end = text.lower().rfind("</body>")
    text = text[:body_end] + JS_TAG + "\n" + text[body_end:]
    leftovers = [k for k in ("hd-mobile", "hd-burger", 'class="hd"', 'class="ft"') if k in text]
    return text, ("migrated-with-leftovers:" + ",".join(leftovers)) if leftovers else "migrated"


def main() -> int:
    write = "--write" in sys.argv
    counts: dict[str, int] = {}
    examples: dict[str, str] = {}
    for path in sorted(ROOT.rglob("*.html")):
        rel = path.relative_to(ROOT).as_posix()
        if rel.startswith(SKIP_DIRS) or rel in EXCLUDE:
            continue
        old = path.read_text(encoding="utf-8")
        new, status = migrate(old)
        counts[status] = counts.get(status, 0) + 1
        examples.setdefault(status, rel)
        if write and new != old:
            path.write_text(new, encoding="utf-8")
    for status, n in sorted(counts.items(), key=lambda kv: -kv[1]):
        print(f"{n:5} {status}  e.g. {examples[status]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
