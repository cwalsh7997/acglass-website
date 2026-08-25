/* ACG Dealer Portal - client-side scripts
 *
 * Phase 1 responsibility:
 *   - Handle the dealer-application form on /become-a-dealer.html.
 *   - POST to the Cloudflare Worker API if it's deployed and reachable.
 *   - Fall back to a mailto: link if the API isn't configured or fails,
 *     so leads always reach connor@acglass.com regardless of backend state.
 *
 * To wire up the live API after deploying the Worker:
 *   1. Set window.ACG_DEALER_API on become-a-dealer.html (or globally) to
 *      the Worker's public URL, e.g. "https://acg-dealer-portal-api.<your-subdomain>.workers.dev"
 *      or your custom subdomain "https://api.acglass.com".
 *   2. The form will start using it automatically; no page edits required.
 */

(function () {
  'use strict';

  // ---- Config -----------------------------------------------------------
  // Resolve the API base URL in this priority:
  //   1. window.ACG_DEALER_API  (set by inline script on a page if needed)
  //   2. <meta name="acg-dealer-api" content="...">  (set per-page or sitewide)
  //   3. null  → mailto fallback only
  function resolveApiBase() {
    if (typeof window.ACG_DEALER_API === 'string' && window.ACG_DEALER_API.length > 0) {
      return window.ACG_DEALER_API.replace(/\/$/, '');
    }
    var meta = document.querySelector('meta[name="acg-dealer-api"]');
    if (meta && meta.content) return meta.content.replace(/\/$/, '');
    return null;
  }

  var API_BASE = resolveApiBase();
  var APPLY_ENDPOINT = API_BASE ? API_BASE + '/api/applications' : null;
  var FALLBACK_EMAIL = 'connor@acglass.com';

  // ---- Helpers ----------------------------------------------------------
  function setStatus(el, kind, msg) {
    if (!el) return;
    el.className = 'dealer-status is-' + kind;
    el.textContent = msg;
  }

  function setLoading(btn, loading) {
    if (!btn) return;
    if (loading) {
      btn.classList.add('is-loading');
      btn.setAttribute('disabled', 'disabled');
    } else {
      btn.classList.remove('is-loading');
      btn.removeAttribute('disabled');
    }
  }

  function safeGtag() {
    return typeof window.gtag === 'function' ? window.gtag : function () {};
  }

  function buildMailto(payload) {
    var subject = 'ACG Dealer Application - ' + (payload.company || payload.contact_name || 'New');
    var lines = [
      'Company: ' + (payload.company || ''),
      'Contact: ' + (payload.contact_name || ''),
      'Email: ' + (payload.email || ''),
      'Phone: ' + (payload.phone || ''),
      'Address: ' + (payload.address || ''),
      'License #: ' + (payload.license_number || ''),
      'Years in Business: ' + (payload.years_in_business || ''),
      'Manufacturers: ' + (payload.manufacturers || ''),
      'Annual Volume: ' + (payload.annual_volume || ''),
      '',
      'Notes:',
      payload.notes || '(none)',
      '',
      '- Submitted from acglass.com/become-a-dealer.html'
    ];
    return 'mailto:' + FALLBACK_EMAIL + '?subject=' + encodeURIComponent(subject) +
      '&body=' + encodeURIComponent(lines.join('\n'));
  }

  // ---- Application form handler ----------------------------------------
  function initApplicationForm() {
    var form = document.getElementById('dealer-application-form');
    if (!form) return;

    var btn = document.getElementById('dealer-submit-btn');
    var status = document.getElementById('dealer-form-status');
    var startedTracking = false;

    form.addEventListener('focusin', function () {
      if (!startedTracking) {
        safeGtag()('event', 'dealer_application_start', { page_location: location.pathname });
        startedTracking = true;
      }
    });

    form.addEventListener('submit', function (e) {
      e.preventDefault();

      // Honeypot: if filled, silently "succeed" (don't tell the bot it failed).
      var honey = form.querySelector('input[name="company_url"]');
      if (honey && honey.value) {
        setStatus(status, 'success', 'Thanks - we\'ll be in touch.');
        form.reset();
        return;
      }

      // Build payload
      var data = new FormData(form);
      var payload = {};
      data.forEach(function (value, key) {
        if (key === 'company_url') return; // never send honeypot
        payload[key] = (typeof value === 'string') ? value.trim() : value;
      });

      // Minimum required fields (defensive - HTML5 also enforces)
      var required = ['company', 'contact_name', 'email', 'phone', 'address', 'years_in_business', 'manufacturers', 'annual_volume'];
      var missing = required.filter(function (k) { return !payload[k]; });
      if (missing.length) {
        setStatus(status, 'error', 'Please fill in: ' + missing.join(', '));
        return;
      }

      // Email sanity check
      if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(payload.email)) {
        setStatus(status, 'error', 'That email address doesn\'t look right.');
        return;
      }

      safeGtag()('event', 'dealer_application_submit', {
        manufacturers: payload.manufacturers || '',
        annual_volume: payload.annual_volume || '',
        page_location: location.pathname
      });

      // If the API is configured, try it first. On any failure, mailto fallback.
      if (APPLY_ENDPOINT) {
        setLoading(btn, true);
        setStatus(status, 'info', 'Submitting…');

        var controller = (typeof AbortController === 'function') ? new AbortController() : null;
        var timeout = controller ? setTimeout(function () { controller.abort(); }, 12000) : null;

        fetch(APPLY_ENDPOINT, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload),
          signal: controller ? controller.signal : undefined
        }).then(function (res) {
          if (timeout) clearTimeout(timeout);
          if (res.ok) {
            // Hand off to thanks page
            window.location.href = 'dealer/thanks.html';
            return;
          }
          return res.json().catch(function () { return {}; }).then(function (body) {
            throw new Error((body && body.error) || ('HTTP ' + res.status));
          });
        }).catch(function (err) {
          if (timeout) clearTimeout(timeout);
          setLoading(btn, false);
          // Fallback to mailto so the lead still reaches Connor.
          setStatus(status, 'info',
            'Opening your email client as a fallback. If nothing happens, please email ' +
            FALLBACK_EMAIL + ' directly.'
          );
          window.location.href = buildMailto(payload);
        });
      } else {
        // No API configured - mailto fallback (matches existing contact form pattern)
        setStatus(status, 'info',
          'Opening your email client. If nothing happens, please email ' + FALLBACK_EMAIL + ' directly.'
        );
        window.location.href = buildMailto(payload);
      }
    });
  }

  // ---- Init -------------------------------------------------------------
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initApplicationForm);
  } else {
    initApplicationForm();
  }
})();
