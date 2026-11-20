<script>
  import Stepper from '../shared/Stepper.svelte';
  import Plot from '../shared/Plot.svelte';
  import { tr, norm, fmt } from '../shared/i18n.js';
  import { flipSequence, poissonCounts } from './conjugate.js';
  import { llBinom, llPoisson, mleBinom, mlePoisson, relLik, likInterval, priorPredictiveBinom, exactPredictiveBinom } from './lik.js';
  import { betaPdf } from './stats.js';

  let { lang: langProp = 'vi', tab: tabProp = 'binom' } = $props();
  const lang = norm(langProp), T = (v, e) => tr(lang, v, e);
  let tab = $state(['binom', 'poisson', 'predictive'].includes(tabProp) ? tabProp : 'binom');
  let step = $state(0), seed = $state(3), prior = $state('1,1'), kObs = $state(9);
  $effect(() => { tab; seed; step = 0; });
  const NB = 20, NP = 15, RS = [10, 50, 200, 1000, 5000, 20000];
  const flips = $derived(flipSequence(0.7, NB, seed)), counts = $derived(poissonCounts(3, NP, seed));
  // ---- binom
  const nb = $derived(Math.min(step, NB)), kb = $derived(flips.slice(0, nb).reduce((a, b) => a + b, 0));
  const llb = $derived((t) => llBinom(kb, nb, t));
  const mb = $derived(nb ? mleBinom(kb, nb) : 0.5);
  const rb = $derived(nb ? relLik(llb, mb, 0, 1, 300) : [[0, 1], [1, 1]]);
  const ib = $derived(nb ? likInterval(llb, mb, 0, 1) : [0, 1]);
  const bLayers = $derived([{ type: 'rect', x0: ib[0], x1: ib[1], color: '#86efac', opacity: 0.3 }, { type: 'area', pts: rb, color: '#3b82f6', opacity: 0.2 }, { type: 'line', pts: rb, color: '#1d4ed8', width: 2.4 }, { type: 'vline', x: mb, color: '#16a34a', label: 'MLE' }, { type: 'vline', x: 0.7, color: '#dc2626', dash: '3 3', label: T('thật', 'true') }]);
  // ---- poisson
  const np = $derived(Math.min(step, NP)), cs = $derived(counts.slice(0, np));
  const llp = $derived((t) => llPoisson(cs, t));
  const mp = $derived(np ? mlePoisson(cs) : 3);
  const rp = $derived(np ? relLik(llp, Math.max(mp, 1e-9), 0.02, 8, 300) : [[0, 1], [8, 1]]);
  const ip = $derived(np && mp > 0 ? likInterval(llp, mp, 0.0001, 12) : [0, 8]);
  const pLayers = $derived([{ type: 'rect', x0: ip[0], x1: Math.min(8, ip[1]), color: '#86efac', opacity: 0.3 }, { type: 'area', pts: rp, color: '#3b82f6', opacity: 0.2 }, { type: 'line', pts: rp, color: '#1d4ed8', width: 2.4 }, { type: 'vline', x: mp, color: '#16a34a', label: 'MLE' }, { type: 'vline', x: 3, color: '#dc2626', dash: '3 3', label: T('thật', 'true') }]);
  // ---- prior predictive (n = 10 lần tung)
  const [pa, pb] = $derived(prior.split(',').map(Number));
  const R = $derived(RS[Math.min(step, RS.length - 1)]);
  const emp = $derived(priorPredictiveBinom(pa, pb, 10, R, seed));
  const ex = $derived(exactPredictiveBinom(pa, pb, 10));
  const tail = $derived(ex.slice(kObs).reduce((a, b) => a + b, 0)), tailSim = $derived(emp.slice(kObs).reduce((a, b) => a + b, 0));
  const prLayers = $derived([{ type: 'bars', bars: emp.map((v, k) => ({ x0: k - 0.4, x1: k + 0.4, h: v, color: k >= kObs ? '#f59e0b' : '#93c5fd' })) }, { type: 'points', pts: ex.map((v, k) => [k, v]), color: '#1d4ed8', r: 4 }]);
  const pdens = $derived(Array.from({ length: 101 }, (_, i) => [0.005 + (0.99 * i) / 100, betaPdf(0.005 + (0.99 * i) / 100, pa, pb)]));
  const flipChips = $derived(flips.slice(0, nb));
</script>

