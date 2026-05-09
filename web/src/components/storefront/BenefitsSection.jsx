import SectionHeading from "../shared/SectionHeading";
import StorefrontCard from "../shared/StorefrontCard";
import { BENEFITS_CONTENT } from "../../data/storefront/brand";

export default function BenefitsSection() {
    return (
        <section className="page-shell__section">
            <SectionHeading
                eyebrow="Diferenciales"
                title="Una experiencia diseñada con calidad, calidez y detalle"
                description="Always Beautiful combina atención personalizada, claridad en la reserva y una experiencia pensada para transmitir confianza desde el primer contacto."
            />

            <div className="storefront-grid storefront-grid--3">
                {BENEFITS_CONTENT.map((benefit) => (
                    <StorefrontCard
                        key={benefit.id}
                        eyebrow={benefit.eyebrow}
                        title={benefit.title}
                        description={benefit.description}
                        highlight="pink"
                    />
                ))}
            </div>
        </section>
    );
}