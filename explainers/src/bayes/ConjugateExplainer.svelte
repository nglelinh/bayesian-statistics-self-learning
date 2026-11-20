<script>
  import Stepper from '../shared/Stepper.svelte';
  import Plot from '../shared/Plot.svelte';
  import { tr, norm, fmt } from '../shared/i18n.js';
  import { betaBinomial, betaPath, flipSequence, gammaPoisson, poissonCounts, normalNormal, normalData } from './conjugate.js';
  import { gridApprox } from './grid.js';
  import { betaPdf, gammaPdf, normalPdf } from './stats.js';

  let { lang: langProp = 'vi', tab: tabProp = 'betabinom', a = 1, b = 1, theta = 0.7 } = $props();
  const lang = norm(langProp), T = (v, e) => tr(lang, v, e);
  let tab = $state(['betabinom', 'gammapoisson', 'normalnormal'].includes(tabProp) ? tabProp : 'betabinom');

  // ---- Beta–Binomial
  const BP = [[1, 1, 'Beta(1, 1)', T('đều, không biết gì', 'flat, know nothing')], [2, 2, 'Beta(2, 2)', T('hơi tin công bằng', 'mildly fair')], [10, 10, 'Beta(10, 10)', T('tin mạnh công bằng', 'strongly fair')], [8, 2, 'Beta(8, 2)', T('tin thiên ngửa', 'believe heads')]];
  const bi = Math.max(0, BP.findIndex((p) => p[0] === Number(a) && p[1] === Number(b)));
  let bpi = $state(bi), th = $state(Number(theta) || 0.7), seed = $state(5), bstep = $state(0), check = $state(false);
  $effect(() => { bpi; th; seed; bstep = Math.min(bstep, 30); });
  const NF = 30;
  const flips = $derived(flipSequence(th, NF, seed));
  const bpath = $derived(betaPath(BP[bpi][0], BP[bpi][1], flips));
  const bcur = $derived(bpath[Math.min(bstep, NF)]);
  const bpost = $derived(betaBinomial(BP[bpi][0], BP[bpi][1], bcur.k, bcur.n));
  const xs = Array.from({ length: 201 }, (_, i) => i / 200);
  const bLayers = $derived.by(() => {
    const [a0, b0] = BP[bpi];
    const L = [{ type: 'rect', x0: bpost.ci[0], x1: bpost.ci[1], color: '#93c5fd', opacity: 0.3 },
      { type: 'line', pts: xs.slice(1, 200).map((x) => [x, betaPdf(x, a0, b0)]), color: '#94a3b8', dash: '5 4' },
      { type: 'area', pts: xs.slice(1, 200).map((x) => [x, betaPdf(x, bpost.a, bpost.b)]), color: '#3b82f6', opacity: 0.25 },
      { type: 'line', pts: xs.slice(1, 200).map((x) => [x, betaPdf(x, bpost.a, bpost.b)]), color: '#1d4ed8' },
      { type: 'vline', x: th, color: '#dc2626', dash: '4 3', label: T('θ thật', 'true θ') }];
    if (check) { const g = gridApprox((t) => betaPdf(t, a0, b0), bcur.k, bcur.n, 40); L.push({ type: 'points', pts: g.theta.map((t, i) => [t, g.density[i]]), color: '#0f766e', r: 3 }); }
    return L;
  });

  // ---- Gamma–Poisson
  const GP = [[1, 0.5, 'Gamma(1, 0.5)', T('mơ hồ, trung bình 2', 'vague, mean 2')], [4, 1, 'Gamma(4, 1)', T('tin ≈ 4 sự kiện', 'believe ≈ 4 events')], [20, 2, 'Gamma(20, 2)', T('tin mạnh ≈ 10', 'strong, ≈ 10')]];
  let gpi = $state(0), lam = $state(6), gseed = $state(4), gstep = $state(0);
  const counts = $derived(poissonCounts(lam, 20, gseed));
  const gcur = $derived(counts.slice(0, Math.min(gstep, 20)));
  const gpost = $derived(gammaPoisson(GP[gpi][0], GP[gpi][1], gcur));
  const gx = $derived(Array.from({ length: 241 }, (_, i) => 0.05 + i * (Math.max(16, lam * 2.2)) / 240));
  const gLayers = $derived([{ type: 'rect', x0: gpost.ci[0], x1: gpost.ci[1], color: '#93c5fd', opacity: 0.3 },
    { type: 'line', pts: gx.map((x) => [x, gammaPdf(x, GP[gpi][0], GP[gpi][1])]), color: '#94a3b8', dash: '5 4' },
    { type: 'area', pts: gx.map((x) => [x, gammaPdf(x, gpost.a, gpost.b)]), color: '#3b82f6', opacity: 0.25 },
    { type: 'line', pts: gx.map((x) => [x, gammaPdf(x, gpost.a, gpost.b)]), color: '#1d4ed8' },
    { type: 'vline', x: lam, color: '#dc2626', dash: '4 3', label: T('λ thật', 'true λ') }]);

  // ---- Normal–Normal
  let mu0 = $state(0), tau0 = $state(2), sigma = $state(2), mu = $state(3), nseed = $state(2), nstep = $state(0);
  const nd = $derived(normalData(mu, sigma, 20, nseed));
  const ncur = $derived(nd.slice(0, Math.min(nstep, 20)));
  const npost = $derived(normalNormal(mu0, tau0, sigma, ncur));
  const nx = Array.from({ length: 241 }, (_, i) => -8 + i * 18 / 240);
  const nLayers = $derived.by(() => {
    const L = [{ type: 'rect', x0: npost.ci[0], x1: npost.ci[1], color: '#93c5fd', opacity: 0.3 },
      { type: 'line', pts: nx.map((x) => [x, normalPdf(x, mu0, tau0)]), color: '#94a3b8', dash: '5 4' }];
    if (ncur.length) { const s = sigma / Math.sqrt(ncur.length); L.push({ type: 'line', pts: nx.map((x) => [x, normalPdf(x, npost.xbar, s)]), color: '#f59e0b', width: 1.6 }); }
    L.push({ type: 'area', pts: nx.map((x) => [x, normalPdf(x, npost.mu, npost.sd)]), color: '#3b82f6', opacity: 0.25 }, { type: 'line', pts: nx.map((x) => [x, normalPdf(x, npost.mu, npost.sd)]), color: '#1d4ed8' }, { type: 'vline', x: mu, color: '#dc2626', dash: '4 3', label: T('μ thật', 'true μ') });
    return L;
  });
