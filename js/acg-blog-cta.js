/* Shared blog end CTA. No build step. Injects once before author / related / footer.
   Skips posts that already have a body Send Us Plans button or Pricing this scope block. */
(function () {
  var SEND = '/send-plans.html';
  var TEL = 'tel:+17724867711';
  var PHONE = '(772) 486-7711';
  var LICENSE = 'FL CGC #1531993';

  var PROJECT_SLUGS = {
    '1172-s-harbor-glazing': 1,
    '2143-carib-circle-glazing': 1,
    '736-lagoon-dr-glazing': 1,
    'aspen-dental-edgewater-glazing': 1,
    'atlantic-fields-glazing': 1,
    'atlantic-fields-golf-house-glazing': 1,
    'atlantic-fields-performance-center-glazing': 1,
    'baron-shoppes-tradition-glazing': 1,
    'bobcat-treasure-coast-glazing': 1,
    'bradley-daytona-glazing': 1,
    'bradley-daytona-multifamily-glazing': 1,
    'causeway-building-bonita-springs-glazing': 1,
    'city-of-haines-emergency-glazing': 1,
    'compass-alton-town-center-glazing': 1,
    'cubesmart-davie-glazing': 1,
    'cudjoe-key-fire-station-glazing': 1,
    'dale-mabry-retail-tampa-glazing': 1,
    'eau-palm-beach-resort-glazing': 1,
    'el-car-wash-northlake-glazing': 1,
    'estero-vista-fort-myers-glazing': 1,
    'ginsberg-eye-center-glazing': 1,
    'gulf-harbour-country-club-glazing': 1,
    'gulfside-twelve-glazing': 1,
    'harbour-cay-fort-pierce-glazing': 1,
    'hardy-world-melbourne-glazing': 1,
    'hca-cape-coral-emergency-glazing': 1,
    'hulett-environmental-port-st-lucie-glazing': 1,
    'ifly-miami-glazing': 1,
    'illumina-fort-myers-glazing': 1,
    'imperial-crossings-bonita-springs-glazing': 1,
    'indiantown-high-school-glazing': 1,
    'klus-lighting-vero-beach-glazing': 1,
    'lake-park-innovation-center-glazing': 1,
    'lucie-at-tradition-clubhouse-glazing': 1,
    'lucie-at-tradition-glazing': 1,
    'medley-business-park-glazing': 1,
    'ocean-prime-ft-lauderdale-glazing': 1,
    'panther-national-clubhouse-glazing': 1,
    'pointe-palm-bay-glazing': 1,
    'prestige-marble-bonita-springs-glazing': 1,
    'project-lift-hobe-sound-glazing': 1,
    'savannas-ridge-clubhouse-glazing': 1,
    'shoppes-westlake-point-glazing': 1,
    'siena-lakes-naples-glazing': 1,
    'sroa-vero-beach-glazing': 1,
    'stayapt-suites-lafayette-glazing': 1,
    'storage-king-winter-haven-glazing': 1,
    'tradewinds-hobe-sound-glazing': 1,
    'turbine-technologies-jupiter-glazing': 1,
    'villa-lonz-riviera-beach-glazing': 1,
    'wave-food-hall-cocoa-beach-glazing': 1,
    'wave-haven-cocoa-beach-glazing': 1,
    'waxins-eurowall-clematis-street': 1,
    'waxins-west-palm-beach-glazing': 1,
    'westlake-hialeah-retrofit-glazing': 1,
    'wild-blue-clubhouse-glazing': 1
  };

  function slugFromPath() {
    var path = (location.pathname || '').replace(/\\/g, '/');
    var file = path.split('/').pop() || '';
    return file.replace(/\.html$/i, '');
  }

  function isRefreshStub() {
    var metas = document.getElementsByTagName('meta');
    for (var i = 0; i < metas.length; i++) {
      var equiv = metas[i].httpEquiv || metas[i].getAttribute('http-equiv') || '';
      if (equiv.toLowerCase() === 'refresh') return true;
    }
    return false;
  }

  function inChrome(el) {
    return !!(el.closest && el.closest(
      'header, nav, footer, .hd, .hd-mobile, .hd-cta, .hd-mobile-cta, .ft, .mobile-cta-bar'
    ));
  }

  function hasExistingBodyCta() {
    if (document.querySelector('.acg-blog-cta, .acg-rfq, .bdgc-cta')) return true;
    var root = document.body;
    if (!root) return false;
    if (/Pricing this scope\?/.test(root.textContent || '')) return true;
    var links = document.querySelectorAll('a[href*="send-plans"]');
    for (var i = 0; i < links.length; i++) {
      var a = links[i];
      if (inChrome(a)) continue;
      var text = ((a.textContent || '') + '').replace(/\s+/g, ' ').trim();
      var cls = a.className || '';
      var style = a.getAttribute('style') || '';
      if (
        /send us plans/i.test(text) ||
        /\bbtn\b/.test(cls) ||
        (style.indexOf('padding') !== -1 && style.indexOf('background') !== -1)
      ) {
        return true;
      }
    }
    return false;
  }

  function insertBefore() {
    var selectors = [
      '[aria-label="Related resources"]',
      '[aria-labelledby="acg-next-h"]',
      '[aria-label="About the author"]',
      'footer.ft',
      'footer'
    ];
    var found = [];
    for (var i = 0; i < selectors.length; i++) {
      var el = document.querySelector(selectors[i]);
      if (el) found.push(el);
    }
    if (!found.length) return null;
    found.sort(function (a, b) {
      return (a.compareDocumentPosition(b) & Node.DOCUMENT_POSITION_FOLLOWING) ? -1 : 1;
    });
    return found[0];
  }

  function ensureCss() {
    if (document.querySelector('link[href*="acg-blog-cta.css"]')) return;
    var link = document.createElement('link');
    link.rel = 'stylesheet';
    link.href = '/css/acg-blog-cta.css';
    (document.head || document.documentElement).appendChild(link);
  }

  function buildBlock(isProject) {
    var kicker = isProject ? 'Working a similar package?' : 'Pricing this scope?';
    var section = document.createElement('section');
    section.className = 'acg-blog-cta';
    section.setAttribute('aria-labelledby', 'acg-blog-cta-h');
    section.innerHTML =
      '<div class="acg-blog-cta-inner">' +
        '<div class="acg-blog-cta-kicker">' + kicker + '</div>' +
        '<h2 id="acg-blog-cta-h" class="acg-blog-cta-title">Send us the drawings. Scope letter back in 48 hours.</h2>' +
        '<p class="acg-blog-cta-copy">Send the elevations and the door and window schedule. Written scope back in 48 hours. ' +
          PHONE + '. ' + LICENSE + '.</p>' +
        '<div class="acg-blog-cta-actions">' +
          '<a class="acg-blog-cta-btn" href="' + SEND + '">Send Us Plans</a>' +
          '<a class="acg-blog-cta-tel" href="' + TEL + '">' + PHONE + '</a>' +
        '</div>' +
        '<p class="acg-blog-cta-print-url">acglass.com/send-plans.html</p>' +
      '</div>';
    return section;
  }

  if (isRefreshStub()) return;
  if (hasExistingBodyCta()) return;

  var target = insertBefore();
  if (!target || !target.parentNode) return;

  ensureCss();
  var slug = slugFromPath();
  target.parentNode.insertBefore(buildBlock(!!PROJECT_SLUGS[slug]), target);
})();
