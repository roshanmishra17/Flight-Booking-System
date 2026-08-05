import { useForm } from "react-hook-form";
import { useNavigate, Link } from "react-router-dom";
import { useState } from "react";

import { loginUser } from "../../api/authApi";
import { useAuth } from "../../hooks/useAuth";
import "../../CSS/Login.css";

export default function Login() {
    const {
        register,
        handleSubmit,
        formState: { errors, isSubmitting },
    } = useForm();

    const [serverError, setServerError] = useState(null);
    const navigate = useNavigate();
    const { login } = useAuth();

    async function onSubmit(data) {

        try {
            const response = await loginUser(data);

            login(response.access_token);
            navigate("/");
        } catch (err) {

            if (!err.response) {
                setServerError("Unable to connect to the server.");
            } else if (err.response.status === 401) {
                setServerError("Incorrect email or password.");
            } else {
                setServerError(
                    err.response.data?.detail ||
                    "Something went wrong."
                );
            }
        }
    }

    return (
        <div className="login-page">
            <div className="login-glow" />

            <div className="login-wrap">
                <div className="login-brand">
                    <h1>SkyRoute</h1>
                    <p>Sign in to manage your trips</p>
                </div>

                <div className="login-card">
                    <div className="login-card-main">
                        <form onSubmit={handleSubmit(onSubmit)} noValidate>
                            {serverError && (
                                <div className="login-error-banner">{serverError}</div>
                            )}

                            <div className="login-field">
                                <label htmlFor="email">Email</label>
                                <input
                                    id="email"
                                    type="email"
                                    autoComplete="email"
                                    placeholder="you@example.com"
                                    className={errors.email ? "input-error" : ""}
                                    {...register("email", {
                                        onChange: () => setServerError(null),
                                        required: "Email is required",
                                        pattern: {
                                            value: /^\S+@\S+\.\S+$/,
                                            message: "Enter a valid email address",
                                        },
                                    })}
                                />
                                {errors.email && <p className="field-error">{errors.email.message}</p>}
                            </div>

                            <div className="login-field">
                                <label htmlFor="password">Password</label>
                                <input
                                    id="password"
                                    type="password"
                                    autoComplete="current-password"
                                    placeholder="••••••••"
                                    className={errors.password ? "input-error" : ""}
                                    {...register("password", { 
                                        onChange: () => setServerError(null),
                                        required: "Password is required" 
                                    })}
                                />
                                {errors.password && <p className="field-error">{errors.password.message}</p>}
                            </div>

                            <button type="submit" disabled={isSubmitting} className="login-submit">
                                {isSubmitting ? "Signing in…" : "Sign in"}
                            </button>

                            <p className="login-footer-text">
                                New to SkyRoute? <Link to="/register">Create an account</Link>
                            </p>
                        </form>
                    </div>

                    <div className="login-card-tab">
                        <span>✈ SKYROUTE</span>
                    </div>
                </div>
            </div>
        </div>
    );
}