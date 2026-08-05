import api from "./axios";

export async function getCurrentUser() {

    const response = await api.get(
        "/user/me",
    );

    return response.data;

}
