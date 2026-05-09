export const SERVICES_CONTENT = [
    {
        id: "corte-cabello",
        name: "Corte de cabello",
        category: "Cabello",
        description:
            "Corte personalizado para hombre, mujer y niños, adaptado al estilo y necesidad del cliente.",
        duration: "30 - 45 min",
        price: "Desde $10.000",
        requiresBooking: true,
        featured: true,
        professional: "Estilista / Cosmetóloga",
        priority: "alta"
    },
    {
        id: "coloracion-capilar",
        name: "Coloración capilar",
        category: "Coloración",
        description:
            "Aplicación de color completo, retoque de raíces o baño de color con productos profesionales.",
        duration: "1.5 - 2 h",
        price: "Desde $30.000",
        requiresBooking: true,
        featured: true,
        professional: "Estilista / Cosmetóloga",
        priority: "alta"
    },
    {
        id: "mechas-balayage",
        name: "Mechas y balayage",
        category: "Coloración",
        description:
            "Técnicas avanzadas de iluminación como balayage, babylights o visos para un resultado natural y moderno.",
        duration: "2 - 3 h",
        price: "Desde $60.000",
        requiresBooking: true,
        featured: true,
        professional: "Estilista / Cosmetóloga",
        priority: "alta"
    },
    {
        id: "alisado-capilar",
        name: "Alisado capilar",
        category: "Tratamientos capilares",
        description:
            "Alisado profesional que reduce el frizz y deja el cabello suave, manejable y brillante.",
        duration: "2 - 3 h",
        price: "Desde $50.000",
        requiresBooking: true,
        featured: true,
        professional: "Estilista / Cosmetóloga",
        priority: "alta"
    },
    {
        id: "botox-capilar",
        name: "Botox capilar",
        category: "Tratamientos capilares",
        description:
            "Tratamiento intensivo de nutrición que repara y revitaliza el cabello dañado.",
        duration: "1 - 1.5 h",
        price: "Desde $35.000",
        requiresBooking: true,
        featured: true,
        professional: "Estilista / Cosmetóloga",
        priority: "alta"
    },
    {
        id: "masaje-capilar",
        name: "Masaje capilar",
        category: "Tratamientos capilares",
        description:
            "Tratamiento hidratante que fortalece y mejora la salud del cabello.",
        duration: "30 - 45 min",
        price: "Desde $15.000",
        requiresBooking: true,
        featured: false,
        professional: "Estilista / Cosmetóloga",
        priority: "media"
    },
    {
        id: "peinados-brushing",
        name: "Peinados y brushing",
        category: "Peinados",
        description:
            "Peinados profesionales y brushing para ocasiones especiales o uso diario.",
        duration: "30 - 60 min",
        price: "Desde $12.000",
        requiresBooking: true,
        featured: true,
        professional: "Cosmetóloga",
        priority: "media"
    },
    {
        id: "depilacion-facial",
        name: "Depilación facial",
        category: "Depilación",
        description:
            "Eliminación de vello facial en distintas zonas con técnicas profesionales.",
        duration: "15 - 30 min",
        price: "Desde $5.000",
        requiresBooking: true,
        featured: false,
        professional: "Cosmetóloga",
        priority: "media"
    },
    {
        id: "depilacion-corporal",
        name: "Depilación corporal",
        category: "Depilación",
        description:
            "Servicio de depilación en distintas zonas del cuerpo con resultados duraderos.",
        duration: "30 - 60 min",
        price: "Desde $10.000",
        requiresBooking: true,
        featured: false,
        professional: "Cosmetóloga",
        priority: "media"
    },
    {
        id: "manicure",
        name: "Manicure",
        category: "Manos y uñas",
        description:
            "Cuidado y embellecimiento de uñas con opciones tradicionales o permanentes.",
        duration: "45 - 60 min",
        price: "Desde $10.000",
        requiresBooking: true,
        featured: true,
        professional: "Cosmetóloga",
        priority: "media"
    },
    {
        id: "pedicure",
        name: "Pedicure",
        category: "Pies",
        description:
            "Tratamiento completo para el cuidado y estética de los pies.",
        duration: "45 - 60 min",
        price: "Desde $15.000",
        requiresBooking: true,
        featured: true,
        professional: "Cosmetóloga",
        priority: "media"
    },
    {
        id: "limpieza-facial",
        name: "Limpieza facial",
        category: "Tratamientos faciales",
        description:
            "Limpieza profunda de la piel que mejora la textura y apariencia del rostro.",
        duration: "60 min",
        price: "Desde $20.000",
        requiresBooking: true,
        featured: true,
        professional: "Cosmetóloga",
        priority: "media"
    },
    {
        id: "lifting-pestanas",
        name: "Lifting de pestañas",
        category: "Pestañas",
        description:
            "Realce natural de pestañas que otorga curvatura y definición sin extensiones.",
        duration: "45 min",
        price: "Desde $18.000",
        requiresBooking: true,
        featured: true,
        professional: "Cosmetóloga",
        priority: "media"
    },
    {
        id: "maquillaje-profesional",
        name: "Maquillaje profesional",
        category: "Maquillaje",
        description:
            "Maquillaje para eventos, día o noche, adaptado al estilo del cliente.",
        duration: "45 - 60 min",
        price: "Desde $25.000",
        requiresBooking: true,
        featured: false,
        professional: "Cosmetóloga",
        priority: "media"
    }
];

export const FEATURED_SERVICES = SERVICES_CONTENT.filter((service) => service.featured).slice(0, 6);

export const SERVICE_CATEGORIES = [
    "Cabello",
    "Coloración",
    "Tratamientos capilares",
    "Peinados",
    "Depilación",
    "Manos y uñas",
    "Pies",
    "Tratamientos faciales",
    "Pestañas",
    "Maquillaje"
];