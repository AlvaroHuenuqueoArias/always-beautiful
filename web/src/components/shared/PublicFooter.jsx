export default function PublicFooter() {
    return (
        <footer className="public-footer">
            <div className="public-footer__container">
                <div>
                    <p className="public-footer__kicker">Always Beautiful</p>
                    <h3 className="public-footer__title">Storefront en construcción profesional</h3>
                    <p className="public-footer__text">
                        Esta capa pública será la base comercial y visual del
                        proyecto, separada del panel administrativo y preparada
                        para crecer hacia reservas, catálogo, carrito y checkout.
                    </p>
                </div>

                <div className="public-footer__meta">
                    <p>Fase actual: Public Shell + Routing</p>
                    <p>Estado: Base estructural en implementación</p>
                </div>
            </div>
        </footer>
    );
}