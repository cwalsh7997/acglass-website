# Multi-line + single-line aware sitemap.xml pruner.
#
# Usage:
#   awk -f scripts/sitemap-prune.awk sitemap.xml | sed 's/$/\r/' > sitemap.xml.new
#   mv sitemap.xml.new sitemap.xml
#
# Before running, edit the PATTERN regex (~5 lines down) to match the <loc>
# URLs you want to remove.
#
# Why this exists: ACG's sitemap.xml mixes two URL-block shapes:
#
#   Multi-line form:
#     <url>
#       <loc>https://acglass.com/some-page.html</loc>
#       <lastmod>...</lastmod>
#       ...
#     </url>
#
#   Single-line form (also valid):
#     <url><loc>https://acglass.com/tools/</loc><lastmod>...</lastmod><priority>0.9</priority></url>
#
# A naive state machine that goes "see <url> → start buffering → wait for
# </url>" will collapse RUNS of single-line entries: when the first <url>
# rule fires it consumes the line, then the next single-line <url> on the
# next line ALSO matches the same rule and overwrites the buffer — the
# block in between is silently lost. On 2026-05-30 this bug ate 169 extra
# URLs from sitemap.xml before being caught in a pre-push diff review.
# (See CLAUDE.md §7 commit a46981c2 for context.)
#
# The fix: on every line, FIRST check whether <url> AND </url> are both
# present (single-line case) and handle inline; only enter the multi-line
# buffer state when <url> is present WITHOUT </url> on the same line.

# ─── EDIT THIS: the regex that matches URLs you want removed ──────────────
# This default removes nothing — replace with your actual targets. Example:
#   PATTERN = "(commercial-glazing-(alabama|georgia)\\.html|national-commercial-glazing-contractor\\.html)"
BEGIN {
  PATTERN = "MATCH_NOTHING_BY_DEFAULT_REPLACE_ME"
  in_url = 0
  buf = ""
}

{
  # Not currently buffering a multi-line block
  if (!in_url) {
    if ($0 ~ /<url>/) {
      # Same-line <url>...</url>?
      if ($0 ~ /<\/url>/) {
        # Single-line URL block — decide immediately
        if ($0 !~ PATTERN) {
          print
        }
        next
      } else {
        # Opens a multi-line block; start buffering
        in_url = 1
        buf = $0 "\n"
        next
      }
    }
    # Plain non-url line (XML preamble, urlset wrappers, comments, etc.)
    print
    next
  }

  # in_url: continuation of a multi-line block
  buf = buf $0 "\n"
  if ($0 ~ /<\/url>/) {
    if (buf !~ PATTERN) {
      printf "%s", buf
    }
    in_url = 0
    buf = ""
  }
}
