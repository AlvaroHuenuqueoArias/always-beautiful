import SectionHeading from "../shared/SectionHeading";
import StorefrontCard from "../shared/StorefrontCard";
import { FEATURED_PRODUCTS } from "../../data/storefront/products";

export default function FeaturedProductsSection() {
    return (
        <section className="page-shell__section">
            <SectionHeading
                eyebrow="Productos"
                title="Productos destacados como extensión del cuidado"
                description="En esta etapa los productos aparecen como apoyo visual secundario, preparando el camino para una integración posterior más completa del catálogo."
            />

            <div className="storefront-grid storefront-grid--4">
                {FEATURED_PRODUCTS.slice(0, 4).map((product) => (
                    <StorefrontCard
                        key={product.id}
                        eyebrow={product.category}
                        title={product.name}
                        description={product.description}
                        meta={[product.price]}
                        highlight="graphite"
                    />
                ))}
            </div>
        </section>
    );
}