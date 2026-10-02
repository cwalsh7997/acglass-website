/* Shared site chrome (architectural design, 2026-10-01): full-screen menu and header scroll state.
   Closed menu uses the hidden attribute, so its links are not focusable. Escape closes it and
   returns focus to the Menu button; Tab is kept inside the open menu. */
(function () {
  var nav = document.querySelector('.ax-nav');
  var button = document.querySelector('.ax-menu-button');
  var panel = document.getElementById('ax-navigation');
  if (nav) {
    var onScroll = function () { nav.classList.toggle('scrolled', window.scrollY > 24); };
    window.addEventListener('scroll', onScroll, { passive: true });
    onScroll();
  }
  if (!button || !panel) return;
  var setOpen = function (open, returnFocus) {
    panel.hidden = !open;
    button.setAttribute('aria-expanded', open ? 'true' : 'false');
    document.body.classList.toggle('ax-menu-open', open);
    if (!open && returnFocus) button.focus();
  };
  button.addEventListener('click', function () { setOpen(panel.hidden, false); });
  panel.querySelectorAll('a').forEach(function (a) { a.addEventListener('click', function () { setOpen(false, false); }); });
  document.addEventListener('keydown', function (e) {
    if (panel.hidden) return;
    if (e.key === 'Escape') { setOpen(false, true); return; }
    if (e.key === 'Tab') {
      var items = [button].concat(Array.prototype.slice.call(panel.querySelectorAll('a')));
      var first = items[0], last = items[items.length - 1];
      if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
      else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
    }
  });
})();
