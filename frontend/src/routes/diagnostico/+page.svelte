<script lang="ts">
  import { goto, invalidateAll } from '$app/navigation';
  import { onMount } from 'svelte';
  import type { ChartDatum, Pyme } from '$lib/types';
  export let data;
  let province = data.filters.province ?? '';
  let maturityLevel = data.filters.maturity_level ?? '';
  let workType = data.filters.work_type ?? '';
  let enterpriseType = data.filters.enterprise_type ?? '';
  let page = 1;
  const perPage = 7;
  let miniMap: any;

  $: summary = data.summary;
  $: rows = summary?.table ?? [];
  $: totalPages = Math.max(1, Math.ceil(rows.length / perPage));
  $: pageRows = rows.slice((page - 1) * perPage, page * perPage);
  $: if (page > totalPages) page = totalPages;

  const maxCount = (items: ChartDatum[]) => Math.max(1, ...items.map((item) => item.count));
  const donut = (items: ChartDatum[]) => {
    const colors = ['#0a203a', '#b5e600', '#1663c7', '#7d8ba0'];
    const total = items.reduce((sum, item) => sum + item.count, 0) || 1;
    let cursor = 0;
    return `conic-gradient(${items.map((item, index) => { const start=cursor; cursor += item.count/total*360; return `${colors[index % colors.length]} ${start}deg ${cursor}deg`; }).join(',')})`;
  };
  function apply() {
    const query = new URLSearchParams();
    for (const [key,value] of Object.entries({province,maturity_level:maturityLevel,work_type:workType,enterprise_type:enterpriseType})) if(value) query.set(key,value);
    goto(`/diagnostico?${query}`);
  }
  function validPoint(company: Pyme) {
    const lat=Number(String(company.latitud).replace(',','.')), lng=Number(String(company.longitud).replace(',','.'));
    return Number.isFinite(lat)&&Number.isFinite(lng)?[lat,lng]:null;
  }
  onMount(() => {
    let disposed=false;
    (async()=>{const L=await import('leaflet');await import('leaflet/dist/leaflet.css');if(disposed||!document.getElementById('diagnostic-map'))return;miniMap=L.map('diagnostic-map',{zoomControl:false,attributionControl:false}).setView([-34.6,-58.48],9);L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(miniMap);const points:any[]=[];for(const company of summary?.companies??[]){const point=validPoint(company);if(!point)continue;points.push(point);L.circleMarker(point,{radius:7,color:'#b5e600',fillColor:'#b5e600',fillOpacity:.78,weight:1}).addTo(miniMap)}if(points.length)miniMap.fitBounds(points,{padding:[18,18]});})();
    return()=>{disposed=true;miniMap?.remove()};
  });
</script>

