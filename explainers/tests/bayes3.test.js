import test from 'node:test';
import assert from 'node:assert/strict';
import * as S from '../src/bayes/stats.js';
import { sineData, design, solve, evalPoly } from '../src/bayes/shrink.js';
import { waic, exactLoo, effectiveParams, analyse, pseudoBma, seDiff } from '../src/bayes/ic.js';
import { eolShip, eolHold, evsi, evpi, expectedLoss, LOSSES, optimal, probBetter, threshold, decide, expectedLosses } from '../src/bayes/decision.js';
import { simulate, gridPosterior, drawGrid, mle, logLik, RANGE } from '../src/bayes/glm.js';
import { SCHOOLS, conditional, logTauPost, tauPosterior, thetaSummary, tauMedian } from '../src/bayes/pool.js';
import { simFork, forkBias, slope, adjustedSlope, simCollider, colliderPartialCorr, partialCorr, corr, simInteraction, fitInteraction, tertiles, strataSlopes } from '../src/bayes/confound.js';
import { simulateT, rejectRate, zPower, powerSim, tStat } from '../src/bayes/pval.js';
import { llBinom, llPoisson, mleBinom, mlePoisson, relLik, likInterval, priorPredictiveBinom, exactPredictiveBinom, nbPmf, priorPredictivePoisson } from '../src/bayes/lik.js';

const close = (a, b, tol, msg) => assert.ok(Math.abs(a - b) <= tol, `${msg ?? ''} ${a} vs ${b}`);

test('digamma và phân phối t khớp giá trị đã biết', () => {
  close(S.digamma(1), -0.5772156649015329, 1e-9); close(S.digamma(0.5), -1.9635100260214235, 1e-8); close(S.digamma(10), 2.251752589066721, 1e-9);
  close(S.tCdf(2.776445, 4), 0.975, 1e-5); close(S.tCdf(2.228139, 10), 0.975, 1e-5);
  for (const t of [-3, -0.7, 0.4, 2]) { close(S.tCdf(t, 1), 0.5 + Math.atan(t) / Math.PI, 1e-9, 'Cauchy'); close(S.tCdf(t, 2), 0.5 + t / (2 * Math.sqrt(2 + t * t)), 1e-9, 'df=2'); }
  let s = 0; for (let i = 0; i < 40000; i++) s += S.tPdf(-20 + (i + 0.5) / 1000, 5) / 1000; close(s, 1, 1e-3);
});

test('WAIC ≈ LOO chính xác; lppd lạc quan hơn LOO; p_waic ≈ tham số hiệu dụng khi mô hình đúng, lớn hơn khi sai', () => {
  const { xs, ys } = sineData(20, 0.3, 3), sigma = 0.3, tau = 3;
  for (const d of [1, 3, 5]) {
    const w = waic(xs, ys, d, sigma, tau, 8000, 7), loo = exactLoo(xs, ys, d, sigma, tau), looSum = loo.reduce((a, b) => a + b, 0);
    close(w.elpd, looSum, 0.06 * Math.abs(looSum) + 0.6, `elpd d=${d}`);
    assert.ok(w.lppdSum > looSum, 'in-sample lppd phải lớn hơn out-of-sample');
  }
  // mô hình đúng: dữ liệu sinh từ đa thức bậc 2
  const r = S.mulberry32(21), px = Array.from({ length: 60 }, () => -1 + 2 * r()), py = px.map((x) => 0.5 - x + 1.5 * x * x + 0.3 * S.randn(r));
  // p_waic,i ≈ r_i²·v_i/σ⁴ + v_i²/(2σ⁴) với v_i = xᵢᵀP⁻¹xᵢ (khai triển bậc hai quanh posterior mean)
  const approx = (X, Y, d) => { const w = waic(X, Y, d, 0.3, 3, 20000, 7), P = w.fit.P; let t = 0; X.forEach((x, i) => { const row = design([x], d)[0], v = row.reduce((q, rv, k) => q + rv * solve(P, row)[k], 0), res = Y[i] - evalPoly(w.fit.w, x); t += res * res * v / 0.3 ** 4 + v * v / (2 * 0.3 ** 4); }); return [w.pSum, t, w]; };
  for (const d of [2, 3]) { const [got, want, w] = approx(px, py, d); close(got, want, 0.04 * want, `p_waic d=${d}`); close(got, effectiveParams(px, d, 0.3, 3), 0.4 * effectiveParams(px, d, 0.3, 3), 'cùng bậc với p_eff'); close(w.pSum, got, 0, 'ổn định'); }
  // mô hình sai (sine ~ đường thẳng): p_waic vượt số tham số hiệu dụng vì phần dư lớn
  const bad = waic(xs, ys, 1, sigma, tau, 8000, 7); assert.ok(bad.pSum > 2 * effectiveParams(xs, 1, sigma, tau));
});

