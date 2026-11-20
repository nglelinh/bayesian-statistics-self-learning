<script>
  import Stepper from '../shared/Stepper.svelte';
  import Plot from '../shared/Plot.svelte';
  import { tr, norm, fmt } from '../shared/i18n.js';
  import { DISTS, sampleMeans, skewness, runningMean } from './clt.js';
  import { histogram, normalPdf, sd as sdOf, mean } from './stats.js';

  let { lang: langProp = 'vi', tab: tabProp = 'clt', dist = 'exponential' } = $props();
  const lang = norm(langProp), T = (v, e) => tr(lang, v, e);
  let tab = $state(tabProp === 'lln' ? 'lln' : 'clt');
  let dk = $state(DISTS[dist] ? dist : 'exponential'), seed = $state(4), step = $state(0);
  $effect(() => { dk; seed; step = 0; });
  const NS = [1, 2, 5, 10, 30, 100];
  const D = $derived(DISTS[dk]);
  const n = $derived(NS[Math.min(step, NS.length - 1)]);
  const means = $derived(sampleMeans(dk, n, 3000, seed));
  const se = $derived(D.sd / Math.sqrt(n));
  const lo = $derived(Math.min(D.mean - 4 * D.sd, Math.min(...means)) ), hi = $derived(Math.max(D.mean + 4 * D.sd, Math.max(...means)));
  const view = $derived(n === 1 ? [Math.min(...means) - 0.05, Math.max(...means) + 0.05] : [D.mean - 4.2 * se, D.mean + 4.2 * se]);
  const hist = $derived(histogram(means, view[0], view[1], 40));
  const curve = $derived(Array.from({ length: 201 }, (_, i) => { const x = view[0] + (view[1] - view[0]) * i / 200; return [x, normalPdf(x, D.mean, se)]; }));
  const layers = $derived([{ type: 'bars', bars: hist.map((h) => ({ x0: h.x0, x1: h.x1, h: h.density })), color: '#93c5fd', opacity: 0.85 }, { type: 'line', pts: curve, color: '#dc2626', width: 2 }, { type: 'vline', x: D.mean, color: '#0f172a', dash: '4 3' }]);
  // LLN
  const CK = [10, 25, 50, 100, 250, 500, 1000, 2000];
  let lstep = $state(0);
  $effect(() => { dk; seed; lstep = 0; });
  const lines = $derived([0, 1, 2, 3, 4].map((i) => runningMean(dk, 2000, seed * 10 + i)));
  const N = $derived(CK[Math.min(lstep, CK.length - 1)]);
  const lLayers = $derived([...lines.map((l, i) => ({ type: 'line', pts: l.slice(0, N).map((v, j) => [j + 1, v]), color: ['#1d4ed8', '#dc2626', '#16a34a', '#f59e0b', '#7c3aed'][i], width: 1.2, opacity: 0.85 })), { type: 'hline', y: D.mean, color: '#0f172a', dash: '4 3' }]);
  const yr = $derived([D.mean - 1.2 * D.sd, D.mean + 1.2 * D.sd]);
</script>

<div class="dx">
  <h4>{T('Luật số lớn và định lý giới hạn trung tâm', 'Law of large numbers and the central limit theorem')}</h4>
  <div class="dx-tabs">
    <button class={tab === 'clt' ? 'on' : 'sec'} onclick={() => (tab = 'clt')}>CLT</button>
    <button class={tab === 'lln' ? 'on' : 'sec'} onclick={() => (tab = 'lln')}>{T('Luật số lớn', 'Law of large numbers')}</button>
  </div>
  <div class="dx-bar"><label>{T('Phân phối gốc', 'Source distribution')} <select bind:value={dk}>{#each Object.entries(DISTS) as [k, v]}<option value={k}>{v[lang]}</option>{/each}</select></label><button class="sec" onclick={() => (seed += 1)}>🎲</button></div>
  {#if tab === 'clt'}
    <p class="dx-help">{T('Lấy 3000 mẫu, mỗi mẫu cỡ n, rồi vẽ histogram của 3000 trung bình mẫu. Khi n tăng, hình dạng tiến tới chuẩn (đường đỏ) với độ lệch chuẩn σ/√n, dù phân phối gốc lệch đến đâu.', 'Draw 3000 samples of size n and plot the histogram of the 3000 sample means. As n grows the shape approaches the normal curve (red) with sd σ/√n, however skewed the source is.')}</p>
    <Stepper bind:step total={NS.length} {lang} />
    <Plot {layers} xmin={view[0]} xmax={view[1]} xlabel={T('trung bình mẫu', 'sample mean')} ylabel={T('mật độ', 'density')} label="CLT" />
    <div class="dx-msg">n = <b>{n}</b>: {T('sd thực của các trung bình', 'observed sd of means')} = {fmt(sdOf(means), 4)} {T('so với', 'vs')} σ/√n = {fmt(se, 4)} · {T('độ lệch (skewness)', 'skewness')} = {fmt(skewness(means), 2)}.</div>
  {:else}
    <p class="dx-help">{T('Năm chuỗi mô phỏng độc lập: trung bình chạy x̄ₙ dao động mạnh khi n nhỏ rồi hội tụ về μ (đường đen nét đứt).', 'Five independent simulations: the running mean x̄ₙ wobbles for small n and settles at μ (dashed black).')}</p>
    <Stepper bind:step={lstep} total={CK.length} {lang} />
    <Plot layers={lLayers} xmin={1} xmax={N} ymin={yr[0]} ymax={yr[1]} xlabel="n" ylabel={T('trung bình chạy', 'running mean')} label="LLN" />
    <div class="dx-msg">n = <b>{N}</b>: {T('khoảng cách tới μ của 5 chuỗi', 'distance to μ of the five runs')} = {lines.map((l) => fmt(Math.abs(l[N - 1] - D.mean), 3)).join(' · ')} ({T('cỡ', 'about')} σ/√n = {fmt(D.sd / Math.sqrt(N), 3)}).</div>
  {/if}
</div>
