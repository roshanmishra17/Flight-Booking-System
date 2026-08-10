import { useState, useEffect } from "react";
import { Link } from "react-router-dom";

import { getMyBookings, cancelBooking } from "../../api/bookingApi";
import { getFlights} from "../../api/flightApi";
import { getAirports } from "../../api/airportApi";
import { formatCurrency, formatTime } from "../../utils/formatTime";
import "../../CSS/MyBookings.css";

const CANCELLABLE = ["pending", "confirmed"];

export default function MyBookings() {
    const [bookings, setBookings] = useState([]);
    const [flights, setFlights] = useState([]);
    const [airports, setAirports] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [cancellingId, setCancellingId] = useState(null);
    const [confirmingId, setConfirmingId] = useState(null);

    useEffect(() => {
        loadAll();
    }, []);

    function loadAll() {
        setLoading(true);
        setError(null);
        Promise.all([getMyBookings(), getFlights(), getAirports()])
            .then(([b, f, a]) => {
                setBookings(b);
                setFlights(f);
                setAirports(a);
            })
            .catch(() => setError("Couldn't load your bookings."))
            .finally(() => setLoading(false));
    }

    async function handleCancel(bookingId) {
        setCancellingId(bookingId);
        try {
            await cancelBooking(bookingId);
            await loadAll();
        } catch (err) {
            setError(err.response?.data?.detail || "Couldn't cancel this booking.");
        } finally {
            setCancellingId(null);
            setConfirmingId(null);
        }
    }

    if (loading) return <p className="mybookings-status">Loading…</p>;
    if (error && bookings.length === 0) return <p className="mybookings-status">{error}</p>;

    return (
        <div className="mybookings-page">
            <h1>My Bookings</h1>

            {error && <div className="mybookings-error-banner">{error}</div>}

            {bookings.length === 0 && (
                <div className="mybookings-empty">
                    <p>You haven't booked any flights yet.</p>
                    <Link to="/" className="mybookings-empty-cta">Search flights</Link>
                </div>
            )}

            <div className="mybookings-list">
                {bookings.map((booking) => {
                    const flight = flights.find((f) => f.id === booking.flight_id);
                    const origin = flight && airports.find((a) => a.id === flight.origin_airport_id);
                    const destination = flight && airports.find((a) => a.id === flight.destination_airport_id);
                    const canCancel = CANCELLABLE.includes(booking.status);

                    return (
                        <div className="booking-item" key={booking.id}>
                            <div className="booking-item-main">
                                <div className="booking-item-route">
                                    <span className="booking-item-airports">
                                        {origin?.iata_code ?? "—"} <span className="booking-item-arrow">→</span> {destination?.iata_code ?? "—"}
                                    </span>
                                    <span className={`booking-item-status status-${booking.status}`}>
                                        {booking.status}
                                    </span>
                                </div>

                                {flight && (
                                    <p className="booking-item-times">
                                        {flight.flight_number} · {formatTime(flight.departure_time)} → {formatTime(flight.arrival_time)}
                                    </p>
                                )}

                                <div className="booking-item-details">
                                    <span>PNR {booking.pnr}</span>
                                    <span>Seat {booking.seat.seat_number}</span>
                                    <span>{booking.passenger_name}</span>
                                    <span className="booking-item-price">{formatCurrency(booking.total_price)}</span>
                                </div>
                            </div>

                            <div className="booking-item-actions">
                                {booking.status === "confirmed" && (
                                    <Link to={`/booking-confirmed/${booking.id}`} className="booking-view-ticket">
                                        View Ticket
                                    </Link>
                                )}

                                {canCancel && (
                                    confirmingId === booking.id ? (
                                        <div className="booking-cancel-confirm">
                                            <span>Cancel this booking?</span>
                                            <button
                                                className="booking-cancel-yes"
                                                disabled={cancellingId === booking.id}
                                                onClick={() => handleCancel(booking.id)}
                                            >
                                                {cancellingId === booking.id ? "Cancelling…" : "Yes, cancel"}
                                            </button>
                                            <button className="booking-cancel-no" onClick={() => setConfirmingId(null)}>
                                                Keep it
                                            </button>
                                        </div>
                                    ) : (
                                        <button className="booking-cancel-trigger" onClick={() => setConfirmingId(booking.id)}>
                                            Cancel Booking
                                        </button>
                                    )
                                )}
                            </div>
                        </div>
                    );
                })}
            </div>
        </div>
    );
}