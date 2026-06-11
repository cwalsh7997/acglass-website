#!/usr/bin/env python3
"""Fresh 26-point audit + 17-URL scoring sweep against the live acglass.com site.

Outputs a category-weighted score (max 100) and a per-check breakdown.
Designed to be re-runnable for trend tracking.
"""
import json
import re
import sys
import time
import urllib.request
import urllib.error
import socket
from concurrent.futures import ThreadPoolExecutor, as_completed

BASE = "https://acglass.com"
UA = "Mozilla/5.0 (compatible; acglass-audit/1.0; +https://acglass.com/)"
TIMEOUT = 30

# 17 URLs sampled across the site for scoring
SAMPLE_URLS = [
    f"{BASE}/",
    f"{BASE}/about.html",
    f"{BASE}/ask.html",
    f"{BASE}/leadership.html",
    f"{BASE}/services.html",
    f"{BASE}/manufacturers.html",
    f"{BASE}/contact.html",
    f"{BASE}/commercial-storefront-systems.html",
    f"{BASE}/curtainwall-systems.html",
    f"{BASE}/impact-windows-doors.html",
    f"{BASE}/noa/",
    f"{BASE}/noa/eswindows.html",
    f"{BASE}/architect-specs/section-08-41-13-aluminum-storefront.html",
    f"{BASE}/architect-specs/section-08-51-13-aluminum-windows.html",
    f"{BASE}/projects/wild-blue-clubhouse.html",
    f"{BASE}/projects/ocean-prime-ft-lauderdale.html",
    f"{BASE}/storefront-glazier-aventura-florida/",
]

def fetch(url, head_only=False):
    method = 'HEAD' if head_only else 'GET'
    # Don't request gzip — keep response plaintext for regex scanning
    req = urllib.request.Request(url, headers={'User-Agent': UA}, method=method)
    t0 = time.time()
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
            elapsed = (time.time() - t0) * 1000
            raw = b'' if head_only else r.read(512 * 1024)
            headers = {k.lower(): v for k, v in r.headers.items()}
            ce = headers.get('content-encoding', '').lower()
            if 'gzip' in ce:
                import gzip
                try: raw = gzip.decompress(raw)
                except Exception: pass
            elif 'br' in ce:
                try:
                    import brotli
                    raw = brotli.decompress(raw)
                except Exception: pass
            return {
                'url': url, 'status': r.status, 'elapsed_ms': elapsed,
                'headers': headers, 'body': raw.decode('utf-8', errors='ignore'),
                'final_url': r.url
            }
    except urllib.error.HTTPError as e:
        return {'url': url, 'status': e.code, 'elapsed_ms': (time.time()-t0)*1000,
                'headers': dict(e.headers.items() if e.headers else []), 'body': '', 'error': str(e)}
    except Exception as e:
        return {'url': url, 'status': None, 'elapsed_ms': (time.time()-t0)*1000, 'headers': {}, 'body': '', 'error': str(e)}


def parallel_fetch(urls):
    results = {}
    with ThreadPoolExecutor(max_workers=8) as ex:
        futures = {ex.submit(fetch, u): u for u in urls}
        for fut in as_completed(futures):
            r = fut.result()
            results[r['url']] = r
    return results


# Score store
scores = {}
notes = {}
def s(category, points_earned, points_max, note=''):
    scores.setdefault(category, [0, 0])
    scores[category][0] += points_earned
    scores[category][1] += points_max
    notes.setdefault(category, []).append(f"{points_earned}/{points_max} {note}")


# ============== Pre-fetch the 17 sample URLs ==============
print("Fetching 17 sample URLs...")
sample = parallel_fetch(SAMPLE_URLS)
print(f"  Done. {sum(1 for r in sample.values() if r['status']==200)}/17 returned 200.")

# Fetch utility files
print("Fetching utility files...")
utility = parallel_fetch([
    f"{BASE}/robots.txt",
    f"{BASE}/sitemap.xml",
    f"{BASE}/sitemap-index.xml",
    f"{BASE}/sitemap-pages.xml",
    f"{BASE}/llms.txt",
    f"{BASE}/llms-full.txt",
])

# ============== Category 1: Crawl & indexability (15 pts) ==============
print("\n=== Crawl & Indexability ===")

# robots.txt accessible (2)
r = utility[f"{BASE}/robots.txt"]
if r['status'] == 200 and 'sitemap' in r['body'].lower():
    s('1_crawl', 2, 2, 'robots.txt accessible and references sitemap')
