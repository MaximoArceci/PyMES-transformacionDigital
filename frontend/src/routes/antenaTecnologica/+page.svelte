<script lang="ts">
    import { quintOut } from 'svelte/easing';
    import { crossfade } from 'svelte/transition';

    // Recibimos los datos del archivo page.server.ts
    export let data;

    // Estado para controlar el modal
    let modalOpen = false;
    let selectedEvent: any = null;

    // Estado para controlar la categoría de eventos seleccionada
    let selectedCategory = 'Eventos y conferencias';

    // Estado para controlar el tipo de evento seleccionado
    let selectedEventType = 'Todos';

    // Función para abrir el modal con un evento específico
    function openModal(evento: any) {
        selectedEvent = evento;
        modalOpen = true;
    }

    // Función para cerrar el modal
    function closeModal() {
        modalOpen = false;
        selectedEvent = null;
    }

    // Los colores de las etiquetas de tipo de evento
    const getEventTypeClass = (tipo: string | undefined) => {
        if (!tipo) {
            return "bg-gray-500";
        }
        // Normalizamos la cadena para que la primera letra esté en mayúscula
        const formattedTipo = tipo.charAt(0).toUpperCase() + tipo.slice(1);
        switch (formattedTipo) {
            case "Conferencia":
                return "bg-blue-600";
            case "Hackathon":
                return "bg-green-600";
            case "Evento":
                return "bg-purple-600";
            case "Competencia":
                return "bg-red-600";
            case "Taller":
                return "bg-yellow-600";
            case "Premio":
                return "bg-orange-600";
            case "Congreso":
                return "bg-teal-600";
            case "Charla":
                return "bg-indigo-600";
            case "Crédito":
                return "bg-emerald-600"; // Nuevo color para financiamientos de crédito
            default:
                return "bg-gray-500";
        }
    };

    // Obtiene una lista de tipos de eventos únicos, excluyendo los valores 'undefined'
    // y normaliza la capitalización para el filtro
    $: eventTypes = data.eventos ? ['Todos', ...new Set(data.eventos.filter(e => e.tipoEvento).map(e => e.tipoEvento.charAt(0).toUpperCase() + e.tipoEvento.slice(1)))] : ['Todos'];


    // Filtra los eventos según la categoría y el tipo seleccionados
    $: filteredEvents = (() => {
        if (!data.eventos || !data.financiamientos) return [];

        let eventsToFilter = selectedCategory === 'Eventos y conferencias'
            ? data.eventos
            : data.financiamientos;

        if (selectedCategory === 'Eventos y conferencias' && selectedEventType !== 'Todos') {
            eventsToFilter = eventsToFilter.filter(evento => {
                // Se agrega esta verificación para evitar el error si tipoEvento es undefined
                if (!evento.tipoEvento) {
                    return false;
                }
                const formattedTipo = evento.tipoEvento.charAt(0).toUpperCase() + evento.tipoEvento.slice(1);
                return formattedTipo === selectedEventType;
            });
        }

        return eventsToFilter;
    })();

    // Resetea el filtro de tipo de evento cuando se cambia la categoría
    $: {
        if (selectedCategory === 'Financiaciones') {
            selectedEventType = 'Todos';
        }
    }
    
    // Handler para eventos de teclado
    function handleKeyDown(event: KeyboardEvent, evento: any) {
        if (event.key === 'Enter' || event.key === ' ') {
            openModal(evento);
        }
    }

</script>

