import { useState } from "react";
import { Outlet } from "react-router-dom";
import AssistantChatWidget from "../components/shared/AssistantChatWidget";
import FloatingAssistantButton from "../components/shared/FloatingAssistantButton";
import PublicFooter from "../components/shared/PublicFooter";
import PublicHeader from "../components/shared/PublicHeader";

export default function PublicLayout() {
    const [isAssistantOpen, setIsAssistantOpen] = useState(false);

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
