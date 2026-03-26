const COPY = {
    en: {
        kicker: "Stylist production",
        note: "Monthly view · Weeks 1–4 · Business calendar Tuesday to Saturday",
        empty: "No trend data available.",
        noTrends: "No stylist trends available."
    },
    es: {
        kicker: "Producción por estilista",
        note: "Vista mensual · Semanas 1–4 · Calendario laboral de martes a sábado",
        empty: "No hay datos de tendencia disponibles.",
        noTrends: "No hay tendencias de estilistas disponibles."
    }
};

function buildBars(points = []) {
    if (!points.length) return [];

    const values = points.map((point) => point.value);
    const max = Math.max(...values) || 1;

    return points.map((point) => ({
        ...point,
        heightPercent: Math.max(28, Math.round((point.value / max) * 100))
    }));
}

function TrendBars({ points = [], direction = "stable", language = "en" }) {
    const t = COPY[language];
    const normalizedBars = buildBars(points);

    if (!normalizedBars.length) {
        return <div className="empty-state-box">{t.empty}</div>;
    }

    return (
        <div className="trend-bars-wrapper">
            <div className="trend-bars-chart">
                {normalizedBars.map((point) => (
                    <div key={point.label} className="trend-bar-column">
                        <div className="trend-bar-area">
                            <div
                                className={`trend-bar-visual trend-${direction}`}
                                style={{ height: `${point.heightPercent}%` }}
                            />
                        </div>
                        <span className="trend-bar-label">{point.label}</span>
                    </div>
                ))}
            </div>

            <div className="trend-chart-note">{t.note}</div>
        </div>
    );
}

function TrendCard({ trend, language = "en" }) {
    const t = COPY[language];
    const directionClass = trend?.direction || "stable";
    const summary =
        language === "es"
            ? trend?.summary_es ?? trend?.summary
            : trend?.summary_en ?? trend?.summary;

    return (
        <article className="trend-card">
            <div className="trend-card-header">
                <div>
                    <p className="panel-kicker">{t.kicker}</p>
                    <h4>{trend?.professionalName}</h4>
                </div>
                <span className={`trend-pill trend-${directionClass}`}>
                    {trend?.variationLabel}
                </span>
            </div>

            <TrendBars
                points={trend?.points ?? []}
                direction={directionClass}
                language={language}
            />

            <p className="trend-summary">{summary}</p>
        </article>
    );
}

export default function TrendSnapshot({
    stylistTrends = [],
    language = "en"
}) {
    const t = COPY[language];

    return (
        <section className="trend-grid">
            {stylistTrends.length > 0 ? (
                stylistTrends.map((trend) => (
                    <TrendCard
                        key={trend.professionalId}
                        trend={trend}
                        language={language}
                    />
                ))
            ) : (
                <article className="panel-card">
                    <div className="empty-state-box">{t.noTrends}</div>
                </article>
            )}
        </section>
    );
}