</script>

<div class="dx">
  <h4>{T('Prior liên hợp: cập nhật từng quan sát', 'Conjugate priors: update one observation at a time')}</h4>
  <div class="dx-tabs">
    <button class={tab === 'betabinom' ? 'on' : 'sec'} onclick={() => (tab = 'betabinom')}>Beta–Binomial</button>
    <button class={tab === 'gammapoisson' ? 'on' : 'sec'} onclick={() => (tab = 'gammapoisson')}>Gamma–Poisson</button>
    <button class={tab === 'normalnormal' ? 'on' : 'sec'} onclick={() => (tab = 'normalnormal')}>Normal–Normal</button>
  </div>

  {#if tab === 'betabinom'}
    <p class="dx-help">{T('Mỗi lần tung xu, posterior Beta(a + số ngửa, b + số sấp) được cập nhật. Nét đứt xám = prior; xanh = posterior; vùng xanh nhạt = khoảng đáng tin 95%.', 'After every flip the posterior is Beta(a + heads, b + tails). Dashed grey = prior; blue = posterior; light band = 95% credible interval.')}</p>
    <div class="dx-bar">
      <label>Prior <select bind:value={bpi}>{#each BP as p, i}<option value={i}>{p[2]} — {p[3]}</option>{/each}</select></label>
      <label>{T('θ thật', 'True θ')} <b>{th}</b> <input type="range" min="0.05" max="0.95" step="0.05" bind:value={th} /></label>
      <button class="sec" onclick={() => { seed += 1; bstep = 0; }}>🎲 {T('Chuỗi mới', 'New flips')}</button>
      <label><input type="checkbox" bind:checked={check} /> {T('Đối chiếu lưới (chấm xanh lục)', 'Check with grid (green dots)')}</label>
    </div>
    <Stepper bind:step={bstep} total={NF + 1} {lang} />
    <div class="dx-trail dx-mono">{#each flips as f, i}{#if i < bstep}<span class="dx-pill {f ? 'good' : 'hot'}">{f ? T('N', 'H') : T('S', 'T')}</span>{/if}{/each}{#if bstep === 0}<span class="dx-k">{T('(chưa có dữ liệu: đường xanh = prior)', '(no data: blue = prior)')}</span>{/if}</div>
    <Plot layers={bLayers} xmin={0} xmax={1} xlabel="θ" ylabel={T('mật độ', 'density')} label="Beta posterior" />
    <div class="dx-msg">{bcur.k} {T('ngửa', 'heads')} / {bcur.n} {T('lần', 'flips')} ⇒ Beta({fmt(bpost.a, 1)}, {fmt(bpost.b, 1)}). {T('Trung bình', 'Mean')} = {fmt(bpost.mean)}{bpost.mode !== null ? ` · ${T('mode', 'mode')} = ${fmt(bpost.mode)}` : ''} · {T('khoảng đáng tin 95%', '95% credible interval')} = [{fmt(bpost.ci[0])}, {fmt(bpost.ci[1])}]. {#if bcur.n}MLE = {fmt(bcur.k / bcur.n)}.{/if}</div>

  {:else if tab === 'gammapoisson'}
    <p class="dx-help">{T('Số sự kiện mỗi giờ ~ Poisson(λ). Prior Gamma(a, b) trên λ; sau khi quan sát n khoảng với tổng S, posterior là Gamma(a + S, b + n).', 'Events per hour ~ Poisson(λ). Prior Gamma(a, b) on λ; after n intervals with total S the posterior is Gamma(a + S, b + n).')}</p>
    <div class="dx-bar">
      <label>Prior <select bind:value={gpi}>{#each GP as p, i}<option value={i}>{p[2]} — {p[3]}</option>{/each}</select></label>
      <label>{T('λ thật', 'True λ')} <b>{lam}</b> <input type="range" min="1" max="12" step="1" bind:value={lam} /></label>
      <button class="sec" onclick={() => { gseed += 1; gstep = 0; }}>🎲 {T('Dữ liệu mới', 'New data')}</button>
    </div>
    <Stepper bind:step={gstep} total={21} {lang} />
    <div class="dx-trail dx-mono">{#each gcur as c}<span class="dx-pill">{c}</span>{/each}{#if !gcur.length}<span class="dx-k">{T('(chưa có dữ liệu)', '(no data yet)')}</span>{/if}</div>
    <Plot layers={gLayers} xmin={0} xmax={Math.max(16, lam * 2.2)} xlabel="λ" ylabel={T('mật độ', 'density')} label="Gamma posterior" />
    <div class="dx-msg">n = {gcur.length}, S = {gcur.reduce((x, y) => x + y, 0)} ⇒ Gamma({fmt(gpost.a, 1)}, {fmt(gpost.b, 1)}). {T('Trung bình', 'Mean')} = {fmt(gpost.mean, 2)} · {T('khoảng 95%', '95% interval')} = [{fmt(gpost.ci[0], 2)}, {fmt(gpost.ci[1], 2)}].</div>

  {:else}
    <p class="dx-help">{T('Dữ liệu ~ N(μ, σ²) với σ đã biết, prior μ ~ N(μ₀, τ₀²). Posterior là trung bình có trọng số theo độ chính xác (1/phương sai) của prior và của trung bình mẫu.', 'Data ~ N(μ, σ²) with σ known, prior μ ~ N(μ₀, τ₀²). The posterior mean is a precision-weighted average of prior mean and sample mean.')}</p>
    <div class="dx-bar" style="gap:14px">
      <label>μ₀ <b>{mu0}</b> <input type="range" min="-4" max="4" step="0.5" bind:value={mu0} /></label>
      <label>τ₀ <b>{tau0}</b> <input type="range" min="0.5" max="5" step="0.5" bind:value={tau0} /></label>
      <label>σ <b>{sigma}</b> <input type="range" min="0.5" max="4" step="0.5" bind:value={sigma} /></label>
      <label>{T('μ thật', 'True μ')} <b>{mu}</b> <input type="range" min="-4" max="6" step="0.5" bind:value={mu} /></label>
      <button class="sec" onclick={() => { nseed += 1; nstep = 0; }}>🎲 {T('Dữ liệu mới', 'New data')}</button>
    </div>
    <Stepper bind:step={nstep} total={21} {lang} />
    <Plot layers={nLayers} xmin={-8} xmax={10} xlabel="μ" ylabel={T('mật độ', 'density')} label="Normal posterior" />
    <div class="dx-msg">n = {ncur.length}{ncur.length ? `, x̄ = ${fmt(npost.xbar, 2)}` : ''} ⇒ μ | {T('dữ liệu', 'data')} ~ N({fmt(npost.mu, 2)}, {fmt(npost.sd, 2)}²). {T('Trọng số của dữ liệu', 'Weight on data')} = {fmt(npost.weight, 2)}, {T('của prior', 'on prior')} = {fmt(1 - npost.weight, 2)}. {T('Khoảng 95%', '95% interval')} = [{fmt(npost.ci[0], 2)}, {fmt(npost.ci[1], 2)}].</div>
    <p class="dx-k">{T('Đường cam = likelihood (quanh x̄); xám nét đứt = prior; xanh = posterior.', 'Orange = likelihood (around x̄); dashed grey = prior; blue = posterior.')}</p>
  {/if}
</div>
