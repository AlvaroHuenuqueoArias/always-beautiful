import { NavLink } from "react-router-dom";
import { STOREFRONT_BRAND } from "../../design/tokens";

export default function PublicFooter() {
    return (
        <footer className="public-footer">
            <div className="public-footer__container">
                <div className="public-footer__intro">
                    <p className="public-footer__kicker">{STOREFRONT_BRAND.name}</p>
                    <h3 className="public-footer__title">
                        Base visual pública en evolución profesional
                    </h3>
                    <p className="public-footer__text">
                        Esta capa pública está siendo diseñada como storefront
                        oficial del proyecto, separada del panel administrativo y
                        preparada para crecer hacia servicios, productos, reservas,
                        carrito y checkout.
                    </p>
                </div>

                <div className="public-footer__column">
                    <h4 className="public-footer__column-title">Navegación</h4>
                    <div className="public-footer__links">
                        <NavLink to="/">Inicio</NavLink>
                        <NavLink to="/services">Servicios</NavLink>
                        <NavLink to="/products">Productos</NavLink>
                        <NavLink to="/booking">Reservas</NavLink>
                        <NavLink to="/admin">Admin</NavLink>
                    </div>
                </div>

                <div className="public-footer__column">
                    <h4 className="public-footer__column-title">Estado del módulo</h4>
                    <div className="public-footer__meta">
                        <p>Fase actual: Design System</p>
                        <p>Estado: Base visual reusable en construcción</p>
                        <p>Datos reales: no requeridos en esta rama</p>
                    </div>
                </div>
            </div>
        </footer>
    );
}