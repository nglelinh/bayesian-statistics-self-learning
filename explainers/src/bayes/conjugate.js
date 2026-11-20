// Cập nhật liên hợp (Beta–Binomial, Gamma–Poisson, Normal–Normal) và đối chứng bằng lưới.
import { betaQuantile, gammaQuantile, normalQuantile, betaPdf, gammaPdf, normalPdf, mulberry32, randn, gammaSample, poissonSample } from './stats.js';

export function betaBinomial(a, b, k, n) {
  const A = a + k, B = b + n - k;
  return { a: A, b: B, mean: A / (A + B), mode: A > 1 && B > 1 ? (A - 1) / (A + B - 2) : null, var: (A * B) / ((A + B) ** 2 * (A + B + 1)), ci: [betaQuantile(0.025, A, B), betaQuantile(0.975, A, B)], pdf: (x) => betaPdf(x, A, B) };
}
/** Dãy cập nhật từng lần tung (flips: mảng 0/1). path[i] = posterior sau i lần. */
export function betaPath(a, b, flips) {
  const path = [{ a, b, k: 0, n: 0 }]; let k = 0;
  flips.forEach((f, i) => { k += f; path.push({ a: a + k, b: b + (i + 1) - k, k, n: i + 1 }); });
  return path;
}
export function flipSequence(theta, n, seed = 1) { const r = mulberry32(seed); return Array.from({ length: n }, () => (r() < theta ? 1 : 0)); }

export function gammaPoisson(a, b, counts) {
  const S = counts.reduce((x, y) => x + y, 0), A = a + S, B = b + counts.length;
  return { a: A, b: B, mean: A / B, mode: A >= 1 ? (A - 1) / B : 0, var: A / B ** 2, ci: [gammaQuantile(0.025, A, B), gammaQuantile(0.975, A, B)], pdf: (x) => gammaPdf(x, A, B) };
}
export function poissonCounts(lambda, n, seed = 1) { const r = mulberry32(seed); return Array.from({ length: n }, () => poissonSample(r, lambda)); }

/** Normal–Normal, σ đã biết. */
export function normalNormal(mu0, tau0, sigma, xs) {
  const n = xs.length, xbar = n ? xs.reduce((a, b) => a + b, 0) / n : 0;
  const prec0 = 1 / tau0 ** 2, precD = n / sigma ** 2, prec = prec0 + precD;
  const mu = (prec0 * mu0 + precD * xbar) / prec, sdp = Math.sqrt(1 / prec);
  return { mu, sd: sdp, weight: precD / prec, xbar, n, ci: [normalQuantile(0.025, mu, sdp), normalQuantile(0.975, mu, sdp)], pdf: (x) => normalPdf(x, mu, sdp) };
}
export function normalData(mu, sigma, n, seed = 1) { const r = mulberry32(seed); return Array.from({ length: n }, () => mu + sigma * randn(r)); }

/** Đối chứng: tích phân số trên lưới đều. */
export function gridMoments(pdf, lo, hi, N = 20001) {
  const h = (hi - lo) / (N - 1); const xs = [], ws = [];
  for (let i = 0; i < N; i++) { xs.push(lo + i * h); ws.push(pdf(lo + i * h) * h * (i === 0 || i === N - 1 ? 0.5 : 1)); }
  const Z = ws.reduce((a, b) => a + b, 0), m = ws.reduce((a, w, i) => a + w * xs[i], 0) / Z, v = ws.reduce((a, w, i) => a + w * (xs[i] - m) ** 2, 0) / Z;
  let acc = 0, q025 = lo, q975 = hi;
  for (let i = 0; i < N; i++) { const prev = acc; acc += ws[i] / Z; if (prev < 0.025 && acc >= 0.025) q025 = xs[i]; if (prev < 0.975 && acc >= 0.975) q975 = xs[i]; }
  return { Z, mean: m, var: v, ci: [q025, q975] };
}
