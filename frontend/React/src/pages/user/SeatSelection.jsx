import { useState, useEffect } from "react";
import { useParams, useNavigate } from "react-router-dom";

import { getSeatMap } from "../../api/seatApi";
import { createBooking } from "../../api/bookingApi";
import SeatMap from "../../components/SeatMap";
import { formatCurrency } from "../../utils/formatTime";
import "../../CSS/SeatSelection.css";

export default function SeatSelection() {
    const { flightId } = useParams();
    const navigate = useNavigate();

    const [seats, setSeats] = useState([]);
    const [selectedSeat, setSelectedSeat] = useState(null);
    const [passengerName, setPassengerName] = useState("");
    const [loading, setLoading] = useState(true);
    const [booking, setBooking] = useState(false);
    const [error, setError] = useState(null);


    const [age, setAge] = useState("");
    const [phone, setPhone] = useState("");
    const [email, setEmail] = useState("");

    function validate() {
        if (!selectedSeat) return "Please select a seat.";
        if (!passengerName.trim()) return "Enter the passenger name.";
        const a = Number(age);
        if (!Number.isInteger(a) || a < 1 || a > 120) return "Enter a valid age.";
        if (!/^(?:\+91|91|0)?[6-9]\d{9}$/.test(phone.replace(/[\s-]/g, "")))
            return "Enter a valid 10-digit mobile number.";
        if (!/^\S+@\S+\.\S+$/.test(email.trim())) return "Enter a valid email address.";
        return null;
    }

    const validationError = validate();
    if (validationError) {
        setError(validationError);
        return;
    }

    useEffect(() => {
        getSeatMap(flightId)
            .then(setSeats)
            .catch(() => setError("Couldn't load the seat map."))
            .finally(() => setLoading(false));
    }, [flightId]);

    function handleSelect(seat) {
        if (seat.availability === "booked") return;
        setSelectedSeat(seat.id === selectedSeat?.id ? null : seat);
        setError(null);
    }

    async function handleConfirm() {
        if (!selectedSeat || !passengerName.trim()) {
            setError("Please select a seat and enter the passenger name.");
            return;
        }

        setBooking(true);
        setError(null);
        try {
            const result = await createBooking({
                flight_id: Number(flightId),
                seat_id: selectedSeat.id,
                passenger_name: passengerName.trim(),
                passenger_age: Number(age),
                passenger_phone: phone,
                passenger_email: email.trim(),
            });
            navigate(`/booking-summary/${result.id}`);
        } catch (err) {
            if (err.response?.status === 409) {
                setError(
                    err.response.data?.detail ||
                        "This seat was just taken by someone else. Please pick another."
                );
                // refresh seat map so the taken seat shows as booked
                setSelectedSeat(null);
                getSeatMap(flightId).then(setSeats).catch(() => {});
            } else {
                setError("Something went wrong. Please try again.");
            }
        } finally {
            setBooking(false);
        }
    }

    if (loading) return <p className="seat-selection-status">Loading seat map…</p>;
    if (error && seats.length === 0) return <p className="seat-selection-status">{error}</p>;

    return (
        <div className="seat-selection-page">
            <div className="seat-selection-layout">
                <SeatMap seats={seats} selectedSeatId={selectedSeat?.id} onSelect={handleSelect} />

                <div className="seat-selection-sidebar">
                    <h2>Your selection</h2>

                    {selectedSeat ? (
                        <div className="seat-selection-summary">
                            <p className="seat-selection-seat-number">{selectedSeat.seat_number}</p>
                            <p className="seat-selection-seat-class">{selectedSeat.seat_class}</p>
                        </div>
                    ) : (
                        <p className="seat-selection-empty">No seat selected yet</p>
                    )}

                    <div className="seat-selection-field">
                        <label>Passenger name</label>
                        <input
                            type="text"
                            value={passengerName}
                            onChange={(e) => setPassengerName(e.target.value)}
                            placeholder="As per ID"
                        />
                    </div>
                    <div className="seat-selection-field">
                        <label>Age</label>
                        <input type="number" min="1" max="120" value={age}
                            onChange={(e) => setAge(e.target.value)} placeholder="e.g. 24" />
                    </div>
                    <div className="seat-selection-field">
                        <label>Mobile number</label>
                        <input type="tel" value={phone}
                            onChange={(e) => setPhone(e.target.value)} placeholder="10-digit mobile" />
                    </div>
                    <div className="seat-selection-field">
                        <label>Email</label>
                        <input type="email" value={email}
                            onChange={(e) => setEmail(e.target.value)} placeholder="Ticket will be sent here" />
                    </div>
                    {error && <p className="seat-selection-error">{error}</p>}

                    <button
                        className="seat-selection-confirm"
                        disabled={!selectedSeat || booking}
                        onClick={handleConfirm}
                    >
                        {booking ? "Booking…" : "Continue to payment"}
                    </button>
                </div>
            </div>
        </div>
    );
}