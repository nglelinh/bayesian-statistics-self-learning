<script>
  // Biểu đồ SVG đơn giản, co giãn theo bề rộng khung (viewBox).
  // layers: line {pts,color,width,dash} · area {pts,color,opacity} · bars {bars:[{x0,x1,h}],color,opacity}
  //         vline {x,color,dash,label} · hline {y,...} · points {pts,color,r,opacity} · rect {x0,x1,color,opacity}
  //         seg {x1,y1,x2,y2,color,width,dash,opacity} · text {x,y,text,color,anchor}
  import { scaleLinear } from 'd3';
  let { width = 560, height = 240, xmin = 0, xmax = 1, ymin = 0, ymax = null, layers = [], xlabel = '', ylabel = '', xticks = 6, yticks = 4, label = 'Biểu đồ', grid = true } = $props();
  const m = { l: 44, r: 12, t: 10, b: 32 };
  const top = $derived.by(() => {
    if (ymax !== null) return ymax;
    let t = 0;
    for (const l of layers) {
      if (l.pts && (l.type === 'line' || l.type === 'area')) for (const p of l.pts) if (Number.isFinite(p[1])) t = Math.max(t, p[1]);
      if (l.type === 'bars') for (const b of l.bars) t = Math.max(t, b.h);
    }
    return t > 0 ? t * 1.08 : 1;
  });
  const X = $derived(scaleLinear().domain([xmin, xmax]).range([m.l, width - m.r]));
  const Y = $derived(scaleLinear().domain([ymin, top]).range([height - m.b, m.t]));
  const path = (pts) => pts.filter((p) => Number.isFinite(p[1])).map((p, i) => (i ? 'L' : 'M') + X(p[0]).toFixed(1) + ',' + Y(p[1]).toFixed(1)).join('');
  const area = (pts) => { const q = pts.filter((p) => Number.isFinite(p[1])); return q.length ? path(q) + `L${X(q[q.length - 1][0]).toFixed(1)},${Y(0).toFixed(1)}L${X(q[0][0]).toFixed(1)},${Y(0).toFixed(1)}Z` : ''; };
  const xt = $derived(X.ticks(xticks));
  const yt = $derived(Y.ticks(yticks));
  const f = (v) => (Math.abs(v) >= 1000 ? +(v / 1000).toFixed(2) + 'k' : Math.abs(v) < 0.01 && v !== 0 ? v.toExponential(0) : +v.toFixed(3));
</script>

<svg viewBox="0 0 {width} {height}" role="img" aria-label={label} style="width:100%;height:auto;display:block;background:#fff;border:1px solid #e2e8f0;border-radius:8px">
  {#if grid}{#each yt as t}<line x1={m.l} x2={width - m.r} y1={Y(t)} y2={Y(t)} stroke="#eef2f7" />{/each}{/if}
  <line x1={m.l} x2={width - m.r} y1={height - m.b} y2={height - m.b} stroke="#94a3b8" />
  <line x1={m.l} x2={m.l} y1={m.t} y2={height - m.b} stroke="#94a3b8" />
  {#each xt as t}<text x={X(t)} y={height - m.b + 14} font-size="11" text-anchor="middle" fill="#64748b">{f(t)}</text>{/each}
  {#each yt as t}<text x={m.l - 5} y={Y(t) + 4} font-size="11" text-anchor="end" fill="#64748b">{f(t)}</text>{/each}
  {#if xlabel}<text x={(m.l + width - m.r) / 2} y={height - 3} font-size="11.5" text-anchor="middle" fill="#334155">{xlabel}</text>{/if}
  {#if ylabel}<text x="11" y={(m.t + height - m.b) / 2} font-size="11.5" text-anchor="middle" fill="#334155" transform="rotate(-90 11 {(m.t + height - m.b) / 2})">{ylabel}</text>{/if}
  {#each layers as l}
    {#if l.type === 'rect'}<rect x={X(l.x0)} y={m.t} width={Math.max(0, X(l.x1) - X(l.x0))} height={height - m.b - m.t} fill={l.color || '#93c5fd'} opacity={l.opacity ?? 0.25} />
    {:else if l.type === 'bars'}{#each l.bars as b}<rect x={X(b.x0) + 0.5} y={Y(b.h)} width={Math.max(0, X(b.x1) - X(b.x0) - 1)} height={Math.max(0, Y(0) - Y(b.h))} fill={b.color || l.color || '#94a3b8'} opacity={l.opacity ?? 0.8} />{/each}
    {:else if l.type === 'area'}<path d={area(l.pts)} fill={l.color || '#3b82f6'} opacity={l.opacity ?? 0.25} />
    {:else if l.type === 'line'}<path d={path(l.pts)} fill="none" stroke={l.color || '#1d4ed8'} stroke-width={l.width ?? 2} stroke-dasharray={l.dash || null} opacity={l.opacity ?? 1} stroke-linejoin="round" />
    {:else if l.type === 'vline'}<line x1={X(l.x)} x2={X(l.x)} y1={m.t} y2={height - m.b} stroke={l.color || '#dc2626'} stroke-width={l.width ?? 1.6} stroke-dasharray={l.dash || null} />{#if l.label}<text x={X(l.x) + 4} y={m.t + 11} font-size="11" fill={l.color || '#dc2626'}>{l.label}</text>{/if}
    {:else if l.type === 'hline'}<line x1={m.l} x2={width - m.r} y1={Y(l.y)} y2={Y(l.y)} stroke={l.color || '#dc2626'} stroke-width={l.width ?? 1.4} stroke-dasharray={l.dash || null} />
    {:else if l.type === 'points'}{#each l.pts as p}<circle cx={X(p[0])} cy={Y(p[1])} r={l.r ?? 3} fill={l.hollow ? '#fff' : (l.color || '#0f172a')} stroke={l.color || '#0f172a'} stroke-width={l.hollow ? 1.8 : 0} opacity={l.opacity ?? 1} />{/each}
    {:else if l.type === 'seg'}<line x1={X(l.x1)} x2={X(l.x2)} y1={Y(l.y1)} y2={Y(l.y2)} stroke={l.color || '#1d4ed8'} stroke-width={l.width ?? 1.5} stroke-dasharray={l.dash || null} opacity={l.opacity ?? 1} />
    {:else if l.type === 'text'}<text x={X(l.x)} y={Y(l.y)} font-size="11.5" fill={l.color || '#0f172a'} text-anchor={l.anchor || 'start'}>{l.text}</text>{/if}
  {/each}
</svg>
