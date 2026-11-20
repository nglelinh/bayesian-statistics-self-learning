// Posterior predictive check cho GLM: logistic (hiệu chuẩn theo nhóm) và Poisson (số 0 dư).
import { mulberry32, poissonSample } from './stats.js';
import { sigmoid, gridPosterior, drawGrid } from './glm.js';

export function genLogistic(n, { a = -0.3, b = 1.2, c = 0 } = {}, seed = 1) {
  const r = mulberry32(seed), xs = Array.from({ length: n }, () => -2 + 4 * r());
  return { xs, ys: xs.map((x) => (r() < sigmoid(a + b * x + c * x * x) ? 1 : 0)) };
}
export function genZeroInflated(n, { a = 0.9, b = 0.4, pi = 0 } = {}, seed = 1) {
  const r = mulberry32(seed), xs = Array.from({ length: n }, () => -2 + 4 * r());
  return { xs, ys: xs.map((x) => (r() < pi ? 0 : poissonSample(r, Math.exp(a + b * x)))) };
}
const binIndex = (x, B) => Math.min(B - 1, Math.max(0, Math.floor(((x + 2) / 4) * B)));
function binned(xs, ys, B) { const n = new Array(B).fill(0), s = new Array(B).fill(0); xs.forEach((x, i) => { const k = binIndex(x, B); n[k]++; s[k] += ys[i]; }); return { n, s }; }
/** Logistic PPC: thống kê χ² theo nhóm T(y; θ) = Σ (s_k − n_k p̄_k)² / (n_k p̄_k (1 − p̄_k)), tính cho dữ liệu thật và cho bản sao dưới cùng θ. */
export function logisticPPC(xs, ys, post, R = 300, seed = 1, B = 8) {
  const g = mulberry32(seed), draws = drawGrid(post, R, seed + 1), obsB = binned(xs, ys, B), centers = Array.from({ length: B }, (_, k) => -2 + ((k + 0.5) * 4) / B);
  const reps = [], Tobs = [], Trep = [], repRates = Array.from({ length: B }, () => []);
  for (const d of draws) {
    const p = xs.map((x) => sigmoid(d.a + d.b * x)), pbar = new Array(B).fill(0);
    xs.forEach((x, i) => { pbar[binIndex(x, B)] += p[i]; });
    const yrep = p.map((q) => (g() < q ? 1 : 0)), rb = binned(xs, yrep, B);
    let to = 0, tr = 0;
    for (let k = 0; k < B; k++) { if (!obsB.n[k]) continue; const pb = pbar[k] / obsB.n[k], den = obsB.n[k] * pb * (1 - pb) || 1e-9; to += (obsB.s[k] - obsB.n[k] * pb) ** 2 / den; tr += (rb.s[k] - obsB.n[k] * pb) ** 2 / den; repRates[k].push(rb.s[k] / obsB.n[k]); }
    Tobs.push(to); Trep.push(tr); reps.push(rb);
  }
  const q = (a, p) => { const s = [...a].sort((x, y) => x - y); return s[Math.floor(p * (s.length - 1))]; };
  const bins = centers.map((x, k) => ({ x, n: obsB.n[k], obs: obsB.n[k] ? obsB.s[k] / obsB.n[k] : null, lo: q(repRates[k], 0.05), hi: q(repRates[k], 0.95), mean: repRates[k].reduce((a, b) => a + b, 0) / repRates[k].length }));
  return { bins, Tobs, Trep, ppp: Trep.filter((t, i) => t >= Tobs[i]).length / R, repLines: reps.slice(0, 12).map((rb) => rb.s.map((s, k) => [centers[k], obsB.n[k] ? s / obsB.n[k] : null])) };
}
/** Poisson PPC bằng thống kê tỉ lệ số 0 (và pmf của các bản sao). */
export function poissonZerosPPC(xs, ys, post, R = 400, seed = 1, K = 12) {
  const g = mulberry32(seed), draws = drawGrid(post, R, seed + 1), zObs = ys.filter((v) => v === 0).length / ys.length, zRep = [], pmf = Array.from({ length: K + 1 }, () => []);
  for (const d of draws) { const rep = xs.map((x) => poissonSample(g, Math.exp(d.a + d.b * x))); zRep.push(rep.filter((v) => v === 0).length / rep.length); for (let k = 0; k <= K; k++) pmf[k].push(rep.filter((v) => v === k).length / rep.length); }
  const q = (a, p) => { const s = [...a].sort((x, y) => x - y); return s[Math.floor(p * (s.length - 1))]; };
  const obsPmf = Array.from({ length: K + 1 }, (_, k) => ys.filter((v) => v === k).length / ys.length);
  return { zObs, zRep, ppp: zRep.filter((z) => z >= zObs).length / R, obsPmf, band: pmf.map((a) => ({ lo: q(a, 0.05), hi: q(a, 0.95), mean: a.reduce((x, y) => x + y, 0) / a.length })) };
}
export { gridPosterior };
