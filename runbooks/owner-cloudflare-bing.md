# Session A — Cloudflare + Bing Webmaster (owner login required)

**Time estimate:** 35–45 minutes
**Prereqs:** You're logged into Cloudflare with the account that owns the `acglass.com` zone, and into Google Search Console for the `sc-domain:acglass.com` property (used for Bing import).

This is the one outside-the-repo session that delivers the largest SEO impact remaining. Run it once, end to end, before doing anything else.

---

## Part 1 — Bing Webmaster import from GSC (8 minutes)

1. Open [Bing Webmaster Tools](https://www.bing.com/webmasters).
2. Sign in with your Microsoft account.
3. On the dashboard, click **Add a Site** → **Import from Google Search Console**.
4. Authorize the GSC connection when prompted.
5. From the property list, choose **`sc-domain:acglass.com`** and click **Import**.
6. After import completes (usually <60 seconds), click into the new property.
7. Go to **Sitemaps** in the left nav.
8. Submit: `https://acglass.com/sitemap-index.xml`
9. Verify status reads "Discovered" / "Submitted" within 30 seconds.

**Acceptance:** Bing Webmaster shows acglass.com with a submitted sitemap-index. No meta-tag verification needed (the GSC import covers it).

---

## Part 2 — Cloudflare: acommercialglass.com → acglass.com 301 (5 minutes)

We own both zones. The mis-spelled zone needs to redirect to the canonical one.

1. Open [Cloudflare dashboard](https://dash.cloudflare.com).
2. Click into the **acommercialglass.com** zone (NOT acglass.com).
3. Left nav → **Rules** → **Redirect Rules** → **Create rule**.
4. Configure:
   - **Rule name:** `acommercialglass to acglass canonical`
   - **When incoming requests match:** Custom filter expression
     - Field: `Hostname` · Operator: `equals` · Value: `acommercialglass.com`
     - Click **Or** → Field: `Hostname` · Operator: `equals` · Value: `www.acommercialglass.com`
   - **Then:**
     - Type: **Dynamic**
     - Expression: `concat("https://acglass.com", http.request.uri.path, if(len(http.request.uri.query) > 0, concat("?", http.request.uri.query), ""))`
     - Status code: **301**
     - Preserve query string: ON
5. **Deploy.**
6. Test in incognito: hit `https://acommercialglass.com/manufacturers.html` — should land at `https://acglass.com/manufacturers.html`, status 301.

**Acceptance:** `curl -sI https://acommercialglass.com/` returns `HTTP/2 301` with `location: https://acglass.com/`.

---

## Part 3 — Cloudflare: HSTS, Crawler Hints, AlwaysHTTPS (5 minutes)

In the **acglass.com** zone:

1. **SSL/TLS** → **Edge Certificates**:
   - **HTTP Strict Transport Security (HSTS)**: Click **Enable HSTS**.
     - Max Age: **6 months (15768000)** to start. After 30 days of clean operation, bump to **12 months (31536000)**. Do NOT enable `preload` yet — you can't easily back out of preload.
     - Apply HSTS to subdomains: **ON**
     - Click **Save**.
   - **Always Use HTTPS**: **ON**
   - **Minimum TLS Version**: **TLS 1.2**
2. **Caching** → **Configuration** → **Crawler Hints**: **ON**.

**Acceptance:** `curl -sI https://acglass.com/` shows a `strict-transport-security:` header.

---

## Part 4 — Cloudflare: Cache Rule for static assets (8 minutes)

In **acglass.com** → **Caching** → **Cache Rules** → **Create rule**:

- **Rule name:** `Static assets — long edge TTL`
- **When incoming requests match:**
  - Custom expression:
    ```
    (http.request.uri.path matches "\\.(avif|webp|jpe?g|png|svg|woff2?|ico)$") or
    (starts_with(http.request.uri.path, "/css/")) or
    (starts_with(http.request.uri.path, "/js/")) or
    (starts_with(http.request.uri.path, "/images/"))
    ```
- **Cache eligibility:** Eligible for cache
- **Edge TTL:** Override origin → **30 days (2,592,000 seconds)**
- **Browser TTL:** Override origin → **7 days (604,800 seconds)**
- **Deploy.**

**Acceptance:** `curl -sI https://acglass.com/images/acg-favicon.svg` shows `cf-cache-status: HIT` (after a second request) and `cache-control: public, max-age=604800`.

---

## Part 5 — Cloudflare: X-Robots-Tag noindex on /pdfs/qualifications/* (4 minutes)

Some qualifications PDFs are exposed at static URLs but should not be indexed.

In **acglass.com** → **Rules** → **Transform Rules** → **Modify Response Header** → **Create rule**:

- **Rule name:** `noindex qualifications PDFs`
- **When:** `starts_with(http.request.uri.path, "/pdfs/qualifications/")`
- **Modify response header:**
  - Set header: `X-Robots-Tag`
  - Value: `noindex, nofollow`
- **Deploy.**

**Acceptance:** `curl -sI https://acglass.com/pdfs/qualifications/<some-file>.pdf` shows `x-robots-tag: noindex, nofollow`.

---

## Part 6 — Cloudflare: Bulk Redirects import (10 minutes)

We have a CSV of legacy 301s ready to import.

1. **Rules** → **Redirects** → **Bulk Redirects** → **Create a redirect list** if you don't already have one named `acglass-legacy-301s`.
2. In that list → **Add from file** → upload `cloudflare-bulk-redirects.csv` from this repo's root.
3. After upload, click **Save**.
4. **Rules** → **Bulk Redirects** → **Create rule**:
   - Rule name: `Legacy URL redirects`
   - Use list: `acglass-legacy-301s`
   - Preserve query string: ON
   - Subpath matching: OFF (unless your CSV intends it)
5. **Deploy.**
6. Spot-test 3 rows from the CSV with `curl -sI`.

**Acceptance:** Bulk Redirects list shows the imported entries; 3 spot-checks return 301 to the new URL.

---

## After the session

Open `OWNER-ACTIONS.md` in the repo root and check off the items completed. Next session: directories (`runbooks/owner-directories.md`).
