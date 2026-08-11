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
