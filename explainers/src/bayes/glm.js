// Hồi quy logistic và Poisson Bayes một biến bằng posterior trên lưới 2-D (a, b), prior N(0, τ²).
import { mulberry32, randn, lgamma } from './stats.js';

export const sigmoid = (z) => 1 / (1 + Math.exp(-z));
export const RANGE = { logistic: { a: [-4, 4], b: [-2, 6], truth: [-0.5, 1.5] }, poisson: { a: [-1, 2.5], b: [-1, 2], truth: [0.8, 0.6] } };
export function simulate(kind, n, a = RANGE[kind].truth[0], b = RANGE[kind].truth[1], seed = 1) {
  const r = mulberry32(seed), xs = Array.from({ length: n }, () => -2 + 4 * r());
  const ys = xs.map((x) => {
    const eta = a + b * x;
    if (kind === 'logistic') return r() < sigmoid(eta) ? 1 : 0;
    const L = Math.exp(-Math.exp(eta)); let k = 0, p = 1; do { k++; p *= r(); } while (p > L); return k - 1;
  });
  return { xs, ys };
}
const softplus = (z) => (z > 30 ? z : Math.log1p(Math.exp(z)));
export function logLik(kind, xs, ys, a, b) {
  let s = 0;
  for (let i = 0; i < xs.length; i++) { const eta = a + b * xs[i]; s += kind === 'logistic' ? ys[i] * eta - softplus(eta) : ys[i] * eta - Math.exp(eta) - lgamma(ys[i] + 1); }
  return s;
}
export function gridPosterior(kind, xs, ys, tau, G = 81, range = RANGE[kind]) {
  const as = Array.from({ length: G }, (_, i) => range.a[0] + (range.a[1] - range.a[0]) * i / (G - 1));
  const bs = Array.from({ length: G }, (_, i) => range.b[0] + (range.b[1] - range.b[0]) * i / (G - 1));
  const lp = new Float64Array(G * G); let mx = -Infinity;
  for (let i = 0; i < G; i++) for (let j = 0; j < G; j++) { const v = logLik(kind, xs, ys, as[i], bs[j]) - (as[i] ** 2 + bs[j] ** 2) / (2 * tau * tau); lp[i * G + j] = v; if (v > mx) mx = v; }
  let Z = 0; const P = new Float64Array(G * G);
  for (let k = 0; k < G * G; k++) { P[k] = Math.exp(lp[k] - mx); Z += P[k]; }
  for (let k = 0; k < G * G; k++) P[k] /= Z;
  let ma = 0, mb = 0; const pa = new Float64Array(G), pb = new Float64Array(G);
  for (let i = 0; i < G; i++) for (let j = 0; j < G; j++) { const q = P[i * G + j]; ma += q * as[i]; mb += q * bs[j]; pa[i] += q; pb[j] += q; }
  return { kind, as, bs, G, P, meanA: ma, meanB: mb, pa, pb, da: as[1] - as[0], db: bs[1] - bs[0] };
}
/** Lấy K mẫu (a, b) từ lưới (chọn ô theo xác suất rồi rung ngẫu nhiên trong ô). */
export function drawGrid(post, K, seed = 1) {
  const r = mulberry32(seed), { G, P, as, bs, da, db } = post, cum = new Float64Array(G * G); let s = 0;
  for (let k = 0; k < G * G; k++) { s += P[k]; cum[k] = s; }
  return Array.from({ length: K }, () => {
    const u = r() * s; let lo = 0, hi = G * G - 1; while (lo < hi) { const mid = (lo + hi) >> 1; if (cum[mid] < u) lo = mid + 1; else hi = mid; }
    return { a: as[Math.floor(lo / G)] + (r() - 0.5) * da, b: bs[lo % G] + (r() - 0.5) * db };
  });
}
/** Hợp lý cực đại bằng IRLS/Newton (kiểm tra chéo cho posterior phẳng). */
export function mle(kind, xs, ys, iters = 50) {
  let a = 0, b = 0;
  for (let t = 0; t < iters; t++) {
    let g0 = 0, g1 = 0, h00 = 0, h01 = 0, h11 = 0;
    xs.forEach((x, i) => { const eta = a + b * x, mu = kind === 'logistic' ? sigmoid(eta) : Math.exp(eta), w = kind === 'logistic' ? mu * (1 - mu) : mu, r = ys[i] - mu; g0 += r; g1 += r * x; h00 += w; h01 += w * x; h11 += w * x * x; });
    const det = h00 * h11 - h01 * h01, da = (h11 * g0 - h01 * g1) / det, db = (-h01 * g0 + h00 * g1) / det;
    a += da; b += db; if (Math.abs(da) + Math.abs(db) < 1e-12) break;
  }
  return { a, b };
}
export const meanFn = (kind, a, b, x) => (kind === 'logistic' ? sigmoid(a + b * x) : Math.exp(a + b * x));
