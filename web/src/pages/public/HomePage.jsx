export default function HomePage() {
    return (
        <section className="public-page">
            <div className="public-page__hero">
                <p className="public-page__eyebrow">Storefront MVP</p>
                <h1 className="public-page__title">
                    Home pública inspirada en el recorrido funcional del repositorio guía
                </h1>
                <p className="public-page__description">
                    Esta pantalla reemplazará la futura home comercial del
                    negocio. Más adelante incorporará hero, narrativa de marca,
                    servicios destacados, productos seleccionados, equipo y
                    bloques promocionales.
                </p>
            </div>

            <div className="public-page__placeholder-grid">
                <article className="public-card">
                    <h2>Hero principal</h2>
                    <p>Bloque reservado para mensaje comercial principal y CTA.</p>
                </article>

                <article className="public-card">
                    <h2>Servicios destacados</h2>
                    <p>Bloque reservado para preview de servicios del salón.</p>
                </article>

                <article className="public-card">
                    <h2>Equipo / profesionales</h2>
                    <p>Bloque reservado para mostrar especialistas ficticios o reales.</p>
                </article>

                <article className="public-card">
                    <h2>Productos destacados</h2>
                    <p>Bloque reservado para preview del catálogo público.</p>
                </article>
            </div>
        </section>
    );
}