export default function CartPage() {
    return (
        <section className="public-page">
            <p className="public-page__eyebrow">Carrito</p>
            <h1 className="public-page__title">Resumen visual de compra</h1>
            <p className="public-page__description">
                Esta pantalla representará el equivalente visual de `cart.php`
                dentro del nuevo storefront. Más adelante incluirá ítems,
                cantidades, subtotales, estados vacíos y transición hacia
                checkout.
            </p>

            <div className="public-card public-card--wide">
                <h2>Fase posterior</h2>
                <p>
                    La implementación real del carrito se abordará en la fase
                    `feature/storefront-cart-checkout-shell`.
                </p>
            </div>
        </section>
    );
}