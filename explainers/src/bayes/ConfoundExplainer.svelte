<script>
  import Stepper from '../shared/Stepper.svelte';
  import Plot from '../shared/Plot.svelte';
  import { tr, norm, fmt } from '../shared/i18n.js';
  import { simFork, forkBias, slope, adjustedSlope, tertiles, strataSlopes, simCollider, colliderPartialCorr, partialCorr, corr, simInteraction, fitInteraction } from './confound.js';

  let { lang: langProp = 'vi', tab: tabProp = 'fork' } = $props();
  const lang = norm(langProp), T = (v, e) => tr(lang, v, e);
  let tab = $state(['fork', 'collider', 'interaction'].includes(tabProp) ? tabProp : 'fork');
  let step = $state(0), seed = $state(3), gamma = $state(1.5), delta = $state(2), beta = $state(-0.4), se = $state(0.5), b3 = $state(1.2);
  $effect(() => { tab; seed; step = 0; });
  const COL = ['#2563eb', '#16a34a', '#dc2626'];
  const line = (b0, b1, lo, hi, color, w = 2.4, dash) => ({ type: 'line', pts: [[lo, b0 + b1 * lo], [hi, b0 + b1 * hi]], color, width: w, dash });
  // ---- fork
  const fk = $derived(simFork({ n: 500, gamma, beta, delta, seed }));
  const fkAll = $derived(simFork({ n: 20000, gamma, beta, delta, seed: 77 }));
  const g3 = $derived(tertiles(fk.z));
  const naive = $derived(slope(fkAll.x, fkAll.y)), adj = $derived(adjustedSlope(fkAll.x, fkAll.y, fkAll.z));
  const strata = $derived(strataSlopes(fkAll.x, fkAll.y, tertiles(fkAll.z)));
  const sline = (idx, b) => { const xs = idx.map((i) => fk.x[i]), my = idx.reduce((s, i) => s + fk.y[i], 0) / idx.length, mx = xs.reduce((a, c) => a + c, 0) / xs.length; return line(my - b * mx, b, Math.min(...xs), Math.max(...xs), COL[g3[idx[0]]], 2.6); };
  const fkLayers = $derived.by(() => {
    const L = [];
    if (step === 0) L.push({ type: 'points', pts: fk.x.map((x, i) => [x, fk.y[i]]), color: '#64748b', r: 2.4, opacity: 0.6 }, line(0, 0, -5, 5, '#0f172a', 0), line(fkAll.y.reduce((a, b) => a + b, 0) / fkAll.y.length - naive * fkAll.x.reduce((a, b) => a + b, 0) / fkAll.x.length, naive, -5, 5, '#0f172a', 3));
    else {
      for (let k = 0; k < 3; k++) L.push({ type: 'points', pts: fk.x.map((x, i) => (g3[i] === k ? [x, fk.y[i]] : null)).filter(Boolean), color: COL[k], r: 2.4, opacity: 0.55 });
      if (step >= 1) [0, 1, 2].forEach((k, ki) => { const idx = g3.map((v, i) => (v === k ? i : -1)).filter((i) => i >= 0); L.push(sline(idx, strata[ki])); });
    }
    return L;
  });
  const fkMsg = $derived(step === 0
    ? T(`Hồi quy Y theo X (bỏ qua Z): hệ số = ${fmt(naive, 2)}, trong khi hiệu ứng thật β = ${beta}. Độ lệch lý thuyết δγ/(γ²+1) = ${fmt(forkBias(gamma, delta), 2)} ⇒ ${fmt(beta + forkBias(gamma, delta), 2)}.`, `Regressing Y on X (ignoring Z): slope = ${fmt(naive, 2)} while the true effect is β = ${beta}. Theoretical bias δγ/(γ²+1) = ${fmt(forkBias(gamma, delta), 2)} ⇒ ${fmt(beta + forkBias(gamma, delta), 2)}.`)
    : step === 1 ? T(`Tô màu theo Z (3 tầng) và vẽ đường trong từng tầng: dốc ≈ ${strata.map((v) => fmt(v, 2)).join(' / ')} — nghịch lý Simpson: dấu có thể đảo. Tầng thô vẫn còn lệch dư vì Z biến thiên trong tầng.`, `Colour by Z (3 strata) and fit within each: slopes ≈ ${strata.map((v) => fmt(v, 2)).join(' / ')} — Simpson's paradox: the sign can flip. Coarse strata still leave residual bias because Z varies within a stratum.`)
    : T(`Hồi quy Y ~ X + Z (đóng backdoor X ← Z → Y): hệ số của X = ${fmt(adj, 2)}, gần β thật = ${beta}.`, `Regression Y ~ X + Z (closing the backdoor X ← Z → Y): coefficient of X = ${fmt(adj, 2)}, close to the true β = ${beta}.`));
  // ---- collider
  const cd = $derived(simCollider({ n: 500, se, seed }));
  const cdBig = $derived(simCollider({ n: 20000, se, seed: 78 }));
  const c3 = $derived(tertiles(cd.c));
  const cdLayers = $derived.by(() => {
    const L = [];
    if (step === 0) L.push({ type: 'points', pts: cd.x.map((x, i) => [x, cd.y[i]]), color: '#64748b', r: 2.4, opacity: 0.6 });
    else for (let k = 0; k < 3; k++) L.push({ type: 'points', pts: cd.x.map((x, i) => (c3[i] === k ? [x, cd.y[i]] : null)).filter(Boolean), color: COL[k], r: 2.4, opacity: step === 2 && k !== 2 ? 0.12 : 0.6 });
    if (step === 2) { const idx = c3.map((v, i) => (v === 2 ? i : -1)).filter((i) => i >= 0), b = slope(idx.map((i) => cd.x[i]), idx.map((i) => cd.y[i])), mx = idx.reduce((s, i) => s + cd.x[i], 0) / idx.length, my = idx.reduce((s, i) => s + cd.y[i], 0) / idx.length; L.push(line(my - b * mx, b, -3, 3, COL[2], 3)); }
    return L;
  });
  const cdMsg = $derived(step === 0 ? T(`X và Y độc lập: tương quan = ${fmt(corr(cdBig.x, cdBig.y), 3)}.`, `X and Y are independent: correlation = ${fmt(corr(cdBig.x, cdBig.y), 3)}.`)
    : step === 1 ? T('Tô màu theo C = X + Y + nhiễu (collider). Mỗi màu là một mức C — "điều kiện theo C" nghĩa là chỉ nhìn một màu.', 'Colour by C = X + Y + noise (the collider). Each colour is one level of C — "conditioning on C" means looking at one colour only.')
    : T(`Chỉ giữ nhóm C cao (đỏ): X và Y trở nên tương quan âm. Tương quan riêng phần khi điều kiện theo C = ${fmt(partialCorr(cdBig.x, cdBig.y, cdBig.c), 3)} (công thức −1/(1+σₑ²) = ${fmt(colliderPartialCorr(se), 3)}).`, `Keeping only high C (red): X and Y become negatively correlated. Partial correlation given C = ${fmt(partialCorr(cdBig.x, cdBig.y, cdBig.c), 3)} (formula −1/(1+σₑ²) = ${fmt(colliderPartialCorr(se), 3)}).`));
  // ---- interaction
  const it = $derived(simInteraction({ n: 160, b0: 1, b1: 0.4, b2: 0.4, b3, sigma: 0.6, seed }));
  const fit = $derived(fitInteraction(it.x, it.g, it.y));
  const itLayers = $derived.by(() => {
    const L = [0, 1].map((g) => ({ type: 'points', pts: it.x.map((x, i) => (it.g[i] === g ? [x, it.y[i]] : null)).filter(Boolean), color: g ? '#dc2626' : '#2563eb', r: 2.8, opacity: 0.7 }));
    if (step === 0) L.push(line(fit.pooled.beta[0], fit.pooled.beta[1], -2, 2, '#0f172a', 3));
    else if (step === 1) { const [a, b, c] = fit.additive.beta; L.push(line(a, b, -2, 2, '#2563eb', 3), line(a + c, b, -2, 2, '#dc2626', 3)); }
    else { const [a, b, c, d] = fit.inter.beta; L.push(line(a, b, -2, 2, '#2563eb', 3), line(a + c, b + d, -2, 2, '#dc2626', 3)); }
    return L;
  });
  const rss = $derived([fit.pooled.rss, fit.additive.rss, fit.inter.rss]);
  const itMsg = $derived([
    T(`Một đường chung cho cả hai nhóm: RSS = ${fmt(rss[0], 1)}.`, `One common line for both groups: RSS = ${fmt(rss[0], 1)}.`),
    T(`Mô hình cộng: hai đường song song (cùng dốc b₁ = ${fmt(fit.additive.beta[1], 2)}), RSS = ${fmt(rss[1], 1)}.`, `Additive model: two parallel lines (shared slope b₁ = ${fmt(fit.additive.beta[1], 2)}), RSS = ${fmt(rss[1], 1)}.`),
    T(`Có tương tác: dốc nhóm xanh = ${fmt(fit.inter.beta[1], 2)}, nhóm đỏ = ${fmt(fit.inter.beta[1] + fit.inter.beta[3], 2)} (chênh = b₃ = ${fmt(fit.inter.beta[3], 2)}). RSS = ${fmt(rss[2], 1)}.`, `With interaction: slope of blue = ${fmt(fit.inter.beta[1], 2)}, red = ${fmt(fit.inter.beta[1] + fit.inter.beta[3], 2)} (difference = b₃ = ${fmt(fit.inter.beta[3], 2)}). RSS = ${fmt(rss[2], 1)}.`)
  ][Math.min(step, 2)]);
