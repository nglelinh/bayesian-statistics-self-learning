<script>
  import Stepper from '../shared/Stepper.svelte';
  import Plot from '../shared/Plot.svelte';
  import { tr, norm, fmt } from '../shared/i18n.js';
  import { sineData, evalPoly, truth, samplePosterior } from './shrink.js';
  import { analyse, seDiff, pseudoBma } from './ic.js';

  let { lang: langProp = 'vi', tab: tabProp = 'waic' } = $props();
  const lang = norm(langProp), T = (v, e) => tr(lang, v, e);
  let tab = $state(tabProp === 'avg' ? 'avg' : 'waic'), seed = $state(3), step = $state(0);
  const sigma = 0.3, tau = 3, N = 20, DEG = 9;
  const data = $derived(sineData(N, sigma, seed));
  const test = sineData(300, sigma, 99);
  const models = $derived(Array.from({ length: DEG }, (_, d) => analyse(data.xs, data.ys, d, sigma, tau, test, 400, 5)));
  $effect(() => { seed; tab; step = 0; });
  const gx = Array.from({ length: 81 }, (_, i) => -1 + (2 * i) / 80);
  const clip = (v) => Math.max(-3, Math.min(3, v));
  const curve = (w) => gx.map((x) => [x, clip(evalPoly(w, x))]);
  const best = $derived(models.reduce((b, m) => (m.looSum > b.looSum ? m : b), models[0]));
  const m = $derived(models[Math.min(step, DEG - 1)]);
  // ---- tab waic: bước = bậc đa thức
  const bundle = $derived(samplePosterior(m.fit, 10, 4));
  const fitLayers = $derived([
    ...bundle.map((w) => ({ type: 'line', pts: curve(w), color: '#3b82f6', width: 1, opacity: 0.25 })),
    { type: 'line', pts: gx.map((x) => [x, truth(x)]), color: '#dc2626', width: 1.5, dash: '4 3' },
    { type: 'line', pts: curve(m.fit.w), color: '#1d4ed8', width: 2.6 },
    { type: 'points', pts: data.xs.map((x, i) => [x, data.ys[i]]), color: '#0f172a', r: 3.6 }
  ]);
  const shown = $derived(models.slice(0, step + 1));
  const all = $derived(models.flatMap((q) => [q.lppdSum, q.elpd, q.looSum, q.test]));
  const ylo = $derived(Math.max(-40, Math.min(...all)) - 1), yhi = $derived(Math.max(...all) + 1);
  const line = (k, color, dash) => ({ type: 'line', pts: shown.map((q) => [q.d, Math.max(ylo, q[k])]), color, width: 2, dash });
  const icLayers = $derived([line('lppdSum', '#94a3b8'), line('elpd', '#2563eb'), line('looSum', '#16a34a', '5 3'), line('test', '#dc2626'),
    { type: 'points', pts: [[m.d, Math.max(ylo, m.looSum)]], color: '#0f172a', r: 5 }]);
  const diffTo = $derived(m.d === best.d ? null : { d: best.looSum - m.looSum, se: seDiff(best.loo, m.loo) });
  // ---- tab avg: bước = số mô hình tham gia (bậc 0..k)
  const k = $derived(Math.min(step, DEG - 1));
  const used = $derived(models.slice(0, k + 1));
  const wts = $derived(pseudoBma(used.map((q) => q.looSum)));
  const avgPts = $derived(gx.map((x) => [x, clip(used.reduce((s, q, i) => s + wts[i] * evalPoly(q.fit.w, x), 0))]));
  const avgLayers = $derived([
    { type: 'line', pts: gx.map((x) => [x, truth(x)]), color: '#dc2626', width: 1.5, dash: '4 3' },
    ...used.map((q, i) => ({ type: 'line', pts: curve(q.fit.w), color: '#64748b', width: 1 + 3 * wts[i], opacity: 0.2 + 0.6 * wts[i] })),
    { type: 'line', pts: avgPts, color: '#16a34a', width: 3 },
    { type: 'points', pts: data.xs.map((x, i) => [x, data.ys[i]]), color: '#0f172a', r: 3.6 }
  ]);
  const wBars = $derived(used.map((q, i) => ({ x0: q.d - 0.4, x1: q.d + 0.4, h: wts[i], color: '#16a34a' })));
</script>

