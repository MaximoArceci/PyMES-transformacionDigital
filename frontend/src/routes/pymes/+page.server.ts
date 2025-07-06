export const load = async () => {
  try {
    const response = await fetch('http://django:9000/api/pyme/', {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Basic YWRtaW46cGFzc3dvcmQ='
      }
    });

    if (!response.ok) {
      throw new Error(`Error al obtener las pymes: ${response.status}`);
    }

    const data = await response.json();

    const pymes = data.results.map((pyme: any) => ({
      name: pyme.name,
      lat: parseFloat(pyme.latitud.replace(',', '.')),
      lng: parseFloat(pyme.longitud.replace(',', '.')),
      trabajoRealizado: pyme.work_type,
      tipoEmpresa: pyme.enterprise_type,
      sector: pyme.sector
    }));

    return { pymes };
  } catch (e) {
    console.error('Error al obtener las pymes desde el endpoint:', e);
    throw e;
  }
};
