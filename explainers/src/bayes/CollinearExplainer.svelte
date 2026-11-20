<script>
  import Stepper from '../shared/Stepper.svelte';
  import Plot from '../shared/Plot.svelte';
  import { tr, norm, fmt } from '../shared/i18n.js';
  import { simData, posterior, sampleBeta, vif } from './collinear.js';

  let { lang: langProp = 'vi' } = $props();
  const lang = norm(langProp), T = (v, e) => tr(lang, v, e);
  const RHO = [0, 0.5, 0.8, 0.9, 0.95, 0.99], n = 60, sigma = 1;
  let step = $state(0), seed = $state(4), tau = $state(10);
  $effect(() => { seed; });
  const all = $derived(RHO.map((rho) => { const d = simData({ n, rho, seed }); return { rho, d, post: posterior(d.x1, d.x2, d.y, sigma, tau) }; }));
  const k = $derived(Math.min(step, RHO.length - 1));
  const cur = $derived(all[k]);
  const draws = $derived(sampleBeta(cur.post, 300, 2));
  const dataLayers = $derived([{ type: 'points', pts: cur.d.x1.map((a, i) => [a, cur.d.x2[i]]), color: '#2563eb', r: 2.6, opacity: 0.7 }]);
  const postLayers = $derived([
    { type: 'hline', y: 1, color: '#cbd5e1', dash: '3 3' }, { type: 'vline', x: 1, color: '#cbd5e1', dash: '3 3' },
    { type: 'points', pts: draws, color: '#3b82f6', r: 2.2, opacity: 0.4 }, { type: 'points', pts: [[1, 1]], color: '#dc2626', r: 5 },
    { type: 'points', pts: [cur.post.mean], color: '#0f172a', r: 4.5 }
  ]);
  const sdLayers = $derived([
    { type: 'line', pts: all.map((a, i) => [i, a.post.sd1]), color: '#dc2626', width: 2, opacity: 0.35 },
    { type: 'line', pts: all.map((a, i) => [i, a.post.sdSum]), color: '#16a34a', width: 2, opacity: 0.35 },
    { type: 'line', pts: all.slice(0, k + 1).map((a, i) => [i, a.post.sd1]), color: '#dc2626', width: 2.6 },
    { type: 'line', pts: all.slice(0, k + 1).map((a, i) => [i, a.post.sdSum]), color: '#16a34a', width: 2.6 },
    { type: 'points', pts: [[k, cur.post.sd1], [k, cur.post.sdSum]], color: '#0f172a', r: 4.5 }
  ]);
  const sdTop = $derived(Math.max(...all.map((a) => a.post.sd1)) * 1.1);
</script>

<div class="dx">
  <h4>{T('Đa cộng tuyến: posterior kéo thành dải chéo', 'Multicollinearity: the posterior stretches into a diagonal ridge')}</h4>
  <p class="dx-help">{T('y = b₁·x₁ + b₂·x₂ + ε với b₁ = b₂ = 1 (chấm đỏ), σ = 1, n = 60. Mỗi bước tăng tương quan ρ giữa x₁ và x₂. Posterior Gaussian có dạng đóng: sd(b₁) tăng theo √VIF, b₁ và b₂ tương quan âm ≈ −ρ (dải chéo), nhưng tổng b₁ + b₂ vẫn được xác định tốt — mô hình dự đoán ổn dù từng hệ số "lúng túng".', 'y = b₁·x₁ + b₂·x₂ + ε with b₁ = b₂ = 1 (red dot), σ = 1, n = 60. Each step raises the correlation ρ between x₁ and x₂. The Gaussian posterior has a closed form: sd(b₁) grows like √VIF, b₁ and b₂ become negatively correlated ≈ −ρ (the diagonal ridge), yet the sum b₁ + b₂ stays well determined — predictions are fine even if individual coefficients are unclear.')}</p>
  <div class="dx-bar" style="gap:14px">
    <label>{T('Prior τ', 'Prior τ')} <b>{tau}</b> <input type="range" min="0.5" max="20" step="0.5" bind:value={tau} /></label>
    <button class="sec" onclick={() => (seed += 1)}>🎲 {T('Dữ liệu mới', 'New data')}</button>
  </div>
  <Stepper bind:step total={RHO.length} {lang} />
  <div class="dx-grid2">
    <div><Plot layers={dataLayers} xmin={-3.5} xmax={3.5} ymin={-3.5} ymax={3.5} xlabel="x₁" ylabel="x₂" label="predictors" height={210} /></div>
    <div><Plot layers={postLayers} xmin={-3} xmax={5} ymin={-3} ymax={5} xlabel="b₁" ylabel="b₂" label="posterior draws" height={210} /></div>
  </div>
  <div class="dx-msg">ρ = <b>{cur.rho}</b> · VIF = {fmt(vif(cur.rho), 1)} · sd(b₁) = <b>{fmt(cur.post.sd1, 2)}</b> · corr(b₁, b₂) = <b>{fmt(cur.post.corr, 2)}</b> · sd(b₁ + b₂) = <b>{fmt(cur.post.sdSum, 2)}</b> · {T('trung bình posterior', 'posterior mean')} b₁ = {fmt(cur.post.mean[0], 2)}, b₂ = {fmt(cur.post.mean[1], 2)}.</div>
  <Plot layers={sdLayers} xmin={0} xmax={RHO.length - 1} ymin={0} ymax={sdTop} xticks={RHO.length - 1} xlabel={T('chỉ số bước (ρ = ' + RHO.join(', ') + ')', 'step index (ρ = ' + RHO.join(', ') + ')')} ylabel="sd" label="sd vs rho" height={170} />
  <p class="dx-k">{T('Đỏ = sd(b₁) tăng theo ρ; xanh lá = sd(b₁ + b₂) không tăng (thực ra giảm). Kéo τ nhỏ để thấy prior regularization co sd lại — đánh đổi bằng một chút thiên lệch.', 'Red = sd(b₁) grows with ρ; green = sd(b₁ + b₂) does not (it even shrinks). Drag τ down to see a regularising prior shrink the sd — at the price of some bias.')}</p>
</div>
