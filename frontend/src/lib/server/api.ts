import { env } from '$env/dynamic/private';
import type { Cookies } from '@sveltejs/kit';

const API_BASE = (env.PRIVATE_API_BASE_URL || 'http://localhost:9000/api').replace(/\/$/, '');
const cookieOptions = {
  path: '/',
  httpOnly: true,
  sameSite: 'lax' as const,
  secure: env.NODE_ENV === 'production'
};

export function setSession(cookies: Cookies, tokens: { access: string; refresh: string }, email: string) {
  cookies.set('pymes_access', tokens.access, { ...cookieOptions, maxAge: 60 * 15 });
  cookies.set('pymes_refresh', tokens.refresh, { ...cookieOptions, maxAge: 60 * 60 * 24 * 7 });
  cookies.set('pymes_user', email, { ...cookieOptions, maxAge: 60 * 60 * 24 * 7 });
}

export function clearSession(cookies: Cookies) {
  for (const name of ['pymes_access', 'pymes_refresh', 'pymes_user']) cookies.delete(name, { path: '/' });
}

export async function publicApi(fetcher: typeof fetch, path: string, init?: RequestInit) {
  return fetcher(`${API_BASE}${path}`, init);
}

async function refreshAccess(fetcher: typeof fetch, cookies: Cookies) {
  const refresh = cookies.get('pymes_refresh');
  if (!refresh) return undefined;
  const response = await publicApi(fetcher, '/token/refresh/', {
    method: 'POST', headers: { 'content-type': 'application/json' }, body: JSON.stringify({ refresh })
  });
  if (!response.ok) { clearSession(cookies); return undefined; }
  const payload = await response.json() as { access: string };
  cookies.set('pymes_access', payload.access, { ...cookieOptions, maxAge: 60 * 15 });
  return payload.access;
}

export async function authenticatedApi(fetcher: typeof fetch, cookies: Cookies, path: string, init: RequestInit = {}) {
  let access = cookies.get('pymes_access');
  const request = (token?: string | null) => publicApi(fetcher, path, {
    ...init,
    headers: { ...(init.headers || {}), ...(token ? { authorization: `Bearer ${token}` } : {}) }
  });
  let response = await request(access);
  if (response.status === 401 && (access = await refreshAccess(fetcher, cookies))) response = await request(access);
  return response;
}
