/**
 * ACG Scope Engine API — Cloudflare Worker
 * ------------------------------------------------------------------
 * Drop-in replacement for the formsubmit.co/ajax endpoint used by
 * /scope-engine.html. Unlike formsubmit's /ajax endpoint, this Worker
 * DELIVERS THE BRANDED PDF BY EMAIL — both to ACG and to the visitor.
 *
 * The scope engine already POSTs multipart/form-data with the branded
 * PDF as the `attachment` file, so the ONLY client change to adopt this
 * is repointing ACG_CONFIG.endpoint at this Worker's URL. This Worker
 * returns the same JSON shape formsubmit does — {"success":"true"} /
 * {"success":"false"} — so scope-engine.html needs no other changes.
 *
 * Env (see wrangler.toml):
 *   ALLOWED_ORIGIN   var    — e.g. "https://acglass.com" (CORS)
 *   NOTIFY_EMAIL     var    — where ACG's lead copy goes (connor@acglass.com)
 *   RESEND_FROM      var    — verified sender, e.g. "ACG Scope Engine <noreply@acglass.com>"
 *   RESEND_API_KEY   secret — from resend.com; enables email. Required.
 *
 * Deploy: see wrangler.toml header + README.md in this folder.
 */

const MAX_BODY_BYTES = 8 * 1024 * 1024;   // 8 MB hard cap on the whole request
const MAX_PDF_BYTES   = 6 * 1024 * 1024;   // 6 MB cap on the attachment

export default {
  async fetch(request, env) {
    const origin = request.headers.get('Origin') || '';

    if (request.method === 'OPTIONS') return corsResponse(env, origin, 204);
    if (request.method === 'GET')     return jsonResponse(env, origin, 200, { ok: true, service: 'acg-scope-engine-api' });
    if (request.method !== 'POST')    return jsonResponse(env, origin, 405, { success: 'false', message: 'Method not allowed' });

    // Reject oversized bodies early (Content-Length is advisory but cheap to check).
    const declaredLen = Number(request.headers.get('Content-Length') || 0);
    if (declaredLen && declaredLen > MAX_BODY_BYTES) {
      return jsonResponse(env, origin, 413, { success: 'false', message: 'Payload too large.' });
    }

    let form;
    try {
      form = await request.formData();
    } catch (_) {
      return jsonResponse(env, origin, 400, { success: 'false', message: 'Expected multipart/form-data.' });
    }

    // Honeypot: bots fill hidden fields. Pretend success, send nothing.
    const honey = (form.get('_gotcha') || form.get('_honey') || '').toString().trim();
    if (honey) return jsonResponse(env, origin, 200, { success: 'true', message: 'The form was submitted successfully.' });

    // --- Contact basics ---
    const name    = str(form.get('name'));
    const email   = str(form.get('email'));
    const company = str(form.get('company'));
    if (!name || !isEmail(email)) {
      return jsonResponse(env, origin, 422, { success: 'false', message: 'Name and a valid email are required.' });
    }

    if (!env.RESEND_API_KEY || !env.NOTIFY_EMAIL) {
      console.error('[scope-engine] RESEND_API_KEY or NOTIFY_EMAIL not configured.');
      return jsonResponse(env, origin, 500, { success: 'false', message: 'Email is not configured on the server.' });
    }

    // --- Collect the branded PDF attachment, if present ---
    let pdf = null;
    const file = form.get('attachment');
    if (file && typeof file === 'object' && typeof file.arrayBuffer === 'function') {
      const buf = await file.arrayBuffer();
      if (buf.byteLength > MAX_PDF_BYTES) {
        // Don't fail the lead over an oversized PDF — send data-only, note it.
        console.warn('[scope-engine] PDF exceeds cap, sending without attachment.');
      } else if (buf.byteLength > 0) {
        pdf = { filename: safeFilename(file.name || 'ACG-Scope-Report.pdf'), content: toBase64(buf) };
      }
    }

    const subject = str(form.get('_subject')) || `[ACG LEAD] New scope-engine lead — ${company || name}`;

    try {
      // 1) ACG's lead copy — every field, PDF attached, reply-to = visitor.
      await sendEmail(env, {
        to: env.NOTIFY_EMAIL,
        replyTo: email,
        subject,
        text: buildAcgLeadText(form),
        attachments: pdf ? [pdf] : [],
      });

      // 2) Visitor autoresponse — their summary + the PDF, best-effort (never fails the lead).
      const auto = str(form.get('_autoresponse'));
      if (auto) {
        try {
          await sendEmail(env, {
            to: email,
            replyTo: env.NOTIFY_EMAIL,
            subject: 'Your ACG Scope Report',
            text: auto,
            attachments: pdf ? [pdf] : [],
          });
        } catch (e) {
          console.warn('[scope-engine] autoresponse failed (lead still delivered):', e.message);
        }
      }

      return jsonResponse(env, origin, 200, { success: 'true', message: 'The form was submitted successfully.' });
    } catch (e) {
      console.error('[scope-engine] send failed:', e.message);
      return jsonResponse(env, origin, 502, { success: 'false', message: 'Could not deliver the lead email.' });
    }
  },
};

