# ESWindows `/products/eswindows` edge 301 - apply note

**Status: NOT ACTIVATED.** `activated` in `eswindows-products-path.json` is
`false`. Merging this note changes no routing. Applying it is a manual act in
the Cloudflare dashboard. This VM cannot apply Bulk Redirects.

## Why this is not a code deploy

`acglass.com` is GitHub Pages behind Cloudflare. Pages serves
`products/eswindows/index.html` as **HTTP 200** (soft meta-refresh + JS to
`/es-windows.html`). `vercel.json` already mirrors both permanent rules; that
file is an observed edge mirror, not a deploy mechanism. Other mirrored
redirects (for example Nashville/Alabama commercial-glazing pairs) **are** live
Cloudflare 301s. This pair is not.

Live probe on 2026-09-17:

| Request | Observed |
|---|---|
| `https://acglass.com/products/eswindows/` | HTTP 200, soft redirect body to `/es-windows.html` |
| `https://acglass.com/products/eswindows` | HTTP 301 to `/products/eswindows/` only |

Keep the HTML stub until the edge 301 is verified. A soft 200 is better than a
hard 404.

## Apply

Cloudflare dashboard → zone `acglass.com` → **Rules → Redirect Rules → Bulk
Redirects**. Add two rows. Do not mark this note activated until step Verify
passes.

| Source URL | Target URL | Status | Preserve query string | Subpath matching |
|---|---|---|---|---|
| `https://acglass.com/products/eswindows` | `https://acglass.com/es-windows.html` | 301 | on | off |
| `https://acglass.com/products/eswindows/` | `https://acglass.com/es-windows.html` | 301 | on | off |

## Verify

```
curl -sI https://acglass.com/products/eswindows | grep -iE '^(HTTP|location)'
curl -sI https://acglass.com/products/eswindows/ | grep -iE '^(HTTP|location)'
```

Expect one hop: `301` then `Location: https://acglass.com/es-windows.html` on
both. If the trailing-slash URL is still `200`, the origin HTML stub is still
winning and the Bulk Redirect is not applied (or is overridden).

After that live 301 is confirmed, set `"activated": true` in
`eswindows-products-path.json` and remove `products/eswindows/index.html` in a
follow-up. Not in this pass.
