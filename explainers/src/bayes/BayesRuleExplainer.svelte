<script>
  import Stepper from '../shared/Stepper.svelte';
  import { tr, norm, fmt } from '../shared/i18n.js';
  import { diagnose, COINS, coinPath } from './bayesrule.js';
  import { flipSequence } from './conjugate.js';

  let { lang: langProp = 'vi', tab: tabProp = 'tree', preset = 'disease' } = $props();
  const lang = norm(langProp), T = (v, e) => tr(lang, v, e);
  let tab = $state(tabProp === 'sequential' ? 'sequential' : 'tree');

  const PRESETS = {
    disease: { vi: 'Bệnh hiếm (1%, nhạy 90%, đặc hiệu 95%)', en: 'Rare disease (1%, sens 90%, spec 95%)', prev: 1, sens: 90, spec: 95, sick: { vi: 'bệnh', en: 'sick' } },
    common: { vi: 'Bệnh phổ biến (20%, nhạy 90%, đặc hiệu 95%)', en: 'Common disease (20%, sens 90%, spec 95%)', prev: 20, sens: 90, spec: 95 },
    spam: { vi: 'Bộ lọc spam (5% là spam, bắt 98%, nhầm 3%)', en: 'Spam filter (5% spam, catches 98%, 3% false alarms)', prev: 5, sens: 98, spec: 97 }
  };
  let pid = $state(PRESETS[preset] ? preset : 'disease');
  let prev = $state(PRESETS[pid].prev), sens = $state(PRESETS[pid].sens), spec = $state(PRESETS[pid].spec);
  let step = $state(0);
  function choose(id) { pid = id; prev = PRESETS[id].prev; sens = PRESETS[id].sens; spec = PRESETS[id].spec; step = 0; }
  const d = $derived(diagnose(prev / 100, sens / 100, spec / 100, 1000));
  const counts = $derived.by(() => {
    const sickR = Math.round(d.sick), tp = Math.round(sickR * sens / 100), fp = Math.round((1000 - sickR) * (100 - spec) / 100);
    return { tp, fn: sickR - tp, fp, tn: 1000 - sickR - fp };
  });
  const dots = $derived.by(() => {
    const order = [...Array(counts.tp).fill('tp'), ...Array(counts.fn).fill('fn'), ...Array(counts.fp).fill('fp'), ...Array(counts.tn).fill('tn')];
    return order.map((c, i) => ({ c, x: 8 + (i % 50) * 10.9, y: 8 + Math.floor(i / 50) * 10.9 }));
  });
  const color = (c) => {
    if (step === 0) return '#94a3b8';
    if (step === 1) return c === 'tp' || c === 'fn' ? '#dc2626' : '#94a3b8';
    return { tp: '#dc2626', fn: '#f59e0b', fp: '#7c3aed', tn: '#94a3b8' }[c];
  };
  const op = (c) => (step >= 3 && c !== 'tp' && c !== 'fp' ? 0.12 : 1);
  const msgs = $derived([
    T(`Hình dung 1000 người. Mỗi chấm là một người.`, `Picture 1000 people. Each dot is one person.`),
    T(`Tỉ lệ nền ${prev}%: khoảng ${fmt(d.sick, 1)} người thật sự mắc (đỏ), còn lại ${fmt(d.healthy, 1)} người khỏe.`, `Base rate ${prev}%: about ${fmt(d.sick, 1)} people truly have it (red); the other ${fmt(d.healthy, 1)} do not.`),
    T(`Xét nghiệm: ${fmt(d.tp, 1)} người bệnh dương tính (đỏ, thật), ${fmt(d.fn, 1)} bị bỏ sót (cam). Trong ${fmt(d.healthy, 1)} người khỏe, ${fmt(d.fp, 1)} bị báo nhầm (tím).`, `Test: ${fmt(d.tp, 1)} sick people test positive (red), ${fmt(d.fn, 1)} are missed (orange). Of ${fmt(d.healthy, 1)} healthy people, ${fmt(d.fp, 1)} get a false alarm (purple).`),
    T(`Bạn nhận kết quả dương tính ⇒ chỉ còn nhóm dương tính: ${fmt(d.positives, 1)} người (đỏ + tím).`, `You tested positive ⇒ only the positives remain: ${fmt(d.positives, 1)} people (red + purple).`),
    T(`Trong nhóm đó, ${fmt(d.tp, 1)} người thật sự mắc: P(mắc | dương tính) = ${fmt(d.tp, 1)} / ${fmt(d.positives, 1)} = ${fmt(d.ppv * 100, 1)}%.`, `Among them ${fmt(d.tp, 1)} truly have it: P(sick | positive) = ${fmt(d.tp, 1)} / ${fmt(d.positives, 1)} = ${fmt(d.ppv * 100, 1)}%.`)
  ]);

  // ---- cập nhật tuần tự
  const PRIORS = { equal: { vi: 'Đều (1/3 mỗi loại)', en: 'Equal (1/3 each)', p: [1 / 3, 1 / 3, 1 / 3] }, fair: { vi: 'Tin đồng xu công bằng (10/80/10)', en: 'Believe fair coin (10/80/10)', p: [0.1, 0.8, 0.1] } };
  let priorKey = $state('equal'), truth = $state(0.8), seed = $state(3), sstep = $state(0);
  $effect(() => { priorKey; truth; seed; sstep = 0; });
  const flips = $derived(flipSequence(truth, 14, seed));
  const path = $derived(coinPath(PRIORS[priorKey].p, flips));
  const cur = $derived(path[Math.min(sstep, path.length - 1)]);
