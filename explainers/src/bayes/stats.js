// Số học xác suất dùng chung: RNG có seed, lấy mẫu, hàm mật độ/phân phối, phân vị.
export function mulberry32(seed) {
  let a = seed >>> 0;
  return () => { a = (a + 0x6d2b79f5) >>> 0; let t = a; t = Math.imul(t ^ (t >>> 15), t | 1); t ^= t + Math.imul(t ^ (t >>> 7), t | 61); return ((t ^ (t >>> 14)) >>> 0) / 4294967296; };
}
export function randn(rng) { let u = 0; while (u === 0) u = rng(); return Math.sqrt(-2 * Math.log(u)) * Math.cos(2 * Math.PI * rng()); }
export function gammaSample(rng, shape) {
  if (shape < 1) return gammaSample(rng, shape + 1) * Math.pow(rng() || 1e-300, 1 / shape);
  const d = shape - 1 / 3, c = 1 / Math.sqrt(9 * d);
  for (;;) {
    let x, v;
    do { x = randn(rng); v = 1 + c * x; } while (v <= 0);
    v = v * v * v; const u = rng();
    if (u < 1 - 0.0331 * x ** 4 || Math.log(u) < 0.5 * x * x + d * (1 - v + Math.log(v))) return d * v;
  }
}
export const betaSample = (rng, a, b) => { const x = gammaSample(rng, a), y = gammaSample(rng, b); return x / (x + y); };
export function poissonSample(rng, lam) {
  let k = 0, rest = lam;
  while (rest > 0) { const l = Math.min(rest, 20); rest -= l; const L = Math.exp(-l); let p = 1, j = 0; do { j++; p *= rng(); } while (p > L); k += j - 1; }
  return k;
}
export const binomialSample = (rng, n, p) => { let k = 0; for (let i = 0; i < n; i++) if (rng() < p) k++; return k; };

const G = 7, COEF = [0.99999999999980993, 676.5203681218851, -1259.1392167224028, 771.32342877765313, -176.61502916214059, 12.507343278686905, -0.13857109526572012, 9.9843695780195716e-6, 1.5056327351493116e-7];
export function lgamma(x) {
  if (x < 0.5) return Math.log(Math.PI / Math.abs(Math.sin(Math.PI * x))) - lgamma(1 - x);
  x -= 1; let a = COEF[0]; const t = x + G + 0.5;
  for (let i = 1; i < G + 2; i++) a += COEF[i] / (x + i);
  return 0.5 * Math.log(2 * Math.PI) + (x + 0.5) * Math.log(t) - t + Math.log(a);
}
export const betaln = (a, b) => lgamma(a) + lgamma(b) - lgamma(a + b);
export const betaPdf = (x, a, b) => (x <= 0 || x >= 1 ? (x === 0 && a === 1 ? b : x === 1 && b === 1 ? a : 0) : Math.exp((a - 1) * Math.log(x) + (b - 1) * Math.log(1 - x) - betaln(a, b)));
export const gammaPdf = (x, a, rate) => (x <= 0 ? 0 : Math.exp(a * Math.log(rate) + (a - 1) * Math.log(x) - rate * x - lgamma(a)));
export const normalPdf = (x, mu = 0, sd = 1) => Math.exp(-0.5 * ((x - mu) / sd) ** 2) / (sd * Math.sqrt(2 * Math.PI));
export function erf(x) {
  const ax = Math.abs(x); if (ax > 6) return Math.sign(x);
  let sum = ax, term = ax;
  for (let n = 1; n < 200; n++) { term *= -ax * ax / n; const add = term / (2 * n + 1); sum += add; if (Math.abs(add) < 1e-17) break; }
  return Math.sign(x) * 2 / Math.sqrt(Math.PI) * sum;
}
export const normalCdf = (x, mu = 0, sd = 1) => 0.5 * (1 + erf((x - mu) / (sd * Math.SQRT2)));

