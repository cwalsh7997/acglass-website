#!/usr/bin/env python3
"""scripts/seo-pulse.py — Nightly SEO/search-performance pulse.

Pulls:
  - GSC API: last-7-day clicks, impressions, CTR, avg position
            (i) totals
            (ii) per query-bucket: commercial glazing, eswindows, euro-wall, division 08, nashville
            (iii) top 20 pages by clicks
  - Bing Webmaster API: indexed-pages count + crawl errors

Appends a row to the 'Rankings' tab of the ACG SEO Ops Google Sheet.
Posts a 6-line WoW delta summary to Slack, flagging any metric moving >20%.

Required repo secrets (read via env):
  GSC_SA_JSON     — Google service-account JSON (multi-line; runner writes to /tmp/gsc-sa.json)
  BING_API_KEY    — Bing Webmaster API key
  SHEETS_SA_JSON  — Google service-account JSON for Sheets append
  SHEETS_ID       — target spreadsheet ID
  SLACK_WEBHOOK   — Slack incoming webhook URL

Missing-secret behavior: exits 1 with a clear message naming the missing secret.
Never hardcoded; never fabricated.
"""
import json
import os
import sys
import urllib.request
import urllib.error
from datetime import date, timedelta

PROPERTY = 'sc-domain:acglass.com'
GA_QUERY_BUCKETS = ['commercial glazing', 'eswindows', 'euro-wall', 'division 08', 'nashville']
BING_SITE = 'https://acglass.com/'

REQUIRED_SECRETS = ['GSC_SA_JSON', 'BING_API_KEY', 'SHEETS_SA_JSON', 'SHEETS_ID', 'SLACK_WEBHOOK']


def fail_missing(name):
    print(f"::error::Missing required secret '{name}'. Add it under Settings → Secrets and variables → Actions.", file=sys.stderr)
    print(f"Cannot run seo-pulse without {name}. Exiting 1.", file=sys.stderr)
    sys.exit(1)


def check_secrets():
    missing = [s for s in REQUIRED_SECRETS if not os.environ.get(s)]
    if missing:
        for m in missing:
            fail_missing(m)


def get_gsc_token(sa_json_str):
    """Mint an access token via the JWT bearer flow for GSC scope."""
    try:
        from google.oauth2 import service_account
        from googleapiclient.discovery import build
    except ImportError:
        print("::error::Missing python deps: google-api-python-client google-auth", file=sys.stderr)
        sys.exit(1)
    info = json.loads(sa_json_str)
    creds = service_account.Credentials.from_service_account_info(
        info, scopes=['https://www.googleapis.com/auth/webmasters.readonly']
    )
    return build('searchconsole', 'v1', credentials=creds, cache_discovery=False)


def fetch_gsc_window(svc, start, end, query_filter=None, dimensions=None, row_limit=20):
    body = {
        'startDate': start.isoformat(),
        'endDate': end.isoformat(),
        'rowLimit': row_limit,
    }
    if dimensions:
        body['dimensions'] = dimensions
    if query_filter:
        body['dimensionFilterGroups'] = [{
            'filters': [{'dimension': 'query', 'operator': 'contains', 'expression': query_filter}]
        }]
    resp = svc.searchanalytics().query(siteUrl=PROPERTY, body=body).execute()
    return resp


def sum_totals(rows):
    totals = {'clicks': 0, 'impressions': 0, 'position_sum': 0, 'n': 0}
    for r in rows or []:
        totals['clicks'] += r.get('clicks', 0)
        totals['impressions'] += r.get('impressions', 0)
        totals['position_sum'] += r.get('position', 0) * r.get('impressions', 1)
        totals['n'] += r.get('impressions', 1)
    if totals['impressions'] > 0:
        totals['ctr'] = totals['clicks'] / totals['impressions']
        totals['avg_position'] = totals['position_sum'] / max(totals['n'], 1)
    else:
        totals['ctr'] = 0.0
        totals['avg_position'] = 0.0
    return totals


def fetch_bing(api_key):
    """Bing Webmaster API: GetUrlInfo + GetCrawlIssues."""
    base = 'https://ssl.bing.com/webmaster/api.svc/json'
    out = {'indexed': None, 'crawl_errors': None}
    # GetUrlInfo for site root
    url = f'{base}/GetUrlInfo?siteUrl={urllib.parse.quote(BING_SITE)}&apikey={api_key}'
    try:
        req = urllib.request.Request(url, headers={'Accept': 'application/json'})
        with urllib.request.urlopen(req, timeout=30) as r:
            d = json.loads(r.read())
            out['indexed'] = d.get('d', {}).get('TotalIndexed')
    except Exception as e:
        out['indexed_error'] = str(e)
    # GetCrawlIssues
    url2 = f'{base}/GetCrawlIssues?siteUrl={urllib.parse.quote(BING_SITE)}&apikey={api_key}'
    try:
        req = urllib.request.Request(url2, headers={'Accept': 'application/json'})
        with urllib.request.urlopen(req, timeout=30) as r:
            d = json.loads(r.read())
            out['crawl_errors'] = len(d.get('d', []))
    except Exception as e:
        out['crawl_errors_error'] = str(e)
    return out


