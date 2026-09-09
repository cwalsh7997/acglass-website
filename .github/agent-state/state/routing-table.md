# Form and endpoint routing table

Required by phase 5. Built 2026-09-08 from the live markup, not from intent.

## Lead-capture forms

| page | form id | transport | endpoint | fallback | honeypot |
|---|---|---|---|---|---|
| `bid.html` | `bid-form` | form action + fetch | `formsubmit.co/connor@acglass.com` | none | `_gotcha` |
| `send-plans.html` | `send-plans-form` | form action | `formsubmit.co/connor@acglass.com` | none | `_gotcha` |
| `partners.html` | (unnamed) | form action | `formsubmit.co/connor@acglass.com` | none | none |
| `contact.html` | `contact-form` | fetch, JS | `formsubmit.co/ajax/connor@acglass.com` | none | `_honey` |
| `commercial-glazing-nashville-tn.html` | `intakeForm` | fetch, JS | `formsubmit.co/ajax/connor@acglass.com` | none | `_honey` |
| `scope-engine.html` | `lead-form` | fetch, JS | `formsubmit.co` | none | `_gotcha` |
| `become-a-dealer.html` | `dealer-application-form` | fetch, JS via `dealer/dealer.js` | `API_BASE + /api/applications` | **prefilled mailto** | n/a |

## Non-lead forms

`tools/glass-weight-calculator/` and `tools/wind-pressure-calculator/` submit to a
local JS handler and post nothing. They are calculators, not intake.

## The capability-statement surface

`qualifications.html` carries the credential rows. LIC-03 was corrected on
2026-09-08 from "Federal registration in process" to the registered SAM wording
per D1, which had been assigned to phase 0 and never executed.

## What is actually wrong with this table

**Six of seven lead forms post to a third-party service with the recipient address
in the page source.** D4 obligation 5 calls this a P0 and names four defects:
exposed staff email, no captcha, no DPA, and upload missing from the primary CTA.
The upload half is fixed, `send-plans.html` now carries file inputs. The other
three stand. See PC-20 for the alias-token fix, which is one paste.

**`become-a-dealer.html` is the only form that degrades correctly.** With no API
configured it falls back to a prefilled mailto rather than dropping the
submission. The other six have no fallback: if formsubmit.co is down or rate
limits, the lead is lost silently and nobody finds out. That is the argument for
moving off it that does not depend on privacy at all.
