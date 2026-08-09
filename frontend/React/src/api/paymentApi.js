import api from "./axios";

export async function createPayment({ booking_id, payment_method, simulate_failure }) {
    const response = await api.post("/payments", {
        booking_id,
        payment_method,
        simulate_failure,
    });
    return response.data;
}