def append_to_sheet(sa_json_str, sheet_id, row_values):
    """Append a single row to the 'Rankings' tab."""
    try:
        from google.oauth2 import service_account
        from googleapiclient.discovery import build
    except ImportError:
        print("::error::Missing python deps: google-api-python-client google-auth", file=sys.stderr)
        sys.exit(1)
    info = json.loads(sa_json_str)
    creds = service_account.Credentials.from_service_account_info(
        info, scopes=['https://www.googleapis.com/auth/spreadsheets']
    )
    svc = build('sheets', 'v4', credentials=creds, cache_discovery=False)
    svc.spreadsheets().values().append(
        spreadsheetId=sheet_id,
        range='Rankings!A1',
        valueInputOption='USER_ENTERED',
        insertDataOption='INSERT_ROWS',
        body={'values': [row_values]}
    ).execute()


def slack_post(webhook, lines):
    payload = {'text': '\n'.join(lines)}
    data = json.dumps(payload).encode()
    req = urllib.request.Request(webhook, data=data, headers={'Content-Type': 'application/json'})
    try:
        urllib.request.urlopen(req, timeout=20).read()
    except Exception as e:
        print(f"::warning::Slack post failed: {e}", file=sys.stderr)


def pct_delta(curr, prev):
    if not prev: return None
    return (curr - prev) / prev * 100


def fmt_delta(d):
    if d is None: return 'n/a'
    flag = ' ⚠️' if abs(d) > 20 else ''
    return f"{d:+.1f}%{flag}"


def main():
    import urllib.parse
    globals()['urllib'].parse = urllib.parse
    check_secrets()
    
    today = date.today()
    end = today - timedelta(days=2)  # GSC has 2-3 day lag
    start = end - timedelta(days=6)
    prev_end = start - timedelta(days=1)
    prev_start = prev_end - timedelta(days=6)
    
    print(f"=== ACG SEO Pulse — {today.isoformat()} ===")
    print(f"Current window: {start} → {end}")
    print(f"Prior window:   {prev_start} → {prev_end}")
    
    # GSC
    svc = get_gsc_token(os.environ['GSC_SA_JSON'])
    curr = fetch_gsc_window(svc, start, end, row_limit=10000)
    prev = fetch_gsc_window(svc, prev_start, prev_end, row_limit=10000)
    curr_total = sum_totals(curr.get('rows', []))
    prev_total = sum_totals(prev.get('rows', []))
    
    # Per-bucket
    bucket_data = {}
    for bucket in GA_QUERY_BUCKETS:
        c = fetch_gsc_window(svc, start, end, query_filter=bucket, dimensions=['query'], row_limit=100)
        p = fetch_gsc_window(svc, prev_start, prev_end, query_filter=bucket, dimensions=['query'], row_limit=100)
        bucket_data[bucket] = (sum_totals(c.get('rows', [])), sum_totals(p.get('rows', [])))
    
    # Top 20 pages
    pages = fetch_gsc_window(svc, start, end, dimensions=['page'], row_limit=20)
    
    # Bing
    bing = fetch_bing(os.environ['BING_API_KEY'])
    
    # Build sheet row
    row = [
        today.isoformat(),
        f"{start}..{end}",
        curr_total['clicks'],
        curr_total['impressions'],
        f"{curr_total['ctr']*100:.2f}%",
        f"{curr_total['avg_position']:.2f}",
        prev_total['clicks'],
        bing.get('indexed') or '',
        bing.get('crawl_errors') if bing.get('crawl_errors') is not None else '',
    ]
    for bucket, (c, p) in bucket_data.items():
        row.extend([bucket, c['clicks'], c['impressions']])
    
    append_to_sheet(os.environ['SHEETS_SA_JSON'], os.environ['SHEETS_ID'], row)
    
    # Slack summary (6 lines exactly)
    clicks_d = pct_delta(curr_total['clicks'], prev_total['clicks'])
    impr_d = pct_delta(curr_total['impressions'], prev_total['impressions'])
    
    top_page = ''
    if pages.get('rows'):
        top_page = pages['rows'][0]['keys'][0]
    
    lines = [
        f"*ACG SEO Pulse · {start.strftime('%b %d')} – {end.strftime('%b %d')}*",
        f"Clicks: {curr_total['clicks']} ({fmt_delta(clicks_d)} WoW) · Impr: {curr_total['impressions']} ({fmt_delta(impr_d)} WoW)",
        f"CTR: {curr_total['ctr']*100:.2f}% · Avg pos: {curr_total['avg_position']:.2f}",
        f"Bing indexed: {bing.get('indexed','n/a')} · Crawl errors: {bing.get('crawl_errors','n/a')}",
        "Buckets · " + " · ".join(f"{b}: {c['clicks']}" for b, (c, _) in bucket_data.items()),
        f"Top page: {top_page or 'n/a'}",
    ]
    slack_post(os.environ['SLACK_WEBHOOK'], lines)
    
    for l in lines:
        print(l)
    return 0


if __name__ == '__main__':
    sys.exit(main())
