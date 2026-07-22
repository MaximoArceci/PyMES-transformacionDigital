import { fail, redirect } from '@sveltejs/kit';
import { publicApi, setSession } from '$lib/server/api';

export const actions = {
  default: async ({ request, fetch, cookies }) => {
    const form = await request.formData();
    const email = String(form.get('email') || '').trim().toLowerCase();
    const password = String(form.get('password') || '');
    const confirm = String(form.get('confirm') || '');
    if (password !== confirm) return fail(400, { error: 'Las contraseñas no coinciden.', email });
    const created = await publicApi(fetch, '/auth/register/', {
      method: 'POST', headers: { 'content-type': 'application/json' }, body: JSON.stringify({ email, password })
    });
    if (!created.ok) {
      const payload = await created.json().catch(() => ({}));
      const detail = payload.email?.[0] || payload.password?.[0] || 'No pudimos crear la cuenta.';
      return fail(400, { error: detail, email });
    }
    const login = await publicApi(fetch, '/token/', {
      method: 'POST', headers: { 'content-type': 'application/json' }, body: JSON.stringify({ email, password })
    });
    if (!login.ok) return fail(400, { error: 'La cuenta se creó, pero no pudimos iniciar sesión.', email });
    setSession(cookies, await login.json(), email);
    throw redirect(303, '/pymes');
  }
};
