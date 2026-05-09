import SectionHeading from "../shared/SectionHeading";
import StorefrontCard from "../shared/StorefrontCard";
import StorefrontButton from "../shared/StorefrontButton";
import { FEATURED_SERVICES } from "../../data/storefront/services";

export default function FeaturedServicesSection() {
    return (
        <section className="page-shell__section">
            <SectionHeading
                eyebrow="Servicios"
                title="Servicios destacados para una experiencia estética superior"
                description="En esta primera etapa destacamos los servicios más representativos del salón, manteniendo una lectura clara, elegante y enfocada en la reserva."
            />

            <div className="storefront-grid storefront-grid--3">
                {FEATURED_SERVICES.map((service) => (
                    <article key={service.id} className="service-card-shell">
                        <StorefrontCard
                            eyebrow={service.category}
                            title={service.name}
                            description={service.description}
                            meta={[service.duration, service.price]}
                            highlight="camel"
                        />

                        <div className="service-card-shell__actions">
                            <StorefrontButton
                                to="/booking"
                                variant="ghost"
                                size="sm"
                            >
                                Reservar
                            </StorefrontButton>
                        </div>
                    </article>
                ))}
            </div>
        </section>
    );
}