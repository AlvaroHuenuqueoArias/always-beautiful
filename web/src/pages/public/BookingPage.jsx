import SectionHeading from "../../components/shared/SectionHeading";
import StorefrontCard from "../../components/shared/StorefrontCard";
import StorefrontButton from "../../components/shared/StorefrontButton";
import { BOOKING_FLOW } from "../../design/tokens";

export default function BookingPage() {
    return (
        <section className="page-shell">
            <SectionHeading
                eyebrow="Reservas"
                title="Shell público de reservas con una base más profesional"
                description="Esta vista sigue siendo de maqueta controlada, pero ya prepara la futura integración de servicios, profesionales, fecha, hora y validaciones."
            />

            <div className="storefront-grid storefront-grid--3">
                {BOOKING_FLOW.map((step) => (
                    <StorefrontCard
                        key={step.title}
                        eyebrow={step.eyebrow}
                        title={step.title}
                        description={step.description}
                        highlight="mango"
                    />
                ))}
            </div>

            <div className="storefront-grid storefront-grid--2">
                <StorefrontCard
                    eyebrow="Datos futuros"
                    title="Profesionales y disponibilidad"
                    description="La siguiente etapa de reservas ya podrá trabajar con profesionales ficticios controlados y luego con datos operativos más cercanos a la realidad."
                    meta={["No requiere agenda real aún", "Preparado para booking"]}
                    highlight="pink"
                />

                <StorefrontCard
                    eyebrow="Dependencias"
                    title="Conexión posterior con backend"
                    description="Esta vista se integrará más adelante con los módulos `booking` y `schedule`, pero hoy su objetivo es puramente estructural y visual."
                    meta={["Shell visual", "Integración futura"]}
                    highlight="graphite"
                />
            </div>

            <StorefrontButton to="/" variant="primary">
                Volver al inicio
            </StorefrontButton>
        </section>
    );
}