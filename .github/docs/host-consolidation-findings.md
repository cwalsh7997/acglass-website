# Duplicate-host indexing investigation: www.acglass.com

Investigated 2026-08-28. All redirect traces below are live `curl -sSI` output taken at that
time. Redirects are served by Cloudflare (`server: cloudflare` on every hop), which is
**outside this repository** -- nothing in this repo can change them.

## 1. The problem, as Google reports it

`sc-domain:acglass.com`, 2026-05-30 to 2026-08-25, `dataState=final`, dimension `page`,
`aggregationType=byPage`:

| Reported page | Clicks | Impressions | CTR | Avg position |
|---|---|---|---|---|
| `https://acglass.com/` | 126 | 4,995 | 2.52% | 25.86 |
| `http://www.acglass.com/` | **73** | **2,425** | 3.01% | **6.11** |
| `https://www.acglass.com/` | 0 | 88 | 0% | 6.47 |

Site totals for the window: **778 clicks, 102,660 impressions** across 1,030 page rows.
The www host therefore accounts for **73 clicks (9.4% of all site clicks)** and
**2,513 impressions (2.4%)**.

This is not a reporting artifact. In a domain property GSC keys `page` rows by the URL
**Google selected as canonical**. `http://www.acglass.com/` carrying clicks means Google
selected the http-www form as the canonical homepage for a share of homepage queries, and
served it. Note also that the www form ranks at position 6.1 while the apex form averages
25.9 -- the two hosts are competing on different query sets, and the higher-intent
homepage queries are landing on the wrong host.

## 2. Confirmed redirect chains and hop counts

### `http://www.acglass.com/` -- TWO hops

```
$ curl -sSI -L http://www.acglass.com/
HTTP/1.1 301 Moved Permanently
Location: https://www.acglass.com/          <- hop 1 (http-www -> https-www)
server: cloudflare
HTTP/2 301
location: https://acglass.com/              <- hop 2 (https-www -> https-apex)
server: cloudflare
HTTP/2 200                                  <- final
server: cloudflare
```

### `https://www.acglass.com/` -- ONE hop

```
$ curl -sSI -L https://www.acglass.com/
HTTP/2 301
location: https://acglass.com/
HTTP/2 200
```

### `http://acglass.com/` (non-www) -- ONE hop

```
$ curl -sSI -L http://acglass.com/
HTTP/1.1 301 Moved Permanently
Location: https://acglass.com/
HTTP/2 200
```

### `https://acglass.com/` -- terminal, `HTTP/2 200`

The behaviour is identical on deep paths, so it is a host-level rule and not a root-only
quirk:

```
$ curl -sSI -L http://www.acglass.com/about.html
HTTP/1.1 301 -> https://www.acglass.com/about.html
HTTP/2 301   -> https://acglass.com/about.html
HTTP/2 200
```

Path and scheme are preserved correctly on every hop. Every hop is a **301** (permanent),
not a 302. Summary:

| Entry URL | Hops to final | Chain |
|---|---|---|
| `http://www.acglass.com/` | **2** | http-www -> https-www -> https-apex |
| `https://www.acglass.com/` | 1 | https-www -> https-apex |
| `http://acglass.com/` | 1 | http-apex -> https-apex |
| `https://acglass.com/` | 0 | 200 |

## 3. Repo grep for hardcoded `www.acglass.com`

```
$ grep -rIn "www\.acglass\.com" --exclude-dir=.git .
./vercel.json:353:          "value": "www.acglass.com"
```

**Exactly one occurrence in the entire repository, and it is correct as written.** It is
the `has.host` *match condition* of the www-to-apex redirect rule in `vercel.json`:

```json
{
  "source": "/:path*",
  "has": [{ "type": "host", "value": "www.acglass.com" }],
  "destination": "https://acglass.com/:path*",
  "permanent": true
}
```

The string is the hostname being redirected **from**. Rewriting it to `acglass.com` would
make the rule match the apex and 301 the apex to itself -- an infinite redirect loop that
would take the whole site down. It has been left untouched deliberately.

Checks that came back clean, i.e. **zero** www references to fix:

| Surface checked | `www.acglass.com` hits |
|---|---|
| `<link rel="canonical">` (all 1,580 HTML files) | 0 |
| `sitemap*.xml` `<loc>` and `<image:loc>` | 0 |
| JSON-LD blocks (`@id`, `url`, `sameAs`, `logo`, `image`) | 0 |
| `hreflang` alternates (only `/same` relative pairs exist) | 0 |
| Internal `href` / `src` attributes | 0 |
| Open Graph / Twitter card URLs | 0 |
| `robots.txt` `Sitemap:` lines | 0 |
| `CNAME` (contains `acglass.com`) | 0 |

