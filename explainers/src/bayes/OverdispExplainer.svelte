<script>
  import Stepper from '../shared/Stepper.svelte';
  import Plot from '../shared/Plot.svelte';
  import { tr, norm, fmt } from '../shared/i18n.js';
  import { simulateNb, simulatePoisson, poissonPosterior, nbGrid, nbDraw, predictivePmf, nbPmf, ppcCounts, meanOf, varOf, logRMedian } from './overdisp.js';

  let { lang: langProp = 'vi', data: dataProp = 'nb' } = $props();
  const lang = norm(langProp), T = (v, e) => tr(lang, v, e);
  let ds = $state(dataProp === 'poisson' ? 'poisson' : 'nb'), n = $state(150), seed = $state(3), step = $state(0);
  $effect(() => { ds; n; seed; step = 0; });
  const K = 16;
  const counts = $derived(ds === 'nb' ? simulateNb(n, 4, 1.5, seed) : simulatePoisson(n, 3, seed));
  const ks = Array.from({ length: K + 1 }, (_, k) => k);
  const obs = $derived(ks.map((k) => counts.filter((c) => c === k).length / n));
  const pp = $derived(poissonPosterior(counts)), post = $derived(nbGrid(counts, 41)), draws = $derived(nbDraw(post, 150, 4));
  const popmf = $derived(ks.map((k) => nbPmf(k, pp.mu, pp.r))), nbp = $derived(predictivePmf(draws, K));
  const ppcP = $derived(ppcCounts(counts, 'poisson', 'ratio', 300, 5)), ppcN = $derived(ppcCounts(counts, 'nb', 'ratio', 300, 5, post));
  const bars = $derived({ type: 'bars', bars: ks.map((k) => ({ x0: k - 0.4, x1: k + 0.4, h: obs[k], color: '#cbd5e1' })) });
  const hist = (vals, lo, hi, bins) => { const h = (hi - lo) / bins, c = new Array(bins).fill(0); vals.forEach((v) => { c[Math.max(0, Math.min(bins - 1, Math.floor((v - lo) / h)))]++; }); return c.map((q, i) => ({ x0: lo + i * h, x1: lo + (i + 1) * h, h: q / vals.length })); };
  const RMAX = 6;
  const layersFor = $derived(() => {
    if (step === 0) return [bars];
    if (step === 1) return [bars, { type: 'points', pts: ks.map((k) => [k, popmf[k]]), color: '#dc2626', r: 4 }, { type: 'line', pts: ks.map((k) => [k, popmf[k]]), color: '#dc2626', width: 1.5 }];
    if (step === 2) return [{ type: 'bars', bars: hist(ppcP.reps, 0, RMAX, 30), color: '#fca5a5' }, { type: 'vline', x: Math.min(ppcP.obs, RMAX - 0.05), color: '#0f172a', label: T('quan sát', 'observed') }];
    if (step === 3) return [bars, { type: 'points', pts: ks.map((k) => [k, nbp[k]]), color: '#16a34a', r: 4 }, { type: 'line', pts: ks.map((k) => [k, nbp[k]]), color: '#16a34a', width: 1.5 }];
    return [{ type: 'bars', bars: hist(ppcN.reps, 0, RMAX, 30), color: '#86efac' }, { type: 'vline', x: Math.min(ppcN.obs, RMAX - 0.05), color: '#0f172a', label: T('quan sát', 'observed') }];
  });
  const isPmf = $derived(step !== 2 && step !== 4);
  const msg = $derived([
    T(`Dữ liệu ${n} số đếm: trung bình = ${fmt(meanOf(counts), 2)}, phương sai = ${fmt(varOf(counts), 2)} ⇒ var/mean = ${fmt(varOf(counts) / meanOf(counts), 2)} (Poisson cần ≈ 1).`, `${n} counts: mean = ${fmt(meanOf(counts), 2)}, variance = ${fmt(varOf(counts), 2)} ⇒ var/mean = ${fmt(varOf(counts) / meanOf(counts), 2)} (Poisson needs ≈ 1).`),
    T(`Khớp Poisson (posterior Gamma, dự báo Poisson–Gamma): đường đỏ. ${ds === 'nb' ? 'Nó quá hẹp: thiếu số 0 và đuôi dài.' : 'Khớp tốt.'}`, `Poisson fit (Gamma posterior, Poisson–Gamma predictive): red line. ${ds === 'nb' ? 'It is too narrow: too few zeros and too short a tail.' : 'A good fit.'}`),
    T(`PPC: tỉ số var/mean của 300 tập dữ liệu sao chép từ mô hình Poisson (cột đỏ) so với dữ liệu thật (vạch đen = ${fmt(ppcP.obs, 2)}): P(T_sao ≥ T_thật) = ${fmt(ppcP.p, 3)}${ppcP.p < 0.02 ? ' — Poisson bị bác bỏ.' : ' — không có dấu hiệu quá phân tán.'}`, `PPC: var/mean in 300 replicated datasets from the Poisson model (red bars) versus the data (black line = ${fmt(ppcP.obs, 2)}): P(T_rep ≥ T_obs) = ${fmt(ppcP.p, 3)}${ppcP.p < 0.02 ? ' — the Poisson model is rejected.' : ' — no sign of overdispersion.'}`),
    T(`Negative Binomial (μ, r): posterior của r có trung vị ≈ ${fmt(Math.exp(logRMedian(post)), 1)}${ds === 'nb' ? ' (thật 1.5)' : ' (dữ liệu Poisson ⇒ r lớn, NB ≈ Poisson)'}. Đường xanh lá bám sát dữ liệu.`, `Negative Binomial (μ, r): the posterior median of r ≈ ${fmt(Math.exp(logRMedian(post)), 1)}${ds === 'nb' ? ' (true 1.5)' : ' (Poisson data ⇒ large r, NB ≈ Poisson)'}. The green line hugs the data.`),
    T(`PPC với NB: P(T_sao ≥ T_thật) = ${fmt(ppcN.p, 3)} — dữ liệu thật nằm giữa các bản sao, mô hình mô tả được độ phân tán.`, `PPC under NB: P(T_rep ≥ T_obs) = ${fmt(ppcN.p, 3)} — the data sit among the replicates; the model captures the dispersion.`)
  ][Math.min(step, 4)]);
