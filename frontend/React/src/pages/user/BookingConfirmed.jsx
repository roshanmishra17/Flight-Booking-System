import { useState, useEffect } from "react";
import { useParams, useNavigate, Link } from "react-router-dom";

import { getBooking } from "../../api/bookingApi";
import { getFlight } from "../../api/flightApi";
import { getAirports } from "../../api/airportApi";
import { formatCurrency, formatTime } from "../../utils/formatTime";
import "../../CSS/BookingConfirmed.css";

export default function BookingConfirmed() {
    const { bookingId } = useParams();
    const navigate = useNavigate();

    const [booking, setBooking] = useState(null);
    const [flight, setFlight] = useState(null);
    const [airports, setAirports] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        async function load() {
            try {
                const b = await getBooking(bookingId);
                setBooking(b);
                const [f, a] = await Promise.all([getFlight(b.flight_id), getAirports()]);
                setFlight(f);
                setAirports(a);
            } catch (err) {
                setError("Couldn't load booking details.");
            } finally {
                setLoading(false);
            }
        }
        load();
    }, [bookingId]);

    if (loading) return <p className="confirmed-status">Loading…</p>;
    if (error) return <p className="confirmed-status">{error}</p>;
    if (!booking || !flight) return null;

    if (booking.status !== "confirmed") {
        return (
            <div className="confirmed-page">
                <div className="confirmed-card">
                    <h1>This booking isn't confirmed</h1>
                    <p>Its current status is "{booking.status}".</p>
                    <button className="confirmed-cta" onClick={() => navigate("/my-bookings")}>
                        Go to My Bookings
                    </button>
                </div>
            </div>
        );
    }

    const origin = airports.find((a) => a.id === flight.origin_airport_id);
    const destination = airports.find((a) => a.id === flight.destination_airport_id);

    return (
        <div className="confirmed-page">
            <div className="confirmed-card">
                <div className="confirmed-icon">✓</div>
                <h1>Booking confirmed</h1>
                <p className="confirmed-subtext">Your seat is booked. Have a great flight!</p>

                <div className="confirmed-pnr">
                    <span>PNR</span>
                    <strong>{booking.pnr}</strong>
                </div>

                <div className="confirmed-divider" />

                <div className="confirmed-row">
                    <span>Flight</span>
                    <span>{flight.airline} · {flight.flight_number}</span>
                </div>
                <div className="confirmed-row">
                    <span>Route</span>
                    <span>
                        {origin?.iata_code ?? "—"} → {destination?.iata_code ?? "—"}
                    </span>
                </div>
                <div className="confirmed-row">
                    <span>Departure</span>
                    <span>{formatTime(flight.departure_time)}</span>
                </div>
                <div className="confirmed-row">
                    <span>Passenger</span>
                    <span>{booking.passenger_name}</span>
                </div>
                <div className="confirmed-row">
                    <span>Seat</span>
                    <span>{booking.seat.seat_number} · {booking.seat.seat_class}</span>
                </div>
                <div className="confirmed-row confirmed-total">
                    <span>Paid</span>
                    <span>{formatCurrency(booking.total_price)}</span>
                </div>

                <div className="confirmed-actions">
                    <Link to="/my-bookings" className="confirmed-cta">
                        View my bookings
                    </Link>
                    <Link to="/" className="confirmed-secondary">
                        Search more flights
                    </Link>
                </div>
            </div>
        </div>
    );
}