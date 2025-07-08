<script lang="ts">
	import { onMount } from 'svelte';
  import pinAmarillo  from '$lib/assets/pinAmarillo.png';
  import pinRojo  from '$lib/assets/pinRojo.png';
  import pinVerde  from '$lib/assets/pinVerde.png';

	export let data;

	let map;
	let markers: any[] = [];
	let coordenadasTotales = data.pymes;
	let coordenadas = coordenadasTotales;

	let puntoVista = { lat: -34.5729, lng: -58.433123 };
	let sectorFiltro = null;
	let trabajoRealizadoFiltro = null;
	let tipoEmpresaFiltro = null;
	let maduracionFiltro = null;

	let L; // guardamos el módulo leaflet

	async function iniciarMapa() {
		L = await import('leaflet');
		await import('leaflet/dist/leaflet.css');

		map = L.map('map').setView([puntoVista.lat, puntoVista.lng], 12);

		L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
			attribution: '&copy; OpenStreetMap contributors'
		}).addTo(map);

		renderizarMarcadores();
	}

	function limpiarMarcadores() {
		markers.forEach((m) => map.removeLayer(m));
		markers = [];
	}

	function renderizarMarcadores() {
	if (!L || !map) return;

	limpiarMarcadores();

	// Define el ícono usando tu imagen personalizada
  
	for (const pyme of coordenadas) {
    if (!pyme.lat || !pyme.lng) continue;
    let customIcon = L.icon({
      iconUrl: pinAmarillo,  // Asegúrate de que la ruta sea correcta según la estructura de tu proyecto
      iconSize: [50, 50],  // Tamaño de la imagen (ajusta según el tamaño de tu imagen)
      iconAnchor: [15, 30],  // El punto de anclaje para el marcador (ajusta según la imagen)
      popupAnchor: [0, -30],  // El punto donde se abre el popup relativo al ícono
      shadowSize: [50, 50],  // Si tienes una sombra para el marcador, ajusta el tamaño de la sombra
    });
    if (pyme.trabajoRealizado == "Transformación Digital") {
      customIcon = L.icon({
        iconUrl: pinRojo,  // Cambia a la imagen roja para este caso
        iconSize: [50, 50],
        iconAnchor: [15, 30],
        popupAnchor: [0, -30],
        shadowSize: [50, 50],
      });
    } else if (pyme.trabajoRealizado == "Sustentabilidad") {
      customIcon = L.icon({
        iconUrl: pinVerde,  // Cambia a la imagen amarilla para este caso
        iconSize: [50, 50],
        iconAnchor: [15, 30],
        popupAnchor: [0, -30],
        shadowSize: [50, 50],
      });
    } else if (pyme.trabajoRealizado == "innovación") {
      customIcon = L.icon({
        iconUrl: pinAmarillo,  // Cambia a la imagen roja para este caso
        iconSize: [50, 50],
        iconAnchor: [15, 30],
        popupAnchor: [0, -30],
        shadowSize: [50, 50],
      });
    }

		// Crea el marcador con el ícono personalizado
		const marker = L.marker([parseFloat(pyme.lat), parseFloat(pyme.lng)], { icon: customIcon })
			.addTo(map)
			.bindPopup(`
				<b>${pyme.name}</b><br>
				Trabajo: ${pyme.trabajoRealizado}<br>
				Tipo: ${pyme.tipoEmpresa}<br>
				Sector: ${pyme.sector}<br>
				Nivel de Maduración: ${pyme.nivelMaduracion}<br>
			`);
		markers.push(marker);
	}
}


	function cambiarCoords() {
		coordenadas = coordenadasTotales;

		if (sectorFiltro !== null) {
			coordenadas = coordenadas.filter((i: any) => i.sector === sectorFiltro);
		}
		if (trabajoRealizadoFiltro !== null) {
			coordenadas = coordenadas.filter((i: any) => i.trabajoRealizado === trabajoRealizadoFiltro);
		}
		if (tipoEmpresaFiltro !== null) {
			coordenadas = coordenadas.filter((i: any) => i.tipoEmpresa === tipoEmpresaFiltro);
		}
		if (maduracionFiltro !== null) {
			coordenadas = coordenadas.filter((i: any) => i.nivelMaduracion === maduracionFiltro);
		}

		renderizarMarcadores();
	}

	onMount(() => {
		iniciarMapa();
	});
</script>

<div class="bg-slate-900 min-h-screen p-4">
<div class="flex flex-col lg:flex-row lg:space-x-6 m-4 ">
	<!-- Filtros -->
	<div class="w-full lg:w-1/5 space-y-4">
		<button
			on:click={cambiarCoords}
			class="w-full bg-blue-500 text-white font-semibold py-2 px-4 rounded-md hover:bg-blue-600 transition-colors ease-in-out"
		>
			Aplicar filtro
		</button>

		<div>
			<label for="trabajoRealizado" class="block text-sm font-medium mb-2 text-white">Filtrar por trabajo realizado:</label>
			<select
				id="trabajoRealizado"
				bind:value={trabajoRealizadoFiltro}
				class="w-full p-3 border border-white rounded-md bg-slate-900 text-white"
			>
				<option value={null}>Mostrar todos</option>
				<option value="Sustentabilidad">Sustentabilidad</option>
				<option value="Transformación Digital">Transformación Digital</option>
				<option value="innovación">innovación</option>
			</select>
		</div>

		<div>
			<label for="tipoEmpresa" class="block text-sm font-medium mb-2 text-white">Filtrar por tipo de empresa:</label>
			<select
				id="tipoEmpresa"
				bind:value={tipoEmpresaFiltro}
				class="w-full p-3 border border-white rounded-md bg-slate-900 text-white"
			>
				<option value={null}>Mostrar todos</option>
				<option value="Micro-Pyme">Micro-Pyme</option>
				<option value="PyME">PyME</option>
				<option value="Mediana Tramo 1">Mediana Tramo 1</option>
			</select>
		</div>

		<div>
			<label for="sector" class="block text-sm font-medium mb-2 text-white">Filtrar por Sector:</label>
			<select
				id="sector"
				bind:value={sectorFiltro}
				class="w-full p-3 border border-white rounded-md bg-slate-900 text-white"
			>
				<option value={null}>Mostrar todos</option>
				<option value="Servicios">Servicios</option>
				<option value="Metalúrgico">Metalúrgico</option>
				<option value="Gráfico">Gráfico</option>
				<option value="Fabrica">Fabrica</option>
				<option value="Textil">Textil</option>
				<option value="Alimentos">Alimentos</option>
			</select>
		</div>

		<div>
			<label for="maduracion" class="block text-sm font-medium mb-2 text-white">Filtrar por Nivel de Maduración:</label>
			<select
				id="maduracion"
				bind:value={maduracionFiltro}
				class="w-full p-3 border border-white rounded-md bg-slate-900 text-white"
			>
				<option value={null}>Mostrar todos</option>
				<option value="inicial">inicial</option>
				<option value="medio">medio</option>
				<option value="alto">alto</option>
			</select>
		</div>
	</div>

	<!-- Mapa -->
	<div class="w-full lg:w-4/5 h-[900px] border border-gray-300 rounded-lg overflow-hidden shadow-md mt-6 lg:mt-0">
		<div id="map" class="w-full h-full rounded-lg"></div>
	</div>
</div>
</div>