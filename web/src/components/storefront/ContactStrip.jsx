import { CONTACT_CONTENT } from "../../data/storefront/contact";

export default function ContactStrip() {
    const instagramSocial = CONTACT_CONTENT.socials.find(
        (social) => social.id === "instagram"
    );

    return (
        <section className="contact-strip">
            <div className="contact-strip__item">
                <span className="contact-strip__label">Horario</span>
                <p className="contact-strip__value">{CONTACT_CONTENT.hours[0]}</p>
            </div>

            <div className="contact-strip__item">
                <span className="contact-strip__label">Ubicación</span>
                <p className="contact-strip__value">
                    {CONTACT_CONTENT.locationLabel}
                </p>
            </div>

            <div className="contact-strip__item">
                <span className="contact-strip__label">Email</span>
                <a
                    href={`mailto:${CONTACT_CONTENT.email}`}
                    className="contact-strip__value contact-strip__email-link"
                >
                    {CONTACT_CONTENT.email}
                </a>
            </div>

            <div className="contact-strip__item contact-strip__item--social">
                <span className="contact-strip__label">Instagram</span>

                <a
                    href={instagramSocial?.href ?? "https://www.instagram.com/"}
                    target="_blank"
                    rel="noreferrer"
                    className="contact-strip__social-link"
                    aria-label="Instagram de Always Beautiful"
                    title="Instagram de Always Beautiful"
                >
                    <svg
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
        </section>
    );
}