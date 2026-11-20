<script>
  import Stepper from '../shared/Stepper.svelte';
  import Plot from '../shared/Plot.svelte';
  import { tr, norm, fmt } from '../shared/i18n.js';
  import { simulate, gridPosterior, drawGrid, meanFn, RANGE } from './glm.js';
  import { normalPdf, sampleQuantile } from './stats.js';

  let { lang: langProp = 'vi', tab: tabProp = 'logistic' } = $props();
  const lang = norm(langProp), T = (v, e) => tr(lang, v, e);
  const STEPS = [0, 1, 2, 3, 5, 8, 12, 16, 24, 32, 45, 60];
  let kind = $state(tabProp === 'poisson' ? 'poisson' : 'logistic'), seed = $state(5), tau = $state(2.5), step = $state(0);
  $effect(() => { kind; seed; step = 0; });
  const truth = $derived(RANGE[kind].truth);
  const all = $derived(simulate(kind, 60, truth[0], truth[1], seed));
  const n = $derived(STEPS[Math.min(step, STEPS.length - 1)]);
  const xs = $derived(all.xs.slice(0, n)), ys = $derived(all.ys.slice(0, n));
  const post = $derived(gridPosterior(kind, xs, ys, tau, 61));
  const draws = $derived(drawGrid(post, 200, 3));
  const gx = Array.from({ length: 61 }, (_, i) => -2 + (4 * i) / 60);
  const cap = $derived(kind === 'poisson' ? 14 : 1);
  const cv = (a, b) => gx.map((x) => [x, Math.min(cap, meanFn(kind, a, b, x))]);
  const mean = $derived(gx.map((x) => [x, Math.min(cap, draws.reduce((s, d) => s + meanFn(kind, d.a, d.b, x), 0) / draws.length)]));
  const curveLayers = $derived([
    ...draws.slice(0, 40).map((d) => ({ type: 'line', pts: cv(d.a, d.b), color: '#3b82f6', width: 1, opacity: 0.2 })),
    { type: 'line', pts: cv(truth[0], truth[1]), color: '#dc2626', width: 1.6, dash: '4 3' },
    { type: 'line', pts: mean, color: '#1d4ed8', width: 2.8 },
    { type: 'points', pts: xs.map((x, i) => [x, Math.min(cap, kind === 'logistic' ? ys[i] * 0.96 + 0.02 : ys[i])]), color: '#0f172a', r: 3.4, opacity: 0.85 }
  ]);
  const bPts = $derived(post.bs.map((b, j) => [b, post.pb[j] / post.db]));
  const priorPts = $derived(post.bs.map((b) => [b, normalPdf(b, 0, tau)]));
  const bLayers = $derived([{ type: 'area', pts: bPts, color: '#3b82f6', opacity: 0.3 }, { type: 'line', pts: bPts, color: '#1d4ed8', width: 2 }, { type: 'line', pts: priorPts, color: '#94a3b8', width: 1.5, dash: '4 3' }, { type: 'vline', x: truth[1], color: '#dc2626', dash: '3 3', label: T('thật', 'true') }, { type: 'vline', x: 0, color: '#0f172a', dash: '2 3' }]);
  const pPos = $derived(draws.filter((d) => d.b > 0).length / draws.length);
  const ratios = $derived(draws.map((d) => Math.exp(d.b)));
  const rq = $derived([sampleQuantile(ratios, 0.025), sampleQuantile(ratios, 0.5), sampleQuantile(ratios, 0.975)]);
  const scat = $derived([{ type: 'points', pts: draws.map((d) => [d.a, d.b]), color: '#3b82f6', r: 2.2, opacity: 0.45 }, { type: 'points', pts: [[truth[0], truth[1]]], color: '#dc2626', r: 5 }]);
  const rr = $derived(kind === 'logistic' ? T('odds ratio', 'odds ratio') : T('rate ratio', 'rate ratio'));
</script>

