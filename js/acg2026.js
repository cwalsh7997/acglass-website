/* ACG 2026 — header, mobile nav, scroll reveals. No dependencies. */
(function () {
  'use strict';
  document.documentElement.classList.add('js');
  document.body && document.body.classList.add('js');
  document.addEventListener('DOMContentLoaded', function () {
    document.body.classList.add('js');

    /* Header state */
    var hd = document.querySelector('.hd');
    var lastY = 0;
    function onScroll() {
      var y = window.scrollY;
      if (hd) hd.classList.toggle('scrolled', y > 24);
      lastY = y;
    }
    onScroll();
    window.addEventListener('scroll', onScroll, { passive: true });

    /* Mobile menu */
    var burger = document.querySelector('.hd-burger');
    var mobile = document.querySelector('.hd-mobile');
    if (burger && mobile) {
      burger.addEventListener('click', function () {
        var open = mobile.classList.toggle('open');
        burger.setAttribute('aria-expanded', open ? 'true' : 'false');
        if (open && hd) hd.classList.add('scrolled');
      });
      mobile.addEventListener('click', function (e) {
        if (e.target.tagName === 'A') {
          mobile.classList.remove('open');
          burger.setAttribute('aria-expanded', 'false');
        }
      });
    }

    /* Scroll reveals */
    var reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    var items = document.querySelectorAll('.rv, .rv-l');
    if (reduced || !('IntersectionObserver' in window)) {
      items.forEach(function (el) { el.classList.add('in'); });
    } else {
      document.querySelectorAll('[data-stagger]').forEach(function (group) {
        Array.prototype.forEach.call(group.children, function (child, i) {
          child.style.setProperty('--i', i);
        });
      });
      var io = new IntersectionObserver(function (entries) {
        entries.forEach(function (en) {
          if (en.isIntersecting) {
            en.target.classList.add('in');
            io.unobserve(en.target);
          }
        });
      }, { rootMargin: '0px 0px -8% 0px', threshold: 0.08 });
      items.forEach(function (el) { io.observe(el); });
    }
  });
})();

/* Magnetic CTAs — subtle pull toward cursor (desktop, fine pointers only) */
(function () {
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  if (!window.matchMedia('(pointer: fine)').matches) return;
  document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('.btn-red, .btn-navy, .hd-cta, .cta-in .btn').forEach(function (btn) {
      btn.addEventListener('mousemove', function (e) {
        var r = btn.getBoundingClientRect();
        var x = (e.clientX - r.left - r.width / 2) / r.width;
        var y = (e.clientY - r.top - r.height / 2) / r.height;
        btn.style.transform = 'translate(' + (x * 6) + 'px,' + (y * 5) + 'px)';
      });
      btn.addEventListener('mouseleave', function () { btn.style.transform = ''; });
    });
  });
})();
