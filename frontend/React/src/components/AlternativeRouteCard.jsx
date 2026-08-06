import { useNavigate } from "react-router-dom";
import { formatTime, formatDuration, formatCurrency } from "../utils/formatTime";
import "../CSS/AlternativeRouteCard.css";

export default function AlternativeRouteCard({ route }) {
    const navigate = useNavigate();

    return (
        <div className="alt-route-card">
            <div className="alt-route-legs">
                <Leg flight={route.first_leg} onBook={() => navigate(`/seat-selection/${route.first_leg.id}`)} />
                <div className="alt-route-layover">Layover: {route.layover_minutes} min</div>
                <Leg flight={route.second_leg} onBook={() => navigate(`/seat-selection/${route.second_leg.id}`)} />
            </div>
            <div className="alt-route-summary">
                <span>Total duration: {formatDuration(route.total_duration)}</span>
                <span className="alt-route-price">Est. {formatCurrency(route.estimated_total_price)}</span>
            </div>
        </div>
    );
}

function Leg({ flight, onBook }) {
    return (
        <div className="alt-route-leg">
            <div className="alt-route-leg-info">
                <span className="alt-route-leg-number">{flight.flight_number}</span>
                <span>{formatTime(flight.departure_time)} → {formatTime(flight.arrival_time)}</span>
                <span className="alt-route-leg-price">{formatCurrency(flight.current_price ?? flight.base_price)}</span>
            </div>
            <button className="alt-route-leg-book" onClick={onBook}>
                Book
            </button>
        </div>
    );
}