#!/usr/bin/env python3
"""arch-interior-migrate.py - move page bodies onto the architectural interior theme.

Phase 2 of the redesign (phase 1, arch-chrome-migrate.py, swapped the header, menu and
footer). For every page that already carries the ax- chrome this script:

  * removes the legacy dark-theme stylesheets (style.css, acg-chrome.css, acg2026*.css,
    acg-flagship.css, acg-reveal.css) and the page's own <style> blocks,
  * links css/acg-arch-interior.css and adds body class "ax-interior",
  * wraps the content between the menu and the footer in <div class="ax-page">,
  * marks the block that holds the page's <h1> with class "ax-hero",
  * rewrites inline style attributes: layout declarations (display, grid, flex, sizing,
    position, overflow, list-style) are kept; decorative ones (colour, background, font,
    spacing, borders, shadows) are dropped and their intent is kept as a semantic class
    (ax-box, ax-btn, ax-kicker, ax-num, ax-red, ax-strong, ax-callout, ax-rule).

Interactive pages (FUNCTIONAL: forms, wizards, filters, maps, tools) keep a reduced copy of
their <style> blocks holding only behaviour (display, visibility, opacity, animations), and the
portfolio lightbox block is kept whole. Stray end tags that would close the wrapper early are
dropped and unclosed elements are closed, exactly where a browser would.

Text, links, head metadata, JSON-LD, forms, scripts and tracking are not touched.
Idempotent: pages that already have body class ax-interior are skipped.

Usage:
  python3 scripts/arch-interior-migrate.py                 # dry run, prints counts
  python3 scripts/arch-interior-migrate.py --write         # rewrite every eligible page
  python3 scripts/arch-interior-migrate.py --write a.html b/index.html   # only these
"""
from __future__ import annotations

import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
SKIP_DIRS = ("_internal/", "drafts/", "node_modules/", ".github/", "src/")
EXCLUDE = {
    "index.html",  # homepage carries its own architectural design
    "impact-windows-palm-beach.html",  # byte-frozen
    "commercial-glazier-near-me-west-palm-beach/index.html",  # byte-frozen
    "location-template-snippet.html",  # template fragment, not a page
}
# Interactive pages (forms, wizards, filters, maps, lightboxes, tools): their <style> blocks are
# reduced to the declarations that drive behaviour (display, visibility, opacity, pointer-events,
# max-height, overflow, entrance animations and their @keyframes) instead of being removed, so steps, panels and filters keep working.
FUNCTIONAL = {
    "bid.html", "send-plans.html", "contact.html", "scope-engine.html", "project-map.html",
    "free-glazing-scope-review.html", "become-a-dealer.html", "partners.html",
    "approvals/index.html", "thanks.html", "blog/index.html", "glossary/index.html",
    "infographics-index.html", "case-study-haines-city-eoc.html",
    "commercial-glazing-nashville-tn.html",
}
FUNCTIONAL_DIRS = ("tools/", "dealer/")
FUNCTIONAL_PROPS = {
    "display", "visibility", "opacity", "pointer-events", "max-height", "overflow",
    # entrance animations end at opacity:1, so they stay with the rules that start at opacity:0
    "animation", "animation-name", "animation-duration", "animation-delay", "animation-fill-mode",
    "animation-timing-function",
}
CSS_TAG = '<link rel="stylesheet" href="/css/acg-arch-interior.css?v=20261001">'
CHROME_CSS_RE = re.compile(r'<link rel="stylesheet" href="/css/acg-arch-chrome\.css\?v=\d+">')
LEGACY_CSS_RE = re.compile(
    r'<link\b[^>]*href="(?:\.\./|/)?css/(?:style|acg-chrome|acg-flagship|acg2026|acg2026-dark|acg-reveal|acg-proof)\.css[^"]*"[^>]*>[ \t]*\n?',
    re.I,
)
STYLE_BLOCK_RE = re.compile(r'[ \t]*<style\b[^>]*>.*?</style>[ \t]*\n?', re.S | re.I)
NAV_END = '<a href="tel:+17724867711">(772) 486-7711</a></div></div>'
FOOTER_START = '<footer class="ax-footer">'
RAW_RE = re.compile(r'<(script|style|svg|template|textarea)\b.*?</\1>', re.S | re.I)
TAG_RE = re.compile(r'<(/?)([a-zA-Z][a-zA-Z0-9-]*)((?:\s+[^\s>/=]+(?:\s*=\s*(?:"[^"]*"|\'[^\']*\'|[^\s>]+))?)*)\s*(/?)>')
VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "source", "track", "wbr"}