Also checked and clean: no `http://acglass.com` or `http://www.acglass.com` absolute
references anywhere in shipped content (the single `http://acglass.com/...` string in the
repo is a test fixture in `.github/scripts/tests/test_seo_measure.py`, not served output).

**Conclusion: this repo is not the source of the duplicate-host indexing.** Every
canonical, sitemap entry, JSON-LD identifier and internal link already declares the
`https://acglass.com` apex form. There were no www references to correct.

## 4. Is the two-hop www chain the reason Google still indexes the www host?

It is a **contributing factor and the only fixable one visible, but it is unlikely to be a
hard blocker on its own.** Being precise about this matters:

**Why the chain is a real problem.** Google's own guidance is to point redirects at the
final destination and avoid chains. The specific damage in this chain is that hop 1 lands
`Googlebot` on `https://www.acglass.com/`, which is *itself* a redirect rather than a
`200`. Canonical consolidation for the www host therefore requires Google to crawl and
resolve two separate URLs across two separate crawl events before it reaches a page with a
`rel=canonical`. Each extra hop adds crawl latency and another chance for the signal to be
scheduled late or dropped. Chained 301s are also treated more weakly than a direct 301.

**Why the chain alone probably is not the whole story.** Two hops is well within what
Google follows and consolidates routinely, so a two-hop chain does not normally prevent
consolidation outright. The corroborating evidence is the `https://www.acglass.com/` row:
it sits behind a clean **single** hop and still shows 88 impressions. A one-hop www URL
appearing in the index at all means the persistence of the www host is partly just
long-lived legacy indexing inertia -- historical external links, and GSC's habit of
retaining a previously-selected canonical in domain-property reporting for a long time
after the redirect is in place. The `http://www` form carrying 73 clicks with 2,425
impressions and a strong position 6.1 is consistent with a well-established legacy URL
that has accumulated external links, not with a freshly created duplicate.

**Net assessment:** collapsing the chain to one hop is correct, cheap, and removes the only
technical impediment under anyone's control. It should be expected to *accelerate*
consolidation rather than to flip it overnight; the www rows will decay over subsequent
crawl cycles rather than vanish.

## 5. Recommended fix -- Cloudflare, not this repo

The redirects are served by Cloudflare. **No change was attempted here**, and no change to
this repository can achieve the fix. Recommended change for the owner:

1. **Create a Cloudflare Redirect Rule** (Rules -> Redirect Rules) named e.g.
   `www to apex, single hop`:
   - **When incoming requests match:** `Hostname equals www.acglass.com`
   - **Then:** Static/Dynamic redirect to
     `concat("https://acglass.com", http.request.uri.path)` (append
     `http.request.uri.query` handling so query strings survive)
   - **Status code:** `301` Permanent
   - **Preserve query string:** enabled
2. **Give that rule higher precedence than the HTTPS upgrade.** The current two-hop
   behaviour exists because *Always Use HTTPS* (SSL/TLS -> Edge Certificates) fires first
   on `http://www`, upgrading scheme only and leaving the host as `www`; the www-to-apex
   rule then fires on the second request. A Redirect Rule that matches `http` **and**
   `https` on the www hostname and rewrites scheme **and** host in one response makes
   `http://www.acglass.com/*` a single 301 straight to `https://acglass.com/*`. In practice
   this means either ordering the redirect rule above the HTTPS upgrade, or scoping
   *Always Use HTTPS* so it does not pre-empt the www hostname.
3. **Keep the existing apex rule.** `http://acglass.com -> https://acglass.com` is already
   a correct single hop and must stay.
4. **Do not delete `vercel.json`'s www rule.** It is the correct fallback if traffic ever
   stops passing through Cloudflare. It costs nothing while Cloudflare answers first.

Verification the owner can run immediately after the change -- this must show exactly one
`301` line and one `200` line, with `location:` pointing at the apex:

```
curl -sSI -L http://www.acglass.com/            # expect 1 hop
curl -sSI -L http://www.acglass.com/about.html  # expect 1 hop, path preserved
curl -sSI -L "http://www.acglass.com/?a=b"      # expect 1 hop, query preserved
```

Follow-up in Search Console: use URL Inspection on `http://www.acglass.com/` to request a
recrawl once the single hop is live, then watch the `http://www.acglass.com/` page row
decay in the `sc-domain:acglass.com` property. Expect weeks, not days.

This file lives at `.github/docs/host-consolidation-findings.md`. GitHub Pages does not
serve `.github/`, so it is not publicly fetchable. Do not move it back under the deploy root.
