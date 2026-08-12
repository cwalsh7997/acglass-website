#!/usr/bin/env python3
"""Behavior tests for the root-scoped service worker navigation policy."""

from __future__ import annotations

import json
import subprocess
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[3]
SW_PATH = REPO_ROOT / "sw.js"

NODE_HARNESS = r"""
const fs = require('fs');
const vm = require('vm');

const source = fs.readFileSync(process.argv[1], 'utf8');
const listeners = {};
const entries = [];
const calls = {deletes: [], fetches: [], matches: [], opens: [], puts: []};

let fetchRejects = false;
let networkResponse = null;
let cachedResponse = null;

function response(options = {}) {
  const headers = new Headers({'content-type': options.contentType || 'text/html'});
  return {
    ok: options.ok !== false,
    redirected: Boolean(options.redirected),
    status: options.status || 200,
    headers,
    marker: options.marker || 'network',
    clone() { return response({...options, marker: options.marker || 'network'}); }
  };
}

const cache = {
  keys() { return Promise.resolve(entries.map(url => ({url}))); },
  put(request) {
    calls.puts.push(request.url);
    entries.push(request.url);
    return Promise.resolve();
  },
  delete(request) {
    calls.deletes.push(request.url);
    const index = entries.indexOf(request.url);
    if (index >= 0) entries.splice(index, 1);
    return Promise.resolve(true);
  }
};

const context = {
  URL,
  Headers,
  Response,
  Promise,
  self: {
    location: {origin: 'https://acglass.com'},
    clients: {claim() { calls.claimed = true; return Promise.resolve(); }},
    skipWaiting() { calls.skipped = true; return Promise.resolve(); },
    addEventListener(type, handler) { listeners[type] = handler; }
  },
  caches: {
    open(name) { calls.opens.push(name); return Promise.resolve(cache); },
    match(request, options) {
      calls.matches.push({url: request.url, cacheName: options && options.cacheName});
      return Promise.resolve(cachedResponse);
    },
    keys() { return Promise.resolve(['acg-v5-2026-08-11', 'acg-navigation-old', 'acg-dealer-cache', 'unrelated-app-cache']); },
    delete(name) { calls.deletedCaches = calls.deletedCaches || []; calls.deletedCaches.push(name); return Promise.resolve(true); }
  },
  fetch(request) {
    calls.fetches.push(request.url);
    if (fetchRejects) return Promise.reject(new Error('network failed'));
    return Promise.resolve(networkResponse || response());
  }
};

vm.runInNewContext(source, context, {filename: 'sw.js'});

async function dispatchFetch(testCase) {
  fetchRejects = Boolean(testCase.fetchRejects);
  networkResponse = response(testCase.response || {});
  cachedResponse = testCase.cached ? response({marker: 'cached'}) : null;
  entries.length = 0;
  entries.push(...(testCase.entries || []));
  for (const key of Object.keys(calls)) {
    if (Array.isArray(calls[key])) calls[key].length = 0;
  }

  let responsePromise;
  const pending = [];
  const request = {
    url: testCase.url,
    method: testCase.method || 'GET',
    mode: testCase.mode || 'navigate'
  };
  listeners.fetch({
    request,
    respondWith(value) { responsePromise = Promise.resolve(value); },
    waitUntil(value) { pending.push(Promise.resolve(value)); }
  });

  const synchronousWaitCount = pending.length;

  let result = 'bypassed';
  let status = null;
  if (responsePromise) {
    const resolved = await responsePromise;
    result = resolved.marker || 'response';
    status = resolved.status;
  }
  await Promise.all(pending);
  return {
    result,
    status,
    synchronousWaitCount,
    entries: [...entries],
    deletes: [...calls.deletes],
    fetches: [...calls.fetches],
    matches: calls.matches.map(item => ({...item})),
    opens: [...calls.opens],
    puts: [...calls.puts]
  };
}

async function dispatchActivate() {
  let pending;
  listeners.activate({waitUntil(value) { pending = Promise.resolve(value); }});
  await pending;
  return calls;
}

(async () => {
  const payload = JSON.parse(fs.readFileSync(0, 'utf8'));
  if (payload.action === 'activate') {
    process.stdout.write(JSON.stringify(await dispatchActivate()));
    return;
  }
  const output = [];
  for (const testCase of payload.cases) output.push(await dispatchFetch(testCase));
  process.stdout.write(JSON.stringify(output));
})().catch(error => {
  process.stderr.write(String(error.stack || error));
  process.exit(1);
});
"""


