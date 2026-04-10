import SectionHeading from "../../components/shared/SectionHeading";
import StorefrontCard from "../../components/shared/StorefrontCard";
import StorefrontButton from "../../components/shared/StorefrontButton";
import { CHECKOUT_FLOW } from "../../design/tokens";

export default function CheckoutPage() {
    return (
        <section className="page-shell">
            <SectionHeading
                eyebrow="Checkout"
                title="Shell inicial de confirmación y preparación del pago"
                description="La pasarela real no entra todavía, pero ya se deja una experiencia más madura para revisar compra, datos del cliente y transición futura al pago."
            />

            <div className="storefront-grid storefront-grid--3">
                {CHECKOUT_FLOW.map((step) => (
                    <StorefrontCard
                        key={step.title}
                        eyebrow={step.eyebrow}
                        title={step.title}
                        description={step.description}
                        highlight="camel"
                    />
                ))}
            </div>

            <div className="info-panel">
                <h3>Importante</h3>
                <p>
                    Esta fase no necesita datos reales de pagos ni despacho. Su
                    función es ordenar la experiencia visual del checkout antes de
                    conectar `payments` y `shipping`.
                </p>
            </div>

            <StorefrontButton to="/booking" variant="secondary">
                Ver módulo de reservas
            </StorefrontButton>
        </section>
    );
}