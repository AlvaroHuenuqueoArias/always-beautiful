import { useNavigate } from "react-router-dom";

import SectionHeading from "../../components/shared/SectionHeading";
import StorefrontCard from "../../components/shared/StorefrontCard";
import { BOOKING_FLOW } from "../../design/tokens";

export default function BookingPage() {
    const navigate = useNavigate();

    function handleReturnHome(event) {
        event.preventDefault();
        navigate("/");

        window.requestAnimationFrame(() => {
            window.scrollTo({ top: 0, left: 0, behavior: "auto" });
        });
    }

    return (
        <div className="public-page-frame public-page-frame--editorial public-page-frame--section-layers">
            <section className="page-shell">
                <div className="page-shell__editorial-inner">
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
                            meta={[
                                "No requiere agenda real aún",
                                "Preparado para booking"
                            ]}
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

                    <a
                        className="storefront-button storefront-button--primary"
                        href="/"
                        onClick={handleReturnHome}
                    >
                        Volver al inicio
                    </a>
                </div>
            </section>
        </div>
    );
}
