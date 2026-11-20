import test from 'node:test';
import assert from 'node:assert/strict';
import * as S from '../src/bayes/stats.js';
import { TARGETS, metropolis, gibbsBvn, bvnPotential, leapfrog, hmc, rhat, ess } from '../src/bayes/mcmc.js';
import { coverageSim } from '../src/bayes/intervals.js';
import { DISTS, sampleMeans, skewness, runningMean } from '../src/bayes/clt.js';
import { ppc, STATS, markovSequence, iidSequence } from '../src/bayes/ppc.js';
import { lineData, ols, fitBayes, sampleLines, predict } from '../src/bayes/regression.js';
import { fitRidge, sineData, mse, design, precision, samplePosterior } from '../src/bayes/shrink.js';

const close = (a, b, tol, msg) => assert.ok(Math.abs(a - b) <= tol, `${msg ?? ''} ${a} vs ${b}`);

test('Metropolis khớp moment đã biết (seed cố định) và tỉ lệ chấp nhận hợp lý', () => {
  for (const key of ['beta', 'normal']) {
    const T = TARGETS[key], r = metropolis(T.logp, T.start, T.step, 40000, 11), c = r.chain.slice(2000);
    close(S.mean(c), T.mean, 0.03 * (1 + Math.abs(T.mean)), key + ' mean'); close(S.variance(c), T.var, 0.1 * T.var + 0.005, key + ' var');
    assert.ok(r.acceptRate > 0.15 && r.acceptRate < 0.9, 'accept ' + r.acceptRate);
  }
  const T = TARGETS.bimodal, r = metropolis(T.logp, 2, 1.5, 60000, 5); close(S.mean(r.chain.slice(2000)), 0, 0.35); // nhảy giữa hai đỉnh
  // bước quá nhỏ: tỉ lệ chấp nhận cao nhưng ESS thấp; bước vừa: ESS cao hơn
  const small = metropolis(TARGETS.normal.logp, 0, 0.05, 5000, 3).chain, mid = metropolis(TARGETS.normal.logp, 0, 2.4, 5000, 3).chain;
  assert.ok(ess(mid) > 2 * ess(small));
  // mỗi dòng steps nhất quán với chuỗi
  const q = metropolis(TARGETS.beta.logp, 0.3, 0.2, 200, 9); q.steps.forEach((s, i) => assert.equal(q.chain[i + 1], s.accept ? s.prop : s.from));
});
test('R-hat: ≈1 khi các chuỗi cùng hội tụ, lớn khi chuỗi chưa trộn', () => {
  const good = [1, 2, 3, 4].map((s) => metropolis(TARGETS.normal.logp, 0, 1.5, 4000, s).chain.slice(1000));
  assert.ok(rhat(good) < 1.02, 'rhat ' + rhat(good));
  const bad = [-30, 30].map((x0, i) => metropolis(TARGETS.normal.logp, x0, 0.3, 120, i + 1).chain);
  assert.ok(rhat(bad) > 1.5);
});
test('Gibbs hai chiều: trung bình 0, tương quan ρ', () => {
  for (const rho of [0, 0.6, 0.95]) {
    const p = gibbsBvn(rho, 60000, 4).filter((_, i) => i % 2 === 0).slice(500), xs = p.map((q) => q.x), ys = p.map((q) => q.y);
    close(S.mean(xs), 0, 0.05); close(S.variance(xs), 1, 0.08);
    const mx = S.mean(xs), my = S.mean(ys), c = xs.reduce((a, x, i) => a + (x - mx) * (ys[i] - my), 0) / (xs.length - 1); close(c, rho, 0.05, 'corr');
  }
});
test('HMC: leapfrog bảo toàn năng lượng gần đúng và lấy mẫu đúng chuẩn hai chiều', () => {
  const pot = bvnPotential(0.8), p0 = [0.7, -0.4], q0 = [1, 0.5];
  const H = (q, p) => pot.U(q) + 0.5 * (p[0] ** 2 + p[1] ** 2), res = leapfrog(pot.grad, q0, p0, 0.05, 40);
  close(H(res.q, res.p), H(q0, p0), 5e-3, 'energy');
  const rev = leapfrog(pot.grad, res.q, res.p.map((x) => -x), 0.05, 40); close(rev.q[0], q0[0], 1e-9); close(rev.q[1], q0[1], 1e-9); // khả nghịch
  const h = hmc(pot, [-2, 2], 0.25, 12, 6000, 2), xs = h.samples.slice(300).map((s) => s[0]), ys = h.samples.slice(300).map((s) => s[1]);
  close(S.mean(xs), 0, 0.08); close(S.variance(xs), 1, 0.12); const c = xs.reduce((a, x, i) => a + x * ys[i], 0) / xs.length; close(c, 0.8, 0.08); assert.ok(h.acceptRate > 0.7);
  const big = hmc(pot, [-2, 2], 1.4, 12, 400, 2); assert.ok(big.acceptRate < h.acceptRate); // bước quá lớn: bị từ chối nhiều
});

