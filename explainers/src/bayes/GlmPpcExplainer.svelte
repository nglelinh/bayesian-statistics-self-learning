<script>
  import Stepper from '../shared/Stepper.svelte';
  import Plot from '../shared/Plot.svelte';
  import { tr, norm, fmt } from '../shared/i18n.js';
  import { gridPosterior, meanFn } from './glm.js';
  import { genLogistic, genZeroInflated, logisticPPC, poissonZerosPPC } from './glmppc.js';

  let { lang: langProp = 'vi', tab: tabProp = 'logistic' } = $props();
  const lang = norm(langProp), T = (v, e) => tr(lang, v, e);
  let kind = $state(tabProp === 'poisson' ? 'poisson' : 'logistic'), truthKey = $state('bad'), step = $state(0), seed = $state(5);
  $effect(() => { kind; truthKey; seed; step = 0; });
  const n = 300;
  // ---- logistic
  const lg = $derived(truthKey === 'ok' ? genLogistic(n, { c: 0 }, seed) : genLogistic(n, { a: 0.4, b: 0.3, c: -1.2 }, seed));
  const lpost = $derived(gridPosterior('logistic', lg.xs, lg.ys, 3, 41));
  const lppc = $derived(logisticPPC(lg.xs, lg.ys, lpost, 200, seed, 8));
  const gx = Array.from({ length: 41 }, (_, i) => -2 + (4 * i) / 40);
  const lLayers = $derived.by(() => {
    const L = [{ type: 'points', pts: lg.xs.map((x, i) => [x, lg.ys[i] * 0.94 + 0.03]), color: '#94a3b8', r: 2, opacity: 0.45 }, { type: 'line', pts: gx.map((x) => [x, meanFn('logistic', lpost.meanA, lpost.meanB, x)]), color: '#1d4ed8', width: 2.4 }];
    if (step === 1) lppc.repLines.forEach((ln) => L.push({ type: 'line', pts: ln.filter((p) => p[1] !== null), color: '#3b82f6', width: 1, opacity: 0.35 }));
    if (step >= 1) L.push({ type: 'line', pts: lppc.bins.filter((b) => b.obs !== null).map((b) => [b.x, b.obs]), color: '#0f172a', width: 2 });
    if (step >= 2) lppc.bins.forEach((b) => { if (b.obs === null) return; const out = b.obs < b.lo || b.obs > b.hi; L.push({ type: 'seg', x1: b.x, x2: b.x, y1: b.lo, y2: b.hi, color: '#16a34a', width: 7, opacity: 0.4 }, { type: 'points', pts: [[b.x, b.obs]], color: out ? '#dc2626' : '#0f172a', r: 5 }); });
    return L;
  });
  const lout = $derived(lppc.bins.filter((b) => b.obs !== null && (b.obs < b.lo || b.obs > b.hi)).length);
  const sc = $derived([...lppc.Trep.map((t, i) => [t, lppc.Tobs[i]])]);
  const smax = $derived(Math.max(5, ...sc.map((p) => Math.max(p[0], p[1]))) * 1.05);
  const lScat = $derived([{ type: 'seg', x1: 0, y1: 0, x2: smax, y2: smax, color: '#94a3b8', dash: '4 3', width: 1.4 }, { type: 'points', pts: sc, color: lppc.ppp < 0.05 ? '#dc2626' : '#2563eb', r: 2.4, opacity: 0.5 }]);
  // ---- poisson
  const pd = $derived(truthKey === 'ok' ? genZeroInflated(n, { pi: 0 }, seed) : genZeroInflated(n, { pi: 0.35 }, seed));
  const ppost = $derived(gridPosterior('poisson', pd.xs, pd.ys, 3, 41));
  const pppc = $derived(poissonZerosPPC(pd.xs, pd.ys, ppost, 300, seed, 12));
  const ks = Array.from({ length: 13 }, (_, k) => k);
  const pLayers = $derived.by(() => {
    const L = [{ type: 'bars', bars: ks.map((k) => ({ x0: k - 0.4, x1: k + 0.4, h: pppc.obsPmf[k], color: '#cbd5e1' })) }, { type: 'points', pts: ks.map((k) => [k, pppc.band[k].mean]), color: '#dc2626', r: 3.6 }];
    if (step >= 1) ks.forEach((k) => L.push({ type: 'seg', x1: k, x2: k, y1: pppc.band[k].lo, y2: pppc.band[k].hi, color: '#dc2626', width: 6, opacity: 0.3 }));
    return L;
  });
  const zh = $derived.by(() => { const lo = Math.min(...pppc.zRep, pppc.zObs) - 0.01, hi = Math.max(...pppc.zRep, pppc.zObs) + 0.01, B = 24, h = (hi - lo) / B, c = new Array(B).fill(0); pppc.zRep.forEach((z) => { c[Math.min(B - 1, Math.floor((z - lo) / h))]++; }); return { lo, hi, bars: c.map((q, i) => ({ x0: lo + i * h, x1: lo + (i + 1) * h, h: q / pppc.zRep.length })) }; });
  const msgL = $derived([
    T('Dữ liệu 0/1 và đường posterior mean của mô hình logistic tuyến tính theo x. Mô hình tốt hay không? Hãy để nó tự dự đoán.', 'The 0/1 data and the posterior-mean curve of a model that is linear in x on the logit scale. Is it good? Let the model predict for itself.'),
    T('Lấy 12 mẫu (a, b) từ posterior, mô phỏng dữ liệu sao chép và tính tỉ lệ y = 1 theo 8 nhóm x (đường xanh mảnh). Đường đen = tỉ lệ quan sát.', 'Draw 12 samples of (a, b) from the posterior, simulate replicated data and compute the rate of y = 1 in 8 bins of x (thin blue lines). Black = the observed rate.'),
    T(`Dải 90% của 200 bản sao theo từng nhóm (xanh lá). Có ${lout}/8 nhóm quan sát (chấm đỏ) nằm ngoài dải${lout >= 2 ? ' — mô hình đang bỏ sót cấu trúc.' : ' — phù hợp với mô hình.'}`, `90% band of 200 replicates in each bin (green). ${lout}/8 observed bins (red dots) fall outside${lout >= 2 ? ' — the model misses structure.' : ' — consistent with the model.'}`),
    T(`Thống kê χ² theo nhóm: mỗi chấm là một (θ, bản sao) so T_sao với T_thật dưới cùng θ. ppp = P(T_sao ≥ T_thật) = ${fmt(lppc.ppp, 3)}${lppc.ppp < 0.05 ? ' ⇒ bác bỏ: thêm số hạng bậc hai x² hoặc dùng spline.' : ' ⇒ không có bằng chứng sai lệch.'}`, `Binned χ² statistic: each dot is one (θ, replicate) comparing T_rep with T_obs under the same θ. ppp = P(T_rep ≥ T_obs) = ${fmt(lppc.ppp, 3)}${lppc.ppp < 0.05 ? ' ⇒ rejected: add an x² term or use a spline.' : ' ⇒ no evidence of misfit.'}`)
  ][Math.min(step, 3)]);
  const msgP = $derived([
    T('Tần suất các giá trị đếm (cột xám) và dự báo posterior trung bình của Poisson regression (chấm đỏ).', 'Frequencies of the observed counts (grey bars) and the posterior-predictive mean of the Poisson regression (red dots).'),
    T('Thêm dải 90% của các bản sao: nếu cột xám nằm ngoài dải ở một giá trị đếm, mô hình đang đoán sai chỗ đó. Chú ý k = 0.', 'Adding the 90% band of replicates: a grey bar outside the band at some count means the model gets that value wrong. Look at k = 0.'),
    T(`Thống kê "tỉ lệ số 0": phân phối ở các bản sao (cột đỏ) và dữ liệu thật (vạch đen = ${fmt(pppc.zObs, 3)}). ppp = ${fmt(pppc.ppp, 3)}.`, `Statistic "share of zeros": its distribution in replicates (red bars) and in the data (black line = ${fmt(pppc.zObs, 3)}). ppp = ${fmt(pppc.ppp, 3)}.`),
    T(`Kết luận: ${pppc.ppp < 0.02 ? 'quá nhiều số 0 so với Poisson ⇒ dùng Zero-Inflated Poisson hoặc NB.' : 'số 0 phù hợp với Poisson ⇒ chưa thấy lý do thêm zero-inflation.'}`, `Verdict: ${pppc.ppp < 0.02 ? 'too many zeros for a Poisson ⇒ use a Zero-Inflated Poisson or NB.' : 'zeros are consistent with the Poisson ⇒ no reason yet to add zero-inflation.'}`)
  ][Math.min(step, 3)]);
