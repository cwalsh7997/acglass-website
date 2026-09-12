# Motion

Four distinct animated behaviors site-wide. That is the ceiling, not a target.
Nothing animates longer than 260ms. `transform` and `opacity` only.

| # | Behavior | Token | Properties |
|---|---|---|---|
| 1 | Hover, focus and color state change on interactive elements | `--dur-fast` 120ms | `opacity`, `color`, `border-color` |
| 2 | Disclosure, tab change, sticky header reveal | `--dur-base` 180ms | `transform`, `opacity` |
| 3 | Scroll reveal, once per element, stagger <= 60ms, one group per section | `--dur-slow` 260ms | `opacity` 0 to 1, `translateY` 8px to 0 |
| 4 | Mobile nav sheet | `--dur-slow` 260ms | `transform` |

Hover lift never exceeds `translateY(-2px)`.

## Banned

Parallax. Scroll-jacking. Pinned sections. Horizontal scroll sections. Counters.
Typewriter. Marquee. Auto-playing carousels. Animating `height`, `width`, `top`,
`box-shadow` or `filter`.

## Reduced motion

`@media (prefers-reduced-motion: reduce)` sets all three duration tokens to 1ms and
disables transforms, in `src/styles/tokens.css`. Required, and verified by committed
screenshot rather than asserted.

## Implementation

Behavior 3 is implemented with Motion (motion.dev) v13.2.0.

    js/vendor/motion-mini-13.2.0.mjs   12.1kb raw, 5.1kb gzip, vendored
    js/acg-reveal.js                    2.7kb raw, 1.4kb gzip
    css/acg-reveal.css                  1.0kb raw, 0.5kb gzip

**Vendored, not CDN.** The site is static on GitHub Pages. A `<script>` tag
pointing at jsDelivr is a third-party runtime dependency, a second point of
failure and a privacy consideration, in exchange for nothing this site needs.

**Mini build, not full.** Mini does not export `inView()`; the full build costs
9kb more and that is most of what the extra weight buys. `IntersectionObserver`
is native and free. So the browser decides WHEN and Motion decides HOW, which is
where the 5kb earns its place: WAAPI handling, easing and playback control that
a hand-rolled transition gets wrong at the edges.

**Honest note on whether Motion is needed here.** For opacity plus an 8px
translate, a CSS transition does the same job at zero bytes. Motion is worth its
weight once there is a second behavior: sequencing, interruption, spring physics,
or animating something CSS cannot reach. If behavior 3 stays the only animated
thing on the site, this could be CSS. It is Motion because the intent is to build
on it, and because the library handles interruption and cleanup correctly without
being asked.

### The rule this implementation exists to obey

Content must never be invisible because of animation code. Three failure paths,
all closed:

    no JavaScript      the hidden state is behind .js-reveal-ready, never added
    library 404s       the import is awaited BEFORE the class is added
    reduced motion     a CSS media query wins regardless of any JS state

Plus a 1.2s failsafe that drops the hidden state outright if the observer has
not fired.

### What this found in the existing site

`css/style.css` already defined `[data-reveal] { opacity: 0 }`, un-hidden by
`js/main.js` adding `.revealed`. 386 pages use it. Two problems:

1. **No `prefers-reduced-motion` handling at all.** Fixed: a media query now
   forces `[data-reveal]`, `[data-reveal-fade]` and `[data-reveal-scale]` visible.
2. **0.9s transition and 40px travel**, well outside the 260ms and 8px specified
   above. Left alone for now: changing the feel of 386 pages is a design decision,
   not a cleanup.

The new work uses `data-acg-reveal` specifically so it can never collide with the
legacy attribute. It collided during development, and because `main.js` is not
loaded on `case-studies/index.html` the cards were hidden with nothing to reveal
them.

## Undocumented behaviour found in the wild, 2026-09-09

A custom cursor follower, `.cursor-dot` and `.cursor-ring`, is defined in
`css/style.css`, `css/acg-flagship.css` and `css/acg2026.css` and driven by
`js/main.js`. It runs on the 792 pages that load main.js and is not one of the
four behaviours above.

Not removed. A cursor follower is a taste call across 792 pages, not a cleanup.
Recorded here because MOTION.md said four behaviours were the ceiling and there
were five.

Worth knowing if it stays: a custom cursor overrides the pointer the operating
system gives the user, it does nothing for touch or keyboard, and it has no
`prefers-reduced-motion` guard. The same gap the `[data-reveal]` system had.
