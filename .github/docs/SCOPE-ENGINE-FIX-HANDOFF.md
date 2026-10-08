# Scope Engine — Why it isn't emailing + drop-in fix

**For:** ACG web developer
**From:** Connor (via Claude Code diagnostic)
**Date:** July 1, 2026
**File:** `scope-engine.html` (single file, no build step — GitHub Pages)

---

## TL;DR

The scope engine's backend (`formsubmit.co/ajax/connor@acglass.com`) is **healthy** — I sent live test payloads (including a 106 KB PDF) and they delivered to Connor's inbox. The failures are **client-side**, and there are three real defects. The most damaging one makes the form tell the visitor *"✓ your report was emailed"* even when nothing was sent.

Fix all three by replacing the submit handler (Section 4). ~20 minutes, zero new dependencies.

---

## What I verified (evidence)

| Test | Endpoint | Payload | Result |
|---|---|---|---|
| A/B | `/ajax/` no Referer | plain + PDF | `success:"false"` — *"open through a web server"* (Referer check) |
| C | `/ajax/` real Referer | plain fields | `success:"true"` → **arrived** |
| D | `/ajax/` real Referer | + PDF attachment | `success:"true"` → **arrived, but `hasAttachments:false`** |
| E | `/ajax/` real Referer | full lead payload + 106 KB PDF + autoresponse | `success:"true"` → **arrived** |

Inbox audit: **zero** `New scope-engine lead` emails have ever arrived — only `send-plans` and main-contact-form leads. Real scope-engine submissions are not landing.

---

## Defect 1 — Success is judged by HTTP status, not FormSubmit's JSON body (CRITICAL)

FormSubmit **always returns HTTP 200**, even on failure. The real result is in the JSON body: `{"success":"true"}` or `{"success":"false"}` (spam-flagged, rate-limited, missing Referer, oversized, etc.).

Current code (line ~2218):

```js
const r = await fetch(ACG_CONFIG.endpoint, { method:'POST', body: payload, headers:{'Accept':'application/json'} });
if (r.ok) {                       // ← 200 is ALWAYS true, even on failure
  ga('generate_lead', {...});      // ← phantom conversion
  status.innerHTML = '✓ ... emailed to you ...';  // ← lies to the visitor
}
```

Consequence: any FormSubmit-side failure is reported to the visitor as success, no email is sent, and GA4 logs a false `generate_lead`. This is the "not sending but looks like it worked" symptom.

**Fix:** parse the JSON and branch on `data.success === 'true'`.

## Defect 2 — The `/ajax/` endpoint silently strips attachments

Test D proved it: the email arrived with `hasAttachments:false`. FormSubmit only delivers file attachments on the **non-`/ajax/`** endpoint. So the code's promise — *"A branded PDF is attached to this email"* — is false for ACG's copy. The visitor still gets the client-side download (that part works); ACG never gets the PDF by email.

**Fix (immediate):** stop promising an emailed PDF; send lead **data** via `/ajax/` (reliable) and keep the client-side download. The lead data already contains everything needed to regenerate. (Real PDF-by-email belongs in the Cloudflare Worker backend the README already scopes — see Section 6.)

## Defect 3 — `buildLeadPayload()` runs outside the try/catch

Line ~2207: `const payload = buildLeadPayload();` sits **before** the `try {`. `buildLeadPayload()` dereferences `ACG_CONFIG.systems[state.recommendedSystem].name`, `ACG_CONFIG.glassMakeup[c.makeupUsed].label`, and `state.cost` — any of which throws a `TypeError` if the engine reached submit with an incomplete `state`. An uncaught throw freezes the UI on **"Sending…"**, leaves the submit button disabled, shows no error, and sends nothing.

**Fix:** move it inside the try, and add an `AbortController` timeout so a hung network shows the fallback instead of spinning forever.

---

## 4. Drop-in replacement — the submit handler

Replace the whole `document.getElementById('lead-form').addEventListener('submit', ...)` block (≈ lines 2154–2276) with this:

