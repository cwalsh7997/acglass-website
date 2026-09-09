# Security headers, CSP and cache policy

Required by D4 obligation 6: "Security headers, CSP, and cache policy are
delivered at the Cloudflare layer. Document the exact values and where they are
configured." No such document existed.

Measured from the live response, not from intent: `curl -D - https://acglass.com/`
on 2026-09-09.

## Delivery chain

    Cloudflare  ->  Fastly  ->  GitHub Pages

Confirmed by the response carrying `server: cloudflare`, `via: 1.1 varnish` with
`x-served-by: cache-sjc10048-SJC`, and `x-github-request-id`. This matches D4's
"hand-authored static HTML on GitHub Pages behind Fastly and Cloudflare".

Two of the three layers are not configurable from this repo. Fastly and GitHub
Pages emit what they emit; everything below is set at Cloudflare.

## What is actually being sent

| header | value | verdict |
|---|---|---|
| `strict-transport-security` | `max-age=15768000; includeSubDomains` | present, see note |
| `x-content-type-options` | `nosniff` | correct |
| `cache-control` | `max-age=600` | 10 minutes, reasonable for a static marketing site |
| `access-control-allow-origin` | `*` | permissive for an HTML document |
| `alt-svc` | `h3=":443"; ma=86400` | HTTP/3 available |

**HSTS note.** 15,768,000 seconds is 182 days. The HSTS preload list requires a
minimum of 31,536,000, one year, plus the `preload` directive. As configured the
site is protected but is not preload-eligible.

## What is NOT being sent

| header | consequence |
|---|---|
| `content-security-policy` | Named explicitly in D4 obligation 6 and absent. No restriction on script or style origins. |
| `x-frame-options` / CSP `frame-ancestors` | Nothing prevents the site being framed. Clickjacking on the lead forms is the practical risk. |
| `referrer-policy` | Full URLs leak to third parties on outbound clicks. |
| `permissions-policy` | Camera, microphone, geolocation and payment are not explicitly denied. |

## Suggested Cloudflare Transform Rule

Response Header Transform on `acglass.com/*`. Static-site safe. **Not applied:
Cloudflare configuration is outside this repo and I have no access to it.**

    referrer-policy:    strict-origin-when-cross-origin
    x-frame-options:    SAMEORIGIN
    permissions-policy: camera=(), microphone=(), geolocation=(), payment=()

CSP needs a measured pass before it ships, not a guessed one. The site loads
Google Tag Manager, Google Fonts and inline JSON-LD, and a policy written without
enumerating those first will break the analytics or the fonts. Report-only mode
first, read the violation reports, then enforce.

## Related edge configuration in this repo

- `cloudflare-410-worker.js` returns HTTP 410 for retired WordPress spam URLs and
  for `/acg-nashville-office-opening`. GitHub Pages cannot emit 410 itself, so
  this is the edge treatment.
- `workers/dealer-portal-api/wrangler.toml` is the dealer portal API worker.