<svelte:head><title>Diagnóstico empresarial · PyMEs</title></svelte:head>
<main class="dashboard page-shell">
  <div class="dashboard-title"><h1 class="display-title">Mapa de diagnóstico empresarial</h1></div>
  <section class="dashboard-body">
    <div class="filters">
      <label>Provincias<select bind:value={province} on:change={apply}><option value="">Todas</option>{#each data.options.provinces as value}<option>{value}</option>{/each}</select></label>
      <label>Nivel<select bind:value={maturityLevel} on:change={apply}><option value="">Todos</option>{#each [1,2,3,4,5] as value}<option value={value}>Nivel {value}</option>{/each}</select></label>
      <label>Tipo de diagnóstico<select bind:value={workType} on:change={apply}><option value="">Todos</option>{#each data.options.work_types as value}<option>{value}</option>{/each}</select></label>
      <label>Tipo de empresa<select bind:value={enterpriseType} on:change={apply}><option value="">Todos</option>{#each data.options.enterprise_types as value}<option>{value}</option>{/each}</select></label>
    </div>
    {#if data.error || !summary}
      <div class="error-state"><h2>Diagnóstico no disponible</h2><p>{data.error}</p><button class="btn-primary" on:click={() => invalidateAll()}>Reintentar</button></div>
    {:else}
      <section class="kpis">
        <article><i>▥</i><span><b class="display-title">Total empresas</b><strong>{summary.total_companies}</strong></span></article>
        <article><i>◆</i><span><b class="display-title">Rubros distintos</b><strong>{summary.distinct_sectors}</strong></span></article>
        <article class="lime"><i>⌁</i><span><b class="display-title">Nivel de madurez prom.</b><strong>{summary.average_maturity_score?.toLocaleString('es-AR') ?? '—'}</strong></span></article>
        <article class="lime"><i>☆</i><span><b class="display-title">Empresas nivel alto</b><strong>{summary.high_maturity_count}</strong></span></article>
      </section>
      <section class="charts-top">
        <article class="chart-card sectors"><h2 class="display-title">Empresas por rubro/sector</h2><div class="horizontal-bars">{#each summary.by_sector as item}<div><span>{item.label}</span><i><b style={`width:${item.count/maxCount(summary.by_sector)*100}%`}></b></i><small>{item.count}</small></div>{/each}</div></article>
        <div class="donut-stack">
          <article class="chart-card"><h2 class="display-title">Distribución por nivel</h2><div class="donut-row"><div class="donut" style={`background:${donut(summary.by_maturity_band)}`}></div><ul>{#each summary.by_maturity_band as item}<li>{item.label} <b>{item.count}</b></li>{/each}</ul></div></article>
          <article class="chart-card"><h2 class="display-title">Tipo de diagnóstico</h2><div class="donut-row"><div class="donut" style={`background:${donut(summary.by_work_type)}`}></div><ul>{#each summary.by_work_type as item}<li>{item.label} <b>{item.count}</b></li>{/each}</ul></div></article>
        </div>
      </section>
      <section class="charts-bottom">
        <article class="chart-card"><h2 class="display-title">Mapa de empresas</h2><div id="diagnostic-map"></div></article>
        <article class="chart-card"><h2 class="display-title">Nivel de madurez de 1/5</h2><div class="vertical-bars">{#each summary.by_maturity_level as item}<div><i style={`height:${item.count/maxCount(summary.by_maturity_level)*100}%`}></i><b>{item.label}</b><small>{item.count}</small></div>{/each}</div></article>
        <article class="chart-card table-card"><h2 class="display-title">Tabla de detalle</h2><div class="table-scroll"><table><thead><tr><th>Provincia</th><th>Nivel prom.</th><th>Diagnóstico</th><th>Empresa</th><th>Total</th></tr></thead><tbody>{#each pageRows as row}<tr><td>{row.province||'Todas'}</td><td>{row.average_maturity ? (row.average_maturity/20).toFixed(1) : '—'}</td><td>{row.work_type}</td><td>{row.enterprise_type}</td><td>{row.count}</td></tr>{/each}</tbody></table></div><div class="pagination"><span>{rows.length ? (page-1)*perPage+1 : 0}–{Math.min(page*perPage,rows.length)} de {rows.length}</span><button disabled={page===1} on:click={()=>page--}>‹</button><button disabled={page===totalPages} on:click={()=>page++}>›</button></div></article>
      </section>
    {/if}
  </section>
</main>

<style>
  .dashboard{background:#fff}.dashboard-title{height:76px;background:var(--navy);color:white;display:flex;align-items:center;padding:0 3.9%}.dashboard-title h1{font-size:1.55rem}.dashboard-body{padding:30px 3.9% 48px}.filters{display:grid;grid-template-columns:repeat(4,1fr);gap:46px;margin-bottom:34px}.filters label{font-size:.9rem}.filters select{display:block;width:100%;height:40px;margin-top:8px;border:0;border-left:2px solid var(--lime);padding:0 8px;color:var(--navy);background:white}.kpis{display:grid;grid-template-columns:repeat(4,1fr);gap:38px;margin-bottom:28px}.kpis article{display:flex;align-items:center;gap:20px;min-height:105px}.kpis i{font-style:normal;font-size:3.8rem;color:var(--navy)}.kpis span{display:grid;gap:10px}.kpis b{font-size:1.2rem}.kpis strong{font-size:2.5rem}.kpis .lime i,.kpis .lime strong{color:var(--lime)}.chart-card{min-width:0;background:white}.chart-card h2{font-size:1.25rem;margin:0 0 20px}.charts-top{display:grid;grid-template-columns:2fr 1fr;gap:48px;margin-bottom:34px}.horizontal-bars{display:grid;gap:10px}.horizontal-bars>div{display:grid;grid-template-columns:310px 1fr 30px;gap:10px;align-items:center;font-size:.82rem}.horizontal-bars span{text-align:right}.horizontal-bars i{height:17px;border-left:1px dashed #8998a8;background:repeating-linear-gradient(90deg,transparent 0,transparent 24.8%,#aab4bf 25%)}.horizontal-bars i b{display:block;height:100%;background:var(--navy)}.horizontal-bars small{color:#65758a}.donut-stack{display:grid;gap:26px}.donut-row{display:flex;align-items:center;justify-content:center;gap:28px}.donut{width:96px;height:96px;border-radius:50%;position:relative}.donut:after{content:'';position:absolute;inset:25%;background:white;border-radius:50%}.donut-row ul{list-style:none;padding:0;margin:0;display:grid;gap:7px;font-size:.72rem}.donut-row li:before{content:'●';color:var(--lime);margin-right:6px}.charts-bottom{display:grid;grid-template-columns:1.15fr .68fr 1fr;gap:18px}.charts-bottom .chart-card{min-height:300px}#diagnostic-map{height:270px;background:#dce3df}.vertical-bars{height:260px;display:flex;align-items:flex-end;gap:18px;padding:20px 12px 0}.vertical-bars>div{height:100%;flex:1;display:flex;flex-direction:column-reverse;align-items:center;gap:7px;position:relative}.vertical-bars i{display:block;width:70%;background:var(--navy);min-height:2px}.vertical-bars b{font-size:.8rem}.vertical-bars small{position:absolute;top:0;font-size:.65rem;color:#7d8ba0}.table-scroll{overflow:auto}table{border-collapse:collapse;width:100%;font-size:.66rem}th{background:var(--navy);color:white;padding:5px;text-align:left;white-space:nowrap}td{padding:7px 5px;white-space:nowrap;border-bottom:1px solid #edf0f2}.pagination{display:flex;align-items:center;justify-content:flex-end;gap:7px;margin-top:10px;font-size:.68rem}.pagination button{border:0;background:white;font-size:1.2rem}.error-state{text-align:center;padding:100px 20px}.error-state p{color:#687a90}
  @media(max-width:1100px){.kpis{grid-template-columns:repeat(2,1fr)}.charts-bottom{grid-template-columns:1fr 1fr}.table-card{grid-column:1/-1}.horizontal-bars>div{grid-template-columns:200px 1fr 30px}}
  @media(max-width:720px){.dashboard-title{height:62px;padding:0 18px}.dashboard-title h1{font-size:1.15rem}.dashboard-body{padding:20px 16px}.filters{grid-template-columns:1fr 1fr;gap:16px}.kpis{grid-template-columns:1fr;gap:4px}.kpis article{min-height:80px}.kpis i{font-size:2.8rem}.kpis strong{font-size:2rem}.charts-top,.charts-bottom{grid-template-columns:1fr;gap:34px}.table-card{grid-column:auto}.horizontal-bars>div{grid-template-columns:120px 1fr 25px}.horizontal-bars span{font-size:.68rem}.chart-card{min-height:auto!important}}
</style>
