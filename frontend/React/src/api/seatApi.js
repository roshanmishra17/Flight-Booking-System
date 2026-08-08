import api from "./axios";

export async function getSeatMap(flightId) {
    const response = await api.get(`/flights/${flightId}/seats`);
    return response.data;
}