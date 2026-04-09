import { Link, NavLink } from "react-router-dom";

const NAV_ITEMS = [
    { to: "/", label: "Inicio" },
    { to: "/services", label: "Servicios" },
    { to: "/products", label: "Productos" },
    { to: "/booking", label: "Reservas" },
    { to: "/cart", label: "Carrito" }
];

export default function PublicHeader() {
    return (
        <header className="public-header">
            <div className="public-header__container">
                <Link to="/" className="public-brand">
                    <span className="public-brand__kicker">Always Beautiful</span>
                    <strong className="public-brand__title">Storefront</strong>
                </Link>

                <nav className="public-nav" aria-label="Navegación principal">
                    {NAV_ITEMS.map((item) => (
                        <NavLink
                            key={item.to}
                            to={item.to}
                            className={({ isActive }) =>
                                isActive
                                    ? "public-nav__link public-nav__link--active"
                                    : "public-nav__link"
                            }
                        >
                            {item.label}
                        </NavLink>
                    ))}
                </nav>

                <div className="public-header__actions">
                    <Link to="/checkout" className="public-cta public-cta--secondary">
                        Checkout
                    </Link>
                    <Link to="/admin" className="public-cta public-cta--primary">
                        Admin
                    </Link>
                </div>
            </div>
        </header>
    );
}