/* ACG unified header behavior - scroll state + mobile menu toggle.
   Self-contained; safe to load alongside legacy js/main.js. */
(function () {
  var hd = document.querySelector('.hd');
  if (hd) {
    var on = false;
    var onScroll = function () {
      var s = window.scrollY > 24;
      if (s !== on) { on = s; hd.classList.toggle('scrolled', s); }
    };
    window.addEventListener('scroll', onScroll, { passive: true });
    onScroll();
  }
  var burger = document.querySelector('.hd-burger');
  var mobile = document.querySelector('.hd-mobile');
  if (burger && mobile) {
    var setMenuState = function (open, returnFocus) {
      mobile.classList.toggle('open', open);
      burger.setAttribute('aria-expanded', open ? 'true' : 'false');
      if (open) {
        mobile.removeAttribute('inert');
      } else {
        mobile.setAttribute('inert', '');
      }
      if (returnFocus) burger.focus();
    };

    setMenuState(false, false);

    burger.addEventListener('click', function () {
      setMenuState(!mobile.classList.contains('open'), false);
    });
    mobile.querySelectorAll('a').forEach(function (a) {
      a.addEventListener('click', function () {
        setMenuState(false, false);
      });
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && mobile.classList.contains('open')) {
        setMenuState(false, true);
      }
    });
  }
})();

/* Blog / bid-day end CTA. Loads js/acg-blog-cta.js on article pages only.
   Skips /blog/index.html. The CTA script itself skips posts that already
   have a body Send Us Plans button. */
(function () {
  var path = (location.pathname || '').replace(/\\/g, '/');
  var file = path.split('/').pop() || '';
  var isTool = file === 'bid-day-glazing-checker.html';
  var isPost = path.indexOf('/blog/') !== -1 && file && file !== 'index.html';
  if (!isPost && !isTool) return;
  if (!document.querySelector('link[href*="acg-blog-cta.css"]')) {
    var link = document.createElement('link');
    link.rel = 'stylesheet';
    link.href = '/css/acg-blog-cta.css?v=20260904-blog-cta';
    (document.head || document.documentElement).appendChild(link);
  }
  var script = document.createElement('script');
  script.src = '/js/acg-blog-cta.js?v=20260904-blog-cta';
  script.defer = true;
  (document.head || document.documentElement).appendChild(script);
})();

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
      if (!/^https:\/\/formsubmit\.co\/(?:ajax\/)?connor@acglass\.com\/?$/.test(form.getAttribute('action') || '')) return;
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
