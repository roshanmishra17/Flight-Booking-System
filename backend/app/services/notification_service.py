import json
import logging
import urllib.request

from app.core.config import EMAIL_API_KEY, EMAIL_SENDER, EMAIL_SENDER_NAME

logger = logging.getLogger(__name__)


class NotificationService:

    @staticmethod
    def build_booking_confirmation(booking) -> dict | None:
        """Call while the DB session is open. Returns plain data only."""
        if not booking.passenger_email:
            return None

        flight = booking.flight
        origin = flight.origin_airport
        destination = flight.destination_airport

        return {
            "to": booking.passenger_email,
            "name": booking.passenger_name,
            "pnr": booking.pnr,
            "flight": f"{flight.airline} {flight.flight_number}",
            "route": f"{origin.city} ({origin.iata_code}) to {destination.city} ({destination.iata_code})",
            "departure": flight.departure_time.strftime("%d %b %Y, %I:%M %p"),
            "arrival": flight.arrival_time.strftime("%d %b %Y, %I:%M %p"),
            "seat": booking.seat.seat_number,
            "amount": f"Rs. {booking.total_price:,.0f}",
        }

    @staticmethod
    def send_booking_confirmation(data: dict) -> None:
        subject = f"Booking confirmed - PNR {data['pnr']}"
        body = (
            f"Hi {data['name']},\n\n"
            f"Your booking is confirmed.\n\n"
            f"PNR: {data['pnr']}\n"
            f"Flight: {data['flight']}\n"
            f"Route: {data['route']}\n"
            f"Departure: {data['departure']}\n"
            f"Arrival: {data['arrival']}\n"
            f"Seat: {data['seat']}\n"
            f"Amount paid: {data['amount']}\n\n"
            f"Have a great flight!\nSkyRoute"
        )
        NotificationService._send_email(data["to"], data["name"], subject, body)

    @staticmethod
    def _send_email(to_email: str, to_name: str, subject: str, text: str) -> None:
        if not (EMAIL_API_KEY and EMAIL_SENDER):
            logger.warning("Email not configured; skipping email to %s", to_email)
            return

        payload = json.dumps({
            "sender": {"name": EMAIL_SENDER_NAME, "email": EMAIL_SENDER},
            "to": [{"email": to_email, "name": to_name}],
            "subject": subject,
            "textContent": text,
        }).encode()

        request = urllib.request.Request(
            "https://api.brevo.com/v3/smtp/email",
            data=payload,
            headers={"api-key": EMAIL_API_KEY, "Content-Type": "application/json"},
            method="POST",
        )
        try:
            urllib.request.urlopen(request, timeout=10)
        except Exception:
            logger.exception("Failed to send email to %s", to_email)