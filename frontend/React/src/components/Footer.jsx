import { Link } from "react-router-dom";
import "../CSS/Footer.css";

export default function Footer() {
    return (
        <footer className="footer">
            <div className="footer-inner">
                <div className="footer-brand">
                    <p className="footer-logo">SkyRoute</p>
                    <p className="footer-tagline">Domestic flights, smarter search.</p>
                </div>

                <div className="footer-links">
                    <div className="footer-column">
                        <p className="footer-heading">Product</p>
                        <Link to="/">Search flights</Link>
                        <Link to="/my-bookings">My bookings</Link>
                    </div>

                    <div className="footer-column">
                        <p className="footer-heading">Project</p>
                        <a href="https://github.com/YOUR_USERNAME/skyroute" target="_blank" rel="noreferrer">
                            GitHub
                        </a>
                        <a href="/docs" target="_blank" rel="noreferrer">
                            API docs
                        </a>
                    </div>
                </div>
            </div>

            <div className="footer-bottom">
                <span>© {new Date().getFullYear()} SkyRoute — built as a portfolio project.</span>
            </div>
        </footer>
    );
}