KEEP_PROPS = {
    "display", "visibility",
    "grid-template-columns", "grid-template-rows", "grid-template-areas", "grid-column", "grid-row",
    "grid-area", "grid-auto-flow", "gap", "row-gap", "column-gap",
    "flex", "flex-wrap", "flex-direction", "flex-flow", "flex-shrink", "flex-grow", "flex-basis",
    "align-items", "align-self", "align-content", "justify-content", "justify-items", "justify-self", "order",
    "width", "height", "min-width", "min-height", "max-width", "max-height", "aspect-ratio",
    "object-fit", "object-position",
    "position", "top", "right", "bottom", "left", "inset", "z-index",
    "overflow", "overflow-x", "overflow-y",
    "list-style", "list-style-type", "white-space", "vertical-align", "float", "clear", "table-layout",
}
HEADINGS = {"h1", "h2", "h3", "h4", "h5", "h6"}
TEXT_TAGS = {"div", "span", "p", "strong", "b", "em", "i", "a", "small", "li", "dt", "dd", "label", "time", "figcaption"}
BOX_TAGS = {"div", "aside", "article", "figure", "blockquote", "a", "li", "details", "form", "fieldset", "nav", "header"}


def px(value: str) -> float | None:
    """Best-effort size in px; clamp()/min()/max() use their largest operand."""
    nums = re.findall(r'(-?\d*\.?\d+)\s*(px|rem|em|vw|%)?', value)
    best = None
    for n, unit in nums:
        v = float(n)
        if unit in ("rem", "em"):
            v *= 16
        elif unit == "vw":
            v *= 14.4
        elif unit == "%":
            continue
        best = v if best is None else max(best, v)
    return best


def is_red(value: str) -> bool:
    v = value.lower()
    m = re.search(r'#([0-9a-f]{6}|[0-9a-f]{3})\b', v)
    if m:
        h = m.group(1)
        if len(h) == 3:
            h = "".join(c * 2 for c in h)
        r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
        return r > 170 and g < 110 and b < 110
    m = re.search(r'rgba?\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)', v)
    if m:
        r, g, b = (int(x) for x in m.groups())
        return r > 170 and g < 110 and b < 110
    return "var(--red" in v or "var(--accent" in v or "crimson" in v


def has_paint(value: str) -> bool:
    v = value.strip().lower()
    return bool(v) and v not in ("none", "transparent", "0", "inherit", "initial", "unset") and not v.startswith("rgba(0,0,0,0)")


def translate(tag: str, style: str) -> tuple[str, list[str]]:
    decls = []
    for part in style.split(";"):
        if ":" not in part:
            continue
        k, v = part.split(":", 1)
        decls.append((k.strip().lower(), v.strip()))
    props = dict(decls)
    keep = [(k, v) for k, v in decls if k in KEEP_PROPS]
    # Text laid over photos (absolute/fixed overlays) loses its scrim with the dark theme,
    # so it returns to normal flow below the image as a caption.
    if tag not in ("img", "picture", "video", "iframe", "svg") and props.get("position", "").lower() in ("absolute", "fixed"):
        keep = [(k, v) for k, v in keep if k not in ("position", "top", "right", "bottom", "left", "inset", "z-index")]
    if tag in ("td", "th") and props.get("text-align") == "right":
        keep.append(("text-align", "right"))
    classes: list[str] = []
    size = px(props.get("font-size", "")) if "font-size" in props else None
    upper = props.get("text-transform", "").lower() == "uppercase"
    weight = props.get("font-weight", "")
    color = props.get("color", "")
    bg = props.get("background", "") or props.get("background-color", "") or props.get("background-image", "")
    border = props.get("border", "")
    if tag not in HEADINGS and tag in TEXT_TAGS:
        if upper and (size is None or size <= 15):
            classes.append("ax-kicker")
        elif size is not None and size >= 40:
            classes.append("ax-num-xl")
        elif size is not None and size >= 26:
            classes.append("ax-num")
        elif size is not None and size >= 19 and tag in ("p", "div"):
            classes.append("ax-lead")
        elif size is not None and size <= 13 and tag in ("p", "div", "span", "small", "figcaption", "time"):
            classes.append("ax-small")
        if color and is_red(color) and tag != "a" and "ax-kicker" not in classes:
            classes.append("ax-red")
        if weight in ("600", "700", "800", "900", "bold", "bolder") and tag in ("span", "div", "a", "p"):
            classes.append("ax-strong")
    if tag == "a" and (has_paint(bg) or has_paint(border)) and "padding" in "".join(props):
        classes.append("ax-btn-primary" if is_red(bg) else "ax-btn")
    elif tag in BOX_TAGS and (has_paint(bg) or (has_paint(border) and not border.startswith("0"))):
        classes.append("ax-box")
    elif tag in BOX_TAGS | {"section", "p"} and has_paint(props.get("border-left", "")) and (px(props["border-left"]) or 0) >= 2:
        classes.append("ax-callout")
    elif tag in BOX_TAGS | {"section", "p", "ul", "ol", "table"} and (
        has_paint(props.get("border-top", "")) or has_paint(props.get("border-bottom", ""))
    ):
        classes.append("ax-rule")
    if tag == "ul" and props.get("list-style", props.get("list-style-type", "")).startswith("none"):
        classes.append("ax-plain-list")
    return ";".join(f"{k}:{v}" for k, v in keep), classes


