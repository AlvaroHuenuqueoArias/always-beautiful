const COPY = {
    en: {
        ecommerce: "E-commerce",
        productOverview: "Product sales overview",
        orders: "orders",
        totalProductEcommerce: "Total product e-commerce",
        totalProductsSold: "Total products sold",
        topProduct: "Top product",
        bestSalesDay: "Best sales day",
        thisMonth: "This month",
        lastMonth: "Last month",
        thisMonthShare: "This month share",
        lastMonthShare: "Last month share",
        quickReference: "Quick reference",
        latestProducts: "Latest 3 products sold",
        items: "items",
        noSales: "No recent product sales available.",
        ownerCollection: "Owner collection",
        secondaryContribution: "Secondary stylist contribution",
        businessDay: "Business day:",
        weeklyView: "Weekly view:",
        collectedToday: "Collected today:",
        collectedWeek: "Collected this week:",
        professional: "Professional",
        todayService: "Today service"
    },
    es: {
        ecommerce: "E-commerce",
        productOverview: "Resumen de ventas de productos",
        orders: "órdenes",
        totalProductEcommerce: "Total e-commerce productos",
        totalProductsSold: "Productos vendidos",
        topProduct: "Producto top",
        bestSalesDay: "Mejor día de venta",
        thisMonth: "Este mes",
        lastMonth: "Mes pasado",
        thisMonthShare: "Participación mes actual",
        lastMonthShare: "Participación mes pasado",
        quickReference: "Referencia rápida",
        latestProducts: "Últimos 3 productos vendidos",
        items: "items",
        noSales: "No hay ventas recientes de productos.",
        ownerCollection: "Recaudación de la dueña",
        secondaryContribution: "Aporte de estilista secundaria",
        businessDay: "Día laboral:",
        weeklyView: "Vista semanal:",
        collectedToday: "Recaudado hoy:",
        collectedWeek: "Recaudado esta semana:",
        professional: "Profesional",
        todayService: "Servicio del día"
    }
};

function formatCurrency(value) {
    return new Intl.NumberFormat("es-CL", {
        style: "currency",
        currency: "CLP",
        maximumFractionDigits: 0
    }).format(value ?? 0);
}

function CircularProgress({
    current = 0,
    previous = 0,
    hideAmounts = false,
    language = "en"
}) {
    const t = COPY[language];
    const total = current + previous || 1;
    const currentShare = Math.round((current / total) * 100);
    const previousShare = 100 - currentShare;

    return (
        <div className="ecommerce-progress-wrap">
            <div
                className="ecommerce-progress-circle"
                style={{
                    background: `conic-gradient(
                        var(--accent-commerce) 0% ${currentShare}%,
                        #343434 ${currentShare}% 100%
                    )`
                }}
            >
                <div className="ecommerce-progress-inner">
                    <strong>{currentShare}%</strong>
                    <span>{t.thisMonthShare}</span>
                </div>
            </div>

            <div className="ecommerce-progress-legend">
                <div className="progress-legend-item">
                    <span className="legend-dot current-dot" />
                    <div>
                        <strong>{t.thisMonth}</strong>
                        <span className={hideAmounts ? "value-hidden" : ""}>
                            {formatCurrency(current)}
                        </span>
                    </div>
                </div>

                <div className="progress-legend-item">
                    <span className="legend-dot previous-dot" />
                    <div>
                        <strong>{t.lastMonth}</strong>
                        <span className={hideAmounts ? "value-hidden" : ""}>
                            {formatCurrency(previous)}
                        </span>
                    </div>
                </div>

                <div className="progress-legend-item progress-legend-secondary">
                    <strong>{previousShare}%</strong>
                    <span>{t.lastMonthShare}</span>
                </div>
            </div>
        </div>
    );
}

function DetailLine({ label, value, valueClass = "" }) {
    return (
        <div className="owner-breakdown-line">
            <span>{label}</span>
            <strong className={valueClass}>{value}</strong>
        </div>
    );
}