<div class="dx">
  <h4>{T('WAIC, LOO và so sánh mô hình', 'WAIC, LOO and model comparison')}</h4>
  <div class="dx-tabs">
    <button class={tab === 'waic' ? 'on' : 'sec'} onclick={() => (tab = 'waic')}>WAIC / LOO</button>
    <button class={tab === 'avg' ? 'on' : 'sec'} onclick={() => (tab = 'avg')}>{T('Trung bình mô hình', 'Model averaging')}</button>
  </div>
  <p class="dx-help">
    {#if tab === 'waic'}
      {T(`Cùng ${N} điểm dữ liệu nhiễu quanh y = sin(πx), ta khớp đa thức bậc 0…8 (Bayes, σ = 0.3 biết, prior N(0, 3²)). Mỗi bước tăng bậc: đường xám = lppd trong mẫu (luôn tăng), xanh dương = elpd theo WAIC = lppd − p_waic, xanh lá nét đứt = LOO chính xác, đỏ = elpd trên dữ liệu mới. WAIC và LOO bám sát đường đỏ — chúng ước lượng chất lượng dự đoán ngoài mẫu mà không cần tập kiểm tra.`,
        `The same ${N} noisy points around y = sin(πx) are fitted by polynomials of degree 0…8 (Bayesian, known σ = 0.3, prior N(0, 3²)). Each step raises the degree: grey = in-sample lppd (always grows), blue = WAIC elpd = lppd − p_waic, dashed green = exact LOO, red = elpd on new data. WAIC and LOO track the red line — they estimate out-of-sample predictive accuracy without a test set.`)}
    {:else}
      {T('Thay vì chọn một "người thắng", gán trọng số pseudo-BMA w ∝ exp(elpd_loo) cho các mô hình. Mỗi bước thêm một mô hình bậc cao hơn vào nhóm; đường xanh lá đậm là dự đoán trung bình có trọng số.', 'Instead of picking one winner, weight models by pseudo-BMA w ∝ exp(elpd_loo). Each step adds one higher-degree model to the pool; the thick green curve is the weighted-average prediction.')}
    {/if}
  </p>
  <div class="dx-bar"><button class="sec" onclick={() => (seed += 1)}>🎲 {T('Dữ liệu mới', 'New data')}</button></div>
  <Stepper bind:step total={DEG} {lang} />
  {#if tab === 'waic'}
    <Plot layers={fitLayers} xmin={-1} xmax={1} ymin={-2} ymax={2} xlabel="x" ylabel="y" label="fit" height={230} />
    <div class="dx-msg">
      {T('Bậc', 'Degree')} <b>{m.d}</b>: lppd = {fmt(m.lppdSum, 1)} · p_waic = {fmt(m.pSum, 2)} · <b>elpd_WAIC = {fmt(m.elpd, 1)}</b> · <b>elpd_LOO = {fmt(m.looSum, 1)}</b> · {T('dữ liệu mới', 'new data')} = {fmt(m.test, 1)}.
      {#if diffTo}{T('Kém mô hình tốt nhất (bậc', 'Behind the best model (degree')} {best.d}{T(')', ')')} {T('là', 'by')} {fmt(diffTo.d, 1)} ± {fmt(diffTo.se, 1)} (Δelpd ± SE){diffTo.d < 2 * diffTo.se ? T(' — chưa đủ bằng chứng phân biệt.', ' — not clearly distinguishable.') : '.'}{:else}{T('Đây là mô hình có elpd_LOO cao nhất.', 'This model has the highest elpd_LOO.')}{/if}
    </div>
    <Plot layers={icLayers} xmin={-0.3} xmax={8.3} ymin={ylo} ymax={yhi} xticks={9} xlabel={T('bậc đa thức', 'polynomial degree')} ylabel="elpd" label="ic" height={210} />
    <div style="overflow-x:auto;margin-top:8px">
      <table class="dx-t"><thead><tr><th>{T('bậc', 'deg')}</th><th>lppd</th><th>p_waic</th><th>WAIC</th><th>LOO</th><th>{T('mới', 'new')}</th></tr></thead>
        <tbody>{#each shown as q}<tr style={q.d === best.d ? 'background:#dcfce7' : ''}><td>{q.d}</td><td>{fmt(q.lppdSum, 1)}</td><td>{fmt(q.pSum, 1)}</td><td>{fmt(q.elpd, 1)}</td><td>{fmt(q.looSum, 1)}</td><td>{fmt(q.test, 1)}</td></tr>{/each}</tbody></table>
    </div>
    <p class="dx-k">{T('Hàng xanh = elpd_LOO cao nhất trong các mô hình đã xét.', 'Green row = highest elpd_LOO among the models shown.')}</p>
  {:else}
    <Plot layers={avgLayers} xmin={-1} xmax={1} ymin={-2} ymax={2} xlabel="x" ylabel="y" label="averaged fit" height={230} />
    <Plot layers={[{ type: 'bars', bars: wBars, color: '#16a34a' }]} xmin={-0.6} xmax={8.6} ymin={0} ymax={1} xticks={9} xlabel={T('bậc đa thức', 'polynomial degree')} ylabel={T('trọng số', 'weight')} label="weights" height={170} />
    <div class="dx-msg">{T('Nhóm gồm bậc 0…', 'Pool = degrees 0…')}{k} · {T('trọng số lớn nhất', 'largest weight')}: {T('bậc', 'degree')} {wts.indexOf(Math.max(...wts))} ({fmt(Math.max(...wts), 2)}). {T('Khi mô hình tốt nhất áp đảo, trung bình ≈ mô hình đó; khi nhiều mô hình ngang nhau, trọng số được chia đều.', 'When one model dominates, the average ≈ that model; when several tie, weights are shared.')}</div>
  {/if}
</div>
