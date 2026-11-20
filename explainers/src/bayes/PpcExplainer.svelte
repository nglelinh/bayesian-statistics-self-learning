<script>
  import Stepper from '../shared/Stepper.svelte';
  import Plot from '../shared/Plot.svelte';
  import { tr, norm, fmt } from '../shared/i18n.js';
  import { ppc, STATS, markovSequence, iidSequence } from './ppc.js';
  import { histogram } from './stats.js';

  let { lang: langProp = 'vi', data = 'streaky', stat = 'switches' } = $props();
  const lang = norm(langProp), T = (v, e) => tr(lang, v, e);
  const DATA = {
    iid: { vi: 'Dữ liệu i.i.d. (θ = 0.6) — mô hình đúng', en: 'i.i.d. data (θ = 0.6) — model is right', make: () => iidSequence(60, 0.6, 11) },
    streaky: { vi: 'Dữ liệu theo chuỗi dài (Markov, giữ 85%)', en: 'Streaky data (Markov, stay 85%)', make: () => markovSequence(60, 0.85, 5) },
    alternating: { vi: 'Dữ liệu đổi mặt liên tục (giữ 15%)', en: 'Alternating data (stay 15%)', make: () => markovSequence(60, 0.15, 9) }
  };
  let dk = $state(DATA[data] ? data : 'streaky'), sk = $state(STATS[stat] ? stat : 'switches'), step = $state(0), seed = $state(2);
  $effect(() => { dk; sk; seed; step = 0; });
  const CK = [0, 1, 2, 3, 5, 10, 20, 50, 100, 250, 500];
  const seq = $derived(DATA[dk].make());
  const res = $derived(ppc(seq, 1, 1, sk, 500, seed));
  const m = $derived(CK[Math.min(step, CK.length - 1)]);
  const shown = $derived(res.reps.slice(0, m));
  const lo = $derived(Math.max(0, Math.min(res.obs, ...res.reps) - 2)), hi = $derived(Math.max(res.obs, ...res.reps) + 2);
  const bins = $derived(Math.min(60, Math.ceil(hi - lo)));
  const hist = $derived(m ? histogram(shown, lo, hi, bins) : []);
  const pnow = $derived(m ? (() => { const up = shown.filter((x) => x >= res.obs).length / m, low = shown.filter((x) => x <= res.obs).length / m; return Math.min(1, 2 * Math.min(up, low)); })() : null);
  const layers = $derived([...(hist.length ? [{ type: 'bars', bars: hist.map((h) => ({ x0: h.x0, x1: h.x1, h: h.density })), color: '#93c5fd', opacity: 0.9 }] : []), { type: 'vline', x: res.obs, color: '#dc2626', width: 2.4, label: T('quan sát', 'observed') }]);
  const rows = $derived([{ name: T('Dữ liệu thật', 'Observed'), s: seq }, ...res.firstReps.map((s, i) => ({ name: T('Bản sao ', 'Replicate ') + (i + 1), s }))]);
</script>

<div class="dx">
  <h4>{T('Kiểm tra dự đoán posterior (PPC)', 'Posterior predictive check (PPC)')}</h4>
  <p class="dx-help">{T('Mô hình: mọi lần tung độc lập với cùng θ, prior Beta(1, 1). Ta lấy θ từ posterior rồi mô phỏng “bản sao” dữ liệu; nếu dữ liệu thật trông khác hẳn bản sao ở một thống kê, mô hình thiếu điều gì đó.', 'Model: all flips independent with the same θ, prior Beta(1, 1). We draw θ from the posterior and simulate replicated data; if the real data looks very different from the replicates on some statistic, the model is missing something.')}</p>
  <div class="dx-bar" style="gap:14px">
    <label>{T('Dữ liệu', 'Data')} <select bind:value={dk}>{#each Object.entries(DATA) as [k, v]}<option value={k}>{v[lang]}</option>{/each}</select></label>
    <label>{T('Thống kê kiểm tra', 'Test statistic')} <select bind:value={sk}>{#each Object.entries(STATS) as [k, v]}<option value={k}>{v[lang]}</option>{/each}</select></label>
    <button class="sec" onclick={() => (seed += 1)}>🎲</button>
  </div>
  <Stepper bind:step total={CK.length} {lang} />
  <div style="overflow-x:auto">
    {#each rows as r}
      <div class="pp-row"><span class="pp-name">{r.name}</span><span class="pp-cells">{#each r.s as v}<i class="pp-c {v ? 'on' : ''}"></i>{/each}</span></div>
    {/each}
  </div>
  <Plot {layers} xmin={lo} xmax={hi} xlabel={STATS[sk][lang]} ylabel={T('mật độ', 'density')} label="PPC" height={210} />
  <div class="dx-msg">{T('Đã mô phỏng', 'Simulated')} <b>{m}</b> {T('bản sao', 'replicates')}. {T('Giá trị quan sát', 'Observed value')} = <b>{res.obs}</b>{#if m} · {T('trung bình bản sao', 'replicate mean')} = {fmt(shown.reduce((a, b) => a + b, 0) / m, 1)} · p-value (2 {T('phía', 'sided')}) = <b class={pnow < 0.05 ? 'dx-bad' : 'dx-ok'}>{fmt(pnow, 3)}</b>{/if}.
    {#if m >= 100}{pnow < 0.05 ? T(' ⇒ Mô hình KHÔNG giải thích được đặc điểm này của dữ liệu.', ' ⇒ The model does NOT explain this feature of the data.') : T(' ⇒ Không thấy bằng chứng sai lệch ở thống kê này.', ' ⇒ No evidence of misfit on this statistic.')}{/if}</div>
  <p class="dx-k">{T('Thử “Tổng số ngửa”: mô hình luôn ổn dù dữ liệu theo chuỗi, vì thống kê này không nhạy với cấu trúc đó. Chọn thống kê đúng chỗ mô hình yếu.', 'Try “Total heads”: the model always looks fine even for streaky data because that statistic is blind to the structure. Pick statistics aimed at where the model is weak.')}</p>
</div>

<style>
  .pp-row { display: flex; align-items: center; gap: 8px; margin: 3px 0; min-width: 520px; }
  .pp-name { width: 96px; font-size: .78rem; color: #475569; flex: none; }
  .pp-cells { display: flex; gap: 1px; }
  .pp-c { width: 6.5px; height: 14px; background: #e2e8f0; display: inline-block; }
  .pp-c.on { background: #2563eb; }
</style>
