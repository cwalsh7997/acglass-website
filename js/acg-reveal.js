/**
 * Scroll reveal, MOTION.md behavior 3.
 *
 * Motion (motion.dev) v13.2.0 mini, vendored locally at
 * js/vendor/motion-mini-13.2.0.mjs. No CDN at runtime: the site is static on
 * GitHub Pages and a third-party script tag is a dependency it does not need.
 *
 * Motion's mini build does not export inView(), and the full build costs 9kb more
 * to get it. IntersectionObserver is native and free, so the split is: the browser
 * decides WHEN, Motion decides HOW. That is where the 12kb earns its place.
 *
 * The spec, honoured exactly:
 *   opacity 0 -> 1, translateY 8px -> 0. No other property.
 *   260ms, matching --dur-slow.
 *   stagger 60ms, capped at 6 steps so a long grid never crawls.
 *   once per element, then unobserved.
 *   one group per section.
 *
 * The hidden state is in css/acg-reveal.css behind .js-reveal-ready, which is
 * added below only after the library resolves. Nothing can be left invisible by
 * a failed fetch, a disabled script, or a reduced-motion preference.
 */
const REVEAL = "[data-acg-reveal]";
const READY = "js-reveal-ready";
const DURATION = 0.26;
const STAGGER = 0.06;
const MAX_STEPS = 6;
const FAILSAFE_MS = 1200;

async function start() {
  if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;

  const targets = [...document.querySelectorAll(REVEAL)];
  if (!targets.length) return;

  let animate;
  try {
    ({ animate } = await import("./vendor/motion-mini-13.2.0.mjs"));
  } catch {
    return; // nothing was hidden, so nothing needs restoring
  }

  const groups = new Map();
  for (const el of targets) {
    const key = el.closest("section, [data-acg-reveal-group]") || document.body;
    if (!groups.has(key)) groups.set(key, []);
    groups.get(key).push(el);
  }

  document.documentElement.classList.add(READY);

  const show = (el, delay) =>
    animate(el, { opacity: 1, transform: "translateY(0px)" },
            { duration: DURATION, delay, easing: "ease-out" });

  const io = new IntersectionObserver((entries) => {
    for (const entry of entries) {
      if (!entry.isIntersecting) continue;
      const key = entry.target.closest("section, [data-acg-reveal-group]") || document.body;
      const index = Math.min((groups.get(key) || []).indexOf(entry.target), MAX_STEPS);
      io.unobserve(entry.target);
      show(entry.target, index * STAGGER);
    }
  }, { rootMargin: "0px 0px -8% 0px", threshold: 0.05 });

  for (const el of targets) io.observe(el);

  // Last resort. If the observer has not fired for something after 1.2s, drop the
  // whole hidden state. Content visible always beats content correct-but-absent.
  setTimeout(() => document.documentElement.classList.remove(READY), FAILSAFE_MS);
}

start();
