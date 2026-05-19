import SectionHeading from "../../components/shared/SectionHeading";
import StorefrontCard from "../../components/shared/StorefrontCard";
import StorefrontButton from "../../components/shared/StorefrontButton";
import { CART_SUMMARY_ITEMS } from "../../design/tokens";

const ASSISTANT_CART_HANDOFF_STORAGE_KEY =
    "always-beautiful:assistant-cart-handoff";

function readAssistantCartPayload() {
    const storage = globalThis.sessionStorage;

    if (!storage) {
        return null;
    }

    try {
        const value = JSON.parse(
            storage.getItem(ASSISTANT_CART_HANDOFF_STORAGE_KEY)
        );

        return value && typeof value === "object" && !Array.isArray(value)
            ? value
            : null;
    } catch {
        return null;
    }
}

function getSelectedServices(cartPayload) {
    if (Array.isArray(cartPayload?.items) && cartPayload.items.length > 0) {
        return cartPayload.items
            .map((item) => item?.service_label)
            .filter((serviceLabel) => typeof serviceLabel === "string");
    }

    return typeof cartPayload?.service_label === "string"
        ? [cartPayload.service_label]
        : [];
}

export default function CartPage() {
    const assistantCartPayload = readAssistantCartPayload();
    const selectedServices = getSelectedServices(assistantCartPayload);
    const hasAssistantReservation = selectedServices.length > 0;

    return (
        <div className="public-page-frame public-page-frame--editorial public-page-frame--section-layers">
            <section className="page-shell">
                <div className="page-shell__editorial-inner">
                    <SectionHeading
                        eyebrow="Carrito"
                        title={
                            hasAssistantReservation
                                ? "Always Beautiful — Reserva pendiente"
                                : "Resumen visual de compra preparado para la siguiente fase"
                        }
                        description={
                            hasAssistantReservation
                                ? "El assistant preparó un borrador de abono web. La reserva no queda confirmada hasta validación operativa del salón."
                                : "Esta vista aún no consume un carrito real, pero ya ordena la interfaz para subtotales, estados vacíos y transición al checkout."
                        }
                    />

                    {hasAssistantReservation ? (
                        <StorefrontCard
                            eyebrow="Reserva pendiente"
                            title="Comprobante preparado"
                            description="Este comprobante organiza la solicitud antes del pago real. No confirma disponibilidad, monto final ni reserva."
                            meta={[
                                `Profesional: ${
                                    assistantCartPayload.professional_label ||
                                    "pendiente"
                                }`,
                                `Abono web: ${
                                    assistantCartPayload.deposit_percentage || 20
                                }%`,
                                `Saldo restante: ${
                                    assistantCartPayload.remaining_percentage || 80
                                }%`,
                            ]}
                            highlight="pink"
                            className="assistant-cart-receipt"
                        >
                            <div className="assistant-cart-receipt__section">
                                <p className="assistant-cart-receipt__label">
                                    Servicios seleccionados
                                </p>
                                <ul className="assistant-cart-receipt__services">
                                    {selectedServices.map((serviceLabel) => (
                                        <li key={serviceLabel}>{serviceLabel}</li>
                                    ))}
                                </ul>
                            </div>

                            <dl className="assistant-cart-receipt__details">
                                <div>
                                    <dt>Estado</dt>
                                    <dd>pendiente de confirmación</dd>
                                </div>
                                <div>
                                    <dt>Monto final</dt>
                                    <dd>pendiente de confirmación</dd>
                                </div>
                            </dl>

                            <p className="assistant-cart-receipt__note">
                                Nota: el comprobante y las instrucciones de pago del saldo restante serán enviados al correo registrado.
                            </p>
                        </StorefrontCard>
                    ) : (
                        <div className="storefront-grid storefront-grid--2">
                            <StorefrontCard
                                eyebrow="Estado actual"
                                title="Carrito shell"
                                description="La lógica comercial vendrá después. En esta fase se ordena la composición visual, el tono de marca y la experiencia base."
                                meta={["Sin ítems reales", "Fase visual"]}
                                highlight="graphite"
                            />

                            <StorefrontCard
                                eyebrow="Checklist"
                                title="Qué deberá soportar esta vista"
                                description="Aquí se consolidan los elementos que más adelante deberá mostrar el carrito real del proyecto."
                                meta={CART_SUMMARY_ITEMS}
                                highlight="pink"
                            />
                        </div>
                    )}

                    <div className="public-hero__actions">
                        <StorefrontButton to="/products" variant="ghost">
                            Volver a productos
                        </StorefrontButton>

                        <StorefrontButton to="/checkout" variant="primary">
                            Ir a checkout
                        </StorefrontButton>
                    </div>
                </div>
            </section>
        </div>
    );
}
