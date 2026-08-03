#!/usr/bin/env node

import { execFileSync } from 'node:child_process';
import { mkdtempSync, readFileSync, writeFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';

const root = new URL('../', import.meta.url);
const dataPath = new URL('data/project-locations.json', root);
const outputPath = new URL('images/infographics/federal/us-project-map.svg', root);
const stateShapefile = process.env.STATE_SHP || '/tmp/tl_2025_us_state/tl_2025_us_state.shp';
const projects = JSON.parse(readFileSync(dataPath, 'utf8'));
const work = mkdtempSync(join(tmpdir(), 'acg-project-map-'));

function spreadCoincidentPoints(items) {
  const groups = new Map();
  for (const item of items) {
    const key = `${item.city}|${item.state}`;
    if (!groups.has(key)) groups.set(key, []);
    groups.get(key).push(item);
  }

  return [...groups.values()].flatMap(group => group.map((item, index) => {
    if (group.length === 1) return item;
    const ring = Math.floor(index / 8) + 1;
    const slot = index % 8;
    const angle = (Math.PI * 2 * slot / Math.min(group.length, 8)) + ring * 0.25;
    const radius = 0.055 * ring;
    return {
      ...item,
      lat: item.lat + Math.sin(angle) * radius,
      lng: item.lng + Math.cos(angle) * radius / Math.max(0.45, Math.cos(item.lat * Math.PI / 180))
    };
  }));
}

function featureCollection(items) {
  return {
    type: 'FeatureCollection',
    features: spreadCoincidentPoints(items).map(item => ({
      type: 'Feature',
      properties: { name: item.name, kind: item.type },
      geometry: { type: 'Point', coordinates: [item.lng, item.lat] }
    }))
  };
}

function runMapshaper(args) {
  execFileSync('npx', ['--yes', 'mapshaper@0.6.113', ...args], { stdio: 'inherit' });
}

function svgBody(path) {
  const svg = readFileSync(path, 'utf8');
  const viewBox = svg.match(/viewBox="([^"]+)"/)?.[1];
  const body = svg.match(/<svg[^>]*>([\s\S]*)<\/svg>/)?.[1]
    .replace(/^\s*<\?xml[^>]*>\s*/u, '')
    .trim();
  if (!viewBox || !body) throw new Error(`Could not parse ${path}`);
  return { viewBox, body };
}

const usPoints = join(work, 'us-points.geojson');
const flPoints = join(work, 'fl-points.geojson');
const usSvg = join(work, 'us.svg');
const flSvg = join(work, 'fl.svg');
writeFileSync(usPoints, JSON.stringify(featureCollection(projects)));
writeFileSync(flPoints, JSON.stringify(featureCollection(projects.filter(p => p.state === 'FL'))));

runMapshaper([
  stateShapefile, usPoints, 'combine-files',
  '-target', '*', '-proj', 'albersusa',
  '-target', 'tl_2025_us_state', '-filter', 'STATEFP <= "56"', '-simplify', '0.05%', 'keep-shapes',
  '-each', 'fill="#101923",stroke="#526273",stroke_width=0.7',
  '-target', 'us-points',
  '-each', 'r=kind == "supply" ? 4.6 : 3.2,fill=kind == "supply" ? "#E11320" : "#F0F3F8",stroke="#080D16",stroke_width=1.1',
  '-target', '*', '-o', 'format=svg', usSvg
]);

runMapshaper([
  stateShapefile, flPoints, 'combine-files',
  '-target', '*', '-proj', '+proj=merc',
  '-target', 'tl_2025_us_state', '-filter', 'STUSPS == "FL"', '-simplify', '0.15%', 'keep-shapes',
  '-each', 'fill="#0E284F",stroke="#8FA3BF",stroke_width=1.2',
  '-target', 'fl-points',
  '-each', 'r=kind == "supply" ? 5.4 : 3.6,fill=kind == "supply" ? "#E11320" : "#F0F3F8",stroke="#080D16",stroke_width=1.2',
  '-target', '*', '-o', 'format=svg', flSvg
]);