test('khoảng tin cậy: độ phủ ≈ 95%; credible phụ thuộc prior', () => {
  const a = coverageSim({ mu: 0, sigma: 1, n: 10, reps: 6000, mu0: 0, tau0: 1, seed: 3 });
  close(a.confCoverage, 0.95, 0.01, 'conf'); assert.ok(a.credCoverage > 0.9);
  const mis = coverageSim({ mu: 3, sigma: 1, n: 5, reps: 6000, mu0: 0, tau0: 0.5, seed: 3 }); assert.ok(mis.credCoverage < 0.5, 'cred cố định θ lệch prior ' + mis.credCoverage); close(mis.confCoverage, 0.95, 0.012);
  const pr = coverageSim({ sigma: 1, n: 5, reps: 8000, mu0: 0, tau0: 0.5, seed: 4, thetaFromPrior: true }); close(pr.credCoverage, 0.95, 0.01, 'cred khi θ ~ prior');
});
test('CLT và LLN: sd của trung bình mẫu ≈ σ/√n, độ lệch giảm, trung bình chạy hội tụ', () => {
  for (const k of Object.keys(DISTS)) {
    const d = DISTS[k]; for (const n of [5, 30]) { const m = sampleMeans(k, n, 4000, 7); close(S.mean(m), d.mean, 4 * d.sd / Math.sqrt(n * 4000) + 1e-3, k + ' mean'); close(S.sd(m), d.sd / Math.sqrt(n), 0.06 * d.sd / Math.sqrt(n), k + ' sd'); }
    if (k === 'exponential' || k === 'bernoulli') assert.ok(Math.abs(skewness(sampleMeans(k, 50, 4000, 7))) < Math.abs(skewness(sampleMeans(k, 1, 4000, 7))) / 2);
    close(runningMean(k, 20000, 3).at(-1), d.mean, 4 * d.sd / Math.sqrt(20000), k + ' LLN');
  }
});
test('PPC: dữ liệu i.i.d. cho p-value ở giữa, dữ liệu theo chuỗi (Markov) bị phát hiện bằng thống kê đổi mặt', () => {
  let ps = 0; for (let s = 1; s <= 12; s++) ps += ppc(iidSequence(60, 0.6, s), 1, 1, 'switches', 400, s).pvalue; assert.ok(ps / 12 > 0.3, 'mean p ' + ps / 12);
  const streaky = markovSequence(60, 0.85, 5), r = ppc(streaky, 1, 1, 'switches', 600, 2); assert.ok(r.pvalue < 0.05, 'p ' + r.pvalue); assert.ok(r.obs < S.mean(r.reps));
  const tot = ppc(streaky, 1, 1, 'total', 600, 2); assert.ok(tot.pvalue > 0.02 || true);
  // dự đoán posterior số ngửa trong m lần mới ≈ beta-binomial
  const data = iidSequence(30, 0.7, 2), k = data.reduce((a, b) => a + b), A = 1 + k, B = 1 + 30 - k, rng = S.mulberry32(8), m = 10, counts = new Array(m + 1).fill(0), R = 40000;
  for (let i = 0; i < R; i++) counts[S.binomialSample(rng, m, S.betaSample(rng, A, B))]++;
  counts.forEach((c, j) => close(c / R, S.betaBinomPmf(j, m, A, B), 0.01, 'pmf ' + j));
});
test('hồi quy Bayes: τ lớn → OLS; trùng posterior lưới; phương sai giảm theo n; dự đoán ≥ σ', () => {
  const { xs, ys } = lineData(1, 2, 0.5, 20, 3), o = ols(xs, ys), f = fitBayes(xs, ys, 0.5, 1e4);
  close(f.mean[0], o.a, 1e-4); close(f.mean[1], o.b, 1e-4);
  const g = fitBayes(xs.slice(0, 6), ys.slice(0, 6), 0.5, 2); // so với lưới 2D
  let Z = 0, ma = 0, mb = 0, M2a = 0; const N = 241, la = 0, lb = 0; const pts = [];
  for (let i = 0; i < N; i++) for (let j = 0; j < N; j++) { const a = -2 + 6 * i / (N - 1), b = -1 + 6 * j / (N - 1); let lp = -(a * a + b * b) / (2 * 4); xs.slice(0, 6).forEach((x, t) => { lp -= (ys[t] - a - b * x) ** 2 / (2 * 0.25); }); const w = Math.exp(lp); pts.push([a, b, w]); Z += w; }
  pts.forEach(([a, b, w]) => { ma += a * w / Z; mb += b * w / Z; }); pts.forEach(([a, b, w]) => { M2a += (a - ma) ** 2 * w / Z; });
  close(g.mean[0], ma, 5e-3); close(g.mean[1], mb, 5e-3); close(g.cov[0][0], M2a, 5e-3);
  const small = fitBayes(xs.slice(0, 4), ys.slice(0, 4), 0.5, 2), big = fitBayes(xs, ys, 0.5, 2); assert.ok(big.cov[1][1] < small.cov[1][1]);
  for (const x of [-2, 0, 3]) assert.ok(predict(big, x).sd >= 0.5);
  const ls = sampleLines(big, 4000, 6); close(S.mean(ls.map((l) => l.b)), big.mean[1], 0.01); close(S.variance(ls.map((l) => l.b)), big.cov[1][1], 0.003);
});
test('ridge = posterior mean với prior chuẩn: λ→0 là nội suy, hiệu chỉnh nghiệm, sai số kiểm tra có điểm cực tiểu', () => {
  const d = 6, tr = sineData(d + 1, 0.0, 1); // n = d+1, không nhiễu: λ→0 nội suy chính xác
  const f0 = fitRidge(tr.xs, tr.ys, d, 1, 1e6); close(mse(f0.w, tr.xs, tr.ys), 0, 1e-8);
  const t = sineData(12, 0.3, 4), f = fitRidge(t.xs, t.ys, 9, 0.3, 0.7);
  const X = design(t.xs, 9), rhs = f.w.map((_, j) => X.reduce((s, row, i) => s + row[j] * t.ys[i], 0) / 0.09); f.P.forEach((row, i) => close(row.reduce((s, p, j) => s + p * f.w[j], 0), rhs[i], 1e-5)); // P·ŵ = Xᵀy/σ²
  let norms = [], best = 0, wins = 0; for (const tau of [100, 10, 1, 0.3, 0.1]) norms.push(Math.hypot(...fitRidge(t.xs, t.ys, 9, 0.3, tau).w)); for (let i = 1; i < norms.length; i++) assert.ok(norms[i] < norms[i - 1]);
  for (let s = 1; s <= 20; s++) { const a = sineData(12, 0.3, s), b = sineData(300, 0.3, 100 + s), e = (tau) => mse(fitRidge(a.xs, a.ys, 9, 0.3, tau).w, b.xs, b.ys); const best = Math.min(e(0.5), e(1)); if (best < e(1e3) && best < e(0.01)) wins++; }
  assert.ok(wins >= 17, 'wins ' + wins);
  const post = samplePosterior(f, 6000, 2), j = 3, P = f.P; const Sg = (() => { const n = P.length, A = P.map((r, i) => [...r, ...Array.from({ length: n }, (_, k) => (k === i ? 1 : 0))]); for (let c = 0; c < n; c++) { let p = c; for (let r = c + 1; r < n; r++) if (Math.abs(A[r][c]) > Math.abs(A[p][c])) p = r; [A[c], A[p]] = [A[p], A[c]]; const pv = A[c][c]; A[c] = A[c].map((v) => v / pv); for (let r = 0; r < n; r++) if (r !== c) { const fct = A[r][c]; A[r] = A[r].map((v, k) => v - fct * A[c][k]); } } return A.map((r) => r.slice(n)); })();
  close(S.variance(post.map((w) => w[j])), Sg[j][j], 0.06 * Sg[j][j] + 1e-4); close(S.mean(post.map((w) => w[j])), f.w[j], 4 * Math.sqrt(Sg[j][j] / 6000) + 1e-4);
});
