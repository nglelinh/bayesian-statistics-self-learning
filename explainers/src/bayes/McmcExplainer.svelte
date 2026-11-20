<script>
  import Stepper from '../shared/Stepper.svelte';
  import Plot from '../shared/Plot.svelte';
  import { tr, norm, fmt } from '../shared/i18n.js';
  import { TARGETS, metropolis, gibbsBvn, bvnPotential, hmc, rhat } from './mcmc.js';
  import { histogram, mean } from './stats.js';

  let { lang: langProp = 'vi', tab: tabProp = 'metropolis', target = 'beta' } = $props();
  const lang = norm(langProp), T = (v, e) => tr(lang, v, e);
  let tab = $state(['metropolis', 'gibbs', 'hmc'].includes(tabProp) ? tabProp : 'metropolis');
  const COL = ['#1d4ed8', '#dc2626', '#16a34a', '#f59e0b'];

  // ---- Metropolis
  let tk = $state(TARGETS[target] ? target : 'beta'), stepSize = $state(TARGETS[tk].step), total = $state(300), seed = $state(3), multi = $state(false), mstep = $state(0);
  $effect(() => { tk; stepSize; total; seed; multi; mstep = 0; });
  $effect(() => { stepSize = TARGETS[tk].step; });
  const TG = $derived(TARGETS[tk]);
  const run = $derived(metropolis(TG.logp, TG.start, stepSize, total, seed));
  const chainsAll = $derived(multi ? [0, 1, 2, 3].map((i) => metropolis(TG.logp, TG.lo + (i + 0.5) / 4 * (TG.hi - TG.lo), stepSize, total, seed + i + 1).chain) : []);
  const s = $derived(Math.min(mstep, total));
  const chain = $derived(run.chain.slice(0, s + 1));
  const last = $derived(s > 0 ? run.steps[s - 1] : null);
  const accSoFar = $derived(s > 0 ? run.steps.slice(0, s).filter((x) => x.accept).length / s : 0);
  const grid = $derived(Array.from({ length: 201 }, (_, i) => TG.lo + (TG.hi - TG.lo) * i / 200));
  const dens = $derived(grid.map((x) => [x, TG.pdf(x)]));
  const hist = $derived(chain.length > 5 ? histogram(chain, TG.lo, TG.hi, 40) : []);
  const dLayers = $derived.by(() => {
    const L = [];
    if (hist.length) L.push({ type: 'bars', bars: hist.map((h) => ({ x0: h.x0, x1: h.x1, h: h.density })), color: '#93c5fd', opacity: 0.8 });
    L.push({ type: 'line', pts: dens, color: '#0f172a', width: 1.6 });
    if (last) { L.push({ type: 'seg', x1: last.from, y1: 0, x2: last.prop, y2: 0, color: last.accept ? '#16a34a' : '#dc2626', width: 2 }); L.push({ type: 'points', pts: [[last.prop, TG.pdf(last.prop) || 0]], color: last.accept ? '#16a34a' : '#dc2626', r: 6, hollow: !last.accept }); }
    L.push({ type: 'points', pts: [[chain.at(-1), TG.pdf(chain.at(-1))]], color: '#1d4ed8', r: 5 });
    return L;
  });
  const tLayers = $derived.by(() => {
    if (!multi) return [{ type: 'line', pts: chain.map((x, i) => [i, x]), color: '#1d4ed8', width: 1.2 }, { type: 'hline', y: TG.mean, color: '#94a3b8', dash: '4 3' }];
    return [...chainsAll.map((c, k) => ({ type: 'line', pts: c.slice(0, s + 1).map((x, i) => [i, x]), color: COL[k], width: 1.1, opacity: 0.85 })), { type: 'hline', y: TG.mean, color: '#94a3b8', dash: '4 3' }];
  });
  const rh = $derived(multi && s >= 20 ? rhat(chainsAll.map((c) => c.slice(Math.floor(s / 2), s + 1))) : null);

  // ---- Gibbs
  let rho = $state(0.9), gseed = $state(2), gstep = $state(0);
  $effect(() => { rho; gseed; gstep = 0; });
  const gpath = $derived(gibbsBvn(rho, 40, gseed));
  const gs = $derived(Math.min(gstep, gpath.length - 1));
  const ell = (r, rr) => Array.from({ length: 81 }, (_, i) => { const t = i / 80 * 2 * Math.PI; return [rr * Math.cos(t), rr * (r * Math.cos(t) + Math.sqrt(1 - r * r) * Math.sin(t))]; });
  const gLayers = $derived.by(() => {
    const L = [{ type: 'line', pts: ell(rho, 1), color: '#94a3b8' }, { type: 'line', pts: ell(rho, 2), color: '#cbd5e1' }];
    for (let i = 1; i <= gs; i++) L.push({ type: 'seg', x1: gpath[i - 1].x, y1: gpath[i - 1].y, x2: gpath[i].x, y2: gpath[i].y, color: gpath[i].axis === 'x' ? '#f59e0b' : '#7c3aed', width: 1.4, opacity: 0.8 });
    L.push({ type: 'points', pts: gpath.slice(0, gs + 1).filter((p, i) => i % 2 === 0).map((p) => [p.x, p.y]), color: '#1d4ed8', r: 3 }, { type: 'points', pts: [[gpath[gs].x, gpath[gs].y]], color: '#dc2626', r: 5 });
    return L;
  });
  const gmsg = $derived(gs === 0 ? T('Điểm bắt đầu (−2.5, 2.5).', 'Starting point (−2.5, 2.5).') : gpath[gs].axis === 'x' ? T(`Cố định y = ${fmt(gpath[gs].y, 2)}, lấy x ~ N(ρy, 1 − ρ²) ⇒ đi ngang (cam).`, `Hold y = ${fmt(gpath[gs].y, 2)}, draw x ~ N(ρy, 1 − ρ²) ⇒ move horizontally (orange).`) : T(`Cố định x = ${fmt(gpath[gs].x, 2)}, lấy y ~ N(ρx, 1 − ρ²) ⇒ đi dọc (tím).`, `Hold x = ${fmt(gpath[gs].x, 2)}, draw y ~ N(ρx, 1 − ρ²) ⇒ move vertically (purple).`));

  // ---- HMC
  let hrho = $state(0.9), eps = $state(0.25), L = $state(10), hseed = $state(2), hstep = $state(0);
  $effect(() => { hrho; eps; L; hseed; hstep = 0; });
  const hr = $derived(hmc(bvnPotential(hrho), [-2, 2], eps, L, 40, hseed));
  const hs = $derived(Math.min(hstep, 40));
  const hLayers = $derived.by(() => {
    const A = [{ type: 'line', pts: ell(hrho, 1), color: '#94a3b8' }, { type: 'line', pts: ell(hrho, 2), color: '#cbd5e1' }];
    hr.samples.slice(0, hs + 1).forEach((q) => A.push({ type: 'points', pts: [[q[0], q[1]]], color: '#1d4ed8', r: 3, opacity: 0.7 }));
    if (hs > 0) { const t = hr.trajs[hs - 1]; A.push({ type: 'line', pts: t.path.map((q) => [q[0], q[1]]), color: t.accept ? '#16a34a' : '#dc2626', width: 1.8 }, { type: 'points', pts: t.path.map((q) => [q[0], q[1]]), color: t.accept ? '#16a34a' : '#dc2626', r: 2 }); }
    return A;
  });
  const hAcc = $derived(hs > 0 ? hr.trajs.slice(0, hs).filter((t) => t.accept).length / hs : 0);
  const ht = $derived(hs > 0 ? hr.trajs[hs - 1] : null);
