#!/usr/bin/env bash
# Design-system enforcement lint. rules/01 section 11.
#
# tokens.css is law. It is the only file permitted to contain a raw value.
# Every rule below fails the build and names file and line.
#
# NOTE ON SCOPE: this lints src/ only, which is where the new token-based system
# lives. The 1,593 legacy pages carry ~1,500 inline style attributes and are NOT
# in scope until their template cluster is migrated in a later phase. Linting them
# now would report thousands of violations against code nobody has touched yet and
# would make the check useless. Scope widens as clusters migrate.
source "$(dirname "$0")/_lib.sh"

SRC="$ROOT/src"
[ -d "$SRC" ] || { say "CONFIG  design-lint: src/ does not exist yet"; exit 3; }

fail=0
report() { printf '  %s\n' "$1"; fail=$((fail+1)); }

scan() { # pattern, message, extra grep args
  local pat="$1" msg="$2"; shift 2
  local out
  out=$(grep -rnE "$pat" "$SRC" "$@" 2>/dev/null)
  [ -n "$out" ] && while IFS= read -r l; do
    report "$(echo "$l" | sed "s|$ROOT/||") :: $msg"
  done <<< "$out"
}

# 1. Any hex outside tokens.css.
scan '#[0-9a-fA-F]{3,8}\b' 'raw hex outside tokens.css' --exclude=tokens.css

# 2. Radius outside the permitted set (0, 2px, 4px, or a var).
out=$(grep -rnE 'border-radius:' "$SRC" 2>/dev/null | grep -vE 'border-radius:\s*(var\(|0|2px|4px)')
[ -n "$out" ] && while IFS= read -r l; do
  report "$(echo "$l" | sed "s|$ROOT/||") :: radius outside {0, 2px, 4px, var()}"
done <<< "$out"

# 3. Off-8pt spacing. The scale is 4/8/12/16/24/32/40/48/64/80/96/128.
#    rules/01 supplies the regex 1[13579]|2[1235679]|3[01345679]|[5-9][0-9] which
#    only catches ODD teens: it misses 18, 20, 28, 36 and every other off-scale even
#    value. Membership testing against the actual scale instead. Corrected 2026-09-08.
ALLOWED_PX=" 0 4 8 12 16 24 32 40 48 64 80 96 128 "
while IFS= read -r l; do
  [ -z "$l" ] && continue
  vals=$(echo "$l" | sed 's/.*:\s*//' | grep -oE '[0-9]+px' | tr -d 'px')
  for v in $vals; do
    case "$ALLOWED_PX" in
      *" $v "*) ;;
      *) report "$(echo "$l" | sed "s|$ROOT/||") :: off-scale spacing value ${v}px"; break;;
    esac
  done
done <<< "$(grep -rnE '(padding|margin|gap)[a-z-]*:[^;]*[0-9]+px' "$SRC" 2>/dev/null)"


# 4. Durations over 260ms.
scan 'transition-duration:\s*(2[7-9][0-9]|[3-9][0-9]{2}|[0-9]+\.?[0-9]*s)' \
     'duration exceeds the 260ms motion budget'

# 5. Pill radius.
scan 'border-radius:\s*(999px|50%)' 'pill radius is banned'

# 6. Gradients, backdrop-filter.
scan '(linear-gradient|radial-gradient|backdrop-filter)' \
     'gradient or backdrop-filter is banned' --exclude=tokens.css

# 7. Stock photo hosts.
scan '(unsplash|shutterstock|istockphoto|pexels|gettyimages|stock\.adobe)' \
     'stock photo host reference'

# 8. font-size in component CSS. Six sizes render per page; components use tokens.
#    NOT a regex with \s*[^v]: that matches zero spaces then eats the space itself,
#    flagging every legitimate var(). grep -E has no negative lookahead, so match all
#    font-size declarations and filter the compliant ones out. Corrected 2026-09-08.
out=$(grep -rnE 'font-size:' "$SRC" --exclude=tokens.css 2>/dev/null | grep -vE 'font-size:\s*var\(')
[ -n "$out" ] && while IFS= read -r l; do
  report "$(echo "$l" | sed "s|$ROOT/||") :: font-size outside a token"
done <<< "$out"

if [ "$fail" -eq 0 ]; then
  say "PASS    design-lint (src/ clean against rules/01 section 11)"
  exit 0
fi
say "FAIL    design-lint: $fail violation(s)"
exit 1
