import { Outlet } from "react-router-dom";

export default function AdminLayout() {
    return (
        <div className="admin-layout-shell">
            <Outlet />
        </div>
    );
}