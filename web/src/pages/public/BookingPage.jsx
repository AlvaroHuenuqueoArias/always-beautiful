export default function BookingPage() {
    return (
        <section className="public-page">
            <p className="public-page__eyebrow">Reservas</p>
            <h1 className="public-page__title">Shell público de reservas</h1>
            <p className="public-page__description">
                Esta pantalla será la traducción futura de `appointment.php` al
                frontend oficial del proyecto. Más adelante integrará servicio,
                profesional, fecha, horario y validaciones visuales.
            </p>

            <div className="public-card public-card--wide">
                <h2>Dependencias futuras</h2>
                <p>
                    Esta vista se conectará más adelante con los módulos backend
                    `booking` y `schedule`, apoyándose inicialmente en datos
                    ficticios controlados.
                </p>
            </div>
        </section>
    );
}