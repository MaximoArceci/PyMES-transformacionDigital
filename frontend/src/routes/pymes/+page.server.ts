import fs from 'fs';
import Papa from 'papaparse';

export const load = async () => {
  try {
    // Leer el archivo CSV local
    const csvFile = fs.readFileSync('./pymes.csv', 'utf8');

    // Parsear el CSV usando papaparse
    const parsedData = Papa.parse(csvFile, {
      header: true,  // Usar la primera fila como cabeceras
    });

    // Convertir los datos en el formato esperado
    const pymes:any = parsedData.data.map((pyme: any) => ({
      name: pyme['Nombre de Fantasia'],
      lat: parseFloat(pyme['Latitud'].replace(',', '.')), 
      lng: parseFloat(pyme['Longitud'].replace(',', '.')), 
      trabajoRealizado: pyme['Trabajo realizado'],
      tipoEmpresa: pyme['Tipo de empresa'],
      sector: pyme['Sector']
    }));
    console.log(pymes);

    return { pymes };
  } catch (e) {
    console.error('Error al leer el archivo CSV:', e);
    throw e;
  }
};

