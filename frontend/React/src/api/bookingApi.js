import api from "./axios";
export async function getBooking(bookingId) {
    const response = await api.get(`/bookings/${bookingId}`);
    return response.data;
}

export async function createBooking(data) {
    const response = await api.post("/bookings", data);
    return response.data;
}

export async function getMyBookings() {
    const response = await api.get("/bookings/me");
    return response.data;
}

export async function cancelBooking(bookingId) {
    const response = await api.patch(`/bookings/${bookingId}/cancel`);
    return response.data;
}