import { useForm } from "react-hook-form";
import { useNavigate, Link } from "react-router-dom";
import { useState } from "react";

import { registerUser } from "../../api/authApi";
import "../../CSS/Login.css";

export default function Register() {
    const {
        register,
        handleSubmit,
        watch,
        formState: { errors, isSubmitting },
    } = useForm();

    const [serverError, setServerError] = useState(null);
    const [success, setSuccess] = useState(false);
    const navigate = useNavigate();

    const password = watch("password");

    async function onSubmit(data) {
        setServerError(null);
        try {
            await registerUser({
                email: data.email,
                password: data.password,
                full_name: data.fullName,
            });
            setSuccess(true);
            setTimeout(() => navigate("/login"), 1500);
        } catch (err) {
            if (err.response?.status === 409) {
                setServerError("An account with this email already exists.");
            }else if (err.response?.status === 422) {
                setServerError("Please check your details and try again.");
            }else if (!err.response) {
                setServerError("Unable to connect to the server.");
            } else if (err.response.status === 409) {
                setServerError("An account with this email already exists.");
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
                    <p>Create your account</p>
                </div>

                <div className="login-card">
                    <div className="login-card-main">
                        {success ? (
                            <div className="login-error-banner" style={{ background: "#f0fdf4", borderColor: "#bbf7d0", color: "#15803d" }}>
                                Account created. Redirecting to sign in…
                            </div>
                        ) : (
                            <form onSubmit={handleSubmit(onSubmit)} noValidate>
                                {serverError && (
                                    <div className="login-error-banner">{serverError}</div>
                                )}

                                <div className="login-field">
                                    <label htmlFor="fullName">Full name</label>
                                    <input
                                        id="fullName"
                                        type="text"
                                        autoComplete="name"
                                        placeholder="James Bond"
                                        className={errors.fullName ? "input-error" : ""}
                                        {...register("fullName", {
                                            onChange: () => setServerError(null),
                                            required: "Full name is required",
                                            minLength: { value: 2, message: "Name is too short" },
                                        })}
                                    />
                                    {errors.fullName && <p className="field-error">{errors.fullName.message}</p>}
                                </div>

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
                                        autoComplete="new-password"
                                        placeholder="At least 8 characters"
                                        className={errors.password ? "input-error" : ""}
                                        {...register("password", {
                                            required: "Password is required",
                                            minLength: { value: 8, message: "Must be at least 8 characters" },
                                        })}
                                    />
                                    {errors.password && <p className="field-error">{errors.password.message}</p>}
                                </div>

                                <div className="login-field">
                                    <label htmlFor="confirmPassword">Confirm password</label>
                                    <input
                                        id="confirmPassword"
                                        type="password"
                                        autoComplete="new-password"
                                        placeholder="Re-enter your password"
                                        className={errors.confirmPassword ? "input-error" : ""}
                                        {...register("confirmPassword", {
                                            onChange: () => setServerError(null),
                                            required: "Please confirm your password",
                                            validate: (value) => value === password || "Passwords do not match",
                                        })}
                                    />
                                    {errors.confirmPassword && (
                                        <p className="field-error">{errors.confirmPassword.message}</p>
                                    )}
                                </div>

                                <button type="submit" disabled={isSubmitting} className="login-submit">
                                    {isSubmitting ? "Creating account…" : "Create account"}
                                </button>

                                <p className="login-footer-text">
                                    Already have an account? <Link to="/login">Sign in</Link>
                                </p>
                            </form>
                        )}
                    </div>

                    <div className="login-card-tab">
                        <span>✈ SKYROUTE</span>
                    </div>
                </div>
            </div>
        </div>
    );
}