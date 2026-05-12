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

function getQuickReplyActions(nextActions) {
    if (!Array.isArray(nextActions)) {
        return [];
    }

    return nextActions
        .map((action) => ({
            action,
            label: sanitizeCommercialCopy(action),
        }))
        .filter(
            ({ action, label }) =>
                typeof action === "string" && action.trim() && label.trim()
        );
}

export default function AssistantMessageList({ messages = [], onQuickReply }) {
    return (
        <div
            className="assistant-message-list"
            role="log"
            aria-live="polite"
            aria-relevant="additions text"
        >
            {messages.map((message) => {
                const quickReplyActions = getQuickReplyActions(message.nextActions);

                return (
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

                        {quickReplyActions.length > 0 && (
                            <div
                                className="assistant-message__quick-replies"
                                aria-label="Acciones rápidas"
                            >
                                {quickReplyActions.map(({ action, label }, index) => (
                                    <button
                                        key={`${message.id}-${index}-${label}`}
                                        type="button"
                                        className="assistant-message__quick-reply"
                                        onClick={() => onQuickReply?.(action)}
                                    >
                                        {label}
                                    </button>
                                ))}
                            </div>
                        )}
                    </article>
                );
            })}
        </div>
    );
}
