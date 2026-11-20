import test from 'node:test';
import assert from 'node:assert/strict';
import * as S from '../src/bayes/stats.js';
import { betaBinomial, betaPath, flipSequence, gammaPoisson, poissonCounts, normalNormal, normalData, gridMoments } from '../src/bayes/conjugate.js';
import { diagnose, bayesPPV, updateDiscrete, coinPath } from '../src/bayes/bayesrule.js';
import { gridApprox, PRIORS } from '../src/bayes/grid.js';

const close = (a, b, tol, msg) => assert.ok(Math.abs(a - b) <= tol, `${msg ?? ''} ${a} vs ${b}`);

test('hàm đặc biệt: lgamma, erf, beta/gamma CDF khớp giá trị đã biết', () => {
  close(S.lgamma(5), Math.log(24), 1e-12); close(S.lgamma(0.5), Math.log(Math.sqrt(Math.PI)), 1e-12);
  close(S.normalCdf(1.96), 0.9750021048517795, 1e-12); close(S.normalCdf(0), 0.5, 1e-15);
  close(S.normalQuantile(0.975), 1.959963984540054, 1e-9);
  close(S.betaCdf(0.5, 2, 2), 0.5, 1e-12); close(S.betaCdf(0.3, 1, 1), 0.3, 1e-12); close(S.betaCdf(0.25, 2, 3), 0.26171875, 1e-10);
  close(S.gammaCdf(2, 1, 1), 1 - Math.exp(-2), 1e-12); close(S.gammaCdf(3, 3, 1), 1 - Math.exp(-3) * (1 + 3 + 4.5), 1e-10);
  close(S.betaQuantile(0.5, 2, 2), 0.5, 1e-9);
  let tot = 0; for (let k = 0; k <= 10; k++) tot += S.binomPmf(k, 10, 0.3); close(tot, 1, 1e-12);
  tot = 0; for (let k = 0; k <= 10; k++) tot += S.betaBinomPmf(k, 10, 2, 3); close(tot, 1, 1e-12);
});
test('bộ lấy mẫu: trung bình/phương sai khớp lý thuyết (seed cố định)', () => {
  const r = S.mulberry32(42), N = 40000;
  const g = Array.from({ length: N }, () => S.gammaSample(r, 3)); close(S.mean(g), 3, 0.05); close(S.variance(g), 3, 0.15);
  const b = Array.from({ length: N }, () => S.betaSample(r, 2, 5)); close(S.mean(b), 2 / 7, 0.005);
  const p = Array.from({ length: N }, () => S.poissonSample(r, 45)); close(S.mean(p), 45, 0.2); close(S.variance(p), 45, 1.5);
  const z = Array.from({ length: N }, () => S.randn(r)); close(S.mean(z), 0, 0.02); close(S.sd(z), 1, 0.02);
  const gs = Array.from({ length: N }, () => S.gammaSample(r, 0.4)); close(S.mean(gs), 0.4, 0.02);
});

