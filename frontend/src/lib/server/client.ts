import createClient from "openapi-fetch";
import { SECRET_BACKEND_URL } from "$env/static/private";

const { GET, POST, PATCH, PUT, DELETE } = createClient({ baseUrl: SECRET_BACKEND_URL });

export {
	GET,
	POST,
	PATCH,
	PUT,
	DELETE,
}