def set_attr(attrs: str, name: str, value: str | None) -> str:
    pat = re.compile(r'\s' + name + r'\s*=\s*("[^"]*"|\'[^\']*\'|[^\s>]+)', re.I)
    if value is None:
        return pat.sub("", attrs, count=1)
    if pat.search(attrs):
        return pat.sub(f' {name}="{value}"', attrs, count=1)
    return attrs + f' {name}="{value}"'


def get_attr(attrs: str, name: str) -> str | None:
    m = re.search(r'\s' + name + r'\s*=\s*("([^"]*)"|\'([^\']*)\'|([^\s>]+))', attrs, re.I)
    if not m:
        return None
    return next(g for g in m.groups()[1:] if g is not None)


def add_classes(attrs: str, extra: list[str]) -> str:
    if not extra:
        return attrs
    current = (get_attr(attrs, "class") or "").split()
    merged = current + [c for c in extra if c not in current]
    return set_attr(attrs, "class", " ".join(merged))


# Elements whose end tag a browser will not close across (HTML "special" category, abridged).
SPECIAL = {
    "address", "article", "aside", "blockquote", "details", "dd", "div", "dl", "dt", "fieldset",
    "figcaption", "figure", "footer", "form", "h1", "h2", "h3", "h4", "h5", "h6", "header", "hgroup",
    "li", "main", "menu", "nav", "ol", "p", "pre", "section", "summary", "table", "tbody", "td",
    "tfoot", "th", "thead", "tr", "ul", "button", "select", "textarea", "iframe", "object",
}
SCOPE_STOP = {"table", "td", "th", "caption", "object", "template", "html"}
CLOSES_P = {
    "address", "article", "aside", "blockquote", "details", "div", "dl", "fieldset", "figcaption",
    "figure", "footer", "form", "h1", "h2", "h3", "h4", "h5", "h6", "header", "hgroup", "hr", "main",
    "menu", "nav", "ol", "p", "pre", "section", "summary", "table", "ul",
}


def strip_style_blocks(html: str) -> str:
    """Remove <style> blocks, except those inside inline SVG (they style the drawing)."""
    svgs = [(m.start(), m.end()) for m in re.finditer(r'<svg\b.*?</svg>', html, re.S | re.I)]
    def keep(m: re.Match) -> bool:
        # Inline SVG styles, and the portfolio project lightbox (a self-contained modal).
        return any(a <= m.start() < b for a, b in svgs) or ".plb-overlay{" in m.group(0)

    return STYLE_BLOCK_RE.sub(lambda m: m.group(0) if keep(m) else "", html)


def functional_css(css: str) -> str:
    """Keep only behaviour-driving declarations of a stylesheet, preserving @media/@supports
    nesting. Decorative rules (colour, type, spacing) are dropped."""
    css = re.sub(r"/\*.*?\*/", "", css, flags=re.S)
    out: list[str] = []
    i = 0
    while i < len(css):
        brace = css.find("{", i)
        if brace < 0:
            break
        prelude = css[i:brace].strip()
        depth, j = 1, brace + 1
        while j < len(css) and depth:
            depth += {"{": 1, "}": -1}.get(css[j], 0)
            j += 1
        body = css[brace + 1 : j - 1]
        if prelude.startswith(("@keyframes", "@-webkit-keyframes")):
            out.append(f"{prelude}{{{body}}}")
        elif prelude.startswith(("@media", "@supports")):
            inner = functional_css(body)
            if inner:
                out.append(f"{prelude}{{{inner}}}")
        elif not prelude.startswith("@"):
            decls = [d.strip() for d in body.split(";") if ":" in d]
            # Custom properties stay: kept rules reference them (e.g. animation easing).
            kept = [d for d in decls if (lambda p: p in FUNCTIONAL_PROPS or p.startswith("--"))(d.split(":", 1)[0].strip().lower())]
            if kept:
                out.append(f"{prelude}{{{';'.join(kept)}}}")
        i = j
    return "".join(out)


