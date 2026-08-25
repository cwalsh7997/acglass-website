/**
 * ACG Dealer Portal API - Cloudflare Worker
 *
 * Handles:
 *   POST   /api/applications        Public - submit a dealer application
 *   GET    /api/applications        Admin  - list applications (Bearer token)
 *   PATCH  /api/applications/:id    Admin  - update status (Bearer token)
 *   GET    /api/health              Public - liveness check
 *
 * Bindings (configured in wrangler.toml):
 *   - DB                    D1 database (see schema.sql)
 *   - ADMIN_TOKEN           secret  - bearer token for admin endpoints
 *   - NOTIFY_EMAIL          var     - email to notify on new applications
 *   - RESEND_API_KEY        secret  - optional, enables email via Resend
 *   - RESEND_FROM           var     - optional, "ACG <noreply@acglass.com>"
 *   - ALLOWED_ORIGIN        var     - e.g. "https://acglass.com" (CORS)
 *
 * This Worker is deployed independently from the existing
 * cloudflare-410-worker.js (which handles spam URL filtering on acglass.com/*).
 * The two Workers do not interact.
 */

const MAX_BODY_BYTES = 16 * 1024; // 16 KB - applications never need more

const REQUIRED_FIELDS = [
  'company',
  'contact_name',
  'email',
  'phone',
  'address',
  'years_in_business',
  'manufacturers',
  'annual_volume',
];

const ALLOWED_FIELDS = REQUIRED_FIELDS.concat(['license_number', 'notes']);

const ALLOWED_STATUSES = new Set(['pending', 'approved', 'rejected']);

// ---------------------------------------------------------------------------
// Routing
// ---------------------------------------------------------------------------

export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);
    const path = url.pathname.replace(/\/+$/, '') || '/';
    const origin = request.headers.get('Origin');

    // CORS preflight
    if (request.method === 'OPTIONS') {
      return corsResponse(env, origin, 204);
    }

    try {
      if (path === '/api/health' && request.method === 'GET') {
        return jsonResponse(env, origin, 200, { ok: true });
      }

      if (path === '/api/applications') {
        if (request.method === 'POST') return handleCreateApplication(request, env, origin, ctx);
        if (request.method === 'GET') return handleListApplications(request, env, origin);
        return methodNotAllowed(env, origin);
      }

      // /api/applications/:id
      const match = path.match(/^\/api\/applications\/([0-9a-zA-Z-]+)$/);
      if (match) {
        const id = match[1];
        if (request.method === 'PATCH') return handleUpdateApplication(request, env, origin, id);
        if (request.method === 'GET') return handleGetApplication(request, env, origin, id);
        return methodNotAllowed(env, origin);
      }

      return jsonResponse(env, origin, 404, { error: 'Not found' });
    } catch (err) {
      console.error('Worker error:', err && err.stack ? err.stack : err);
      return jsonResponse(env, origin, 500, { error: 'Internal error' });
    }
  },
};

// ---------------------------------------------------------------------------
// Handlers
// ---------------------------------------------------------------------------

async function handleCreateApplication(request, env, origin, ctx) {
  // Reject oversized bodies before parsing.
  const lenHeader = request.headers.get('Content-Length');
  if (lenHeader && Number(lenHeader) > MAX_BODY_BYTES) {
    return jsonResponse(env, origin, 413, { error: 'Payload too large' });
  }

  let body;
  try {
    body = await request.json();
  } catch (e) {
    return jsonResponse(env, origin, 400, { error: 'Invalid JSON' });
  }
  if (!body || typeof body !== 'object') {
    return jsonResponse(env, origin, 400, { error: 'Invalid payload' });
  }

  // Honeypot: if any unknown "company_url" field is non-empty, silently 200.
  if (body.company_url) {
    return jsonResponse(env, origin, 200, { ok: true });
  }

  // Whitelist + trim fields
  const cleaned = {};
  for (const key of ALLOWED_FIELDS) {
    if (typeof body[key] === 'string') {
      cleaned[key] = body[key].trim().slice(0, 2000);
    }
  }

  // Validate required
  const missing = REQUIRED_FIELDS.filter((k) => !cleaned[k]);
  if (missing.length) {
    return jsonResponse(env, origin, 400, {
      error: 'Missing required fields',
      fields: missing,
    });
  }

  // Email sanity check
  if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(cleaned.email)) {
    return jsonResponse(env, origin, 400, { error: 'Invalid email' });
  }

  if (!env.DB) {
    console.error('D1 binding "DB" missing - application not saved.');
    return jsonResponse(env, origin, 500, { error: 'Database unavailable' });
  }

  const id = crypto.randomUUID();
  const now = new Date().toISOString();
  const ip = request.headers.get('CF-Connecting-IP') || '';
  const ua = (request.headers.get('User-Agent') || '').slice(0, 500);

  try {
    await env.DB.prepare(
      `INSERT INTO dealer_applications
        (id, created_at, status, company, contact_name, email, phone, address,
         license_number, years_in_business, manufacturers, annual_volume, notes,
         submitted_ip, user_agent)
       VALUES (?, ?, 'pending', ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)`
    )
      .bind(
        id,
        now,
        cleaned.company,
        cleaned.contact_name,
        cleaned.email,
        cleaned.phone,
        cleaned.address,
        cleaned.license_number || null,
        cleaned.years_in_business,
        cleaned.manufacturers,
        cleaned.annual_volume,
        cleaned.notes || null,
        ip,
        ua
      )
      .run();
  } catch (err) {
    console.error('D1 insert failed:', err && err.message ? err.message : err);
    return jsonResponse(env, origin, 500, { error: 'Could not save application' });
  }

  // Fire-and-forget email notification (does not block the response).
  if (typeof ctx?.waitUntil === 'function') {
    ctx.waitUntil(
      sendNewApplicationEmail(env, { id, created_at: now, ...cleaned }).catch((err) => {
        console.error('Email notification failed:', err && err.message ? err.message : err);
      })
    );
  }

  return jsonResponse(env, origin, 201, { ok: true, id });
}