function betacf(x, a, b) {
  const FP = 1e-300; let qab = a + b, qap = a + 1, qam = a - 1, c = 1, d = 1 - qab * x / qap;
  if (Math.abs(d) < FP) d = FP; d = 1 / d; let h = d;
  for (let m = 1; m <= 300; m++) {
    const m2 = 2 * m; let aa = m * (b - m) * x / ((qam + m2) * (a + m2));
    d = 1 + aa * d; if (Math.abs(d) < FP) d = FP; c = 1 + aa / c; if (Math.abs(c) < FP) c = FP; d = 1 / d; h *= d * c;
    aa = -(a + m) * (qab + m) * x / ((a + m2) * (qap + m2));
    d = 1 + aa * d; if (Math.abs(d) < FP) d = FP; c = 1 + aa / c; if (Math.abs(c) < FP) c = FP; d = 1 / d; const del = d * c; h *= del;
    if (Math.abs(del - 1) < 1e-14) break;
  }
  return h;
}
export function betaCdf(x, a, b) {
  if (x <= 0) return 0; if (x >= 1) return 1;
  const bt = Math.exp(a * Math.log(x) + b * Math.log(1 - x) - betaln(a, b));
  return x < (a + 1) / (a + b + 2) ? bt * betacf(x, a, b) / a : 1 - bt * betacf(1 - x, b, a) / b;
}
export function gammaCdf(x, a, rate) {
  x *= rate; if (x <= 0) return 0;
  if (x < a + 1) { let ap = a, sum = 1 / a, del = sum; for (let n = 0; n < 500; n++) { ap++; del *= x / ap; sum += del; if (Math.abs(del) < Math.abs(sum) * 1e-15) break; } return sum * Math.exp(-x + a * Math.log(x) - lgamma(a)); }
  let b = x + 1 - a, c = 1e300, d = 1 / b, h = d;
  for (let i = 1; i < 500; i++) { const an = -i * (i - a); b += 2; d = an * d + b; if (Math.abs(d) < 1e-300) d = 1e-300; c = b + an / c; if (Math.abs(c) < 1e-300) c = 1e-300; d = 1 / d; const del = d * c; h *= del; if (Math.abs(del - 1) < 1e-15) break; }
  return 1 - Math.exp(-x + a * Math.log(x) - lgamma(a)) * h;
}
export function quantile(cdf, p, lo, hi) {
  for (let i = 0; i < 200; i++) { const mid = (lo + hi) / 2; if (cdf(mid) < p) lo = mid; else hi = mid; }
  return (lo + hi) / 2;
}
export const betaQuantile = (p, a, b) => quantile((x) => betaCdf(x, a, b), p, 0, 1);
export const gammaQuantile = (p, a, rate) => quantile((x) => gammaCdf(x, a, rate), p, 0, 1 + (a + 40 * Math.sqrt(a + 1)) / rate);
export const normalQuantile = (p, mu = 0, sd = 1) => mu + sd * quantile((x) => normalCdf(x), p, -40, 40);
export const binomPmf = (k, n, p) => Math.exp(lgamma(n + 1) - lgamma(k + 1) - lgamma(n - k + 1) + (k ? k * Math.log(p) : 0) + (n - k ? (n - k) * Math.log(1 - p) : 0));
export const betaBinomPmf = (k, n, a, b) => Math.exp(lgamma(n + 1) - lgamma(k + 1) - lgamma(n - k + 1) + betaln(k + a, n - k + b) - betaln(a, b));

export const mean = (xs) => xs.reduce((a, b) => a + b, 0) / xs.length;
export const variance = (xs) => { const m = mean(xs); return xs.reduce((a, b) => a + (b - m) ** 2, 0) / (xs.length - 1); };
export const sd = (xs) => Math.sqrt(variance(xs));
export function sampleQuantile(xs, p) { const s = [...xs].sort((a, b) => a - b); const i = p * (s.length - 1), lo = Math.floor(i); return s[lo] + (s[Math.min(lo + 1, s.length - 1)] - s[lo]) * (i - lo); }
export function histogram(xs, lo, hi, bins) {
  const h = new Array(bins).fill(0);
  for (const x of xs) { const i = Math.floor((x - lo) / (hi - lo) * bins); if (i >= 0 && i < bins) h[i]++; }
  return h.map((c, i) => ({ x0: lo + (hi - lo) * i / bins, x1: lo + (hi - lo) * (i + 1) / bins, count: c, density: c / xs.length / ((hi - lo) / bins) }));
}

/** digamma ψ(x) (đệ quy lên x ≥ 6 rồi khai triển tiệm cận). */
export function digamma(x) {
  let r = 0;
  while (x < 6) { r -= 1 / x; x += 1; }
  const f = 1 / (x * x);
  return r + Math.log(x) - 0.5 / x - f * (1 / 12 - f * (1 / 120 - f * (1 / 252 - f * (1 / 240 - f / 132))));
}
/** Phân phối t (df bậc tự do) qua beta không đầy đủ. */
export function tCdf(t, df) { const x = df / (df + t * t), I = betaCdf(x, df / 2, 0.5); return t > 0 ? 1 - I / 2 : I / 2; }
export const tPdf = (t, df) => Math.exp(lgamma((df + 1) / 2) - lgamma(df / 2) - 0.5 * Math.log(df * Math.PI) - ((df + 1) / 2) * Math.log(1 + t * t / df));
