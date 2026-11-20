// MCMC: Metropolis, Gibbs (chuẩn hai chiều), Hamiltonian Monte Carlo, R-hat.
import { mulberry32, randn, mean, variance, betaPdf, normalPdf } from './stats.js';

export const TARGETS = {
  beta: { vi: 'Posterior Beta(8, 4)', en: 'Posterior Beta(8, 4)', lo: 0, hi: 1, start: 0.1, step: 0.15, logp: (x) => (x <= 0 || x >= 1 ? -Infinity : 7 * Math.log(x) + 3 * Math.log(1 - x)), pdf: (x) => betaPdf(x, 8, 4), mean: 8 / 12, var: (8 * 4) / (144 * 13) },
  normal: { vi: 'Chuẩn N(0, 1)', en: 'Normal N(0, 1)', lo: -4.5, hi: 4.5, start: -3, step: 1.2, logp: (x) => -0.5 * x * x, pdf: (x) => normalPdf(x), mean: 0, var: 1 },
  bimodal: { vi: 'Hai đỉnh: 0.5·N(−2, 0.7²) + 0.5·N(2, 0.7²)', en: 'Two peaks: 0.5·N(−2, 0.7²) + 0.5·N(2, 0.7²)', lo: -5, hi: 5, start: -2, step: 1.5, logp: (x) => Math.log(0.5 * normalPdf(x, -2, 0.7) + 0.5 * normalPdf(x, 2, 0.7)), pdf: (x) => 0.5 * normalPdf(x, -2, 0.7) + 0.5 * normalPdf(x, 2, 0.7), mean: 0, var: 4 + 0.49 }
};

/** Metropolis bước ngẫu nhiên (đề xuất đối xứng chuẩn). steps[i] mô tả lần đề xuất thứ i. */
export function metropolis(logp, x0, step, n, seed = 1) {
  const r = mulberry32(seed); let x = x0, lp = logp(x); const chain = [x0], steps = []; let acc = 0;
  for (let i = 0; i < n; i++) {
    const prop = x + step * randn(r), lq = logp(prop), logA = Math.min(0, lq - lp), u = r(), ok = Math.log(u) < logA;
    steps.push({ from: x, prop, alpha: Math.exp(logA), u, accept: ok });
    if (ok) { x = prop; lp = lq; acc++; }
    chain.push(x);
  }
  return { chain, steps, acceptRate: acc / n };
}

/** Gibbs cho (x, y) chuẩn chuẩn hóa có tương quan rho: x|y ~ N(ρy, 1−ρ²), y|x tương tự. */
export function gibbsBvn(rho, n, seed = 1, start = [-2.5, 2.5]) {
  const r = mulberry32(seed), s = Math.sqrt(1 - rho * rho); let [x, y] = start; const path = [{ x, y, axis: null }];
  for (let i = 0; i < n; i++) { x = rho * y + s * randn(r); path.push({ x, y, axis: 'x' }); y = rho * x + s * randn(r); path.push({ x, y, axis: 'y' }); }
  return path;
}

/** Chuẩn hai chiều tương quan rho: U(q) = ½ qᵀΣ⁻¹q. */
export const bvnPotential = (rho) => ({
  U: ([x, y]) => (x * x - 2 * rho * x * y + y * y) / (2 * (1 - rho * rho)),
  grad: ([x, y]) => [(x - rho * y) / (1 - rho * rho), (y - rho * x) / (1 - rho * rho)]
});
export function leapfrog(grad, q0, p0, eps, L) {
  let q = q0.slice(), p = p0.slice(); const path = [{ q: q.slice(), p: p.slice() }];
  let g = grad(q); p = p.map((pi, i) => pi - 0.5 * eps * g[i]);
  for (let l = 0; l < L; l++) {
    q = q.map((qi, i) => qi + eps * p[i]); g = grad(q);
    if (l < L - 1) p = p.map((pi, i) => pi - eps * g[i]);
    path.push({ q: q.slice(), p: p.map((pi, i) => (l === L - 1 ? pi - 0.5 * eps * g[i] : pi)) });
  }
  p = p.map((pi, i) => pi - 0.5 * eps * g[i]);
  return { q, p, path };
}
export function hmc(pot, q0, eps, L, n, seed = 1) {
  const r = mulberry32(seed); let q = q0.slice(); const samples = [q.slice()], trajs = []; let acc = 0;
  for (let i = 0; i < n; i++) {
    const p0 = q.map(() => randn(r)), H0 = pot.U(q) + 0.5 * p0.reduce((a, b) => a + b * b, 0);
    const res = leapfrog(pot.grad, q, p0, eps, L), H1 = pot.U(res.q) + 0.5 * res.p.reduce((a, b) => a + b * b, 0);
    const ok = Math.log(r()) < Math.min(0, H0 - H1);
    trajs.push({ path: res.path.map((s) => s.q), accept: ok, dH: H1 - H0, from: q.slice(), to: res.q });
    if (ok) { q = res.q; acc++; }
    samples.push(q.slice());
  }
  return { samples, trajs, acceptRate: acc / n };
}

/** R-hat (Gelman–Rubin) cho nhiều chuỗi cùng độ dài. */
export function rhat(chains) {
  const m = chains.length, n = chains[0].length, means = chains.map(mean), W = mean(chains.map(variance));
  const B = n * variance(means), varPlus = ((n - 1) / n) * W + B / n;
  return Math.sqrt(varPlus / W);
}
/** ESS ước lượng qua tự tương quan (cắt khi âm). */
export function ess(chain) {
  const n = chain.length, m = mean(chain), v = chain.reduce((a, x) => a + (x - m) ** 2, 0) / n; let s = 0;
  for (let lag = 1; lag < n / 2; lag++) { let c = 0; for (let i = 0; i < n - lag; i++) c += (chain[i] - m) * (chain[i + lag] - m); const rho = c / n / v; if (rho < 0.05) break; s += rho; }
  return n / (1 + 2 * s);
}
