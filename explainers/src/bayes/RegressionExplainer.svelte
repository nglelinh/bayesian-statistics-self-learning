<script>
  import Stepper from '../shared/Stepper.svelte';
  import Plot from '../shared/Plot.svelte';
  import { tr, norm, fmt } from '../shared/i18n.js';
  import { lineData, ols, fitBayes, sampleLines, predict } from './regression.js';
  import { normalPdf } from './stats.js';

  let { lang: langProp = 'vi', a = 1, b = 1.5 } = $props();
  const lang = norm(langProp), T = (v, e) => tr(lang, v, e);
  let ta = $state(Number(a)), tb = $state(Number(b)), sigma = $state(1), tau = $state(3), seed = $state(4), step = $state(0);
  $effect(() => { ta; tb; sigma; tau; seed; step = Math.min(step, 25); });
  const NN = 25;
  const dat = $derived(lineData(ta, tb, sigma, NN, seed));
  const n = $derived(Math.min(step, NN));
  const xs = $derived(dat.xs.slice(0, n)), ys = $derived(dat.ys.slice(0, n));
  const fit = $derived(fitBayes(xs, ys, sigma, tau));
  const lines = $derived(sampleLines(fit, 40, 9));
  const line = (c) => [[-2.2, c.a - 2.2 * c.b], [2.2, c.a + 2.2 * c.b]];
  const gx = Array.from({ length: 45 }, (_, i) => -2.2 + 4.4 * i / 44);
  const bandHi = $derived(gx.map((x) => { const p = predict(fit, x); return [x, p.mean + 1.96 * p.sd]; })), bandLo = $derived(gx.map((x) => { const p = predict(fit, x); return [x, p.mean - 1.96 * p.sd]; }));
  const o = $derived(n >= 2 ? ols(xs, ys) : null);
  const layers = $derived([
    { type: 'area', pts: bandHi, color: '#e2e8f0', opacity: 0.0 },
    { type: 'line', pts: bandHi, color: '#94a3b8', dash: '4 3', width: 1.2 }, { type: 'line', pts: bandLo, color: '#94a3b8', dash: '4 3', width: 1.2 },
    ...lines.map((l) => ({ type: 'line', pts: line(l), color: '#3b82f6', width: 1, opacity: 0.22 })),
    { type: 'line', pts: line({ a: fit.mean[0], b: fit.mean[1] }), color: '#1d4ed8', width: 2.6 },
    ...(o ? [{ type: 'line', pts: line(o), color: '#16a34a', width: 1.6, dash: '5 3' }] : []),
    { type: 'line', pts: line({ a: ta, b: tb }), color: '#dc2626', width: 1.4, dash: '2 3' },
    { type: 'points', pts: xs.map((x, i) => [x, ys[i]]), color: '#0f172a', r: 3.6 }
  ]);
  const slope = $derived(Array.from({ length: 201 }, (_, i) => -1 + 5 * i / 200));
  const sd1 = $derived(Math.sqrt(fit.cov[1][1]));
  const sLayers = $derived([{ type: 'line', pts: slope.map((s) => [s, normalPdf(s, 0, tau)]), color: '#94a3b8', dash: '5 4' }, { type: 'area', pts: slope.map((s) => [s, normalPdf(s, fit.mean[1], sd1)]), color: '#3b82f6', opacity: 0.25 }, { type: 'line', pts: slope.map((s) => [s, normalPdf(s, fit.mean[1], sd1)]), color: '#1d4ed8' }, { type: 'vline', x: tb, color: '#dc2626', dash: '4 3', label: T('b thật', 'true b') }]);
</script>

<div class="dx">
  <h4>{T('Hồi quy tuyến tính Bayes: posterior là cả một bó đường thẳng', 'Bayesian linear regression: the posterior is a bundle of lines')}</h4>
  <p class="dx-help">{T('Mô hình y = a + b·x + ε, ε ~ N(0, σ²), prior a, b ~ N(0, τ²). Mỗi điểm dữ liệu thu hẹp bó đường thẳng khả dĩ (xanh nhạt = 40 mẫu từ posterior; xanh đậm = trung bình posterior; xanh lục nét đứt = OLS; đỏ chấm = đường thật; nét đứt xám = khoảng dự đoán 95%).', 'Model y = a + b·x + ε, ε ~ N(0, σ²), prior a, b ~ N(0, τ²). Each data point narrows the bundle of plausible lines (pale blue = 40 posterior draws; dark blue = posterior mean; green dashed = OLS; red dotted = truth; grey dashed = 95% predictive band).')}</p>
  <div class="dx-bar" style="gap:14px">
    <label>a {T('thật', 'true')} <b>{ta}</b> <input type="range" min="-2" max="3" step="0.5" bind:value={ta} /></label>
    <label>b {T('thật', 'true')} <b>{tb}</b> <input type="range" min="-3" max="3" step="0.5" bind:value={tb} /></label>
    <label>σ <b>{sigma}</b> <input type="range" min="0.25" max="2.5" step="0.25" bind:value={sigma} /></label>
    <label>{T('τ (prior)', 'τ (prior sd)')} <b>{tau}</b> <input type="range" min="0.25" max="10" step="0.25" bind:value={tau} /></label>
    <button class="sec" onclick={() => (seed += 1)}>🎲</button>
  </div>
  <Stepper bind:step total={NN + 1} {lang} />
  <Plot {layers} xmin={-2.2} xmax={2.2} ymin={-8} ymax={8} xlabel="x" ylabel="y" label="regression" height={280} />
  <div class="dx-msg">n = {n}: a | {T('dữ liệu', 'data')} ≈ {fmt(fit.mean[0], 2)} ± {fmt(Math.sqrt(fit.cov[0][0]), 2)} · b | {T('dữ liệu', 'data')} ≈ <b>{fmt(fit.mean[1], 2)} ± {fmt(sd1, 2)}</b>{#if o} · OLS: b = {fmt(o.b, 2)}{/if}. {T('Khi n = 0, bó đường thẳng chỉ phản ánh prior.', 'At n = 0 the bundle reflects only the prior.')}</div>
  <Plot layers={sLayers} xmin={-1} xmax={4} xlabel={T('độ dốc b', 'slope b')} ylabel={T('mật độ', 'density')} label="slope posterior" height={170} />
</div>
