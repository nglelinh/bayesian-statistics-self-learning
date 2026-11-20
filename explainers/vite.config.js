import { defineConfig } from 'vite';
import { svelte } from '@sveltejs/vite-plugin-svelte';
import cssInjectedByJs from 'vite-plugin-css-injected-by-js';
import { resolve, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';
import { ENTRIES } from './entries.mjs';

const root = dirname(fileURLToPath(import.meta.url));
const outDir = resolve(root, '../public/js/explainers');

// `npm run dev`: trang xem trước tất cả explainer.
// `npm run build`: build.mjs gọi Vite lần lượt cho từng bundle (mode = key trong entries.mjs).
export default defineConfig(({ command, mode }) => {
  if (command === 'serve') {
    return {
      plugins: [svelte()],
      root,
      server: { port: 5173, open: false }
    };
  }
  const spec = ENTRIES[mode];
  if (!spec) throw new Error('Mode không hợp lệ: ' + mode + '. Dùng: ' + Object.keys(ENTRIES).join(', '));
  return {
    plugins: [
      svelte({ onwarn: (w, handler) => (w.code === 'state_referenced_locally' ? null : handler(w)) }),
      cssInjectedByJs({ styleId: `explainer-${mode}` })
    ],
    logLevel: 'warn',
    build: {
      outDir,
      emptyOutDir: false,
      sourcemap: false,
      lib: {
        entry: resolve(root, spec.entry),
        name: spec.name,
        formats: ['iife'],
        fileName: () => `${mode}.js`
      },
      rollupOptions: { output: { inlineDynamicImports: true } }
    }
  };
});
