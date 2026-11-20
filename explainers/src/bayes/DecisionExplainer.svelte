<script>
  import Stepper from '../shared/Stepper.svelte';
  import Plot from '../shared/Plot.svelte';
  import { tr, norm, fmt } from '../shared/i18n.js';
  import { mulberry32, binomialSample, betaPdf, betaQuantile } from './stats.js';
  import { probBetter, threshold, decide, expectedLosses, expectedLoss, LOSSES, optimal, evsi, evpi, eolShip, eolHold } from './decision.js';

  let { lang: langProp = 'vi', tab: tabProp = 'threshold' } = $props();
  const lang = norm(langProp), T = (v, e) => tr(lang, v, e);
  let tab = $state(['threshold', 'loss', 'voi'].includes(tabProp) ? tabProp : 'threshold');
  let step = $state(0), seed = $state(4), trueP = $state(0.125), p0 = 0.1, ratio = $state(3), costPer = $state(0.05);
  $effect(() => { tab; seed; trueP; step = 0; });
  const grid = Array.from({ length: 201 }, (_, i) => 0.04 + (0.2 * i) / 200);

  // ---- tab threshold: dữ liệu theo lô 150 người
  const BATCH = 150, NB = 12;
  const stream = $derived.by(() => { const r = mulberry32(seed * 7 + 1); let k = 0, n = 0; return Array.from({ length: NB + 1 }, (_, i) => { if (i) { k += binomialSample(r, BATCH, trueP); n += BATCH; } return { k, n, a: 1 + k, b: 1 + n - k }; }); });
  const cur = $derived(stream[Math.min(step, NB)]);
  const pi = $derived(probBetter(cur.a, cur.b, p0));
  const cfp = 1, cfn = $derived(ratio);
  const thr = $derived(threshold(cfp, cfn));
  const dec = $derived(decide(pi, cfp, cfn));
  const loss = $derived(expectedLosses(pi, cfp, cfn));
  const postPts = $derived(grid.map((p) => [p, betaPdf(p, cur.a, cur.b)]));
  const thrLayers = $derived([
    { type: 'area', pts: postPts.filter((q) => q[0] >= p0), color: '#16a34a', opacity: 0.3 },
    { type: 'area', pts: postPts.filter((q) => q[0] <= p0), color: '#dc2626', opacity: 0.2 },
    { type: 'line', pts: postPts, color: '#1d4ed8', width: 2.4 },
    { type: 'vline', x: p0, color: '#0f172a', dash: '4 3', label: 'p₀' },
    { type: 'vline', x: trueP, color: '#dc2626', dash: '2 3', label: T('thật', 'true') }
  ]);
  const piPath = $derived(stream.slice(0, Math.min(step, NB) + 1).map((s, i) => [i, probBetter(s.a, s.b, p0)]));
  const piLayers = $derived([
    { type: 'hline', y: thr, color: '#f59e0b', dash: '5 3' }, { type: 'line', pts: piPath, color: '#1d4ed8', width: 2.2 }, { type: 'points', pts: [piPath.at(-1)], color: '#0f172a', r: 5 }
  ]);

  // ---- tab loss: posterior Beta(9,5) ≈ 8 chuyển đổi trong 12, prior phẳng — 4 hàm loss theo bước
  const KEYS = ['squared', 'absolute', 'zeroOne', 'pinball'];
  const NAMES = $derived([T('Bình phương → trung bình', 'Squared → mean'), T('Trị tuyệt đối → trung vị', 'Absolute → median'), T('0–1 → mode', '0–1 → mode'), T('Bất đối xứng (thiếu hụt tốn gấp 4) → phân vị 0.8', 'Asymmetric (under-estimating costs 4×) → 0.8 quantile')]);
  const A = 9, B = 5, lk = $derived(KEYS[Math.min(step, 3)]);
  const cs = Array.from({ length: 99 }, (_, i) => 0.02 + (0.96 * i) / 98);
  const elCurve = $derived(cs.map((c) => [c, expectedLoss(A, B, LOSSES[lk](c), 0, 1, 500)]));
  const copt = $derived(optimal[lk](A, B));
  const elMax = $derived(Math.max(...elCurve.map((q) => q[1])));
  const lossLayers = $derived([{ type: 'line', pts: elCurve, color: '#7c3aed', width: 2.4 }, { type: 'vline', x: copt, color: '#16a34a', label: 'c*' }]);
  const dens = cs.map((c) => [c, betaPdf(c, A, B)]);
  const dLayers = $derived([{ type: 'area', pts: dens, color: '#3b82f6', opacity: 0.3 }, { type: 'line', pts: dens, color: '#1d4ed8', width: 2 }, { type: 'vline', x: copt, color: '#16a34a', label: 'c*' }]);

  // ---- tab voi: mẫu thêm m người
  const MS = [0, 25, 50, 100, 200, 400, 700, 1000, 1500];
  const prior = { a: 13, b: 91 }, Ncust = 200000, val = 20;
  const ev = MS.map((m) => ({ m, v: evsi(prior.a, prior.b, p0, m) }));
  const evp = evpi(prior.a, prior.b, p0);
  const net = $derived(ev.map((e) => ({ m: e.m, v: Ncust * val * e.v - costPer * e.m })));
  const bestIdx = $derived(net.reduce((bi, e, i) => (e.v > net[bi].v ? i : bi), 0));
  const mi = $derived(Math.min(step, MS.length - 1));
  const evLayers = $derived([
    { type: 'hline', y: evp, color: '#dc2626', dash: '5 3' },
    { type: 'line', pts: ev.map((e) => [e.m, e.v]), color: '#2563eb', width: 2.4 },
    { type: 'points', pts: [[ev[mi].m, ev[mi].v]], color: '#0f172a', r: 5 }
  ]);
  const netLayers = $derived([
    { type: 'hline', y: 0, color: '#94a3b8' },
    { type: 'line', pts: net.map((e) => [e.m, e.v]), color: '#16a34a', width: 2.4 },
    { type: 'points', pts: [[net[bestIdx].m, net[bestIdx].v]], color: '#16a34a', r: 5 }, { type: 'points', pts: [[net[mi].m, net[mi].v]], color: '#0f172a', r: 5 }
  ]);
  const netLo = $derived(Math.min(0, ...net.map((e) => e.v)) * 1.1), netHi = $derived(Math.max(1, ...net.map((e) => e.v)) * 1.15);
