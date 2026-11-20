// Bayes factor / marginal likelihood: M0 θ = θ0 (điểm) vs M1 θ ~ Beta(a, b), dữ liệu k thành công trong n.
import { binomPmf, betaBinomPmf, betaPdf, mulberry32, betaSample } from './stats.js';

export const marginal0 = (k, n, t0 = 0.5) => binomPmf(k, n, t0);
export const marginal1 = (k, n, a, b) => betaBinomPmf(k, n, a, b);
export const bf10 = (k, n, a, b, t0 = 0.5) => marginal1(k, n, a, b) / marginal0(k, n, t0);
export const postProb1 = (bf, priorOdds = 1) => (bf * priorOdds) / (1 + bf * priorOdds);
/** Savage–Dickey: BF10 = p(θ0) / p(θ0 | y) khi M0 lồng trong M1. */
export const savageDickey = (k, n, a, b, t0 = 0.5) => betaPdf(t0, a, b) / betaPdf(t0, a + k, b + n - k);
/** Ước lượng Monte Carlo của marginal likelihood: trung bình likelihood theo prior. */
export function mcMarginal(k, n, a, b, R = 200000, seed = 1) { const r = mulberry32(seed); let s = 0; for (let i = 0; i < R; i++) s += binomPmf(k, n, betaSample(r, a, b)); return s / R; }
/** Tích phân số trên lưới: ∫ Bin(k | n, θ) Beta(θ | a, b) dθ. */
export function gridMarginal(k, n, a, b, N = 20000) { let s = 0; for (let i = 0; i < N; i++) { const t = (i + 0.5) / N; s += binomPmf(k, n, t) * betaPdf(t, a, b) / N; } return s; }
/** log10 BF10 sau mỗi lần tung (đường tích lũy bằng chứng). */
export function bfPath(flips, a, b, t0 = 0.5) { let k = 0; return [{ n: 0, k: 0, log10: 0 }, ...flips.map((f, i) => { k += f; const n = i + 1; return { n, k, log10: Math.log10(bf10(k, n, a, b, t0)) }; })]; }
export const jeffreys = (log10bf) => { const x = Math.abs(log10bf); return x < 0.5 ? 0 : x < 1 ? 1 : x < 1.5 ? 2 : x < 2 ? 3 : 4; };
