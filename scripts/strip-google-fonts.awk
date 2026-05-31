# Strip Google Fonts <link> + preconnect from a page, insert a font
# preload before the css/style.css link, and bump the css/style.css
# cache-buster.
#
# Usage:
#   CB=$(date +%s)
#   for f in $(grep -l "fonts.googleapis.com" --include="*.html" -r .); do
#     # Skip pages that still need Google Fonts for fonts we don't self-host
#     grep -q "Fraunces\|Manrope" "$f" && continue
#     case "$f" in ./workers/*|./preview/*|./node_modules/*) continue ;; esac
#     awk -v cb=$CB -f scripts/strip-google-fonts.awk "$f" \
#       | sed 's/$/\r/' > /tmp/_.html
#     diff -q "$f" /tmp/_.html > /dev/null 2>&1 || mv /tmp/_.html "$f"
#   done
#
# What it does per line:
#   1. Strip <link href="https://fonts.googleapis.com/css2…" rel="stylesheet">
#      (both attribute orders)
#   2. Strip <link rel="preconnect" href="https://fonts.googleapis.com">
#      and the matching fonts.gstatic.com preconnect
#   3. Bump ?v=N cache-buster on css/style.css to the value of `cb`
#   4. Insert <link rel="preload" as="font" type="font/woff2"
#      href="/fonts/inter-variable-latin.woff2" crossorigin> once per
#      file, just BEFORE the css/style.css <link>
#   5. If a line is now whitespace-only AND we made it whitespace-only,
#      drop it (preserves pre-existing blank lines — NEAR-MISS #2)
#
# ────────────────────────────────────────────────────────────────────────
# DOCUMENTED NEAR-MISSES (do not regress these):
#
# #5  gawk's gsub() does NOT expand backref \1 in the replacement
#     string. An earlier version had:
#       gsub(/(css\/style\.css)\?v=[0-9]+/, "\\1?v=" cb)
#     which produced literal `href="\1?v=1780170531"` in 1,275 files.
#     Caught in a pre-push `diff -u` before mv. Fix: scope the gsub to
#     lines that already contain css/style.css and substitute just
#     the `?v=N` portion, no backref needed.
#
# #6  Aggressive blank-line deletion. First version had:
#       if ($0 ~ /^[ \t\r]*$/) next
#     This drops ANY whitespace-only line — including ~80 pre-existing
#     intentional blank lines per page (~50,000 site-wide). Caught when
#     overall diff stats showed -27,858 deletions vs an expected ~6,000.
#     Reverted via `git checkout -- '*.html'`, fixed to only drop lines
#     that THIS awk pass blanked (compare `original` to current `$0`).
#
# #4  ALSO see scripts/dim-inject.awk and lazy-async-inject.awk:
#     google9d45280643313cec.html requires exact-byte content (Google
#     site-verification check). Sed `s/$/\r/` post-process appends \r
#     to its only line → 53 → 54 bytes → verification fails. ALWAYS
#     skip in the mass-apply loop.
# ────────────────────────────────────────────────────────────────────────

BEGIN { preload_done = 0 }

{
  original = $0   # NEAR-MISS #6: remember pristine line so we only drop what we blanked

  # --- strip the Google Fonts stylesheet link (both attribute orders) ---
  gsub(/<link[^>]*href="https:\/\/fonts\.googleapis\.com\/css2[^"]*"[^>]*rel="stylesheet"[^>]*>/, "")
  gsub(/<link[^>]*rel="stylesheet"[^>]*href="https:\/\/fonts\.googleapis\.com\/css2[^"]*"[^>]*>/, "")

  # --- strip preconnects to both fonts hosts ---
  gsub(/<link[^>]*rel="preconnect"[^>]*href="https:\/\/fonts\.googleapis\.com"[^>]*>/, "")
  gsub(/<link[^>]*rel="preconnect"[^>]*href="https:\/\/fonts\.gstatic\.com"[^>]*>/, "")

  # --- insert preload ONCE before the css/style.css <link>, BEFORE
  #     the cache-buster gsub (which would otherwise mangle the line) ---
  if (!preload_done && /<link[^>]*rel="stylesheet"[^>]*href="[^"]*css\/style\.css/) {
    indent = $0
    sub(/[^ \t].*$/, "", indent)
    print indent "<link rel=\"preload\" as=\"font\" type=\"font/woff2\" href=\"/fonts/inter-variable-latin.woff2\" crossorigin>"
    preload_done = 1
  }

  # --- bump cache-buster ONLY on lines that contain css/style.css.
  #     NEAR-MISS #5: NO backref. Scope the gsub to lines that
  #     already contain css/style.css and substitute just ?v=NNN. ---
  if (/css\/style\.css\?v=[0-9]+/) {
    gsub(/\?v=[0-9]+/, "?v=" cb)
  }

  # --- NEAR-MISS #6: drop the line ONLY if WE blanked it. Preserves
  #     pre-existing intentional blank lines. ---
  if ($0 != original && $0 ~ /^[ \t\r]*$/) next

  print
}
