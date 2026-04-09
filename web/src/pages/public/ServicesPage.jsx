export default function ServicesPage() {
    return (
        <section className="public-page">
            <p className="public-page__eyebrow">Servicios</p>
            <h1 className="public-page__title">Vista pública de servicios</h1>
            <p className="public-page__description">
                Esta pantalla tomará como referencia funcional la página
                `services.php` del proyecto guía. Más adelante incorporará cards,
                categorías, precios, descripciones y filtros visuales.
            </p>

            <div className="public-card public-card--wide">
                <h2>Estado actual de la fase</h2>
                <p>
                    En esta rama solo se registra la ruta pública y el shell de
                    navegación. La implementación visual detallada llegará en la
                    fase `feature/storefront-home-services`.
                </p>
            </div>
        </section>
    );
}