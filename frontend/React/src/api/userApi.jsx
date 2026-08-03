import api from "./axios";

export async function getCurrentUser() {

    const response = await api.get(
        "/users/me",
    );

    return response.data;

}
