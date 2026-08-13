const CACHE = 'acg-navigation-v1-2026-08-12';
const MAX_NAVIGATION_ENTRIES = 20;

function isOwnedCacheName(name) {
  return name.startsWith('acg-navigation-') ||
    /^acg-v\d+-\d{4}-\d{2}-\d{2}$/.test(name);
}

function isCacheableNavigation(request, url) {
  return request.method === 'GET' &&
    request.mode === 'navigate' &&
    url.origin === self.location.origin;
}

function isCacheableResponse(response) {
  const contentType = response.headers.get('content-type') || '';
  return response.ok &&
    !response.redirected &&
    contentType.toLowerCase().includes('text/html');
}

async function trimNavigationCache(cache) {
  const keys = await cache.keys();
  const excess = keys.length - MAX_NAVIGATION_ENTRIES;
  if (excess <= 0) return;
  await Promise.all(keys.slice(0, excess).map(request => cache.delete(request)));
}

async function cacheNavigation(request, response) {
  if (!isCacheableResponse(response)) return;
  const copy = response.clone();
  const cache = await caches.open(CACHE);
  await cache.put(request, copy);
  await trimNavigationCache(cache);
}

self.addEventListener('install', event => {
  event.waitUntil(self.skipWaiting());
});

self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys().then(keys => Promise.all(
      keys
        .filter(key => isOwnedCacheName(key) && key !== CACHE)
        .map(key => caches.delete(key))
    )).then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', event => {
  let url;
  try {
    url = new URL(event.request.url);
  } catch (error) {
    return;
  }

  if (!isCacheableNavigation(event.request, url)) return;

  const cacheWork = {};
  cacheWork.promise = new Promise(resolve => {
    cacheWork.resolve = resolve;
  });
  event.waitUntil(cacheWork.promise);

  event.respondWith((async () => {
    try {
      const response = await fetch(event.request);
      if (isCacheableResponse(response)) {
        cacheNavigation(event.request, response).then(
          cacheWork.resolve,
          cacheWork.resolve
        );
      } else {
        cacheWork.resolve();
      }
      return response;
    } catch (error) {
      cacheWork.resolve();
      const cached = await caches.match(event.request, {cacheName: CACHE});
      if (cached) return cached;
      return new Response('Offline', {
        status: 503,
        headers: {'Content-Type': 'text/plain; charset=utf-8'}
      });
    }
  })());
});
