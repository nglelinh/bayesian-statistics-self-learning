// Xấp xỉ lưới: posterior ∝ prior × likelihood trên N điểm.
import { betaPdf, binomPmf } from './stats.js';

export const PRIORS = {
  flat: { vi: 'Đều (Beta(1,1))', en: 'Flat (Beta(1,1))', pdf: () => 1 },
  beta22: { vi: 'Beta(2,2) — hơi tin công bằng', en: 'Beta(2,2) — mild belief in fairness', pdf: (t) => betaPdf(t, 2, 2) },
  beta55: { vi: 'Beta(5,5) — tin khá mạnh', en: 'Beta(5,5) — fairly strong', pdf: (t) => betaPdf(t, 5, 5) },
  tri: { vi: 'Tam giác lệch (không liên hợp)', en: 'Skewed triangle (not conjugate)', pdf: (t) => (t < 0.7 ? t / 0.7 * 2 : (1 - t) / 0.3 * 2) * 0.5 / 0.5 * 1 },
  bimodal: { vi: 'Hai đỉnh (không liên hợp)', en: 'Two-peak (not conjugate)', pdf: (t) => 0.5 * betaPdf(t, 20, 5) + 0.5 * betaPdf(t, 5, 20) }
};

export function gridApprox(priorPdf, k, n, N) {
  const theta = Array.from({ length: N }, (_, i) => (i + 0.5) / N);
  const prior = theta.map(priorPdf), like = theta.map((t) => binomPmf(k, n, t)), un = prior.map((p, i) => p * like[i]);
  const Z = un.reduce((a, b) => a + b, 0), post = un.map((u) => u / Z);
  const mean = post.reduce((a, p, i) => a + p * theta[i], 0), variance = post.reduce((a, p, i) => a + p * (theta[i] - mean) ** 2, 0);
  let acc = 0, lo = theta[0], hi = theta[N - 1];
  for (let i = 0; i < N; i++) { const prev = acc; acc += post[i]; if (prev < 0.025 && acc >= 0.025) lo = theta[i]; if (prev < 0.975 && acc >= 0.975) hi = theta[i]; }
  return { theta, prior, like, unnormalized: un, post, evidence: Z / N, mean, sd: Math.sqrt(variance), ci: [lo, hi], density: post.map((p) => p * N) };
}
