const DEPOSIT_WARNING =
    "Para confirmar la hora se debe cancelar el 20% del valor del servicio desde la web.";

const COMMERCIAL_COPY_REPLACEMENTS = [
    {
        pattern: /reserva confirmada/gi,
        replacement: "reserva pendiente de validación",
    },
    {
        pattern: /hora confirmada/gi,
        replacement: "hora pendiente de validación",
    },
    {
        pattern: /cita agendada/gi,
        replacement: "solicitud de cita recibida",
    },
];

function sanitizeCommercialCopy(value) {
    if (typeof value !== "string") {
        return "";
    }

    return COMMERCIAL_COPY_REPLACEMENTS.reduce(
        (currentValue, replacement) =>
            currentValue.replace(replacement.pattern, replacement.replacement),
        value
    );
}

function getRoleLabel(role) {
    return role === "user" ? "Tú" : "Asistente";
}

export default function AssistantMessageList({ messages = [] }) {
    return (
        <div
            className="assistant-message-list"
            role="log"
            aria-live="polite"
            aria-relevant="additions text"
        >
            {messages.map((message) => (
                <article
                    key={message.id}
                    className={`assistant-message assistant-message--${message.role}`}
                >
                    <p className="assistant-message__role">
                        {getRoleLabel(message.role)}
                    </p>

                    <p className="assistant-message__content">
                        {sanitizeCommercialCopy(message.content)}
                    </p>

                    {message.requiresDeposit && (
                        <p className="assistant-message__deposit-warning">
                            {DEPOSIT_WARNING}
                        </p>
                    )}

                    {Array.isArray(message.nextActions) &&
                        message.nextActions.length > 0 && (
                            <ul className="assistant-message__next-actions">
                                {message.nextActions.map((action) => (
                                    <li key={action}>
                                        {sanitizeCommercialCopy(action)}
                                    </li>
                                ))}
                            </ul>
                        )}
                </article>
            ))}
        </div>
    );
}
