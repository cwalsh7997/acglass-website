# Review-Engine: QBO Closeout → PM Review-Ask (Pipedream workflow)

**Time estimate:** 30 minutes for first build, 5 minutes per refinement.
**Prereqs:** You have Pipedream signed in and connected to QuickBooks Online + Gmail + Google Sheets.

This is the operational pattern that turns project closeouts into Google reviews without you ever drafting an email. The workflow is in **draft-first mode** for the first 30 days — you approve every send. After 30 days of clean operation we switch the final send step to auto-send.

---

## 1. Trigger

**Pipedream trigger:** QuickBooks Online → **New Closed Invoice** (filtered).

Filter expression:
```
(invoice.balance == 0) AND
(invoice.line_items contains 'Commercial Glazing' OR 'Storefront' OR 'Curtainwall' OR 'Impact Windows')
```

This fires once per invoice when the payment closes it out — typically at the end of a project, not mid-project progress billings.

---

## 2. PM-Map Sheet lookup

Pipedream **Action:** Google Sheets → **Read Row**.

Sheet: **ACG SEO Ops** → tab **PM-Map**.

Match key: `invoice.customer_ref.value` (the QBO customer ID) → returns the row containing:
- Project Manager (PM) name and email
- GC Primary Contact name and email
- Project name
- Project address
- Google Review short link (set in step 4 below)

If no match: the workflow stops here and writes a "needs PM-Map row" line to the **Pending PM** tab. Connor adds the row manually and re-runs.

---

## 3. Draft generator

Pipedream **Action:** Code (Python). Reads invoice + PM-map data and emits a draft email body.

Template (DO NOT auto-send during the first 30 days):

```
Subject: Quick favor — Google review for ACG

Hi {gc_primary_first_name},

Wanted to thank you for partnering with us on {project_name}. The team enjoyed running the {primary_scope} scope alongside your build.

If you're willing, a short Google review goes a long way for our team — many of our future bid invitations come from GCs reading what other GCs say.

Direct link: {gbp_short_link}

Anything we should do differently next time? Hit reply — that's also useful.

Connor Walsh
American Commercial Glass
+1-772-486-7711
connor@acglass.com
```

---

## 4. GBP short link placeholder

In the PM-Map sheet, the `Google Review short link` column holds a short URL like `https://g.page/r/<id>/review`. You generate this once in your Google Business Profile dashboard:

1. [business.google.com](https://business.google.com) → **Customers** → **Reviews** → **Get more reviews**.
2. Copy the short link.
3. Paste it into the `gbp_short_link` field on every row in the PM-Map sheet (it's the same link for all reviews).

---

## 5. Send branch (draft-first mode — DAYS 0–30)

Pipedream **Action:** Gmail → **Create Draft** (not Send Email yet).

- To: `gc_primary_email`
- CC: `pm_email`
- From: connor@acglass.com
- Subject: from the template
- Body: from the template

Connor opens the draft in Gmail, reads it, and either:
- Sends it as-is, or
- Edits and sends, or
- Discards (then writes a one-line note to the **Discarded** tab so we know what went wrong).

After 30 days of clean drafts, switch this step from **Create Draft** to **Send Email**.

---

## 6. Follow-up branch

Pipedream **Schedule:** 7 days after the original draft created.

Reads the **Sent** tab of the SEO Ops sheet to see if the original was actually sent. If yes AND no review has come in (track via GBP API or by manual marking in **Reviews-Received**), emit a SECOND draft:

```
Subject: One quick ask on {project_name}

Hi {gc_primary_first_name},

Following up on my note last week — if you had a minute for a short review, here is the direct link again:

{gbp_short_link}

If life got in the way, no problem — please just disregard.

Connor
```

Same draft-first mode for 30 days.

---

## 7. Logging

Every step writes to the **Review Engine Log** tab of the SEO Ops sheet:
| Date | Invoice ID | Customer | PM | Stage | Action | Notes |

Weekly: Connor reviews the log to confirm volume and quality. If review velocity drops, that's a signal something in the operations chain (closeout, PM hand-off) is broken — separate from a marketing issue.

---

## Acceptance

1. The workflow exists in Pipedream and is **Active**.
2. The PM-Map sheet exists with at least 10 active customer rows, each carrying the canonical GBP short link.
3. A test invoice closeout triggers a Gmail draft in your inbox within 90 seconds.
4. The Review Engine Log records the draft.
5. After 30 days in draft-first mode, switch step 5 to Send Email and document the change in this file with a `## Changelog` section below.

---

## Changelog

- 2026-06-11 — Initial spec written by build agent. In draft-first mode by default.
