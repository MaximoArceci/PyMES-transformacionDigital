import { GET } from '$lib/server/client.js';
import { error } from '@sveltejs/kit';

export const load = async ({ fetch }) => {
	try {
		const { data: pymes, } = await GET("/pymes", { fetch });


		return{ pymes };
	}
	catch (e) {
		throw e;
	}
};