def run_harness(payload: dict[str, object]):
    completed = subprocess.run(
        ["node", "-e", NODE_HARNESS, str(SW_PATH)],
        input=json.dumps(payload),
        text=True,
        capture_output=True,
        check=True,
    )
    return json.loads(completed.stdout)


class ServiceWorkerNavigationPolicyTests(unittest.TestCase):
    def test_only_same_origin_get_navigations_are_intercepted(self):
        cases = [
            {"url": "https://acglass.com/portfolio.html"},
            {"url": "https://acglass.com/css/style.css", "mode": "no-cors"},
            {"url": "https://acglass.com/js/main.js", "mode": "same-origin"},
            {"url": "https://acglass.com/portfolio.html", "method": "POST"},
            {"url": "https://www.google-analytics.com/g/collect"},
        ]
        results = run_harness({"cases": cases})
        self.assertEqual("network", results[0]["result"])
        for result in results[1:]:
            self.assertEqual("bypassed", result["result"])
            self.assertEqual([], result["fetches"])
            self.assertEqual([], result["opens"])
            self.assertEqual([], result["puts"])

    def test_navigation_is_network_first_and_caches_only_html_success(self):
        cases = [
            {"url": "https://acglass.com/portfolio.html", "cached": True},
            {"url": "https://acglass.com/not-found", "response": {"ok": False, "status": 404}},
            {"url": "https://acglass.com/redirect", "response": {"redirected": True}},
            {"url": "https://acglass.com/file", "response": {"contentType": "application/pdf"}},
        ]
        results = run_harness({"cases": cases})
        first = results[0]
        self.assertEqual("network", first["result"])
        self.assertEqual(1, first["synchronousWaitCount"])
        self.assertEqual(["https://acglass.com/portfolio.html"], first["fetches"])
        self.assertEqual([], first["matches"])
        self.assertEqual(["https://acglass.com/portfolio.html"], first["puts"])
        for result in results[1:]:
            self.assertEqual(1, result["synchronousWaitCount"])
            self.assertEqual([], result["puts"])

    def test_offline_returns_exact_cached_route_or_503(self):
        cases = [
            {"url": "https://acglass.com/about.html", "cached": True, "fetchRejects": True},
            {"url": "https://acglass.com/unvisited.html", "fetchRejects": True},
        ]
        cached, missing = run_harness({"cases": cases})
        self.assertEqual("cached", cached["result"])
        self.assertEqual(
            [{"url": "https://acglass.com/about.html", "cacheName": "acg-navigation-v1-2026-08-12"}],
            cached["matches"],
        )
        self.assertEqual(503, missing["status"])
        self.assertEqual([], missing["puts"])

    def test_navigation_cache_has_a_hard_twenty_entry_limit(self):
        existing = [f"https://acglass.com/page-{index}.html" for index in range(20)]
        [result] = run_harness({
            "cases": [{"url": "https://acglass.com/new.html", "entries": existing}]
        })
        self.assertEqual(20, len(result["entries"]))
        self.assertNotIn(existing[0], result["entries"])
        self.assertIn("https://acglass.com/new.html", result["entries"])

    def test_activation_deletes_only_owned_navigation_caches(self):
        result = run_harness({"action": "activate"})
        self.assertEqual(
            ["acg-v5-2026-08-11", "acg-navigation-old"],
            result["deletedCaches"],
        )
        self.assertNotIn("acg-dealer-cache", result["deletedCaches"])
        self.assertNotIn("unrelated-app-cache", result["deletedCaches"])
        self.assertTrue(result["claimed"])

    def test_policy_source_has_no_precache_shell_or_asset_cache_path(self):
        source = SW_PATH.read_text(encoding="utf-8")
        self.assertNotIn("SHELL", source)
        self.assertNotIn("addAll", source)
        self.assertIn("request.mode === 'navigate'", source)
        self.assertIn("MAX_NAVIGATION_ENTRIES = 20", source)
        self.assertLess(
            source.index("const copy = response.clone();"),
            source.index("const cache = await caches.open(CACHE);"),
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
