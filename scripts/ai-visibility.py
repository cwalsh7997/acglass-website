#!/usr/bin/env python3
"""scripts/ai-visibility.py — Monthly AI-visibility audit.

Runs 10 fixed prompts through 3 AI engines with web-search/grounding enabled:
  - Perplexity Sonar API
  - Gemini API with grounding
  - OpenAI Responses (web search)

For each (engine, prompt) pair:
  - engine, ACG-named (Y/N), cited URL (first acglass.com URL in citations, or '')

Logs to AI-Citations tab of the ACG SEO Ops sheet + Slack summary.

Required secrets:
  PPLX_API_KEY, GEMINI_API_KEY, OPENAI_API_KEY, SHEETS_SA_JSON, SHEETS_ID, SLACK_WEBHOOK
"""
import json
import os
import sys
import urllib.request
import urllib.error
from datetime import date

PROMPTS = [
    "best commercial glazing contractor in Tampa",
    "who installs ESWindows in Florida",
    "Euro-Wall installer near Naples",
    "NOA for ES-7000",
    "Division 08 subcontractor Florida",
    "commercial glazing West Palm Beach",
    "restaurant glazing contractor Florida",
    "impact storefront installer Miami",
    "Nashville commercial glazing",
    "who is American Commercial Glass",
]

REQUIRED_SECRETS = ['PPLX_API_KEY', 'GEMINI_API_KEY', 'OPENAI_API_KEY',
                    'SHEETS_SA_JSON', 'SHEETS_ID', 'SLACK_WEBHOOK']

ACG_TOKENS = ['american commercial glass', 'acglass.com', 'acglass', 'ACG ']


def fail_missing(name):
    print(f"::error::Missing required secret '{name}'. Add it under Settings → Secrets and variables → Actions.", file=sys.stderr)
    sys.exit(1)


def check_secrets():
    for s in REQUIRED_SECRETS:
        if not os.environ.get(s):
            fail_missing(s)


def http_json(url, headers, body=None, method='POST', timeout=120):
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read())


def query_perplexity(prompt):
    """Perplexity Sonar API. Returns (text, citations[])."""
    try:
        d = http_json(
            'https://api.perplexity.ai/chat/completions',
            headers={
                'Authorization': f"Bearer {os.environ['PPLX_API_KEY']}",
                'Content-Type': 'application/json',
            },
            body={
                'model': 'sonar',
                'messages': [
                    {'role': 'system', 'content': 'Answer in 1-3 sentences. Cite sources.'},
                    {'role': 'user', 'content': prompt},
                ],
            }
        )
        text = d.get('choices', [{}])[0].get('message', {}).get('content', '')
        citations = d.get('citations') or d.get('search_results') or []
        urls = []
        for c in citations:
            if isinstance(c, str):
                urls.append(c)
            elif isinstance(c, dict):
                urls.append(c.get('url', '') or c.get('link', ''))
        return text, [u for u in urls if u]
    except Exception as e:
        return f"[error: {e}]", []


def query_gemini(prompt):
    """Gemini API with Google Search grounding."""
    try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={os.environ['GEMINI_API_KEY']}"
        body = {
            'contents': [{'parts': [{'text': prompt}]}],
            'tools': [{'google_search': {}}],
        }
        d = http_json(url, headers={'Content-Type': 'application/json'}, body=body)
        cands = d.get('candidates', [])
        if not cands:
            return '[no candidate]', []
        cand = cands[0]
        parts = cand.get('content', {}).get('parts', [])
        text = ''.join(p.get('text', '') for p in parts)
        # Grounding metadata
        urls = []
        gm = cand.get('groundingMetadata', {})
        chunks = gm.get('groundingChunks', [])
        for ch in chunks:
            web = ch.get('web', {})
            uri = web.get('uri') or web.get('url') or ''
            if uri:
                urls.append(uri)
        return text, urls
    except Exception as e:
        return f"[error: {e}]", []


def query_openai(prompt):
    """OpenAI Responses API with web_search tool."""
    try:
        d = http_json(
            'https://api.openai.com/v1/responses',
            headers={
                'Authorization': f"Bearer {os.environ['OPENAI_API_KEY']}",
                'Content-Type': 'application/json',
            },
            body={
                'model': 'gpt-4o-mini',
                'input': prompt,
                'tools': [{'type': 'web_search_preview'}],
            }
        )
        # Output: list of messages and tool calls
        output = d.get('output', [])
        text_parts = []
        urls = []
        for item in output:
            if item.get('type') == 'message':
                for c in item.get('content', []):
                    if c.get('type') == 'output_text':
                        text_parts.append(c.get('text', ''))
                        # Annotations carry URL citations
                        for ann in c.get('annotations', []):
                            if ann.get('type') == 'url_citation':
                                urls.append(ann.get('url', ''))
        return ''.join(text_parts), [u for u in urls if u]
    except Exception as e:
        return f"[error: {e}]", []


def named(text):
    lc = text.lower()
    return any(tok.lower() in lc for tok in ACG_TOKENS)


def first_acg_citation(urls):
    for u in urls:
        if 'acglass.com' in u:
            return u
    return ''


def append_sheet(sa_json_str, sheet_id, rows):
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
        range='AI-Citations!A1',
        valueInputOption='USER_ENTERED',
        insertDataOption='INSERT_ROWS',
        body={'values': rows}
    ).execute()


def slack_post(webhook, lines):
    payload = {'text': '\n'.join(lines)}
    req = urllib.request.Request(webhook, data=json.dumps(payload).encode(),
                                 headers={'Content-Type': 'application/json'})
    try:
        urllib.request.urlopen(req, timeout=20).read()
    except Exception as e:
        print(f"::warning::Slack post failed: {e}", file=sys.stderr)


def main():
    check_secrets()
    today = date.today().isoformat()
    results = []  # for sheet
    summary = {'PPLX': [0, 0], 'GEMINI': [0, 0], 'OPENAI': [0, 0]}  # [acg_named, total]
    print(f"=== ACG AI Visibility — {today} ===")
    for prompt in PROMPTS:
        for engine_name, fn in [('PPLX', query_perplexity), ('GEMINI', query_gemini), ('OPENAI', query_openai)]:
            text, urls = fn(prompt)
            is_named = named(text)
            cited = first_acg_citation(urls)
            row = [today, engine_name, prompt, 'Y' if is_named else 'N', cited, (text or '')[:240].replace('\n', ' ')]
            results.append(row)
            summary[engine_name][1] += 1
            if is_named:
                summary[engine_name][0] += 1
            print(f"  {engine_name:6s} | {'Y' if is_named else 'N'} | {prompt[:40]:40s} | {cited[:60]}")
    
    append_sheet(os.environ['SHEETS_SA_JSON'], os.environ['SHEETS_ID'], results)
    
    lines = [
        f"*ACG AI Visibility · {today}*",
        f"PPLX:   {summary['PPLX'][0]}/{summary['PPLX'][1]} prompts cite ACG",
        f"GEMINI: {summary['GEMINI'][0]}/{summary['GEMINI'][1]} prompts cite ACG",
        f"OPENAI: {summary['OPENAI'][0]}/{summary['OPENAI'][1]} prompts cite ACG",
        f"Full log: AI-Citations tab of the ACG SEO Ops sheet",
    ]
    slack_post(os.environ['SLACK_WEBHOOK'], lines)
    for l in lines:
        print(l)
    return 0


if __name__ == '__main__':
    sys.exit(main())
