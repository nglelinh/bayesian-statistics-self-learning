<script>
  import Stepper from '../shared/Stepper.svelte';
  import Plot from '../shared/Plot.svelte';
  import { tr, norm, fmt } from '../shared/i18n.js';
  import { flipSequence } from './conjugate.js';
  import { marginal0, marginal1, bf10, postProb1, bfPath, jeffreys } from './bf.js';

  let { lang: langProp = 'vi', tab: tabProp = 'seq' } = $props();
  const lang = norm(langProp), T = (v, e) => tr(lang, v, e);
  let tab = $state(tabProp === 'prior' ? 'prior' : 'seq'), step = $state(0), seed = $state(3), theta = $state(0.8), priorKey = $state('1,1'), kObs = $state(14);
  $effect(() => { tab; seed; theta; priorKey; step = 0; });
  const NF = 40, CS = [0.1, 0.3, 1, 3, 10, 30, 100], N20 = 20;
  const sci = (v) => (v < 0.001 ? v.toExponential(1) : v.toFixed(4));
  const LAB = $derived([T('không đáng kể', 'barely worth a mention'), T('đáng kể', 'substantial'), T('mạnh', 'strong'), T('rất mạnh', 'very strong'), T('quyết định', 'decisive')]);
  // ---- tab seq
  const [pa, pb] = $derived(priorKey.split(',').map(Number));
  const flips = $derived(flipSequence(theta, NF, seed));
  const path = $derived(bfPath(flips, pa, pb));
  const cur = $derived(path[Math.min(step, NF)]);
  const ks = $derived(Array.from({ length: cur.n + 1 }, (_, k) => k));
  const seqPred = $derived([
    { type: 'bars', bars: ks.map((k) => ({ x0: k - 0.4, x1: k + 0.4, h: marginal1(k, cur.n, pa, pb), color: '#93c5fd' })) },
    { type: 'points', pts: ks.map((k) => [k, marginal0(k, cur.n)]), color: '#dc2626', r: 3.6 },
    { type: 'vline', x: cur.k, color: '#0f172a', dash: '3 3', label: 'k' }
  ]);
  const clip = (v) => Math.max(-3, Math.min(3, v));
  const pathLayers = $derived([
    { type: 'hline', y: 0, color: '#94a3b8' }, { type: 'hline', y: 0.5, color: '#cbd5e1', dash: '3 3' }, { type: 'hline', y: -0.5, color: '#cbd5e1', dash: '3 3' }, { type: 'hline', y: 1, color: '#cbd5e1', dash: '3 3' }, { type: 'hline', y: -1, color: '#cbd5e1', dash: '3 3' },
    { type: 'line', pts: path.slice(0, Math.min(step, NF) + 1).map((p) => [p.n, clip(p.log10)]), color: '#7c3aed', width: 2.4 },
    { type: 'points', pts: [[cur.n, clip(cur.log10)]], color: '#0f172a', r: 5 }
  ]);
  const bfNow = $derived(Math.pow(10, cur.log10)), pM1 = $derived(postProb1(bfNow, 1));
  const fav = $derived(jeffreys(cur.log10));
  // ---- tab prior
  const c = $derived(CS[Math.min(step, CS.length - 1)]);
  const bfCurve = $derived(Array.from({ length: 61 }, (_, i) => { const lc = -1.3 + (3.4 * i) / 60; return [lc, Math.log10(bf10(kObs, N20, 10 ** lc, 10 ** lc))]; }));
  const k20 = Array.from({ length: N20 + 1 }, (_, k) => k);
  const priorPred = $derived([
    { type: 'bars', bars: k20.map((k) => ({ x0: k - 0.4, x1: k + 0.4, h: marginal1(k, N20, c, c), color: '#93c5fd' })) },
    { type: 'points', pts: k20.map((k) => [k, marginal0(k, N20)]), color: '#dc2626', r: 3.4 },
    { type: 'vline', x: kObs, color: '#0f172a', dash: '3 3', label: 'k' }
  ]);
  const bfPrior = $derived(bf10(kObs, N20, c, c));
  const curveLayers = $derived([{ type: 'hline', y: 0, color: '#94a3b8' }, { type: 'line', pts: bfCurve.map((p) => [p[0], Math.max(-3, p[1])]), color: '#7c3aed', width: 2.4 }, { type: 'points', pts: [[Math.log10(c), Math.max(-3, Math.log10(bfPrior))]], color: '#0f172a', r: 5 }]);
</script>

