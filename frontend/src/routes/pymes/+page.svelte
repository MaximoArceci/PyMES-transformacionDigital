<script lang="ts">
  import { goto, invalidateAll } from '$app/navigation';
  import { onMount } from 'svelte';
  import { parseCoordinates } from '$lib/coordinates';
  import type { Pyme } from '$lib/types';
  export let data;

  let map: any;
  let L: any;
  let markerLayer: any;
  let selected: Pyme | null = null;
  let view: 'map' | 'list' = 'map';
  let filtersOpen = false;
  let filtersCollapsed = false;
  let search = data.filters.search ?? '';
  let workType = data.filters.work_type ?? '';
  let enterpriseType = data.filters.enterprise_type ?? '';
  let sector = data.filters.sector ?? '';
  let maturityBand = data.filters.maturity_band ?? '';

  const BUENOS_AIRES_CENTER: [number, number] = [-34.6037, -58.3816];
  const BUENOS_AIRES_ZOOM = 11;
  const WORK_TYPE_COLORS = ['#1663c7', '#b5e600', '#f97316', '#8b5cf6', '#14b8a6', '#ef4444', '#f59e0b', '#64748b'];
  const coordinates = (pyme: Pyme) => parseCoordinates(pyme);
  const hasActiveFilters = () => Object.values(data.filters).some(Boolean);

  $: availableWorkTypes = (data.options.work_types?.length
    ? data.options.work_types
    : [...new Set((data.pymes as Pyme[]).map((pyme) => pyme.work_type).filter(Boolean))]) as string[];
  $: workTypeLegend = availableWorkTypes.map((type) => ({ type, color: workTypeColor(type) }));

  function workTypeColor(type: string) {
    const index = availableWorkTypes.indexOf(type);
    if (index >= 0) return WORK_TYPE_COLORS[index % WORK_TYPE_COLORS.length];
    let hash = 0;
    for (const char of type || 'Sin tipo') hash = char.charCodeAt(0) + ((hash << 5) - hash);
    return WORK_TYPE_COLORS[Math.abs(hash) % WORK_TYPE_COLORS.length];
  }

  function selectCompany(pyme: Pyme) {
    selected = pyme;
    const point = coordinates(pyme);
    if (map && point) map.flyTo(point, Math.max(map.getZoom(), 13), { duration: .55 });
    renderMarkers();
  }

  function renderMarkers() {
    if (!L || !map) return;
    if (markerLayer) markerLayer.clearLayers(); else markerLayer = L.layerGroup().addTo(map);
    const bounds: any[] = [];
    for (const pyme of data.pymes as Pyme[]) {
      const point = coordinates(pyme); if (!point) continue;
      bounds.push(point);
      const active = selected?.id === pyme.id;
      const color = workTypeColor(pyme.work_type);
      const icon = L.divIcon({
        className: '',
        html: `<span class="company-pin ${active ? 'is-active' : ''}" style="--pin-color:${color}" aria-hidden="true"><i></i></span>`,
        iconSize: [38, 46], iconAnchor: [19, 44]
      });
      L.marker(point, { icon, title: pyme.name }).on('click', () => selectCompany(pyme)).addTo(markerLayer);
    }
    if (!selected && hasActiveFilters()) {
      if (bounds.length === 1) map.setView(bounds[0], 13);
      else if (bounds.length > 1) map.fitBounds(bounds, { padding: [55, 55], maxZoom: 12 });
    } else if (!selected) {
      map.setView(BUENOS_AIRES_CENTER, BUENOS_AIRES_ZOOM, { animate: false });
    }
  }

  function applyFilters() {
    const query = new URLSearchParams();
    for (const [key, value] of Object.entries({ search, work_type: workType, enterprise_type: enterpriseType, sector, maturity_band: maturityBand })) if (value) query.set(key, value);
    filtersOpen = false; selected = null; goto(`/pymes?${query}`);
  }
  function toggleFilters() {
    if (window.matchMedia('(max-width: 700px)').matches) filtersOpen = !filtersOpen;
    else filtersCollapsed = !filtersCollapsed;
    requestAnimationFrame(() => map?.invalidateSize());
  }
  function clearFilters() { search = workType = enterpriseType = sector = maturityBand = ''; goto('/pymes'); }
  function handleKeys(event: KeyboardEvent) { if (event.key === 'Escape') { selected = null; filtersOpen = false; renderMarkers(); } }

  $: if (map && data.pymes) renderMarkers();
  onMount(() => {
    let disposed = false;
    (async () => {
      L = await import('leaflet'); await import('leaflet/dist/leaflet.css');
      if (disposed) return;
      map = L.map('company-map', { zoomControl: false }).setView(BUENOS_AIRES_CENTER, BUENOS_AIRES_ZOOM);
      L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', { attribution: '&copy; OpenStreetMap contributors' }).addTo(map);
      L.control.zoom({ position: 'topleft' }).addTo(map); renderMarkers();
      window.addEventListener('keydown', handleKeys);
    })();
    return () => { disposed = true; window.removeEventListener('keydown', handleKeys); map?.remove(); };
  });
