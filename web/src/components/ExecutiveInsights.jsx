const ALERT_COPY = {
    en: {
        kicker: "AI signals",
        title: "Business notes",
        items: "items",
        empty: "No business notes available."
    },
    es: {
        kicker: "Señales IA",
        title: "Notas del negocio",
        items: "items",
        empty: "No hay notas del negocio disponibles."
    }
};

function getAlertField(alert, language, field) {
    if (language === "es") {
        return alert[`${field}_es`] ?? alert[field];
    }
    return alert[`${field}_en`] ?? alert[field];
}

function AlertItem({ alert, compact = false, language = "en" }) {
    const title = getAlertField(alert, language, "title");
    const message = getAlertField(alert, language, "message");
    const tag = getAlertField(alert, language, "tag");

    return (
        <div className={`alert-item severity-${alert.kind} ${compact ? "compact-alert-item" : ""}`}>
            <div className="alert-item-header">
                <strong>{title}</strong>
                <span className={`alert-tag kind-${alert.kind}`}>{tag}</span>
            </div>
            <p>{message}</p>
        </div>
    );
}

export default function ExecutiveInsights({
    alerts = [],
    compact = false,
    language = "en"
}) {
    const t = ALERT_COPY[language];

    if (compact) {
        return (
            <article className="system-box executive-side-box">
                <div className="executive-side-header">
                    <div>
                        <p className="brand-kicker">{t.kicker}</p>
                        <h2>{t.title}</h2>
                    </div>
                    <span className="small-indicator">{alerts.length} {t.items}</span>
                </div>

                <div className="executive-side-list">
                    {alerts.length > 0 ? (
                        alerts.map((alert) => (
                            <AlertItem
                                key={alert.id}
                                alert={alert}
                                compact
                                language={language}
                            />
                        ))
                    ) : (
                        <div className="empty-state-box">{t.empty}</div>
                    )}
                </div>
            </article>
        );
    }

    return (
        <section className="executive-insights-grid">
            <article className="panel-card">
                <div className="panel-card-header">
                    <div>
                        <p className="panel-kicker">{t.kicker}</p>
                        <h3>{t.title}</h3>
                    </div>
                    <span className="small-indicator">{alerts.length} {t.items}</span>
                </div>

                <div className="alerts-list">
                    {alerts.length > 0 ? (
                        alerts.map((alert) => (
                            <AlertItem
                                key={alert.id}
                                alert={alert}
                                language={language}
                            />
                        ))
                    ) : (
                        <div className="empty-state-box">{t.empty}</div>
                    )}
                </div>
            </article>
        </section>
    );
}