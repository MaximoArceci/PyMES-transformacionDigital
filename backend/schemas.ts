import { t } from 'elysia';

export const pyme = t.Object({
	name: t.String(),
	lat: t.Number(),
	lng: t.Number(),
	trabajoRealizado: t.String(),
	tipoEmpresa: t.String(),
	sector: t.String()
})