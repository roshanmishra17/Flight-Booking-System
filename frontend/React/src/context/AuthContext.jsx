import { createContext, useEffect, useState } from "react";
import { getCurrentUser } from "../api/userApi";

export const AuthContext = createContext(null);

export function AuthProvider({ children }) {
    const [token, setToken] = useState(
        localStorage.getItem("token")
    );

    const [user, setUser] = useState(null);

    const [loading, setLoading] = useState(true);

    const login = (accessToken) => {
        localStorage.setItem("token", accessToken);
        setToken(accessToken);
    };

    const logout = () => {
        localStorage.removeItem("token");
        setToken(null);
        setUser(null);
    };

    useEffect(() => {
        async function loadUser() {

            if (!token) {
                setLoading(false);
                return;
            }

            try {
                const response = await getCurrentUser();
                setUser(response);
            }
            catch {
                logout();
            }
            finally {
                setLoading(false);
            }

        }

        loadUser();

    }, [token]);

    return (
        <AuthContext.Provider
            value={{
                token,
                user,
                loading,
                login,
                logout,
                isAuthenticated: !!user,
            }}
        >
            {children}
        </AuthContext.Provider>
    );
}