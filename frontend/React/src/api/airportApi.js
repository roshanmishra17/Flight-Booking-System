import api from "./axios";

export async function getAirports() {
    const response = await api.get("/airports");
    return response.data;
}