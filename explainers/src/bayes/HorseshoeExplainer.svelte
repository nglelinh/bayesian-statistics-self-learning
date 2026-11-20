<script>
  import Stepper from '../shared/Stepper.svelte';
  import Plot from '../shared/Plot.svelte';
  import { tr, norm, fmt } from '../shared/i18n.js';
  import { PRIORS, sparseData, mse } from './horseshoe.js';

  let { lang: langProp = 'vi' } = $props();
  const lang = norm(langProp), T = (v, e) => tr(lang, v, e);
  const METHODS = ['mle', 'gaussian', 'laplace', 'horseshoe'], COLORS = { mle: '#64748b', gaussian: '#2563eb', laplace: '#d97706', horseshoe: '#16a34a' };
  const SC = [0.05, 0.1, 0.2, 0.4, 0.7, 1, 2];
  let step = $state(0), si = $state(2), seed = $state(3);
  const P = 50, K = 5;
  const data = $derived(sparseData({ p: P, k: K, big: 6, seed }));
  const sc = $derived(SC[si]);
  const method = $derived(METHODS[Math.min(step, 3)]);
  const est = $derived(Object.fromEntries(METHODS.map((m) => [m, data.y.map((y) => PRIORS[m](y, sc))])));
  const err = $derived(Object.fromEntries(METHODS.map((m) => [m, mse(est[m], data.beta)])));
  const ys = Array.from({ length: 65 }, (_, i) => -8 + i * 0.25);
  const curves = $derived(Object.fromEntries(METHODS.slice(1).map((m) => [m, ys.map((y) => [y, PRIORS[m](y, sc)])])));
  const idx = Array.from({ length: P }, (_, j) => j + 1);
  const dotLayers = $derived([
    { type: 'hline', y: 0, color: '#cbd5e1' },
    ...idx.map((j) => ({ type: 'seg', x1: j, x2: j, y1: data.y[j - 1], y2: est[method][j - 1], color: '#cbd5e1', width: 1 })),
    { type: 'points', pts: idx.map((j) => [j, data.y[j - 1]]), color: '#94a3b8', r: 2.8 },
    { type: 'points', pts: idx.map((j) => [j, data.beta[j - 1]]), color: '#dc2626', hollow: true, r: 3.6 },
    { type: 'points', pts: idx.map((j) => [j, est[method][j - 1]]), color: COLORS[method], r: 3.4 }
  ]);
  const curveLayers = $derived([
    { type: 'line', pts: [[-8, -8], [8, 8]], color: '#cbd5e1', width: 1.2, dash: '4 3' },
    ...METHODS.slice(1).filter((m) => m !== method).map((m) => ({ type: 'line', pts: curves[m], color: COLORS[m], width: 1.4, opacity: 0.35 })),
    ...(method === 'mle' ? [] : [{ type: 'line', pts: curves[method], color: COLORS[method], width: 3 }])
  ]);
  const NAME = $derived({ mle: T('Không co rút (ước lượng thô y)', 'No shrinkage (raw y)'), gaussian: T('Prior Gaussian = ridge', 'Gaussian prior = ridge'), laplace: T('Prior Laplace = Bayesian lasso', 'Laplace prior = Bayesian lasso'), horseshoe: 'Horseshoe' });
  const zeroErr = $derived(est[method].slice(K).reduce((a, e) => a + e * e, 0) / (P - K)), sigErr = $derived(est[method].slice(0, K).reduce((a, e, j) => a + (e - data.beta[j]) ** 2, 0) / K);
</script>

<div class="dx">
  <h4>{T('Prior co rút cho nhiều biến: Gaussian, Laplace và Horseshoe', 'Shrinkage priors for many predictors: Gaussian, Laplace and horseshoe')}</h4>
  <p class="dx-help">{T('50 hệ số, chỉ 5 cái thật sự lớn (±6, vòng đỏ), còn lại bằng 0; ta chỉ thấy y = β + nhiễu (chấm xám). Mỗi bước đổi prior và vẽ posterior mean (chấm màu). Gaussian co mọi thứ như nhau nên hoặc không dọn được nhiễu hoặc làm hỏng tín hiệu; Laplace co đều; Horseshoe co mạnh các giá trị nhỏ nhưng gần như không đụng giá trị lớn. Đường cong dưới: posterior mean theo y (nét đứt chéo = không co).', '50 coefficients, only 5 truly large (±6, red rings), the rest zero; we only see y = β + noise (grey dots). Each step switches the prior and draws the posterior mean (coloured dots). The Gaussian shrinks everything alike so it either leaves noise or damages signals; the Laplace shrinks evenly; the horseshoe shrinks small values hard yet barely touches large ones. Curve below: posterior mean as a function of y (dashed diagonal = no shrinkage).')}</p>
  <div class="dx-bar" style="gap:14px">
    <label>{T('Thang đo prior', 'Prior scale')} <b>{sc}</b> <input type="range" min="0" max={SC.length - 1} bind:value={si} /></label>
    <button class="sec" onclick={() => (seed += 1)}>🎲 {T('Dữ liệu mới', 'New data')}</button>
  </div>
  <Stepper bind:step total={4} {lang} />
  <Plot layers={dotLayers} xmin={0} xmax={P + 1} ymin={-9} ymax={9} xticks={10} xlabel={T('chỉ số hệ số', 'coefficient index')} ylabel="β" label="estimates" height={230} />
  <div class="dx-msg"><b style={'color:' + COLORS[method]}>{NAME[method]}</b> · MSE = <b>{fmt(err[method], 3)}</b> ({T('thô', 'raw')} {fmt(err.mle, 3)}) · {T('sai số trên 45 hệ số 0', 'error on the 45 zero coefficients')} = {fmt(zeroErr, 3)} · {T('trên 5 tín hiệu', 'on the 5 signals')} = {fmt(sigErr, 3)}</div>
  <Plot layers={curveLayers} xmin={-8} xmax={8} ymin={-8} ymax={8} xticks={8} xlabel="y" ylabel="E[β | y]" label="shrinkage curve" height={200} />
  <p class="dx-k">{T('Xanh dương = Gaussian, cam = Laplace, xanh lá = Horseshoe. Thử tăng/giảm thang đo prior: Gaussian không có thang đo nào vừa cho sạch nhiễu vừa giữ tín hiệu; Horseshoe thì có.', 'Blue = Gaussian, orange = Laplace, green = horseshoe. Try raising/lowering the scale: no Gaussian scale both cleans the noise and keeps the signals; the horseshoe can.')}</p>
</div>
