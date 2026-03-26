export const mockDashboard = {
    date: "2026-03-20",
    professional_id: "all",
    summary: {
        totalBookings: 18,
        confirmedBookings: 12,
        pendingBookings: 4,
        cancelledBookings: 2,
        totalOrders: 7,
        revenueToday: 286000,
        revenueWeekGlobal: 1426000,
        ownerShareToday: 57600
    },
    executiveKpis: {
        revenueMonth: 4820000,
        ownerShareMonth: 1928000,
        averageTicket: 39700,
        occupancyRate: 84,
        cancellationRate: 11
    },
    alerts: [
        {
            id: "ALT-1",
            title_en: "Peak time",
            title_es: "Hora peak",
            message_en: "13:00 to 15:00 is the busiest block today.",
            message_es: "13:00 a 15:00 es el bloque con más movimiento hoy.",
            tag_en: "Agenda",
            tag_es: "Agenda",
            kind: "focus"
        },
        {
            id: "ALT-2",
            title_en: "Top load",
            title_es: "Mayor carga",
            message_en: "María carries the highest booking load this week.",
            message_es: "María concentra la mayor carga de reservas esta semana.",
            tag_en: "Today",
            tag_es: "Hoy",
            kind: "attention"
        },
        {
            id: "ALT-3",
            title_en: "Free slots",
            title_es: "Horas libres",
            message_en: "Paula still has availability from 11:00 to 13:00.",
            message_es: "Paula aún tiene disponibilidad entre 11:00 y 13:00.",
            tag_en: "Open",
            tag_es: "Libre",
            kind: "available"
        },
        {
            id: "ALT-4",
            title_en: "Follow-up",
            title_es: "Seguimiento",
            message_en: "One cancelled booking should be reviewed today.",
            message_es: "Una reserva cancelada debe revisarse hoy.",
            tag_en: "Review",
            tag_es: "Revisar",
            kind: "followup"
        }
    ],
    stylistTrends: [
        {
            professionalId: "PRO-1",
            professionalName: "María González",
            variationLabel: "+13.3%",
            direction: "up",
            summary_en:
                "María is showing a stronger month and a clearer upward pace in weekly production.",
            summary_es:
                "María muestra un mes más fuerte y una subida más clara en su producción semanal.",
            points: [
                { label: "W1", value: 620000 },
                { label: "W2", value: 700000 },
                { label: "W3", value: 660000 },
                { label: "W4", value: 840000 }
            ]
        },
        {
            professionalId: "PRO-2",
            professionalName: "Paula Ramírez",
            variationLabel: "+5.3%",
            direction: "stable",
            summary_en:
                "Paula remains more stable and still has room to improve occupancy between 11:00 and 13:00.",
            summary_es:
                "Paula se mantiene más estable y aún tiene espacio para mejorar la ocupación entre 11:00 y 13:00.",
            points: [
                { label: "W1", value: 360000 },
                { label: "W2", value: 415000 },
                { label: "W3", value: 392000 },
                { label: "W4", value: 450000 }
            ]
        }
    ],
    professionalStats: [
        {
            id: "PRO-1",
            name: "María González",
            appointments: 11,
            revenue: 242000,
            averageTicket: 52000,
            occupancyRate: 91,
            cancellationRate: 5,
            topService: "Balayage + Corte"
        },
        {
            id: "PRO-2",
            name: "Paula Ramírez",
            appointments: 7,
            revenue: 144000,
            averageTicket: 34000,
            occupancyRate: 72,
            cancellationRate: 14,
            topService: "Color Global"
        }
    ],
    bookings: [
        {
            id: "BK-1001",
            professional_id: "PRO-1",
            client_name: "Camila Rojas",
            professional_name: "María González",
            service_name: "Balayage + Corte",
            start_at: "11:00",
            end_at: "12:30",
            status: "confirmed"
        },
        {
            id: "BK-1002",
            professional_id: "PRO-1",
            client_name: "Valentina Pérez",
            professional_name: "María González",
            service_name: "Manicure Permanente",
            start_at: "13:00",
            end_at: "14:00",
            status: "pending"
        },
        {
            id: "BK-1003",
            professional_id: "PRO-2",
            client_name: "Daniela Soto",
            professional_name: "Paula Ramírez",
            service_name: "Color Global",
            start_at: "15:00",
            end_at: "16:30",
            status: "confirmed"
        },
        {
            id: "BK-1004",
            professional_id: "PRO-2",
            client_name: "Sofía Herrera",
            professional_name: "Paula Ramírez",
            service_name: "Peinado",
            start_at: "17:30",
            end_at: "18:30",
            status: "cancelled"
        }
    ],
    orders: [
        {
            id: "OR-3001",
            client_name: "Camila Rojas",
            item: "Tratamiento capilar premium",
            amount: 42000,
            status: "paid"
        },
        {
            id: "OR-3002",
            client_name: "Daniela Soto",
            item: "Pack cuidado color",
            amount: 36000,
            status: "pending"
        },
        {
            id: "OR-3003",
            client_name: "Sofía Herrera",
            item: "Línea hidratación intensa",
            amount: 58000,
            status: "paid"
        }
    ],
    ecommerceSummary: {
        totalOrders: 5,
        totalRevenue: 214000,
        revenueToday: 52000,
        revenueWeek: 148000,
        currentMonthRevenue: 214000,
        previousMonthRevenue: 168000,
        topProduct: "Pack cuidado color",
        bestDay: "Thursday",
        bestDayEs: "Jueves",
        currentDayOfMonth: 20,
        daysInMonth: 31
    },
    ecommerceSales: [
        {
            id: "EC-1005",
            client_name: "Ignacia Muñoz",
            product_name: "Mascarilla reparación profunda",
            sale_date: "2026-03-20",
            amount: 50000,
            status: "paid"
        },
        {
            id: "EC-1004",
            client_name: "Valentina Pérez",
            product_name: "Shampoo nutritivo profesional",
            sale_date: "2026-03-20",
            amount: 28000,
            status: "pending"
        },
        {
            id: "EC-1003",
            client_name: "Sofía Herrera",
            product_name: "Línea hidratación intensa",
            sale_date: "2026-03-19",
            amount: 58000,
            status: "paid"
        },
        {
            id: "EC-1002",
            client_name: "Daniela Soto",
            product_name: "Tratamiento capilar premium",
            sale_date: "2026-03-18",
            amount: 42000,
            status: "paid"
        },
        {
            id: "EC-1001",
            client_name: "Camila Rojas",
            product_name: "Pack cuidado color",
            sale_date: "2026-03-17",
            amount: 36000,
            status: "paid"
        }
    ],
    ownerBreakdown: {
        currentBusinessDay: "Friday",
        weekRangeLabel: "Tuesday to Saturday",
        amountCollectedToday: 57600,
        amountCollectedWeek: 198400,
        rateLabel: "40% retained",
        rateContext: "Owner share on Color Global service value",
        professionalName: "Paula Ramírez",
        serviceName: "Color Global"
    },
    professionals: [
        { id: "all", name: "All professionals" },
        { id: "PRO-1", name: "María González" },
        { id: "PRO-2", name: "Paula Ramírez" }
    ]
};