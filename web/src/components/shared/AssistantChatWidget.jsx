import { useState } from "react";

import {
    getOrCreateAssistantSessionId,
    sendAssistantMessage,
} from "../../services/assistantClient";
import AssistantChatPanel from "./AssistantChatPanel";
import AssistantComposer from "./AssistantComposer";
import AssistantMessageList from "./AssistantMessageList";

const INITIAL_ASSISTANT_MESSAGE = {
    id: "assistant-welcome",
    role: "assistant",
    content:
        "Hola, soy el asistente de Always Beautiful. Puedo orientarte para elegir servicios o productos; la disponibilidad, precios definitivos y pagos se revisan solo en los flujos autorizados de la web.",
    requiresDeposit: false,
    depositPercentage: 0,
    nextActions: [
        "Cuéntame qué servicio o tratamiento buscas.",
        "Pídeme una recomendación de producto.",
        "Si quieres reservar, te recordaré el abono web requerido.",
    ],
};

function createMessageId(role) {
    const timestamp = Date.now().toString(36);
    const randomValue = Math.random().toString(36).slice(2, 8);

    return `${role}-${timestamp}-${randomValue}`;
}

function buildAssistantMessage(response) {
    return {
        id: createMessageId("assistant"),
        role: "assistant",
        content: response.message,
        intent: response.intent,
        requiresDeposit: response.requiresDeposit,
        depositPercentage: response.depositPercentage,
        nextActions: response.nextActions,
    };
}

export default function AssistantChatWidget({ isOpen = false, onClose }) {
    const [messages, setMessages] = useState([INITIAL_ASSISTANT_MESSAGE]);
    const [draftMessage, setDraftMessage] = useState("");
    const [isLoading, setIsLoading] = useState(false);
    const [errorMessage, setErrorMessage] = useState("");

    async function handleSubmit(message) {
        const trimmedMessage = message.trim();

        if (!trimmedMessage || isLoading) {
            return;
        }

        const userMessage = {
            id: createMessageId("user"),
            role: "user",
            content: trimmedMessage,
            requiresDeposit: false,
            depositPercentage: 0,
            nextActions: [],
        };

        setMessages((currentMessages) => [...currentMessages, userMessage]);
        setDraftMessage("");
        setErrorMessage("");
        setIsLoading(true);

        try {
            const response = await sendAssistantMessage({
                sessionId: getOrCreateAssistantSessionId(),
                message: trimmedMessage,
            });

            setMessages((currentMessages) => [
                ...currentMessages,
                buildAssistantMessage(response),
            ]);
        } catch {
            setErrorMessage(
                "No pudimos contactar al asistente en este momento. Intenta nuevamente desde la web en unos minutos."
            );
        } finally {
            setIsLoading(false);
        }
    }

    return (
        <AssistantChatPanel isOpen={isOpen} onClose={onClose}>
            <AssistantMessageList
                messages={messages}
                onQuickReply={handleSubmit}
            />

            {isLoading && (
                <p className="assistant-chat-widget__status" aria-live="polite">
                    El asistente está preparando una respuesta.
                </p>
            )}

            {errorMessage && (
                <p className="assistant-chat-widget__error" role="alert">
                    {errorMessage}
                </p>
            )}

            <AssistantComposer
                value={draftMessage}
                onChange={setDraftMessage}
                onSubmit={handleSubmit}
                disabled={isLoading}
            />
        </AssistantChatPanel>
    );
}
