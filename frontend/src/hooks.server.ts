import { redirect, type Handle } from '@sveltejs/kit';

const publicRoutes = new Set(['/login', '/register']);

export const handle: Handle = async ({ event, resolve }) => {
  const email = event.cookies.get('pymes_user');
  const hasSession = Boolean(email && event.cookies.get('pymes_refresh'));
  event.locals.user = hasSession ? { email: email as string } : null;
  const path = event.url.pathname;
  if (!publicRoutes.has(path) && !event.locals.user && path !== '/') {
    throw redirect(303, `/login?next=${encodeURIComponent(path + event.url.search)}`);
  }
  if (publicRoutes.has(path) && event.locals.user) throw redirect(303, '/pymes');
  return resolve(event);
};
