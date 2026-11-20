import test from 'node:test';
import assert from 'node:assert/strict';
import * as S from '../src/bayes/stats.js';
import { marginal0, marginal1, bf10, postProb1, savageDickey, mcMarginal, gridMarginal, bfPath } from '../src/bayes/bf.js';
import { simData, posterior, vif, sampleBeta, sampleCorr } from '../src/bayes/collinear.js';
import { olsMulti } from '../src/bayes/confound.js';
import { ensemble, decompose, testError } from '../src/bayes/biasvar.js';
import { gaussianMean, laplaceMean, horseshoeMean, numericMean, sparseData, mse, PRIORS } from '../src/bayes/horseshoe.js';
import { nbPmf, poisPmf, nbSample, simulateNb, simulatePoisson, meanOf, varOf, poissonPosterior, nbGrid, logRMedian, ppcCounts } from '../src/bayes/overdisp.js';
import { genLogistic, genZeroInflated, logisticPPC, poissonZerosPPC } from '../src/bayes/glmppc.js';
import { gridPosterior } from '../src/bayes/glm.js';
import { flipSequence } from '../src/bayes/conjugate.js';

const close = (a, b, tol, msg) => assert.ok(Math.abs(a - b) <= tol, `${msg ?? ''} ${a} vs ${b}`);

test('Bayes factor: marginal likelihood chuẩn hóa, khớp Monte Carlo/lưới, Savage–Dickey, hiệu ứng Occam', () => {
  for (const [a, b] of [[1, 1], [2, 2], [10, 10], [0.5, 0.5]]) {
    let s = 0; for (let k = 0; k <= 20; k++) s += marginal1(k, 20, a, b); close(s, 1, 1e-9, 'Σ_k m1');
    close(marginal1(13, 20, a, b), gridMarginal(13, 20, a, b), 2e-4, 'lưới');
    close(marginal1(13, 20, a, b) / mcMarginal(13, 20, a, b, 400000, 3), 1, 0.02, 'MC');
    close(bf10(13, 20, a, b), savageDickey(13, 20, a, b), 1e-9, 'Savage–Dickey');
  }
  close(marginal1(7, 20, 1, 1), 1 / 21, 1e-12, 'Beta(1,1) ⇒ đều trên 0..n');
  assert.ok(bf10(10, 20, 1, 1) < 0.3, 'k=n/2: ủng hộ M0'); assert.ok(bf10(17, 20, 1, 1) > 10, 'k lệch xa: ủng hộ M1');
  assert.ok(bf10(10, 20, 100, 100) > 0.9 && bf10(10, 20, 100, 100) < 1.1, 'prior dồn về θ0 ⇒ BF → 1');
  assert.ok(bf10(10, 20, 1, 1) > bf10(10, 20, 0.2, 0.2) * 0 + 0 && bf10(11, 20, 0.05, 0.05) < bf10(11, 20, 1, 1), 'prior quá rộng bị phạt (Occam)');
  close(postProb1(3, 1), 0.75, 1e-12); close(postProb1(1, 1), 0.5, 1e-12);
  const flips = Array.from({ length: 400 }, (_, i) => (i % 2)), path = bfPath(flips, 1, 1); assert.ok(path.at(-1).log10 < -1, 'dữ liệu θ=0.5: bằng chứng tích lũy cho M0');
  const f7 = flipSequence(0.8, 80, 4), p7 = bfPath(f7, 1, 1); assert.ok(p7.at(-1).log10 > 2, 'θ=0.8: bằng chứng mạnh cho M1');
});