test('Beta–Binomial: posterior liên hợp trùng posterior lưới (trung bình, phương sai, khoảng 95%)', () => {
  for (const [a, b, k, n] of [[1, 1, 7, 10], [2, 2, 3, 12], [5, 5, 20, 25], [1.5, 1.5, 0, 6]]) {
    const c = betaBinomial(a, b, k, n);
    const g = gridMoments((t) => S.betaPdf(t, a, b) * S.binomPmf(k, n, t), 1e-9, 1 - 1e-9, 40001);
    close(c.mean, g.mean, 2e-4, 'mean'); close(c.var, g.var, 1e-5, 'var');
    close(c.ci[0], g.ci[0], 2e-3, 'lo'); close(c.ci[1], g.ci[1], 2e-3, 'hi');
  }
  const p = betaPath(1, 1, [1, 1, 0, 1]); assert.deepEqual(p.at(-1), { a: 4, b: 2, k: 3, n: 4 });
  const fs = flipSequence(0.7, 2000, 3); close(fs.reduce((x, y) => x + y) / 2000, 0.7, 0.03);
  // cập nhật tuần tự = cập nhật một lần
  const seq = betaPath(2, 3, fs.slice(0, 50)).at(-1), one = betaBinomial(2, 3, fs.slice(0, 50).reduce((x, y) => x + y), 50); assert.equal(seq.a, one.a); assert.equal(seq.b, one.b);
});
test('Gamma–Poisson và Normal–Normal khớp tích phân số', () => {
  for (const [a, b, lam, n] of [[2, 1, 4, 10], [1, 0.5, 9, 5], [10, 2, 3, 20]]) {
    const xs = poissonCounts(lam, n, 7), c = gammaPoisson(a, b, xs), S1 = xs.reduce((x, y) => x + y, 0);
    const g = gridMoments((t) => S.gammaPdf(t, a, b) * Math.exp(S1 * Math.log(t) - n * t), 1e-9, 60 + 8 * lam, 60001);
    close(c.mean, g.mean, 5e-3, 'mean'); close(c.var, g.var, 5e-3, 'var'); close(c.ci[0], g.ci[0], 0.01); close(c.ci[1], g.ci[1], 0.01);
  }
  for (const [mu0, tau0, sigma, n] of [[0, 1, 2, 5], [170, 10, 8, 30], [0, 100, 1, 3]]) {
    const xs = normalData(mu0 + 1, sigma, n, 5), c = normalNormal(mu0, tau0, sigma, xs);
    const g = gridMoments((t) => S.normalPdf(t, mu0, tau0) * xs.reduce((p, x) => p * Math.exp(-0.5 * ((x - t) / sigma) ** 2), 1), mu0 - 12 * tau0 - 20, mu0 + 12 * tau0 + 20, 80001);
    close(c.mu, g.mean, 1e-3 * (1 + tau0), 'mean'); close(c.sd ** 2, g.var, 1e-3 * (1 + tau0), 'var');
  }
  const noData = normalNormal(3, 2, 1, []); close(noData.mu, 3, 1e-12); close(noData.sd, 2, 1e-12);
});
test('Bayes: tần suất tự nhiên khớp công thức; cập nhật rời rạc chuẩn hóa', () => {
  const d = diagnose(0.01, 0.9, 0.95, 10000); close(d.ppv, bayesPPV(0.01, 0.9, 0.95), 1e-12); close(d.tp + d.fn + d.fp + d.tn, 10000, 1e-9);
  close(bayesPPV(0.01, 0.9, 0.95), 0.9 * 0.01 / (0.9 * 0.01 + 0.05 * 0.99), 1e-12);
  const u = updateDiscrete([0.5, 0.3, 0.2], [0.1, 0.4, 0.8]); close(u.posterior.reduce((a, b) => a + b), 1, 1e-12);
  const path = coinPath([1 / 3, 1 / 3, 1 / 3], [1, 1, 1, 1, 0, 1]);
  // tuần tự = một lần với likelihood tích
  const lk = [0.2, 0.5, 0.8].map((p) => p ** 5 * (1 - p)); const one = updateDiscrete([1 / 3, 1 / 3, 1 / 3], lk).posterior;
  path.at(-1).forEach((v, i) => close(v, one[i], 1e-12));
});
test('xấp xỉ lưới hội tụ về posterior chính xác; prior không liên hợp khớp lưới mịn', () => {
  const exact = betaBinomial(1, 1, 6, 9);
  let prev = Infinity;
  for (const N of [5, 10, 50, 200, 1000]) { const g = gridApprox(PRIORS.flat.pdf, 6, 9, N); const e = Math.abs(g.mean - exact.mean); assert.ok(e <= prev + 1e-12 || e < 1e-4); prev = e; }
  const g = gridApprox(PRIORS.flat.pdf, 6, 9, 2000); close(g.mean, exact.mean, 1e-4); close(g.sd, Math.sqrt(exact.var), 2e-4); close(g.ci[0], exact.ci[0], 2e-3); close(g.evidence, 1 / 10, 1e-4); // ∫ Binom(6;9,θ)dθ = 1/(n+1)
  for (const key of ['tri', 'bimodal']) { const a = gridApprox(PRIORS[key].pdf, 8, 12, 200), b = gridApprox(PRIORS[key].pdf, 8, 12, 20000); close(a.mean, b.mean, 2e-3, key); close(b.post.reduce((x, y) => x + y), 1, 1e-9); }
});