</script>

<div class="dx">
  <h4>{T('Posterior predictive check cho GLM', 'Posterior predictive checks for GLMs')}</h4>
  <div class="dx-tabs">
    <button class={kind === 'logistic' ? 'on' : 'sec'} onclick={() => (kind = 'logistic')}>{T('Logistic: hiệu chuẩn', 'Logistic: calibration')}</button>
    <button class={kind === 'poisson' ? 'on' : 'sec'} onclick={() => (kind = 'poisson')}>{T('Poisson: số 0 dư', 'Poisson: excess zeros')}</button>
  </div>
  <div class="dx-bar" style="gap:14px">
    <label>{T('Dữ liệu thật', 'True data')} <select bind:value={truthKey}>
      {#if kind === 'logistic'}<option value="bad">{T('logit có số hạng x² (mô hình bị sai)', 'logit has an x² term (misspecified)')}</option><option value="ok">{T('logit tuyến tính (mô hình đúng)', 'linear logit (well specified)')}</option>
      {:else}<option value="bad">{T('Poisson + 35% số 0 dư (mô hình sai)', 'Poisson + 35% extra zeros (misspecified)')}</option><option value="ok">{T('Poisson thuần (mô hình đúng)', 'plain Poisson (well specified)')}</option>{/if}
    </select></label>
    <button class="sec" onclick={() => (seed += 1)}>🎲</button>
  </div>
  <Stepper bind:step total={4} {lang} />
  {#if kind === 'logistic'}
    <Plot layers={lLayers} xmin={-2} xmax={2} ymin={0} ymax={1} xlabel="x" ylabel={T('tỉ lệ y = 1', 'rate of y = 1')} label="calibration" height={230} />
    <div class="dx-msg">{msgL}</div>
    {#if step >= 3}<Plot layers={lScat} xmin={0} xmax={smax} ymin={0} ymax={smax} xlabel={T('T sao chép', 'T replicated')} ylabel={T('T quan sát', 'T observed')} label="discrepancy" height={190} />{/if}
  {:else}
    <Plot layers={pLayers} xmin={-0.7} xmax={12.7} ymin={0} xticks={13} xlabel={T('giá trị đếm', 'count')} ylabel={T('tần suất', 'frequency')} label="counts" height={210} />
    <div class="dx-msg">{msgP}</div>
    {#if step >= 2}<Plot layers={[{ type: 'bars', bars: zh.bars, color: '#fca5a5' }, { type: 'vline', x: pppc.zObs, color: '#0f172a', label: T('quan sát', 'observed') }]} xmin={zh.lo} xmax={zh.hi} ymin={0} xlabel={T('tỉ lệ số 0', 'share of zeros')} ylabel={T('tỉ lệ bản sao', 'share of replicates')} label="zeros" height={170} />{/if}
  {/if}
</div>
