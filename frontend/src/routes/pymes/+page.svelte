<script lang="ts">
	import { Map, Marker } from "@netnix/leaflet-sveltekit";
	export let data;
	let coordenadasTotales:any = data.pymes;
  let puntoVista:any = [{lat: -34.5729,lng: -58.433123}]
  let coordenadas:any = coordenadasTotales;
  let sectorFiltro:any = null;
  let trabajoRealizadoFiltro:any = null;
  let tipoEmpresaFiltro:any = null;
	
  function cambiarCoords() {
    coordenadas = coordenadasTotales;
    if (sectorFiltro !== null){
    coordenadas = coordenadas.filter((i:any) => i.sector == sectorFiltro);
    }
    if (trabajoRealizadoFiltro !== null){
      coordenadas = coordenadas.filter((i:any) => i.trabajoRealizado == trabajoRealizadoFiltro);
    }
    if (tipoEmpresaFiltro !== null){
      coordenadas = coordenadas.filter((i:any) => i.tipoEmpresa == tipoEmpresaFiltro);
    }
}
</script>

<div class="flex flex-col lg:flex-row lg:space-x-6 m-4">
  <!-- Filtros en una columna -->
  <div class="w-full lg:w-1/3 space-y-4">
    <button 
      on:click={cambiarCoords} 
      class="w-full bg-blue-500 text-white font-semibold py-2 px-4 rounded-md hover:bg-blue-600 transition-colors ease-in-out">
      Aplicar filtro
    </button>
    
    <div>
      <label for="trabajoRealizado" class="block text-gray-700 text-sm font-medium mb-2">Filtrar por trabajo realizado:</label>
      <select 
      id="trabajoRealizado" 
      bind:value={trabajoRealizadoFiltro} 
      class="w-full p-3 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 bg-white shadow-sm transition ease-in-out hover:border-blue-400 hover:shadow-lg">
      <option value={null}>Mostrar todos</option>
      <option value="Sustentabilidad">Sustentabilidad</option>
      <option value="Transformación Digital">Transformación Digital</option>
      <option value="innovación">innovación</option>
    </select>
  </div>
  
  <div>
    <label for="tipoEmpresa" class="block text-gray-700 text-sm font-medium mb-2">Filtrar por tipo de empresa:</label>
    <select 
    id="tipoEmpresa" 
    bind:value={tipoEmpresaFiltro} 
    class="w-full p-3 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 bg-white shadow-sm transition ease-in-out hover:border-blue-400 hover:shadow-lg">
    <option value={null}>Mostrar todos</option>
    <option value="Micro-Pyme">Micro-Pyme</option>
    <option value="PyME">PyME</option>
    <option value="Mediana Tramo 1">Mediana Tramo 1</option>
  </select>
</div>

  <div>
    <label for="sector" class="block text-gray-700 text-sm font-medium mb-2">Filtrar por Sector:</label>
    <select 
      id="sector" 
      bind:value={sectorFiltro} 
      class="w-full p-3 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 bg-white shadow-sm transition ease-in-out hover:border-blue-400 hover:shadow-lg">
      <option value={null}>Mostrar todos</option>
      <option value="Servicios">Servicios</option>
      <option value="Metalúrgico">Metalúrgico</option>
      <option value="Gráfico">Gráfico</option>
      <option value="Fabrica">Fabrica</option>
      <option value="Textil">Textil</option>
      <option value="Alimentos">Alimentos</option>
    </select>
  </div>
    
  </div>

  <!-- Mapa -->
  <div class="w-full lg:w-2/3 h-[500px] border border-gray-300 rounded-lg overflow-hidden shadow-md mt-6 lg:mt-0">
    {#if puntoVista}
      <Map view={[puntoVista[0].lat, puntoVista[0].lng]}>
        {#if coordenadas.length > 0}
          {#each coordenadas as coordenada}
          <Marker latLng={[parseFloat(coordenada.lat), parseFloat(coordenada.lng)]}></Marker>
          {/each}
        {/if}
      </Map>
    {/if}
  </div>
</div>

<!-- Tabla de información debajo del mapa -->
<div class="m-4">
  <h2 class="text-xl font-semibold mb-4">Información de las PYMEs seleccionadas:</h2>
  <table class="min-w-full table-auto border-collapse border border-gray-300 text-left">
    <thead>
      <tr class="bg-gray-100">
        <th class="border border-gray-300 px-4 py-2">Nombre</th>
        <th class="border border-gray-300 px-4 py-2">Latitud</th>
        <th class="border border-gray-300 px-4 py-2">Longitud</th>
        <th class="border border-gray-300 px-4 py-2">Trabajo Realizado</th>
        <th class="border border-gray-300 px-4 py-2">Tipo de Empresa</th>
        <th class="border border-gray-300 px-4 py-2">Sector</th>
      </tr>
    </thead>
    <tbody>
      {#each coordenadas as pyme (pyme.name)}
        <tr>
          <td class="border border-gray-300 px-4 py-2">{pyme.name}</td>
          <td class="border border-gray-300 px-4 py-2">{pyme.lat}</td>
          <td class="border border-gray-300 px-4 py-2">{pyme.lng}</td>
          <td class="border border-gray-300 px-4 py-2">{pyme.trabajoRealizado}</td>
          <td class="border border-gray-300 px-4 py-2">{pyme.tipoEmpresa}</td>
          <td class="border border-gray-300 px-4 py-2">{pyme.sector}</td>
        </tr>
      {/each}
    </tbody>
  </table>
</div>
