#!/usr/bin/env python3
"""T1.2 — Regenerate city/service templates with the exact pattern from the spec.

Title: '{Service} in {City}, FL | ACG' (+ ' — 48-Hr Bids' if total ≤ 60)
Desc:  'Licensed FL glazing subcontractor (CGC #1531993). {Service} in {City} — impact-rated systems, bonded, 48-hour scope letters.' (adjust word order only as needed for 80-155 range)

H1 stays untouched. Service comes from the H1 service term.
"""
import os
import re
from pathlib import Path

SAFE = "abcdefghijklmnopqrstuvwxyz0123456789-"

TITLE_RE = re.compile(r'(<title[^>]*>)([^<]+)(</title>)', re.IGNORECASE)
DESC_RE = re.compile(r'(<meta\s+name=["\']description["\']\s+content=")([^"]+)(")', re.IGNORECASE)
OG_TITLE_RE = re.compile(r'(<meta\s+property=["\']og:title["\']\s+content=")([^"]+)(")', re.IGNORECASE)
OG_DESC_RE = re.compile(r'(<meta\s+property=["\']og:description["\']\s+content=")([^"]+)(")', re.IGNORECASE)
TW_TITLE_RE = re.compile(r'(<meta\s+name=["\']twitter:title["\']\s+content=")([^"]+)(")', re.IGNORECASE)
TW_DESC_RE = re.compile(r'(<meta\s+name=["\']twitter:description["\']\s+content=")([^"]+)(")', re.IGNORECASE)
H1_RE = re.compile(r'<h1[^>]*>(.*?)</h1>', re.IGNORECASE | re.DOTALL)


# Service-name shorteners for cases where the H1 service term doesn't fit the 60-char title.
# These map verbose H1 services to a tighter SEO-equivalent term. Truthful, not invented.
SERVICE_SHORTENERS = [
    (r'^Hurricane Impact Windows and Doors$', 'Impact Windows & Doors'),
    (r'^Hurricane Impact Windows And Doors$', 'Impact Windows & Doors'),
    (r'^Assisted Living & Senior Living Commercial Glazing$', 'Senior Living Glazing'),
    (r'^Assisted Living &amp; Senior Living Commercial Glazing$', 'Senior Living Glazing'),
    (r'^Commercial Storefront Installation$', 'Storefront Installation'),
    (r'^Automotive Showroom Commercial Glazing$', 'Showroom Glazing'),
    (r'^Automotive Showroom Glazing$', 'Showroom Glazing'),
    (r'^Hospital and Healthcare Glazing$', 'Healthcare Glazing'),
    (r'^Hotel and Hospitality Glazing$', 'Hotel Glazing'),
    (r'^Multifamily Residential Glazing$', 'Multifamily Glazing'),
    (r'^Restaurant Storefront and Bi-fold Glazing$', 'Restaurant Glazing'),
    (r'^Office and Commercial Tenant Glazing$', 'Office Glazing'),
    (r'^Mixed-Use Commercial Glazing$', 'Mixed-Use Glazing'),
    (r'^Retail Storefront Glazing$', 'Retail Glazing'),
    (r'^Class A Office Building Glazing$', 'Class A Office Glazing'),
    (r'^Government and Municipal Glazing$', 'Government Glazing'),
    (r'^K-12 School Commercial Glazing$', 'School Glazing'),
    (r'^Higher Education Commercial Glazing$', 'Higher Ed Glazing'),
    (r'^All Glass Entrances$', 'All-Glass Entrances'),
    (r'^All-Glass Entrance Installation$', 'All-Glass Entrances'),
    (r'^Glass Railings$', 'Glass Railings'),
]

def shorten_service(service):
    """Apply known shorteners. Returns short form if matched, else original."""
    for pat, repl in SERVICE_SHORTENERS:
        if re.match(pat, service, re.IGNORECASE):
            return repl
    return service


def title_case(s):
    """Title-case a city/service string while preserving 'and'/'of' lowercase except at start."""
    minor = {'and', 'of', 'the', 'in'}
    words = s.split()
    out = []
    for i, w in enumerate(words):
        if i > 0 and w.lower() in minor:
            out.append(w.lower())
        else:
            out.append(w[:1].upper() + w[1:])
    return ' '.join(out)


