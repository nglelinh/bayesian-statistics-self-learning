// Đa cộng tuyến: y = b1·x1 + b2·x2 + ε, prior b ~ N(0, τ²), σ biết ⇒ posterior Gaussian dạng đóng.
import { mulberry32, randn } from './stats.js';

/** x2 = ρ·x1 + √(1−ρ²)·z; nhiễu cố định theo seed nên so sánh được giữa các ρ. */
export function simData({ n = 60, rho = 0, b1 = 1, b2 = 1, sigma = 1, seed = 1 }) {
  const r = mulberry32(seed), x1 = [], x2 = [], y = [];
  for (let i = 0; i < n; i++) { const z1 = randn(r), z2 = randn(r), e = randn(r), a = z1, b = rho * z1 + Math.sqrt(1 - rho * rho) * z2; x1.push(a); x2.push(b); y.push(b1 * a + b2 * b + sigma * e); }
  return { x1, x2, y };
}
export function posterior(x1, x2, y, sigma, tau) {
  let s11 = 0, s12 = 0, s22 = 0, t1 = 0, t2 = 0;
  x1.forEach((a, i) => { s11 += a * a; s12 += a * x2[i]; s22 += x2[i] * x2[i]; t1 += a * y[i]; t2 += x2[i] * y[i]; });
  const s2 = sigma * sigma, p = 1 / (tau * tau), P11 = s11 / s2 + p, P12 = s12 / s2, P22 = s22 / s2 + p, det = P11 * P22 - P12 * P12;
  const C = [[P22 / det, -P12 / det], [-P12 / det, P11 / det]], r1 = t1 / s2, r2 = t2 / s2;
  return { mean: [C[0][0] * r1 + C[0][1] * r2, C[1][0] * r1 + C[1][1] * r2], cov: C, sd1: Math.sqrt(C[0][0]), sd2: Math.sqrt(C[1][1]), corr: C[0][1] / Math.sqrt(C[0][0] * C[1][1]), sdSum: Math.sqrt(C[0][0] + C[1][1] + 2 * C[0][1]) };
}
export const vif = (rho) => 1 / (1 - rho * rho);
export function sampleBeta(post, K, seed = 1) {
  const r = mulberry32(seed), [[c11, c12]] = post.cov, l11 = Math.sqrt(c11), l21 = c12 / l11, l22 = Math.sqrt(Math.max(0, post.cov[1][1] - l21 * l21));
  return Array.from({ length: K }, () => { const z1 = randn(r), z2 = randn(r); return [post.mean[0] + l11 * z1, post.mean[1] + l21 * z1 + l22 * z2]; });
}
export const sampleCorr = (x1, x2) => { const n = x1.length, m1 = x1.reduce((a, b) => a + b) / n, m2 = x2.reduce((a, b) => a + b) / n; let a = 0, b = 0, c = 0; for (let i = 0; i < n; i++) { a += (x1[i] - m1) * (x2[i] - m2); b += (x1[i] - m1) ** 2; c += (x2[i] - m2) ** 2; } return a / Math.sqrt(b * c); };
