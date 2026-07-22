import { fail, redirect } from '@sveltejs/kit';
import { publicApi, setSession } from '$lib/server/api';

export const actions = {
  default: async ({ request, fetch, cookies, url }) => {
    const form = await request.formData();
    const email = String(form.get('email') || '').trim().toLowerCase();
    const password = String(form.get('password') || '');
    if (!email || !password) return fail(400, { error: 'Completá correo y contraseña.', email });
    const response = await publicApi(fetch, '/token/', {
      method: 'POST', headers: { 'content-type': 'application/json' }, body: JSON.stringify({ email, password })
    });
    if (!response.ok) return fail(400, { error: 'El correo o la contraseña no son correctos.', email });
    const tokens = await response.json() as { access: string; refresh: string };
    setSession(cookies, tokens, email);
    const next = url.searchParams.get('next');
    throw redirect(303, next?.startsWith('/') && !next.startsWith('//') ? next : '/pymes');
  }
};
