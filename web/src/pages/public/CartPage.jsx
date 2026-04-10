import SectionHeading from "../../components/shared/SectionHeading";
import StorefrontCard from "../../components/shared/StorefrontCard";
import StorefrontButton from "../../components/shared/StorefrontButton";
import { CART_SUMMARY_ITEMS } from "../../design/tokens";

export default function CartPage() {
    return (
        <section className="page-shell">
            <SectionHeading
                eyebrow="Carrito"
                title="Resumen visual de compra preparado para la siguiente fase"
                description="Esta vista aún no consume un carrito real, pero ya ordena la interfaz para subtotales, estados vacíos y transición al checkout."
            />

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

            <div className="public-hero__actions">
                <StorefrontButton to="/products" variant="ghost">
                    Volver a productos
                </StorefrontButton>
                <StorefrontButton to="/checkout" variant="primary">
                    Ir a checkout
                </StorefrontButton>
            </div>
        </section>
    );
}