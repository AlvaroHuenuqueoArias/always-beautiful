export const STOREFRONT_THEME = {
    brandKicker: "Salón de Belleza",
    palette: {
        background: "#f4ede5",
        surface: "#fbf5ef",
        surfaceStrong: "#fffaf5",
        textPrimary: "#1f1713",
        textSecondary: "#67584b",
        magenta: "#bb7a45",
        magentaSoft: "#ebd2b5",
        salmon: "#d6a072",
        terracotta: "#8e5e3b",
        cream: "#f6ede5",
        black: "#17120f",
        graphite: "#3b3029",
        mango: "#c68752",
        mangoSoft: "#e7c7a4"
    }
};

export const STOREFRONT_NAV_ITEMS = [
    { to: "/", label: "Inicio" },
    { to: "/services", label: "Servicios" },
    { to: "/products", label: "Productos" },
    { to: "/booking", label: "Reservas" }
];

export const STOREFRONT_CART_ITEM = {
    to: "/cart",
    label: "🛒",
    ariaLabel: "Carrito"
};

/**
 * Capa de compatibilidad (legacy exports)
 * Estas constantes siguen siendo consumidas por:
 * - ProductsPage.jsx
 * - BookingPage.jsx
 * - CartPage.jsx
 * - CheckoutPage.jsx
 *
 * En una rama futura, refactorizaremos esas páginas para consumir data/storefront/*
 * y podremos eliminar esta sección.
 */

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