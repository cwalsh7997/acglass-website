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
    link.href = '/css/acg-blog-cta.css';
    (document.head || document.documentElement).appendChild(link);
  }
  var script = document.createElement('script');
  script.src = '/js/acg-blog-cta.js';
  script.defer = true;
  (document.head || document.documentElement).appendChild(script);
})();
