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

/* V3 — sheet-index rail active state, horizontal strip drag/nav/progress */
(function () {
  document.addEventListener('DOMContentLoaded', function () {
    /* Rail */
    var rail = document.querySelector('.rail');
    if (rail && 'IntersectionObserver' in window) {
      var links = rail.querySelectorAll('a[href^="#"]');
      var map = {};
      links.forEach(function (a) {
        var id = a.getAttribute('href').slice(1);
        var el = id === 'top' ? document.querySelector('.hero') : document.getElementById(id);
        if (el) map[id] = { a: a, el: el.closest('section') || el };
      });
      var secIO = new IntersectionObserver(function (entries) {
        entries.forEach(function (en) {
          if (!en.isIntersecting) return;
          links.forEach(function (l) { l.classList.remove('act'); });
          Object.keys(map).forEach(function (id) {
            if (map[id].el === en.target) map[id].a.classList.add('act');
          });
          rail.classList.toggle('on-dark', en.target.classList.contains('pillars') || en.target.classList.contains('hero'));
        });
      }, { rootMargin: '-45% 0px -45% 0px' });
      Object.keys(map).forEach(function (id) { secIO.observe(map[id].el); });
    }

    /* Strip */
    var strip = document.querySelector('.strip');
    if (strip) {
      var prog = document.querySelector('.strip-progress i');
      function upd() {
        if (!prog) return;
        var max = strip.scrollWidth - strip.clientWidth;
        prog.style.width = (max > 0 ? (strip.scrollLeft / max) * 100 : 0) + '%';
      }
      strip.addEventListener('scroll', upd, { passive: true });
      upd();
      document.querySelectorAll('.strip-btn').forEach(function (btn) {
        btn.addEventListener('click', function () {
          strip.scrollBy({ left: parseInt(btn.dataset.dir, 10) * (strip.clientWidth * 0.72), behavior: 'smooth' });
        });
      });
      var down = false, startX = 0, startL = 0;
      strip.addEventListener('pointerdown', function (e) {
        if (e.pointerType !== 'mouse') return;
        down = true; startX = e.clientX; startL = strip.scrollLeft;
        strip.classList.add('dragging');
      });
      window.addEventListener('pointermove', function (e) {
        if (!down) return;
        strip.scrollLeft = startL - (e.clientX - startX);
        if (Math.abs(e.clientX - startX) > 6) strip.dataset.dragged = '1';
      });
      window.addEventListener('pointerup', function () {
        down = false; strip.classList.remove('dragging');
        setTimeout(function () { delete strip.dataset.dragged; }, 50);
      });
      strip.addEventListener('click', function (e) {
        if (strip.dataset.dragged) { e.preventDefault(); e.stopPropagation(); }
      }, true);
    }
  });
})();
