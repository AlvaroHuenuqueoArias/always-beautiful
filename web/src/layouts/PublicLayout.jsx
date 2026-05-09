import { Outlet } from "react-router-dom";
import FloatingAssistantButton from "../components/shared/FloatingAssistantButton";
import PublicFooter from "../components/shared/PublicFooter";
import PublicHeader from "../components/shared/PublicHeader";

export default function PublicLayout() {
    return (
        <div className="public-shell">
            <PublicHeader />

            <main className="public-main">
                <Outlet />
            </main>

            <FloatingAssistantButton />
            <PublicFooter />
        </div>
    );
}