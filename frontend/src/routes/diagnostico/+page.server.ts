import { authenticatedApi } from '$lib/server/api';
import type { FilterOptions, Summary } from '$lib/types';

export const load = async ({ fetch, cookies, url }) => {
  const keys = ['province', 'maturity_level', 'work_type', 'enterprise_type'];
  const query = new URLSearchParams();
  for (const key of keys) { const value = url.searchParams.get(key); if (value) query.set(key, value); }
  try {
    const [summaryResponse, optionsResponse] = await Promise.all([
      authenticatedApi(fetch, cookies, `/pymes/summary/?${query}`),
      authenticatedApi(fetch, cookies, '/pymes/options/')
    ]);
    if (!summaryResponse.ok || !optionsResponse.ok) throw new Error();
    return {
      summary: await summaryResponse.json() as Summary,
      options: await optionsResponse.json() as FilterOptions,
      filters: Object.fromEntries(query), error: null
    };
  } catch {
    return {
      summary: null,
      options: { work_types: [], enterprise_types: [], sectors: [], provinces: [] } as FilterOptions,
      filters: Object.fromEntries(query), error: 'No pudimos calcular el diagnóstico empresarial.'
    };
  }
};