test('đa cộng tuyến: sd(b1) tăng √VIF, tương quan posterior ≈ −ρ, tổng b1+b2 vẫn chính xác', () => {
  const n = 6000, sigma = 1, tau = 1e3, base = posterior(...Object.values(simData({ n, rho: 0, seed: 1 })).slice(0, 3), sigma, tau);
  for (const rho of [0.5, 0.9, 0.99]) {
    const d = simData({ n, rho, seed: 1 }), post = posterior(d.x1, d.x2, d.y, sigma, tau);
    close(post.sd1 / base.sd1, Math.sqrt(vif(rho)), 0.06 * Math.sqrt(vif(rho)), 'sd ratio ρ=' + rho);
    close(post.corr, -rho, 0.03, 'corr'); close(post.sdSum, Math.sqrt((2 * sigma * sigma) / (n * (1 + rho))), 0.05 * post.sdSum, 'sd tổng');
    const ols = olsMulti(d.x1.map((a, i) => [a, d.x2[i]]), d.y).beta; close(post.mean[0], ols[0], 1e-3); close(post.mean[1], ols[1], 1e-3);
  }
  const d = simData({ n: 60, rho: 0.95, seed: 2 }), wide = posterior(d.x1, d.x2, d.y, 1, 100), tight = posterior(d.x1, d.x2, d.y, 1, 0.5);
  assert.ok(tight.sd1 < wide.sd1 && Math.abs(tight.mean[0]) < Math.abs(wide.mean[0]) + 5, 'prior chặt giảm phương sai');
  const dr = sampleBeta(wide, 40000, 3); close(sampleCorr(dr.map((p) => p[0]), dr.map((p) => p[1])), wide.corr, 0.02); close(dr.reduce((s, p) => s + p[0], 0) / dr.length, wide.mean[0], 0.03 * wide.sd1 * 10 + 0.05);
});

test('bias–variance: total = bias² + variance (đồng nhất thức), total + σ² ≈ sai số dữ liệu mới; bias giảm, variance tăng theo bậc', () => {
  const rows = [0, 1, 3, 6, 9].map((d) => { const fits = ensemble(d, { n: 20, tau: 3, R: 150, seed: 2 }), dc = decompose(fits); return { d, fits, ...dc }; });
  rows.forEach((r) => { close(r.bias2 + r.variance, r.total, 1e-9, 'đồng nhất thức d=' + r.d); close(testError(r.fits, 0.3, 20000, 9), r.total + 0.09, 0.04 * (r.total + 0.09) + 0.01, 'test error d=' + r.d); });
  for (let i = 1; i < rows.length; i++) { assert.ok(rows[i].variance > rows[i - 1].variance, 'variance tăng'); }
  assert.ok(rows[0].bias2 > 1.5 * rows[1].bias2 && rows[1].bias2 > 1.5 * rows[2].bias2, 'bias² giảm rõ khi mô hình còn quá đơn giản'); assert.ok(rows[3].bias2 - rows[3].variance / 149 < 0.015 && rows[4].bias2 - rows[4].variance / 149 < 0.015, 'bậc cao: bias² hiệu chỉnh ≈ 0');
  const flat = decompose(ensemble(9, { n: 20, tau: 100, R: 150, seed: 2 })), shrunk = decompose(ensemble(9, { n: 20, tau: 0.5, R: 150, seed: 2 })); assert.ok(shrunk.variance < 0.1 * flat.variance && rows.at(-1).variance < 0.1 * flat.variance, 'prior chặt (ridge) giảm variance mạnh'); assert.ok(shrunk.total < flat.total, 'ridge giảm tổng sai số khi mô hình quá phức tạp');
  const U = rows.map((r) => r.total); assert.ok(Math.min(...U) < U[0] && Math.min(...U) < U.at(-1), 'tổng sai số có dạng chữ U');
});

