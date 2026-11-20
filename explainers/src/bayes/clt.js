// Luật số lớn và CLT: phân phối của trung bình mẫu.
import { mulberry32, randn, mean, sd } from './stats.js';

export const DISTS = {
  uniform: { vi: 'Đều U(0, 1)', en: 'Uniform U(0, 1)', mean: 0.5, sd: Math.sqrt(1 / 12), draw: (r) => r() },
  exponential: { vi: 'Mũ Exp(1) — lệch phải', en: 'Exponential(1) — right-skewed', mean: 1, sd: 1, draw: (r) => -Math.log(1 - r()) },
  bernoulli: { vi: 'Bernoulli(0.1) — rất lệch', en: 'Bernoulli(0.1) — very skewed', mean: 0.1, sd: Math.sqrt(0.09), draw: (r) => (r() < 0.1 ? 1 : 0) },
  bimodal: { vi: 'Hai đỉnh (0 hoặc 1 cân bằng, nhiễu)', en: 'Two peaks (0 or 1, noisy)', mean: 0.5, sd: Math.sqrt(0.25 + 0.0025), draw: (r) => (r() < 0.5 ? 0 : 1) + 0.05 * randn(r) }
};
export function sampleMeans(dist, n, reps, seed = 1) {
  const r = mulberry32(seed), d = DISTS[dist]; const out = [];
  for (let i = 0; i < reps; i++) { let s = 0; for (let j = 0; j < n; j++) s += d.draw(r); out.push(s / n); }
  return out;
}
export function skewness(xs) { const m = mean(xs), s = Math.sqrt(xs.reduce((a, x) => a + (x - m) ** 2, 0) / xs.length); return xs.reduce((a, x) => a + ((x - m) / s) ** 3, 0) / xs.length; }
export function runningMean(dist, N, seed = 1) {
  const r = mulberry32(seed), d = DISTS[dist]; let s = 0; const out = [];
  for (let i = 1; i <= N; i++) { s += d.draw(r); out.push(s / i); }
  return out;
}
export { sd };
