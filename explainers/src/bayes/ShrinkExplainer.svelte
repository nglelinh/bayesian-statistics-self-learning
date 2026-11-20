<script>
  import Stepper from '../shared/Stepper.svelte';
  import Plot from '../shared/Plot.svelte';
  import { tr, norm, fmt } from '../shared/i18n.js';
  import { fitRidge, sineData, mse, evalPoly, truth, samplePosterior } from './shrink.js';

  let { lang: langProp = 'vi', degree = 9 } = $props();
  const lang = norm(langProp), T = (v, e) => tr(lang, v, e);
  const TAUS = [100, 10, 3, 1, 0.5, 0.3, 0.1, 0.03, 0.01];
  let d = $state(Math.max(1, Math.min(12, Number(degree) || 9))), seed = $state(2), step = $state(0), nTrain = $state(12);
  const sigma = 0.3;
  $effect(() => { d; seed; nTrain; step = 0; });
  const tau = $derived(TAUS[Math.min(step, TAUS.length - 1)]);
  const tr_ = $derived(sineData(nTrain, sigma, seed));
  const te = sineData(300, sigma, 999);
  const fit = $derived(fitRidge(tr_.xs, tr_.ys, d, sigma, tau));
  const post = $derived(samplePosterior(fit, 14, 5));
  const gx = Array.from({ length: 101 }, (_, i) => -1 + 2 * i / 100);
  const clip = (v) => Math.max(-6, Math.min(6, v));
  const curve = (w) => gx.map((x) => [x, clip(evalPoly(w, x))]);
  const trainErr = $derived(mse(fit.w, tr_.xs, tr_.ys)), testErr = $derived(mse(fit.w, te.xs, te.ys));
  const path = $derived(TAUS.map((t, i) => { const f = fitRidge(tr_.xs, tr_.ys, d, sigma, t); return { i, t, tr: mse(f.w, tr_.xs, tr_.ys), te: mse(f.w, te.xs, te.ys) }; }));
  const layers = $derived([
    ...post.map((w) => ({ type: 'line', pts: curve(w), color: '#3b82f6', width: 1, opacity: 0.25 })),
    { type: 'line', pts: gx.map((x) => [x, truth(x)]), color: '#dc2626', width: 1.5, dash: '4 3' },
    { type: 'line', pts: curve(fit.w), color: '#1d4ed8', width: 2.6 },
    { type: 'points', pts: tr_.xs.map((x, i) => [x, tr_.ys[i]]), color: '#0f172a', r: 3.6 }
  ]);
  const eLayers = $derived([
    { type: 'line', pts: path.map((p) => [Math.log10(p.t), Math.min(p.tr, 1.5)]), color: '#94a3b8', width: 2 },
    { type: 'line', pts: path.map((p) => [Math.log10(p.t), Math.min(p.te, 1.5)]), color: '#dc2626', width: 2 },
    { type: 'points', pts: [[Math.log10(tau), Math.min(trainErr, 1.5)], [Math.log10(tau), Math.min(testErr, 1.5)]], color: '#0f172a', r: 5 }
  ]);
</script>

<div class="dx">
  <h4>{T('Prior chuẩn co hệ số: từ overfitting đến hồi quy ridge', 'A normal prior shrinks coefficients: from overfitting to ridge regression')}</h4>
  <p class="dx-help">{T('Đa thức bậc d khớp dữ liệu nhiễu quanh y = sin(πx). Prior hệ số N(0, τ²) cho posterior mean = nghiệm ridge với λ = σ²/τ². Bấm Bước tiếp để giảm τ (prior chặt hơn): đường cong mượt dần; bó xanh nhạt là các đường lấy từ posterior.', 'A degree-d polynomial fits noisy data around y = sin(πx). A N(0, τ²) prior on coefficients makes the posterior mean the ridge solution with λ = σ²/τ². Press Next to decrease τ (tighter prior): the curve smooths; the pale bundle is draws from the posterior.')}</p>
  <div class="dx-bar" style="gap:14px">
    <label>{T('Bậc đa thức', 'Degree')} <b>{d}</b> <input type="range" min="1" max="12" bind:value={d} /></label>
    <label>{T('Số điểm huấn luyện', 'Training points')} <b>{nTrain}</b> <input type="range" min="6" max="30" bind:value={nTrain} /></label>
    <button class="sec" onclick={() => (seed += 1)}>🎲 {T('Dữ liệu mới', 'New data')}</button>
  </div>
  <Stepper bind:step total={TAUS.length} {lang} />
  <Plot {layers} xmin={-1} xmax={1} ymin={-2} ymax={2} xlabel="x" ylabel="y" label="polynomial fit" height={260} />
  <div class="dx-msg">τ = <b>{tau}</b> (λ = {fmt(sigma ** 2 / tau ** 2, 3)}) · {T('sai số huấn luyện', 'train error')} = {fmt(trainErr, 3)} · <b>{T('sai số kiểm tra', 'test error')} = {fmt(testErr, 3)}</b> · {T('chuẩn hệ số', 'coefficient norm')} = {fmt(Math.hypot(...fit.w), 2)}</div>
  <Plot layers={eLayers} xmin={-2} xmax={2} ymin={0} ymax={1.5} xlabel={T('log₁₀ τ (trái = prior chặt, phải = prior lỏng)', 'log₁₀ τ (left = tight prior, right = loose prior)')} ylabel="MSE" label="error vs tau" height={180} />
  <p class="dx-k">{T('Xám = lỗi huấn luyện, đỏ = lỗi kiểm tra (300 điểm mới). Prior quá lỏng ⇒ overfit; quá chặt ⇒ underfit; ở giữa là prior tốt.', 'Grey = train error, red = test error (300 fresh points). Prior too loose ⇒ overfit; too tight ⇒ underfit; the sweet spot is in between.')}</p>
</div>
