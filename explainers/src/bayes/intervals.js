// Khoảng tin cậy (confidence) và khoảng đáng tin (credible): mô phỏng độ phủ.
import { mulberry32, randn, normalQuantile } from './stats.js';
import { normalNormal } from './conjugate.js';

/** Mỗi lần lặp: lấy n quan sát từ N(mu, σ²) (σ biết); tính CI chuẩn và credible interval với prior N(mu0, tau0²). */
export function coverageSim({ mu = 0, sigma = 1, n = 10, reps = 100, mu0 = 0, tau0 = 1, level = 0.95, seed = 1, thetaFromPrior = false }) {
  const r = mulberry32(seed), z = normalQuantile(0.5 + level / 2), rows = []; let ci = 0, cr = 0;
  for (let i = 0; i < reps; i++) {
    const theta = thetaFromPrior ? mu0 + tau0 * randn(r) : mu;
    let sum = 0; const xs = []; for (let j = 0; j < n; j++) { const x = theta + sigma * randn(r); xs.push(x); sum += x; }
    const xbar = sum / n, half = z * sigma / Math.sqrt(n), conf = [xbar - half, xbar + half];
    const post = normalNormal(mu0, tau0, sigma, xs), cred = [post.mu - z * post.sd, post.mu + z * post.sd];
    const okC = conf[0] <= theta && theta <= conf[1], okB = cred[0] <= theta && theta <= cred[1];
    if (okC) ci++; if (okB) cr++;
    rows.push({ theta, xbar, conf, cred, okC, okB });
  }
  return { rows, confCoverage: ci / reps, credCoverage: cr / reps };
}
