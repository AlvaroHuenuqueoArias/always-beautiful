import { NavLink } from "react-router-dom";
import { CONTACT_CONTENT } from "../../data/storefront/contact";

export default function PublicFooter() {
    const instagramSocial = CONTACT_CONTENT.socials.find(
        (social) => social.id === "instagram"
    );

    return (
        <footer className="public-footer">
            <div className="public-footer__container">
                <div className="public-footer__column">
                    <h4 className="public-footer__column-title">Empresa</h4>
                    <div className="public-footer__links">
                        <NavLink to="/">Sobre nosotros</NavLink>
                    </div>
                    <div className="public-footer__meta">
                        <p>Experiencia pública institucional en fase storefront.</p>
                    </div>
                </div>

                <div className="public-footer__column">
                    <h4 className="public-footer__column-title">Navegación</h4>
                    <div className="public-footer__links">
                        <NavLink to="/services">Servicios</NavLink>
                        <NavLink to="/products">Productos</NavLink>
                        <NavLink to="/booking">Reservar</NavLink>
                    </div>
                </div>

                <div className="public-footer__column">
                    <h4 className="public-footer__column-title">Legal</h4>
                    <div className="public-footer__links">
                        <span
                            className="public-footer__placeholder-link"
                            aria-disabled="true"
                        >
                            Política de privacidad
                        </span>
                        <span
                            className="public-footer__placeholder-link"
                            aria-disabled="true"
                        >
                            Términos y condiciones
                        </span>
                    </div>
                    <p className="public-footer__legal-note">
                        Placeholder formal pendiente de redacción legal definitiva.
                    </p>
                </div>

                <div className="public-footer__column">
                    <h4 className="public-footer__column-title">Contacto</h4>

                    <div className="public-footer__meta">
                        <p>{CONTACT_CONTENT.locationLabel}</p>
                        {CONTACT_CONTENT.hours.map((hour, index) => (
                            <p key={index}>{hour}</p>
                        ))}
                    </div>

                    <a
                        href={`mailto:${CONTACT_CONTENT.email}`}
                        className="public-footer__link-inline"
                    >
                        Contacto
                    </a>

                    <a
                        href={`mailto:${CONTACT_CONTENT.email}`}
                        className="public-footer__link-inline public-footer__link-inline--muted"
                    >
                        {CONTACT_CONTENT.email}
                    </a>

                    <div className="public-footer__social-row">
                        <a
                            href={instagramSocial?.href ?? "https://www.instagram.com/"}
                            target="_blank"
                            rel="noreferrer"
                            className="public-footer__social-link"
                            aria-label="Instagram de Always Beautiful"
                            title="Instagram de Always Beautiful"
                        >
                            <svg
                                className="public-footer__social-icon"
                                viewBox="0 0 24 24"
                                xmlns="http://www.w3.org/2000/svg"
                                focusable="false"
                                aria-hidden="true"
                            >
                                <path
                                    fill="currentColor"
                                    d="M7.75 2h8.5A5.75 5.75 0 0 1 22 7.75v8.5A5.75 5.75 0 0 1 16.25 22h-8.5A5.75 5.75 0 0 1 2 16.25v-8.5A5.75 5.75 0 0 1 7.75 2Zm0 1.5A4.25 4.25 0 0 0 3.5 7.75v8.5A4.25 4.25 0 0 0 7.75 20.5h8.5A4.25 4.25 0 0 0 20.5 16.25v-8.5A4.25 4.25 0 0 0 16.25 3.5h-8.5Zm8.75 2a1.25 1.25 0 1 1 0 2.5 1.25 1.25 0 0 1 0-2.5ZM12 7a5 5 0 1 1 0 10 5 5 0 0 1 0-10Zm0 1.5A3.5 3.5 0 1 0 12 15.5 3.5 3.5 0 0 0 12 8.5Z"
                                />
                            </svg>
                        </a>
                    </div>
                </div>
            </div>
        </footer>
    );
}
