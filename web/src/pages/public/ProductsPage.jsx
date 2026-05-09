import SectionHeading from "../../components/shared/SectionHeading";
import StorefrontCard from "../../components/shared/StorefrontCard";
import StorefrontButton from "../../components/shared/StorefrontButton";
import { PRODUCTS_PREVIEW } from "../../design/tokens";

export default function ProductsPage() {
    return (
        <section className="public-page-frame public-page-frame--editorial public-page-frame--section-layers">
            <div className="page-shell page-shell--products">
                <div className="page-shell__editorial-inner">
                    <SectionHeading
                        eyebrow="Productos"
                        title="Catálogo público base con mejor lenguaje visual"
                        description="La lógica sigue siendo de placeholder, pero esta vista ya prepara la futura lectura de cards, filtros, stock y recorrido hacia el detalle de producto."
                    />

                    <div className="storefront-grid storefront-grid--3">
                        {PRODUCTS_PREVIEW.map((product) => (
                            <StorefrontCard
                                key={product.title}
                                eyebrow={product.eyebrow}
                                title={product.title}
                                description={product.description}
                                meta={product.meta}
                                highlight="mango"
                            />
                        ))}
                    </div>

                    <div className="stack-panel">
                        <div className="info-panel">
                            <h3>Siguiente bloque natural</h3>
                            <p>
                                El catálogo detallado llegará en
                                `feature/storefront-catalog-detail`, donde recién tendrá
                                sentido trabajar con categorías, stock y contratos reales
                                del backend.
                            </p>
                        </div>

                        <StorefrontButton to="/cart" variant="secondary">
                            Continuar al carrito shell
                        </StorefrontButton>
                    </div>
                </div>
            </div>
        </section>
    );
}