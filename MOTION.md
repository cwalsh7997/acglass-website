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
