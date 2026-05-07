#!/usr/bin/env python3
"""Inject Bing + Yandex verification meta tags + Microsoft Clarity script
into every HTML file on the site. Idempotent — re-running is safe.

Update the placeholders below after creating accounts:
- BING_VERIFY: from Bing Webmaster Tools → Add Site → Meta tag method
- YANDEX_VERIFY: from Yandex Webmaster → Add Site → Meta tag method
- CLARITY_PROJECT_ID: from clarity.microsoft.com → Settings → Setup
"""
import os, re, glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

# === FILL THESE IN AFTER CREATING ACCOUNTS ===
BING_VERIFY = "PASTE_BING_VERIFICATION_CODE_HERE"
YANDEX_VERIFY = "PASTE_YANDEX_VERIFICATION_CODE_HERE"
CLARITY_PROJECT_ID = "PASTE_CLARITY_PROJECT_ID_HERE"
# =============================================

placeholders = {
    "BING_VERIFY": BING_VERIFY.startswith("PASTE_"),
    "YANDEX_VERIFY": YANDEX_VERIFY.startswith("PASTE_"),
    "CLARITY_PROJECT_ID": CLARITY_PROJECT_ID.startswith("PASTE_"),
}
if any(placeholders.values()):
    print("Placeholders not filled in:")
    for k, v in placeholders.items():
        if v: print(f"  - {k}")
    print("\nFill in the constants at the top of this script and re-run.")
    print("Without doing this, no changes will be made.")
    raise SystemExit(0)

bing_tag = f'<meta name="msvalidate.01" content="{BING_VERIFY}">'
yandex_tag = f'<meta name="yandex-verification" content="{YANDEX_VERIFY}">'
clarity = f"""<script type="text/javascript">
(function(c,l,a,r,i,t,y){{
  c[a]=c[a]||function(){{(c[a].q=c[a].q||[]).push(arguments)}};
  t=l.createElement(r);t.async=1;t.src="https://www.clarity.ms/tag/"+i;
  y=l.getElementsByTagName(r)[0];y.parentNode.insertBefore(t,y);
}})(window, document, "clarity", "script", "{CLARITY_PROJECT_ID}");
</script>"""

INJECT = f"\n  {bing_tag}\n  {yandex_tag}\n  {clarity}\n"

n = 0
for p in glob.glob("**/*.html", recursive=True):
    s = open(p, encoding="utf-8").read()
    if BING_VERIFY in s:
        continue  # already injected
    if "</head>" not in s:
        continue
    s = s.replace("</head>", INJECT + "</head>", 1)
    open(p, "w", encoding="utf-8").write(s)
    n += 1
print(f"Injected Bing + Yandex + Clarity into {n} pages.")
