export const STOREFRONT_BRAND = {
    name: "Always Beautiful",
    division: "Storefront",
    eyebrow: "Boutique Beauty Experience",
    headline: "Belleza, cuidado y experiencia visual en una sola plataforma",
    description:
        "La capa pública del proyecto está siendo diseñada para presentar servicios, productos y reservas con una identidad más elegante, cálida y profesional.",
    palette: {
        camel: "#b38b6d",
        pink: "#e6cad4",
        graphite: "#3f3f46",
        cream: "#f4e8df",
        mango: "#f1a55d"
    }
};

export const STOREFRONT_NAV_ITEMS = [
    { to: "/", label: "Inicio" },
    { to: "/services", label: "Servicios" },
    { to: "/products", label: "Productos" },
    { to: "/booking", label: "Reservas" },
    { to: "/cart", label: "Carrito" }
];

export const STOREFRONT_TRUST_POINTS = [
    "Estética boutique",
    "Reserva simple",
    "Catálogo visual",
    "Checkout preparado"
];

export const HOME_FEATURES = [
    {
        eyebrow: "Experiencia",
        title: "Servicios con identidad premium",
        description:
            "La futura home destacará una propuesta visual elegante, cercana y comercial para presentar el salón con una narrativa más profesional."
    },
    {
        eyebrow: "Operación",
        title: "Agenda y reservas conectadas",
        description:
            "La experiencia pública quedará preparada para conectarse más adelante con los módulos de booking y schedule sin rehacer la base visual."
    },
    {
        eyebrow: "Comercio",
        title: "Catálogo y carrito listos para crecer",
        description:
            "La estructura del storefront ya contempla evolución hacia productos, detalle de catálogo, carrito y transición ordenada a checkout."
    },
    {
        eyebrow: "Escalabilidad",
        title: "Diseño reusable y coherente",
        description:
            "Esta rama formaliza un sistema visual reutilizable para que las siguientes fases no dependan de CSS improvisado por pantalla."
    }
];

export const SERVICES_PREVIEW = [
    {
        eyebrow: "Cabello",
        title: "Color, corte y tratamiento",
        description:
            "Bloque visual pensado para servicios de transformación, mantención y cuidado capilar con una lectura más editorial.",
        meta: ["Preview comercial", "Sin datos reales aún"]
    },
    {
        eyebrow: "Rostro",
        title: "Cosmetología y cuidado facial",
        description:
            "Espacio preparado para integrar servicios estéticos con duración, beneficios y futura categorización visual.",
        meta: ["Fase siguiente", "Datos ficticios"]
    },
    {
        eyebrow: "Manos y estilo",
        title: "Detalles de imagen y acabado",
        description:
            "Sección diseñada para agrupar servicios complementarios con foco en experiencia, presentación y claridad comercial.",
        meta: ["UI de referencia", "Sin conexión real aún"]
    }
];

export const PRODUCTS_PREVIEW = [
    {
        eyebrow: "Catálogo",
        title: "Producto destacado A",
        description:
            "Placeholder para una tarjeta de producto con imagen, categoría, precio, stock y transición futura al detalle.",
        meta: ["Imagen pendiente", "Stock referencial"]
    },
    {
        eyebrow: "Catálogo",
        title: "Producto destacado B",
        description:
            "Esta tarjeta representa el estilo general del storefront para ecommerce, sin depender todavía de inventario real.",
        meta: ["Catálogo base", "Sin backend acoplado aún"]
    },
    {
        eyebrow: "Catálogo",
        title: "Producto destacado C",
        description:
            "Bloque pensado para soportar navegación visual, filtros y posterior integración con el módulo Catalog.",
        meta: ["Vista pública", "Datos de muestra"]
    }
];

export const BOOKING_FLOW = [
    {
        eyebrow: "Paso 1",
        title: "Elegir servicio",
        description:
            "La interfaz quedará preparada para seleccionar el servicio antes de mostrar disponibilidad real."
    },
    {
        eyebrow: "Paso 2",
        title: "Elegir profesional",
        description:
            "Se incorporará una capa visual para asignar atención por profesional, manteniendo consistencia con el backend."
    },
    {
        eyebrow: "Paso 3",
        title: "Elegir fecha y horario",
        description:
            "La agenda visual partirá con datos controlados y luego podrá conectarse al motor de booking y schedule."
    }
];

export const CHECKOUT_FLOW = [
    {
        eyebrow: "Resumen",
        title: "Revisión de compra",
        description:
            "Espacio reservado para productos, cantidades, subtotales y observaciones comerciales."
    },
    {
        eyebrow: "Cliente",
        title: "Datos de contacto y entrega",
        description:
            "Shell visual preparado para dirección, validaciones y estructura posterior de despacho."
    },
    {
        eyebrow: "Pago",
        title: "Transición a pasarela real",
        description:
            "En esta fase no se conecta el pago, pero sí se ordena la experiencia para integrarlo después."
    }
];

export const CART_SUMMARY_ITEMS = [
    "Ítems seleccionados",
    "Subtotales visibles",
    "Estado vacío preparado",
    "Transición ordenada a checkout"
];