</script>

<div class="dx">
  <h4>{T('Định lý Bayes bằng tần suất tự nhiên và cập nhật tuần tự', 'Bayes’ theorem with natural frequencies and sequential updating')}</h4>
  <div class="dx-tabs">
    <button class={tab === 'tree' ? 'on' : 'sec'} onclick={() => (tab = 'tree')}>{T('Cây tần suất tự nhiên', 'Natural-frequency tree')}</button>
    <button class={tab === 'sequential' ? 'on' : 'sec'} onclick={() => (tab = 'sequential')}>{T('Cập nhật tuần tự (3 đồng xu)', 'Sequential update (3 coins)')}</button>
  </div>
  {#if tab === 'tree'}
    <p class="dx-help">{T('Thay vì nhân xác suất, hãy đếm người. Kéo thanh trượt để thấy vì sao một xét nghiệm “chính xác 95%” vẫn có thể cho kết quả dương tính phần lớn là báo nhầm khi bệnh hiếm.', 'Instead of multiplying probabilities, count people. Drag the sliders to see why a “95% accurate” test can still produce mostly false alarms when the condition is rare.')}</p>
    <div class="dx-bar"><label>{T('Ví dụ', 'Example')} <select value={pid} onchange={(e) => choose(e.currentTarget.value)}>{#each Object.entries(PRESETS) as [k, p]}<option value={k}>{p[lang]}</option>{/each}</select></label></div>
    <div class="dx-bar" style="gap:14px">
      <label>{T('Tỉ lệ nền', 'Base rate')} <b>{prev}%</b> <input type="range" min="0.1" max="50" step="0.1" bind:value={prev} /></label>
      <label>{T('Độ nhạy', 'Sensitivity')} <b>{sens}%</b> <input type="range" min="50" max="100" step="1" bind:value={sens} /></label>
      <label>{T('Độ đặc hiệu', 'Specificity')} <b>{spec}%</b> <input type="range" min="50" max="100" step="1" bind:value={spec} /></label>
    </div>
    <Stepper bind:step total={5} {lang} />
    <div class="dx-msg">{msgs[Math.min(step, 4)]}</div>
    <svg viewBox="0 0 556 224" role="img" aria-label={T('1000 người', '1000 people')} style="width:100%;height:auto;border:1px solid #e2e8f0;border-radius:8px;background:#fff">
      {#each dots as p}<circle cx={p.x} cy={p.y} r="4.4" fill={color(p.c)} opacity={op(p.c)} />{/each}
    </svg>
    <div class="dx-trail" style="margin-top:6px">
      <span class="dx-pill" style="border-color:#dc2626">{T('Bệnh & dương', 'Sick & +')}: {fmt(d.tp, 1)}</span>
      <span class="dx-pill" style="border-color:#f59e0b">{T('Bệnh & âm', 'Sick & −')}: {fmt(d.fn, 1)}</span>
      <span class="dx-pill" style="border-color:#7c3aed">{T('Khỏe & dương', 'Healthy & +')}: {fmt(d.fp, 1)}</span>
      <span class="dx-pill">{T('Khỏe & âm', 'Healthy & −')}: {fmt(d.tn, 1)}</span>
    </div>
    <p class="dx-k">{T('Công thức tương ứng', 'Matching formula')}: P(H | +) = P(+|H)P(H) / [P(+|H)P(H) + P(+|¬H)P(¬H)] = {sens / 100} × {prev / 100} / ({sens / 100} × {prev / 100} + {fmt(1 - spec / 100, 2)} × {fmt(1 - prev / 100, 3)}) = <b>{fmt(d.ppv, 3)}</b></p>
  {:else}
    <p class="dx-help">{T('Có ba đồng xu: thiên sấp (p = 0.2), công bằng (0.5), thiên ngửa (0.8). Mỗi lần tung, nhân prior với likelihood rồi chuẩn hóa: posterior hôm nay là prior của lần sau.', 'Three coins: tails-biased (p = 0.2), fair (0.5), heads-biased (0.8). After each flip, multiply prior by likelihood and normalise: today’s posterior is tomorrow’s prior.')}</p>
    <div class="dx-bar">
      <label>Prior <select bind:value={priorKey}>{#each Object.entries(PRIORS) as [k, p]}<option value={k}>{p[lang]}</option>{/each}</select></label>
      <label>{T('Đồng xu thật', 'True coin')} <select bind:value={truth}>{#each COINS as c}<option value={c.p}>{c.name}</option>{/each}</select></label>
      <button class="sec" onclick={() => (seed += 1)}>🎲 {T('Chuỗi mới', 'New sequence')}</button>
    </div>
    <Stepper bind:step={sstep} total={flips.length + 1} {lang} />
    <div class="dx-trail dx-mono">{#each flips as f, i}{#if i < sstep}<span class="dx-pill {f ? 'good' : 'hot'}">{f ? T('N', 'H') : T('S', 'T')}</span>{/if}{/each}{#if sstep === 0}<span class="dx-k">{T('(chưa tung)', '(no flips yet)')}</span>{/if}</div>
    <div class="bp-bars">
      {#each COINS as c, i}
        <div class="bp-row"><span class="dx-mono bp-name">{c.name}</span>
          <div class="bp-track"><div class="bp-bar prior" style="width:{PRIORS[priorKey].p[i] * 100}%"></div><div class="bp-bar post" style="width:{cur[i] * 100}%"></div></div>
          <b class="dx-mono">{fmt(cur[i] * 100, 1)}%</b></div>
      {/each}
    </div>
    <p class="dx-k">{T('Xám = prior ban đầu; xanh = posterior sau', 'Grey = initial prior; blue = posterior after')} {sstep} {T('lần tung', 'flips')}.</p>
  {/if}
</div>

<style>
  .bp-bars { display: flex; flex-direction: column; gap: 8px; margin: 10px 0; }
  .bp-row { display: grid; grid-template-columns: 64px 1fr 58px; gap: 8px; align-items: center; }
  .bp-track { position: relative; height: 22px; background: #f1f5f9; border-radius: 6px; overflow: hidden; }
  .bp-bar { position: absolute; left: 0; top: 0; height: 100%; transition: width .25s; }
  .bp-bar.prior { background: #cbd5e1; height: 40%; top: 0; }
  .bp-bar.post { background: #3b82f6; height: 60%; top: 40%; }
</style>
