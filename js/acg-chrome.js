/* ACG unified header behavior — scroll state + mobile menu toggle.
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
    burger.addEventListener('click', function () {
      var open = mobile.classList.toggle('open');
      burger.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
    mobile.querySelectorAll('a').forEach(function (a) {
      a.addEventListener('click', function () {
        mobile.classList.remove('open');
        burger.setAttribute('aria-expanded', 'false');
      });
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && mobile.classList.contains('open')) {
        mobile.classList.remove('open');
        burger.setAttribute('aria-expanded', 'false');
      }
    });
  }
})();
