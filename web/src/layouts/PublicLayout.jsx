import { Outlet } from "react-router-dom";
import PublicFooter from "../components/shared/PublicFooter";
import PublicHeader from "../components/shared/PublicHeader";

export default function PublicLayout() {
    return (
        <div className="public-shell">
            <PublicHeader />

            <main className="public-main">
                <Outlet />
            </main>

            <PublicFooter />
        </div>
    );
}