test('chọn mô hình: elpd_loo cao nhất ở bậc vừa phải, không phải bậc cao nhất; trọng số pseudo-BMA', () => {
  const { xs, ys } = sineData(20, 0.3, 3), test_ = sineData(400, 0.3, 99);
  const M = Array.from({ length: 9 }, (_, d) => analyse(xs, ys, d, 0.3, 3, test_, 300, 5));
  const best = M.reduce((b, m) => (m.looSum > b.looSum ? m : b));
  assert.ok(best.d >= 3 && best.d <= 7, 'best d=' + best.d);
  assert.ok(M[0].looSum < best.looSum - 3 && M[0].test < M[best.d].test, 'bậc 0 underfit');
  assert.ok(M[8].lppdSum > M[3].lppdSum, 'lppd tăng theo độ phức tạp');
  const w = pseudoBma(M.map((m) => m.looSum)); close(w.reduce((a, b) => a + b), 1, 1e-12); assert.equal(w.indexOf(Math.max(...w)), best.d);
  assert.ok(seDiff(M[3].loo, M[3].loo) === 0 && seDiff(M[0].loo, M[3].loo) > 0);
});

test('mất mát kỳ vọng dạng đóng khớp tích phân số; EVSI ≥ 0, đơn điệu, hội tụ về EVPI', () => {
  for (const [a, b, p0] of [[13, 91, 0.1], [2, 3, 0.5], [30, 270, 0.12]]) {
    close(eolShip(a, b, p0), expectedLoss(a, b, (p) => Math.max(0, p0 - p), 0, 1, 20000), 2e-6, 'ship');
    close(eolHold(a, b, p0), expectedLoss(a, b, (p) => Math.max(0, p - p0), 0, 1, 20000), 2e-6, 'hold');
    // E[p - p0] = hold - ship
    close(eolHold(a, b, p0) - eolShip(a, b, p0), a / (a + b) - p0, 1e-9, 'identity');
  }
  const a = 13, b = 91, p0 = 0.1;
  let prev = 0; for (const m of [10, 50, 200, 800]) { const v = evsi(a, b, p0, m); assert.ok(v >= -1e-12 && v >= prev - 1e-12 && v <= evpi(a, b, p0) + 1e-12, 'm=' + m); prev = v; }
  close(evsi(a, b, p0, 6000) / evpi(a, b, p0), 1, 0.03, 'EVSI → EVPI');
  // EVSI so với Monte Carlo
  const r = S.mulberry32(5); let acc = 0; const R = 20000, m = 100;
  for (let i = 0; i < R; i++) { const p = S.betaSample(r, a, b), y = S.binomialSample(r, m, p); acc += Math.min(eolShip(a + y, b + m - y, p0), eolHold(a + y, b + m - y, p0)); }
  close(evpi(a, b, p0) - acc / R, evsi(a, b, p0, m), 0.0004, 'EVSI MC');
});

test('quy tắc ngưỡng và điểm tóm tắt tối ưu theo từng loss', () => {
  close(threshold(1, 3), 0.25, 1e-12); assert.equal(decide(0.3, 1, 3), 'ship'); assert.equal(decide(0.2, 1, 3), 'hold');
  const l = expectedLosses(0.25, 1, 3); close(l.ship, l.hold, 1e-12, 'bằng nhau tại ngưỡng');
  close(probBetter(13, 91, 0.1), 1 - S.betaCdf(0.1, 13, 91), 1e-12);
  const a = 8, b = 4, grid = Array.from({ length: 999 }, (_, i) => (i + 1) / 1000);
  for (const k of ['squared', 'absolute', 'zeroOne', 'pinball']) {
    let best = 0, bv = Infinity; for (const c of grid) { const v = expectedLoss(a, b, LOSSES[k](c), 0, 1, 1500); if (v < bv) { bv = v; best = c; } }
    close(best, optimal[k](a, b), 0.01, k);
  }
});

