/* Keep approved Business Profile campaign attribution with a submitted RFQ.
   Session-only, fixed campaign vocabulary, no visitor IDs or arbitrary URL data. */
(function () {
  'use strict';
  var key = 'acg_gbp_attribution_v1';
  var campaigns = ['gbp_west_palm_beach', 'gbp_stuart', 'gbp_tampa', 'gbp_naples'];
  var contents = ['website', 'storefront', 'curtainwall', 'window_wall', 'impact_windows_doors', 'folding_doors', 'fire_rated', 'automatic_entrances', 'interior_partitions'];
  var params = new URLSearchParams(window.location.search || '');
  var attribution = null;
  try {
    attribution = JSON.parse(window.sessionStorage.getItem(key) || 'null');
  } catch (error) { /* Storage restrictions must not interfere with a lead. */ }
  function valid(value) {
    return value && value.utm_source === 'google' && value.utm_medium === 'organic' &&
      campaigns.indexOf(value.utm_campaign) !== -1 && contents.indexOf(value.utm_content) !== -1;
  }
  if (!valid(attribution)) attribution = null;
  if (params.has('utm_source') || params.has('utm_campaign') || params.has('gclid')) {
    var incoming = {
      utm_source: params.get('utm_source'),
      utm_medium: params.get('utm_medium'),
      utm_campaign: params.get('utm_campaign'),
      utm_content: params.get('utm_content') || 'website'
    };
    attribution = valid(incoming) ? incoming : null;
    try {
      if (attribution) window.sessionStorage.setItem(key, JSON.stringify(attribution));
      else window.sessionStorage.removeItem(key);
    } catch (error) { /* Same-page attribution still works without storage. */ }
  }
  if (!attribution) return;
  function attach() {
    document.querySelectorAll('form').forEach(function (form) {
      // Only the existing ACG lead receiver. Never modify search or login forms.
      var receiver = /^https:\/\/formsubmit\.co\/(?:ajax\/)?connor@acglass\.com\/?$/.test(form.getAttribute('action') || '');
      // Contact builds FormData in its existing AJAX handler and has no action attribute.
      var contact = window.location.pathname === '/contact.html' && form.id === 'contact-form';
      if (!receiver && !contact) return;
      ['utm_source', 'utm_medium', 'utm_campaign', 'utm_content'].forEach(function (name) {
        var input = form.querySelector('input[name="' + name + '"]');
        if (!input) {
          input = document.createElement('input');
          input.type = 'hidden';
          input.name = name;
          form.appendChild(input);
        }
        input.value = attribution[name];
      });
    });
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', attach);
  else attach();
})();