test('co rút: Gaussian khớp tích phân số, κ của horseshoe ~ Beta(½,½), horseshoe ít co giá trị lớn; MSE thưa tốt nhất', () => {
  for (const y of [-3, 0.5, 2, 6]) { close(gaussianMean(y, 1.5), numericMean(y, (b) => S.normalPdf(b, 0, 1.5)), 1e-6, 'gauss'); }
  // τ = s = 1: κ = 1/(1+λ²), λ ~ C⁺ ⇒ P(κ ≤ c) = 1 − (2/π)·atan(√(1/c − 1)) = Beta(½,½) cdf
  for (const c of [0.05, 0.3, 0.5, 0.8, 0.97]) close(1 - (2 / Math.PI) * Math.atan(Math.sqrt(1 / c - 1)), S.betaCdf(c, 0.5, 0.5), 1e-6, 'κ cdf');
  let prev = 0; for (const y of [0.5, 1, 2, 3, 4, 6, 8]) { const m = horseshoeMean(y, 0.3), l = laplaceMean(y, 0.5), g = gaussianMean(y, 0.3); assert.ok(m >= prev - 1e-9 && m <= y); prev = m; close(horseshoeMean(-y, 0.3), -m, 1e-9, 'đối xứng'); if (y >= 6) { assert.ok(y - m < y - g, 'horseshoe co ít hơn Gaussian với tín hiệu lớn'); assert.ok(y - m < 0.6, 'gần như không co'); } void l; }
  assert.ok(Math.abs(horseshoeMean(0.5, 0.3)) < 0.5 * 0.5, 'tín hiệu nhỏ bị co mạnh về 0');
  const best = (name, scales) => { let b = Infinity; for (const sc of scales) { let t = 0; for (let seed = 1; seed <= 8; seed++) { const d = sparseData({ p: 60, k: 5, big: 6, seed }); t += mse(d.y.map((y) => PRIORS[name](y, sc)), d.beta); } b = Math.min(b, t / 8); } return b; };
  const sc = [0.05, 0.1, 0.2, 0.4, 0.7, 1, 2, 4];
  const mle = best('mle', [1]), g = best('gaussian', sc), l = best('laplace', [0.1, 0.2, 0.4, 0.7, 1, 2]), h = best('horseshoe', sc);
  assert.ok(h < l && l < g && g < mle, `MSE: horseshoe ${h} < laplace ${l} < gaussian ${g} < MLE ${mle}`);
});

test('quá phân tán: NB đúng moment, → Poisson khi r lớn; dự báo Poisson–Gamma = NB; PPC bắt được overdispersion', () => {
  let s = 0, m = 0, v = 0; for (let k = 0; k < 400; k++) { const p = nbPmf(k, 4, 1.5); s += p; m += k * p; v += k * k * p; } close(s, 1, 1e-9); close(m, 4, 1e-6); close(v - m * m, 4 + 16 / 1.5, 1e-4);
  for (let k = 0; k < 12; k++) close(nbPmf(k, 3, 1e6), poisPmf(k, 3), 1e-5, 'r→∞');
  const g = S.mulberry32(5), xs = Array.from({ length: 80000 }, () => nbSample(g, 4, 1.5)); close(meanOf(xs), 4, 0.05); close(varOf(xs), 4 + 16 / 1.5, 0.4);
  const cts = simulatePoisson(50, 3, 2), pp = poissonPosterior(cts, 2, 1);
  for (let k = 0; k < 8; k++) { let q = 0; const N = 40000, hi = 30; for (let i = 0; i < N; i++) { const lam = (i + 0.5) * hi / N; q += poisPmf(k, lam) * S.gammaPdf(lam, pp.a, pp.b) * hi / N; } close(nbPmf(k, pp.mu, pp.r), q, 1e-5, 'predictive k=' + k); }
  const nbData = simulateNb(300, 4, 1.5, 3), po = ppcCounts(nbData, 'poisson', 'ratio', 400, 1), nb = ppcCounts(nbData, 'nb', 'ratio', 400, 1);
  assert.ok(po.p < 0.01 && nb.pTwo > 0.05, `PPC Poisson p=${po.p}, NB p2=${nb.pTwo}`);
  const poData = simulatePoisson(300, 3, 4); assert.ok(ppcCounts(poData, 'poisson', 'ratio', 400, 1).pTwo > 0.05, 'Poisson đúng ⇒ không báo động');
});

