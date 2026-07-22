import { env } from '$env/dynamic/private';

export const load = async ({ fetch }) => {
  const base = (env.ANTENNA_API_BASE_URL || 'https://antena-tecnologica.onrender.com').replace(/\/$/, '');
  const headers: Record<string, string> = { accept: 'application/json' };
  if (env.ANTENNA_API_AUTHORIZATION) headers.authorization = env.ANTENNA_API_AUTHORIZATION;
  try {
    const [eventsResponse, fundingResponse] = await Promise.all([
      fetch(`${base}/data/eventos`, { headers }), fetch(`${base}/data/financiamientos`, { headers })
    ]);
    if (!eventsResponse.ok || !fundingResponse.ok) throw new Error();
    const [eventsData, fundingData] = await Promise.all([eventsResponse.json(), fundingResponse.json()]);
    return {
      eventos: eventsData.map((item: any) => ({ nombre:item.nombre,organizacion:item.organizacion,link:item.link,tipoEvento:item.tipo_evento,descripcion:item.descripcion,fecha:item.fecha,lugar:item.lugar })),
      financiamientos: fundingData.map((item: any) => ({ nombre:item.nombre,organizacion:item.organizacion,link:item.link,tipoEvento:'Crédito',descripcion:item.requisitos,fecha:null,lugar:null })),
      error: null
    };
  } catch {
    return { eventos: [], financiamientos: [], error: 'La fuente de Antena Tecnológica no está disponible en este momento.' };
  }
};
