import SectionHeading from "../../components/shared/SectionHeading";
import StorefrontCard from "../../components/shared/StorefrontCard";
import {
    SERVICE_CATEGORIES,
    SERVICES_CONTENT
} from "../../data/storefront/services";

export default function ServicesPage() {
    return (
        <section className="public-page-frame public-page-frame--editorial public-page-frame--section-layers public-page-frame--services">
            <div className="page-shell page-shell--services">
                <div className="page-shell__editorial-inner">
                    <SectionHeading
                        eyebrow="Servicios"
                        title="Servicios diseñados para una experiencia clara, cálida y profesional"
                        description="Explora la oferta principal de Always Beautiful y avanza hacia la reserva con mayor claridad, manteniendo una lectura elegante y comercial."
                    />

                    <div className="category-chip-row">
                        {SERVICE_CATEGORIES.map((category) => (
                            <span key={category} className="signal-chip">
                                {category}
                            </span>
                        ))}
                    </div>

                    <div className="storefront-grid storefront-grid--3">
                        {SERVICES_CONTENT.map((service) => (
                            <article
                                key={service.id}
                                className="service-card-shell"
                            >
                                <StorefrontCard
                                    eyebrow={service.category}
                                    title={service.name}
                                    description={service.description}
                                    meta={[
                                        service.duration,
                                        service.price,
                                        service.professional
                                    ]}
                                    highlight={
                                        service.priority === "alta"
                                            ? "pink"
                                            : "camel"
                                    }
                                />
                            </article>
                        ))}
                    </div>
                </div>
            </div>
        </section>
    );
}