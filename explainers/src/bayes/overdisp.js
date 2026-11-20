// Quá phân tán: Poisson vs Negative Binomial (đếm quanh trung bình μ, tham số dispersion r; Var = μ + μ²/r).
import { mulberry32, gammaSample, poissonSample, lgamma } from './stats.js';

export const nbLogPmf = (k, mu, r) => lgamma(k + r) - lgamma(r) - lgamma(k + 1) + r * Math.log(r / (r + mu)) + k * Math.log(mu / (r + mu));
export const nbPmf = (k, mu, r) => Math.exp(nbLogPmf(k, mu, r));
export const poisPmf = (k, lam) => Math.exp(k * Math.log(lam) - lam - lgamma(k + 1));
export const nbSample = (rng, mu, r) => poissonSample(rng, (gammaSample(rng, r) * mu) / r);
export function simulateNb(n, mu, r, seed = 1) { const g = mulberry32(seed); return Array.from({ length: n }, () => nbSample(g, mu, r)); }
export function simulatePoisson(n, lam, seed = 1) { const g = mulberry32(seed); return Array.from({ length: n }, () => poissonSample(g, lam)); }
export const meanOf = (xs) => xs.reduce((a, b) => a + b, 0) / xs.length;
export const varOf = (xs) => { const m = meanOf(xs); return xs.reduce((a, b) => a + (b - m) ** 2, 0) / (xs.length - 1); };
export const dispersionRatio = (xs) => varOf(xs) / Math.max(meanOf(xs), 1e-9);

/** Poisson + prior Gamma(a, b) trên λ: posterior Gamma(a + Σy, b + n) ⇒ dự báo là NB(μ = a′/b′, r = a′). */
export function poissonPosterior(counts, a = 0.01, b = 0.01) { const a2 = a + counts.reduce((x, y) => x + y, 0), b2 = b + counts.length; return { a: a2, b: b2, mu: a2 / b2, r: a2 }; }
/** Posterior 2-D (log μ, log r) của NB trên lưới; prior log μ ~ N(1, 3²), log r ~ N(0, 2²). */
export function nbGrid(counts, G = 61) {
  const us = Array.from({ length: G }, (_, i) => -2 + (6 * i) / (G - 1)), vs = Array.from({ length: G }, (_, i) => -3 + (8 * i) / (G - 1));
  const lp = new Float64Array(G * G); let mx = -Infinity;
  for (let i = 0; i < G; i++) for (let j = 0; j < G; j++) { const mu = Math.exp(us[i]), r = Math.exp(vs[j]); let l = -((us[i] - 1) ** 2) / 18 - (vs[j] ** 2) / 8; for (const y of counts) l += nbLogPmf(y, mu, r); lp[i * G + j] = l; if (l > mx) mx = l; }
  let Z = 0; const P = new Float64Array(G * G); for (let k = 0; k < G * G; k++) { P[k] = Math.exp(lp[k] - mx); Z += P[k]; } for (let k = 0; k < G * G; k++) P[k] /= Z;
  const pv = new Float64Array(G); for (let i = 0; i < G; i++) for (let j = 0; j < G; j++) pv[j] += P[i * G + j];
  return { G, us, vs, P, pv };
}
export function nbDraw(post, K, seed = 1) {
  const g = mulberry32(seed), { G, P, us, vs } = post, cum = new Float64Array(G * G); let s = 0; for (let k = 0; k < G * G; k++) { s += P[k]; cum[k] = s; }
  return Array.from({ length: K }, () => { const u = g() * s; let lo = 0, hi = G * G - 1; while (lo < hi) { const m = (lo + hi) >> 1; if (cum[m] < u) lo = m + 1; else hi = m; } return { mu: Math.exp(us[Math.floor(lo / G)]), r: Math.exp(vs[lo % G]) }; });
}
export const logRMedian = (post) => { let c = 0; for (let j = 0; j < post.G; j++) { c += post.pv[j]; if (c >= 0.5) return post.vs[j]; } return post.vs.at(-1); };
export function predictivePmf(draws, kmax) { const out = new Array(kmax + 1).fill(0); draws.forEach((d) => { for (let k = 0; k <= kmax; k++) out[k] += nbPmf(k, d.mu, d.r) / draws.length; }); return out; }
/** PPC: thống kê T(y) (tỉ số var/mean, tỉ lệ số 0…) của dữ liệu thật so với R bản sao từ dự báo posterior. */
export const STATS = { ratio: dispersionRatio, zeros: (xs) => xs.filter((v) => v === 0).length / xs.length, max: (xs) => Math.max(...xs) };
export function ppcCounts(counts, model, stat, R = 400, seed = 1, nbpost = null) {
  const g = mulberry32(seed), n = counts.length, T = STATS[stat], obs = T(counts), post = model === 'nb' ? nbpost || nbGrid(counts) : poissonPosterior(counts), draws = model === 'nb' ? nbDraw(post, R, seed + 1) : null, reps = [];
  for (let i = 0; i < R; i++) {
    const rep = model === 'nb' ? Array.from({ length: n }, () => nbSample(g, draws[i].mu, draws[i].r)) : (() => { const lam = gammaSample(g, post.a) / post.b; return Array.from({ length: n }, () => poissonSample(g, lam)); })();
    reps.push(T(rep));
  }
  return { obs, reps, p: reps.filter((v) => v >= obs).length / R, pTwo: 2 * Math.min(reps.filter((v) => v >= obs).length, reps.filter((v) => v <= obs).length) / R };
}
