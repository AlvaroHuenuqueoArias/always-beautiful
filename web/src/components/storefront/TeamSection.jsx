import { useState } from "react";
import SectionHeading from "../shared/SectionHeading";
import { PROFESSIONALS_CONTENT } from "../../data/storefront/professionals";

export default function TeamSection() {
    const [activeProfileId, setActiveProfileId] = useState(null);

    function handleOpenProfile(profileId) {
        setActiveProfileId(profileId);
    }

    function handleCloseProfile() {
        setActiveProfileId(null);
    }

    return (
        <section className="page-shell__section team-section">
            <SectionHeading
                eyebrow="Equipo"
                title="Profesionales que sostienen la experiencia del salón"
                description="Ambas profesionales cumplen un rol clave en la experiencia Always Beautiful y aportan especialización, detalle y atención personalizada."
            />

            <div className="team-grid">
                {PROFESSIONALS_CONTENT.map((person) => {
                    const isActive = activeProfileId === person.id;
                    const profilePanelId = `professional-profile-${person.id
                        .toLowerCase()
                        .replace(/\s+/g, "-")}`;
                    const frontTitleId = `professional-title-${person.id
                        .toLowerCase()
                        .replace(/\s+/g, "-")}`;

                    return (
                        <article
                            key={person.id}
                            className={[
                                "team-card",
                                person.id === "Nadia"
                                    ? "team-card--nadia"
                                    : "team-card--maria",
                                isActive ? "team-card--detail-mode" : ""
                            ]
                                .filter(Boolean)
                                .join(" ")}
                        >
                            <div
                                className="team-card__view team-card__view--front"
                                aria-hidden={isActive}
                            >
                                <div className="team-card__compact-row">
                                    <p className="team-card__compact-kicker">
                                        Always Beautiful
                                    </p>

                                    <div className="team-card__compact-main">
                                        <div className="team-card__compact-identity">
                                            <h3
                                                className="team-card__name"
                                                id={frontTitleId}
                                            >
                                                {person.name}
                                            </h3>

                                            <p className="team-card__role">
                                                {person.role}
                                            </p>
                                        </div>

                                        <div className="team-card__skills-block">
                                            <p className="team-card__skills-title">
                                                Áreas principales
                                            </p>

                                            <ul className="team-card__skills-list">
                                                {person.profileSkills.map(
                                                    (skill) => (
                                                        <li
                                                            key={`${person.id}-${skill}`}
                                                            className="team-card__skills-item"
                                                        >
                                                            <span
                                                                className="team-card__skills-bullet"
                                                                aria-hidden="true"
                                                            />
                                                            <span>{skill}</span>
                                                        </li>
                                                    )
                                                )}
                                            </ul>
                                        </div>
                                    </div>

                                    <div className="team-card__compact-actions">
                                        <button
                                            type="button"
                                            className="storefront-button storefront-button--profile storefront-button--sm"
                                            onClick={() =>
                                                handleOpenProfile(person.id)
                                            }
                                            aria-expanded={isActive}
                                            aria-controls={profilePanelId}
                                            tabIndex={isActive ? -1 : 0}
                                        >
                                            Ver perfil del profesional
                                        </button>
                                    </div>
                                </div>
                            </div>

                            <div
                                id={profilePanelId}
                                className="team-card__view team-card__view--detail"
                                role="region"
                                aria-label={`Perfil profesional de ${person.name} pendiente de contenido editorial`}
                                aria-hidden={!isActive}
                            >
                                <div className="team-card__detail-topbar">
                                    <button
                                        type="button"
                                        className="team-card__detail-back"
                                        onClick={handleCloseProfile}
                                        aria-label={`Volver a la vista principal de ${person.name}`}
                                        tabIndex={isActive ? 0 : -1}
                                    >
                                        <span
                                            className="team-card__detail-back-icon"
                                            aria-hidden="true"
                                        />
                                    </button>
                                </div>

                                <div
                                    className="team-card__detail-placeholder"
                                    aria-hidden="true"
                                />
                            </div>
                        </article>
                    );
                })}
            </div>
        </section>
    );
}