import { useState } from "react";
import { NavLink } from "react-router-dom";
import { STOREFRONT_CART_ITEM, STOREFRONT_NAV_ITEMS } from "../../design/tokens";

export default function PublicHeader() {
    const [isMenuOpen, setIsMenuOpen] = useState(false);

    const mobileNavItems = STOREFRONT_NAV_ITEMS;

    function closeMobileMenu() {
        setIsMenuOpen(false);
    }

    return (
        <header
            className={
                isMenuOpen
                    ? "public-header public-header--menu-open"
                    : "public-header"
            }
        >
            <div className="public-header__container">
                <div className="public-header__left-spacer">
                    <NavLink
                        to="/"
                        aria-label="Always Beautiful"
                        className="public-header__brand-link"
                        onClick={closeMobileMenu}
                    >
                        <img
                            src="/images/storefront/home/logo.png"
                            alt="Always Beautiful"
                            className="public-header__brand-logo"
                        />
                    </NavLink>
                </div>

                <nav
                    className="public-nav public-nav--desktop"
                    aria-label="Navegación principal"
                >
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
                    <button
                        type="button"
                        className="public-header__menu-toggle"
                        aria-label={
                            isMenuOpen
                                ? "Cerrar navegación pública"
                                : "Abrir navegación pública"
                        }
                        aria-expanded={isMenuOpen}
                        aria-controls="public-mobile-menu"
                        onClick={() => setIsMenuOpen((current) => !current)}
                    >
                        <span
                            className="public-header__menu-icon"
                            aria-hidden="true"
                        >
                            <span />
                            <span />
                            <span />
                        </span>
                    </button>

                    <div className="public-header__cart-slot">
                        <NavLink
                            to={STOREFRONT_CART_ITEM.to}
                            aria-label={STOREFRONT_CART_ITEM.ariaLabel}
                            className={({ isActive }) =>
                                isActive
                                    ? "public-header__cart-link public-header__cart-link--active"
                                    : "public-header__cart-link"
                            }
                            onClick={closeMobileMenu}
                        >
                            <span className="public-header__cart-badge">
                                <span
                                    className="public-header__cart-icon"
                                    aria-hidden="true"
                                >
                                    <svg
                                        className="public-header__cart-svg"
                                        viewBox="0 0 24 24"
                                        fill="none"
                                        xmlns="http://www.w3.org/2000/svg"
                                    >
                                        <path
                                            d="M3 4H5L7.2 14.2C7.32 14.76 7.8 15.16 8.38 15.16H17.56C18.12 15.16 18.6 14.78 18.74 14.24L20.4 8H6.1"
                                            stroke="currentColor"
                                            strokeWidth="1.9"
                                            strokeLinecap="round"
                                            strokeLinejoin="round"
                                        />
                                        <circle
                                            cx="9.5"
                                            cy="19"
                                            r="1.4"
                                            fill="currentColor"
                                        />
                                        <circle
                                            cx="17"
                                            cy="19"
                                            r="1.4"
                                            fill="currentColor"
                                        />
                                    </svg>
                                </span>
                            </span>
                        </NavLink>
                    </div>
                </div>

                <div
                    id="public-mobile-menu"
                    className={
                        isMenuOpen
                            ? "public-header__mobile-panel public-header__mobile-panel--open"
                            : "public-header__mobile-panel"
                    }
                    aria-hidden={!isMenuOpen}
                    hidden={!isMenuOpen}
                >
                    <nav
                        className="public-header__mobile-nav"
                        aria-label="Navegación pública móvil"
                    >
                        {mobileNavItems.map((item) => (
                            <NavLink
                                key={item.to}
                                to={item.to}
                                className={({ isActive }) =>
                                    isActive
                                        ? "public-header__mobile-link public-header__mobile-link--active"
                                        : "public-header__mobile-link"
                                }
                                onClick={closeMobileMenu}
                            >
                                {item.label}
                            </NavLink>
                        ))}
                    </nav>
                </div>
            </div>
        </header>
    );
}