</script>

<svelte:head><title>Explorar empresas · PyMEs</title></svelte:head>
<div class="explorer page-shell">
  <div class="explorer-toolbar">
    <h1>Explorar empresas</h1>
    <div class="search"><span>⌕</span><input aria-label="Buscar empresa" placeholder="Buscar empresa…" bind:value={search} on:keydown={(e) => e.key === 'Enter' && applyFilters()} /></div>
    <button class="btn-dark filter-trigger" aria-controls="company-filters" on:click={toggleFilters}>☷ <span>Filtros</span></button>
  </div>

  <div class:filters-collapsed={filtersCollapsed} class="workspace">
    {#if filtersOpen}<button class="drawer-backdrop" aria-label="Cerrar filtros" on:click={() => filtersOpen = false}></button>{/if}
    <aside id="company-filters" class:open={filtersOpen}>
      <div class="filter-heading"><strong>Refinar búsqueda</strong><button on:click={clearFilters}>Limpiar</button></div>
      <label>▣ Trabajo realizado<select class="field" bind:value={workType}><option value="">Todos</option>{#each data.options.work_types as value}<option>{value}</option>{/each}</select></label>
      <label>▦ Tipo de empresa<select class="field" bind:value={enterpriseType}><option value="">Todos</option>{#each data.options.enterprise_types as value}<option>{value}</option>{/each}</select></label>
      <label>▧ Sector<select class="field" bind:value={sector}><option value="">Todos</option>{#each data.options.sectors as value}<option>{value}</option>{/each}</select></label>
      <label>⌁ Nivel de maduración<select class="field" bind:value={maturityBand}><option value="">Todos</option><option>Inicial</option><option>Medio</option><option>Alto</option></select></label>
      <button class="btn-primary apply" on:click={applyFilters}>Aplicar filtros</button>

      <section class="results">
        <div class="results-summary"><strong>Resultados</strong><b>{data.pymes.length}</b><small>Seleccioná una empresa para ver más información.</small></div>
        {#each data.pymes as pyme}
          <button class:selected={selected?.id === pyme.id} class="company-card" on:click={() => selectCompany(pyme)}>
            <span><strong>{pyme.name}</strong><small>{pyme.locality || pyme.province || 'Ubicación no informada'}</small></span>
            <b>{pyme.rating?.toFixed(1) ?? '—'}</b>
            <span class="card-badges"><i>{pyme.sector || 'Sin sector'}</i><i>{pyme.maturity_band || 'Sin nivel'}</i></span>
          </button>
        {/each}
      </section>
    </aside>

    <main class="content">
      <div class="map-caption"><span>Vista del mapa</span><strong>Buenos Aires y alrededores</strong></div>
      {#if workTypeLegend.length}
        <div class="work-type-legend" aria-label="Colores por trabajo realizado">
          <strong>Trabajo realizado</strong>
          {#each workTypeLegend as item}
            <span><i style={`background:${item.color}`}></i>{item.type}</span>
          {/each}
        </div>
      {/if}
      <div class="view-toggle"><button class:active={view === 'map'} on:click={() => view='map'}>Mapa</button><button class:active={view === 'list'} on:click={() => view='list'}>Lista</button></div>
      <div id="company-map" class:hidden={view !== 'map'}></div>
      {#if view === 'list'}
        <section class="list-view">
          {#if data.error}<div class="empty"><h2>No pudimos cargar el mapa</h2><p>{data.error}</p><button class="btn-primary" on:click={() => invalidateAll()}>Reintentar</button></div>
          {:else if data.pymes.length === 0}<div class="empty"><h2>Sin resultados</h2><p>Probá quitando alguno de los filtros.</p></div>
          {:else}{#each data.pymes as pyme}<button on:click={() => { selectCompany(pyme); view='map'; }}><span><strong>{pyme.name}</strong><small>{pyme.locality || pyme.province}</small></span><span>{pyme.sector}</span><span>{pyme.work_type}</span><b>{pyme.rating?.toFixed(1) ?? '—'}</b></button>{/each}{/if}
        </section>
      {/if}
      {#if data.error && view === 'map'}<div class="map-error">{data.error} <button on:click={() => invalidateAll()}>Reintentar</button></div>{/if}
      {#if selected}
        <article class="company-detail">
          <button class="close" aria-label="Cerrar detalle" on:click={() => { selected=null; renderMarkers(); }}>×</button>
          <span class="lime-label">Trabajo realizado</span><h2>{selected.name}</h2><p class="location">{selected.locality || selected.province || 'Ubicación no informada'}</p><p>{selected.description || 'Empresa participante del programa de diagnóstico y transformación digital.'}</p>
          <div class="detail-grid"><span><small>Diagnóstico</small><b>{selected.work_type || 'Sin datos'}</b></span><span><small>Empresa</small><b>{selected.enterprise_type || 'Sin datos'}</b></span><span><small>Sector</small><b>{selected.sector || 'Sin datos'}</b></span><span><small>Madurez</small><b>{selected.maturity_band || 'Sin datos'}</b></span></div>
          {#if selected.website}<a class="btn-primary" href={selected.website} target="_blank" rel="noreferrer">Ver detalle de empresa</a>{:else}<button class="btn-primary" disabled>Detalle no disponible</button>{/if}
        </article>
      {/if}
    </main>
  </div>
</div>

<style>
  .explorer{display:flex;flex-direction:column;height:calc(100vh - 72px);height:calc(100dvh - 72px);min-height:0;overflow:hidden;background:#fff}.explorer-toolbar{height:70px;flex:0 0 70px;display:flex;align-items:center;padding:0 3.8%;gap:16px;border-bottom:1px solid #dce2e8;box-shadow:0 2px 7px #0a203a16;z-index:800}.explorer-toolbar h1{font-size:1.25rem;margin:0 auto 0 0}.search{height:40px;width:min(320px,30vw);display:flex;align-items:center;gap:8px;border:1px solid var(--border);border-radius:9px;padding:0 10px}.search span{font-size:1.6rem;color:#8395aa}.search input{border:0;outline:0;width:100%}.filter-trigger{min-height:40px}.workspace{display:grid;grid-template-columns:282px 1fr;flex:1;min-height:0;overflow:hidden}aside{min-height:0;padding:40px 24px 24px;overflow-y:auto;overscroll-behavior:contain;background:#fff;z-index:500;box-shadow:4px 0 10px #0a203a16}.filter-heading{display:flex;justify-content:space-between;margin-bottom:30px;font-size:.9rem}.filter-heading button{border:0;background:none;color:#8192a8}aside label{display:grid;gap:7px;margin-bottom:18px;font-size:.88rem}.apply{width:100%;margin:24px 0 28px}.results{display:grid;gap:14px}.results-summary{display:grid;grid-template-columns:1fr auto;gap:8px;background:var(--navy);color:white;border-radius:16px;padding:14px 16px}.results-summary b{color:var(--lime)}.results-summary small{grid-column:1/-1;color:#b9c6d3;font-size:.68rem;line-height:1.4}.company-card{width:100%;display:grid;grid-template-columns:1fr auto;text-align:left;gap:5px;padding:12px 14px;border:1px solid var(--border);border-radius:16px;background:#fff;color:var(--navy)}.company-card.selected{border-color:var(--lime);box-shadow:0 6px 16px #b5e60025}.company-card span:first-child{display:grid;gap:4px}.company-card small{color:#65758a;font-size:.68rem}.company-card>b{color:var(--lime-dark)}.card-badges{grid-column:1/-1;display:flex;gap:8px}.card-badges i{font-style:normal;font-size:.65rem;padding:3px 10px;border:1px solid var(--border);border-radius:20px}.card-badges i:first-child{background:var(--lime);border-color:var(--lime)}.content{position:relative;height:100%;min-width:0;min-height:0;overflow:hidden;background:#e8eef0}.map-caption{position:absolute;top:12px;left:30px;z-index:450;background:var(--navy);color:white;padding:10px 16px;border-radius:16px;display:grid}.map-caption span{text-transform:uppercase;font-size:.58rem;color:#b9c6d3}.view-toggle{position:absolute;right:4%;top:32px;z-index:450;display:flex}.view-toggle button{width:88px;height:34px;border:1px solid var(--navy);background:white}.view-toggle button:first-child{border-radius:9px 0 0 9px}.view-toggle button:last-child{border-radius:0 9px 9px 0}.view-toggle button.active{background:var(--navy);color:white}#company-map{height:100%;min-height:0}.hidden{visibility:hidden;position:absolute;inset:0}.company-detail{position:absolute;right:40px;bottom:24px;width:min(352px,calc(100% - 32px));background:var(--navy);color:white;border-radius:18px;padding:20px 16px 16px;z-index:450;box-shadow:0 20px 40px #0a203a44}.close{position:absolute;right:12px;top:9px;border:0;background:transparent;color:white;font-size:1.4rem}.lime-label{color:var(--lime);font-size:.67rem}.company-detail h2{font-size:1rem;margin:2px 0}.location{color:#b9c6d3;margin:0 0 14px!important}.company-detail p{color:#c7d0da;font-size:.72rem;line-height:1.4}.detail-grid{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin:16px 0}.detail-grid span{background:var(--navy-2);border-radius:15px;padding:10px 12px;display:grid}.detail-grid small{color:#aebbc8}.detail-grid b{font-size:.7rem;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}.company-detail .btn-primary{width:100%;font-size:.78rem}.company-detail button:disabled{opacity:.6}.list-view{height:100%;min-height:0;padding:90px 4% 30px;background:#f5f7f6;overflow:auto}.list-view>button{width:100%;display:grid;grid-template-columns:2fr 1fr 1.2fr 60px;align-items:center;gap:20px;padding:16px;border:0;border-bottom:1px solid #d9e0e7;background:white;text-align:left}.list-view>button span:first-child{display:grid}.list-view small{color:#74859a}.empty{text-align:center;padding:80px 20px}.map-error{position:absolute;z-index:500;top:90px;left:50%;transform:translateX(-50%);background:white;padding:14px 18px;border-radius:10px;box-shadow:0 8px 30px #0002}.map-error button{border:0;background:none;color:#789c00;font-weight:bold}.drawer-backdrop{display:none}:global(.company-pin){display:block;width:34px;height:40px;background:white;border-radius:17px 17px 17px 4px;transform:rotate(-45deg);box-shadow:0 4px 12px #0a203a44;border:1px solid #d7e0e7}:global(.company-pin i){position:absolute;width:10px;height:10px;border-radius:50%;background:var(--navy);left:11px;top:11px}:global(.company-pin.is-active){background:var(--lime);border-color:var(--lime);transform:rotate(-45deg) scale(1.12)}
  .work-type-legend{position:absolute;left:22px;top:92px;z-index:650;display:grid;gap:7px;max-width:min(270px,42vw);padding:12px 14px;background:#fffffff2;border:1px solid #d6dee6;border-radius:14px;box-shadow:0 8px 22px #0a203a18;color:var(--navy);font-size:.72rem}.work-type-legend strong{font-size:.76rem;text-transform:uppercase;letter-spacing:.04em}.work-type-legend span{display:flex;align-items:center;gap:8px;line-height:1.2}.work-type-legend i{width:12px;height:12px;flex:0 0 auto;border:2px solid white;border-radius:50%;box-shadow:0 0 0 1px #0a203a20}:global(.company-pin){--pin-color:var(--lime);position:relative;display:block;width:34px;height:34px;border:3px solid white;border-radius:50% 50% 50% 0;background:var(--pin-color);box-shadow:0 5px 15px #0a203a55;transform:rotate(-45deg)}:global(.company-pin i){position:absolute;inset:8px;display:block;border-radius:50%;background:white;box-shadow:inset 0 0 0 2px #0a203a16}:global(.company-pin.is-active){width:42px;height:42px;box-shadow:0 8px 22px #0a203a66,0 0 0 5px #ffffffaa}:global(.company-pin.is-active i){inset:10px}
  @media(min-width:701px){.workspace.filters-collapsed{grid-template-columns:1fr}.workspace.filters-collapsed aside{display:none}}
  @media(max-width:900px){.workspace{grid-template-columns:240px 1fr}.explorer-toolbar{padding:0 18px}.results{display:none}.company-detail{right:16px}}
  @media(max-width:700px){.explorer{height:calc(100vh - 62px);height:calc(100dvh - 62px)}.explorer-toolbar{height:64px;flex-basis:64px}.explorer-toolbar h1{font-size:1rem}.search{width:auto;flex:1}.filter-trigger span{display:none}.workspace{display:block;min-height:0}.workspace,.content{height:100%}aside{position:fixed;left:0;top:0;bottom:0;width:min(88vw,340px);transform:translateX(-105%);transition:.2s;padding-top:28px;z-index:2000}aside.open{transform:none}.drawer-backdrop{display:block;position:fixed;inset:0;border:0;background:#07182c88;z-index:1900}.results{display:grid}#company-map{min-height:0;height:100%}.map-caption{left:12px;top:12px}.work-type-legend{left:12px;top:132px;max-width:calc(100vw - 24px);font-size:.68rem}.view-toggle{right:12px;top:74px}.company-detail{left:12px;right:12px;bottom:12px;width:auto;max-height:64vh;overflow:auto}.list-view{padding:122px 12px 24px;height:100%}.list-view>button{grid-template-columns:1fr 50px}.list-view>button span:nth-child(2),.list-view>button span:nth-child(3){display:none}}
</style>
