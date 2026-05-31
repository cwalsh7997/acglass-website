# Add loading="lazy" and decoding="async" to <img> tags that lack them.
#
# Usage:
#   for f in $(find . -name "*.html" -not -path './.git/*' -not -path './workers/*' \
#                   -not -path './preview/*' -not -path './node_modules/*'); do
#     [ "$f" = "./google9d45280643313cec.html" ] && continue   # see NEAR-MISS #4
#     awk -f scripts/lazy-async-inject.awk "$f" | sed 's/$/\r/' > /tmp/_.html
#     diff -q "$f" /tmp/_.html > /dev/null 2>&1 || mv /tmp/_.html "$f"
#   done
#
# Skip conditions for loading="lazy":
#   - <img> already has loading="(lazy|eager)" — don't override
#   - <img> has fetchpriority="high"   — LCP marker, must load eager
#   - <img> has loading="eager"        — explicit eager intent (redundant
#                                        with the first rule but explicit)
#   - <img> src="" (lightbox JS placeholders)
#   - <img> contains a JS template literal ${...}
#
# Skip conditions for decoding="async":
#   - <img> already has decoding=
#   - <img> src="" / template literals (same as above)
#   decoding="async" is safe on LCP imgs — async decoding happens off the
#   main thread and does not gate paint.
#
# ────────────────────────────────────────────────────────────────────────
# DOCUMENTED NEAR-MISS (do not regress these):
#
# #1  lazy + fetchpriority="high" collision.
#     The first version of this awk only checked `loading="eager"` for
#     LCP-protection. But many imgs on this codebase use
#     `fetchpriority="high"` *without* `loading="eager"` — most notably
#     the ACG nav logo (height=72 width=338) which appears in the
#     page-top nav on every page. Result: 674 LCP-critical imgs across
#     671 files ended up with BOTH `loading="lazy"` AND
#     `fetchpriority="high"`, which conflict — fetchpriority signals
#     LCP-critical but lazy still defers until viewport intersection.
#     LCP regressed on every page. Caught post-deploy by Computer; fixed
#     site-wide at commit 8c6b5a74. THIS SCRIPT now skips on either
#     loading="eager" OR fetchpriority="high".
#
# #2  ALSO see scripts/dim-inject.awk: BEGIN { RS="\0" } before a getline
#     from a side file breaks the side file's record parsing. Always set
#     RS = "\0" AFTER loading any dim/lookup maps via getline.
# ────────────────────────────────────────────────────────────────────────

BEGIN { RS = "\0" }

function process_img(buf,    has_loading, has_decoding, has_fp_high, gtpos, pre, post, add_loading, add_decoding, extra) {
  if (buf ~ /\$\{/) return buf
  if (buf ~ /src=""/) return buf

  has_loading  = (buf ~ /loading="(lazy|eager)"/)
  has_decoding = (buf ~ /decoding="(async|sync|auto)"/)
  has_fp_high  = (buf ~ /fetchpriority="high"/)

  # NEAR-MISS #1: skip on either eager-loading OR fp=high
  add_loading  = (!has_loading && !has_fp_high)
  add_decoding = (!has_decoding)

  if (!add_loading && !add_decoding) return buf

  gtpos = index(buf, ">")
  if (gtpos == 0) return buf
  pre = substr(buf, 1, gtpos - 1)
  post = substr(buf, gtpos)

  extra = ""
  if (add_loading)  extra = extra " loading=\"lazy\""
  if (add_decoding) extra = extra " decoding=\"async\""

  # Self-closing /> ?
  if (substr(pre, length(pre), 1) == "/") {
    pre = substr(pre, 1, length(pre) - 1)
    return pre extra " /" post
  }
  return pre extra post
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
