# ACG Dealer Portal - Phase 1

This directory powers the public dealer-application flow on acglass.com.

## What's here

| File | Purpose |
| --- | --- |
| `../become-a-dealer.html` | Public-facing application form (in repo root so it's `acglass.com/become-a-dealer`) |
| `dealer.css` | Supplemental styles layered on top of `/css/style.css` |
| `dealer.js` | Form submit handler - posts to the Worker if configured, falls back to mailto |
| `thanks.html` | Confirmation page after a successful submission |
| `login.html` | "Coming soon" stub for the Phase 2 dealer portal |
| `admin.html` | Internal applications viewer (gated by an admin token in localStorage) |
| `../workers/dealer-portal-api/` | Cloudflare Worker + D1 schema that backs the API |

## How it fits together

```
Visitor                                  acglass.com (GitHub Pages, Cloudflare)
  ├── visits /become-a-dealer.html ──→  static HTML/CSS/JS rendered
  └── submits the form                  │
                                        └── dealer.js POSTs JSON to →
                                            ┌────────────────────────────────────┐
                                            │ Cloudflare Worker                  │
                                            │ acg-dealer-portal-api              │
                                            │   POST /api/applications           │
                                            │   GET  /api/applications  (admin)  │
                                            │   PATCH /api/applications/:id      │
                                            └─────────────┬──────────────────────┘
                                                          ↓
                                                    Cloudflare D1
                                                    (acg-dealer-portal)
                                                          ↓
                                            (optional) Resend → email connor@acglass.com
```

If the Worker URL isn't configured on the page, `dealer.js` falls back to opening
the visitor's email client with a prefilled mailto - so leads still reach Connor
regardless of backend state. This is the same pattern as the existing
`contact.html` and `send-plans.html` forms.

## Deploying the Worker

Prerequisites: Node + a Cloudflare account that owns acglass.com.

```bash
# From repo root
cd workers/dealer-portal-api
npm install -g wrangler          # one-time
wrangler login                   # browser-based OAuth into your Cloudflare account

# Create the D1 database - copy the printed database_id into wrangler.toml.
wrangler d1 create acg-dealer-portal

# Apply the schema.
wrangler d1 execute acg-dealer-portal --file=./schema.sql

# Set the admin bearer token. Use any long random string - paste it into
# /dealer/admin.html when prompted. It's stored in your browser's localStorage,
# never in the repo.
wrangler secret put ADMIN_TOKEN

# (Optional) Enable email notifications via Resend (https://resend.com).
# Without this, applications are still saved - you'll see them on the admin page.
wrangler secret put RESEND_API_KEY

# Deploy.
wrangler deploy
```

Wrangler will print a URL like
`https://acg-dealer-portal-api.<your-account>.workers.dev`. That's your API base.

## Wiring the site to the Worker

Once the Worker is deployed, point the site's pages at it. The simplest way is
a single inline script tag at the top of `become-a-dealer.html` and
`dealer/admin.html`:

```html
<script>window.ACG_DEALER_API = "https://acg-dealer-portal-api.<your-account>.workers.dev";</script>
```

Add it just inside `<head>`, before `dealer.js` loads. Both pages also accept a
`<meta name="acg-dealer-api" content="...">` tag if that's cleaner for you.

When you bind a custom subdomain like `api.acglass.com` later, swap the URL.
Nothing else changes.

## Testing locally

Static pages can be previewed with the existing PowerShell script in the repo root:

```powershell
.\preview.ps1
# then open http://localhost:8000/become-a-dealer.html
```

Without the Worker URL configured, the form will mailto-fallback on submit.
That's the pre-deploy expected behavior.

For end-to-end Worker testing:

```bash
cd workers/dealer-portal-api
wrangler d1 execute acg-dealer-portal --local --file=./schema.sql
wrangler dev
# In another terminal:
curl -s -X POST http://localhost:8787/api/applications \
  -H "Content-Type: application/json" \
  -d '{"company":"Test Co","contact_name":"Test","email":"t@example.com","phone":"5551234","address":"1 Test Way","years_in_business":"4-10","manufacturers":"ESWindows","annual_volume":"$50k-$250k"}'
```

Expected: `{"ok":true,"id":"<uuid>"}`. Then list with the admin token:

```bash
curl -s http://localhost:8787/api/applications -H "Authorization: Bearer <your-token>"
```

## Verification checklist (Phase 1)

After deploying:

- [ ] Submit a real application from an incognito window. Confirm a row appears
      on `acglass.com/dealer/admin.html` after pasting your admin token.
- [ ] If Resend is configured, confirm `connor@acglass.com` receives an email.
- [ ] Submit a deliberately bad payload (empty company). Expect a 400 response
      and a friendly "fill in: company" message on the form.
- [ ] Try `acglass.com/dealer/admin.html` without a token → token gate appears.
- [ ] Approve and reject an application from the admin page → table updates.
- [ ] Confirm the rest of acglass.com is unchanged and still deploying via
      GitHub Pages exactly as before. The new Worker is independent of the
      existing `cloudflare-410-worker.js`.

## What's NOT in Phase 1

Per `~/.claude/plans/i-am-a-distributor-moonlit-dawn.md`:

- Dealer logins. `dealer/login.html` is currently a "rolling out soon" stub.
- CSV → ACG-branded PDF generation (Phase 3).
- Welcome / password-reset email templates (Phase 4).
- Top-nav integration on the rest of acglass.com (Phase 4).
- Cloudflare Turnstile on the public form (Phase 4) - Phase 1 ships with a
  honeypot only. If volume spam appears, add Turnstile before public traffic.

## Operational notes

- **Two Workers, one site.** This deploys a new Worker (`acg-dealer-portal-api`)
  alongside the existing `cloudflare-410-worker.js` (which handles spam URL
  filtering on `acglass.com/*`). They're independent. Don't merge them - the
  spam filter is on every page, this Worker only handles `/api/*`.
- **Admin token lives in your browser only.** It's stored in localStorage on the
  device(s) you visit `dealer/admin.html` from. To revoke, run
  `wrangler secret put ADMIN_TOKEN` with a new value and the old token stops
  working immediately. Each device that bookmarked admin.html will need the new
  one re-pasted.
- **Free-tier headroom.** D1: 5 GB free. Workers: 100k req/day free. R2: 10 GB
  free. Resend: 3k emails/month free. Volume in Phase 1 is application
  submissions only - comfortably under all caps.
- **Honeypot, not Turnstile.** Phase 1 uses a hidden `company_url` field. Bots
  that auto-fill all fields get silently dropped (we return 200). If real spam
  starts arriving, add Turnstile before promoting the page in marketing.

This file lives at `.github/docs/dealer-README.md`. GitHub Pages does not serve `.github/`,
so it is not publicly fetchable. Do not move it back under the deploy root.