</script>

<div class="dx">
  <h4>{T('MCMC từng bước: Metropolis · Gibbs · HMC', 'MCMC step by step: Metropolis · Gibbs · HMC')}</h4>
  <div class="dx-tabs">
    <button class={tab === 'metropolis' ? 'on' : 'sec'} onclick={() => (tab = 'metropolis')}>Metropolis</button>
    <button class={tab === 'gibbs' ? 'on' : 'sec'} onclick={() => (tab = 'gibbs')}>Gibbs</button>
    <button class={tab === 'hmc' ? 'on' : 'sec'} onclick={() => (tab = 'hmc')}>HMC</button>
  </div>

  {#if tab === 'metropolis'}
    <p class="dx-help">{T('Mỗi bước: đề xuất x′ = x + nhiễu chuẩn; chấp nhận với xác suất min(1, p(x′)/p(x)). Chấm tròn đặc = trạng thái hiện tại; vòng tròn = đề xuất (xanh = chấp nhận, đỏ = từ chối). Cột xanh nhạt = histogram của chuỗi.', 'Each step: propose x′ = x + Gaussian noise; accept with probability min(1, p(x′)/p(x)). Solid dot = current state; ring = proposal (green accepted, red rejected). Light bars = histogram of the chain.')}</p>
    <div class="dx-bar" style="gap:14px">
      <label>{T('Phân phối đích', 'Target')} <select bind:value={tk}>{#each Object.entries(TARGETS) as [k, v]}<option value={k}>{v[lang]}</option>{/each}</select></label>
      <label>{T('Độ rộng bước', 'Step size')} <b>{fmt(stepSize, 2)}</b> <input type="range" min="0.02" max="4" step="0.02" bind:value={stepSize} /></label>
      <label>{T('Số bước', 'Steps')} <select bind:value={total}>{#each [100, 300, 1000, 3000] as v}<option value={v}>{v}</option>{/each}</select></label>
      <label><input type="checkbox" bind:checked={multi} /> {T('4 chuỗi + R-hat', '4 chains + R-hat')}</label>
      <button class="sec" onclick={() => (seed += 1)}>🎲</button>
      <button class="sec" onclick={() => (mstep = total)}>{T('⏭ Chạy hết', '⏭ Run all')}</button>
    </div>
    <Stepper bind:step={mstep} total={total + 1} speed={4} {lang} />
    <div class="dx-msg">
      {#if !last}{T('Chuỗi bắt đầu tại', 'The chain starts at')} x₀ = {fmt(TG.start, 2)}.
      {:else}x = {fmt(last.from, 2)}, {T('đề xuất', 'proposal')} x′ = {fmt(last.prop, 2)} ⇒ {T('tỉ lệ', 'ratio')} α = {fmt(last.alpha, 3)}, u = {fmt(last.u, 3)} ⇒ <b class={last.accept ? 'dx-ok' : 'dx-bad'}>{last.accept ? T('chấp nhận', 'accept') : T('từ chối (ở lại)', 'reject (stay)')}</b>.{/if}
      {T('Tỉ lệ chấp nhận', 'Acceptance')} = {fmt(accSoFar * 100, 0)}% · {T('trung bình chuỗi', 'chain mean')} = {fmt(mean(chain), 3)} ({T('thật', 'true')} {fmt(TG.mean, 3)}){#if rh !== null} · R-hat = <b class={rh < 1.05 ? 'dx-ok' : 'dx-bad'}>{fmt(rh, 3)}</b>{/if}
    </div>
    <Plot layers={dLayers} xmin={TG.lo} xmax={TG.hi} xlabel="x" ylabel={T('mật độ', 'density')} label="Metropolis" height={200} />
    <Plot layers={tLayers} xmin={0} xmax={total} ymin={TG.lo} ymax={TG.hi} xlabel={T('bước', 'step')} ylabel="x" label="trace" height={190} />
    <p class="dx-k">{T('Thử bước rất nhỏ (chấp nhận cao nhưng đi chậm) và rất lớn (đề xuất hay bị từ chối).', 'Try a tiny step (high acceptance, slow exploration) and a huge one (most proposals rejected).')}</p>

  {:else if tab === 'gibbs'}
    <p class="dx-help">{T('Gibbs lần lượt lấy mẫu từng biến theo phân phối có điều kiện chính xác, nên luôn chấp nhận. Khi tương quan ρ lớn, các bước ngang/dọc rất ngắn và chuỗi trộn chậm.', 'Gibbs draws each variable in turn from its exact conditional, so it always accepts. With large correlation ρ the horizontal/vertical moves are short and mixing is slow.')}</p>
    <div class="dx-bar"><label>ρ <b>{rho}</b> <input type="range" min="0" max="0.98" step="0.02" bind:value={rho} /></label><button class="sec" onclick={() => (gseed += 1)}>🎲</button></div>
    <Stepper bind:step={gstep} total={gpath.length} speed={4} {lang} />
    <div class="dx-msg">{gmsg}</div>
    <div style="max-width:460px;margin:0 auto"><Plot layers={gLayers} xmin={-4} xmax={4} ymin={-4} ymax={4} width={440} height={400} xlabel="x" ylabel="y" label="Gibbs" /></div>

  {:else}
    <p class="dx-help">{T('HMC thêm “động lượng” p, rồi mô phỏng chuyển động trên mặt −log p bằng leapfrog (L bước, độ dài ε). Quỹ đạo dài đi xa mà vẫn được chấp nhận; ε quá lớn làm năng lượng lệch và bị từ chối.', 'HMC adds a momentum p and simulates motion on the −log p surface with leapfrog (L steps of size ε). Long trajectories travel far and are still accepted; too large ε breaks energy conservation and gets rejected.')}</p>
    <div class="dx-bar" style="gap:14px">
      <label>ρ <b>{hrho}</b> <input type="range" min="0" max="0.98" step="0.02" bind:value={hrho} /></label>
      <label>ε <b>{eps}</b> <input type="range" min="0.05" max="1.6" step="0.05" bind:value={eps} /></label>
      <label>L <b>{L}</b> <input type="range" min="1" max="40" step="1" bind:value={L} /></label>
      <button class="sec" onclick={() => (hseed += 1)}>🎲</button>
    </div>
    <Stepper bind:step={hstep} total={41} {lang} />
    <div class="dx-msg">{#if ht}{T('Quỹ đạo', 'Trajectory')} #{hs}: ΔH = {fmt(ht.dH, 3)} ⇒ <b class={ht.accept ? 'dx-ok' : 'dx-bad'}>{ht.accept ? T('chấp nhận', 'accept') : T('từ chối', 'reject')}</b>.&nbsp;{:else}{T('Bắt đầu tại (−2, 2).', 'Start at (−2, 2).')} {/if}{T('Tỉ lệ chấp nhận', 'Acceptance')} = {fmt(hAcc * 100, 0)}%.</div>
    <div style="max-width:460px;margin:0 auto"><Plot layers={hLayers} xmin={-4} xmax={4} ymin={-4} ymax={4} width={440} height={400} xlabel="x" ylabel="y" label="HMC" /></div>
  {/if}
</div>