<!-- Contenedor principal con padding y un título grande -->
<div class="p-8 bg-slate-900 min-h-screen">
  <h1 class="text-4xl font-extrabold text-center text-white mb-12 leading-tight">
    Últimos y Próximos Eventos de Tecnología en la Región
  </h1>
  
  <!-- Contenedor de botones de filtrado de categoría -->
  <div class="flex justify-center space-x-4 mb-4">
    <button
      on:click={() => selectedCategory = 'Eventos y conferencias'}
      class="py-2 px-6 rounded-full font-medium transition-colors duration-200
             {selectedCategory === 'Eventos y conferencias' ? 'bg-blue-600 text-white shadow-lg' : 'bg-slate-700 text-slate-300 hover:bg-slate-600'}"
    >
      Eventos y conferencias
    </button>
    <button
      on:click={() => selectedCategory = 'Financiaciones'}
      class="py-2 px-6 rounded-full font-medium transition-colors duration-200
             {selectedCategory === 'Financiaciones' ? 'bg-blue-600 text-white shadow-lg' : 'bg-slate-700 text-slate-300 hover:bg-slate-600'}"
    >
      Financiaciones
    </button>
  </div>

  <!-- Filtro por tipo de evento -->
  {#if selectedCategory === 'Eventos y conferencias'}
  <div class="flex justify-center mb-8">
    <label for="eventTypeFilter" class="text-white font-medium mr-2 self-center">Filtrar por tipo:</label>
    <select 
      id="eventTypeFilter"
      bind:value={selectedEventType}
      class="bg-slate-700 text-white rounded-lg p-2"
    >
      {#each eventTypes as tipo}
        <option value={tipo}>{tipo}</option>
      {/each}
    </select>
  </div>
  {/if}

  <!-- Contenedor de las tarjetas, usando un grid responsivo -->
  <div class="grid gap-8 sm:grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
    <!-- El bucle each ahora usa los eventos filtrados -->
    {#if filteredEvents.length > 0}
      {#each filteredEvents.filter(e => e.nombre && e.link) as evento}
        <!-- Tarjeta individual para cada evento, ahora con bg-slate-800 -->
        <div class="bg-slate-800 rounded-2xl shadow-xl hover:shadow-2xl transition-all duration-300 transform hover:-translate-y-1 overflow-hidden cursor-pointer" 
             on:click={() => openModal(evento)}
             on:keydown={(e) => handleKeyDown(e, evento)}
             role="button"
             tabindex="0"
        >
          <div class="p-6 flex flex-col h-full text-white">
            <!-- Tipo de evento -->
            {#if evento.tipoEvento}
              <div class="flex items-center mb-3">
                <span class="text-sm font-semibold px-3 py-1 rounded-full text-white {getEventTypeClass(evento.tipoEvento)}">
                  {evento.tipoEvento.charAt(0).toUpperCase() + evento.tipoEvento.slice(1)}
                </span>
              </div>
            {/if}
            
            <!-- Título y organización -->
            <h3 class="text-xl font-bold mb-2 flex-grow">{evento.nombre}</h3>
            {#if evento.organizacion}
              <p class="text-sm text-slate-300 mb-4">{evento.organizacion}</p>
            {/if}
            
            <!-- Nueva información: fecha y lugar, con renderizado condicional -->
            <div class="text-sm mb-4">
              {#if evento.fecha}
                <p class="font-medium">📅 Fecha: <span class="font-normal text-slate-300">{evento.fecha}</span></p>
              {/if}
              {#if evento.lugar}
                <p class="font-medium">📍 Lugar: <span class="font-normal text-slate-300">{evento.lugar}</span></p>
              {/if}
            </div>

            <!-- Descripción recortada y botón "Leer más" -->
            {#if evento.descripcion}
              <!-- Usamos line-clamp-3 para cortar el texto de forma elegante -->
              <p class="text-sm text-slate-400 flex-grow mb-2 line-clamp-3">
                {evento.descripcion}
              </p>
              <!-- Mostramos "Leer más" solo si la descripción es lo suficientemente larga -->
              {#if evento.descripcion.length > 100}
                <button on:click|stopPropagation={() => openModal(evento)} class="text-blue-400 hover:text-blue-300 text-sm font-medium">
                  Leer más...
                </button>
              {/if}
            {/if}
          </div>
        </div>
      {/each}
    {:else}
      <p class="text-slate-400 col-span-full text-center">No hay eventos disponibles en esta categoría.</p>
    {/if}
  </div>

  <!-- Aclaración sobre la IA -->
  <div class="mt-12 text-center text-sm text-slate-400">
    <p>
      ℹ️ Esta información ha sido generada y procesada por una inteligencia artificial. Se recomienda verificar los datos en las fuentes originales.
    </p>
  </div>
</div>

<!-- Modal para mostrar la descripción completa -->
{#if modalOpen && selectedEvent}
  <div class="fixed inset-0 bg-black bg-opacity-75 flex items-center justify-center p-4 z-50">
    <div class="bg-slate-800 rounded-2xl p-8 max-w-2xl w-full text-white shadow-2xl relative">
      <button on:click={closeModal} class="absolute top-4 right-4 text-slate-400 hover:text-white transition-colors duration-200">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
        </svg>
      </button>

      <!-- Contenido del modal -->
      <div class="mb-4">
        <span class="text-sm font-semibold px-3 py-1 rounded-full text-white {getEventTypeClass(selectedEvent.tipoEvento)}">
          {selectedEvent.tipoEvento.charAt(0).toUpperCase() + selectedEvent.tipoEvento.slice(1)}
        </span>
      </div>
      <h3 class="text-2xl font-bold mb-2">{selectedEvent.nombre}</h3>
      {#if selectedEvent.organizacion}
        <p class="text-sm text-slate-300 mb-4">{selectedEvent.organizacion}</p>
      {/if}
      <div class="text-sm mb-4">
        {#if selectedEvent.fecha}
          <p class="font-medium">📅 Fecha: <span class="font-normal text-slate-300">{selectedEvent.fecha}</span></p>
        {/if}
        {#if selectedEvent.lugar}
          <p class="font-medium">📍 Lugar: <span class="font-normal text-slate-300">{selectedEvent.lugar}</span></p>
        {/if}
      </div>
      <p class="text-sm text-slate-400 mb-6">{selectedEvent.descripcion}</p>
      <a href={selectedEvent.link} target="_blank" rel="noopener noreferrer" 
         class="inline-block text-center bg-blue-500 hover:bg-blue-600 text-white font-medium py-2 px-4 rounded-lg transition-colors duration-200 shadow-md hover:shadow-lg">
        Ver más detalles
      </a>
    </div>
  </div>
{/if}

<!-- Puedes agregar estilos CSS adicionales aquí si lo deseas -->
<style lang="postcss">
  /*
    @tailwind base;
    @tailwind components;
    @tailwind utilities;
  */
</style>
