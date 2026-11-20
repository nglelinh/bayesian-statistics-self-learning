// Hồi quy tuyến tính Bayes y = a + b·x + ε, ε ~ N(0, σ²), prior a, b ~ N(0, τ²) (σ biết), nghiệm đóng.
import { mulberry32, randn } from './stats.js';

export function lineData(a, b, sigma, n, seed = 1, lo = -2, hi = 2) {
  const r = mulberry32(seed); const xs = Array.from({ length: n }, () => lo + (hi - lo) * r());
  return { xs, ys: xs.map((x) => a + b * x + sigma * randn(r)) };
}
export function ols(xs, ys) {
  const n = xs.length, mx = xs.reduce((a, b) => a + b) / n, my = ys.reduce((a, b) => a + b) / n;
  const b = xs.reduce((s, x, i) => s + (x - mx) * (ys[i] - my), 0) / xs.reduce((s, x) => s + (x - mx) ** 2, 0);
  return { a: my - b * mx, b };
}
export function fitBayes(xs, ys, sigma, tau) {
  let sxx = 0, sx = 0, sxy = 0, sy = 0; const n = xs.length;
  xs.forEach((x, i) => { sx += x; sxx += x * x; sxy += x * ys[i]; sy += ys[i]; });
  const p0 = 1 / tau ** 2, s2 = sigma ** 2;
  const P = [[n / s2 + p0, sx / s2], [sx / s2, sxx / s2 + p0]], det = P[0][0] * P[1][1] - P[0][1] ** 2;
  const S = [[P[1][1] / det, -P[0][1] / det], [-P[1][0] / det, P[0][0] / det]], rhs = [sy / s2, sxy / s2];
  return { mean: [S[0][0] * rhs[0] + S[0][1] * rhs[1], S[1][0] * rhs[0] + S[1][1] * rhs[1]], cov: S, sigma, tau, n };
}
export function sampleLines(fit, K, seed = 1) {
  const r = mulberry32(seed), [[s11, s12], , ] = [fit.cov[0]], s22 = fit.cov[1][1];
  const l11 = Math.sqrt(s11), l21 = s12 / l11, l22 = Math.sqrt(Math.max(0, s22 - l21 * l21));
  return Array.from({ length: K }, () => { const z1 = randn(r), z2 = randn(r); return { a: fit.mean[0] + l11 * z1, b: fit.mean[1] + l21 * z1 + l22 * z2 }; });
}
export function predict(fit, x, withNoise = true) {
  const m = fit.mean[0] + fit.mean[1] * x, v = fit.cov[0][0] + 2 * x * fit.cov[0][1] + x * x * fit.cov[1][1];
  return { mean: m, sd: Math.sqrt(v + (withNoise ? fit.sigma ** 2 : 0)) };
}
