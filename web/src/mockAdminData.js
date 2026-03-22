export const mockDashboard = {
    date: "2026-03-20",
    professional_id: "all",
    summary: {
        totalBookings: 18,
        confirmedBookings: 12,
        pendingBookings: 4,
        cancelledBookings: 2,
        totalOrders: 7,
        revenueToday: 286000
    },
    bookings: [
        {
        id: "BK-1001",
        client_name: "Camila Rojas",
        professional_name: "María González",
        service_name: "Balayage + Corte",
        start_at: "09:00",
        end_at: "10:30",
        status: "confirmed"
        },
        {
        id: "BK-1002",
        client_name: "Valentina Pérez",
        professional_name: "María González",
        service_name: "Manicure Permanente",
        start_at: "11:00",
        end_at: "12:00",
        status: "pending"
        },
        {
        id: "BK-1003",
        client_name: "Daniela Soto",
        professional_name: "Paula Ramírez",
        service_name: "Color Global",
        start_at: "12:30",
        end_at: "14:00",
        status: "confirmed"
        },
        {
        id: "BK-1004",
        client_name: "Sofía Herrera",
        professional_name: "Paula Ramírez",
        service_name: "Peinado",
        start_at: "16:00",
        end_at: "17:00",
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
    professionals: [
    { id: "all", name: "All professionals" },
    { id: "PRO-1", name: "María González" },
    { id: "PRO-2", name: "Paula Ramírez" }
    ]
};