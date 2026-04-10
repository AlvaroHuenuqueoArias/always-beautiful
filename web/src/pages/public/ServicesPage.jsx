import SectionHeading from "../../components/shared/SectionHeading";
import StorefrontCard from "../../components/shared/StorefrontCard";
import { SERVICES_PREVIEW } from "../../design/tokens";

export default function ServicesPage() {
    return (
        <section className="page-shell">
            <SectionHeading
                eyebrow="Servicios"
                title="Vista pública de servicios con jerarquía más boutique"
                description="Esta pantalla sigue siendo una base visual, pero ya comienza a parecerse a una sección comercial seria inspirada en el flujo funcional del repositorio guía."
            />

            <div className="storefront-grid storefront-grid--3">
                {SERVICES_PREVIEW.map((service) => (
                    <StorefrontCard
                        key={service.title}
                        eyebrow={service.eyebrow}
                        title={service.title}
                        description={service.description}
                        meta={service.meta}
                        highlight="camel"
                    />
                ))}
            </div>

            <div className="info-panel">
                <h3>Nota de implementación</h3>
                <p>
                    En esta rama todavía no usamos servicios reales ni precios
                    definitivos. Aquí solo se formaliza la estructura visual
                    reusable que luego consumirá datos reales o controlados.
                </p>
            </div>
        </section>
    );
}