export default function EcommercePerformance({
    summary = {},
    sales = [],
    ownerBreakdown = {},
    hideAmounts = false,
    language = "en"
}) {
    const t = COPY[language];
    const latestProducts = sales.slice(0, 3);

    return (
        <section className="ecommerce-grid">
            <article className="panel-card ecommerce-summary-card">
                <div className="panel-card-header">
                    <div>
                        <p className="panel-kicker">{t.ecommerce}</p>
                        <h3>{t.productOverview}</h3>
                    </div>
                    <span className="small-indicator">
                        {summary.totalOrders ?? 0} {t.orders}
                    </span>
                </div>

                <div className="ecommerce-main-kpi">
                    <span>{t.totalProductEcommerce}</span>
                    <strong className={hideAmounts ? "value-hidden" : ""}>
                        {formatCurrency(summary.totalRevenue ?? 0)}
                    </strong>
                </div>

                <div className="ecommerce-inline-meta">
                    <div className="ecommerce-mini-box">
                        <span>{t.totalProductsSold}</span>
                        <strong>{summary.totalOrders ?? 0}</strong>
                    </div>

                    <div className="ecommerce-mini-box">
                        <span>{t.topProduct}</span>
                        <strong>{summary.topProduct ?? "N/A"}</strong>
                    </div>

                    <div className="ecommerce-mini-box">
                        <span>{t.bestSalesDay}</span>
                        <strong>
                            {language === "es"
                                ? summary.bestDayEs ?? summary.bestDay
                                : summary.bestDay ?? summary.bestDayEs}
                        </strong>
                    </div>
                </div>

                <CircularProgress
                    current={summary.currentMonthRevenue ?? 0}
                    previous={summary.previousMonthRevenue ?? 0}
                    hideAmounts={hideAmounts}
                    language={language}
                />
            </article>

            <article className="panel-card ecommerce-side-card">
                <div className="panel-card-header">
                    <div>
                        <p className="panel-kicker">{t.quickReference}</p>
                        <h3>{t.latestProducts}</h3>
                    </div>
                    <span className="small-indicator">
                        {latestProducts.length} {t.items}
                    </span>
                </div>

                <div className="ecommerce-products-list">
                    {latestProducts.length > 0 ? (
                        latestProducts.map((sale) => (
                            <div key={sale.id} className="ecommerce-product-item">
                                <div>
                                    <p className="ecommerce-product-title">
                                        {sale.product_name}
                                    </p>
                                    <p className="ecommerce-product-subtitle">
                                        {sale.sale_date}
                                    </p>
                                </div>
                                <strong className={hideAmounts ? "value-hidden" : ""}>
                                    {formatCurrency(sale.amount)}
                                </strong>
                            </div>
                        ))
                    ) : (
                        <div className="empty-state-box">{t.noSales}</div>
                    )}
                </div>

                <div className="owner-breakdown-card">
                    <p className="panel-kicker">{t.ownerCollection}</p>
                    <h4>{t.secondaryContribution}</h4>

                    <div className="owner-breakdown-period">
                        <DetailLine
                            label={t.businessDay}
                            value={ownerBreakdown.currentBusinessDay ?? "N/A"}
                            valueClass="value-green-soft"
                        />
                        <DetailLine
                            label={t.weeklyView}
                            value={ownerBreakdown.weekRangeLabel ?? "N/A"}
                            valueClass="value-green-soft"
                        />
                    </div>

                    <div className="owner-breakdown-amounts">
                        <div className="owner-breakdown-amount-box">
                            <span>{t.collectedToday}</span>
                            <strong
                                className={`value-green-soft ${hideAmounts ? "value-hidden" : ""}`}
                            >
                                {formatCurrency(ownerBreakdown.amountCollectedToday ?? 0)}
                            </strong>
                        </div>

                        <div className="owner-breakdown-amount-box">
                            <span>{t.collectedWeek}</span>
                            <strong
                                className={`value-green-soft ${hideAmounts ? "value-hidden" : ""}`}
                            >
                                {formatCurrency(ownerBreakdown.amountCollectedWeek ?? 0)}
                            </strong>
                        </div>
                    </div>

                    <div className="owner-breakdown-main owner-breakdown-rate">
                        <strong className="value-yellow-soft">
                            {ownerBreakdown.rateLabel ?? "N/A"}
                        </strong>
                        <span>{ownerBreakdown.rateContext ?? ""}</span>
                    </div>

                    <div className="owner-breakdown-meta">
                        <DetailLine
                            label={t.professional}
                            value={ownerBreakdown.professionalName ?? "N/A"}
                            valueClass="value-pink-soft"
                        />

                        <DetailLine
                            label={t.todayService}
                            value={ownerBreakdown.serviceName ?? "N/A"}
                            valueClass="value-gold-soft"
                        />
                    </div>
                </div>
            </article>
        </section>
    );
}