def extract_service_city(h1):
    """Return (service, city) or (None, None) if not parseable."""
    h1 = re.sub(r'<[^>]+>', '', h1).strip()
    h1 = re.sub(r'\s+', ' ', h1)
    h1 = h1.rstrip('.').rstrip(',').strip()
    
    # Pattern 1: '<Service> in <City>, Florida' or '<Service> in <City>, FL'
    m = re.match(r'^(.+?)\s+in\s+(.+?),\s*(?:Florida|FL)$', h1, re.IGNORECASE)
    if m:
        return title_case(m.group(1)), title_case(m.group(2))
    
    # Pattern 1b: '<Service> Near <City>, FL' or '<Service> Near <City>'
    m = re.match(r'^(.+?)\s+[Nn]ear\s+(.+?),\s*(?:Florida|FL)$', h1, re.IGNORECASE)
    if m:
        return title_case(m.group(1)), title_case(m.group(2))
    m = re.match(r'^(.+?)\s+[Nn]ear\s+(.+?)$', h1, re.IGNORECASE)
    if m:
        return title_case(m.group(1)), title_case(m.group(2))
    
    # Pattern 2: '<Service> in <City>'
    m = re.match(r'^(.+?)\s+in\s+(.+?)$', h1, re.IGNORECASE)
    if m:
        return title_case(m.group(1)), title_case(m.group(2))
    
    # Pattern 3: '<Service> — <Neighborhood> <City>' (em-dash neighborhoods)
    m = re.match(r'^(.+?)\s+[—–-]\s+(.+?)$', h1)
    if m:
        return title_case(m.group(1)), title_case(m.group(2))
    
    # Pattern 4: '<Service> <City>, Florida'
    m = re.match(r'^(.+?)\s+(.+?),\s*(?:Florida|FL)$', h1, re.IGNORECASE)
    if m:
        # Heuristic: if right side is 1-3 words, it's the city
        right = m.group(2).strip()
        if 1 <= len(right.split()) <= 3:
            return title_case(m.group(1)), title_case(right)
    
    return None, None


def slug_to_city(slug):
    """Convert a URL slug like 'boca-raton' to 'Boca Raton'."""
    return ' '.join(w[:1].upper() + w[1:] for w in slug.split('-'))


def build_title(service, city):
    """Build title using exact spec pattern."""
    base = f"{service} in {city}, FL | ACG"
    with_suffix = base.replace(' | ACG', ' | ACG — 48-Hr Bids')
    if len(with_suffix) <= 60:
        return with_suffix
    if len(base) <= 60:
        return base
    # Try to drop the FL state suffix
    no_fl = f"{service} in {city} | ACG"
    if len(no_fl) <= 60:
        return no_fl
    return None  # cannot fit


def build_desc(service, city):
    """Build description, target 80-155 chars."""
    # Default
    d = f"Licensed FL glazing subcontractor (CGC #1531993). {service} in {city} — impact-rated systems, bonded, 48-hour scope letters."
    if 80 <= len(d) <= 155:
        return d
    if len(d) > 155:
        # Shorter form
        d2 = f"Licensed FL glazing sub (CGC #1531993). {service} in {city} — impact-rated, bonded, 48-hour scope letters."
        if 80 <= len(d2) <= 155:
            return d2
        # Even shorter
        d3 = f"FL glazing sub CGC #1531993. {service} in {city} — impact-rated, bonded, 48-hour scope letters."
        if 80 <= len(d3) <= 155:
            return d3
        return None
    if len(d) < 80:
        # Pad with city-specific framing
        d4 = f"Licensed FL commercial glazing subcontractor (CGC #1531993). {service} in {city} — impact-rated systems, bonded, 48-hour scope letters."
        if 80 <= len(d4) <= 155:
            return d4
        return d  # accept under-80 in extreme case (shouldn't happen with our wording)


def is_city_service_page(path: Path) -> bool:
    """Heuristic: is this a city/service page that should get the template?"""
    s = str(path)
    if s.startswith('commercial-glazier-') and '-' in s.split('/')[0][len('commercial-glazier-'):]:
        # /commercial-glazier-<city>/ — but skip non-city slugs
        slug = s.split('/')[0][len('commercial-glazier-'):]
        # Skip topic-like slugs
        TOPIC_HINTS = ['bid-process', 'questions-to-ask', 'sba-set', 'florida-2026', 'near-me']
        if any(h in slug for h in TOPIC_HINTS):
            # "near-me" types are still city pages
            if 'near-me' in slug:
                return True
            return False
        return True
    if s.startswith('storefront-glazier-') and s.endswith('/index.html'):
        return True
    # Locality directories /<city>/<service>/index.html or /<city>/index.html
    parts = s.split('/')
    if len(parts) == 3 and parts[2] == 'index.html':
        # /city/service/index.html — accept if H1 has a service+city pattern (checked at extraction time)
        return True
    if len(parts) == 2 and parts[1] == 'index.html':
        # /city/index.html — accept if H1 parses
        return True
    return False


