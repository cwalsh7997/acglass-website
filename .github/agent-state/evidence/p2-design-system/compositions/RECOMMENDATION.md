# Hero composition: recommendation

**Take A, the split.** Five lines, measured, no mood language.

1. B fails WCAG on this photograph. Measured against the rendered backdrop with the
   copy hidden: eyebrow 1.34:1, h1 2.02:1. The thresholds are 4.5:1 and 3:1.
2. rules/01 already decides what to do about that: "the text must still measure
   >=4.5:1 against the darkest sampled region. If it does not, move the text out of
   the image." A moves it out.
3. A's text sits on paper. navy-800 on white is 14.63:1, recorded in tokens.css and
   not dependent on which photograph ships.
4. B makes every future hero image carry a contrast requirement. A photo dark enough
   for white text is a real constraint on a company whose proof shots are daylight
   exteriors.
5. A keeps the mandated 4:3 hero ratio and never goes full-bleed, which rules/01
   requires on the homepage. B satisfies both too, so this is not the deciding factor.

## What is not being claimed

B is not unusable. Its `lead` run measures 6.11:1 and passes. With a darker photograph
B could pass everywhere. The measurement is against **this** image, and the point is
that A's contrast does not depend on the image at all.

## Measurement method

`--headless --screenshot` at 1440x900, copy set to `visibility:hidden` so layout is
preserved and only the backdrop is sampled, then worst-case (lightest) pixel per text
band compared against the foreground token. Sampling the rendered page with text
visible measures the text against itself and reports 1.00:1, which is what my first
two attempts did.
