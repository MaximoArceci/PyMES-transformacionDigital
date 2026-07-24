type CoordinateSource = {
  latitud: string | null | undefined;
  longitud: string | null | undefined;
};

export function parseCoordinates(source: CoordinateSource): [number, number] | null {
  const latitudeText = String(source.latitud ?? '').trim();
  const longitudeText = String(source.longitud ?? '').trim();
  if (!latitudeText || !longitudeText) return null;

  const latitude = Number(latitudeText.replace(',', '.'));
  const longitude = Number(longitudeText.replace(',', '.'));
  if (
    !Number.isFinite(latitude)
    || !Number.isFinite(longitude)
    || latitude < -90
    || latitude > 90
    || longitude < -180
    || longitude > 180
  ) return null;

  return [latitude, longitude];
}
