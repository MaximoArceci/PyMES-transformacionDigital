// See https://kit.svelte.dev/docs/types#app
// for information about these interfaces
declare global {
	namespace App {
		interface Locals {
			user: { email: string } | null;
		}
		interface PageData {
			user?: { email: string } | null;
		}
		// interface PageState {}
		// interface Platform {}
	}
}

export {};
