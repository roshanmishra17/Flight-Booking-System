import { Link, useNavigate } from "react-router-dom";
import { useState, useRef, useEffect } from "react";

import { useAuth } from "../hooks/useAuth";
import "../CSS/Navbar.css";

export default function Navbar() {
    const { isAuthenticated, user, logout, loading } = useAuth();
    const navigate = useNavigate();
    const [menuOpen, setMenuOpen] = useState(false);
    const menuRef = useRef(null);

    useEffect(() => {
        function handleClickOutside(e) {
            if (menuRef.current && !menuRef.current.contains(e.target)) {
                setMenuOpen(false);
            }
        }
        document.addEventListener("mousedown", handleClickOutside);
        return () => document.removeEventListener("mousedown", handleClickOutside);
    }, []);

    function handleLogout() {
        setMenuOpen(false);
        logout();
        navigate("/login");
    }

    const isAdmin = user?.role === "admin";

    return (
        <nav className="navbar">
            <div className="navbar-inner">
                <Link to="/" className="navbar-brand">
                    ✈ SkyRoute
                </Link>

                <div className="navbar-links">
                    <Link to="/" className="navbar-link">
                        Home
                    </Link>

                    {loading ? null : isAuthenticated ? (
                        <>
                            <Link to="/my-bookings" className="navbar-link">
                                My Bookings
                            </Link>

                            {isAdmin && (
                                <Link to="/admin" className="navbar-link navbar-link-admin">
                                    Dashboard
                                </Link>
                            )}

                            <div className="navbar-user" ref={menuRef}>
                                <button
                                    className="navbar-user-trigger"
                                    onClick={() => setMenuOpen((open) => !open)}
                                >
                                    <span className="navbar-avatar">
                                        {user?.full_name?.charAt(0)?.toUpperCase() || "U"}
                                    </span>
                                    <span className="navbar-user-name">
                                        {user?.full_name?.split(" ")[0] || "Account"}
                                    </span>
                                </button>

                                {menuOpen && (
                                    <div className="navbar-dropdown">
                                        <div className="navbar-dropdown-header">
                                            <p className="navbar-dropdown-name">{user?.full_name}</p>
                                            <p className="navbar-dropdown-email">{user?.email}</p>
                                        </div>
                                        <button className="navbar-dropdown-item" onClick={handleLogout}>
                                            Log out
                                        </button>
                                    </div>
                                )}
                            </div>
                        </>
                    ) : (
                        <>
                            <Link to="/login" className="navbar-link">
                                Log in
                            </Link>
                            <Link to="/register" className="navbar-link navbar-link-cta">
                                Sign up
                            </Link>
                        </>
                    )}
                </div>
            </div>
        </nav>
    );
}