# Skip cornerstone topics that LOOK like city pages but aren't
COMMENTARY_SLUGS = {
    'acg-glass-florida', 'ai-overview', 'about-acg-for-ai',
    'florida-commercial-glass-statistics-2026',
    'florida-aluminum-tariff-impact-2026',
    'agi-glass-perplexity-test',
    'best-glazing-subcontractor-florida',
    'best-storefront-contractor-florida',
}


def process(path: Path):
    """Returns ('skipped'|'ok'|'failed', detail)."""
    parts = str(path).split('/')
    top = parts[0]
    if top in COMMENTARY_SLUGS:
        return 'skipped', f'commentary slug: {top}'
    
    if not is_city_service_page(path):
        return 'skipped', f'not city/service: {path}'
    
    try:
        c = path.read_text()
    except UnicodeDecodeError:
        return 'skipped', 'unicode'
    
    if 'http-equiv="refresh"' in c.lower() and len(c) < 3000:
        return 'skipped', 'redirect stub'
    
    h1m = H1_RE.search(c)
    if not h1m:
        return 'skipped', 'no h1'
    h1 = h1m.group(1)
    h1_text = re.sub(r'<[^>]+>', '', h1).strip()
    h1_text = re.sub(r'\s+', ' ', h1_text)
    
    service, city = extract_service_city(h1_text)
    if not service or not city:
        return 'failed', f'unparsed H1: {h1_text[:80]}'
    
    # Special handling: skip pages where the "city" is actually a Florida/state-level term
    if city.lower() in ('florida', 'fl', 'tennessee', 'tn'):
        return 'failed', f'city resolved to state: {h1_text[:80]}'
    
    title = build_title(service, city)
    if not title:
        # Try shortening service
        short_service = shorten_service(service)
        if short_service != service:
            title = build_title(short_service, city)
            if title:
                service = short_service
        if not title:
            return 'failed', f'title too long: {service} in {city}'
    
    desc = build_desc(service, city)
    if not desc:
        # Try shortening service for desc too
        short_service = shorten_service(service)
        if short_service != service:
            desc = build_desc(short_service, city)
        if not desc:
            return 'failed', f'desc out of range: {service} in {city}'
    
    new = c
    new_title = title
    new_desc = desc
    
    tm = TITLE_RE.search(new)
    if tm:
        new = new[:tm.start(2)] + new_title + new[tm.end(2):]
    
    dm = DESC_RE.search(new)
    if dm:
        new = new[:dm.start(2)] + new_desc + new[dm.end(2):]
    
    # Realign og/twitter
    for r in (OG_TITLE_RE, TW_TITLE_RE):
        m = r.search(new)
        if m: new = new[:m.start(2)] + new_title + new[m.end(2):]
    for r in (OG_DESC_RE, TW_DESC_RE):
        m = r.search(new)
        if m: new = new[:m.start(2)] + new_desc + new[m.end(2):]
    
    path.write_text(new)
    return 'ok', f'{service} | {city} → t={len(new_title)} d={len(new_desc)}'


# Walk targets from /tmp/t12-targets.txt
targets = [Path(l.strip()) for l in open('/tmp/t12-targets.txt') if l.strip()]
results = {'ok': 0, 'skipped': 0, 'failed': 0}
failures = []
longest_title = 0
longest_desc = 0
for p in targets:
    if not p.exists(): continue
    status, detail = process(p)
    results[status] += 1
    if status == 'failed':
        failures.append((str(p), detail))
    elif status == 'ok':
        # Re-read to record longest
        c = p.read_text()
        tm = TITLE_RE.search(c)
        dm = DESC_RE.search(c)
        if tm: longest_title = max(longest_title, len(tm.group(2)))
        if dm: longest_desc = max(longest_desc, len(dm.group(2)))

print(f"\n=== T1.2 SUMMARY ===")
print(f"OK:      {results['ok']}")
print(f"Skipped: {results['skipped']}")
print(f"Failed:  {results['failed']}")
print(f"Longest title written: {longest_title}")
print(f"Longest desc written:  {longest_desc}")
print(f"\nFailures (could not template):")
for p, d in failures[:30]:
    print(f"  {p}: {d}")

# Append to report
with open('reports/t12-templater-2026-06-11.txt','w') as f:
    f.write(f"T1.2 templater run — 2026-06-11\n\n")
    f.write(f"OK:      {results['ok']}\n")
    f.write(f"Skipped: {results['skipped']}\n")
    f.write(f"Failed:  {results['failed']}\n")
    f.write(f"Longest title written: {longest_title}\n")
    f.write(f"Longest desc written:  {longest_desc}\n\n")
    f.write(f"Failures:\n")
    for p, d in failures:
        f.write(f"  {p}: {d}\n")
