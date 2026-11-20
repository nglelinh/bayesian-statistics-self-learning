// Phân tích quyết định cho A/B test: posterior p ~ Beta(a,b), baseline p0, tổn thất tuyến tính.
import { betaCdf, betaQuantile, betaBinomPmf, betaPdf } from './stats.js';

/** E[(p0 − p)⁺]: mất mát kỳ vọng nếu ship B (nhưng B thực ra kém baseline). Dạng đóng nhờ E[p·1{p<p0}] = mean·F(p0; a+1, b). */
export const eolShip = (a, b, p0) => p0 * betaCdf(p0, a, b) - (a / (a + b)) * betaCdf(p0, a + 1, b);
/** E[(p − p0)⁺]: mất mát kỳ vọng nếu giữ nguyên (bỏ lỡ cải thiện). */
export const eolHold = (a, b, p0) => (a / (a + b)) * (1 - betaCdf(p0, a + 1, b)) - p0 * (1 - betaCdf(p0, a, b));
export const eolBest = (a, b, p0) => Math.min(eolShip(a, b, p0), eolHold(a, b, p0));
export const probBetter = (a, b, p0) => 1 - betaCdf(p0, a, b);
/** Quy tắc ngưỡng: ship khi (1−π)·c_fp < π·c_fn ⇔ π > c_fp/(c_fp+c_fn). */
export const threshold = (cfp, cfn) => cfp / (cfp + cfn);
export const decide = (pi, cfp, cfn) => ((1 - pi) * cfp < pi * cfn ? 'ship' : 'hold');
export const expectedLosses = (pi, cfp, cfn) => ({ ship: (1 - pi) * cfp, hold: pi * cfn });

/** Giá trị kỳ vọng của mẫu thêm m người (EVSI), đơn vị: mất mát kỳ vọng giảm được (theo tỉ lệ chuyển đổi). */
export function evsi(a, b, p0, m) {
  if (m === 0) return 0;
  let after = 0;
  for (let y = 0; y <= m; y++) { const w = betaBinomPmf(y, m, a, b); if (w < 1e-13) continue; after += w * eolBest(a + y, b + m - y, p0); }
  return eolBest(a, b, p0) - after;
}
export const evpi = (a, b, p0) => eolBest(a, b, p0);
/** Tổng lợi ròng của việc thu thêm m mẫu: N·v·EVSI − c·m. */
export const netValue = (a, b, p0, m, N, v, c) => N * v * evsi(a, b, p0, m) - c * m;

/** Mất mát kỳ vọng E[L(p, c)] trên lưới (tích phân điểm giữa). */
export function expectedLoss(a, b, loss, lo = 0, hi = 1, N = 2000) {
  const h = (hi - lo) / N; let s = 0;
  for (let i = 0; i < N; i++) { const p = lo + (i + 0.5) * h; s += betaPdf(p, a, b) * loss(p) * h; }
  return s;
}
export const LOSSES = {
  squared: (c) => (p) => (p - c) ** 2,
  absolute: (c) => (p) => Math.abs(p - c),
  zeroOne: (c, eps = 0.02) => (p) => (Math.abs(p - c) > eps ? 1 : 0),
  pinball: (c, q = 0.8) => (p) => (p > c ? q * (p - c) : (1 - q) * (c - p))
};
/** Điểm tóm tắt tối ưu theo từng loại loss (dạng đóng). */
export const optimal = {
  squared: (a, b) => a / (a + b),
  absolute: (a, b) => betaQuantile(0.5, a, b),
  zeroOne: (a, b) => (a > 1 && b > 1 ? (a - 1) / (a + b - 2) : a <= 1 ? 0 : 1),
  pinball: (a, b, q = 0.8) => betaQuantile(q, a, b)
};