const us = svgBody(usSvg);
const florida = svgBody(flSvg);
const output = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 680" width="1000" height="680" role="img" aria-labelledby="us-map-title us-map-desc">
  <title id="us-map-title">American Commercial Glass project locations across the United States</title>
  <desc id="us-map-desc">Verified ACG work across Florida, Louisiana, and Tennessee. White markers identify glazing projects and red markers identify supply-only material orders. The Florida inset separates projects sharing the same metro area.</desc>
  <metadata>State boundaries simplified from the U.S. Census Bureau 2025 TIGER/Line state boundary. Markers are plotted at city level and fanned slightly when multiple projects share one city.</metadata>
  <rect width="1000" height="680" fill="#080D16"/>
  <text x="30" y="36" fill="#F0F3F8" font-family="ui-monospace, SFMono-Regular, Menlo, monospace" font-size="16" letter-spacing="2.2">PROJECT FOOTPRINT</text>
  <text x="970" y="36" text-anchor="end" fill="#8FA3BF" font-family="ui-monospace, SFMono-Regular, Menlo, monospace" font-size="15" letter-spacing="1.8">FLORIDA + BEYOND</text>
  <line x1="30" y1="54" x2="970" y2="54" stroke="#526273" stroke-width="1"/>
  <svg x="22" y="72" width="700" height="440" viewBox="${us.viewBox}" preserveAspectRatio="xMidYMid meet">
    ${us.body}
  </svg>
  <g aria-label="Lafayette, Louisiana glazing project">
    <path d="M436 419 L398 390 L345 390" fill="none" stroke="#8FA3BF" stroke-width="1"/>
    <text x="342" y="386" text-anchor="end" fill="#F0F3F8" font-family="ui-monospace, SFMono-Regular, Menlo, monospace" font-size="14" letter-spacing="1.2">LAFAYETTE, LA</text>
  </g>
  <g aria-label="Midway, Tennessee supply-only order">
    <path d="M550 309 L580 278 L640 278" fill="none" stroke="#E11320" stroke-width="1.2"/>
    <text x="644" y="282" fill="#F0F3F8" font-family="ui-monospace, SFMono-Regular, Menlo, monospace" font-size="14" letter-spacing="1.2">MIDWAY, TN</text>
  </g>
  <rect x="596" y="306" width="380" height="346" rx="3" fill="#0A111C" stroke="#526273"/>
  <text x="618" y="334" fill="#F0F3F8" font-family="ui-monospace, SFMono-Regular, Menlo, monospace" font-size="14" letter-spacing="1.6">FLORIDA</text>
  <line x1="618" y1="348" x2="954" y2="348" stroke="#526273" stroke-width="1"/>
  <svg x="614" y="360" width="344" height="276" viewBox="${florida.viewBox}" preserveAspectRatio="xMidYMid meet">
    ${florida.body}
  </svg>
  <g transform="translate(34 612)" font-family="ui-monospace, SFMono-Regular, Menlo, monospace" font-size="14" letter-spacing="1.1">
    <circle cx="5" cy="-4" r="4" fill="#F0F3F8"/>
    <text x="18" y="0" fill="#8FA3BF">GLAZING</text>
    <circle cx="128" cy="-4" r="5" fill="#E11320"/>
    <text x="142" y="0" fill="#8FA3BF">SUPPLY-ONLY</text>
  </g>
  <text x="34" y="645" fill="#526273" font-family="ui-monospace, SFMono-Regular, Menlo, monospace" font-size="11" letter-spacing="1">CITY-LEVEL LOCATIONS / COINCIDENT RECORDS SEPARATED FOR VISIBILITY</text>
</svg>
`;

writeFileSync(outputPath, output);
console.log(`Wrote ${outputPath.pathname} with ${projects.length} project records.`);
