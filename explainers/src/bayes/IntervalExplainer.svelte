<script>
  import Stepper from '../shared/Stepper.svelte';
  import Plot from '../shared/Plot.svelte';
  import { tr, norm, fmt } from '../shared/i18n.js';
  import { coverageSim } from './intervals.js';

  let { lang: langProp = 'vi' } = $props();
  const lang = norm(langProp), T = (v, e) => tr(lang, v, e);
  let mu = $state(1), n = $state(8), sigma = $state(2), mu0 = $state(0), tau0 = $state(1), fromPrior = $state(false), seed = $state(7), step = $state(0);
  $effect(() => { mu; n; sigma; mu0; tau0; fromPrior; seed; step = 0; });
  const SHOW = 40;
  const sim = $derived(coverageSim({ mu, sigma, n, reps: SHOW, mu0, tau0, seed, thetaFromPrior: fromPrior }));
  const big = $derived(coverageSim({ mu, sigma, n, reps: 4000, mu0, tau0, seed: seed + 1000, thetaFromPrior: fromPrior }));
  const rows = $derived(sim.rows.slice(0, step));
  const span = $derived(3 * sigma / Math.sqrt(n) + 0.8 * Math.abs(mu0 - mu) + (fromPrior ? 2 * tau0 : 0));
  const center = $derived(fromPrior ? mu0 : mu);
  const layers = $derived.by(() => {
    const L = [];
    if (!fromPrior) L.push({ type: 'vline', x: mu, color: '#0f172a', width: 1.6, label: T('μ thật', 'true μ') });
    rows.forEach((r, i) => {
      const y = i + 1;
      L.push({ type: 'seg', x1: r.conf[0], x2: r.conf[1], y1: y - 0.22, y2: y - 0.22, color: r.okC ? '#2563eb' : '#dc2626', width: 3 });
      L.push({ type: 'seg', x1: r.cred[0], x2: r.cred[1], y1: y + 0.22, y2: y + 0.22, color: r.okB ? '#f59e0b' : '#dc2626', width: 3 });
      if (fromPrior) L.push({ type: 'points', pts: [[r.theta, y]], color: '#0f172a', r: 2 });
    });
    return L;
  });
  const cC = $derived(rows.filter((r) => r.okC).length), cB = $derived(rows.filter((r) => r.okB).length);
</script>

<div class="dx">
  <h4>{T('Khoảng tin cậy (confidence) và khoảng đáng tin (credible): chạy lặp thí nghiệm', 'Confidence vs credible intervals: repeat the experiment')}</h4>
  <p class="dx-help">{T('Mỗi hàng là một thí nghiệm mới (n quan sát từ N(μ, σ²)). Xanh dương = khoảng tin cậy 95% (σ biết). Cam = khoảng đáng tin 95% với prior N(μ₀, τ₀²). Đỏ = khoảng trượt μ thật.', 'Each row is a fresh experiment (n draws from N(μ, σ²)). Blue = 95% confidence interval (σ known). Orange = 95% credible interval with prior N(μ₀, τ₀²). Red = misses the true μ.')}</p>
  <div class="dx-bar" style="gap:14px">
    <label>μ {T('thật', 'true')} <b>{mu}</b> <input type="range" min="-3" max="4" step="0.5" bind:value={mu} /></label>
    <label>n <b>{n}</b> <input type="range" min="2" max="40" bind:value={n} /></label>
    <label>σ <b>{sigma}</b> <input type="range" min="0.5" max="4" step="0.5" bind:value={sigma} /></label>
  </div>
  <div class="dx-bar" style="gap:14px">
    <label>μ₀ <b>{mu0}</b> <input type="range" min="-3" max="3" step="0.5" bind:value={mu0} /></label>
    <label>τ₀ <b>{tau0}</b> <input type="range" min="0.25" max="4" step="0.25" bind:value={tau0} /></label>
    <label><input type="checkbox" bind:checked={fromPrior} /> {T('θ lấy ngẫu nhiên từ prior', 'draw θ from the prior')}</label>
    <button class="sec" onclick={() => (seed += 1)}>🎲</button>
    <button class="sec" onclick={() => (step = SHOW)}>{T('⏭ Hiện đủ 40', '⏭ Show all 40')}</button>
  </div>
  <Stepper bind:step total={SHOW + 1} speed={4} {lang} />
  <Plot {layers} xmin={center - span} xmax={center + span} ymin={0} ymax={SHOW + 1} xticks={7} xlabel="μ" ylabel={T('thí nghiệm', 'experiment')} label="intervals" height={360} />
  <div class="dx-msg">{T('Trong', 'Among')} {rows.length} {T('thí nghiệm đã chạy', 'experiments so far')}: <b style="color:#2563eb">{T('tin cậy', 'confidence')} {cC}/{rows.length}</b> · <b style="color:#b45309">{T('đáng tin', 'credible')} {cB}/{rows.length}</b>.<br />
    {T('Độ phủ với 4000 lần lặp', 'Coverage over 4000 repetitions')}: <b>{fmt(big.confCoverage * 100, 1)}%</b> ({T('tin cậy', 'confidence')}) · <b>{fmt(big.credCoverage * 100, 1)}%</b> ({T('đáng tin', 'credible')}).</div>
  <p class="dx-k">{T('Khoảng tin cậy phủ μ cố định đúng 95% số lần lặp. Khoảng đáng tin phủ đúng 95% khi θ thật sự đến từ prior (đánh dấu ô bên trên); nếu prior lệch xa μ thật, độ phủ theo kiểu lặp có thể thấp hơn nhiều.', 'The confidence interval covers a fixed μ in exactly 95% of repetitions. The credible interval covers 95% when θ truly comes from the prior (tick the box); if the prior is far from the true μ its repeated-sampling coverage can be much lower.')}</p>
</div>