test('GLM trên lưới: posterior nhị phân khớp công thức đóng (digamma)', () => {
  // logistic, x ∈ {0,1}; prior phẳng trên logit ⇒ p ~ Beta(k, n−k), E[logit p] = ψ(k) − ψ(n−k)
  const n0 = 100, k0 = 30, n1 = 80, k1 = 48, xs = [], ys = [];
  for (let i = 0; i < n0; i++) { xs.push(0); ys.push(i < k0 ? 1 : 0); } for (let i = 0; i < n1; i++) { xs.push(1); ys.push(i < k1 ? 1 : 0); }
  const post = gridPosterior('logistic', xs, ys, 100, 121), ea = S.digamma(k0) - S.digamma(n0 - k0), eb = S.digamma(k1) - S.digamma(n1 - k1) - ea;
  close(post.meanA, ea, 0.03, 'E[a]'); close(post.meanB, eb, 0.05, 'E[b]');
  close(post.P.reduce((a, b) => a + b, 0), 1, 1e-9, 'chuẩn hóa');
  // poisson: prior phẳng trên log λ ⇒ λ ~ Gamma(Σy, n), E[log λ] = ψ(Σy) − log n
  const c0 = [1, 3, 2, 2, 4, 1, 2, 3, 2, 2, 1, 3], c1 = [3, 4, 2, 5, 3, 3, 4, 2, 3, 4, 3, 3], sx = [...c0.map(() => 0), ...c1.map(() => 1)], sy = [...c0, ...c1];
  const S0 = c0.reduce((a, b) => a + b), S1 = c1.reduce((a, b) => a + b), pp = gridPosterior('poisson', sx, sy, 100, 141);
  const ea2 = S.digamma(S0) - Math.log(c0.length), eb2 = S.digamma(S1) - Math.log(c1.length) - ea2;
  close(pp.meanA, ea2, 0.03, 'poisson E[a]'); close(pp.meanB, eb2, 0.04, 'poisson E[b]');
});

test('GLM: mode posterior (prior rất rộng) ≈ MLE (Newton); mẫu từ lưới khớp moment lưới', () => {
  for (const kind of ['logistic', 'poisson']) {
    const { xs, ys } = simulate(kind, 300, ...RANGE[kind].truth, 11), m = mle(kind, xs, ys);
    const best = [m.a, m.b], eps = 1e-4;
    // gradient của loglik bằng 0 tại MLE
    const g = (da, db) => (logLik(kind, xs, ys, m.a + da, m.b + db) - logLik(kind, xs, ys, m.a - da, m.b - db)) / (2 * eps);
    close(g(eps, 0), 0, 1e-3, 'dL/da'); close(g(0, eps), 0, 1e-3, 'dL/db');
    const post = gridPosterior(kind, xs, ys, 100, 121); let mx = 0, mi = 0; post.P.forEach((v, i) => { if (v > mx) { mx = v; mi = i; } });
    close(post.as[Math.floor(mi / 121)], best[0], 2 * post.da, kind + ' a'); close(post.bs[mi % 121], best[1], 2 * post.db, kind + ' b');
    const dr = drawGrid(post, 6000, 3), ma = dr.reduce((s, d) => s + d.a, 0) / dr.length, mb = dr.reduce((s, d) => s + d.b, 0) / dr.length;
    close(ma, post.meanA, 0.02, 'draw mean a'); close(mb, post.meanB, 0.02, 'draw mean b');
  }
});

