import { useState } from "react";
import { Outlet } from "react-router-dom";
import AssistantChatWidget from "../components/shared/AssistantChatWidget";
import FloatingAssistantButton from "../components/shared/FloatingAssistantButton";
import PublicFooter from "../components/shared/PublicFooter";
import PublicHeader from "../components/shared/PublicHeader";

const ASSISTANT_CHAT_STATE_STORAGE_KEY =
    "alwaysBeautifulAssistantChatState";

function getInitialAssistantOpenState() {
    const storage = globalThis.sessionStorage;

    if (!storage) {
        return false;
    }

    try {
        const storedState = JSON.parse(
            storage.getItem(ASSISTANT_CHAT_STATE_STORAGE_KEY)
        );

        return Boolean(storedState?.isOpen);
    } catch {
        return false;
    }
}

export default function PublicLayout() {
    const [isAssistantOpen, setIsAssistantOpen] = useState(
        getInitialAssistantOpenState
    );

    return (
        <div className="public-shell">
            <PublicHeader />

            <main className="public-main">
                <Outlet />
            </main>

            <AssistantChatWidget
                isOpen={isAssistantOpen}
                onClose={() => setIsAssistantOpen(false)}
            />
            <FloatingAssistantButton
                isOpen={isAssistantOpen}
                onToggle={() =>
                    setIsAssistantOpen((currentIsOpen) => !currentIsOpen)
                }
            />
            <PublicFooter />
        </div>
    );
}
