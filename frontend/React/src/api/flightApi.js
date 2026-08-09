import api from "./axios";

export async function searchFlights({ origin, destination, departureDate }) {
    const response = await api.get("/flights/search", {
        params: { origin, destination, departure_date: departureDate },
    });
    return response.data;
}

export async function searchFlightsRanked({ origin, destination, departureDate, travelClass, mode }) {
    const response = await api.get("/flights/search/ranked", {
        params: {
            origin,
            destination,
            departure_date: departureDate,
            travel_class: travelClass,
            mode,
        },
    });
    return response.data;
}

export async function searchAlternativeRoutes({ origin, destination, departureDate }) {
    const response = await api.get("/flights/search/alternatives", {
        params: { origin, destination, departure_date: departureDate },
    });
    return response.data;
}

export async function getFlight(flightId) {
    const response = await api.get(`/flights/${flightId}`);
    return response.data;
}