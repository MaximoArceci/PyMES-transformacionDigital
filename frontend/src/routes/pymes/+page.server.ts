import { authenticatedApi } from '$lib/server/api';
import type { FilterOptions, Pyme } from '$lib/types';

export const load = async ({ fetch, cookies, url }) => {
  const allowed = ['search', 'work_type', 'enterprise_type', 'sector', 'maturity_band'];
  const query = new URLSearchParams();
  for (const key of allowed) { const value = url.searchParams.get(key); if (value) query.set(key, value); }
  try {
    const [companiesResponse, optionsResponse] = await Promise.all([
      authenticatedApi(fetch, cookies, `/pymes/?${query}`),
      authenticatedApi(fetch, cookies, '/pymes/options/')
    ]);
    if (!companiesResponse.ok || !optionsResponse.ok) throw new Error('API unavailable');
    return {
      pymes: await companiesResponse.json() as Pyme[],
      options: await optionsResponse.json() as FilterOptions,
      filters: Object.fromEntries(query), error: null
    };
  } catch {
    return {
      pymes: [] as Pyme[],
      options: { work_types: [], enterprise_types: [], sectors: [], provinces: [] } as FilterOptions,
      filters: Object.fromEntries(query),
      error: 'No pudimos cargar las empresas. Verificá la conexión e intentá nuevamente.'
    };
  }
};
