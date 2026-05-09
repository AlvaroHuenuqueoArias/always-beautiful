import { BOOKING_CTA_CONTENT } from "../../data/storefront/brand";
import StorefrontButton from "../shared/StorefrontButton";

export default function BookingCTASection() {
    return (
        <section className="booking-cta">
            <div className="booking-cta__content">
                <p className="booking-cta__eyebrow">{BOOKING_CTA_CONTENT.eyebrow}</p>
                <h2 className="booking-cta__title">{BOOKING_CTA_CONTENT.title}</h2>
                <p className="booking-cta__description">
                    {BOOKING_CTA_CONTENT.description}
                </p>
            </div>

            <div className="booking-cta__action">
                <StorefrontButton
                    to={BOOKING_CTA_CONTENT.buttonTo}
                    variant="primary"
                >
                    {BOOKING_CTA_CONTENT.buttonLabel}
                </StorefrontButton>
            </div>
        </section>
    );
}