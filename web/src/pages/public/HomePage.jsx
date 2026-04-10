import {
    HOME_FEATURES,
    STOREFRONT_BRAND,
    STOREFRONT_TRUST_POINTS
} from "../../design/tokens";
import SectionHeading from "../../components/shared/SectionHeading";
import StorefrontButton from "../../components/shared/StorefrontButton";
import StorefrontCard from "../../components/shared/StorefrontCard";

export default function HomePage() {
    return (
        <section className="page-shell">
            <section className="public-hero">
                <div className="public-hero__content">
                    <p className="public-page__eyebrow">Storefront MVP</p>

                    <h1 className="public-page__title">{STOREFRONT_BRAND.headline}</h1>

                    <p className="public-page__description">
                        {STOREFRONT_BRAND.description}
                    </p>

                    <div className="public-hero__actions">
                        <StorefrontButton to="/booking" variant="primary">
                            Reservar experiencia
                        </StorefrontButton>

                        <StorefrontButton to="/products" variant="secondary">
                            Explorar catálogo
                        </StorefrontButton>
                    </div>

                    <div className="signal-strip">
                        {STOREFRONT_TRUST_POINTS.map((item) => (
                            <span key={item} className="signal-chip">
                                {item}
                            </span>
                        ))}
                    </div>
                </div>

                <div className="public-hero__media">
                    <div className="placeholder-visual">
                        <span className="placeholder-visual__badge">
                            Placeholder visual
                        </span>
                        <h2>Hero editorial del storefront</h2>
                        <p>
                            Aquí más adelante irá la composición visual principal
                            de la marca con fotografía real o imagen genérica de
                            referencia.
                        </p>
                    </div>
                </div>
            </section>

            <section className="page-shell__section">
                <SectionHeading
                    eyebrow="Base visual"
                    title="Qué estamos construyendo en esta fase"
                    description="Esta rama no cierra aún el negocio visual definitivo, pero sí deja una identidad reusable para que el storefront crezca con coherencia."
                />

                <div className="storefront-grid storefront-grid--4">
                    {HOME_FEATURES.map((item) => (
                        <StorefrontCard
                            key={item.title}
                            eyebrow={item.eyebrow}
                            title={item.title}
                            description={item.description}
                            highlight="pink"
                        />
                    ))}
                </div>
            </section>
        </section>
    );
}