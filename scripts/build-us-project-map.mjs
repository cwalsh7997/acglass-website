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
const totals = projects.reduce((acc, project) => {
  acc[project.state] = (acc[project.state] || 0) + 1;
  return acc;
}, {});

const output = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 720" width="1000" height="720" role="img" aria-labelledby="us-map-title us-map-desc">
  <title id="us-map-title">American Commercial Glass project locations across the United States</title>
  <desc id="us-map-desc">${projects.length} source-backed ACG project records: ${totals.FL} in Florida, ${totals.LA} in Louisiana, and ${totals.TN} in Tennessee. White markers identify glazing projects and red markers identify supply-only material orders. The Florida inset separates projects sharing the same metro area.</desc>
  <metadata>State boundaries simplified from the U.S. Census Bureau 2025 TIGER/Line state boundary. Markers are plotted at city level and fanned slightly when multiple projects share one city.</metadata>
  <rect width="1000" height="720" fill="#080D16"/>
  <text x="30" y="38" fill="#8FA3BF" font-family="ui-monospace, SFMono-Regular, Menlo, monospace" font-size="14" letter-spacing="2">VERIFIED PROJECT GEOGRAPHY / ${projects.length} RECORDS</text>
  <svg x="24" y="62" width="690" height="435" viewBox="${us.viewBox}" preserveAspectRatio="xMidYMid meet">
    ${us.body}
  </svg>
  <path d="M704 415 C760 430 765 476 748 505" fill="none" stroke="#526273" stroke-width="1.5" stroke-dasharray="5 7"/>
  <rect x="604" y="310" width="372" height="382" rx="4" fill="#0A111C" stroke="#526273"/>
  <text x="626" y="340" fill="#F0F3F8" font-family="ui-monospace, SFMono-Regular, Menlo, monospace" font-size="13" letter-spacing="2">FLORIDA INSET / ${totals.FL}</text>
  <svg x="620" y="355" width="340" height="315" viewBox="${florida.viewBox}" preserveAspectRatio="xMidYMid meet">
    ${florida.body}
  </svg>
  <g transform="translate(34 640)" font-family="ui-monospace, SFMono-Regular, Menlo, monospace" font-size="13" letter-spacing="1.1">
    <circle cx="5" cy="-4" r="4" fill="#F0F3F8" stroke="#080D16"/>
    <text x="18" y="0" fill="#8FA3BF">GLAZING PROJECT</text>
    <circle cx="198" cy="-4" r="5" fill="#E11320" stroke="#080D16"/>
    <text x="213" y="0" fill="#8FA3BF">SUPPLY-ONLY ORDER</text>
  </g>
  <text x="34" y="683" fill="#526273" font-family="ui-monospace, SFMono-Regular, Menlo, monospace" font-size="11" letter-spacing="1">CITY-LEVEL LOCATIONS / COINCIDENT PROJECTS FANNED FOR VISIBILITY</text>
</svg>
`;

writeFileSync(outputPath, output);
console.log(`Wrote ${outputPath.pathname} with ${projects.length} project records.`);
