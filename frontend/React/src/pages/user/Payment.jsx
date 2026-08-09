import { useState, useEffect, useRef } from "react";
import { useParams, useNavigate } from "react-router-dom";

import { getBooking } from "../../api/bookingApi";
import { createPayment } from "../../api/paymentApi";
import { formatCurrency } from "../../utils/formatTime";
import "../../CSS/Payment.css";

const LOCK_TTL_SECONDS = 300;

export default function Payment() {
    const { bookingId } = useParams();
    const navigate = useNavigate();

    const [booking, setBooking] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    const [paymentMethod, setPaymentMethod] = useState("upi");
    const [simulateFailure, setSimulateFailure] = useState(false);
    const [submitting, setSubmitting] = useState(false);
    const [paymentError, setPaymentError] = useState(null);
    const [lastFailed, setLastFailed] = useState(false);

    const [secondsLeft, setSecondsLeft] = useState(null);
    const intervalRef = useRef(null);

    function parseServerTimestamp(isoString) {
        // Server stores naive datetimes as UTC (Render's system clock).
        // Append 'Z' if not already present so JS parses it as UTC, not local time.
        const hasTimezone = /Z$|[+-]\d{2}:\d{2}$/.test(isoString);
        return new Date(hasTimezone ? isoString : `${isoString}Z`);
    }
    useEffect(() => {
        getBooking(bookingId)
            .then((b) => {
                setBooking(b);
                const bookedAt = parseServerTimestamp(b.booked_at).getTime();
                const elapsed = Math.floor((Date.now() - bookedAt) / 1000);
                setSecondsLeft(Math.max(LOCK_TTL_SECONDS - elapsed, 0));
            })
            .catch(() => setError("Couldn't load booking details."))
            .finally(() => setLoading(false));
    }, [bookingId]);

    useEffect(() => {
        if (secondsLeft === null) return;
        const interval = setInterval(() => {
            setSecondsLeft((s) => (s !== null && s > 0 ? s - 1 : 0));
        }, 1000);
        return () => clearInterval(intervalRef.current);
    }, [secondsLeft !== null]);

    async function handlePay() {
        setSubmitting(true);
        setPaymentError(null);

        try {
            const payment = await createPayment({
                booking_id: Number(bookingId),
                payment_method: paymentMethod,
                simulate_failure: simulateFailure,
            });

            if (payment.status === "success") {
                navigate(`/booking-confirmed/${bookingId}`);
            } else {
                setLastFailed(true);
                setPaymentError("Payment failed. You can retry below.");
            }
        } catch (err) {
            const detail = err.response?.data?.detail;
            if (err.response?.status === 409) {
                setPaymentError(detail || "This booking has already been paid for.");
            } else if (err.response?.status === 400) {
                setPaymentError(detail || "This booking can no longer be paid for.");
            } else {
                setPaymentError("Something went wrong. Please try again.");
            }
        } finally {
            setSubmitting(false);
        }
    }

    if (loading) return <p className="payment-status">Loading…</p>;
    if (error) return <p className="payment-status">{error}</p>;
    if (!booking) return null;

    const expired = secondsLeft === 0;
    const mins = Math.floor((secondsLeft ?? 0) / 60);
    const secs = (secondsLeft ?? 0) % 60;

    return (
        <div className="payment-page">
            <div className="payment-card">
                <div className="payment-header">
                    <h1>Payment</h1>
                    {!expired && (
                        <span className="payment-timer">
                            Hold expires in {mins}:{secs.toString().padStart(2, "0")}
                        </span>
                    )}
                </div>

                {expired && (
                    <div className="payment-expired-banner">
                        Your seat hold has expired. Please search and select a seat again.
                    </div>
                )}

                <div className="payment-summary">
                    <span>PNR {booking.pnr}</span>
                    <span className="payment-total">{formatCurrency(booking.total_price)}</span>
                </div>

                <div className="payment-field">
                    <label>Payment method</label>
                    <div className="payment-method-options">
                        {["upi", "credit_card", "debit_card"].map((method) => (
                            <button
                                key={method}
                                type="button"
                                className={`payment-method-btn ${paymentMethod === method ? "active" : ""}`}
                                onClick={() => setPaymentMethod(method)}
                                disabled={expired}
                            >
                                {method.replace("_", " ").toUpperCase()}
                            </button>
                        ))}
                    </div>
                </div>

                <label className="payment-simulate-toggle">
                    <input
                        type="checkbox"
                        checked={simulateFailure}
                        onChange={(e) => setSimulateFailure(e.target.checked)}
                        disabled={expired}
                    />
                    Simulate a failed payment (demo)
                </label>

                {paymentError && (
                    <div className="payment-error-banner">
                        {paymentError}
                    </div>
                )}

                <button
                    className="payment-submit"
                    onClick={handlePay}
                    disabled={submitting || expired}
                >
                    {submitting ? "Processing…" : lastFailed ? "Retry payment" : "Pay now"}
                </button>
            </div>
        </div>
    );
}