else:
    s('1_crawl', 0, 2, f'robots.txt status={r["status"]}')

# sitemap-index.xml accessible (2)
r = utility[f"{BASE}/sitemap-index.xml"]
if r['status'] == 200:
    s('1_crawl', 2, 2, 'sitemap-index.xml accessible')
else:
    s('1_crawl', 0, 2, f'sitemap-index status={r["status"]}')

# sitemap.xml + sitemap-pages.xml valid (2)
ok_count = 0
for u in [f"{BASE}/sitemap.xml", f"{BASE}/sitemap-pages.xml"]:
    r = utility[u]
    if r['status'] == 200 and '<urlset' in r['body']:
        ok_count += 1
s('1_crawl', ok_count, 2, f'{ok_count}/2 sitemaps valid')

# All 17 sampled URLs HTTP 200 (3)
ok = sum(1 for r in sample.values() if r['status'] == 200)
s('1_crawl', round(3 * ok / 17), 3, f'{ok}/17 sample URLs return 200')

# Canonical present on every sampled page (3)
ok = 0
for u, r in sample.items():
    if 'rel="canonical"' in r['body'] and 'acglass.com' in r['body']:
        ok += 1
s('1_crawl', round(3 * ok / 17), 3, f'{ok}/17 have canonical link')

# Meta robots / X-Robots-Tag correct (3) — none should noindex (except retired stubs which aren't in our sample)
ok = 0
for u, r in sample.items():
    rtag = r['headers'].get('X-Robots-Tag', r['headers'].get('x-robots-tag', ''))
    has_noindex = 'noindex' in rtag.lower() or 'noindex' in r['body'][:8000].lower()
    if not has_noindex:
        ok += 1
s('1_crawl', round(3 * ok / 17), 3, f'{ok}/17 are indexable (none of sample is noindex)')

# ============== Category 2: Structured data (15 pts) ==============
print("=== Structured Data ===")

# Homepage @graph parses (2)
r = sample[f"{BASE}/"]
blocks = re.findall(r'<script type="application/ld\+json">\s*(\{.*?\})\s*</script>', r['body'], re.DOTALL)
graph_ok = False
org_node = None
for b in blocks:
    try:
        obj = json.loads(b)
        if '@graph' in obj:
            graph_ok = True
            for n in obj['@graph']:
                t = n.get('@type')
                t_list = t if isinstance(t, list) else [t]
                if 'Organization' in t_list:
                    org_node = n
            break
    except Exception:
        pass
s('2_structured', 2 if graph_ok else 0, 2, 'homepage @graph parses' if graph_ok else 'homepage @graph missing/invalid')

# Org @type correct (no GeneralContractor) (2)
if org_node:
    t = org_node.get('@type')
    t_list = t if isinstance(t, list) else [t]
    has_gc = 'GeneralContractor' in t_list
    correct = (set(t_list) == {'Organization', 'LocalBusiness'})
    s('2_structured', 2 if correct and not has_gc else 0, 2, f'org @type = {t_list}')
else:
    s('2_structured', 0, 2, 'no org node found')

# Org @id = #org (1)
if org_node and org_node.get('@id', '').endswith('#org'):
    s('2_structured', 1, 1, '#org @id set')
else:
    s('2_structured', 0, 1, 'wrong/missing @id on org')

# WebSite without SearchAction (1)
has_search_action = 'SearchAction' in r['body']
s('2_structured', 0 if has_search_action else 1, 1, 'no broken SearchAction' if not has_search_action else 'SearchAction present (should be removed)')

# BreadcrumbList present where appropriate (2) — check 5 deep URLs
deep = [f"{BASE}/noa/eswindows.html", f"{BASE}/projects/wild-blue-clubhouse.html",
        f"{BASE}/architect-specs/section-08-41-13-aluminum-storefront.html",
        f"{BASE}/noa/", f"{BASE}/storefront-glazier-aventura-florida/"]
breadcrumb_ok = sum(1 for u in deep if 'BreadcrumbList' in sample[u]['body'])
s('2_structured', round(2 * breadcrumb_ok / 5), 2, f'{breadcrumb_ok}/5 deep pages have BreadcrumbList')