test('phân cấp: giới hạn τ→0 (gộp hoàn toàn) và τ→∞ (không gộp), khớp tích phân số của μ', () => {
  const { y, s } = SCHOOLS;
  const c0 = conditional(y, s, 1e-6), W = s.reduce((a, sj) => a + 1 / (sj * sj), 0), mu = y.reduce((a, yj, j) => a + yj / (s[j] * s[j]), 0) / W;
  c0.theta.forEach((t) => close(t.mean, mu, 1e-6, 'complete pooling')); close(mu, 7.685, 0.01, 'trung bình trọng số 8 trường');
  const c1 = conditional(y, s, 1e6); c1.theta.forEach((t, j) => close(t.mean, y[j], 1e-3, 'no pooling'));
  // log p(τ|y) so với tích phân số của μ (lưới mịn)
  const marg = (tau) => { let a = 0; for (let i = 0; i < 40000; i++) { const mu_ = -60 + i * 0.005; a += Math.exp(y.reduce((l, yj, j) => l + Math.log(S.normalPdf(yj, mu_, Math.sqrt(s[j] ** 2 + tau * tau))), 0)) * 0.005; } return a; };
  for (const [t1, t2] of [[2, 8], [5, 20]]) close(logTauPost(y, s, t1) - logTauPost(y, s, t2), Math.log(marg(t1) / marg(t2)), 1e-4, 'marginal τ');
  // hệ số co: B_j = σ²/(σ²+τ²) và mean = (1−B)y + Bμ̂
  const c = conditional(y, s, 5); close(c.theta[0].B, 225 / 250, 1e-12); close(c.theta[0].mean, (1 - 0.9) * 28 + 0.9 * c.muHat, 1e-12);
});

test('phân cấp: posterior của τ chuẩn hóa; trung bình θ_j (RB) khớp mẫu Monte Carlo; co về giữa', () => {
  const { y, s } = SCHOOLS, post = tauPosterior(y, s, 60, 1201); close(post.p.reduce((a, b) => a + b), 1, 1e-9);
  const sum = thetaSummary(y, s, post);
  const r = S.mulberry32(9), cum = []; let a = 0; post.p.forEach((p) => { a += p; cum.push(a); });
  const R = 40000, acc = new Array(8).fill(0);
  for (let i = 0; i < R; i++) { const u = r(), k = cum.findIndex((c) => c >= u), t = post.taus[k], c = conditional(y, s, t), mu = c.muHat + Math.sqrt(c.Vmu) * S.randn(r); y.forEach((yj, j) => { const B = c.theta[j].B, v = (1 - B) * s[j] * s[j]; acc[j] += (1 - B) * yj + B * mu + Math.sqrt(v) * S.randn(r); }); }
  sum.forEach((t, j) => close(acc[j] / R, t.mean, 0.25, 'MC θ_' + j));
  sum.forEach((t, j) => assert.ok(Math.abs(t.mean - 7.7) < Math.abs(y[j] - 7.7) + 1e-9, 'co về trung bình'));
  assert.ok(sum[0].mean > 8 && sum[0].mean < 13 && tauMedian(post) > 2 && tauMedian(post) < 9);
});

test('confounding: ước lượng ngây thơ lệch δγ/(γ²+1), hiệu chỉnh Z phục hồi β; Simpson trong từng tầng', () => {
  const { x, y, z } = simFork({ n: 60000, gamma: 1, beta: 0.5, delta: 1.5, seed: 4 });
  close(slope(x, y), 0.5 + forkBias(1, 1.5), 0.03, 'naive'); close(adjustedSlope(x, y, z), 0.5, 0.02, 'adjusted');
  // Simpson: β âm nhưng ước lượng ngây thơ dương
  const sp = simFork({ n: 40000, gamma: 1.5, beta: -0.4, delta: 2, seed: 5 });
  assert.ok(slope(sp.x, sp.y) > 0.3 && adjustedSlope(sp.x, sp.y, sp.z) < -0.3);
  const naive = slope(sp.x, sp.y); strataSlopes(sp.x, sp.y, tertiles(sp.z)).forEach((v) => assert.ok(v < 0.4 * naive, 'phân tầng giảm mạnh độ lệch ' + v + ' vs ' + naive));
});

test('collider: độc lập, nhưng điều kiện theo C tạo tương quan −1/(1+σe²)', () => {
  for (const se of [0.3, 1]) {
    const { x, y, c } = simCollider({ n: 150000, se, seed: 6 });
    close(corr(x, y), 0, 0.01, 'không điều kiện'); close(partialCorr(x, y, c), colliderPartialCorr(se), 0.01, 'điều kiện C se=' + se);
  }
});

