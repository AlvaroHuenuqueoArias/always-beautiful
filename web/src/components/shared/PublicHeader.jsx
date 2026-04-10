import { NavLink } from "react-router-dom";
import {
    STOREFRONT_BRAND,
    STOREFRONT_NAV_ITEMS
} from "../../design/tokens";
import StorefrontButton from "./StorefrontButton";

export default function PublicHeader() {
    return (
        <header className="public-header">
            <div className="public-header__container">
                <div className="public-brand-block">
                    <NavLink to="/" className="public-brand">
                        <span className="public-brand__kicker">
                            {STOREFRONT_BRAND.name}
                        </span>
                        <strong className="public-brand__title">
                            {STOREFRONT_BRAND.division}
                        </strong>
                    </NavLink>

                    <p className="public-brand__subtitle">
                        {STOREFRONT_BRAND.eyebrow}
                    </p>
                </div>

                <nav className="public-nav" aria-label="Navegación principal">
                    {STOREFRONT_NAV_ITEMS.map((item) => (
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
                    <StorefrontButton
                        to="/checkout"
                        variant="ghost"
                        size="sm"
                    >
                        Checkout
                    </StorefrontButton>

                    <StorefrontButton
                        to="/admin"
                        variant="primary"
                        size="sm"
                    >
                        Admin
                    </StorefrontButton>
                </div>
            </div>
        </header>
    );
}