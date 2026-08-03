import { Routes, Route } from "react-router-dom";

import Home from "../pages/user/Home";
import Login from "../pages/auth/Login";
import Register from "../pages/auth/Register";
import SearchResults from "../pages/user/SearchResults";
import SeatSelection from "../pages/user/SeatSelection";
import Booking from "../pages/user/Booking";
import Payment from "../pages/user/Payment";
import MyBookings from "../pages/user/MyBookings";
import AdminDashboard from "../admin/AdminDashboard";

export default function AppRoutes() {
    return (
        <Routes>
            <Route path="/" element={<Home />} />

            <Route path="/login" element={<Login />} />
            <Route path="/register" element={<Register />} />

            <Route path="/search" element={<SearchResults />} />

            <Route path="/seat-selection" element={<SeatSelection />} />

            <Route path="/booking/:bookingId" element={<Booking />} />

            <Route path="/payment/:bookingId" element={<Payment />} />

            <Route path="/my-bookings" element={<MyBookings />} />

            <Route path="/admin" element={<AdminDashboard />} />
        </Routes>
    );
}