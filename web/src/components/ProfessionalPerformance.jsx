const COPY = {
    en: {
        kicker: "Performance",
        title: "Production by professional",
        profiles: "profiles",
        bookings: "bookings",
        revenue: "Revenue",
        avgTicket: "Avg. ticket",
        occupancy: "Occupancy",
        cancellation: "Cancellation",
        empty: "No professional performance data available."
    },
    es: {
        kicker: "Rendimiento",
        title: "Producción por profesional",
        profiles: "perfiles",
        bookings: "reservas",
        revenue: "Ingresos",
        avgTicket: "Ticket prom.",
        occupancy: "Ocupación",
        cancellation: "Cancelación",
        empty: "No hay datos de rendimiento profesional disponibles."
    }
};

function formatCurrency(value) {
    return new Intl.NumberFormat("es-CL", {
        style: "currency",
        currency: "CLP",
        maximumFractionDigits: 0
    }).format(value ?? 0);
}

function formatPercent(value) {
    return `${value ?? 0}%`;
}

export default function ProfessionalPerformance({
    professionals = [],
    language = "en"
}) {
    const t = COPY[language];

    return (
        <article className="panel-card">
            <div className="panel-card-header">
                <div>
                    <p className="panel-kicker">{t.kicker}</p>
                    <h3>{t.title}</h3>
                </div>
                <span className="small-indicator">
                    {professionals.length} {t.profiles}
                </span>
            </div>

            <div className="performance-grid">
                {professionals.length > 0 ? (
                    professionals.map((professional) => (
                        <article key={professional.id} className="performance-card">
                            <div className="performance-card-top">
                                <div>
                                    <h4>{professional.name}</h4>
                                    <p>{professional.topService}</p>
                                </div>
                                <span className="performance-pill">
                                    {professional.appointments} {t.bookings}
                                </span>
                            </div>

                            <div className="performance-metrics">
                                <div>
                                    <span>{t.revenue}</span>
                                    <strong>{formatCurrency(professional.revenue)}</strong>
                                </div>
                                <div>
                                    <span>{t.avgTicket}</span>
                                    <strong>{formatCurrency(professional.averageTicket)}</strong>
                                </div>
                                <div>
                                    <span>{t.occupancy}</span>
                                    <strong>{formatPercent(professional.occupancyRate)}</strong>
                                </div>
                                <div>
                                    <span>{t.cancellation}</span>
                                    <strong>{formatPercent(professional.cancellationRate)}</strong>
                                </div>
                            </div>
                        </article>
                    ))
                ) : (
                    <div className="empty-state-box">{t.empty}</div>
                )}
            </div>
        </article>
    );
}