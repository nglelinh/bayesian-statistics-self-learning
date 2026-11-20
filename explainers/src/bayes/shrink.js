// Prior chuẩn cho hệ số đa thức = hồi quy ridge: posterior mean = (XᵀX + λI)⁻¹Xᵀy, λ = σ²/τ².
import { mulberry32, randn } from './stats.js';

export const design = (xs, d) => xs.map((x) => Array.from({ length: d + 1 }, (_, j) => x ** j));
export function solve(A, b) {
  const n = b.length, M = A.map((r, i) => [...r, b[i]]);
  for (let c = 0; c < n; c++) {
    let p = c; for (let r = c + 1; r < n; r++) if (Math.abs(M[r][c]) > Math.abs(M[p][c])) p = r;
    [M[c], M[p]] = [M[p], M[c]];
    for (let r = c + 1; r < n; r++) { const f = M[r][c] / M[c][c]; for (let k = c; k <= n; k++) M[r][k] -= f * M[c][k]; }
  }
  const x = new Array(n).fill(0);
  for (let i = n - 1; i >= 0; i--) { let s = M[i][n]; for (let k = i + 1; k < n; k++) s -= M[i][k] * x[k]; x[i] = s / M[i][i]; }
  return x;
}
export function precision(xs, d, sigma, tau) {
  const X = design(xs, d), m = d + 1;
  return Array.from({ length: m }, (_, i) => Array.from({ length: m }, (_, j) => X.reduce((s, row) => s + row[i] * row[j], 0) / sigma ** 2 + (i === j ? 1 / tau ** 2 : 0)));
}
export function fitRidge(xs, ys, d, sigma, tau) {
  const X = design(xs, d), P = precision(xs, d, sigma, tau), rhs = Array.from({ length: d + 1 }, (_, j) => X.reduce((s, row, i) => s + row[j] * ys[i], 0) / sigma ** 2);
  return { w: solve(P, rhs), P, d, sigma, tau };
}
export const evalPoly = (w, x) => w.reduce((s, c, j) => s + c * x ** j, 0);
export const mse = (w, xs, ys) => xs.reduce((s, x, i) => s + (evalPoly(w, x) - ys[i]) ** 2, 0) / xs.length;
export const truth = (x) => Math.sin(Math.PI * x);
export function sineData(n, sigma, seed = 1) { const r = mulberry32(seed); const xs = Array.from({ length: n }, () => -1 + 2 * r()); return { xs, ys: xs.map((x) => truth(x) + sigma * randn(r)) }; }
/** Lấy mẫu w ~ N(w_hat, P⁻¹) bằng Cholesky của P: w = ŵ + L⁻ᵀz với P = LLᵀ. */
export function samplePosterior(fit, K, seed = 1) {
  const P = fit.P, m = P.length, L = Array.from({ length: m }, () => new Array(m).fill(0));
  for (let i = 0; i < m; i++) for (let j = 0; j <= i; j++) { let s = P[i][j]; for (let k = 0; k < j; k++) s -= L[i][k] * L[j][k]; L[i][j] = i === j ? Math.sqrt(s) : s / L[j][j]; }
  const r = mulberry32(seed);
  return Array.from({ length: K }, () => { const z = Array.from({ length: m }, () => randn(r)); const y = new Array(m).fill(0); for (let i = m - 1; i >= 0; i--) { let s = z[i]; for (let k = i + 1; k < m; k++) s -= L[k][i] * y[k]; y[i] = s / L[i][i]; } return fit.w.map((wi, i) => wi + y[i]); });
}