def reduce_style_blocks(html: str) -> str:
    """For interactive pages: each <style> block keeps only its functional declarations."""
    def repl(m: re.Match) -> str:
        inner = re.search(r"<style\b[^>]*>(.*?)</style>", m.group(0), re.S | re.I)
        kept = functional_css(inner.group(1)) if inner else ""
        return f"<style>{kept}</style>\n" if kept else ""
    return STYLE_BLOCK_RE.sub(repl, html)


def balance(segment: str) -> str:
    """Drop end tags a browser ignores and close elements left open, so the .ax-page
    wrapper's own </div> cannot be consumed by legacy markup. Rendering is unchanged:
    an ignored end tag is a no-op, and an unclosed element is closed at the same point
    the browser would close it anyway."""
    masked = RAW_RE.sub(lambda m: " " * len(m.group(0)), segment)
    stack: list[str] = []
    drop: list[tuple[int, int]] = []

    def in_scope(tag: str) -> bool:
        for t in reversed(stack):
            if t == tag:
                return True
            if t in SCOPE_STOP:
                return False
        return False

    for m in TAG_RE.finditer(masked):
        closing, tag = m.group(1), m.group(2).lower()
        if tag in VOID or m.group(4):
            continue
        if not closing:
            if tag in CLOSES_P and in_scope("p"):
                while stack and stack.pop() != "p":
                    pass
            if tag == "li":
                for i in range(len(stack) - 1, -1, -1):
                    if stack[i] == "li":
                        del stack[i:]
                        break
                    if stack[i] in SPECIAL and stack[i] not in ("address", "div", "p"):
                        break
            if tag in ("dt", "dd"):
                for i in range(len(stack) - 1, -1, -1):
                    if stack[i] in ("dt", "dd"):
                        del stack[i:]
                        break
                    if stack[i] in SPECIAL and stack[i] not in ("address", "div", "p"):
                        break
            stack.append(tag)
            continue
        if tag == "p" and not in_scope("p"):
            continue  # browser inserts an empty <p>; leave the source as it is
        if tag in SPECIAL:
            if in_scope(tag):
                while stack and stack.pop() != tag:
                    pass
            else:
                drop.append((m.start(), m.end()))
            continue
        for i in range(len(stack) - 1, -1, -1):
            if stack[i] == tag:
                del stack[i:]
                break
            if stack[i] in SPECIAL:
                drop.append((m.start(), m.end()))
                break
        else:
            drop.append((m.start(), m.end()))
    for start, end in reversed(drop):
        segment = segment[:start] + segment[end:]
    return segment + "".join(f"</{t}>" for t in reversed(stack))


def hero_size(segment: str) -> str:
    """ax-hero-s/m/l by h1 length, so a 90-character h1 does not set at 118px."""
    m = re.search(r'<h1\b[^>]*>(.*?)</h1>', segment, re.S | re.I)
    words = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", m.group(1) if m else "")).strip()
    return "ax-hero-s" if len(words) <= 32 else "ax-hero-m" if len(words) <= 60 else "ax-hero-l"


def rewrite_tags(segment: str, hero_at: int | None) -> str:
    """Rewrite inline styles in a body segment, skipping raw blocks (script, svg, ...)."""
    out = []
    last = 0
    raw_spans = [(m.start(), m.end()) for m in RAW_RE.finditer(segment)]
    raw_iter = iter(raw_spans)
    nxt = next(raw_iter, None)
    for m in TAG_RE.finditer(segment):
        while nxt and m.start() >= nxt[1]:
            nxt = next(raw_iter, None)
        if nxt and nxt[0] <= m.start() < nxt[1] and m.start() != nxt[0]:
            continue
        closing, tag, attrs, selfclose = m.group(1), m.group(2).lower(), m.group(3), m.group(4)
        if closing:
            continue
        new_attrs = attrs
        extra: list[str] = []
        style = get_attr(attrs, "style")
        if style is not None and tag != "svg":
            kept, extra = translate(tag, style)
            new_attrs = set_attr(new_attrs, "style", kept or None)
            if get_attr(attrs, "class") is not None:
                extra = []  # a component class already carries the styling; keep class strings exact
        if hero_at is not None and m.start() == hero_at:
            extra = extra + ["ax-hero", hero_size(segment)]
        new_attrs = add_classes(new_attrs, extra)
        if new_attrs != attrs:
            out.append(segment[last:m.start()])
            out.append(f"<{m.group(2)}{new_attrs}{' /' if selfclose else ''}>")
            last = m.end()
    out.append(segment[last:])
    return "".join(out)