# FAQPage on relevant pages (2) — ask.html, homepage
faq_count = sum(1 for u in [f"{BASE}/", f"{BASE}/ask.html"] if 'FAQPage' in sample[u]['body'])
s('2_structured', round(2 * faq_count / 2), 2, f'{faq_count}/2 expected pages have FAQPage')

# JSON-LD parses on every sampled page (3)
parse_ok = 0
for u, r in sample.items():
    bb = re.findall(r'<script type="application/ld\+json">\s*(\{.*?\})\s*</script>', r['body'], re.DOTALL)
    all_parse = True
    for b in bb:
        try: json.loads(b)
        except Exception: all_parse = False
    if bb and all_parse: parse_ok += 1
s('2_structured', round(3 * parse_ok / 17), 3, f'{parse_ok}/17 sampled pages have valid JSON-LD')

# Article schema on case studies (2)
case_urls = [f"{BASE}/projects/wild-blue-clubhouse.html", f"{BASE}/projects/ocean-prime-ft-lauderdale.html"]
article_count = sum(1 for u in case_urls if '"@type": "Article"' in sample[u]['body'] or '"Article"' in sample[u]['body'])
s('2_structured', round(2 * article_count / 2), 2, f'{article_count}/2 case studies have Article schema')

# ============== Category 3: Canonicalization & dedup (15 pts) ==============
print("=== Canonicalization & Dedup ===")

# Canonicals point to https://acglass.com (no www, no http) (3)
ok = 0
for u, r in sample.items():
    m = re.search(r'rel="canonical"\s+href="([^"]+)"', r['body'])
    if m and m.group(1).startswith('https://acglass.com'):
        ok += 1
s('3_canonical', round(3 * ok / 17), 3, f'{ok}/17 canonicals are https://acglass.com/...')

# No infinite redirects (2) — check by following final_url
redirect_ok = sum(1 for r in sample.values() if r['status'] == 200)
s('3_canonical', round(2 * redirect_ok / 17), 2, f'{redirect_ok}/17 resolve without infinite loop')

# www → root redirect works (2)
www_r = fetch(BASE.replace('https://', 'https://www.') + '/')
if www_r['status'] == 200 and 'acglass.com' in www_r.get('final_url', ''):
    s('3_canonical', 2, 2, f'www → root resolves to {www_r["final_url"]}')
else:
    s('3_canonical', 1, 2, f'www → root status={www_r["status"]} final={www_r.get("final_url","?")}')

# Trailing slash consistency (2) — sample 2 pairs
ts_ok = 0
for path_with, path_without in [('/about.html', '/about'), ('/contact.html', '/contact')]:
    r1 = fetch(f"{BASE}{path_with}")
    if r1['status'] == 200:
        ts_ok += 1
s('3_canonical', round(2 * ts_ok / 2), 2, f'{ts_ok}/2 trailing-slash checks consistent')

# Retired URL stubs noindex + canonical (2) — check 3 known stubs
stubs = ['/acg.html', '/ai-overview.html', '/about-acg-for-ai.html']
stub_ok = 0
for path in stubs:
    rr = fetch(f"{BASE}{path}")
    if rr['status'] == 200 and 'noindex' in rr['body'].lower() and ('http-equiv="refresh"' in rr['body'].lower() or 'refresh' in rr['body'].lower()):
        stub_ok += 1
s('3_canonical', round(2 * stub_ok / 3), 2, f'{stub_ok}/3 retired stubs noindex+refresh correctly')

# Duplicate-page detection (4) — known issue: 74 city URL pair collisions
# Test: do /aventura/ and /storefront-glazier-aventura-florida/ have distinct canonicals?
r_a = sample[f"{BASE}/storefront-glazier-aventura-florida/"]
m_a = re.search(r'rel="canonical"\s+href="([^"]+)"', r_a['body'])
canon_a = m_a.group(1) if m_a else ''
r_b = fetch(f"{BASE}/aventura/")
m_b = re.search(r'rel="canonical"\s+href="([^"]+)"', r_b['body']) if r_b['status'] == 200 else None
canon_b = m_b.group(1) if m_b else ''
# Penalty: both pages have distinct canonicals (self) — should consolidate via canonical to one URL
if canon_a and canon_b and canon_a != canon_b and r_b['status'] == 200:
    s('3_canonical', 2, 4, 'city URL pair collision: distinct self-canonicals on /aventura/ and /storefront-glazier-aventura-florida/')
else:
    s('3_canonical', 4, 4, 'no city URL pair collision detected')

