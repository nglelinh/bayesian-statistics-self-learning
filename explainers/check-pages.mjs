// Kiểm tra bằng Chrome headless: mount explainer, bấm thử các nút, bắt lỗi console.
// Dùng:  node check-pages.mjs http://127.0.0.1:4011/discrete-mathematics-for-computer-science-iuh /contents/chapter12/12_04_Euler_Hamilton_and_Graph_Traversal/ ...
// Biến môi trường: CHROME (đường dẫn Chrome), PORT (cổng CDP, mặc định 9333)
import { spawn } from 'node:child_process';
import { mkdtempSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';

const [base, ...paths] = process.argv.slice(2);
if (!base || !paths.length) {
  console.error('Cách dùng: node check-pages.mjs <base-url> <đường-dẫn-trang>...');
  process.exit(2);
}
const CHROME = process.env.CHROME || '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
const PORT = Number(process.env.PORT || 9333);
const profile = mkdtempSync(join(tmpdir(), 'dx-chrome-'));
const chrome = spawn(CHROME, ['--headless=new', '--disable-gpu', '--disable-extensions', '--no-first-run', `--user-data-dir=${profile}`, `--remote-debugging-port=${PORT}`, 'about:blank'], { stdio: 'ignore' });
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
let tabs;
for (let i = 0; i < 50; i++) {
  try { tabs = await fetch(`http://127.0.0.1:${PORT}/json/list`).then((r) => r.json()); if (tabs.some((t) => t.type === 'page')) break; } catch {}
  await sleep(200);
}
const tab = tabs.find((t) => t.type === 'page');
const ws = new WebSocket(tab.webSocketDebuggerUrl);
await new Promise((res, rej) => { ws.addEventListener('open', res); ws.addEventListener('error', rej); });
let n = 0;
const errors = [];
const waiters = new Map();
ws.addEventListener('message', (ev) => {
  const msg = JSON.parse(ev.data);
  if (msg.id && waiters.has(msg.id)) { waiters.get(msg.id)(msg); waiters.delete(msg.id); return; }
  if (msg.method === 'Runtime.exceptionThrown') {
    const d = msg.params.exceptionDetails || {};
    errors.push('exception: ' + ((d.exception && (d.exception.description || d.exception.value)) || d.text));
  }
  if (msg.method === 'Runtime.consoleAPICalled' && msg.params.type === 'error') errors.push('console.error: ' + (msg.params.args || []).map((a) => a.value || a.description).join(' '));
  if (msg.method === 'Log.entryAdded' && msg.params.entry.level === 'error') errors.push('log: ' + msg.params.entry.text + ' ' + (msg.params.entry.url || ''));
  if (msg.method === 'Page.loadEventFired') loadWaiter?.();
});
let loadWaiter = null;
const cdp = (method, params = {}) => new Promise((resolve, reject) => {
  const id = ++n;
  const t = setTimeout(() => reject(new Error('timeout ' + method)), 30000);
  waiters.set(id, (m) => { clearTimeout(t); m.error ? reject(new Error(JSON.stringify(m.error))) : resolve(m.result); });
  ws.send(JSON.stringify({ id, method, params }));
});
await cdp('Runtime.enable'); await cdp('Page.enable'); await cdp('Log.enable');

const probe = `(async () => {
  const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
  const roots = [...document.querySelectorAll('[data-demo$="-explainer"]')];
  const out = { demos: roots.map((r) => r.getAttribute('data-demo')), mounted: roots.every((r) => r.dataset.mounted === '1'), ui: roots.every((r) => r.querySelector('.dx, .gex, .bex')), svg: roots.every((r) => r.querySelector('svg, canvas, table, .dx-card, input')), hub: document.querySelectorAll('.hub-card').length, hubLinks: document.querySelectorAll('.hub-card a').length, clicks: 0, text: roots.map((r) => (r.innerText || '').slice(0, 50).replace(/\\s+/g, ' ')) };
  for (const r of roots) {
    const btns = [...r.querySelectorAll('button')];
    for (const b of btns) { if (b.disabled) continue; try { b.click(); out.clicks++; } catch (e) { out.clickError = String(e); } await sleep(15); }
    const sels = [...r.querySelectorAll('select')];
    for (const s of sels) { if (s.options.length > 1) { s.selectedIndex = s.options.length - 1; s.dispatchEvent(new Event('change', { bubbles: true })); s.dispatchEvent(new Event('input', { bubbles: true })); await sleep(15); } }
    await sleep(100);
  }
  out.afterUi = roots.every((r) => r.querySelector('.dx, .gex, .bex'));
  return JSON.stringify(out);
})()`;

let bad = 0;
for (const p of paths) {
  errors.length = 0;
  await new Promise(async (resolve) => { loadWaiter = resolve; await cdp('Page.navigate', { url: base + p }); setTimeout(resolve, 20000); });
  await sleep(700);
  let info;
  try {
    const r = await cdp('Runtime.evaluate', { expression: probe, awaitPromise: true, returnByValue: true });
    info = JSON.parse(r.result.value);
  } catch (e) { info = { error: String(e) }; }
  const hubOk = info && info.hub > 0 && info.hubLinks >= info.hub && !errors.length;
  const ok = hubOk || info && info.demos && info.demos.length && info.mounted && info.ui && info.svg && info.afterUi && !errors.length && !info.clickError;
  if (!ok) bad++;
  console.log(ok ? 'OK   ' : 'FAIL ', p, hubOk ? `[hub: ${info.hub} thẻ, ${info.hubLinks} liên kết]` : info.demos ? `[${info.demos.join(',')}] clicks=${info.clicks}` : JSON.stringify(info), errors.length ? '\n   ' + errors.slice(0, 5).join('\n   ') : '');
}
ws.close(); chrome.kill();
process.exit(bad ? 1 : 0);