</script>

<div class="dx">
  <h4>{T('Từ posterior đến quyết định', 'From posterior to decision')}</h4>
  <div class="dx-tabs">
    <button class={tab === 'threshold' ? 'on' : 'sec'} onclick={() => (tab = 'threshold')}>{T('Ngưỡng quyết định', 'Decision threshold')}</button>
    <button class={tab === 'loss' ? 'on' : 'sec'} onclick={() => (tab = 'loss')}>{T('Hàm mất mát', 'Loss function')}</button>
    <button class={tab === 'voi' ? 'on' : 'sec'} onclick={() => (tab = 'voi')}>{T('Giá trị thông tin', 'Value of information')}</button>
  </div>
  {#if tab === 'threshold'}
    <p class="dx-help">{T('A/B test: tỉ lệ chuyển đổi nền p₀ = 10%. Mỗi bước thêm 150 người dùng phương án B. Chỉ ship khi mất mát kỳ vọng của "ship" nhỏ hơn "giữ": (1 − π)·c_fp < π·c_fn ⇔ π > c_fp/(c_fp + c_fn), với π = P(p > p₀ | dữ liệu).', 'A/B test: baseline conversion p₀ = 10%. Each step adds 150 users on variant B. Ship only when the expected loss of shipping is below that of holding: (1 − π)·c_fp < π·c_fn ⇔ π > c_fp/(c_fp + c_fn), where π = P(p > p₀ | data).')}</p>
    <div class="dx-bar" style="gap:14px">
      <label>{T('Tỉ lệ thật của B', 'True rate of B')} <b>{(trueP * 100).toFixed(1)}%</b> <input type="range" min="0.08" max="0.16" step="0.005" bind:value={trueP} /></label>
      <label>c_fn/c_fp <b>{ratio}</b> <input type="range" min="0.25" max="6" step="0.25" bind:value={ratio} /></label>
      <button class="sec" onclick={() => (seed += 1)}>🎲 {T('Dữ liệu mới', 'New data')}</button>
    </div>
    <Stepper bind:step total={NB + 1} {lang} />
    <Plot layers={thrLayers} xmin={0.04} xmax={0.24} ymin={0} xlabel={T('tỉ lệ chuyển đổi p', 'conversion rate p')} ylabel={T('mật độ', 'density')} label="posterior" height={210} />
    <div class="dx-msg">n = {cur.n}, {T('chuyển đổi', 'conversions')} = {cur.k} ({cur.n ? fmt(cur.k / cur.n * 100, 1) : '—'}%) · π = P(p {'>'} p₀) = <b>{fmt(pi, 3)}</b> · {T('ngưỡng', 'threshold')} = {fmt(thr, 3)} · {T('mất mát kỳ vọng', 'expected loss')}: ship = {fmt(loss.ship, 3)}, {T('giữ', 'hold')} = {fmt(loss.hold, 3)} ⇒ <b class={dec === 'ship' ? 'dx-ok' : 'dx-bad'}>{dec === 'ship' ? T('SHIP B', 'SHIP B') : T('GIỮ NGUYÊN', 'HOLD')}</b>.</div>
    <Plot layers={piLayers} xmin={0} xmax={NB} ymin={0} ymax={1} xticks={NB} xlabel={T('số lô 150 người', 'batches of 150 users')} ylabel="π" label="pi path" height={160} />
    <p class="dx-k">{T('Đường cam = ngưỡng. Khi π vượt ngưỡng, quyết định đổi; chi phí bất đối xứng dời ngưỡng chứ không đổi posterior.', 'Orange = threshold. When π crosses it the decision flips; asymmetric costs move the threshold, not the posterior.')}</p>
  {:else if tab === 'loss'}
    <p class="dx-help">{T('Posterior Beta(9, 5) (8 chuyển đổi/12, prior phẳng). Một con số tóm tắt c phải làm tối thiểu mất mát kỳ vọng E[L(p, c)]. Mỗi bước đổi hàm mất mát; chấm xanh lá là c* tối ưu — khác loss thì khác điểm tóm tắt.', 'Posterior Beta(9, 5) (8 conversions of 12, flat prior). A single summary c must minimise the expected loss E[L(p, c)]. Each step changes the loss; the green line is the optimal c* — different losses give different summaries.')}</p>
    <Stepper bind:step total={4} {lang} />
    <div class="dx-msg"><b>{NAMES[Math.min(step, 3)]}</b> · c* = <b>{fmt(copt, 3)}</b> · {T('trung bình', 'mean')} = {fmt(optimal.squared(A, B), 3)} · {T('trung vị', 'median')} = {fmt(optimal.absolute(A, B), 3)} · mode = {fmt(optimal.zeroOne(A, B), 3)}</div>
    <Plot layers={lossLayers} xmin={0} xmax={1} ymin={0} ymax={elMax * 1.1} xlabel="c" ylabel={T('mất mát kỳ vọng', 'expected loss')} label="expected loss" height={190} />
    <Plot layers={dLayers} xmin={0} xmax={1} ymin={0} xlabel="p" ylabel={T('mật độ posterior', 'posterior density')} label="posterior" height={160} />
  {:else}
    <p class="dx-help">{T('Nên thu thêm dữ liệu không? Với posterior hiện tại Beta(13, 91) và baseline p₀ = 10%, EVPI (đường đỏ) là mất mát kỳ vọng nếu hành động ngay — trần giá trị của mọi thông tin. EVSI(m) là phần giảm mất mát khi thêm m người dùng. Mỗi bước thử một cỡ mẫu m; xanh lá = lợi ròng 200 000 khách × $20 × EVSI − chi phí.', 'Should we collect more data? With the current posterior Beta(13, 91) and baseline p₀ = 10%, EVPI (red) is the expected loss from acting now — the ceiling on any information value. EVSI(m) is the loss reduction from m extra users. Each step tries a sample size m; green = net gain 200 000 customers × $20 × EVSI − cost.')}</p>
    <div class="dx-bar" style="gap:14px"><label>{T('Chi phí mỗi người dùng thêm', 'Cost per extra user')} <b>${costPer.toFixed(2)}</b> <input type="range" min="0.01" max="0.5" step="0.01" bind:value={costPer} /></label></div>
    <Stepper bind:step total={MS.length} {lang} />
    <div class="dx-msg">m = <b>{ev[mi].m}</b> · EVSI = {fmt(ev[mi].v, 5)} ({fmt(ev[mi].v / evp * 100, 0)}% EVPI = {fmt(evp, 5)}) · {T('lợi ròng', 'net gain')} = <b>${fmt(net[mi].v, 0)}</b> · {T('tốt nhất trong lưới: m =', 'best on the grid: m =')} <b>{net[bestIdx].m}</b>{bestIdx === mi ? ' ✔' : ''}</div>
    <Plot layers={evLayers} xmin={0} xmax={1500} ymin={0} ymax={evp * 1.15} xlabel="m" ylabel="EVSI" label="evsi" height={190} />
    <Plot layers={netLayers} xmin={0} xmax={1500} ymin={netLo} ymax={netHi} xlabel="m" ylabel={T('lợi ròng ($)', 'net gain ($)')} label="net" height={170} />
    <p class="dx-k">{T('EVSI tăng chậm dần (lợi suất giảm dần) còn chi phí tăng tuyến tính ⇒ có cỡ mẫu tối ưu; nếu chi phí đủ cao, tốt nhất là không thu thêm (m = 0).', 'EVSI grows with diminishing returns while cost grows linearly ⇒ an optimal sample size exists; if costs are high enough, collecting nothing (m = 0) is best.')}</p>
  {/if}
</div>
