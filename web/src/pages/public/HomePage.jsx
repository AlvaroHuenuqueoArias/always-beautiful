import HeroSection from "../../components/storefront/HeroSection";
import TeamSection from "../../components/storefront/TeamSection";

export default function HomePage() {
    return (
        <>
            <section className="page-shell">
                <HeroSection />
            </section>

            <div
                id="home-followup-viewport"
                className="public-page-frame public-page-frame--editorial public-page-frame--home-followup"
            >
                <section className="page-shell">
                    <div className="page-shell__editorial-inner page-shell__editorial-inner--home-followup">
                        <div
                            id="home-team-section"
                            className="home-followup__team-anchor"
                        >
                            <TeamSection />
                        </div>

                        <div
                            className="home-followup__reserved-space"
                            aria-hidden="true"
                        />
                    </div>
                </section>
            </div>
        </>
    );
}
