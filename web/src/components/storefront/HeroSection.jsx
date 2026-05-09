import { useEffect, useState } from "react";
import { BRAND_CONTENT } from "../../data/storefront/brand";
import StorefrontButton from "../shared/StorefrontButton";

/*
 * LÓGICA EDITORIAL ESCALABLE:
 * - hero-primary.png
 * - hero-primary2.png
 * - hero-primary3.png
 * ...
 * - hero-primary10.png
 *
 * El componente detecta automáticamente cuáles existen realmente
 * en /public/images/storefront/home/ y solo recorre esas.
 */
const HERO_IMAGE_CANDIDATES = Array.from({ length: 10 }, (_, index) =>
    index === 0
        ? "/images/storefront/home/hero-primary.png"
        : `/images/storefront/home/hero-primary${index + 1}.png`
);

export default function HeroSection() {
    const [availableImages, setAvailableImages] = useState([
        HERO_IMAGE_CANDIDATES[0]
    ]);
    const [currentIndex, setCurrentIndex] = useState(0);

    useEffect(() => {
        let isMounted = true;

        async function resolveAvailableImages() {
            const checks = await Promise.all(
                HERO_IMAGE_CANDIDATES.map(
                    (src) =>
                        new Promise((resolve) => {
                            const image = new Image();

                            image.onload = () => resolve(src);
                            image.onerror = () => resolve(null);
                            image.src = src;
                        })
                )
            );

            const validImages = checks.filter(Boolean);

            if (!isMounted) return;

            setAvailableImages(
                validImages.length > 0
                    ? validImages
                    : [HERO_IMAGE_CANDIDATES[0]]
            );
        }

        resolveAvailableImages();

        return () => {
            isMounted = false;
        };
    }, []);

    useEffect(() => {
        if (currentIndex >= availableImages.length) {
            setCurrentIndex(0);
        }
    }, [availableImages, currentIndex]);

    const activeImage = availableImages[currentIndex] ?? HERO_IMAGE_CANDIDATES[0];

    /*
     * AJUSTE EDITORIAL:
     * La disolvencia ahora se aplica SOLO a hero-primary.png.
     * Las demás imágenes mantienen el mismo marco visual,
     * pero sin la máscara difusa inferior.
     */
    const hasPrimaryFade = activeImage === HERO_IMAGE_CANDIDATES[0];

    function handleNextEditorialImage() {
        setCurrentIndex((previousIndex) => {
            if (availableImages.length <= 1) return previousIndex;

            return (previousIndex + 1) % availableImages.length;
        });
    }

    function handleScrollToTeamSection() {
        const isCompactViewport = window.matchMedia(
            "(max-width: 1024px)"
        ).matches;
        const targetId = isCompactViewport
            ? "home-followup-viewport"
            : "home-team-section";
        const targetSection = document.getElementById(targetId);

        if (!targetSection) return;

        targetSection.scrollIntoView({
            behavior: "smooth",
            block: "start"
        });
    }

    return (
        <section className="home-hero">
            <div className="home-hero__background" aria-hidden="true">
                <div className="home-hero__color-field" />
            </div>

            <div className="home-hero__inner">
                <div className="home-hero__grid">
                    <div className="home-hero__content">
                        <p className="home-hero__eyebrow">
                            {BRAND_CONTENT.categoryLabel ?? "Salón de Belleza"}
                        </p>

                        <div className="home-hero__title-wrap">
                            <h1 className="home-hero__title">
                                <span className="home-hero__title-primary">
                                    {BRAND_CONTENT.namePrimary}
                                </span>
                                <span className="home-hero__title-secondary">
                                    {BRAND_CONTENT.nameSecondary}
                                </span>
                            </h1>
                        </div>

                        <div className="home-hero__info-panel">
                            <p className="home-hero__subtitle">
                                {BRAND_CONTENT.subtitle}
                            </p>

                            <p className="home-hero__description">
                                {BRAND_CONTENT.description}
                            </p>
                        </div>

                        <div className="home-hero__actions">
                            <div className="home-hero__cta-cluster">
                                <StorefrontButton
                                    to={BRAND_CONTENT.primaryCta.to}
                                    variant="primary"
                                >
                                    {BRAND_CONTENT.primaryCta.label}
                                </StorefrontButton>

                                <img
                                    src="/images/storefront/home/hero-booking.png"
                                    alt=""
                                    aria-hidden="true"
                                    className="home-hero__booking-badge"
                                    loading="eager"
                                    decoding="async"
                                />
                            </div>
                        </div>

                        <div className="home-hero__scroll-cue">
                            <button
                                type="button"
                                className="home-hero__scroll-trigger"
                                onClick={handleScrollToTeamSection}
                                aria-label="Desplazar hacia la sección de equipo"
                                title="Ver equipo"
                            >
                                <span
                                    className="home-hero__scroll-trigger-icon"
                                    aria-hidden="true"
                                />
                            </button>
                        </div>
                    </div>

                    <div
                        className="home-hero__visual"
                        aria-label="Galería editorial del Home"
                    >
                        <div className="home-hero__editorial-stage">
                            <figure
                                className={[
                                    "home-hero__image-card",
                                    "home-hero__image-card--primary",
                                    hasPrimaryFade
                                        ? "home-hero__image-card--with-fade"
                                        : ""
                                ]
                                    .filter(Boolean)
                                    .join(" ")}
                            >
                                <img
                                    key={activeImage}
                                    src={activeImage}
                                    alt={`Editorial principal del salón Always beautiful ${currentIndex + 1}`}
                                    className="home-hero__image"
                                />
                            </figure>

                            <button
                                type="button"
                                className="home-hero__editorial-arrow"
                                onClick={handleNextEditorialImage}
                                aria-label="Ver siguiente imagen editorial"
                            >
                                <span className="home-hero__editorial-arrow-head" />
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </section>
    );
}