</script>

<div class="dx">
  <h4>{T('Quá phân tán: Poisson hay Negative Binomial?', 'Overdispersion: Poisson or Negative Binomial?')}</h4>
  <p class="dx-help">{T('Poisson ép var = mean; Negative Binomial thêm tham số r với var = μ + μ²/r. Đi qua 5 bước: nhìn dữ liệu → khớp Poisson → kiểm tra posterior predictive (PPC) → khớp NB → PPC lại. Đổi dữ liệu sang Poisson thật để thấy NB tự co về Poisson khi không cần.', 'Poisson forces var = mean; the Negative Binomial adds r with var = μ + μ²/r. Five steps: look at the data → fit Poisson → posterior predictive check (PPC) → fit NB → PPC again. Switch to truly Poisson data to see NB collapse to Poisson when it is not needed.')}</p>
  <div class="dx-bar" style="gap:14px">
    <label>{T('Dữ liệu', 'Data')} <select bind:value={ds}><option value="nb">NB (μ = 4, r = 1.5)</option><option value="poisson">Poisson (λ = 3)</option></select></label>
    <label>n <b>{n}</b> <input type="range" min="50" max="400" step="50" bind:value={n} /></label>
    <button class="sec" onclick={() => (seed += 1)}>🎲</button>
  </div>
  <Stepper bind:step total={5} {lang} />
  <Plot layers={layersFor()} xmin={isPmf ? -0.7 : 0} xmax={isPmf ? K + 0.7 : RMAX} ymin={0} xticks={isPmf ? 9 : 6} xlabel={isPmf ? T('giá trị đếm', 'count') : T('var/mean của dữ liệu sao chép', 'var/mean of replicated data')} ylabel={isPmf ? T('tần suất', 'frequency') : T('tỉ lệ', 'share')} label="overdispersion" height={230} />
  <div class="dx-msg">{msg}</div>
</div>