def find_hero(segment: str) -> int | None:
    """Offset of the outermost content block that contains the first <h1>."""
    h1 = re.search(r'<h1\b', segment, re.I)
    if not h1:
        return None
    stack: list[tuple[str, int]] = []
    masked = RAW_RE.sub(lambda m: " " * len(m.group(0)), segment[: h1.start()])
    for m in TAG_RE.finditer(masked):
        closing, tag = m.group(1), m.group(2).lower()
        if tag in VOID or m.group(4):
            continue
        if not closing:
            stack.append((tag, m.start()))
        else:
            while stack:
                t, _ = stack.pop()
                if t == tag:
                    break
    # Skip pure wrappers (main/article/div.ax-page level wrappers) to reach the hero block.
    for tag, start in stack:
        if tag in ("main", "article"):
            continue
        return start
    return None


def migrate(text: str, functional: bool = False) -> tuple[str, str]:
    if 'class="ax-nav"' not in text:
        return text, "no-chrome"
    if re.search(r'<body[^>]*class="[^"]*\bax-interior\b', text):
        return text, "already"
    if 'http-equiv="refresh' in text.lower():
        return text, "stub"
    # Phase 1 left a legacy <header role="banner"> wrapping the new chrome on a few pages
    # (noa/*). Unwrap it so the chrome, page and footer are siblings under <body>.
    wrapped = re.search(r'<header role="banner">\s*(?=<header class="ax-nav">)', text)
    if wrapped:
        close = re.compile(r'\s*</header>').match(text, text.find(NAV_END) + len(NAV_END))
        if close:
            text = text[: close.start()] + text[close.end():]
            text = text[: wrapped.start()] + text[wrapped.end():]
    start = text.find(NAV_END)
    end = text.find(FOOTER_START)
    if start < 0 or end < 0 or end < start:
        return text, "no-anchors"
    start += len(NAV_END)
    segment = text[start:end]
    segment = balance(reduce_style_blocks(segment) if functional else strip_style_blocks(segment))
    segment = rewrite_tags(segment, find_hero(segment))
    text = text[:start] + '<div class="ax-page">' + segment + "</div>" + text[end:]
    head_end = text.lower().find("</head>")
    head = LEGACY_CSS_RE.sub("", text[:head_end])
    head = reduce_style_blocks(head) if functional else STYLE_BLOCK_RE.sub("", head)
    if not CHROME_CSS_RE.search(head):
        return text, "no-chrome-css"
    head = CHROME_CSS_RE.sub(lambda m: m.group(0) + "\n" + CSS_TAG, head, count=1)
    text = head + text[head_end:]
    body = re.search(r'<body\b([^>]*)>', text)
    if body is None:
        return text, "no-body"
    text = text[: body.start()] + f"<body{add_classes(body.group(1), ['ax-interior'])}>" + text[body.end():]
    # Legacy stylesheets referenced after </head> (rare) are removed too.
    text = LEGACY_CSS_RE.sub("", text)
    return text, "migrated"


def main() -> int:
    write = "--write" in sys.argv
    only = [a for a in sys.argv[1:] if not a.startswith("--")]
    counts: dict[str, int] = {}
    examples: dict[str, str] = {}
    paths = [ROOT / p for p in only] if only else sorted(ROOT.rglob("*.html"))
    for path in paths:
        rel = path.relative_to(ROOT).as_posix()
        if not only and (rel.startswith(SKIP_DIRS) or rel in EXCLUDE):
            continue
        old = path.read_text(encoding="utf-8")
        new, status = migrate(old, functional=rel in FUNCTIONAL or rel.startswith(FUNCTIONAL_DIRS))
        counts[status] = counts.get(status, 0) + 1
        examples.setdefault(status, rel)
        if write and new != old:
            path.write_text(new, encoding="utf-8")
    for status, n in sorted(counts.items(), key=lambda kv: -kv[1]):
        print(f"{n:5} {status}  e.g. {examples[status]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
