// p-value và t-test bằng mô phỏng.
import { mulberry32, randn, tCdf, normalCdf } from './stats.js';

export function tStat(xs, mu0 = 0) { const n = xs.length, m = xs.reduce((a, b) => a + b, 0) / n, s = Math.sqrt(xs.reduce((a, b) => a + (b - m) ** 2, 0) / (n - 1)); return (m - mu0) / (s / Math.sqrt(n)); }
export const pTwoSided = (t, df) => 2 * (1 - tCdf(Math.abs(t), df));
/** reps thí nghiệm, mỗi thí nghiệm n quan sát N(d, 1); kiểm định H0: μ = 0. */
export function simulateT({ n = 10, d = 0, reps = 1000, seed = 1 }) {
  const r = mulberry32(seed), t = [], p = [];
  for (let k = 0; k < reps; k++) { const xs = Array.from({ length: n }, () => d + randn(r)), ti = tStat(xs); t.push(ti); p.push(pTwoSided(ti, n - 1)); }
  return { t, p };
}
export const rejectRate = (p, alpha = 0.05) => p.filter((v) => v < alpha).length / p.length;
/** Công suất của z-test hai phía (xấp xỉ khi n lớn). */
export const zPower = (n, d, alpha = 0.05, z = 1.959964) => { const s = d * Math.sqrt(n); return normalCdf(-z + s) + normalCdf(-z - s); };
export const powerSim = (n, d, reps = 400, seed = 1) => rejectRate(simulateT({ n, d, reps, seed }).p);
export function histDensity(xs, lo, hi, bins) { const h = (hi - lo) / bins, c = new Array(bins).fill(0); xs.forEach((v) => { if (v >= lo && v < hi) c[Math.floor((v - lo) / h)]++; }); return c.map((k, i) => ({ x0: lo + i * h, x1: lo + (i + 1) * h, h: k / (xs.length * h) })); }