<div class="dx">
  <h4>{T('Khám phá likelihood và prior predictive', 'Exploring the likelihood and the prior predictive')}</h4>
  <div class="dx-tabs">
    <button class={tab === 'binom' ? 'on' : 'sec'} onclick={() => (tab = 'binom')}>{T('Đồng xu (nhị thức)', 'Coin (binomial)')}</button>
    <button class={tab === 'poisson' ? 'on' : 'sec'} onclick={() => (tab = 'poisson')}>{T('Cuộc gọi (Poisson)', 'Calls (Poisson)')}</button>
    <button class={tab === 'predictive' ? 'on' : 'sec'} onclick={() => (tab = 'predictive')}>Prior predictive</button>
  </div>
  {#if tab === 'binom'}
    <p class="dx-help">{T('Likelihood L(θ) là hàm của THAM SỐ khi dữ liệu đã cố định (không phải mật độ của θ). Ở đây vẽ likelihood tương đối R(θ) = L(θ)/L(θ̂). Mỗi bước thêm một lần tung (θ thật = 0.7): đỉnh (MLE) hẹp dần; vùng xanh = khoảng likelihood R ≥ 0.147 (~95%).', 'The likelihood L(θ) is a function of the PARAMETER with the data fixed (it is not a density of θ). We plot the relative likelihood R(θ) = L(θ)/L(θ̂). Each step adds one flip (true θ = 0.7): the peak (MLE) narrows; green = likelihood interval R ≥ 0.147 (~95%).')}</p>
    <div class="dx-bar"><button class="sec" onclick={() => (seed += 1)}>🎲 {T('Chuỗi mới', 'New sequence')}</button></div>
    <Stepper bind:step total={NB + 1} {lang} />
    <div class="dx-chips">{#each flipChips as f}<span class="dx-chip" style={f ? 'background:#dcfce7' : 'background:#fef3c7'}>{f ? T('N', 'H') : T('S', 'T')}</span>{/each}</div>
    <Plot layers={bLayers} xmin={0} xmax={1} ymin={0} ymax={1.1} xlabel="θ" ylabel="R(θ)" label="relative likelihood" height={220} />
    <div class="dx-msg">{kb} {T('ngửa /', 'heads /')} {nb} · {nb ? T('MLE θ̂ = k/n = ', 'MLE θ̂ = k/n = ') + fmt(mb, 3) : T('chưa có dữ liệu: likelihood phẳng, mọi θ ngang nhau', 'no data: flat likelihood, every θ is equally supported')} {nb ? `· ${T('khoảng likelihood', 'likelihood interval')} [${fmt(ib[0], 2)}, ${fmt(ib[1], 2)}]` : ''}.</div>
  {:else if tab === 'poisson'}
    <p class="dx-help">{T('Số cuộc gọi mỗi giờ ~ Poisson(λ) với λ thật = 3. Log-likelihood cộng dồn theo từng quan sát nên likelihood là TÍCH — mỗi bước nhân thêm một thừa số và đỉnh quanh trung bình mẫu hẹp lại.', 'Calls per hour ~ Poisson(λ) with true λ = 3. The log-likelihood adds over observations so the likelihood is a PRODUCT — each step multiplies in a factor and the peak around the sample mean narrows.')}</p>
    <div class="dx-bar"><button class="sec" onclick={() => (seed += 1)}>🎲</button></div>
    <Stepper bind:step total={NP + 1} {lang} />
    <div class="dx-chips">{#each cs as c}<span class="dx-chip">{c}</span>{/each}</div>
    <Plot layers={pLayers} xmin={0} xmax={8} ymin={0} ymax={1.1} xlabel="λ" ylabel="R(λ)" label="poisson likelihood" height={220} />
    <div class="dx-msg">n = {np} · {np ? `MLE λ̂ = ${T('trung bình mẫu', 'sample mean')} = ${fmt(mp, 2)}` : T('chưa có dữ liệu', 'no data yet')} {np ? `· ${T('khoảng likelihood', 'likelihood interval')} [${fmt(ip[0], 2)}, ${fmt(Math.min(ip[1], 99), 2)}]` : ''}.</div>
  {:else}
    <p class="dx-help">{T('Prior predictive: lấy θ từ prior, rồi mô phỏng dữ liệu (10 lần tung) — cho thấy prior ngụ ý bạn "mong đợi" thấy dữ liệu nào TRƯỚC khi quan sát. Cột = mô phỏng, chấm xanh = công thức đóng Beta–Binomial. Mỗi bước tăng số mô phỏng.', 'Prior predictive: draw θ from the prior, then simulate data (10 flips) — it shows which data the prior makes you "expect" BEFORE observing anything. Bars = simulation, blue dots = the closed-form Beta–Binomial. Each step raises the number of simulations.')}</p>
    <div class="dx-bar" style="gap:14px">
      <label>Prior <select bind:value={prior}><option value="1,1">Beta(1, 1)</option><option value="2,2">Beta(2, 2)</option><option value="10,10">Beta(10, 10)</option><option value="0.5,0.5">Beta(0.5, 0.5)</option><option value="8,2">Beta(8, 2)</option></select></label>
      <label>{T('Dữ liệu quan sát', 'Observed data')} k = <b>{kObs}</b> <input type="range" min="0" max="10" bind:value={kObs} /></label>
    </div>
    <Stepper bind:step total={RS.length} {lang} />
    <Plot layers={prLayers} xmin={-0.7} xmax={10.7} ymin={0} ymax={0.5} xticks={11} xlabel={T('số ngửa trong 10 lần', 'heads in 10 flips')} ylabel={T('xác suất', 'probability')} label="prior predictive" height={210} />
    <div class="dx-msg">{R} {T('mô phỏng', 'simulations')} · P(k ≥ {kObs}) {T('theo prior', 'under the prior')}: {T('mô phỏng', 'simulated')} = <b>{fmt(tailSim, 3)}</b>, {T('công thức', 'exact')} = {fmt(tail, 3)}. {tail < 0.02 ? T('Prior coi dữ liệu này là rất bất ngờ — cân nhắc lại prior.', 'The prior finds this data very surprising — reconsider the prior.') : T('Prior chấp nhận dữ liệu này là hợp lý.', 'The prior finds this data plausible.')}</div>
    <Plot layers={[{ type: 'area', pts: pdens, color: '#3b82f6', opacity: 0.25 }, { type: 'line', pts: pdens, color: '#1d4ed8', width: 2 }]} xmin={0} xmax={1} ymin={0} ymax={3} xlabel="θ" ylabel={T('mật độ prior', 'prior density')} label="prior" height={130} />
  {/if}
</div>
