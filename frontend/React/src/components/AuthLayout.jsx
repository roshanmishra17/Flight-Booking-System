import "../CSS/AuthLayout.css";

export default function AuthLayout({ heading, subheading, children }) {
    return (
        <div className="auth-layout">
            <aside className="auth-aside">
                <div className="auth-aside-inner">
                    <p className="auth-aside-brand">✈ SkyRoute</p>
                    <h2 className="auth-aside-heading">{heading}</h2>
                    <p className="auth-aside-sub">{subheading}</p>

                    <div className="auth-route-card">
                        <div className="auth-route-top">
                            <span className="auth-route-tag">Example result</span>
                            <span className="auth-route-badge">#1 Recommended</span>
                        </div>

                        <div className="auth-route-row">
                            <div className="auth-route-city">
                                <strong>BOM</strong>
                                <small>Mumbai</small>
                            </div>

                            <svg className="auth-route-path" viewBox="0 0 160 44">
                                <path
                                    d="M6 34 Q80 -12 154 34"
                                    fill="none"
                                    stroke="#e8a33d"
                                    strokeWidth="1.5"
                                    strokeDasharray="4 5"
                                />
                                <circle cx="6" cy="34" r="3.5" fill="#e8a33d" />
                                <circle cx="154" cy="34" r="3.5" fill="#e8a33d" />
                                <text x="80" y="9" textAnchor="middle" fontSize="13" fill="#f5f3ee">
                                    ✈
                                </text>
                            </svg>

                            <div className="auth-route-city">
                                <strong>DEL</strong>
                                <small>New Delhi</small>
                            </div>
                        </div>

                        <div className="auth-route-bottom">
                            <span>Direct · 2h 10m</span>
                            <span className="auth-route-price">₹5,500</span>
                        </div>
                    </div>

                    <ul className="auth-features">
                        <li>
                            <span className="auth-feature-icon">📈</span>
                            <div>
                                <strong>Live dynamic pricing</strong>
                                <p>Fares adjust with seat demand and how close you book to departure.</p>
                            </div>
                        </li>
                        <li>
                            <span className="auth-feature-icon">🧭</span>
                            <div>
                                <strong>Ranked your way</strong>
                                <p>Sort by cheapest, fastest or a balanced mix, scored for every search.</p>
                            </div>
                        </li>
                        <li>
                            <span className="auth-feature-icon">🔒</span>
                            <div>
                                <strong>No double bookings</strong>
                                <p>A seat is held for you while you pay, so nobody can grab it from under you.</p>
                            </div>
                        </li>
                    </ul>
                </div>
            </aside>

            <div className="auth-main">
                <div className="login-glow" />
                {children}
            </div>
        </div>
    );
}