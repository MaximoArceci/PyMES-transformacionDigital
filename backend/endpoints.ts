import { Elysia, t } from "elysia";
import { pyme } from "./schemas";

export const router = new Elysia();

router.get('/pymes', async ({}) => {
	return [
        {
            name: "EcoConsulting",
            lat: -34.603722,
            lng: -58.381592,
            trabajoRealizado: "Sustentabilidad",
            tipoEmpresa: "Consultoría ambiental",
            sector: "Servicios"
        },
        {
            name: "Tech Innovators",
            lat: -34.6083,
            lng: -58.3712,
            trabajoRealizado: "Transformación digital",
            tipoEmpresa: "Desarrollo de software",
            sector: "Tecnología"
        },
        {
            name: "AutoPro",
            lat: -34.6099,
            lng: -58.3891,
            trabajoRealizado: "Mejora de procesos",
            tipoEmpresa: "Taller mecánico",
            sector: "Automotriz"
        },
        {
            name: "Mecánica Avanzada",
            lat: -34.6116,
            lng: -58.4039,
            trabajoRealizado: "Innovación",
            tipoEmpresa: "Taller mecánico",
            sector: "Automotriz"
        },
        {
            name: "Green Solutions",
            lat: -34.6143,
            lng: -58.3771,
            trabajoRealizado: "Sustentabilidad",
            tipoEmpresa: "Consultoría ambiental",
            sector: "Servicios"
        },
        {
            name: "Digital Boost",
            lat: -34.6171,
            lng: -58.3928,
            trabajoRealizado: "Transformación digital",
            tipoEmpresa: "Marketing digital",
            sector: "Comunicaciones"
        },
        {
            name: "Textiles Premium",
            lat: -34.6201,
            lng: -58.4048,
            trabajoRealizado: "Mejora de procesos",
            tipoEmpresa: "Textil",
            sector: "Moda"
        },
        {
            name: "Fábrica Creativa",
            lat: -34.6057,
            lng: -58.3716,
            trabajoRealizado: "Innovación",
            tipoEmpresa: "Textil",
            sector: "Moda"
        }
    ];	
},{
	response: t.Array(pyme)
});