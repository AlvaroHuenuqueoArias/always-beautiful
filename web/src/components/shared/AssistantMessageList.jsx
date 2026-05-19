import { useEffect, useRef } from "react";

const DEPOSIT_WARNING =
    "La hora queda pendiente hasta confirmación del salón y abono web.";

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

function getInformationalActions(nextActions) {
    if (!Array.isArray(nextActions)) {
        return [];
    }

    return nextActions
        .map((action) => sanitizeCommercialCopy(action))
        .filter((action) => action.trim());
}

function getQuickReplyActions(quickReplies) {
    if (!Array.isArray(quickReplies)) {
        return [];
    }

    return quickReplies
        .map((quickReply) => ({
            ...quickReply,
            label: sanitizeCommercialCopy(quickReply?.label),
            message:
                typeof quickReply?.message === "string"
                    ? quickReply.message
                    : "",
        }))
        .filter(({ label, message }) => label.trim() && message.trim());
}

export default function AssistantMessageList({
    messages = [],
    onQuickReply,
    disabled = false,
}) {
    const endOfMessagesRef = useRef(null);

    useEffect(() => {
        endOfMessagesRef.current?.scrollIntoView({
            behavior: "smooth",
            block: "end",
        });
    }, [messages.length]);

    return (
        <div
            className="assistant-message-list"
            role="log"
            aria-live="polite"
            aria-relevant="additions text"
        >
            {messages.map((message) => {
                const informationalActions = getInformationalActions(
                    message.nextActions
                );
                const quickReplyActions = getQuickReplyActions(
                    message.quickReplies
                );

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

                        {message.cartPayload && (
                            <p className="assistant-message__deposit-warning">
                                {DEPOSIT_WARNING}
                            </p>
                        )}

                        {informationalActions.length > 0 && (
                            <ul className="assistant-message__next-actions">
                                {informationalActions.map((action, index) => (
                                    <li key={`${message.id}-next-${index}`}>
                                        {action}
                                    </li>
                                ))}
                            </ul>
                        )}

                        {quickReplyActions.length > 0 && (
                            <div
                                className="assistant-message__quick-replies"
                                aria-label="Acciones rápidas"
                            >
                                {quickReplyActions.map((quickReply, index) => (
                                    <button
                                        key={`${message.id}-${index}-${quickReply.label}`}
                                        type="button"
                                        className="assistant-message__quick-reply"
                                        disabled={disabled}
                                        onClick={() => onQuickReply?.(quickReply)}
                                    >
                                        {quickReply.label}
                                    </button>
                                ))}
                            </div>
                        )}
                    </article>
                );
            })}
            <div ref={endOfMessagesRef} aria-hidden="true" />
        </div>
    );
}