<div class="dx">
  <h4>{kind === 'logistic' ? T('Hồi quy logistic Bayes: posterior là cả họ đường cong', 'Bayesian logistic regression: the posterior is a family of curves') : T('Hồi quy Poisson Bayes: posterior là cả họ đường cong', 'Bayesian Poisson regression: the posterior is a family of curves')}</h4>
  <div class="dx-tabs">
    <button class={kind === 'logistic' ? 'on' : 'sec'} onclick={() => (kind = 'logistic')}>{T('Logistic (nhị phân)', 'Logistic (binary)')}</button>
    <button class={kind === 'poisson' ? 'on' : 'sec'} onclick={() => (kind = 'poisson')}>{T('Poisson (đếm)', 'Poisson (counts)')}</button>
  </div>
  <p class="dx-help">{kind === 'logistic'
    ? T('Mô hình P(y = 1) = sigmoid(a + b·x), prior a, b ~ N(0, τ²). Posterior được tính chính xác trên lưới 2-D (không cần MCMC). Mỗi bước thêm dữ liệu: bó đường xanh nhạt = 40 mẫu posterior, xanh đậm = trung bình, đỏ nét đứt = đường thật; chấm đen = dữ liệu.', 'Model P(y = 1) = sigmoid(a + b·x), prior a, b ~ N(0, τ²). The posterior is computed exactly on a 2-D grid (no MCMC). Each step adds data: pale bundle = 40 posterior draws, dark blue = mean, red dashed = truth; black dots = data.')
    : T('Mô hình y ~ Poisson(exp(a + b·x)), prior a, b ~ N(0, τ²). Posterior tính chính xác trên lưới 2-D. Mỗi bước thêm dữ liệu: bó đường = tốc độ kỳ vọng λ(x) khả dĩ; mỗi đơn vị x nhân tốc độ lên exp(b) lần.', 'Model y ~ Poisson(exp(a + b·x)), prior a, b ~ N(0, τ²). The posterior is computed exactly on a 2-D grid. Each step adds data: the bundle is plausible rate curves λ(x); each unit of x multiplies the rate by exp(b).')}</p>
  <div class="dx-bar" style="gap:14px">
    <label>τ <b>{tau}</b> <input type="range" min="0.5" max="10" step="0.5" bind:value={tau} /></label>
    <button class="sec" onclick={() => (seed += 1)}>🎲 {T('Dữ liệu mới', 'New data')}</button>
  </div>
  <Stepper bind:step total={STEPS.length} {lang} />
  <Plot layers={curveLayers} xmin={-2} xmax={2} ymin={0} ymax={cap} xlabel="x" ylabel={kind === 'logistic' ? 'P(y = 1)' : 'λ(x)'} label="curves" height={230} />
  <div class="dx-msg">n = {n} · {T('trung bình posterior', 'posterior mean')} b = <b>{fmt(post.meanB, 2)}</b> ({T('thật', 'true')} {truth[1]}) · P(b {'>'} 0) = <b>{fmt(pPos, 2)}</b> · {rr} = exp(b): <b>{fmt(rq[1], 2)}</b> [{fmt(rq[0], 2)}, {fmt(rq[2], 2)}]{n === 0 ? T(' — chưa có dữ liệu, chỉ còn prior.', ' — no data yet, prior only.') : ''}</div>
  <div class="dx-grid2">
    <div><Plot layers={bLayers} xmin={RANGE[kind].b[0]} xmax={RANGE[kind].b[1]} ymin={0} xlabel="b" ylabel={T('mật độ', 'density')} label="posterior b" height={180} /></div>
    <div><Plot layers={scat} xmin={RANGE[kind].a[0]} xmax={RANGE[kind].a[1]} ymin={RANGE[kind].b[0]} ymax={RANGE[kind].b[1]} xlabel="a" ylabel="b" label="joint draws" height={180} /></div>
  </div>
  <p class="dx-k">{T('Trái: posterior biên của b (nét đứt xám = prior). Phải: các mẫu (a, b) — chúng tương quan, nên bó đường không thể hiểu từng tham số riêng lẻ.', 'Left: marginal posterior of b (grey dashed = prior). Right: draws of (a, b) — they are correlated, so the bundle cannot be read parameter by parameter.')}</p>
</div>
