<script>
  import Stepper from '../shared/Stepper.svelte';
  import Plot from '../shared/Plot.svelte';
  import { tr, norm, fmt } from '../shared/i18n.js';
  import { SCHOOLS, EQUAL, conditional, tauPosterior, thetaSummary, tauMedian } from './pool.js';

  let { lang: langProp = 'vi', data: dataProp = 'schools' } = $props();
  const lang = norm(langProp), T = (v, e) => tr(lang, v, e);
  const TAUS = [0, 2, 4, 8, 16, 32, 100];
  let ds = $state(dataProp === 'equal' ? 'equal' : 'schools'), step = $state(0);
  $effect(() => { ds; step = 0; });
  const D = $derived(ds === 'equal' ? EQUAL : SCHOOLS), J = 8;
  const post = $derived(tauPosterior(D.y, D.s, 60, 601));
  const sum = $derived(thetaSummary(D.y, D.s, post));
  const last = TAUS.length; // bước cuối = lấy trung bình theo p(τ | y)
  const atData = $derived(step >= last);
  const tau = $derived(TAUS[Math.min(step, last - 1)]);
  const cond = $derived(conditional(D.y, D.s, Math.max(tau, 1e-6)));
  const est = $derived(atData ? sum.map((t) => ({ mean: t.mean, sd: t.sd })) : cond.theta.map((t) => ({ mean: t.mean, sd: Math.sqrt(t.v) })));
  const muShow = $derived(atData ? conditional(D.y, D.s, tauMedian(post)).muHat : cond.muHat);
  const lo = $derived(Math.min(...D.y.map((v, j) => v - D.s[j])) - 4), hi = $derived(Math.max(...D.y.map((v, j) => v + D.s[j])) + 4);
  const layers = $derived([
    { type: 'vline', x: muShow, color: '#16a34a', dash: '5 3', label: 'μ̂' },
    ...D.y.map((v, j) => ({ type: 'seg', x1: v - D.s[j], x2: v + D.s[j], y1: j + 1 + 0.18, y2: j + 1 + 0.18, color: '#94a3b8', width: 2 })),
    { type: 'points', pts: D.y.map((v, j) => [v, j + 1 + 0.18]), color: '#64748b', hollow: true, r: 4.5 },
    ...est.map((e, j) => ({ type: 'seg', x1: e.mean - e.sd, x2: e.mean + e.sd, y1: j + 1 - 0.18, y2: j + 1 - 0.18, color: '#93c5fd', width: 3 })),
    { type: 'points', pts: est.map((e, j) => [e.mean, j + 1 - 0.18]), color: '#1d4ed8', r: 4.5 },
    ...D.y.map((v, j) => ({ type: 'seg', x1: v, x2: est[j].mean, y1: j + 1 + 0.18, y2: j + 1 - 0.18, color: '#f59e0b', width: 1, dash: '2 2' })),
    ...D.names.map((nm, j) => ({ type: 'text', x: lo + 0.5, y: j + 1 + 0.35, text: nm, color: '#334155' }))
  ]);
  const tauPts = $derived(post.taus.map((t, i) => [t, post.p[i] / post.dt]));
  const tauLayers = $derived([{ type: 'area', pts: tauPts, color: '#7c3aed', opacity: 0.25 }, { type: 'line', pts: tauPts, color: '#6d28d9', width: 2 }, ...(atData ? [{ type: 'vline', x: tauMedian(post), color: '#16a34a', label: T('trung vị', 'median') }] : [{ type: 'vline', x: Math.min(tau, 60), color: '#dc2626', label: 'τ' }])]);
  const msg = $derived(atData
    ? T(`Dùng toàn bộ p(τ | y) (trung vị τ ≈ ${fmt(tauMedian(post), 1)}): mỗi nhóm co một lượng vừa phải — nhóm có σ_j lớn co mạnh hơn.`, `Averaging over p(τ | y) (median τ ≈ ${fmt(tauMedian(post), 1)}): each group shrinks a moderate amount — groups with large σ_j shrink more.`)
    : tau === 0 ? T('τ = 0: gộp hoàn toàn — mọi nhóm có cùng một ước lượng (trung bình có trọng số).', 'τ = 0: complete pooling — every group gets the same estimate (the weighted mean).')
    : tau >= 100 ? T('τ rất lớn: không gộp — ước lượng của mỗi nhóm gần như bằng dữ liệu thô.', 'τ very large: no pooling — each group estimate is almost its raw data.')
    : T(`τ = ${tau}: gộp một phần. Hệ số co B_j = σ_j²/(σ_j² + τ²) càng lớn thì nhóm càng bị kéo về μ̂.`, `τ = ${tau}: partial pooling. The shrinkage factor B_j = σ_j²/(σ_j² + τ²) is larger the more a group is pulled toward μ̂.`));
</script>

<div class="dx">
  <h4>{T('Mô hình phân cấp: partial pooling và shrinkage', 'Hierarchical model: partial pooling and shrinkage')}</h4>
  <p class="dx-help">{T('Tám nhóm, mỗi nhóm có ước lượng thô y_j (vòng rỗng, ± σ_j) và θ_j ~ N(μ, τ²). Chấm xanh đậm = ước lượng posterior của θ_j. τ là "độ giống nhau giữa các nhóm": bấm Bước tiếp để tăng τ từ gộp hoàn toàn đến không gộp; bước cuối dùng toàn bộ phân phối posterior của τ.', 'Eight groups, each with a raw estimate y_j (hollow, ± σ_j) and θ_j ~ N(μ, τ²). Dark blue = posterior estimate of θ_j. τ is "how alike the groups are": press Next to raise τ from complete pooling to no pooling; the last step uses the whole posterior of τ.')}</p>
  <div class="dx-bar">
    <label>{T('Dữ liệu', 'Data')} <select bind:value={ds}><option value="schools">{T('8 trường (Rubin)', 'Eight schools (Rubin)')}</option><option value="equal">{T('8 nhóm cùng độ chính xác', '8 equally precise groups')}</option></select></label>
  </div>
  <Stepper bind:step total={last + 1} {lang} />
  <Plot {layers} xmin={lo} xmax={hi} ymin={0.4} ymax={J + 0.8} xticks={7} yticks={J} grid={false} xlabel={T('hiệu ứng', 'effect')} ylabel={T('nhóm', 'group')} label="shrinkage" height={300} />
  <div class="dx-msg">{msg}</div>
  <div style="overflow-x:auto"><table class="dx-t"><thead><tr><th></th>{#each D.names as nm}<th>{nm}</th>{/each}</tr></thead><tbody>
    <tr><td>y</td>{#each D.y as v}<td>{v}</td>{/each}</tr>
    <tr><td>σ</td>{#each D.s as v}<td>{v}</td>{/each}</tr>
    <tr><td>θ̂</td>{#each est as e}<td><b>{fmt(e.mean, 1)}</b></td>{/each}</tr>
    {#if !atData}<tr><td>B</td>{#each cond.theta as t}<td>{fmt(t.B, 2)}</td>{/each}</tr>{/if}</tbody></table></div>
  <Plot layers={tauLayers} xmin={0} xmax={40} ymin={0} xlabel="τ" ylabel={T('p(τ | y)', 'p(τ | y)')} label="tau posterior" height={150} />
  <p class="dx-k">{T('Posterior của τ có đuôi phải dài: dữ liệu không loại trừ được τ lớn, nhưng cũng không ủng hộ "không gộp".', 'The posterior of τ has a long right tail: the data cannot rule out large τ, yet they do not favour "no pooling" either.')}</p>
</div>
