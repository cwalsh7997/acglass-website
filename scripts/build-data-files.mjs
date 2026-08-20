#!/usr/bin/env node
/**
 * build-data-files.mjs
 *
 * Regenerates the two data files that are served to users but were previously
 * maintained by hand:
 *
 *   search-index.json  — the client-side site search index
 *   feed.xml           — the RSS feed for the field notes / blog
 *
 * Why this exists
 * ---------------
 * Both files had drifted away from the published HTML. search-index.json was
 * still serving copy that no longer appears anywhere on the site: OSHA
 * recordable-rate claims that were retired for claim safety, "AI-managed"
 * positioning that appears in zero live pages, and a "premier" superlative.
 * It also indexed 9 URLs that are instant-redirect stubs, so site search could
 * land a visitor on a page that immediately bounces them somewhere else.
 * feed.xml was missing 29 real posts and still listed one redirected URL, with
 * a lastBuildDate months out of date.
 *
 * Hand-maintained derivative files always drift. Deriving them from the HTML
 * means a copy change on a page can no longer leave a stale claim behind in a
 * file nobody thinks to open.
 *
 * Rules
 * -----
 *  - Redirect stubs (meta refresh at 0 seconds) are never indexed or fed.
 *  - Anything under /drafts/ is excluded; it is disallowed in robots.txt.
 *  - Text is taken from the page's own <title>, meta description and <h1>.
 *    The generator never invents copy.
 *  - Feed item dates come from the page's own published-date metadata. A post
 *    with no parseable date is reported and skipped rather than given a
 *    fabricated date.
 *
 * Usage:  node scripts/build-data-files.mjs [--check]
 *         --check writes nothing and exits 1 if the committed files are stale.
 */

import { readFileSync, writeFileSync, readdirSync, statSync, existsSync } from 'node:fs';
import { join, relative, dirname } from 'node:path';

const ROOT = join(dirname(new URL(import.meta.url).pathname), '..');
const ORIGIN = 'https://acglass.com';
const CHECK = process.argv.includes('--check');

/* ---------------------------------------------------------------- helpers */

const EXCLUDE_DIRS = new Set(['.git', 'qa', 'drafts', 'node_modules', 'scripts']);

function walk(dir, out = []) {
  for (const name of readdirSync(dir)) {
    const full = join(dir, name);
    const rel = relative(ROOT, full);
    if (EXCLUDE_DIRS.has(rel.split('/')[0])) continue;
    const st = statSync(full);
    if (st.isDirectory()) walk(full, out);
    else if (name.endsWith('.html')) out.push(full);
  }
  return out;
}

const isRedirectStub = (html) =>
  /http-equiv=["']refresh["'][^>]*content=["']\s*0\s*;/i.test(html);

