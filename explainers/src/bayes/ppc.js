// Kiểm tra dự đoán posterior (PPC) cho chuỗi nhị phân với mô hình Bernoulli i.i.d. + prior Beta.
import { mulberry32, betaSample } from './stats.js';

export const STATS = {
  total: { vi: 'Tổng số ngửa', en: 'Total heads', f: (s) => s.reduce((a, b) => a + b, 0) },
  switches: { vi: 'Số lần đổi mặt (0↔1)', en: 'Number of switches (0↔1)', f: (s) => s.reduce((a, b, i) => a + (i && b !== s[i - 1] ? 1 : 0), 0) },
  longestRun: { vi: 'Chuỗi liên tiếp dài nhất', en: 'Longest run', f: (s) => { let best = 0, cur = 0; s.forEach((b, i) => { cur = i && b === s[i - 1] ? cur + 1 : 1; best = Math.max(best, cur); }); return best; } }
};
export function markovSequence(n, stay, seed = 1) { const r = mulberry32(seed); const s = [r() < 0.5 ? 1 : 0]; for (let i = 1; i < n; i++) s.push(r() < stay ? s[i - 1] : 1 - s[i - 1]); return s; }
export function iidSequence(n, theta, seed = 1) { const r = mulberry32(seed); return Array.from({ length: n }, () => (r() < theta ? 1 : 0)); }

export function ppc(data, a0, b0, statKey, R = 500, seed = 1) {
  const r = mulberry32(seed), n = data.length, k = data.reduce((x, y) => x + y, 0), A = a0 + k, B = b0 + n - k, f = STATS[statKey].f;
  const obs = f(data), reps = [], thetas = [], firstReps = [];
  for (let i = 0; i < R; i++) { const th = betaSample(r, A, B); thetas.push(th); const seq = Array.from({ length: n }, () => (r() < th ? 1 : 0)); if (i < 4) firstReps.push(seq); reps.push(f(seq)); }
  const upper = reps.filter((x) => x >= obs).length / R, lower = reps.filter((x) => x <= obs).length / R;
  return { obs, reps, thetas, firstReps, pvalue: Math.min(1, 2 * Math.min(upper, lower)), upper, lower, posterior: { a: A, b: B } };
}