async function handleListApplications(request, env, origin) {
  if (!requireAdmin(request, env)) return unauthorized(env, origin);
  if (!env.DB) return jsonResponse(env, origin, 500, { error: 'Database unavailable' });

  const result = await env.DB.prepare(
    `SELECT id, created_at, status, company, contact_name, email, phone, address,
            license_number, years_in_business, manufacturers, annual_volume, notes
     FROM dealer_applications
     ORDER BY created_at DESC
     LIMIT 1000`
  ).all();

  return jsonResponse(env, origin, 200, { applications: result.results || [] });
}

async function handleGetApplication(request, env, origin, id) {
  if (!requireAdmin(request, env)) return unauthorized(env, origin);
  if (!env.DB) return jsonResponse(env, origin, 500, { error: 'Database unavailable' });

  const result = await env.DB.prepare(
    `SELECT * FROM dealer_applications WHERE id = ?`
  ).bind(id).first();

  if (!result) return jsonResponse(env, origin, 404, { error: 'Not found' });
  return jsonResponse(env, origin, 200, { application: result });
}

async function handleUpdateApplication(request, env, origin, id) {
  if (!requireAdmin(request, env)) return unauthorized(env, origin);
  if (!env.DB) return jsonResponse(env, origin, 500, { error: 'Database unavailable' });

  let body;
  try { body = await request.json(); }
  catch (e) { return jsonResponse(env, origin, 400, { error: 'Invalid JSON' }); }

  if (!body || typeof body !== 'object') {
    return jsonResponse(env, origin, 400, { error: 'Invalid payload' });
  }

  if (!body.status || !ALLOWED_STATUSES.has(body.status)) {
    return jsonResponse(env, origin, 400, {
      error: 'status must be one of: ' + Array.from(ALLOWED_STATUSES).join(', '),
    });
  }

  const result = await env.DB.prepare(
    `UPDATE dealer_applications
     SET status = ?, status_updated_at = ?
     WHERE id = ?`
  ).bind(body.status, new Date().toISOString(), id).run();

  if (!result.success) {
    return jsonResponse(env, origin, 500, { error: 'Update failed' });
  }
  if ((result.meta?.changes || 0) === 0) {
    return jsonResponse(env, origin, 404, { error: 'Not found' });
  }

  return jsonResponse(env, origin, 200, { ok: true, id, status: body.status });
}

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------

function requireAdmin(request, env) {
  if (!env.ADMIN_TOKEN) return false;
  const auth = request.headers.get('Authorization') || '';
  const m = auth.match(/^Bearer\s+(.+)$/);
  if (!m) return false;
  // Constant-time-ish compare to prevent timing leaks.
  return safeCompare(m[1].trim(), env.ADMIN_TOKEN);
}

function safeCompare(a, b) {
  if (typeof a !== 'string' || typeof b !== 'string') return false;
  if (a.length !== b.length) return false;
  let out = 0;
  for (let i = 0; i < a.length; i++) out |= a.charCodeAt(i) ^ b.charCodeAt(i);
  return out === 0;
}

function corsHeaders(env, origin) {
  const allow = env.ALLOWED_ORIGIN || '*';
  // If a specific allowed origin is set, only echo it back when it matches.
  let headerValue = allow;
  if (allow !== '*' && origin && origin !== allow) {
    headerValue = allow; // Still send the configured one - browser will block.
  }
  return {
    'Access-Control-Allow-Origin': headerValue,
    'Access-Control-Allow-Methods': 'GET, POST, PATCH, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type, Authorization',
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

function unauthorized(env, origin) {
  return jsonResponse(env, origin, 401, { error: 'Unauthorized' });
}

function methodNotAllowed(env, origin) {
  return jsonResponse(env, origin, 405, { error: 'Method not allowed' });
}

// ---------------------------------------------------------------------------
// Email notification (Resend)
// ---------------------------------------------------------------------------

async function sendNewApplicationEmail(env, app) {
  if (!env.RESEND_API_KEY || !env.NOTIFY_EMAIL) {
    console.log('[email] Skipping send - RESEND_API_KEY or NOTIFY_EMAIL not configured.');
    return;
  }
  const from = env.RESEND_FROM || 'ACG Dealer Portal <noreply@acglass.com>';
  const subject = 'New ACG Dealer Application - ' + app.company;
  const lines = [
    'A new dealer application was submitted via acglass.com.',
    '',
    'Company:           ' + app.company,
    'Contact:           ' + app.contact_name,
    'Email:             ' + app.email,
    'Phone:             ' + app.phone,
    'Address:           ' + app.address,
    'License #:         ' + (app.license_number || '-'),
    'Years in Business: ' + app.years_in_business,
    'Manufacturers:     ' + app.manufacturers,
    'Annual Volume:     ' + app.annual_volume,
    '',
    'Notes:',
    app.notes || '(none)',
    '',
    '- Application ID: ' + app.id,
    '- Submitted: ' + app.created_at,
    '',
    'Review at: https://acglass.com/dealer/admin.html',
  ];
  const text = lines.join('\n');

  const res = await fetch('https://api.resend.com/emails', {
    method: 'POST',
    headers: {
      'Authorization': 'Bearer ' + env.RESEND_API_KEY,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      from,
      to: [env.NOTIFY_EMAIL],
      subject,
      text,
      reply_to: app.email,
    }),
  });
  if (!res.ok) {
    const body = await res.text().catch(() => '');
    throw new Error('Resend ' + res.status + ': ' + body);
  }
}
