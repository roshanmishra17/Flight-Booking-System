import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";

import { getBooking } from "../../api/bookingApi";
import { getFlight } from "../../api/flightApi";
import { getAirports } from "../../api/airportApi";

import { formatCurrency, formatTime } from "../../utils/formatTime";

import "../../CSS/BookingSummary.css";

export default function BookingSummary() {
    const { bookingId } = useParams();
    const navigate = useNavigate();

    const [booking, setBooking] = useState(null);
    const [flight, setFlight] = useState(null);
    const [airports, setAirports] = useState([]);

    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        async function loadBookingSummary() {
            try {
                setLoading(true);
                setError(null);

                const bookingData = await getBooking(bookingId);

                setBooking(bookingData);

                const [flightData, airportData] = await Promise.all([
                    getFlight(bookingData.flight_id),
                    getAirports(),
                ]);

                setFlight(flightData);
                setAirports(airportData);
            } catch (err) {
                console.error("Failed to load booking summary:", err);

                setError(
                    err.response?.data?.detail ||
                    "Couldn't load booking details."
                );
            } finally {
                setLoading(false);
            }
        }

        loadBookingSummary();
    }, [bookingId]);

    if (loading) {
        return (
            <div className="summary-page">
                <div className="summary-status">
                    Loading booking details...
                </div>
            </div>
        );
    }

    if (error) {
        return (
            <div className="summary-page">
                <div className="summary-status summary-error">
                    {error}
                </div>
            </div>
        );
    }

    if (!booking || !flight) {
        return null;
    }

    const origin = airports.find(
        (airport) =>
            airport.id === flight.origin_airport_id
    );

    const destination = airports.find(
        (airport) =>
            airport.id === flight.destination_airport_id
    );

    const formatClass = (value) =>
        value
            ?.replace("_", " ")
            .replace(/\b\w/g, (char) => char.toUpperCase());

    const formatStatus = (value) =>
        value
            ?.replace("_", " ")
            .replace(/\b\w/g, (char) => char.toUpperCase());

    return (
        <div className="summary-page">

            <div className="summary-card">

                {/* Header */}
                <div className="summary-header">
                    <div>
                        <p className="summary-eyebrow">
                            Booking Summary
                        </p>

                        <h1>
                            {flight.airline}
                        </h1>

                        <p className="summary-flight-number">
                            {flight.flight_number}
                        </p>
                    </div>

                    <div className="summary-pnr">
                        <span>PNR</span>
                        <strong>{booking.pnr}</strong>
                    </div>
                </div>


                {/* Flight Information */}
                <div className="summary-flight">

                    <div className="summary-airport">

                        <strong>
                            {origin?.iata_code ||
                                flight.origin_airport_id}
                        </strong>

                        <span>
                            {origin?.name || "Origin"}
                        </span>

                        <small>
                            {formatTime(
                                flight.departure_time
                            )}
                        </small>

                    </div>


                    <div className="summary-route-line">
                        <span className="summary-duration">{flight.duration_minutes} min</span>
                        <div className="summary-line" />
                        <span className="summary-stops">
                            {flight.stops === 0 ? "Non-stop" : `${flight.stops} stop${flight.stops > 1 ? "s" : ""}`}
                        </span>
                    </div>


                    <div className="summary-airport">
                        <strong>
                            {destination?.iata_code ||
                                flight.destination_airport_id}
                        </strong>
                        <span>
                            {destination?.name || "Destination"}
                        </span>
                        <small>
                            {formatTime(
                                flight.arrival_time
                            )}
                        </small>
                    </div>
                </div>

                <div className="summary-divider" />

                {/* Passenger Information */}
                <div className="summary-section">
                    <h2>
                        Passenger Details
                    </h2>
                    <div className="summary-details">
                        <div className="summary-detail">
                            <span>Passenger</span>
                            <strong>
                                {booking.passenger_name}
                            </strong>
                        </div>
                        <div className="summary-detail">
                            <span>Seat</span>
                            <strong>
                                {booking.seat.seat_number}
                            </strong>
                        </div>

                        <div className="summary-detail">
                            <span>Position</span>
                            <strong>
                                {formatClass(
                                    booking.seat.seat_position
                                )}
                            </strong>
                        </div>

                        <div className="summary-detail">
                            <span>Class</span>
                            <strong>
                                {formatClass(
                                    booking.seat.seat_class
                                )}
                            </strong>
                        </div>
                    </div>
                </div>

                <div className="summary-divider" />

                {/* Price */}
                <div className="summary-price">
                    <div className="summary-price-row">
                        <span>Booking total</span>
                        <strong>
                            {formatCurrency(
                                booking.total_price
                            )}
                        </strong>
                    </div>

                    <div className="summary-total">
                        <span>Total to pay</span>
                        <strong>
                            {formatCurrency(
                                booking.total_price
                            )}
                        </strong>
                    </div>
                </div>

                {/* Continue */}
                <button
                    className="summary-continue"
                    onClick={() =>
                        navigate(
                            `/payment/${booking.id}`
                        )
                    }
                >
                    Continue to Payment
                </button>
            </div>
        </div>
    );
}