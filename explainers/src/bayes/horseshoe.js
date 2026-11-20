// Co rút: posterior mean E[β | y] của mô hình y ~ N(β, s²) dưới prior Gaussian, Laplace và Horseshoe.
import { normalPdf, mulberry32, randn } from './stats.js';

export const gaussianMean = (y, tau, s = 1) => (y * tau * tau) / (tau * tau + s * s);
export const laplacePdf = (b, scale) => Math.exp(-Math.abs(b) / scale) / (2 * scale);
/** Posterior mean với prior bất kỳ trên β, tích phân số 1-D. */
export function numericMean(y, priorPdf, s = 1, lo = -40, hi = 40, N = 8001) {
  const h = (hi - lo) / (N - 1); let num = 0, den = 0;
  for (let i = 0; i < N; i++) { const b = lo + i * h, w = normalPdf(y, b, s) * priorPdf(b); num += w * b; den += w; }
  return num / den;
}
export const laplaceMean = (y, scale, s = 1) => numericMean(y, (b) => laplacePdf(b, scale), s);
const LG = Array.from({ length: 601 }, (_, i) => -9 + (18 * i) / 600); // log λ
/** Horseshoe: β | λ ~ N(0, τ²λ²), λ ~ C⁺(0,1). E[β|y] = y·(1 − E[κ|y]), κ = s²/(s² + τ²λ²). */
export function horseshoeMean(y, tau, s = 1) {
  let num = 0, den = 0;
  for (const u of LG) { const lam = Math.exp(u), v = tau * tau * lam * lam, w = normalPdf(y, 0, Math.sqrt(s * s + v)) * (2 / (Math.PI * (1 + lam * lam))) * lam; num += w * (v / (s * s + v)); den += w; }
  return y * (num / den);
}
export const PRIORS = { mle: (y) => y, gaussian: (y, sc) => gaussianMean(y, sc), laplace: (y, sc) => laplaceMean(y, sc), horseshoe: (y, sc) => horseshoeMean(y, sc) };
export function sparseData({ p = 50, k = 5, big = 5, s = 1, seed = 1 }) {
  const r = mulberry32(seed), beta = Array.from({ length: p }, (_, j) => (j < k ? big * (j % 2 ? -1 : 1) : 0));
  return { beta, y: beta.map((b) => b + s * randn(r)) };
}
export const mse = (est, truth) => est.reduce((a, e, j) => a + (e - truth[j]) ** 2, 0) / est.length;