```js
document.getElementById('lead-form').addEventListener('submit', async (e) => {
  e.preventDefault();
  const status = document.getElementById('lf-status');
  const submit = document.getElementById('lf-submit');

  const fail = (msg) => {
    status.className = 'se-form-status err';
    status.innerHTML = msg;
    submit.disabled = false;
    submit.style.opacity = '1';
  };
  const FALLBACK = '⚠ We couldn\'t deliver that automatically. Please email '
    + '<a href="mailto:connor@acglass.com" style="color:var(--se-accent);">connor@acglass.com</a> '
    + 'or call (772) 486-7711 — your numbers are safe, just resend.';

  // --- validation (unchanged) ---
  const required = ['lf-name','lf-email','lf-company','lf-role'];
  for (const id of required) {
    const el = document.getElementById(id);
    if (!el.value || !el.value.trim()) { fail('⚠ Please complete all required fields.'); el.focus(); return; }
  }
  if (!document.getElementById('lf-tcpa').checked) { fail('⚠ Please check the consent box so we can reply to you.'); return; }
  const emailVal = document.getElementById('lf-email').value.trim();
  if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(emailVal)) { fail('⚠ That email looks off — double-check it?'); document.getElementById('lf-email').focus(); return; }

  submit.disabled = true;
  submit.style.opacity = '.6';
  status.className = 'se-form-status';
  status.textContent = 'Sending…';

  // Build the PDF for the visitor's download (best-effort, never blocks the lead)
  let pdfBlob = null, pdfFilename = null;
  try {
    const out = generateBrandedPDF('blob');
    if (out && out.blob) { pdfBlob = out.blob; pdfFilename = out.filename; }
  } catch (err) { ga('scope_pdf_failed', { error: String(err).slice(0,100) }); }

  // Everything that can throw is now INSIDE the try (Defect 3)
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), 15000);   // 15s network guard
  try {
    const payload = buildLeadPayload();                        // moved inside try
    // NOTE: /ajax/ silently drops attachments (verified). We send DATA only and let
    // the visitor download the PDF locally. PDF-by-email → Cloudflare Worker (README §4).
    const r = await fetch(ACG_CONFIG.endpoint, {
      method: 'POST',
      body: payload,
      headers: { 'Accept': 'application/json' },
      signal: controller.signal
    });
    clearTimeout(timer);

    let data = {};
    try { data = await r.json(); } catch (_) {}                 // FormSubmit returns JSON

    // Defect 1: trust the JSON body, not just r.ok
    if (r.ok && String(data.success) === 'true') {
      ga('scope_lead_captured', {
        project_type: state.projectType, height: state.height, location: state.location,
        system: state.recommendedSystem, system_sf: state.computedSystemSF });
      ga('generate_lead', { form_id:'scope-engine', source_page:'/scope-engine.html', currency:'USD', value:1000 });

      status.className = 'se-form-status ok';
      if (pdfBlob && pdfFilename) {
        const a = document.createElement('a');
        const url = URL.createObjectURL(pdfBlob);
        a.href = url; a.download = pdfFilename;
        document.body.appendChild(a); a.click();
        setTimeout(() => { URL.revokeObjectURL(url); a.remove(); }, 1500);
        ga('scope_pdf_generated', { filename: pdfFilename });
        // Honest copy: report went to ACG; PDF downloaded here (Defect 2)
        status.innerHTML = '✓ Got it — our estimating team has your scope and will reach out within 48 hours. '
          + 'Your branded PDF just downloaded as <strong>' + pdfFilename + '</strong>.'
          + '<br><button id="redownload-pdf-btn" class="se-cta se-cta-ghost" style="margin-top:14px;padding:10px 18px;">Re-download PDF</button>';
        setTimeout(() => {
          const rb = document.getElementById('redownload-pdf-btn');
          if (rb) rb.addEventListener('click', () => {
            ga('scope_pdf_redownload');
            const out = generateBrandedPDF('blob');
            if (out && out.blob) {
              const aa = document.createElement('a'); const u = URL.createObjectURL(out.blob);
              aa.href = u; aa.download = out.filename; document.body.appendChild(aa); aa.click();
              setTimeout(() => { URL.revokeObjectURL(u); aa.remove(); }, 1500);
            }
          });
        }, 50);
      } else {
        status.innerHTML = '✓ Got it — our estimating team has your scope and will reach out within 48 hours.'
          + '<br>You can also <button id="print-pdf-btn" class="se-cta se-cta-ghost" style="margin-top:14px;padding:10px 18px;">Print / save this report as PDF</button>';
        setTimeout(() => {
          const pb = document.getElementById('print-pdf-btn');
          if (pb) pb.addEventListener('click', () => { ga('scope_pdf_print'); window.print(); });
        }, 50);
      }
      document.getElementById('lead-form').querySelectorAll('input, select').forEach(el => el.disabled = true);
    } else {
      ga('form_submission_failed', { form_id:'scope-engine', http_status: r.status, reason: String(data.message||'').slice(0,120) });
      fail(FALLBACK);
    }
  } catch (err) {
    clearTimeout(timer);
    ga('form_submission_failed', { form_id:'scope-engine', error_type: err.name === 'AbortError' ? 'timeout' : 'network' });
    fail(FALLBACK);
  }
});
```

