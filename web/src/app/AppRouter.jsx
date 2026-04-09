import { BrowserRouter, Navigate, Route, Routes } from "react-router-dom";
import AdminLayout from "../layouts/AdminLayout";
import PublicLayout from "../layouts/PublicLayout";
import DashboardPage from "../pages/admin/DashboardPage";
import BookingPage from "../pages/public/BookingPage";
import CartPage from "../pages/public/CartPage";
import CheckoutPage from "../pages/public/CheckoutPage";
import HomePage from "../pages/public/HomePage";
import ProductsPage from "../pages/public/ProductsPage";
import ServicesPage from "../pages/public/ServicesPage";

export default function AppRouter() {
    return (
        <BrowserRouter>
            <Routes>
                <Route element={<PublicLayout />}>
                    <Route path="/" element={<HomePage />} />
                    <Route path="/services" element={<ServicesPage />} />
                    <Route path="/products" element={<ProductsPage />} />
                    <Route path="/cart" element={<CartPage />} />
                    <Route path="/checkout" element={<CheckoutPage />} />
                    <Route path="/booking" element={<BookingPage />} />
                </Route>

                <Route element={<AdminLayout />}>
                    <Route path="/admin" element={<DashboardPage />} />
                </Route>

                <Route path="*" element={<Navigate to="/" replace />} />
            </Routes>
        </BrowserRouter>
    );
}