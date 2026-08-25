/* ACG conversion tracking - standalone, no UI side effects.
 *
 * Why this file exists: js/main.js carries the GA4 conversion events AND the
 * custom cursor, nav-scroll, mobile nav and sticky CTA bar. Adding main.js to a
 * page that was not built for it changes how the page looks and behaves. As of
 * 2026-07-29, 731 of 1,504 indexable pages had no conversion tracking at all
 * because of that coupling - roughly half the site could not report a lead,
 * which is the site's north-star metric.
 *
 * This file is the tracking half only. It is safe on every page.
 *
 * Loaded on pages that do NOT load main.js. The two sets are disjoint, so no
 * event double-fires; the guard below makes that true even if they ever overlap.
 *
 * Follow-up (not done here - it would touch 773 working pages for no
 * measurement gain): delete the GA4 block from main.js and load this file
 * everywhere, so the event definitions live in exactly one place.
 */
(function () {
  'use strict';
  if (window.__acgTrackInit) return;   // idempotent: never double-bind
  window.__acgTrackInit = true;

  function trackEvent(name, params) {
    params = params || {};
    if (typeof gtag === 'function') {
      gtag('event', name, params);
    }
    if (window.dataLayer) {
      window.dataLayer.push(Object.assign({ event: name }, params));
    }
  }

  function init() {
    var path = location.pathname;

    document.querySelectorAll('a[href^="tel:"]').forEach(function (a) {
      a.addEventListener('click', function () {
        trackEvent('phone_click', {
          phone_number: a.getAttribute('href').replace('tel:', ''),
          page_location: path
        });
      });
    });

    document.querySelectorAll('a[href^="mailto:"]').forEach(function (a) {
      a.addEventListener('click', function () {
        trackEvent('email_click', {
          email_address: a.getAttribute('href').replace('mailto:', ''),
          page_location: path
        });
      });
    });

    document.querySelectorAll('a').forEach(function (a) {
      var text = (a.textContent || '').trim().toLowerCase();
      var href = a.getAttribute('href') || '';
      if (text.indexOf('send us plans') !== -1 ||
          text.indexOf('submit plans') !== -1 ||
          text === 'send plans' ||
          /send-plans\.html$/.test(href)) {
        a.addEventListener('click', function () {
          trackEvent('cta_submit_plans_click', {
            cta_text: (a.textContent || '').trim(),
            page_location: path,
            cta_href: href
          });
        });
      }
    });

    document.querySelectorAll('a[href$=".pdf"]').forEach(function (a) {
      a.addEventListener('click', function () {
        trackEvent('resource_download', {
          file_name: (a.getAttribute('href') || '').split('/').pop(),
          file_url: a.getAttribute('href'),
          link_text: (a.textContent || '').trim()
        });
      });
    });

    // A submit event records intent, not confirmed delivery. Success events must
    // come from the form's delivery handler after the receiving service responds.
    document.querySelectorAll('form').forEach(function (f) {
      f.addEventListener('submit', function () {
        trackEvent('form_submit_attempt', {
          form_id: f.getAttribute('id') || f.getAttribute('name') || 'unnamed',
          form_action: f.getAttribute('action') || '',
          page_location: path
        });
      });
    });

    if (path.indexOf('scope-engine') !== -1) {
      trackEvent('scope_engine_start', { page_location: path });
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
