import { fail, redirect } from '@sveltejs/kit';
import { publicApi, setSession } from '$lib/server/api';

function responseDetail(payload: unknown) {
  if (!payload || typeof payload !== 'object') return undefined;
  const record = payload as Record<string, unknown>;
  for (const key of ['detail', 'message', 'error']) {
    if (typeof record[key] === 'string') return record[key] as string;
  }
  const firstValue = Object.values(record)[0];
  if (typeof firstValue === 'string') return firstValue;
  if (Array.isArray(firstValue) && typeof firstValue[0] === 'string') return firstValue[0];
  return undefined;
}

function responseRequestId(payload: unknown) {
  if (!payload || typeof payload !== 'object') return undefined;
  const requestId = (payload as Record<string, unknown>).request_id;
  return typeof requestId === 'string' ? requestId : undefined;
}

export const actions = {
  default: async ({ request, fetch, cookies, url }) => {
    const form = await request.formData();
    const email = String(form.get('email') || '').trim().toLowerCase();
    const password = String(form.get('password') || '');
    if (!email || !password) {
      return fail(400, {
        error: 'Completá correo y contraseña.',
        errorCode: undefined,
        errorDetail: undefined,
        email
      });
    }

    let response: Response;
    try {
      response = await publicApi(fetch, '/token/', {
        method: 'POST', headers: { 'content-type': 'application/json' }, body: JSON.stringify({ email, password })
      });
    } catch (error) {
      return fail(503, {
        error: 'No se pudo conectar con el servidor de autenticación.',
        errorCode: 'AUTH_API_UNREACHABLE',
        errorDetail: error instanceof Error ? error.message : 'Error de conexión desconocido.',
        email
      });
    }

    let payload: unknown;
    try {
      payload = await response.json();
    } catch {
      return fail(502, {
        error: 'El servidor de autenticación devolvió una respuesta inválida.',
        errorCode: `AUTH_INVALID_RESPONSE_${response.status}`,
        errorDetail: `HTTP ${response.status}: se esperaba una respuesta JSON.`,
        email
      });
    }

    if (!response.ok) {
      const detail = responseDetail(payload) || `La API respondió con HTTP ${response.status}.`;
      const requestId = responseRequestId(payload);
      return fail(response.status, {
        error: response.status === 401
          ? 'El correo o la contraseña no son correctos.'
          : 'El servidor rechazó el inicio de sesión.',
        errorCode: `AUTH_HTTP_${response.status}`,
        errorDetail: requestId ? `${detail} · Request ID: ${requestId}` : detail,
        email
      });
    }

    const tokens = payload as Partial<{ access: string; refresh: string }>;
    if (!tokens.access || !tokens.refresh) {
      return fail(502, {
        error: 'El servidor de autenticación no devolvió una sesión válida.',
        errorCode: 'AUTH_TOKENS_MISSING',
        errorDetail: 'La respuesta no contiene los tokens access y refresh.',
        email
      });
    }

    setSession(cookies, { access: tokens.access, refresh: tokens.refresh }, email);
    const next = url.searchParams.get('next');
    throw redirect(303, next?.startsWith('/') && !next.startsWith('//') ? next : '/pymes');
  }
};
