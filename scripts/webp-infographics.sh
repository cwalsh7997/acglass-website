#!/bin/bash
cd /home/user/workspace/acglass-website
TOTAL=0
SAVED=0
for f in images/infographics/*.png; do
  [ -f "$f" ] || continue
  base="${f%.png}"
  out="${base}.webp"
  if [ -f "$out" ]; then continue; fi
  cwebp -q 85 -m 6 "$f" -o "$out" -quiet
  in_size=$(stat -c%s "$f")
  out_size=$(stat -c%s "$out")
  TOTAL=$((TOTAL+1))
  SAVED=$((SAVED + in_size - out_size))
  echo "OK ${f} | $((in_size/1024))K -> $((out_size/1024))K"
done
echo "==="
echo "Converted: $TOTAL files"
echo "Saved: $((SAVED/1024/1024)) MB"
