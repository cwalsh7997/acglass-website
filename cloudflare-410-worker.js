/**
 * ACG Cloudflare 410 Worker — Returns "410 Gone" for old WordPress spam URLs
 * 
 * DEPLOYMENT:
 * 1. Log into Cloudflare dashboard → acglass.com
 * 2. Go to Workers & Pages → Create Worker
 * 3. Paste this code
 * 4. Add route: acglass.com/* (or specific patterns below)
 * 5. Deploy
 */

const SPAM_PATTERNS = [
  /\/(casino|gambling|poker|slot|omegle|betting|roulette|blackjack)/i,
  /\/wp-(admin|login|content|includes|json)/i,
  /\/(xmlrpc|wp-cron|wp-signup|wp-trackback)/i,
  /\/\?p=\d+/,
  /\/\?page_id=\d+/,
  /\/\?attachment_id=\d+/,
  /\/feed\/?$/,
  /\/author\//,
  /\/category\//,
  /\/tag\//,
  /\/wp-sitemap/,
  /\/(bitcoin|crypto|forex|pharma|viagra|cialis)/i,
  /\/(greatest|best|top|list).*?(casino|gambling|betting|slot)/i,
  /\/whats-the.*?casino/i,
  /\/listing-of.*?betting/i,
  /\/omegle-review/i,
];

addEventListener('fetch', event => {
  event.respondWith(handleRequest(event.request));
});

async function handleRequest(request) {
  const url = new URL(request.url);
  const path = url.pathname + url.search;

  // Check if the URL matches any spam pattern
  for (const pattern of SPAM_PATTERNS) {
    if (pattern.test(path)) {
      return new Response(
        '<!DOCTYPE html><html><head><title>410 Gone</title></head><body><h1>410 Gone</h1><p>This page has been permanently removed.</p><p><a href="https://acglass.com">Visit acglass.com</a></p></body></html>',
        {
          status: 410,
          headers: {
            'Content-Type': 'text/html;charset=UTF-8',
            'X-Robots-Tag': 'noindex',
            'Cache-Control': 'public, max-age=86400',
          },
        }
      );
    }
  }

  // Pass through all other requests
  return fetch(request);
}
