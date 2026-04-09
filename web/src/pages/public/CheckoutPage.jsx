export default function CheckoutPage() {
    return (
        <section className="public-page">
            <p className="public-page__eyebrow">Checkout</p>
            <h1 className="public-page__title">Shell inicial del checkout</h1>
            <p className="public-page__description">
                Esta vista servirá como base para el flujo de confirmación y
                preparación del pago, inspirado en la secuencia funcional del
                repositorio guía, pero adaptado a nuestra arquitectura.
            </p>

            <div className="public-card public-card--wide">
                <h2>Nota importante</h2>
                <p>
                    En esta fase no se conectarán pasarelas reales. El objetivo
                    actual es dejar la ruta y la estructura visual preparadas.
                </p>
            </div>
        </section>
    );
}