</script>

<div class="dx">
  <h4>{T('Confounding, collider và interaction bằng mô phỏng', 'Confounding, colliders and interaction by simulation')}</h4>
  <div class="dx-tabs">
    <button class={tab === 'fork' ? 'on' : 'sec'} onclick={() => (tab = 'fork')}>{T('Confounder (fork)', 'Confounder (fork)')}</button>
    <button class={tab === 'collider' ? 'on' : 'sec'} onclick={() => (tab = 'collider')}>Collider</button>
    <button class={tab === 'interaction' ? 'on' : 'sec'} onclick={() => (tab = 'interaction')}>Interaction</button>
  </div>
  {#if tab === 'fork'}
    <p class="dx-help">{T('DAG: Z → X, Z → Y, X → Y. Z là nguyên nhân chung nên mở "backdoor" X ← Z → Y. Kéo γ (Z → X), δ (Z → Y) và β (hiệu ứng thật của X) rồi bấm Bước tiếp: ước lượng ngây thơ → phân tầng theo Z → hiệu chỉnh Z.', 'DAG: Z → X, Z → Y, X → Y. Z is a common cause, opening the backdoor X ← Z → Y. Drag γ (Z → X), δ (Z → Y) and β (true effect of X), then press Next: naive estimate → stratify by Z → adjust for Z.')}</p>
    <div class="dx-bar" style="gap:14px">
      <label>γ <b>{gamma}</b> <input type="range" min="0" max="3" step="0.1" bind:value={gamma} /></label>
      <label>δ <b>{delta}</b> <input type="range" min="-3" max="3" step="0.1" bind:value={delta} /></label>
      <label>β <b>{beta}</b> <input type="range" min="-2" max="2" step="0.1" bind:value={beta} /></label>
      <button class="sec" onclick={() => (seed += 1)}>🎲</button>
    </div>
    <Stepper bind:step total={3} {lang} />
    <Plot layers={fkLayers} xmin={-5} xmax={5} ymin={-8} ymax={8} xlabel="X" ylabel="Y" label="fork" height={250} />
    <div class="dx-msg">{fkMsg}</div>
  {:else if tab === 'collider'}
    <p class="dx-help">{T('DAG: X → C ← Y, X và Y độc lập. Điều chỉnh (lọc, kiểm soát) theo collider C tạo ra liên hệ giả giữa X và Y — "control cho mọi thứ" có thể gây hại.', 'DAG: X → C ← Y with X and Y independent. Adjusting for (filtering on, controlling for) the collider C creates a spurious link between X and Y — "controlling for everything" can hurt.')}</p>
    <div class="dx-bar" style="gap:14px"><label>σₑ <b>{se}</b> <input type="range" min="0.1" max="2" step="0.1" bind:value={se} /></label><button class="sec" onclick={() => (seed += 1)}>🎲</button></div>
    <Stepper bind:step total={3} {lang} />
    <Plot layers={cdLayers} xmin={-3.5} xmax={3.5} ymin={-3.5} ymax={3.5} xlabel="X" ylabel="Y" label="collider" height={250} />
    <div class="dx-msg">{cdMsg}</div>
  {:else}
    <p class="dx-help">{T('Hiệu ứng của x phụ thuộc nhóm g? Kéo b₃ (độ tương tác) và bấm Bước tiếp: một đường chung → hai đường song song (cộng) → hai đường khác dốc (tương tác). RSS giảm mạnh khi b₃ lớn.', 'Does the effect of x depend on group g? Drag b₃ (interaction strength) and press Next: one common line → two parallel lines (additive) → two lines with different slopes (interaction). RSS drops sharply when b₃ is large.')}</p>
    <div class="dx-bar" style="gap:14px"><label>b₃ <b>{b3}</b> <input type="range" min="-2" max="2" step="0.1" bind:value={b3} /></label><button class="sec" onclick={() => (seed += 1)}>🎲</button></div>
    <Stepper bind:step total={3} {lang} />
    <Plot layers={itLayers} xmin={-2} xmax={2} ymin={-5} ymax={6} xlabel="x" ylabel="y" label="interaction" height={250} />
    <div class="dx-msg">{itMsg}</div>
  {/if}
</div>
