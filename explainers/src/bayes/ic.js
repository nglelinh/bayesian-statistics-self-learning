// WAIC / LOO cho hồi quy đa thức Gaussian (σ biết, prior N(0,τ²)): WAIC từ mẫu posterior, LOO chính xác bằng fit lại (dạng đóng).
import { fitRidge, samplePosterior, evalPoly, design, solve, precision } from './shrink.js';

const LOG2PI = Math.log(2 * Math.PI);
export const logNorm = (y, m, s) => -0.5 * LOG2PI - Math.log(s) - 0.5 * ((y - m) / s) ** 2;
export function logSumExp(a) { const m = Math.max(...a); return m + Math.log(a.reduce((s, v) => s + Math.exp(v - m), 0)); }
const dot = (u, v) => u.reduce((s, x, i) => s + x * v[i], 0);

/** Với mỗi điểm i: lppd_i = log mean_s p(y_i|w_s) và p_waic,i = Var_s log p(y_i|w_s). */
export function waic(xs, ys, d, sigma, tau, S = 1500, seed = 1) {
  const fit = fitRidge(xs, ys, d, sigma, tau), W = samplePosterior(fit, S, seed);
  const lppd = [], pw = [];
  xs.forEach((x, i) => {
    const ll = W.map((w) => logNorm(ys[i], evalPoly(w, x), sigma)), m = ll.reduce((a, b) => a + b, 0) / S;
    lppd.push(logSumExp(ll) - Math.log(S)); pw.push(ll.reduce((a, b) => a + (b - m) ** 2, 0) / (S - 1));
  });
  const sum = (a) => a.reduce((x, y) => x + y, 0);
  return { fit, W, lppd, pw, lppdSum: sum(lppd), pSum: sum(pw), elpd: sum(lppd) - sum(pw) };
}
/** Số tham số hiệu dụng giải tích: tr(P⁻¹ XᵀX)/σ². */
export function effectiveParams(xs, d, sigma, tau) {
  const P = precision(xs, d, sigma, tau), X = design(xs, d), m = d + 1;
  let tr = 0;
  for (let j = 0; j < m; j++) { const col = Array.from({ length: m }, (_, i) => X.reduce((s, r) => s + r[i] * r[j], 0) / sigma ** 2); tr += solve(P, col)[j]; }
  return tr;
}
/** Mật độ dự báo posterior (dạng đóng) tại x: N(x·ŵ, σ² + xᵀP⁻¹x). */
export function predictiveLog(fit, x, y) {
  const row = design([x], fit.d)[0], mean = dot(row, fit.w), v = fit.sigma ** 2 + dot(row, solve(fit.P, row));
  return logNorm(y, mean, Math.sqrt(v));
}
/** LOO chính xác: fit lại không có điểm i, rồi lấy log mật độ dự báo tại (x_i, y_i). */
export function exactLoo(xs, ys, d, sigma, tau) {
  return xs.map((x, i) => { const xi = xs.filter((_, j) => j !== i), yi = ys.filter((_, j) => j !== i); return predictiveLog(fitRidge(xi, yi, d, sigma, tau), x, ys[i]); });
}
export function testElpd(fit, xt, yt) { return xt.reduce((s, x, i) => s + predictiveLog(fit, x, yt[i]), 0) / xt.length; }
export function analyse(xs, ys, d, sigma, tau, test, S = 600, seed = 1) {
  const w = waic(xs, ys, d, sigma, tau, S, seed), loo = exactLoo(xs, ys, d, sigma, tau), looSum = loo.reduce((a, b) => a + b, 0);
  return { d, ...w, loo, looSum, test: testElpd(w.fit, test.xs, test.ys) * xs.length };
}
/** Sai số chuẩn của chênh lệch elpd theo điểm giữa hai mô hình: sqrt(n·Var(diff_i)). */
export function seDiff(a, b) { const n = a.length, d = a.map((v, i) => v - b[i]), m = d.reduce((x, y) => x + y, 0) / n; return Math.sqrt(n * d.reduce((s, v) => s + (v - m) ** 2, 0) / (n - 1)); }
/** Trọng số pseudo-BMA ∝ exp(elpd). */
export function pseudoBma(elpds) { const m = Math.max(...elpds), e = elpds.map((v) => Math.exp(v - m)), s = e.reduce((a, b) => a + b, 0); return e.map((v) => v / s); }
