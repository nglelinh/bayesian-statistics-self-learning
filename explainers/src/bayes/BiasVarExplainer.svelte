<script>
  import Stepper from '../shared/Stepper.svelte';
  import Plot from '../shared/Plot.svelte';
  import { tr, norm, fmt } from '../shared/i18n.js';
  import { ensemble, decompose, GRID } from './biasvar.js';
  import { truth } from './shrink.js';

  let { lang: langProp = 'vi', tau: tauProp = '3' } = $props();
  const lang = norm(langProp), T = (v, e) => tr(lang, v, e);
  const DEG = 10, sigma = 0.3;
  let step = $state(0), tau = $state(['100', '3', '0.5'].includes(String(tauProp)) ? String(tauProp) : '3'), n = $state(20), seed = $state(2);
  const rows = $derived(Array.from({ length: DEG }, (_, d) => { const fits = ensemble(d, { n, sigma, tau: Number(tau), R: 100, seed }), dc = decompose(fits); return { d, fits, ...dc }; }));
  const m = $derived(rows[Math.min(step, DEG - 1)]);
  const clip = (v) => Math.max(-3, Math.min(3, v));
  const layers = $derived([
    ...m.F.slice(0, 15).map((f) => ({ type: 'line', pts: GRID.map((x, j) => [x, clip(f[j])]), color: '#3b82f6', width: 1, opacity: 0.22 })),
    { type: 'line', pts: GRID.map((x) => [x, truth(x)]), color: '#dc2626', width: 1.6, dash: '4 3' },
    { type: 'line', pts: GRID.map((x, j) => [x, clip(m.fbar[j])]), color: '#0f172a', width: 2.6 }
  ]);
  const TOP = 0.8, cl = (v) => Math.min(TOP, v);
  const shown = $derived(rows.slice(0, Math.min(step, DEG - 1) + 1));
  const errLayers = $derived([
    { type: 'line', pts: shown.map((r) => [r.d, cl(r.bias2)]), color: '#2563eb', width: 2.4 },
    { type: 'line', pts: shown.map((r) => [r.d, cl(r.variance)]), color: '#dc2626', width: 2.4 },
    { type: 'line', pts: shown.map((r) => [r.d, cl(r.total + sigma * sigma)]), color: '#0f172a', width: 2.6 },
    { type: 'hline', y: sigma * sigma, color: '#94a3b8', dash: '4 3' },
    { type: 'points', pts: [[m.d, cl(m.total + sigma * sigma)]], color: '#0f172a', r: 5 }
  ]);
  const best = $derived(rows.reduce((b, r) => (r.total < b.total ? r : b), rows[0]));
</script>

<div class="dx">
  <h4>{T('Bias–variance bằng mô phỏng: MSE = bias² + variance + nhiễu', 'Bias–variance by simulation: MSE = bias² + variance + noise')}</h4>
  <p class="dx-help">{T('Lặp 100 lần: mỗi lần sinh một tập dữ liệu mới quanh y = sin(πx) và khớp đa thức bậc d. Bó xanh nhạt = 15 đường khớp, đường đen đậm = trung bình của chúng, đỏ nét đứt = hàm thật. Khoảng cách đen–đỏ là bias; độ tản mạn của bó xanh là variance. Mỗi bước tăng bậc: bias² giảm, variance tăng, tổng có dạng chữ U (xám nét đứt = nhiễu σ² = 0.09 không thể giảm).', 'Repeat 100 times: each draws a new dataset around y = sin(πx) and fits a degree-d polynomial. Pale bundle = 15 fits, thick black = their average, red dashed = the true function. The black–red gap is bias; the spread of the bundle is variance. Each step raises the degree: bias² falls, variance rises, the total is U-shaped (grey dashed = irreducible noise σ² = 0.09).')}</p>
  <div class="dx-bar" style="gap:14px">
    <label>Prior <select bind:value={tau}><option value="100">{T('hầu như phẳng (τ = 100)', 'almost flat (τ = 100)')}</option><option value="3">{T('vừa (τ = 3)', 'moderate (τ = 3)')}</option><option value="0.5">{T('chặt (τ = 0.5)', 'tight (τ = 0.5)')}</option></select></label>
    <label>n <b>{n}</b> <input type="range" min="12" max="40" step="4" bind:value={n} /></label>
    <button class="sec" onclick={() => (seed += 1)}>🎲</button>
  </div>
  <Stepper bind:step total={DEG} {lang} />
  <Plot {layers} xmin={-1} xmax={1} ymin={-2} ymax={2} xlabel="x" ylabel="y" label="fits" height={220} />
  <div class="dx-msg">{T('Bậc', 'Degree')} <b>{m.d}</b> · bias² = <b>{fmt(m.bias2, 3)}</b> + variance = <b>{fmt(m.variance, 3)}</b> + σ² = {fmt(sigma * sigma, 2)} ⇒ MSE = <b>{fmt(m.total + sigma * sigma, 3)}</b>. {T('Bậc tốt nhất trong các bậc đã xét:', 'Best degree among those shown:')} {best.d}.</div>
  <Plot layers={errLayers} xmin={-0.3} xmax={DEG - 0.7} ymin={0} ymax={TOP} xticks={DEG} xlabel={T('bậc đa thức', 'polynomial degree')} ylabel="MSE" label="error curves" height={190} />
  <p class="dx-k">{T('Xanh dương = bias², đỏ = variance, đen = tổng (cắt ở 0.8). Với prior phẳng, variance bậc cao nổ rất lớn; prior chặt (ridge) nén variance lại — đổi một ít bias lấy nhiều variance.', 'Blue = bias², red = variance, black = total (capped at 0.8). With a flat prior the variance of high degrees explodes; a tight (ridge) prior tames it — trading a little bias for a lot of variance.')}</p>
</div>
