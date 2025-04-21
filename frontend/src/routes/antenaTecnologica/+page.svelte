<script lang="ts">
	let eventos = [
		{
			institucion: "Universidad Católica de Cordoba (UCC)",
			nombre: "Encuentro de Alumni por 25 y 50 aniversario",
			fecha: "Jueves 27/02",
			lugar: "Campus UCC"
		},
		{
			institucion: "Universidad Católica de Cordoba (UCC)",
			nombre: 'Concierto de Mingui Ingaramo: "Piano y silencio"',
			fecha: "Viernes 28/02",
			lugar: "Aud. Diego De Torres"
		},
		{
			institucion: "Universidad Católica de Cordoba (UCC)",
			nombre: 'Muestra fotográfica “En busca de las 4C”',
			fecha: "Viernes 28/02",
			lugar: "Edificio Centro"
		},
		{
			institucion: "Universidad Católica de Cordoba (UCC)",
			nombre: 'Bienvenida ingresantes 2025',
			fecha: "Miercoles 05/03",
			lugar: "Campus UCC"
		},
		{
			institucion: "Universidad Católica de Cordoba (UCC)",
			nombre: 'Inicio año académico 2025',
			fecha: "Viernes 07/03",
			lugar: "Campus UCC"
		},
		{
			institucion: "Universidad Católica de Cordoba (UCC)",
			nombre: 'Cierre convocatoria AUSJAL para investigación',
			fecha: "Viernes 09/05",
			lugar: "Virtual"
		}
	]
</script>

<div class="m-4">
	<h2 class="text-xl font-semibold mb-4">Información de las PYMEs seleccionadas:</h2>
	<table class="min-w-full table-auto border-collapse border border-gray-300 text-left">
	  <thead>
		<tr class="bg-gray-100">
		  <th class="border border-gray-300 px-4 py-2">Institucion</th>
		  <th class="border border-gray-300 px-4 py-2">Nombre</th>
		  <th class="border border-gray-300 px-4 py-2">Fecha</th>
		  <th class="border border-gray-300 px-4 py-2">Lugar</th>
		</tr>
	  </thead>
	  <tbody>
		{#each eventos as evento}
		<tr>
			<td class="border border-gray-300 px-4 py-2">{evento.institucion}</td>
			<td class="border border-gray-300 px-4 py-2">{evento.nombre}</td>
			<td class="border border-gray-300 px-4 py-2">{evento.fecha}</td>
			<td class="border border-gray-300 px-4 py-2">{evento.lugar}</td>
		</tr>
		{/each}
	  </tbody>
	</table>
  </div>