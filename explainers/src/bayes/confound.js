// Confounding (fork), collider và interaction: mô phỏng + OLS.
import { mulberry32, randn } from './stats.js';
import { solve } from './shrink.js';

export function olsMulti(X, y) {
  const m = X[0].length, A = Array.from({ length: m }, (_, i) => Array.from({ length: m }, (_, j) => X.reduce((s, r) => s + r[i] * r[j], 0))), b = Array.from({ length: m }, (_, j) => X.reduce((s, r, i) => s + r[j] * y[i], 0));
  const beta = solve(A, b), rss = X.reduce((s, r, i) => s + (y[i] - r.reduce((t, v, k) => t + v * beta[k], 0)) ** 2, 0);
  return { beta, rss };
}
export const slope = (x, y) => olsMulti(x.map((v) => [1, v]), y).beta[1];
export const corr = (x, y) => { const n = x.length, mx = x.reduce((a, b) => a + b) / n, my = y.reduce((a, b) => a + b) / n; let sxy = 0, sxx = 0, syy = 0; for (let i = 0; i < n; i++) { sxy += (x[i] - mx) * (y[i] - my); sxx += (x[i] - mx) ** 2; syy += (y[i] - my) ** 2; } return sxy / Math.sqrt(sxx * syy); };

/** Z → X, Z → Y, X → Y:  X = γZ + e,  Y = βX + δZ + e. Hệ số "ngây thơ" lệch δγ/(γ²+1). */
export function simFork({ n = 400, gamma = 1, beta = 0.5, delta = 1.5, seed = 1 }) {
  const r = mulberry32(seed), z = [], x = [], y = [];
  for (let i = 0; i < n; i++) { const zi = randn(r), xi = gamma * zi + randn(r); z.push(zi); x.push(xi); y.push(beta * xi + delta * zi + randn(r)); }
  return { x, y, z };
}
export const forkBias = (gamma, delta) => (delta * gamma) / (gamma * gamma + 1);
export const adjustedSlope = (x, y, z) => olsMulti(x.map((v, i) => [1, v, z[i]]), y).beta[1];
export function tertiles(v) { const s = [...v].sort((a, b) => a - b), q1 = s[Math.floor(s.length / 3)], q2 = s[Math.floor((2 * s.length) / 3)]; return v.map((t) => (t < q1 ? 0 : t < q2 ? 1 : 2)); }
export function strataSlopes(x, y, g) { return [0, 1, 2].map((k) => { const idx = g.map((v, i) => (v === k ? i : -1)).filter((i) => i >= 0); return slope(idx.map((i) => x[i]), idx.map((i) => y[i])); }); }

/** X ⟂ Y nhưng C = X + Y + e (collider). corr(X,Y | C) = −1/(1+σe²). */
export function simCollider({ n = 400, se = 0.5, seed = 1 }) {
  const r = mulberry32(seed), x = [], y = [], c = [];
  for (let i = 0; i < n; i++) { const xi = randn(r), yi = randn(r); x.push(xi); y.push(yi); c.push(xi + yi + se * randn(r)); }
  return { x, y, c };
}
export const colliderPartialCorr = (se) => -1 / (1 + se * se);
export function partialCorr(x, y, c) { const X = c.map((v) => [1, v]), rx = olsMulti(X, x).beta, ry = olsMulti(X, y).beta; return corr(x.map((v, i) => v - rx[0] - rx[1] * c[i]), y.map((v, i) => v - ry[0] - ry[1] * c[i])); }

/** y = b0 + b1·x + b2·g + b3·x·g + ε, g ∈ {0,1}. */
export function simInteraction({ n = 120, b0 = 1, b1 = 0.5, b2 = 0.5, b3 = 1, sigma = 0.6, seed = 1 }) {
  const r = mulberry32(seed), x = [], g = [], y = [];
  for (let i = 0; i < n; i++) { const xi = -2 + 4 * r(), gi = r() < 0.5 ? 0 : 1; x.push(xi); g.push(gi); y.push(b0 + b1 * xi + b2 * gi + b3 * xi * gi + sigma * randn(r)); }
  return { x, g, y };
}
export function fitInteraction(x, g, y) {
  return {
    pooled: olsMulti(x.map((v) => [1, v]), y),
    additive: olsMulti(x.map((v, i) => [1, v, g[i]]), y),
    inter: olsMulti(x.map((v, i) => [1, v, g[i], v * g[i]]), y)
  };
}
