export default function AssistantChatPanel({ isOpen, onClose, children }) {
    if (!isOpen) {
        return null;
    }

    return (
        <section
            id="assistant-chat-panel"
            className="assistant-chat-panel"
            role="dialog"
            aria-modal="false"
            aria-labelledby="assistant-chat-panel-title"
        >
            <header className="assistant-chat-panel__header">
                <div>
                    <p className="assistant-chat-panel__eyebrow">
                        Atención comercial
                    </p>
                    <h2
                        id="assistant-chat-panel-title"
                        className="assistant-chat-panel__title"
                    >
                        Asistente Always Beautiful
                    </h2>
                </div>

                <button
                    type="button"
                    className="assistant-chat-panel__close"
                    aria-label="Cerrar asistente Always Beautiful"
                    onClick={onClose}
                >
                    ×
                </button>
            </header>

            <div className="assistant-chat-panel__body">{children}</div>
        </section>
    );
}