const decode = (s) =>
  s.replace(/&amp;/g, '&').replace(/&lt;/g, '<').replace(/&gt;/g, '>')
   .replace(/&quot;/g, '"').replace(/&#39;|&apos;/g, "'").replace(/&nbsp;/g, ' ')
   .replace(/&mdash;/g, '\u2014').replace(/&ndash;/g, '\u2013')
   .replace(/&hellip;/g, '\u2026').replace(/\s+/g, ' ').trim();

const strip = (s) => decode(s.replace(/<[^>]*>/g, ' '));

function meta(html, name) {
  const re = new RegExp(
    `<meta[^>]+(?:name|property)=["']${name}["'][^>]+content=["']([^"']*)["']`, 'i');
  const m = html.match(re) ||
    html.match(new RegExp(
      `<meta[^>]+content=["']([^"']*)["'][^>]+(?:name|property)=["']${name}["']`, 'i'));
  return m ? decode(m[1]) : '';
}

function urlFor(file) {
  let u = '/' + relative(ROOT, file).replace(/\\/g, '/');
  return u.replace(/\/index\.html$/, '/');
}

/* ------------------------------------------------------- search-index.json */

function buildSearchIndex(pages) {
  const records = [];
  const skipped = { stub: 0, noTitle: 0 };

  for (const { file, html } of pages) {
    if (isRedirectStub(html)) { skipped.stub++; continue; }
    if (/<meta[^>]+name=["']robots["'][^>]*noindex/i.test(html)) { skipped.stub++; continue; }

    const title = decode((html.match(/<title[^>]*>([\s\S]*?)<\/title>/i) || [, ''])[1]);
    if (!title) { skipped.noTitle++; continue; }

    const desc = meta(html, 'description') || meta(html, 'og:description');
    const h1m = html.match(/<h1[^>]*>([\s\S]*?)<\/h1>/i);
    const h1 = h1m ? strip(h1m[1]) : '';

    // The index is fetched by the browser on /search.html, so weight matters.
    // Two safe reductions, neither of which loses a searchable term:
    //  - strip the "| American Commercial Glass" / "| ACG" boilerplate that
    //    repeats on ~1,400 titles; it also reads better in results
    //  - blank h1 when the title already contains it, since a query matching
    //    the h1 would already match the title
    // The key is still emitted as a string: search.html calls item.h
    // .toLowerCase() unguarded, and a missing key would throw.
    const t = title.replace(/\s*\|\s*(American Commercial Glass|ACG)\s*$/i, '').trim() || title;
    const h = h1 && t.toLowerCase().includes(h1.toLowerCase()) ? '' : h1;

    records.push({ t, d: desc, h, u: urlFor(file) });
  }

  records.sort((a, b) => a.u.localeCompare(b.u));
  return { records, skipped };
}

/* ------------------------------------------------------------- feed.xml */

const MONTHS = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
const DAYS = ['Sun','Mon','Tue','Wed','Thu','Fri','Sat'];

function rfc822(d) {
  const p = (n) => String(n).padStart(2, '0');
  return `${DAYS[d.getUTCDay()]}, ${p(d.getUTCDate())} ${MONTHS[d.getUTCMonth()]} ` +
    `${d.getUTCFullYear()} ${p(d.getUTCHours())}:${p(d.getUTCMinutes())}:` +
    `${p(d.getUTCSeconds())} +0000`;
}

function pageDate(html) {
  const cands = [
    meta(html, 'article:published_time'),
    meta(html, 'article:modified_time'),
    meta(html, 'datePublished'),
    (html.match(/"datePublished"\s*:\s*"([^"]+)"/) || [, ''])[1],
    (html.match(/<time[^>]+datetime=["']([^"']+)["']/i) || [, ''])[1],
  ].filter(Boolean);
  for (const c of cands) {
    const d = new Date(c);
    if (!isNaN(d)) return d;
  }
  return null;
}

const xml = (s) => String(s)
  .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
  .replace(/"/g, '&quot;').replace(/'/g, '&apos;');

function buildFeed(pages) {
  const items = [];
  const undated = [];

  for (const { file, html } of pages) {
    const rel = relative(ROOT, file).replace(/\\/g, '/');
    if (!rel.startsWith('blog/')) continue;
    if (rel === 'blog/index.html') continue;
    if (isRedirectStub(html)) continue;
    if (/<meta[^>]+name=["']robots["'][^>]*noindex/i.test(html)) continue;

    const title = decode((html.match(/<title[^>]*>([\s\S]*?)<\/title>/i) || [, ''])[1])
      .replace(/\s*[|\u2014]\s*(American Commercial Glass|ACG)\s*$/i, '');
    const desc = meta(html, 'description') || meta(html, 'og:description');
    const d = pageDate(html);
    if (!d) { undated.push(urlFor(file)); continue; }
    const author = meta(html, 'author') || 'Connor Walsh';

    items.push({ title, desc, url: ORIGIN + urlFor(file), date: d, author });
  }

  items.sort((a, b) => b.date - a.date);
  const total = items.length;
  // Cap the feed at the 50 most recent posts. The previous hand-built file
  // carried 208 items at 147 KB, which is well outside normal RSS practice and
  // is pure weight: post discovery for search engines runs through
  // sitemap-blog.xml, which still lists every post. A feed reader only ever
  // shows recent items anyway.
  const FEED_MAX = 50;
  if (items.length > FEED_MAX) items.length = FEED_MAX;
  const build = items.length ? items[0].date : new Date();

  const body = items.map((i) => `    <item>
      <title>${xml(i.title)}</title>
      <link>${xml(i.url)}</link>
      <guid isPermaLink="true">${xml(i.url)}</guid>
      <description>${xml(i.desc)}</description>
      <dc:creator>${xml(i.author)}</dc:creator>
      <pubDate>${rfc822(i.date)}</pubDate>
    </item>`).join('\n');

  const feed = `<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom" xmlns:content="http://purl.org/rss/1.0/modules/content/" xmlns:dc="http://purl.org/dc/elements/1.1/">
  <channel>
    <title>American Commercial Glass \u2014 The ACG Field Notes</title>
    <link>${ORIGIN}/blog/</link>
    <atom:link href="${ORIGIN}/feed.xml" rel="self" type="application/rss+xml"/>
    <description>Commercial glazing field notes from American Commercial Glass: code, systems, and project write-ups.</description>
    <language>en-us</language>
    <copyright>\u00a9 ${new Date().getUTCFullYear()} American Commercial Glass, Inc.</copyright>
    <lastBuildDate>${rfc822(build)}</lastBuildDate>
    <managingEditor>connor@acglass.com (Connor Walsh)</managingEditor>
    <webMaster>connor@acglass.com (Connor Walsh)</webMaster>
    <category>Construction</category>
    <category>Commercial Glazing</category>
${body}
  </channel>
</rss>
`;
  return { feed, count: items.length, total, undated };
}

/* ---------------------------------------------------------------- main */

const files = walk(ROOT);
const pages = files.map((file) => ({ file, html: readFileSync(file, 'utf8') }));

const { records, skipped } = buildSearchIndex(pages);
const { feed, count, total, undated } = buildFeed(pages);

const indexJson = JSON.stringify(records) + '\n';

// Retired-claim guard. These strings were removed from the site's HTML for
// claim safety; if a generated file reintroduces one, the build should fail
// loudly rather than quietly republish it.
const RETIRED = ['recordable', 'ai-managed', 'premier', 'world-class',
                 'best-in-class', 'number one', '#1 '];
const leaks = [];
for (const [label, text] of [['search-index.json', indexJson], ['feed.xml', feed]]) {
  for (const term of RETIRED) {
    // the ai-managed URL slug is a real page path, not a copy claim
    const hay = text.toLowerCase().replace(/\/ai-managed-glazing-contractor\.html/g, '');
    const n = hay.split(term).length - 1;
    if (n) leaks.push(`${label}: "${term}" x${n}`);
  }
}

console.log(`html files scanned      ${files.length}`);
console.log(`search-index records    ${records.length}  (skipped ${skipped.stub} redirect/noindex, ${skipped.noTitle} untitled)`);
console.log(`feed items              ${count} of ${total} eligible posts (capped at 50 most recent)`);
if (undated.length) {
  console.log(`posts with no parseable date, EXCLUDED rather than given a made-up date: ${undated.length}`);
  undated.slice(0, 10).forEach((u) => console.log(`    ${u}`));
}
if (leaks.length) {
  console.log('RETIRED CLAIM LEAK:');
  leaks.forEach((l) => console.log('    ' + l));
  process.exit(2);
}
console.log('retired-claim guard     clean');

const paths = { 'search-index.json': indexJson, 'feed.xml': feed };
if (CHECK) {
  let stale = false;
  for (const [p, content] of Object.entries(paths)) {
    const cur = existsSync(join(ROOT, p)) ? readFileSync(join(ROOT, p), 'utf8') : '';
    if (cur !== content) { console.log(`STALE: ${p}`); stale = true; }
  }
  if (stale) process.exit(1);
  console.log('both files up to date');
} else {
  for (const [p, content] of Object.entries(paths)) writeFileSync(join(ROOT, p), content);
  console.log('wrote search-index.json and feed.xml');
}