test('quá phân tán: posterior của NB hồi phục r; dữ liệu Poisson đẩy r lớn', () => {
  const lr = logRMedian(nbGrid(simulateNb(500, 4, 2, 6))); close(lr, Math.log(2), 0.4, 'log r');
  assert.ok(Math.exp(logRMedian(nbGrid(simulatePoisson(500, 4, 7)))) > 15, 'r lớn ⇒ NB ≈ Poisson');
});

test('PPC cho GLM: mô hình sai bị bắt (logistic thiếu bậc hai, Poisson thiếu số 0 dư), mô hình đúng thì không', () => {
  const ppps = [], bads = [];
  for (let seed = 1; seed <= 10; seed++) {
    const good = genLogistic(400, { c: 0 }, seed), bad = genLogistic(400, { a: 0.4, b: 0.3, c: -1.2 }, seed);
    ppps.push(logisticPPC(good.xs, good.ys, gridPosterior('logistic', good.xs, good.ys, 3, 41), 200, 2).ppp);
    bads.push(logisticPPC(bad.xs, bad.ys, gridPosterior('logistic', bad.xs, bad.ys, 3, 41), 200, 2).ppp);
  }
  const mean = (a) => a.reduce((x, y) => x + y, 0) / a.length;
  assert.ok(mean(ppps) > 0.2 && mean(ppps) < 0.8 && ppps.filter((p) => p < 0.05).length <= 2, 'đúng: ppp trải đều ' + ppps.join(','));
  assert.ok(Math.max(...bads) < 0.02, 'sai: ppp ' + bads.join(','));
  const good = genLogistic(400, { c: 0 }, 5), bad = genLogistic(400, { a: 0.4, b: 0.3, c: -1.2 }, 5);
  const pg = logisticPPC(good.xs, good.ys, gridPosterior('logistic', good.xs, good.ys, 3, 61), 300, 2), pb = logisticPPC(bad.xs, bad.ys, gridPosterior('logistic', bad.xs, bad.ys, 3, 61), 300, 2);
  close(pg.bins.reduce((s, b) => s + b.n, 0), 400, 0, 'đủ điểm');
  const covered = pg.bins.filter((b) => b.obs >= b.lo - 1e-9 && b.obs <= b.hi + 1e-9).length; assert.ok(covered >= pg.bins.length - 2, 'đúng: hầu hết nhóm nằm trong dải 90%');
  const outBad = pb.bins.filter((b) => b.obs < b.lo || b.obs > b.hi).length; assert.ok(outBad >= 2, 'sai: nhiều nhóm lệch khỏi dải');
  const zi = genZeroInflated(300, { pi: 0.35 }, 3), ok = genZeroInflated(300, { pi: 0 }, 3);
  const ppz = []; for (let seed = 1; seed <= 6; seed++) { const o = genZeroInflated(300, { pi: 0 }, seed); ppz.push(poissonZerosPPC(o.xs, o.ys, gridPosterior('poisson', o.xs, o.ys, 3, 41), 300, 2).ppp); } assert.ok(mean(ppz) > 0.2 && mean(ppz) < 0.8, 'Poisson đúng: ' + ppz.join(','));
  const pz = poissonZerosPPC(zi.xs, zi.ys, gridPosterior('poisson', zi.xs, zi.ys, 3, 61), 400, 2), po = poissonZerosPPC(ok.xs, ok.ys, gridPosterior('poisson', ok.xs, ok.ys, 3, 61), 400, 2);
  assert.ok(pz.ppp < 0.01 && po.ppp > 0.0 && po.ppp <= 1, `zero-inflated ppp=${pz.ppp}`);
  close(pz.obsPmf.reduce((a, b) => a + b, 0), 1, 0.02, 'pmf quan sát (K=12)');
});
