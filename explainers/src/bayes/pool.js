// Mô hình phân cấp chuẩn–chuẩn (BDA §5.4): y_j ~ N(θ_j, σ_j²), θ_j ~ N(μ, τ²), prior phẳng trên μ và τ.
export const SCHOOLS = { y: [28, 8, -3, 7, -1, 1, 18, 12], s: [15, 10, 16, 11, 9, 11, 10, 18], names: ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H'] };
export const EQUAL = { y: [12, 5, -4, 9, 1, -7, 15, 3], s: [8, 8, 8, 8, 8, 8, 8, 8], names: ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H'] };

/** Với τ cố định: μ̂(τ), Var(μ|τ,y) và posterior của từng θ_j (trung bình, phương sai, hệ số co B_j). */
export function conditional(y, s, tau) {
  const w = s.map((sj) => 1 / (sj * sj + tau * tau)), W = w.reduce((a, b) => a + b, 0), muHat = w.reduce((a, wj, j) => a + wj * y[j], 0) / W, Vmu = 1 / W;
  const theta = y.map((yj, j) => { const B = (s[j] * s[j]) / (s[j] * s[j] + tau * tau); return { B, mean: (1 - B) * yj + B * muHat, v: (1 - B) * s[j] * s[j] + B * B * Vmu }; });
  return { muHat, Vmu, theta };
}
/** log p(τ | y) (chưa chuẩn hóa) dưới prior phẳng trên τ. */
export function logTauPost(y, s, tau) {
  const { muHat, Vmu } = conditional(y, s, tau);
  let l = 0.5 * Math.log(Vmu);
  y.forEach((yj, j) => { const v = s[j] * s[j] + tau * tau; l += -0.5 * Math.log(v) - 0.5 * (yj - muHat) ** 2 / v; });
  return l;
}
export function tauPosterior(y, s, tmax = 40, N = 801) {
  const taus = Array.from({ length: N }, (_, i) => (tmax * i) / (N - 1)), lp = taus.map((t) => logTauPost(y, s, t)), mx = Math.max(...lp), q = lp.map((v) => Math.exp(v - mx)), Z = q.reduce((a, b) => a + b, 0);
  return { taus, p: q.map((v) => v / Z), dt: taus[1] - taus[0] };
}
/** E[θ_j | y] và SD, lấy trung bình theo p(τ|y) (Rao–Blackwell). */
export function thetaSummary(y, s, post = tauPosterior(y, s)) {
  const J = y.length, m = new Array(J).fill(0), m2 = new Array(J).fill(0);
  post.taus.forEach((t, i) => { const c = conditional(y, s, t); c.theta.forEach((th, j) => { m[j] += post.p[i] * th.mean; m2[j] += post.p[i] * (th.v + th.mean ** 2); }); });
  return m.map((mj, j) => ({ mean: mj, sd: Math.sqrt(m2[j] - mj * mj) }));
}
export const tauMedian = (post) => { let c = 0; for (let i = 0; i < post.taus.length; i++) { c += post.p[i]; if (c >= 0.5) return post.taus[i]; } return post.taus.at(-1); };
