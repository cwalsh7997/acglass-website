# Inject Privacy + Terms links into every <div class="footer-bottom">
# block on the page, before its matching </div>.
#
# Usage:
#   for f in $(find . -name "*.html" -not -path './.git/*' -not -path './workers/*' \
#                   -not -path './preview/*' -not -path './node_modules/*'); do
#     grep -q 'class="footer-bottom"' "$f" || continue
#     awk -f scripts/inject-legal-footer.awk "$f" \
#       | sed 's/$/\r/' > /tmp/_.html
#     diff -q "$f" /tmp/_.html > /dev/null 2>&1 || mv /tmp/_.html "$f"
#   done
#
#   # partners.html uses a "lp-footer-bottom" variant — hand-edit that one.
#
# Handles three footer-bottom shapes that exist on this site:
#   1. Single-line: <div class="footer-bottom"><span>...</span></div>
#   2. Multi-line with <span> children (most pages)
#   3. Multi-line with nested <div> children (WPB landing page —
#      storefront-glazier-west-palm-beach-florida/index.html)
#
# Uses depth-tracking on <div / </div> so the correct OUTER </div>
# gets the injection — naive "first </div> after open" breaks on
# nested-div variants.
#
# IDEMPOTENT: if the footer-bottom block already contains a
# privacy-policy.html href, the block is left untouched. Safe to
# re-run multiple times.
#
# ────────────────────────────────────────────────────────────────────────
# DOCUMENTED NEAR-MISS: an earlier (audit-branch) version of this
# injector did NOT track depth, just looked for the first </div> after
# the open. On the WPB landing page's nested-div footer-bottom that
# would have closed the WRONG </div> — the inner one — and left dangling
# Privacy/Terms anchors outside the footer-bottom block. Always track
# depth on <div>/</div> when scanning for the matching closer.
# ────────────────────────────────────────────────────────────────────────

BEGIN { RS = "\0" }

{
  s = $0; out = ""; pos = 1
  while (1) {
    rel = index(substr(s, pos), "<div class=\"footer-bottom\"")
    if (rel == 0) { out = out substr(s, pos); break }
    abs_open = pos + rel - 1
    out = out substr(s, pos, abs_open - pos)
    gt = index(substr(s, abs_open), ">")
    if (gt == 0) { out = out substr(s, abs_open); break }
    body_start = abs_open + gt

    # Walk forward tracking <div / </div> depth to find the matching closer
    depth = 1; p = body_start; end_pos = 0
    while (p <= length(s)) {
      open_at  = index(substr(s, p), "<div")
      close_at = index(substr(s, p), "</div>")
      if (close_at == 0) break
      if (open_at > 0 && open_at < close_at) {
        depth++
        p = p + open_at + 3
      } else {
        depth--
        if (depth == 0) { end_pos = p + close_at - 1; break }
        p = p + close_at + 5
      }
    }
    if (end_pos == 0) { out = out substr(s, abs_open); break }

    block_inner = substr(s, body_start, end_pos - body_start)
    full_open   = substr(s, abs_open, body_start - abs_open)

    if (block_inner ~ /privacy-policy\.html/) {
      # Idempotent: already injected
      out = out full_open block_inner
    } else {
      legal = " <span style=\"opacity:.55;\">&middot;</span> <a href=\"/privacy-policy.html\" style=\"color:inherit;text-decoration:none;\">Privacy</a> <span style=\"opacity:.55;\">&middot;</span> <a href=\"/terms-of-use.html\" style=\"color:inherit;text-decoration:none;\">Terms</a>"
      out = out full_open block_inner legal
    }
    out = out "</div>"
    pos = end_pos + 6
  }
  printf "%s", out
}
