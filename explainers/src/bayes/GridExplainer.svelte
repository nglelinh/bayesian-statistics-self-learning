<script>
  import Stepper from '../shared/Stepper.svelte';
  import Plot from '../shared/Plot.svelte';
  import { tr, norm, fmt } from '../shared/i18n.js';
  import { gridApprox, PRIORS } from './grid.js';
  import { betaBinomial } from './conjugate.js';
  import { betaPdf } from './stats.js';

  let { lang: langProp = 'vi', prior = 'flat', k = 6, n = 9, points = 20 } = $props();
  const lang = norm(langProp), T = (v, e) => tr(lang, v, e);
  let pk = $state(PRIORS[prior] ? prior : 'flat'), K = $state(Number(k)), Nn = $state(Number(n)), N = $state(Number(points)), step = $state(0);
  $effect(() => { if (K > Nn) K = Nn; });
  const g = $derived(gridApprox(PRIORS[pk].pdf, Math.min(K, Nn), Nn, N));
  const conj = { flat: [1, 1], beta22: [2, 2], beta55: [5, 5] };
  const exact = $derived(conj[pk] ? betaBinomial(conj[pk][0], conj[pk][1], Math.min(K, Nn), Nn) : null);
  const stage = $derived(Math.min(step, 4));
  const series = $derived([g.theta.map(() => 0), g.prior, g.like, g.unnormalized, g.density][stage] ?? []);
  const barsFor = $derived(g.theta.map((t, i) => ({ x0: t - 0.5 / N, x1: t + 0.5 / N, h: series[i] })));
  const xs = Array.from({ length: 201 }, (_, i) => i / 200);
  const layers = $derived.by(() => {
    const L = [];
    if (stage >= 1) L.push({ type: 'bars', bars: barsFor, color: ['#94a3b8', '#94a3b8', '#f59e0b', '#7c3aed', '#3b82f6'][stage], opacity: 0.75 });
    if (stage >= 1) L.push({ type: 'points', pts: g.theta.map((t, i) => [t, series[i]]), color: '#0f172a', r: 2.2 });
    if (stage === 4 && exact) L.push({ type: 'line', pts: xs.slice(1, 200).map((x) => [x, exact.pdf(x)]), color: '#dc2626', width: 1.6 });
    if (stage === 0) g.theta.forEach((t) => L.push({ type: 'points', pts: [[t, 0]], color: '#0f172a', r: 2.6 }));
    return L;
  });
  const msgs = $derived([
    T(`Bước 1: chia đoạn [0, 1] thành ${N} điểm θ cách đều.`, `Step 1: split [0, 1] into ${N} equally spaced values of θ.`),
    T('Bước 2: tại mỗi θ, ghi giá trị prior p(θ).', 'Step 2: at each θ, record the prior p(θ).'),
    T(`Bước 3: tại mỗi θ, tính likelihood p(${K} ngửa trong ${Nn} | θ).`, `Step 3: at each θ compute the likelihood p(${K} heads in ${Nn} | θ).`),
    T('Bước 4: nhân prior × likelihood ⇒ posterior chưa chuẩn hóa.', 'Step 4: multiply prior × likelihood ⇒ unnormalised posterior.'),
    T('Bước 5: chia cho tổng ⇒ posterior chuẩn hóa (tổng = 1). Đường đỏ = đáp án chính xác (nếu prior liên hợp).', 'Step 5: divide by the sum ⇒ normalised posterior (sums to 1). Red line = exact answer (when the prior is conjugate).')
  ]);
</script>

<div class="dx">
  <h4>{T('Xấp xỉ lưới: prior × likelihood → posterior', 'Grid approximation: prior × likelihood → posterior')}</h4>
  <p class="dx-help">{T('Không cần công thức đóng: chỉ cần tính trên một lưới điểm rồi chuẩn hóa. Tăng số điểm để thấy xấp xỉ tiến tới posterior chính xác.', 'No closed form needed: evaluate on a grid and normalise. Add grid points and the approximation approaches the exact posterior.')}</p>
  <div class="dx-bar">
    <label>Prior <select bind:value={pk}>{#each Object.entries(PRIORS) as [key, p]}<option value={key}>{p[lang]}</option>{/each}</select></label>
  </div>
  <div class="dx-bar" style="gap:14px">
    <label>{T('Số ngửa', 'Heads')} <b>{Math.min(K, Nn)}</b> <input type="range" min="0" max={Nn} bind:value={K} /></label>
    <label>{T('Số lần tung', 'Flips')} <b>{Nn}</b> <input type="range" min="1" max="40" bind:value={Nn} /></label>
    <label>{T('Số điểm lưới', 'Grid points')} <b>{N}</b> <input type="range" min="3" max="200" bind:value={N} /></label>
  </div>
  <Stepper bind:step total={5} {lang} />
  <div class="dx-msg">{msgs[stage]}</div>
  <Plot {layers} xmin={0} xmax={1} xlabel="θ" ylabel={['', 'prior', 'likelihood', T('prior × likelihood', 'prior × likelihood'), T('mật độ posterior', 'posterior density')][stage]} label="Grid approximation" />
  {#if stage === 4}
    <div style="overflow-x:auto"><table class="dx-t dx-mono"><thead><tr><th></th><th>{T('Trung bình', 'Mean')}</th><th>SD</th><th>{T('Khoảng 95%', '95% interval')}</th></tr></thead>
      <tbody><tr><td>{T('Lưới', 'Grid')} ({N})</td><td>{fmt(g.mean, 4)}</td><td>{fmt(g.sd, 4)}</td><td>[{fmt(g.ci[0], 3)}, {fmt(g.ci[1], 3)}]</td></tr>
        {#if exact}<tr><td>{T('Chính xác', 'Exact')}</td><td>{fmt(exact.mean, 4)}</td><td>{fmt(Math.sqrt(exact.var), 4)}</td><td>[{fmt(exact.ci[0], 3)}, {fmt(exact.ci[1], 3)}]</td></tr>{/if}</tbody></table></div>
    <p class="dx-k">{T('Evidence p(dữ liệu) ≈', 'Evidence p(data) ≈')} {g.evidence.toExponential(3)}. {#if !exact}{T('Prior này không liên hợp: lưới là cách làm hợp lý.', 'This prior is not conjugate: the grid is the sensible route.')}{/if}</p>
  {/if}
</div>
