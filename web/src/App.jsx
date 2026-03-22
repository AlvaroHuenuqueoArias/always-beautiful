import { useEffect, useMemo, useState } from "react";
import { mockDashboard } from "./mockAdminData";

const API_BASE_URL = "http://127.0.0.1:8000";

function formatCurrency(value) {
    return new Intl.NumberFormat("es-CL", {
        style: "currency",
        currency: "CLP",
        maximumFractionDigits: 0
    }).format(value ?? 0);
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

function MetricCard({ label, value, accent }) {
    return (
        <article className={`metric-card accent-${accent}`}>
        <p className="metric-label">{label}</p>
        <h3 className="metric-value">{value}</h3>
        </article>
    );
}

export default function App() {
    const [selectedDate, setSelectedDate] = useState(todayAsInputValue());
    const [selectedProfessional, setSelectedProfessional] = useState("all");
    const [dashboardData, setDashboardData] = useState(mockDashboard);
    const [loading, setLoading] = useState(false);
    const [source, setSource] = useState("mock");
    const [error, setError] = useState("");

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
            throw new Error(`Dashboard request failed with status ${response.status}`);
        }

            const data = await response.json();

        setDashboardData({
            ...mockDashboard,
            ...data,
            professionals: data.professionals ?? mockDashboard.professionals,
            bookings: data.bookings ?? [],
            orders: data.orders ?? [],
            summary: {
            ...mockDashboard.summary,
            ...(data.summary ?? {})
            }
        });
        setSource("api");
        } catch (err) {
            if (err.name !== "AbortError") {
            setDashboardData(mockDashboard);
            setSource("mock");
            setError("Backend unavailable. Mock data loaded for UI continuity.");
        }
        } finally {
        setLoading(false);
        }
    }

    fetchDashboard();

        return () => controller.abort();
    }, [selectedDate, selectedProfessional]);

    const summary = dashboardData.summary ?? {};

    const bookings = useMemo(() => {
        const list = dashboardData.bookings ?? [];

    if (selectedProfessional === "all") return list;

    return list.filter(
        (booking) =>
            booking.professional_id === selectedProfessional ||
            booking.professional_name ===
            dashboardData.professionals?.find((p) => p.id === selectedProfessional)?.name
    );
    }, [dashboardData, selectedProfessional]);

    const orders = dashboardData.orders ?? [];
    const professionals = dashboardData.professionals ?? mockDashboard.professionals;

    return (
    <div className="dashboard-shell">
        <aside className="sidebar-panel">
        <div className="brand-box">
            <span className="brand-kicker">Always Beautiful</span>
            <h1>Admin Console</h1>
            <p>
            Advanced operational visibility for agenda, bookings, orders and daily salon metrics.
            </p>
        </div>

        <div className="system-box">
            <h2>System status</h2>
            <div className="system-row">
            <span>Data source</span>
            <strong className={`pill pill-${source}`}>{source.toUpperCase()}</strong>
            </div>
            <div className="system-row">
            <span>Interface mode</span>
            <strong>Neo Futurist Luxury</strong>
            </div>
            <div className="system-row">
            <span>Visual profile</span>
            <strong>Premium Admin</strong>
            </div>
        </div>
        </aside>

        <main className="main-panel">
        <header className="topbar">
            <div>
            <p className="eyebrow">Administrative Dashboard</p>
            <h2>Daily operations overview</h2>
            </div>

            <div className="filters-panel">
            <label className="field-group">
                <span>Date</span>
                <input
                type="date"
                value={selectedDate}
                onChange={(event) => setSelectedDate(event.target.value)}
                />
            </label>

            <label className="field-group">
                <span>Professional</span>
                <select
                value={selectedProfessional}
                onChange={(event) => setSelectedProfessional(event.target.value)}
                >
                {professionals.map((professional) => (
                    <option key={professional.id} value={professional.id}>
                    {professional.name}
                    </option>
                ))}
                </select>
            </label>
            </div>
        </header>

        {error && <div className="alert-banner">{error}</div>}

        <section className="metrics-grid">
            <MetricCard
            label="Today bookings"
            value={summary.totalBookings ?? 0}
            accent="pink"
            />
            <MetricCard
            label="Confirmed"
            value={summary.confirmedBookings ?? 0}
            accent="cream"
            />
            <MetricCard
            label="Pending"
            value={summary.pendingBookings ?? 0}
            accent="camel"
            />
            <MetricCard
            label="Today revenue"
            value={formatCurrency(summary.revenueToday ?? 0)}
            accent="graphite"
            />
        </section>

        <section className="content-grid">
            <article className="panel-card">
            <div className="panel-card-header">
                <div>
                <p className="panel-kicker">Agenda</p>
                <h3>Bookings of the day</h3>
                </div>
                <span className="small-indicator">
                {loading ? "Refreshing..." : `${bookings.length} records`}
                </span>
            </div>

            <div className="table-scroll">
                <table>
                <thead>
                    <tr>
                    <th>Time</th>
                    <th>Client</th>
                    <th>Professional</th>
                    <th>Service</th>
                    <th>Status</th>
                    </tr>
                </thead>
                <tbody>
                    {bookings.length > 0 ? (
                    bookings.map((booking) => (
                        <tr key={booking.id}>
                        <td>
                            {booking.start_at} - {booking.end_at}
                        </td>
                        <td>{booking.client_name}</td>
                        <td>{booking.professional_name}</td>
                        <td>{booking.service_name}</td>
                        <td>
                            <StatusBadge status={booking.status} />
                        </td>
                        </tr>
                    ))
                    ) : (
                    <tr>
                        <td colSpan="5" className="empty-state">
                        No bookings available for the selected filters.
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
                <p className="panel-kicker">Commerce</p>
                <h3>Recent orders</h3>
                </div>
                <span className="small-indicator">{orders.length} records</span>
            </div>

            <div className="orders-list">
                {orders.length > 0 ? (
                orders.map((order) => (
                    <div key={order.id} className="order-item">
                    <div>
                        <p className="order-title">{order.item}</p>
                        <p className="order-client">{order.client_name}</p>
                    </div>

                    <div className="order-meta">
                        <strong>{formatCurrency(order.amount)}</strong>
                        <StatusBadge status={order.status} />
                    </div>
                    </div>
                ))
                ) : (
                <div className="empty-state-box">
                    No recent orders available.
                </div>
                )}
            </div>
            </article>
        </section>
        </main>
    </div>
    );
}