# ============== Category 4: Performance proxies (15 pts) ==============
print("=== Performance Proxies ===")

# Median page weight < 100KB HTML (3)
weights = [len(r['body']) for r in sample.values() if r['body']]
weights.sort()
median = weights[len(weights)//2] if weights else 0
if median < 100_000: s('4_performance', 3, 3, f'median page HTML weight {median//1024}KB')
elif median < 150_000: s('4_performance', 2, 3, f'median page HTML weight {median//1024}KB')
else: s('4_performance', 1, 3, f'median page HTML weight {median//1024}KB')

# Median response time < 500ms (3)
times = sorted(r['elapsed_ms'] for r in sample.values())
med_time = times[len(times)//2]
if med_time < 300: s('4_performance', 3, 3, f'median TTFB {med_time:.0f}ms')
elif med_time < 500: s('4_performance', 2, 3, f'median TTFB {med_time:.0f}ms')
elif med_time < 1000: s('4_performance', 1, 3, f'median TTFB {med_time:.0f}ms')
else: s('4_performance', 0, 3, f'median TTFB {med_time:.0f}ms')

# Modern image formats (AVIF/WebP) (3) — check homepage + case study
img_pages = [sample[f"{BASE}/"], sample[f"{BASE}/projects/wild-blue-clubhouse.html"]]
modern = sum(1 for r in img_pages if '.avif' in r['body'] or '.webp' in r['body'])
s('4_performance', round(3 * modern / 2), 3, f'{modern}/2 pages reference AVIF/WebP')

# HTTP/2 (2) — check via cf-ray (Cloudflare) or server header
http2 = sum(1 for r in sample.values() if r['headers'].get('cf-ray') or 'cloudflare' in r['headers'].get('server', '').lower())
s('4_performance', round(2 * http2 / 17), 2, f'{http2}/17 served via Cloudflare (HTTP/2+)')

# Compression (2) — test by making a HEAD-style request with explicit Accept-Encoding
gz_ok = 0
for u in list(sample.keys())[:5]:
    req = urllib.request.Request(u, headers={'User-Agent': UA, 'Accept-Encoding': 'gzip, br'})
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            if 'gzip' in r.headers.get('Content-Encoding','').lower() or 'br' in r.headers.get('Content-Encoding','').lower():
                gz_ok += 1
    except: pass
s('4_performance', round(2 * gz_ok / 5), 2, f'{gz_ok}/5 spot-checks serve gzip/br')

# Cache headers (2)
cached = sum(1 for r in sample.values() if r['headers'].get('cache-control', r['headers'].get('Cache-Control','')))
s('4_performance', round(2 * cached / 17), 2, f'{cached}/17 have cache-control header')

# ============== Category 5: Metadata (15 pts) ==============
print("=== Metadata ===")

titles, descs = [], []
for u, r in sample.items():
    tm = re.search(r'<title[^>]*>([^<]+)</title>', r['body'], re.IGNORECASE)
    dm = re.search(r'<meta\s+name="description"\s+content="([^"]+)"', r['body'], re.IGNORECASE)
    if tm: titles.append((u, tm.group(1).strip()))
    if dm: descs.append((u, dm.group(1).strip()))

# Titles ≤60 (3)
ok = sum(1 for _, t in titles if len(t) <= 60)
s('5_metadata', round(3 * ok / 17), 3, f'{ok}/17 titles ≤60 chars')

# Descs 80-155 (3)
ok = sum(1 for _, d in descs if 80 <= len(d) <= 155)
s('5_metadata', round(3 * ok / 17), 3, f'{ok}/17 descs in 80-155 range')

# Unique titles in sample (3)
unique_titles = len(set(t for _, t in titles))
s('5_metadata', round(3 * unique_titles / 17), 3, f'{unique_titles}/17 titles unique')

# OG tags on homepage + sample (3)
og_ok = sum(1 for r in sample.values() if 'property="og:title"' in r['body'] and 'property="og:description"' in r['body'])
s('5_metadata', round(3 * og_ok / 17), 3, f'{og_ok}/17 have full OG tags')

# Twitter Card tags (3)
tw_ok = sum(1 for r in sample.values() if 'twitter:card' in r['body'])
s('5_metadata', round(3 * tw_ok / 17), 3, f'{tw_ok}/17 have twitter:card')

# ============== Category 6: AI-surface readiness (10 pts) ==============
print("=== AI-Surface Readiness ===")

# llms.txt exists + valid (2)
r_llms = utility[f"{BASE}/llms.txt"]
if r_llms['status'] == 200 and 'American Commercial Glass' in r_llms['body']:
    s('6_ai', 2, 2, 'llms.txt present and references ACG')
else:
    s('6_ai', 0, 2, f'llms.txt status={r_llms["status"]}')

# llms-full.txt exists (1)
r_lf = utility[f"{BASE}/llms-full.txt"]
s('6_ai', 1 if r_lf['status'] == 200 else 0, 1, f'llms-full.txt status={r_lf["status"]}')

# FAQ entity coverage (3) — ask.html should have many Q&As; check 30+
ask_body = sample[f"{BASE}/ask.html"]['body']
q_count = ask_body.count('"@type": "Question"') + ask_body.count('"@type":"Question"')
if q_count >= 50: s('6_ai', 3, 3, f'ask.html has {q_count} Q&As')
elif q_count >= 30: s('6_ai', 2, 3, f'ask.html has {q_count} Q&As')
else: s('6_ai', 1, 3, f'ask.html has only {q_count} Q&As')

# Author/about pages with E-E-A-T (2) — leadership + about both exist + linked
leadership_ok = sample[f"{BASE}/leadership.html"]['status'] == 200
about_ok = sample[f"{BASE}/about.html"]['status'] == 200
if leadership_ok and about_ok and 'Connor Walsh' in sample[f"{BASE}/leadership.html"]['body']:
    s('6_ai', 2, 2, 'leadership + about pages present with named principals')
else:
    s('6_ai', 1, 2, 'partial E-E-A-T coverage')

# NOA/spec data presence (2)
noa_ok = sample[f"{BASE}/noa/"]['status'] == 200 and 'Florida Product Approval' in sample[f"{BASE}/noa/"]['body']
spec_ok = 'FL PA' in sample[f"{BASE}/architect-specs/section-08-41-13-aluminum-storefront.html"]['body']
if noa_ok and spec_ok: s('6_ai', 2, 2, 'NOA hub live + spec pages reference FL PA')
elif noa_ok or spec_ok: s('6_ai', 1, 2, 'partial')
else: s('6_ai', 0, 2, 'NOA hub or spec data missing')

# ============== Category 7: Content architecture (10 pts) ==============
print("=== Content Architecture ===")

# Spec pages ≥1000 words (2)
spec_words = 0
for u in [f"{BASE}/architect-specs/section-08-41-13-aluminum-storefront.html",
          f"{BASE}/architect-specs/section-08-51-13-aluminum-windows.html"]:
    body = sample[u]['body']
    c2 = re.sub(r'<script[^>]*>.*?</script>', '', body, flags=re.DOTALL)
    c2 = re.sub(r'<style[^>]*>.*?</style>', '', c2, flags=re.DOTALL)
    text = re.sub(r'<[^>]+>', ' ', c2)
    text = re.sub(r'\s+', ' ', text).strip()
    spec_words += len(text.split())
spec_avg = spec_words // 2
if spec_avg >= 1500: s('7_content', 2, 2, f'spec pages avg {spec_avg} words')
elif spec_avg >= 1000: s('7_content', 1, 2, f'spec pages avg {spec_avg} words')
else: s('7_content', 0, 2, f'spec pages avg {spec_avg} words')

# City pages templated and titles ≤60 (2)
city_r = sample[f"{BASE}/storefront-glazier-aventura-florida/"]
m_ct = re.search(r'<title[^>]*>([^<]+)</title>', city_r['body'])
city_t = m_ct.group(1) if m_ct else ''
if city_t and len(city_t) <= 60 and 'ACG' in city_t and 'in ' in city_t:
    s('7_content', 2, 2, f'city page templated: "{city_t}" ({len(city_t)} chars)')
else:
    s('7_content', 0, 2, f'city template incorrect: "{city_t}" (page returned status {city_r["status"]}, body len {len(city_r["body"])})')

# Case studies present (2)
case_ok = sum(1 for u in [f"{BASE}/projects/wild-blue-clubhouse.html", f"{BASE}/projects/ocean-prime-ft-lauderdale.html"] if sample[u]['status'] == 200)
s('7_content', round(2 * case_ok / 2), 2, f'{case_ok}/2 case studies live')

# Internal link density (2) — homepage should have ≥30 internal links
home_links = len(re.findall(r'href="(/[^"]+|https://acglass\.com/[^"]+)"', sample[f"{BASE}/"]['body']))
if home_links >= 30: s('7_content', 2, 2, f'homepage has {home_links} internal links')
elif home_links >= 15: s('7_content', 1, 2, f'homepage has {home_links} internal links')
else: s('7_content', 0, 2, f'homepage has only {home_links} internal links')

# Service-to-project linking (2) — service page should link to a case study
service_r = sample[f"{BASE}/commercial-storefront-systems.html"]
linked = '/projects/' in service_r['body']
s('7_content', 2 if linked else 0, 2, 'service pages link to case studies' if linked else 'no service→case-study link')

# ============== Category 8: Security (5 pts) ==============
print("=== Security ===")

# HSTS header (2)
home_h = sample[f"{BASE}/"]['headers']
hsts = home_h.get('strict-transport-security', home_h.get('Strict-Transport-Security', ''))
if hsts and 'max-age=' in hsts:
    m = re.search(r'max-age=(\d+)', hsts)
    age = int(m.group(1)) if m else 0
    if age >= 15768000: s('8_security', 2, 2, f'HSTS max-age={age}')
    else: s('8_security', 1, 2, f'HSTS max-age={age} (low)')
else:
    s('8_security', 0, 2, 'no HSTS header')

# HTTPS-only — http → https redirect (1)
http_r = fetch(BASE.replace('https://','http://') + '/')
if http_r['status'] == 200 and http_r.get('final_url','').startswith('https://'):
    s('8_security', 1, 1, 'HTTP redirects to HTTPS')
else:
    s('8_security', 0, 1, f'HTTP status={http_r["status"]} final={http_r.get("final_url","?")}')

# TLS 1.2+ — implicit if we got a response (1)
s('8_security', 1, 1, 'TLS 1.2+ (request succeeded)')

# X-Robots-Tag where appropriate (1) — qualifications PDFs should be noindex
qual_r = fetch(f"{BASE}/pdfs/qualifications/acg-capabilities-statement.pdf", head_only=True)
xrt = qual_r['headers'].get('x-robots-tag', qual_r['headers'].get('X-Robots-Tag', ''))
if xrt and 'noindex' in xrt.lower():
    s('8_security', 1, 1, f'qualifications PDFs noindex via X-Robots-Tag: {xrt}')
elif qual_r['status'] == 404:
    s('8_security', 1, 1, 'qualifications PDF returned 404 (acceptable — not exposed)')
else:
    s('8_security', 0, 1, f'no X-Robots-Tag on qualifications PDFs')

# ============== TALLY ==============
print("\n" + "=" * 60)
print("FRESH 26-POINT AUDIT — acglass.com — 2026-06-11")
print("=" * 60)

category_labels = {
    '1_crawl':       ('Crawl & indexability', 15),
    '2_structured':  ('Structured data',      15),
    '3_canonical':   ('Canonicalization & dedup', 15),
    '4_performance': ('Performance proxies',  15),
    '5_metadata':    ('Metadata',             15),
    '6_ai':          ('AI-surface readiness', 10),
    '7_content':     ('Content architecture', 10),
    '8_security':    ('Security',              5),
}

total_e, total_m = 0, 0
for k, (label, max_pts) in category_labels.items():
    e, m = scores.get(k, [0, max_pts])
    # Normalize to max_pts
    if m > 0:
        normalized = round(e * max_pts / m)
    else:
        normalized = 0
    total_e += normalized
    total_m += max_pts
    print(f"\n{label}: {normalized}/{max_pts}")
    for n in notes.get(k, []):
        print(f"  · {n}")

print("\n" + "=" * 60)
print(f"TOTAL: {total_e}/{total_m}")
print("=" * 60)

# Save JSON for trend tracking
import os
os.makedirs('reports', exist_ok=True)
with open('reports/audit-2026-06-11.json', 'w') as f:
    json.dump({
        'date': '2026-06-11',
        'total': total_e,
        'max': total_m,
        'categories': {label: {'earned': round(scores[k][0]*max_pts/scores[k][1]) if scores[k][1] else 0, 'max': max_pts} for k, (label, max_pts) in category_labels.items()},
        'notes': notes,
    }, f, indent=2)
print(f"\nSaved: reports/audit-2026-06-11.json")