<div class="dx">
  <h4>{T('Bayes factor và marginal likelihood', 'Bayes factor and the marginal likelihood')}</h4>
  <div class="dx-tabs">
    <button class={tab === 'seq' ? 'on' : 'sec'} onclick={() => (tab = 'seq')}>{T('Bằng chứng tích lũy', 'Accumulating evidence')}</button>
    <button class={tab === 'prior' ? 'on' : 'sec'} onclick={() => (tab = 'prior')}>{T('Độ nhạy theo prior', 'Prior sensitivity')}</button>
  </div>
  {#if tab === 'seq'}
    <p class="dx-help">{T('Hai mô hình cho đồng xu: M₀: θ = 0.5 (công bằng) và M₁: θ ~ Beta(a, b). Marginal likelihood là xác suất mô hình gán cho dữ liệu sau khi lấy trung bình theo prior: cột xanh = M₁, chấm đỏ = M₀ (đều tại các k có thể). BF₁₀ = m₁(k)/m₀(k). Mỗi bước tung thêm một lần: đường tím là log₁₀ BF₁₀ (trên 0 ủng hộ M₁; dưới 0 ủng hộ M₀).', 'Two models for a coin: M₀: θ = 0.5 (fair) and M₁: θ ~ Beta(a, b). The marginal likelihood is the probability a model gives the data after averaging over its prior: blue bars = M₁, red dots = M₀ at each possible k. BF₁₀ = m₁(k)/m₀(k). Each step adds a flip: the purple path is log₁₀ BF₁₀ (above 0 favours M₁, below 0 favours M₀).')}</p>
    <div class="dx-bar" style="gap:14px">
      <label>θ {T('thật', 'true')} <b>{theta.toFixed(2)}</b> <input type="range" min="0.5" max="0.9" step="0.05" bind:value={theta} /></label>
      <label>Prior M₁ <select bind:value={priorKey}><option value="1,1">Beta(1, 1)</option><option value="2,2">Beta(2, 2)</option><option value="10,10">Beta(10, 10)</option><option value="0.5,0.5">Beta(0.5, 0.5)</option></select></label>
      <button class="sec" onclick={() => (seed += 1)}>🎲</button>
    </div>
    <Stepper bind:step total={NF + 1} {lang} />
    <Plot layers={seqPred} xmin={-0.7} xmax={cur.n + 0.7} ymin={0} xticks={Math.min(cur.n + 1, 11)} xlabel={T('số ngửa k (n = ' + cur.n + ')', 'heads k (n = ' + cur.n + ')')} ylabel={T('xác suất dữ liệu', 'probability of data')} label="marginal likelihood" height={200} />
    <div class="dx-msg">n = {cur.n}, k = {cur.k} · m₁ = {sci(marginal1(cur.k, cur.n, pa, pb))}, m₀ = {sci(marginal0(cur.k, cur.n))} · <b>BF₁₀ = {bfNow >= 100 || bfNow < 0.01 ? bfNow.toExponential(1) : fmt(bfNow, 2)}</b> · P(M₁ | {T('dữ liệu', 'data')}) = <b>{fmt(pM1, 3)}</b> ({T('prior odds 1:1', 'prior odds 1:1')}){cur.n ? ' · ' + T('ủng hộ ', 'favours ') + (cur.log10 >= 0 ? 'M₁' : 'M₀') + ': ' + LAB[fav] : ''}.</div>
    <Plot layers={pathLayers} xmin={0} xmax={NF} ymin={-3} ymax={3} xticks={8} xlabel={T('số lần tung', 'flips')} ylabel="log₁₀ BF₁₀" label="evidence path" height={170} />
    <p class="dx-k">{T('Nếu θ thật = 0.5 đường tím trôi xuống: marginal likelihood phạt M₁ vì nó "dàn trải" xác suất cho mọi θ (hiệu ứng Occam) — bằng chứng cho M₀ tăng chậm nhưng chắc.', 'If the true θ = 0.5 the path drifts down: the marginal likelihood penalises M₁ for spreading probability over every θ (the Occam effect) — evidence for M₀ grows slowly but surely.')}</p>
  {:else}
    <p class="dx-help">{T('Với k ngửa trong 20 lần, BF₁₀ phụ thuộc mạnh vào độ rộng prior của M₁. Mỗi bước dùng prior Beta(c, c) rộng hơn hay chặt hơn (c nhỏ = prior dồn về 0 và 1, c lớn = dồn về 0.5). Prior quá phân tán hoặc quá giống M₀ đều làm BF kém thuyết phục — nên luôn kèm phân tích độ nhạy.', 'With k heads in 20 flips, BF₁₀ depends strongly on how wide the prior of M₁ is. Each step uses a wider or tighter prior Beta(c, c) (small c = mass near 0 and 1, large c = mass near 0.5). A prior that is too diffuse or too close to M₀ both weaken the BF — always report a sensitivity analysis.')}</p>
    <div class="dx-bar"><label>{T('Dữ liệu quan sát', 'Observed data')} k = <b>{kObs}</b> / 20 <input type="range" min="0" max="20" bind:value={kObs} /></label></div>
    <Stepper bind:step total={CS.length} {lang} />
    <Plot layers={priorPred} xmin={-0.7} xmax={20.7} ymin={0} xticks={11} xlabel="k" ylabel={T('xác suất dữ liệu', 'probability of data')} label="prior predictive" height={190} />
    <div class="dx-msg">Prior Beta({c}, {c}) · m₁(k) = {sci(marginal1(kObs, N20, c, c))} · m₀(k) = {sci(marginal0(kObs, N20))} · <b>BF₁₀ = {bfPrior >= 100 || bfPrior < 0.01 ? bfPrior.toExponential(1) : fmt(bfPrior, 2)}</b> · {T('ủng hộ ', 'favours ')}{bfPrior >= 1 ? 'M₁' : 'M₀'}: {LAB[jeffreys(Math.log10(bfPrior))]}.</div>
    <Plot layers={curveLayers} xmin={-1.3} xmax={2.1} ymin={-3} ymax={3} xlabel="log₁₀ c" ylabel="log₁₀ BF₁₀" label="bf vs prior" height={170} />
    <p class="dx-k">{T('Khi c → ∞ prior của M₁ trùng M₀ nên BF → 1 (log = 0). Với dữ liệu gần k = 10, BF còn nghiêng về M₀ mạnh hơn khi prior của M₁ càng rộng.', 'As c → ∞ the prior of M₁ coincides with M₀ so BF → 1 (log = 0). For data near k = 10 the BF leans further toward M₀ the wider the prior of M₁.')}</p>
  {/if}
</div>
