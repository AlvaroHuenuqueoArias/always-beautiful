export default function ProductsPage() {
    return (
        <section className="public-page">
            <p className="public-page__eyebrow">Productos</p>
            <h1 className="public-page__title">Catálogo público base</h1>
            <p className="public-page__description">
                Esta pantalla será la traducción inicial de `products.php` a
                React/Vite. Más adelante incluirá filtros, categorías, cards de
                producto, estado de stock y transición hacia carrito.
            </p>

            <div className="public-card public-card--wide">
                <h2>Implementación posterior</h2>
                <p>
                    El catálogo detallado se construirá en la fase
                    `feature/storefront-catalog-detail`, utilizando datos
                    ficticios o reales según disponibilidad.
                </p>
            </div>
        </section>
    );
}