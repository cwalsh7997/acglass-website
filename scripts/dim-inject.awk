# Add width=N height=N attributes to <img> tags that lack them.
# Core Web Vitals (CLS) — declared aspect ratio prevents layout shift as
# images load.
#
# Usage:
#   # 1. Build the dim map (path|WxH) for every image on disk.
#   #    Note the LAST WxH per file output to skip JPEG "density 1x1".
#   > /tmp/img-dims.txt
#   find images -type f \( -name "*.jpg" -o -name "*.jpeg" \
#                       -o -name "*.png" -o -name "*.webp" \) | while read img; do
#     dim=$(file "$img" | grep -oE '[0-9]+ ?x ?[0-9]+' | tail -1 | tr -d ' ')
#     [ -z "$dim" ] || [ "$dim" = "1x1" ] && continue
#     w=${dim%x*}; h=${dim#*x}
#     [ "$w" -lt 16 ] || [ "$h" -lt 16 ] && continue
#     echo "$img|$dim"
#   done >> /tmp/img-dims.txt
#
#   # 2. Mass-apply (CRLF preserved via the sed post-process).
#   for f in $(find . -name "*.html" -not -path './.git/*' -not -path './workers/*' \
#                   -not -path './preview/*' -not -path './node_modules/*'); do
#     [ "$f" = "./google9d45280643313cec.html" ] && continue   # NEAR-MISS #4
#     awk -f scripts/dim-inject.awk "$f" | sed 's/$/\r/' > /tmp/_.html
#     diff -q "$f" /tmp/_.html > /dev/null 2>&1 || mv /tmp/_.html "$f"
#   done
#
# Skips: imgs that already declare width OR height, empty src="",
# external/data URLs, JS template literals (${...}), and srcs whose
# normalized form isn't in the dim map (3 SVG logos on press.html
# typically — SVGs scale, no CLS benefit).
#
# ────────────────────────────────────────────────────────────────────────
# DOCUMENTED NEAR-MISSES (do not regress these):
#
# #2  BEGIN { RS = "\0"; while (getline line < "/tmp/img-dims.txt") ... }
#     Setting RS = "\0" BEFORE the getline loop makes getline read the
#     ENTIRE dim-map file as one giant record. img_w ends up with one
#     mega-key, every real lookup misses, zero rewrites. Caught by a
#     70% → 70% coverage non-change before push. Fix: load the dim map
#     FIRST with default RS, then set RS = "\0" for the main input.
#
# #3  "First > after <img>" matters for nested constructs. Earlier
#     versions of an img-rewriter on this codebase used a buffered
#     state machine that could read past the </img> closer and into
#     surrounding </picture> or </source> tags, corrupting the close.
#     This script uses `index(buf, ">")` for the FIRST > only.
#
# #4  Google verification stub (google9d45280643313cec.html) is a
#     single-line file with no trailing newline. A sed `s/$/\r/`
#     post-process appends \r → 53 bytes becomes 54 → Google's
#     exact-byte verification check fails → site ownership invalidated.
#     ALWAYS skip this file in the mass-apply loop.
# ────────────────────────────────────────────────────────────────────────

BEGIN {
  # NEAR-MISS #2: load dim map FIRST with default RS=\n, before slurp mode
  while ((getline line < "/tmp/img-dims.txt") > 0) {
    n = split(line, parts, "|")
    if (n != 2) continue
    split(parts[2], wh, "x")
    img_w[parts[1]] = wh[1]
    img_h[parts[1]] = wh[2]
  }
  close("/tmp/img-dims.txt")
  RS = "\0"
}

function process_img(buf,    src, normalized, qpos, gtpos, pre, post, w, h) {
  if (buf ~ /width="?[0-9]+"?/ || buf ~ /height="?[0-9]+"?/) return buf
  if (!match(buf, /src="[^"]*"/)) return buf
  src = substr(buf, RSTART + 5, RLENGTH - 6)
  if (src == "" || src ~ /^(https?:|data:|\/\/)/) return buf
  if (buf ~ /\$\{/) return buf
  normalized = src
  while (substr(normalized, 1, 3) == "../") normalized = substr(normalized, 4)
  if (substr(normalized, 1, 1) == "/") normalized = substr(normalized, 2)
  qpos = index(normalized, "?")
  if (qpos > 0) normalized = substr(normalized, 1, qpos - 1)
  if (!(normalized in img_w)) return buf
  # NEAR-MISS #3: FIRST > only — closes the <img>, not any wrapper
  gtpos = index(buf, ">")
  if (gtpos == 0) return buf
  pre = substr(buf, 1, gtpos - 1)
  post = substr(buf, gtpos)
  w = img_w[normalized]; h = img_h[normalized]
  if (substr(pre, length(pre), 1) == "/") {
    pre = substr(pre, 1, length(pre) - 1)
    return pre " width=\"" w "\" height=\"" h "\" /" post
  }
  return pre " width=\"" w "\" height=\"" h "\"" post
}

{
  s = $0; pos = 1; out = ""
  while (1) {
    p = index(substr(s, pos), "<img")
    if (p == 0) { out = out substr(s, pos); break }
    abs_p = pos + p - 1
    out = out substr(s, pos, abs_p - pos)
    rest = substr(s, abs_p)
    gt = index(rest, ">")
    if (gt == 0) { out = out rest; break }
    img_tag = substr(rest, 1, gt)
    out = out process_img(img_tag)
    pos = abs_p + gt
  }
  printf "%s", out
}
