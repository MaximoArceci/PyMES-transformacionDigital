// @ts-nocheck
import type { PageServerLoad } from './$types';

export const load: PageServerLoad = async ({ fetch }) => {
  const headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Basic YWRtaW46cGFzc3dvcmQ='
  };

  try {
    // Fetch para eventos
    const eventosResponse = await fetch('https://antena-tecnologica.onrender.com/data/eventos', {
      method: 'GET',
      headers: headers
    });

    if (!eventosResponse.ok) {
      throw new Error(`Error al obtener los eventos: ${eventosResponse.status}`);
    }

    const eventosData = await eventosResponse.json();

    // Fetch para financiamientos
    const financiamientosResponse = await fetch('https://antena-tecnologica.onrender.com/data/financiamientos', {
      method: 'GET',
      headers: headers
    });

    if (!financiamientosResponse.ok) {
      throw new Error(`Error al obtener los financiamientos: ${financiamientosResponse.status}`);
    }

    const financiamientosData = await financiamientosResponse.json();

    // Mapeamos los datos de eventos a un formato consistente
    const eventos = eventosData.map((evento: any) => ({
      nombre: evento.nombre,
      organizacion: evento.organizacion,
      link: evento.link,
      tipoEvento: evento.tipo_evento,
      descripcion: evento.descripcion,
      fecha: evento.fecha,
      lugar: evento.lugar
    }));

    // Mapeamos los datos de financiamientos a un formato consistente
    const financiamientos = financiamientosData.map((financiamiento: any) => ({
      nombre: financiamiento.nombre,
      organizacion: financiamiento.organizacion,
      link: financiamiento.link,
      tipoEvento: 'Crédito', // Mapeamos tipo_financiamiento a tipoEvento para el frontend
      descripcion: financiamiento.requisitos, // Usamos requisitos como la descripción
      fecha: undefined, // No se provee fecha en este endpoint
      lugar: undefined // No se provee lugar en este endpoint
    }));

    // Retornamos ambos arrays de datos
    return { eventos, financiamientos };
  } catch (e) {
    console.error('Error al obtener datos desde los endpoints:', e);
    // En caso de error, retornamos arrays vacíos para evitar que la página falle
    return { eventos: [], financiamientos: [] };
  }
};
