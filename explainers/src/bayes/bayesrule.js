// Quy tắc Bayes: tần suất tự nhiên (cây) và cập nhật tuần tự nhiều giả thuyết.
export function diagnose(prev, sens, spec, N = 1000) {
  const sick = prev * N, healthy = N - sick;
  const tp = sick * sens, fn = sick - tp, tn = healthy * spec, fp = healthy - tn;
  return { N, sick, healthy, tp, fn, fp, tn, positives: tp + fp, ppv: tp + fp > 0 ? tp / (tp + fp) : NaN, npv: tn + fn > 0 ? tn / (tn + fn) : NaN };
}
/** Công thức Bayes trực tiếp P(bệnh | dương tính). */
export const bayesPPV = (prev, sens, spec) => (sens * prev) / (sens * prev + (1 - spec) * (1 - prev));

/** Cập nhật rời rạc: priors[i] · L(data | h_i) rồi chuẩn hóa. */
export function updateDiscrete(priors, likes) {
  const joint = priors.map((p, i) => p * likes[i]); const Z = joint.reduce((a, b) => a + b, 0);
  return { joint, evidence: Z, posterior: joint.map((j) => j / Z) };
}
/** Ba loại đồng xu (công bằng, thiên ngửa 0.8, thiên sấp 0.2): cập nhật sau từng lần tung. */
export const COINS = [{ name: 'p = 0.2', p: 0.2 }, { name: 'p = 0.5', p: 0.5 }, { name: 'p = 0.8', p: 0.8 }];
export function coinPath(priors, flips, coins = COINS) {
  const path = [priors.slice()]; let cur = priors.slice();
  for (const f of flips) { cur = updateDiscrete(cur, coins.map((c) => (f ? c.p : 1 - c.p))).posterior; path.push(cur); }
  return path;
}