### What changed vs. current
1. **`data.success` is now the source of truth** (was `r.ok` only). No more phantom conversions / false "emailed" messages.
2. **`buildLeadPayload()` moved inside `try`** — a bad `state` shows the fallback instead of freezing on "Sending…".
3. **15 s `AbortController` timeout** — hung networks recover with the fallback + re-enabled button.
4. **Honest success copy** — we no longer claim ACG got the PDF by email (it can't via `/ajax/`); we say the *scope* reached the team and the *PDF downloaded* to the visitor.
5. **Every failure path re-enables the button and preserves inputs** via the `fail()` helper — the visitor can retry.

---

## 5. Optional UX / optimization upgrades (nice-to-have, same file)

- **`_autoresponse` still works on `/ajax/`** (verified) — the visitor gets their summary email. Keep it. Consider a checkbox "Email me a copy" that toggles whether `_autoresponse` is appended, for visitors who don't want it.
- **Preload jsPDF earlier.** It's `defer`-loaded from cdnjs; on a fast submit it may not be ready, silently dropping the download. Add `<link rel="preload" as="script" href="https://cdnjs.cloudflare.com/ajax/libs/jspdf/2.5.2/jspdf.umd.min.js">` in `<head>`, or self-host it (site already self-hosts fonts).
- **Full ARIA radiogroup keyboard pattern** (arrow keys) — README §7 lists this as the remaining a11y TODO. Tab + Enter/Space works today.
- **Progress persistence already good** (sessionStorage). Add a visible "Step X of 6" counter + a "Start over" reset to cut abandonment.
- **De-duplicate the pricing config note:** README says `_template` should be `basic` (less likely to hit Promotions), but code sends `_template=table`. CLAUDE.md §4 standard is `basic`. Recommend `basic` for deliverability consistency with the other 3 forms.

---

## 6. The real long-term fix (PDF-by-email to ACG)

`/ajax/` can never email ACG the attachment. To have ACG receive the branded PDF automatically, stand up the Cloudflare Worker already scoped in `SCOPE-ENGINE-README.md` §4:
1. Worker accepts `multipart/form-data` (data + PDF blob).
2. Worker emails `connor@acglass.com` via Resend/Postmark **with the PDF attached**, and sends the visitor the autoresponse.
3. Point `ACG_CONFIG.endpoint` at the Worker URL. Payload shape is unchanged.

Until then, the Section 4 fix makes the form **correct and honest**: leads reliably reach ACG, the visitor reliably gets their PDF + summary email, and nothing lies about what happened.

---

*Generated from live endpoint tests + inbox audit on 2026-07-01.*
