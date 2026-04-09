import { useEffect, useMemo, useState } from "react";
import EcommercePerformance from "../../components/EcommercePerformance";
import ExecutiveInsights from "../../components/ExecutiveInsights";
import ProfessionalPerformance from "../../components/ProfessionalPerformance";
import TrendSnapshot from "../../components/TrendSnapshot";
import { mockDashboard } from "../../mockAdminData";

const API_BASE_URL = "http://127.0.0.1:8000";

const UI_COPY = {
    en: {
        dashboardTitle: "Administrative Dashboard",
        dashboardSubtitle: "Operational and analytics overview",
        date: "Date",
        professional: "Professional",
        amountsVisible: "Amounts visible",
        amountsHidden: "Amounts hidden",
        systemStatus: "System status",
        dataSource: "Data source",
        interfaceMode: "Interface mode",
        visualProfile: "Visual profile",
        premiumSimple: "Premium Simple",
        organizedAdmin: "Organized Admin",
        dailyActivity: "Daily activity",
        operationalControl: "Operational control",
        todayBookings: "Today bookings",
        confirmed: "Confirmed",
        pending: "Pending",
        cancelled: "Cancelled",
        businessRevenue: "Business revenue",
        financialSummary: "Financial summary",
        todayServiceRevenue: "Today service revenue",
        weeklySalonRevenue: "Weekly salon revenue",
        monthServiceRevenue: "Month service revenue",
        ownerShareMonth: "Owner share month",
        supportIndicators: "Support indicators",
        referenceMetrics: "Reference metrics",
        averageTicket: "Average ticket",
        occupancy: "Occupancy",
        cancellationRate: "Cancellation rate",
        ecommerceToday: "E-commerce today",
        ecommerceWeek: "E-commerce week",
        ecommerceMonth: "E-commerce month",
        monthProgress: "Month progress",
        ownerToday: "Owner share today",
        ownerWeek: "Owner share week"
    },
    es: {
        dashboardTitle: "Panel administrativo",
        dashboardSubtitle: "Resumen operativo y analítico",
        date: "Fecha",
        professional: "Profesional",
        amountsVisible: "Montos visibles",
        amountsHidden: "Montos ocultos",
        systemStatus: "Estado del sistema",
        dataSource: "Fuente de datos",
        interfaceMode: "Modo de interfaz",
        visualProfile: "Perfil visual",
        premiumSimple: "Premium Simple",
        organizedAdmin: "Admin Organizado",
        dailyActivity: "Actividad diaria",
        operationalControl: "Control operativo",
        todayBookings: "Reservas del día",
        confirmed: "Confirmadas",
        pending: "Pendientes",
        cancelled: "Canceladas",
        businessRevenue: "Ingresos del negocio",
        financialSummary: "Resumen financiero",
        todayServiceRevenue: "Ingresos de servicios del día",
        weeklySalonRevenue: "Ingresos semanales del salón",
        monthServiceRevenue: "Ingresos mensuales de servicios",
        ownerShareMonth: "Participación mensual de la dueña",
        supportIndicators: "Indicadores de apoyo",
        referenceMetrics: "Métricas de referencia",
        averageTicket: "Ticket promedio",
        occupancy: "Ocupación",
        cancellationRate: "Tasa de cancelación",
        ecommerceToday: "E-commerce hoy",
        ecommerceWeek: "E-commerce semana",
        ecommerceMonth: "E-commerce mes",
        monthProgress: "Avance mes",
        ownerToday: "Dueña hoy",
        ownerWeek: "Dueña semana"
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

function todayAsInputValue() {
    const now = new Date();
    const year = now.getFullYear();
    const month = `${now.getMonth() + 1}`.padStart(2, "0");
    const day = `${now.getDate()}`.padStart(2, "0");
    return `${year}-${month}-${day}`;
}

function StatusBadge({ status }) {
    const normalized = status?.toLowerCase?.() || "unknown";

    return (
        <span className={`status-badge status-${normalized}`}>
            {normalized}
        </span>
    );
}

function EyeIcon({ closed = false }) {
    if (closed) {
        return (
            <svg viewBox="0 0 24 24" aria-hidden="true" className="visibility-icon">
                <path
                    d="M3 4.5 20 21"
                    fill="none"
                    stroke="currentColor"
                    strokeWidth="1.8"
                    strokeLinecap="round"
                />
                <path
                    d="M10.6 6.3A10.7 10.7 0 0 1 12 6.2c5.4 0 9.2 5.8 9.2 5.8a16.2 16.2 0 0 1-3.5 3.9M6.7 9A15.4 15.4 0 0 0 2.8 12s3.8 5.8 9.2 5.8a9.8 9.8 0 0 0 3-.5"
                    fill="none"
                    stroke="currentColor"
                    strokeWidth="1.8"
                    strokeLinecap="round"
                    strokeLinejoin="round"
                />
                <path
                    d="M9.9 9.9A3 3 0 0 0 9 12a3 3 0 0 0 5.1 2.1"
                    fill="none"
                    stroke="currentColor"
                    strokeWidth="1.8"
                    strokeLinecap="round"
                    strokeLinejoin="round"
                />
            </svg>
        );
    }

    return (
        <svg viewBox="0 0 24 24" aria-hidden="true" className="visibility-icon">
            <path
                d="M2.8 12S6.6 6.2 12 6.2 21.2 12 21.2 12 17.4 17.8 12 17.8 2.8 12 2.8 12Z"
                fill="none"
                stroke="currentColor"
                strokeWidth="1.8"
                strokeLinecap="round"
                strokeLinejoin="round"
            />
            <circle
                cx="12"
                cy="12"
                r="3"
                fill="none"
                stroke="currentColor"
                strokeWidth="1.8"
            />
        </svg>
    );
}

function MetricCard({ label, value, accent, hidden = false }) {
    return (
        <article className={`metric-card accent-${accent}`}>
            <p className="metric-label">{label}</p>
            <h3 className={`metric-value ${hidden ? "value-hidden" : ""}`}>
                {value}
            </h3>
        </article>
    );
}

export default function DashboardPage() {
    const [selectedDate, setSelectedDate] = useState(todayAsInputValue());
    const [selectedProfessional, setSelectedProfessional] = useState("all");
    const [dashboardData, setDashboardData] = useState(mockDashboard);
    const [loading, setLoading] = useState(false);
    const [source, setSource] = useState("mock");
    const [error, setError] = useState("");
    const [hideAmounts, setHideAmounts] = useState(false);
    const [language, setLanguage] = useState("en");

    const t = UI_COPY[language];

    useEffect(() => {
        const controller = new AbortController();

        async function fetchDashboard() {
            setLoading(true);
            setError("");

            try {
                const params = new URLSearchParams();
                params.set("date", selectedDate);

                if (selectedProfessional && selectedProfessional !== "all") {
                    params.set("professional_id", selectedProfessional);
                }

                const response = await fetch(
                    `${API_BASE_URL}/admin/dashboard?${params.toString()}`,
                    {
                        signal: controller.signal
                    }
                );

                if (!response.ok) {
                    throw new Error(
                        `Dashboard request failed with status ${response.status}`
                    );
                }

                const data = await response.json();

                setDashboardData({
                    ...mockDashboard,
                    ...data,
                    professionals: data.professionals ?? mockDashboard.professionals,
                    bookings: data.bookings ?? mockDashboard.bookings,
                    orders: data.orders ?? mockDashboard.orders,
                    summary: {
                        ...mockDashboard.summary,
                        ...(data.summary ?? {})
                    },
                    executiveKpis: {
                        ...mockDashboard.executiveKpis,
                        ...(data.executiveKpis ?? {})
                    },
                    alerts: data.alerts ?? mockDashboard.alerts,
                    professionalStats:
                        data.professionalStats ?? mockDashboard.professionalStats,
                    stylistTrends:
                        data.stylistTrends ?? mockDashboard.stylistTrends,
                    ecommerceSummary:
                        data.ecommerceSummary ?? mockDashboard.ecommerceSummary,
                    ecommerceSales:
                        data.ecommerceSales ?? mockDashboard.ecommerceSales,
                    ownerBreakdown:
                        data.ownerBreakdown ?? mockDashboard.ownerBreakdown
                });

                setSource("api");
            } catch (err) {
                if (err.name !== "AbortError") {
                    setDashboardData(mockDashboard);
                    setSource("mock");
                    setError(
                        "Backend unavailable. Mock data loaded for UI continuity."
                    );
                }
            } finally {
                setLoading(false);
            }
        }

        fetchDashboard();

        return () => controller.abort();
    }, [selectedDate, selectedProfessional]);

    const summary = dashboardData.summary ?? {};
    const executiveKpis = dashboardData.executiveKpis ?? {};
    const orders = dashboardData.orders ?? [];
    const professionals = dashboardData.professionals ?? mockDashboard.professionals;
    const alerts = dashboardData.alerts ?? [];
    const professionalStats =
        dashboardData.professionalStats ?? mockDashboard.professionalStats;
    const stylistTrends = dashboardData.stylistTrends ?? mockDashboard.stylistTrends;
    const ecommerceSummary =
        dashboardData.ecommerceSummary ?? mockDashboard.ecommerceSummary;
    const ecommerceSales =
        dashboardData.ecommerceSales ?? mockDashboard.ecommerceSales;
    const ownerBreakdown =
        dashboardData.ownerBreakdown ?? mockDashboard.ownerBreakdown;

    const filteredBookings = useMemo(() => {
        const list = dashboardData.bookings ?? [];

        if (selectedProfessional === "all") return list;

        return list.filter(
            (booking) =>
                booking.professional_id === selectedProfessional ||
                booking.professional_name ===
                    dashboardData.professionals?.find(
                        (p) => p.id === selectedProfessional
                    )?.name
        );
    }, [dashboardData, selectedProfessional]);

    const filteredProfessionalStats = useMemo(() => {
        if (selectedProfessional === "all") return professionalStats;

        return professionalStats.filter(
            (professional) => professional.id === selectedProfessional
        );
    }, [professionalStats, selectedProfessional]);

    const visibleStylistTrends = useMemo(() => {
        if (selectedProfessional === "all") {
            return stylistTrends;
        }

        return stylistTrends.filter(
            (trend) => trend.professionalId === selectedProfessional
        );
    }, [stylistTrends, selectedProfessional]);

    return (
        <div className="dashboard-shell">
            <aside className="sidebar-panel">
                <div className="brand-box">
                    <span className="brand-kicker">Always Beautiful</span>
                    <h1>Admin Console</h1>
                    <p>
                        Advanced operational visibility for agenda, bookings,
                        orders and daily salon metrics.
                    </p>
                </div>

                <div className="system-box">
                    <h2>{t.systemStatus}</h2>
                    <div className="system-row">
                        <span>{t.dataSource}</span>
                        <strong className={`pill pill-${source}`}>
                            {source.toUpperCase()}
                        </strong>
                    </div>
                    <div className="system-row">
                        <span>{t.interfaceMode}</span>
                        <strong>{t.premiumSimple}</strong>
                    </div>
                    <div className="system-row">
                        <span>{t.visualProfile}</span>
                        <strong>{t.organizedAdmin}</strong>
                    </div>
                </div>

                <ExecutiveInsights alerts={alerts} compact language={language} />
            </aside>

            <main className="main-panel">
                <header className="topbar">
                    <div>
                        <p className="eyebrow">{t.dashboardTitle}</p>
                        <h2>{t.dashboardSubtitle}</h2>
                    </div>

                    <div className="topbar-right">
                        <button
                            type="button"
                            className="language-toggle-btn"
                            onClick={() =>
                                setLanguage((current) =>
                                    current === "en" ? "es" : "en"
                                )
                            }
                            aria-label="Toggle language"
                            title="Toggle language"
                        >
                            <span className={language === "en" ? "active-lang" : ""}>
                                English
                            </span>
                            <span className="lang-divider">/</span>
                            <span className={language === "es" ? "active-lang" : ""}>
                                Español
                            </span>
                        </button>

                        <button
                            type="button"
                            className="visibility-toggle-btn"
                            onClick={() => setHideAmounts((current) => !current)}
                            aria-label={
                                hideAmounts ? t.amountsVisible : t.amountsHidden
                            }
                            title={hideAmounts ? t.amountsVisible : t.amountsHidden}
                        >
                            <span className="visibility-icon-wrap">
                                <EyeIcon closed={hideAmounts} />
                            </span>
                            <span>
                                {hideAmounts ? t.amountsHidden : t.amountsVisible}
                            </span>
                        </button>

                        <div className="filters-panel">
                            <label className="field-group">
                                <span>{t.date}</span>
                                <input
                                    type="date"
                                    value={selectedDate}
                                    onChange={(event) =>
                                        setSelectedDate(event.target.value)
                                    }
                                />
                            </label>

                            <label className="field-group">
                                <span>{t.professional}</span>
                                <select
                                    value={selectedProfessional}
                                    onChange={(event) =>
                                        setSelectedProfessional(event.target.value)
                                    }
                                >
                                    {professionals.map((professional) => (
                                        <option
                                            key={professional.id}
                                            value={professional.id}
                                        >
                                            {professional.name}
                                        </option>
                                    ))}
                                </select>
                            </label>
                        </div>
                    </div>
                </header>

                {error && <div className="alert-banner">{error}</div>}

                <section className="metric-block">
                    <div className="metric-block-header">
                        <p className="panel-kicker">{t.dailyActivity}</p>
                        <h3>{t.operationalControl}</h3>
                    </div>

                    <div className="metrics-grid operations-grid">
                        <MetricCard
                            label={t.todayBookings}
                            value={summary.totalBookings ?? 0}
                            accent="pink"
                        />
                        <MetricCard
                            label={t.confirmed}
                            value={summary.confirmedBookings ?? 0}
                            accent="cream"
                        />
                        <MetricCard
                            label={t.pending}
                            value={summary.pendingBookings ?? 0}
                            accent="camel"
                        />
                        <MetricCard
                            label={t.cancelled}
                            value={summary.cancelledBookings ?? 0}
                            accent="graphite"
                        />
                    </div>
                </section>

                <section className="metric-block">
                    <div className="metric-block-header">
                        <p className="panel-kicker">{t.businessRevenue}</p>
                        <h3>{t.financialSummary}</h3>
                    </div>

                    <div className="metrics-grid financial-grid">
                        <MetricCard
                            label={t.todayServiceRevenue}
                            value={formatCurrency(summary.revenueToday ?? 0)}
                            accent="graphite"
                            hidden={hideAmounts}
                        />
                        <MetricCard
                            label={t.weeklySalonRevenue}
                            value={formatCurrency(summary.revenueWeekGlobal ?? 0)}
                            accent="camel"
                            hidden={hideAmounts}
                        />
                        <MetricCard
                            label={t.monthServiceRevenue}
                            value={formatCurrency(executiveKpis.revenueMonth ?? 0)}
                            accent="camel"
                            hidden={hideAmounts}
                        />
                        <MetricCard
                            label={t.ecommerceToday}
                            value={formatCurrency(ecommerceSummary.revenueToday ?? 0)}
                            accent="commerce"
                            hidden={hideAmounts}
                        />
                        <MetricCard
                            label={t.ecommerceWeek}
                            value={formatCurrency(ecommerceSummary.revenueWeek ?? 0)}
                            accent="commerce"
                            hidden={hideAmounts}
                        />
                        <MetricCard
                            label={t.ecommerceMonth}
                            value={formatCurrency(ecommerceSummary.totalRevenue ?? 0)}
                            accent="commerce"
                            hidden={hideAmounts}
                        />
                        <MetricCard
                            label={t.monthProgress}
                            value={`${ecommerceSummary.currentDayOfMonth ?? 0}/${ecommerceSummary.daysInMonth ?? 0}`}
                            accent="cream"
                        />
                        <MetricCard
                            label={t.ownerToday}
                            value={formatCurrency(ownerBreakdown.amountCollectedToday ?? 0)}
                            accent="owner"
                            hidden={hideAmounts}
                        />
                        <MetricCard
                            label={t.ownerWeek}
                            value={formatCurrency(ownerBreakdown.amountCollectedWeek ?? 0)}
                            accent="owner"
                            hidden={hideAmounts}
                        />
                        <MetricCard
                            label={t.ownerShareMonth}
                            value={formatCurrency(executiveKpis.ownerShareMonth ?? 0)}
                            accent="owner"
                            hidden={hideAmounts}
                        />
                    </div>
                </section>

                <section className="metric-block">
                    <div className="metric-block-header">
                        <p className="panel-kicker">{t.supportIndicators}</p>
                        <h3>{t.referenceMetrics}</h3>
                    </div>

                    <div className="metrics-grid support-grid">
                        <MetricCard
                            label={t.averageTicket}
                            value={formatCurrency(executiveKpis.averageTicket ?? 0)}
                            accent="pink"
                            hidden={hideAmounts}
                        />
                        <MetricCard
                            label={t.occupancy}
                            value={formatPercent(executiveKpis.occupancyRate ?? 0)}
                            accent="cream"
                        />
                        <MetricCard
                            label={t.cancellationRate}
                            value={formatPercent(
                                executiveKpis.cancellationRate ?? 0
                            )}
                            accent="graphite"
                        />
                    </div>
                </section>

                <ProfessionalPerformance
                    professionals={filteredProfessionalStats}
                    language={language}
                />

                <TrendSnapshot
                    stylistTrends={visibleStylistTrends}
                    language={language}
                />

                <EcommercePerformance
                    summary={ecommerceSummary}
                    sales={ecommerceSales}
                    ownerBreakdown={ownerBreakdown}
                    hideAmounts={hideAmounts}
                    language={language}
                />

                <section className="content-grid">
                    <article className="panel-card">
                        <div className="panel-card-header">
                            <div>
                                <p className="panel-kicker">
                                    {language === "en" ? "Agenda" : "Agenda"}
                                </p>
                                <h3>
                                    {language === "en"
                                        ? "Bookings of the day"
                                        : "Reservas del día"}
                                </h3>
                            </div>
                            <span className="small-indicator">
                                {loading
                                    ? language === "en"
                                        ? "Refreshing..."
                                        : "Actualizando..."
                                    : `${filteredBookings.length} ${
                                        language === "en" ? "records" : "registros"
                                    }`}
                            </span>
                        </div>

                        <div className="table-scroll">
                            <table>
                                <thead>
                                    <tr>
                                        <th>{language === "en" ? "Time" : "Hora"}</th>
                                        <th>{language === "en" ? "Client" : "Cliente"}</th>
                                        <th>
                                            {language === "en"
                                                ? "Professional"
                                                : "Profesional"}
                                        </th>
                                        <th>
                                            {language === "en" ? "Service" : "Servicio"}
                                        </th>
                                        <th>{language === "en" ? "Status" : "Estado"}</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    {filteredBookings.length > 0 ? (
                                        filteredBookings.map((booking) => (
                                            <tr key={booking.id}>
                                                <td>
                                                    {booking.start_at} -{" "}
                                                    {booking.end_at}
                                                </td>
                                                <td>{booking.client_name}</td>
                                                <td>
                                                    {booking.professional_name}
                                                </td>
                                                <td>{booking.service_name}</td>
                                                <td>
                                                    <StatusBadge
                                                        status={booking.status}
                                                    />
                                                </td>
                                            </tr>
                                        ))
                                    ) : (
                                        <tr>
                                            <td colSpan="5" className="empty-state">
                                                {language === "en"
                                                    ? "No bookings available for the selected filters."
                                                    : "No hay reservas disponibles para los filtros seleccionados."}
                                            </td>
                                        </tr>
                                    )}
                                </tbody>
                            </table>
                        </div>
                    </article>

                    <article className="panel-card">
                        <div className="panel-card-header">
                            <div>
                                <p className="panel-kicker">
                                    {language === "en" ? "Commerce" : "Comercio"}
                                </p>
                                <h3>
                                    {language === "en"
                                        ? "Recent orders"
                                        : "Órdenes recientes"}
                                </h3>
                            </div>
                            <span className="small-indicator">
                                {orders.length}{" "}
                                {language === "en" ? "records" : "registros"}
                            </span>
                        </div>

                        <div className="orders-list">
                            {orders.length > 0 ? (
                                orders.map((order) => (
                                    <div key={order.id} className="order-item">
                                        <div>
                                            <p className="order-title">
                                                {order.item}
                                            </p>
                                            <p className="order-client">
                                                {order.client_name}
                                            </p>
                                        </div>

                                        <div className="order-meta">
                                            <strong
                                                className={
                                                    hideAmounts ? "value-hidden" : ""
                                                }
                                            >
                                                {formatCurrency(order.amount)}
                                            </strong>
                                            <StatusBadge status={order.status} />
                                        </div>
                                    </div>
                                ))
                            ) : (
                                <div className="empty-state-box">
                                    {language === "en"
                                        ? "No recent orders available."
                                        : "No hay órdenes recientes disponibles."}
                                </div>
                            )}
                        </div>
                    </article>
                </section>
            </main>
        </div>
    );
}