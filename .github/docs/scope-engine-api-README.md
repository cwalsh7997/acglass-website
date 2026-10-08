# ACG Scope Engine API (Cloudflare Worker)

Emails ACG the scope-engine lead **with the branded PDF attached**, and emails the
visitor their report — the thing `formsubmit.co/ajax` structurally can't do (its
`/ajax` endpoint silently strips file attachments).

The scope engine already POSTs `multipart/form-data` with the PDF as the `attachment`
field, so adopting this Worker is a **one-line client change** plus a deploy.

---

## Why this exists

`scope-engine.html` builds a branded PDF in the browser and attaches it to the lead
POST. Against `formsubmit.co/ajax/…` the attachment is dropped (verified: lead emails
arrive `hasAttachments:false`). This Worker accepts the identical payload and uses
Resend to send real emails with the PDF attached. It returns the same JSON shape
formsubmit does (`{"success":"true"|"false"}`), so no other client code changes.

---

## Deploy (one time, ~10 min)

1. **Resend account + verified domain**
   - Sign up at https://resend.com and create an API key.
   - Add `acglass.com` as a domain and verify it. Because `acglass.com` DNS is on
     Cloudflare, this is just pasting the SPF/DKIM/DMARC records Resend gives you.
     (Until the domain is verified, Resend only sends to your own address.)

2. **Deploy the Worker**
   ```bash
   cd workers/scope-engine-api
   npm install -g wrangler
   wrangler login
   wrangler secret put RESEND_API_KEY      # paste the Resend key
   wrangler deploy
   ```
   Wrangler prints a URL like:
   `https://acg-scope-engine-api.<your-subdomain>.workers.dev`

3. **Point the scope engine at it** — in `scope-engine.html`, change the one line in
   `ACG_CONFIG`:
   ```js
   // before
   endpoint: 'https://formsubmit.co/ajax/connor@acglass.com',
   // after
   endpoint: 'https://acg-scope-engine-api.<your-subdomain>.workers.dev',
   ```
   (Optional but cleaner: put the Worker behind `https://acglass.com/api/scope` via a
   Cloudflare route so it's same-origin. Not required — CORS is already handled.)

4. **Ship it.** Commit + PR + merge to `main`. Send Claude Code the Worker URL and it
   will make the client swap for you.

---

## Verify after deploy

```bash
# health check
curl https://acg-scope-engine-api.<sub>.workers.dev            # -> {"ok":true,...}

# simulated lead (no PDF) — should email connor@acglass.com and return success
curl -X POST https://acg-scope-engine-api.<sub>.workers.dev \
  -H 'Origin: https://acglass.com' \
  -F 'name=Test GC' -F 'email=connor@acglass.com' -F 'company=Test' \
  -F 'scope_project_type=storefront' -F 'scope_system_sf=4200' \
  -F '_subject=[ACG LEAD] Worker smoke test'
# -> {"success":"true","message":"The form was submitted successfully."}
```

Then run the real form end-to-end from the deployed site and confirm the lead email
arrives **with the PDF attached** and the visitor gets their copy.

---

## Config reference

| Key | Type | Purpose |
|---|---|---|
| `ALLOWED_ORIGIN` | var | CORS origin (`https://acglass.com`) |
| `NOTIFY_EMAIL` | var | Where ACG's lead copy goes (`connor@acglass.com`) |
| `RESEND_FROM` | var | Verified sender (`noreply@acglass.com`) |
| `RESEND_API_KEY` | secret | Resend API key — enables sending + attachments |

## Behavior notes

- **Honeypot**: if `_gotcha`/`_honey` is filled, returns success and sends nothing.
- **Validation**: requires `name` + a valid `email`; returns `{"success":"false"}` otherwise.
- **Caps**: 8 MB request / 6 MB PDF. An oversized PDF is dropped but the lead still sends.
- **Autoresponse**: if `_autoresponse` is present, the visitor is emailed it + the PDF.
  A failed autoresponse never fails ACG's lead delivery.
- **Once this is live**, update the scope-engine success copy — the visitor now really
  does get the PDF by email (not only the local download).