// ---------------------------------------------------------------------------
// Email (Resend) — supports base64 attachments, which formsubmit /ajax cannot.
// ---------------------------------------------------------------------------
async function sendEmail(env, { to, replyTo, subject, text, attachments }) {
  const body = {
    from: env.RESEND_FROM || 'ACG Scope Engine <noreply@acglass.com>',
    to: [to],
    subject,
    text,
  };
  if (replyTo) body.reply_to = replyTo;
  if (attachments && attachments.length) body.attachments = attachments;

  const res = await fetch('https://api.resend.com/emails', {
    method: 'POST',
    headers: {
      'Authorization': 'Bearer ' + env.RESEND_API_KEY,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(body),
  });
  if (!res.ok) {
    const t = await res.text().catch(() => '');
    throw new Error('Resend ' + res.status + ': ' + t.slice(0, 300));
  }
  return res.json().catch(() => ({}));
}

// Render every submitted field into a readable plain-text lead email.
// Skips formsubmit control fields (_subject, _autoresponse, etc.) and the file.
function buildAcgLeadText(form) {
  const skip = new Set(['_subject', '_template', '_captcha', '_gotcha', '_honey', '_autoresponse', '_replyto', 'attachment']);
  const order = [
    'name', 'company', 'role', 'email', 'phone', 'project_name', 'needed_by_date', 'consent',
    'scope_project_type', 'scope_height', 'scope_size_method', 'scope_system_sf', 'scope_location',
    'scope_location_label', 'scope_hvhz', 'scope_requirements', 'scope_glass_makeup',
    'scope_recommended_system', 'scope_system_name', 'recommended_system', 'system_sf',
    'timeline_total_weeks', 'lead_id', 'timestamp_iso', 'page_url', 'referrer',
  ];
  const seen = new Set();
  const rows = [];
  const push = (k) => {
    if (skip.has(k) || seen.has(k)) return;
    const v = form.get(k);
    if (v === null || typeof v === 'object') return;   // skip files/absent
    seen.add(k);
    rows.push(label(k).padEnd(22) + str(v));
  };
  order.forEach(push);
  for (const k of form.keys()) push(k);   // any extra fields (utm_*, etc.)

  return [
    'New scope-engine lead from acglass.com — full scope + branded PDF attached.',
    '',
    ...rows,
    '',
    'Reply to this email to reach the lead directly.',
  ].join('\n');
}

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------
function str(v) { return (v === null || v === undefined) ? '' : String(v).trim(); }
function isEmail(v) { return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(str(v)); }
function label(k) { return k.replace(/_/g, ' ').replace(/\b\w/g, (c) => c.toUpperCase()) + ':'; }

function safeFilename(name) {
  const clean = String(name).replace(/[^\w.\-]+/g, '-').slice(0, 120);
  return /\.pdf$/i.test(clean) ? clean : clean + '.pdf';
}

// Base64-encode an ArrayBuffer in chunks (avoids call-stack limits on big files).
function toBase64(buf) {
  const bytes = new Uint8Array(buf);
  let bin = '';
  const CHUNK = 0x8000;
  for (let i = 0; i < bytes.length; i += CHUNK) {
    bin += String.fromCharCode.apply(null, bytes.subarray(i, i + CHUNK));
  }
  return btoa(bin);
}

function corsHeaders(env, origin) {
  const allow = env.ALLOWED_ORIGIN || '*';
  return {
    'Access-Control-Allow-Origin': allow === '*' ? '*' : allow,
    'Access-Control-Allow-Methods': 'POST, GET, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type, Accept',
    'Access-Control-Max-Age': '86400',
    'Vary': 'Origin',
  };
}

function jsonResponse(env, origin, status, body) {
  return new Response(JSON.stringify(body), {
    status,
    headers: {
      'Content-Type': 'application/json;charset=UTF-8',
      'Cache-Control': 'no-store',
      ...corsHeaders(env, origin),
    },
  });
}

function corsResponse(env, origin, status) {
  return new Response(null, { status, headers: corsHeaders(env, origin) });
}
