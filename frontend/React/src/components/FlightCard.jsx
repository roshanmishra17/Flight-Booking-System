import { useNavigate } from "react-router-dom";
import { formatTime, formatDuration, formatCurrency } from "../utils/formatTime";
import "../CSS/FlightCard.css";

export default function FlightCard({ flight, badge }) {
    const navigate = useNavigate();
    const priceChanged = Number(flight.current_price) !== Number(flight.base_price);

    return (
        <div className="flight-card">
            <div className="flight-card-main">
                <div className="flight-card-airline">
                    <p className="flight-card-flight-number">{flight.flight_number}</p>
                    <p className="flight-card-airline-name">{flight.airline}</p>
                </div>

                <div className="flight-card-route">
                    <div className="flight-card-time">
                        <span>{formatTime(flight.departure_time)}</span>
                    </div>
                    <div className="flight-card-line">
                        <span className="flight-card-duration">
                            {formatDuration(flight.duration_minutes)}
                        </span>
                        <div className="flight-card-line-bar" />
                        <span className="flight-card-stops">
                            {flight.stops === 0 ? "Direct" : `${flight.stops} stop${flight.stops > 1 ? "s" : ""}`}
                        </span>
                    </div>
                    <div className="flight-card-time">
                        <span>{formatTime(flight.arrival_time)}</span>
                    </div>
                </div>

                {badge && <div className="flight-card-badge">{badge}</div>}
            </div>

            <div className="flight-card-price-col">
                {priceChanged && (
                    <span className="flight-card-base-price">{formatCurrency(flight.base_price)}</span>
                )}
                <span className="flight-card-current-price">
                    {formatCurrency(flight.current_price ?? flight.base_price)}
                </span>
                <button
                    className="flight-card-book"
                    onClick={() => navigate(`/seat-selection/${flight.id}`)}
                >
                    Book
                </button>
            </div>
        </div>
    );
}