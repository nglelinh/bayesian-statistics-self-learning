<script>
  import Stepper from '../shared/Stepper.svelte';
  import Plot from '../shared/Plot.svelte';
  import { tr, norm, fmt } from '../shared/i18n.js';
  import { simulateT, rejectRate, zPower, powerSim, histDensity } from './pval.js';
  import { tPdf, normalPdf, tCdf, normalCdf } from './stats.js';

  let { lang: langProp = 'vi', tab: tabProp = 'pnull' } = $props();
  const lang = norm(langProp), T = (v, e) => tr(lang, v, e);
  let tab = $state(['pnull', 'tdist', 'power'].includes(tabProp) ? tabProp : 'pnull');
  let step = $state(0), seed = $state(2), n = $state(10), d = $state(0);
  $effect(() => { tab; seed; n; d; step = 0; });
  // ---- p-value: 2000 thí nghiệm, mỗi bước lộ thêm 200
  const sim = $derived(simulateT({ n, d, reps: 2000, seed }));
  const shown = $derived(sim.p.slice(0, 200 * (step + 1)));
  const pbars = $derived.by(() => { const c = new Array(10).fill(0); shown.forEach((p) => c[Math.min(9, Math.floor(p * 10))]++); return c.map((k, i) => ({ x0: i / 10, x1: (i + 1) / 10, h: k, color: i === 0 ? '#dc2626' : '#3b82f6' })); });
  const rej = $derived(rejectRate(shown));
  // ---- t-distribution theo n nhỏ
  const NS = [3, 4, 5, 8, 12, 20, 30, 60];
  const nt = $derived(NS[Math.min(step, NS.length - 1)]);
  const tsim = $derived(simulateT({ n: nt, d: 0, reps: 6000, seed: seed + 10 }).t);
  const tg = Array.from({ length: 161 }, (_, i) => -6 + (12 * i) / 160);
  const tLayers = $derived([
    { type: 'bars', bars: histDensity(tsim, -6, 6, 48), color: '#93c5fd' },
    { type: 'line', pts: tg.map((t) => [t, normalPdf(t)]), color: '#dc2626', width: 2, dash: '5 3' },
    { type: 'line', pts: tg.map((t) => [t, tPdf(t, nt - 1)]), color: '#1d4ed8', width: 2.4 }
  ]);
  const crit = 1.959964;
  const tailSim = $derived(tsim.filter((t) => Math.abs(t) > crit).length / tsim.length), tailT = $derived(2 * (1 - tCdf(crit, nt - 1))), tailZ = 2 * (1 - normalCdf(crit));
  // ---- công suất theo hiệu ứng d (đơn vị σ)
  const NP = [5, 10, 20, 40, 80, 160];
  const np = $derived(NP[Math.min(step, NP.length - 1)]);
  const ds = Array.from({ length: 13 }, (_, i) => i * 0.075);
  const pw = $derived(ds.map((x) => [x, powerSim(np, x, 250, 5)]));
  const pwZ = $derived(Array.from({ length: 61 }, (_, i) => [i * 0.015, zPower(np, i * 0.015)]));
  const dShow = $derived(Math.max(0, d)), pAt = $derived(powerSim(np, dShow, 600, 9));
  const pwLayers = $derived([{ type: 'hline', y: 0.05, color: '#94a3b8', dash: '3 3' }, { type: 'line', pts: pwZ, color: '#94a3b8', width: 1.5, dash: '5 3' }, { type: 'line', pts: pw, color: '#16a34a', width: 2.4 }, { type: 'points', pts: [[dShow, pAt]], color: '#0f172a', r: 5 }]);
</script>

