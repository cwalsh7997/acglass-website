# Form architecture

Written phase 5, 2026-09-08. The handler is **not stood up**: provisioning external
infrastructure is hard stop 7, irreversible outside the repo. This is the design
and the reasoning, ready to execute.

## What is live today

| Page | Action | Method |
|---|---|---|
| `bid.html` | `formsubmit.co/connor@acglass.com` | POST |
| `send-plans.html` | `formsubmit.co/connor@acglass.com` | POST |
| `partners.html` | **`mailto:connor@acglass.com`** | POST |
| `contact.html`, `scope-engine.html`, `commercial-glazing-nashville-tn.html` | JS `fetch` to formsubmit | POST |
| 4 tool pages | none, client-side only | GET |

Ten forms, not the nine the phase brief assumes.

`POST mailto:` on `partners.html` fails silently in most browsers. The visitor sees
a submit, nothing is sent, and nobody learns the lead was lost.

## Fixed in this phase

`_captcha=false` removed from all five forms that carried it. It disabled
formsubmit's only built-in abuse control on forms whose sole remaining protection was
a `_gotcha` honeypot, which any competent scraper steps over.

## The exposure that is bigger than the brief says

The brief scopes staff-email exposure to the form pages. Measured: **`connor@acglass.com`
appears in the page source of 1,530 pages with no protection.** Only 4 pages wrap it
in Cloudflare's `<!--email_off-->` Scrape Shield markers.

That is a sitewide harvesting surface, mostly a footer contact link rather than a form
action. Fixing it is not a form change: it is either a Scrape Shield sweep across
1,530 pages or a routed alias. Both are phase-6 scale. Recorded here so the number is
on the table.

## Target architecture

The origin serves files only, so the handler is external. ACG already runs Pipedream,
which makes it the lower-risk choice over a new serverless function: one less vendor,
one less deploy target, one less thing to hold credentials.

```
browser ──POST multipart──► handler (Pipedream)
                              ├─ verify Turnstile SERVER-SIDE
                              ├─ honeypot check
                              ├─ presign direct-to-storage upload
                              └─ notify + acknowledge
```

Limits, per rules/05: **2 GB per file, 5 GB per submission, 25 files max.**
Quarantine until scanned. A plan-room URL field as a first-class alternative, not a
fallback: on real bids the plans are usually already in a plan room, and asking for a
link rather than a 2 GB upload is faster for the GC and cheaper for ACG.

No staff email address in page source. Turnstile verified server-side, never
client-only. Honeypot kept, because it is free and catches the low tier.

## Deliberately out of scope

Form redesign, new forms, the routing table, SMS alerting, the Pipedream fan-out to
Trello, Dropbox and Sheets, retention automation, the confirmation page.
