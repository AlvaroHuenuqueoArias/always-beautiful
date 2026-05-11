export default function AssistantComposer({
    value = "",
    onChange,
    onSubmit,
    disabled = false,
}) {
    const isSubmitDisabled = disabled || !value.trim();

    function handleSubmit(event) {
        event.preventDefault();

        if (isSubmitDisabled) {
            return;
        }

        onSubmit(value.trim());
    }

    return (
        <form className="assistant-composer" onSubmit={handleSubmit}>
            <label
                className="assistant-composer__label"
                htmlFor="assistant-composer-message"
            >
                Mensaje para el asistente
            </label>

            <div className="assistant-composer__controls">
                <textarea
                    id="assistant-composer-message"
                    className="assistant-composer__input"
                    value={value}
                    onChange={(event) => onChange(event.target.value)}
                    placeholder="Escribe tu consulta"
                    rows={3}
                    disabled={disabled}
                />

                <button
                    type="submit"
                    className="assistant-composer__submit"
                    disabled={isSubmitDisabled}
                >
                    Enviar
                </button>
            </div>
        </form>
    );
}
