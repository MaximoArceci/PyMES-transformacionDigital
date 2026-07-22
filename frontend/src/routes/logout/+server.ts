import { redirect } from '@sveltejs/kit';
import { clearSession } from '$lib/server/api';
export const POST = ({ cookies }) => { clearSession(cookies); throw redirect(303, '/login'); };