test('interaction: OLS phục hồi hệ số; mô hình tương tác giảm RSS; khi b3=0 thì không cải thiện nhiều', () => {
  const d = simInteraction({ n: 20000, b0: 1, b1: 0.5, b2: 0.5, b3: 1, sigma: 0.6, seed: 8 }), f = fitInteraction(d.x, d.g, d.y);
  [1, 0.5, 0.5, 1].forEach((v, i) => close(f.inter.beta[i], v, 0.03, 'β' + i));
  assert.ok(f.inter.rss < f.additive.rss * 0.7 && f.additive.rss <= f.pooled.rss + 1e-9);
  close(f.inter.rss / 20000, 0.36, 0.02, 'σ̂² ≈ 0.36');
  const d0 = simInteraction({ n: 20000, b3: 0, seed: 8 }), f0 = fitInteraction(d0.x, d0.g, d0.y); close(f0.inter.rss / f0.additive.rss, 1, 0.005);
});

test('p-value: đều dưới H0, tỉ lệ bác bỏ ≈ α; đuôi t dày hơn chuẩn; công suất khớp xấp xỉ z', () => {
  const sim = simulateT({ n: 5, d: 0, reps: 20000, seed: 2 });
  close(rejectRate(sim.p), 0.05, 0.007, 'α'); close(sim.p.filter((p) => p < 0.5).length / 20000, 0.5, 0.012, 'P(p<.5)'); close(sim.p.filter((p) => p < 0.1).length / 20000, 0.1, 0.008);
  close(sim.t.filter((t) => Math.abs(t) > 2.776445).length / 20000, 0.05, 0.007, 'đuôi t df=4');
  assert.ok(sim.t.filter((t) => Math.abs(t) > 2.776445).length / 20000 > 5 * (2 * (1 - S.normalCdf(2.776445))), 'đuôi chuẩn mỏng hơn nhiều');
  close(powerSim(50, 0.4, 3000, 3), zPower(50, 0.4), 0.04, 'power n=50'); close(zPower(10, 0), 0.05, 1e-4);
  assert.ok(powerSim(20, 0.5, 1500, 4) < powerSim(80, 0.5, 1500, 4) && powerSim(40, 0.2, 1500, 5) < powerSim(40, 0.8, 1500, 5));
  close(tStat([1, 2, 3, 4, 5]), 3 / (Math.sqrt(2.5) / Math.sqrt(5)), 1e-12);
});

test('likelihood: MLE, cộng tính theo quan sát, khoảng likelihood; prior predictive khớp công thức đóng', () => {
  close(mleBinom(7, 10), 0.7, 1e-12); close(mlePoisson([2, 3, 4]), 3, 1e-12);
  const ll = (t) => llBinom(7, 10, t); for (const t of [0.2, 0.5, 0.9]) assert.ok(ll(t) < ll(0.7));
  close(llBinom(3, 4, 0.6) + llBinom(5, 6, 0.6), llBinom(8, 10, 0.6) , 0, 'cộng tính theo nhóm (cùng hệ số tổ hợp bị bỏ)');
  const c = [2, 3, 1, 4]; close(llPoisson(c, 2.5), c.reduce((s, y) => s + llPoisson([y], 2.5), 0), 1e-12);
  const [L, U] = likInterval((t) => llBinom(70, 100, t), 0.7, 0, 1); close(Math.exp(llBinom(70, 100, L) - llBinom(70, 100, 0.7)), Math.exp(-1.92), 1e-6); close(Math.exp(llBinom(70, 100, U) - llBinom(70, 100, 0.7)), Math.exp(-1.92), 1e-6);
  close((L + U) / 2, 0.7, 0.01); assert.ok(U - L > 0.15 && U - L < 0.22);
  assert.equal(relLik(ll, 0.7, 0, 1, 100).length, 101);
  for (const [a, b] of [[1, 1], [2, 2], [8, 2], [0.5, 0.5]]) {
    const emp = priorPredictiveBinom(a, b, 10, 200000, 3), ex = exactPredictiveBinom(a, b, 10);
    close(ex.reduce((x, y) => x + y), 1, 1e-9); emp.forEach((v, k) => close(v, ex[k], 0.006, `Beta(${a},${b}) k=${k}`));
  }
  close(exactPredictiveBinom(1, 1, 10)[3], 1 / 11, 1e-12, 'Beta(1,1) ⇒ đều trên 0..n');
  let tot = 0; for (let k = 0; k < 400; k++) tot += nbPmf(k, 3, 1); close(tot, 1, 1e-9);
  const emp = priorPredictivePoisson(3, 1, 12, 200000, 4); emp.forEach((v, k) => close(v, nbPmf(k, 3, 1), 0.005, 'NB k=' + k));
});
