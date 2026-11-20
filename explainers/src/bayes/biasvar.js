// Phân rã bias–variance bằng mô phỏng: nhiều tập dữ liệu độc lập, mỗi tập khớp một đa thức (ridge).
import { fitRidge, evalPoly, truth, sineData } from './shrink.js';
import { mulberry32, randn } from './stats.js';

/** Lưới điểm giữa (đều theo độ đo đều trên [−1, 1], không dồn trọng số vào hai đầu mút nơi đa thức bậc cao dao động mạnh). */
export const GRID = Array.from({ length: 400 }, (_, i) => -1 + (2 * (i + 0.5)) / 400);
export function ensemble(d, { n = 20, sigma = 0.3, tau = 100, R = 120, seed = 1 } = {}) {
  return Array.from({ length: R }, (_, r) => { const { xs, ys } = sineData(n, sigma, seed * 1000 + r + 1); return fitRidge(xs, ys, d, sigma, tau).w; });
}
/** bias² = mean_x (f̄ − f*)², variance = mean_x mean_r (f_r − f̄)², total = mean_x mean_r (f_r − f*)². Đồng nhất thức: total = bias² + variance. */
export function decompose(fits, grid = GRID, f = truth) {
  const R = fits.length, F = fits.map((w) => grid.map((x) => evalPoly(w, x))), fbar = grid.map((_, j) => F.reduce((s, row) => s + row[j], 0) / R);
  let bias2 = 0, variance = 0, total = 0;
  grid.forEach((x, j) => { bias2 += (fbar[j] - f(x)) ** 2; F.forEach((row) => { variance += (row[j] - fbar[j]) ** 2 / R; total += (row[j] - f(x)) ** 2 / R; }); });
  const G = grid.length; return { bias2: bias2 / G, variance: variance / G, total: total / G, fbar, F };
}
/** Sai số dự đoán trên dữ liệu mới có nhiễu: kỳ vọng = total + σ². */
export function testError(fits, sigma = 0.3, M = 400, seed = 7) {
  const r = mulberry32(seed), xs = Array.from({ length: M }, () => -1 + 2 * r()), ys = xs.map((x) => truth(x) + sigma * randn(r));
  return fits.reduce((s, w) => s + xs.reduce((q, x, i) => q + (evalPoly(w, x) - ys[i]) ** 2, 0) / M, 0) / fits.length;
}
