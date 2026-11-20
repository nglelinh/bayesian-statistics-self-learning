// Build tất cả bundle vào ../public/js/explainers/
import { build } from 'vite';
import { rmSync, mkdirSync, readdirSync, statSync } from 'node:fs';
import { resolve, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';
import { ENTRIES } from './entries.mjs';

const root = dirname(fileURLToPath(import.meta.url));
const outDir = resolve(root, '../public/js/explainers');
const only = process.argv.slice(2);

if (!only.length) rmSync(outDir, { recursive: true, force: true });
mkdirSync(outDir, { recursive: true });

for (const key of Object.keys(ENTRIES)) {
  if (only.length && !only.includes(key)) continue;
  await build({ configFile: resolve(root, 'vite.config.js'), mode: key, root });
  console.log('✓', key);
}
for (const f of readdirSync(outDir)) {
  console.log(' ', f.padEnd(28), Math.round(statSync(resolve(outDir, f)).size / 1024) + ' kB');
}
