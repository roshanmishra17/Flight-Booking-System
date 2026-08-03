import api from "./axios";

export async function loginUser(data) {

    const formData = new URLSearchParams();

    formData.append(
        "username",
        data.email,
    );

    formData.append(
        "password",
        data.password,
    );

    const response = await api.post(
        "/auth/login",
        formData,
        {
            headers: {
                "Content-Type":
                    "application/x-www-form-urlencoded",
            },
        },
    );

    return response.data;
}

export async function registerUser(data) {

    const response = await api.post(
        "/auth/register",
        data,
    );

    return response.data;

}