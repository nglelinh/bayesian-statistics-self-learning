<script>
  // Thanh điều khiển dùng chung: Về đầu · Lùi · Play/Dừng · Bước tiếp + tốc độ.
  let { step = $bindable(0), total = 1, speed: speedProp = 3, lang = 'vi' } = $props();
  const en = $derived(lang === 'en');
  let speed = $state(speedProp);
  let playing = $state(false);
  const last = $derived(Math.max(0, total - 1));
  const MS = [2000, 1300, 850, 480, 230];

  $effect(() => {
    if (step > last) step = last;
  });
  $effect(() => {
    if (!playing) return;
    const id = setInterval(() => {
      if (step >= last) playing = false;
      else step += 1;
    }, MS[speed - 1] ?? 850);
    return () => clearInterval(id);
  });
  function toggle() {
    if (playing) { playing = false; return; }
    if (step >= last) step = 0;
    playing = true;
  }
</script>

<div class="dx-bar dx-stepper">
  <button class="sec" onclick={() => { playing = false; step = 0; }}>{en ? '⏮ Restart' : '⏮ Về đầu'}</button>
  <button class="sec" disabled={step <= 0} onclick={() => { playing = false; step = Math.max(0, step - 1); }}>{en ? '◀ Back' : '◀ Lùi'}</button>
  <button class={playing ? 'on' : ''} onclick={toggle}>{playing ? (en ? '⏸ Pause' : '⏸ Dừng') : '▶ Play'}</button>
  <button class="sec" disabled={step >= last} onclick={() => { playing = false; step = Math.min(last, step + 1); }}>{en ? 'Next ▶' : 'Bước tiếp ▶'}</button>
  <label>{en ? 'Speed' : 'Tốc độ'} <input type="range" min="1" max="5" bind:value={speed} /></label>
  <span class="dx-k">{en ? 'Step' : 'Bước'} {Math.min(step, last) + 1} / {last + 1}</span>
</div>
