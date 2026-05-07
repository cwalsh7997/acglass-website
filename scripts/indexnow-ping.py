#!/usr/bin/env python3
"""IndexNow ping helper.

Usage:
  python3 scripts/indexnow-ping.py                    # submit all URLs in sitemap.xml
  python3 scripts/indexnow-ping.py path1.html path2   # submit specific URLs

Pings: Bing, Yandex, IndexNow.org (federates to Naver, Seznam, Yep).
Run after pushing new content. Bing typically indexes within minutes.
"""
import sys, os, re, json, urllib.request, urllib.error

KEY = "q7kv6cmi125pbq5u7h7trgv3noxpnm3w"
HOST = "acglass.com"
KEY_LOC = f"https://{HOST}/{KEY}.txt"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def collect_urls():
    if len(sys.argv) > 1:
        urls = []
        for a in sys.argv[1:]:
            a = a.lstrip("/")
            if a.startswith("http"):
                urls.append(a)
            else:
                urls.append(f"https://{HOST}/{a}")
        return urls
    sitemap = os.path.join(ROOT, "sitemap.xml")
    with open(sitemap) as f:
        sm = f.read()
    urls = re.findall(r"<loc>(https?://[^<]+)</loc>", sm)
    urls = [
        u.replace("http://acglass.com", "https://acglass.com")
         .replace("https://www.acglass.com", "https://acglass.com")
        for u in urls
    ]
    return sorted(set(urls))


def ping(name, endpoint, payload):
    req = urllib.request.Request(
        endpoint,
        data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json; charset=utf-8"},
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return r.status, r.read()[:200].decode("utf-8", errors="replace")
    except urllib.error.HTTPError as e:
        return e.code, str(e)[:200]
    except Exception as e:
        return "ERR", str(e)[:200]


def main():
    urls = collect_urls()
    print(f"IndexNow: submitting {len(urls)} URLs")
    payload = {"host": HOST, "key": KEY, "keyLocation": KEY_LOC, "urlList": urls}
    for name, ep in [
        ("Bing", "https://www.bing.com/indexnow"),
        ("Yandex", "https://yandex.com/indexnow"),
        ("IndexNow.org", "https://api.indexnow.org/indexnow"),
    ]:
        code, msg = ping(name, ep, payload)
        print(f"  {name}: {code} {msg[:80]}")


if __name__ == "__main__":
    main()
