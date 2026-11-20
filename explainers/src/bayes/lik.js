// Likelihood explorer + prior predictive.
import { mulberry32, betaSample, binomialSample, gammaSample, poissonSample, lgamma, betaBinomPmf } from './stats.js';

export const llBinom = (k, n, th) => (th <= 0 ? (k === 0 ? 0 : -Infinity) : th >= 1 ? (k === n ? 0 : -Infinity) : (k ? k * Math.log(th) : 0) + (n - k ? (n - k) * Math.log(1 - th) : 0));
export const llPoisson = (counts, lam) => (lam <= 0 ? -Infinity : counts.reduce((s, y) => s + y * Math.log(lam) - lam - lgamma(y + 1), 0));
export const mleBinom = (k, n) => k / n;
export const mlePoisson = (counts) => counts.reduce((a, b) => a + b, 0) / counts.length;
/** Likelihood tương đối R(θ) = L(θ)/L(θ̂) trên lưới. */
export function relLik(ll, mle, lo, hi, N = 400) { const top = ll(mle); return Array.from({ length: N + 1 }, (_, i) => { const t = lo + (hi - lo) * i / N; return [t, Math.exp(ll(t) - top)]; }); }
/** Khoảng likelihood {θ: R(θ) ≥ c}; c = exp(−1.92) ≈ 0.147 tương ứng ~95% (xấp xỉ). */
export function likInterval(ll, mle, lo, hi, c = Math.exp(-1.92), N = 4000) {
  const top = ll(mle), ok = (t) => ll(t) - top >= Math.log(c);
  const bis = (a, b) => { for (let i = 0; i < 80; i++) { const m = (a + b) / 2; if (ok(m) === ok(a)) a = m; else b = m; } return (a + b) / 2; };
  let L = lo, U = hi; const eps = 1e-9;
  if (!ok(lo + eps)) L = bis(lo + eps, mle); if (!ok(hi - eps)) U = bis(mle, hi - eps);
  return [L, U];
}
/** Phân phối dự báo prior (Beta–Binomial / Gamma–Poisson=nhị thức âm): mô phỏng dữ liệu từ prior. */
export function priorPredictiveBinom(a, b, n, R, seed = 1) { const r = mulberry32(seed), c = new Array(n + 1).fill(0); for (let i = 0; i < R; i++) c[binomialSample(r, n, betaSample(r, a, b))]++; return c.map((v) => v / R); }
export const exactPredictiveBinom = (a, b, n) => Array.from({ length: n + 1 }, (_, k) => betaBinomPmf(k, n, a, b));
export const nbPmf = (k, a, rate) => Math.exp(lgamma(k + a) - lgamma(a) - lgamma(k + 1) + a * Math.log(rate / (1 + rate)) - k * Math.log(1 + rate));
export function priorPredictivePoisson(a, rate, kmax, R, seed = 1) { const r = mulberry32(seed), c = new Array(kmax + 1).fill(0); for (let i = 0; i < R; i++) { const y = poissonSample(r, gammaSample(r, a) / rate); if (y <= kmax) c[y]++; } return c.map((v) => v / R); }