<div class="dx">
  <h4>{T('p-value và t-test bằng mô phỏng', 'p-values and t-tests by simulation')}</h4>
  <div class="dx-tabs">
    <button class={tab === 'pnull' ? 'on' : 'sec'} onclick={() => (tab = 'pnull')}>{T('Phân phối p-value', 'Distribution of p')}</button>
    <button class={tab === 'tdist' ? 'on' : 'sec'} onclick={() => (tab = 'tdist')}>{T('Phân phối t', 't distribution')}</button>
    <button class={tab === 'power' ? 'on' : 'sec'} onclick={() => (tab = 'power')}>{T('Công suất', 'Power')}</button>
  </div>
  {#if tab === 'pnull'}
    <p class="dx-help">{T('Lặp lại một thí nghiệm nhiều lần (mỗi lần n quan sát N(d, 1), kiểm định H₀: μ = 0 bằng t-test). Khi H₀ đúng (d = 0), p-value phân phối ĐỀU trên [0, 1] ⇒ đúng 5% thí nghiệm có p < 0.05 dù không có hiệu ứng. Mỗi bước thêm 200 thí nghiệm.', 'Repeat an experiment many times (each with n observations N(d, 1), testing H₀: μ = 0 with a t-test). When H₀ is true (d = 0) the p-value is UNIFORM on [0, 1] ⇒ exactly 5% of experiments give p < 0.05 even with no effect. Each step adds 200 experiments.')}</p>
    <div class="dx-bar" style="gap:14px"><label>n <b>{n}</b> <input type="range" min="3" max="60" bind:value={n} /></label><label>{T('hiệu ứng thật d', 'true effect d')} <b>{d.toFixed(2)}</b> <input type="range" min="0" max="1" step="0.05" bind:value={d} /></label><button class="sec" onclick={() => (seed += 1)}>🎲</button></div>
    <Stepper bind:step total={10} {lang} />
    <Plot layers={[{ type: 'bars', bars: pbars }, { type: 'hline', y: shown.length / 10, color: '#16a34a', dash: '5 3' }]} xmin={0} xmax={1} ymin={0} xticks={10} xlabel="p-value" ylabel={T('số thí nghiệm', 'experiments')} label="p histogram" height={210} />
    <div class="dx-msg">{shown.length} {T('thí nghiệm', 'experiments')} · {T('tỉ lệ p < 0.05 (cột đỏ)', 'share with p < 0.05 (red bar)')} = <b>{fmt(rej * 100, 1)}%</b> {d === 0 ? T('— xấp xỉ α = 5% dù H₀ đúng; nếu chạy 20 phép thử độc lập, xác suất có ít nhất một p < 0.05 là 1 − 0.95²⁰ ≈ 64%.', '— about α = 5% although H₀ is true; with 20 independent tests the chance of at least one p < 0.05 is 1 − 0.95²⁰ ≈ 64%.') : T('— đó chính là công suất của kiểm định ở hiệu ứng này.', '— that is the power of the test at this effect size.')}</div>
  {:else if tab === 'tdist'}
    <p class="dx-help">{T('Thống kê t = (x̄ − μ₀)/(s/√n) dùng s ước lượng nên có đuôi dày hơn chuẩn khi n nhỏ. Cột xanh = 6000 giá trị t mô phỏng (H₀ đúng); xanh đậm = mật độ t với n − 1 bậc tự do; đỏ nét đứt = chuẩn. Mỗi bước tăng n: t tiến về chuẩn.', 'The statistic t = (x̄ − μ₀)/(s/√n) uses an estimated s so it has heavier tails than the normal when n is small. Blue bars = 6000 simulated t values (H₀ true); dark blue = t density with n − 1 df; red dashed = normal. Each step raises n: t approaches the normal.')}</p>
    <Stepper bind:step total={NS.length} {lang} />
    <Plot layers={tLayers} xmin={-6} xmax={6} ymin={0} ymax={0.45} xlabel="t" ylabel={T('mật độ', 'density')} label="t distribution" height={220} />
    <div class="dx-msg">n = {nt} (df = {nt - 1}) · P(|t| {'>'} 1.96): {T('mô phỏng', 'simulated')} = <b>{fmt(tailSim * 100, 1)}%</b>, {T('phân phối t', 't distribution')} = {fmt(tailT * 100, 1)}%, {T('chuẩn', 'normal')} = {fmt(tailZ * 100, 1)}%. {nt <= 8 ? T('Dùng ngưỡng chuẩn 1.96 với n nhỏ sẽ bác bỏ H₀ quá nhiều lần.', 'Using the normal cut-off 1.96 with small n rejects H₀ too often.') : T('Hai đường gần trùng nhau khi n lớn.', 'The two curves nearly coincide for large n.')}</div>
  {:else}
    <p class="dx-help">{T('Công suất = xác suất bác bỏ H₀ khi hiệu ứng thật d ≠ 0. Đường xanh lá = công suất mô phỏng t-test theo d (đơn vị σ); xám nét đứt = xấp xỉ z. Mỗi bước tăng n; chấm đen = hiệu ứng d bạn chọn.', 'Power = probability of rejecting H₀ when the true effect d ≠ 0. Green = simulated t-test power versus d (in units of σ); grey dashed = z approximation. Each step raises n; the black dot is the effect d you pick.')}</p>
    <div class="dx-bar"><label>{T('hiệu ứng d', 'effect d')} <b>{d.toFixed(2)}</b> <input type="range" min="0" max="0.9" step="0.05" bind:value={d} /></label></div>
    <Stepper bind:step total={NP.length} {lang} />
    <Plot layers={pwLayers} xmin={0} xmax={0.9} ymin={0} ymax={1} xlabel="d" ylabel={T('công suất', 'power')} label="power" height={220} />
    <div class="dx-msg">n = {np} · d = {dShow.toFixed(2)} ⇒ {T('công suất', 'power')} ≈ <b>{fmt(pAt * 100, 0)}%</b>. {T('Đường nằm sát 5% tại d = 0 (sai lầm loại I) và tăng lên 100% khi n hoặc d lớn; mẫu nhỏ thường không đủ công suất để phát hiện hiệu ứng nhỏ.', 'The curve sits at 5% when d = 0 (Type I error) and rises to 100% for large n or d; small samples rarely have enough power for small effects.')}</div>
  {/if}
</div>
