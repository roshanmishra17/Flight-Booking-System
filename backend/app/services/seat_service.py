from sqlalchemy.orm import Session

from app.layout.aircraft_layout import AIRCRAFT_LAYOUTS
from app.models.flights import Flight
from app.repositories.seat_repository import SeatRepository
from app.services.seat_generator import SeatGenerator
from app.core.exceptions import FlightNotFoundError, FlightSeatsNotFoundError, UnsupportedAircraftTypeError
from app.schemas.seats import SeatAvailability, SeatResponse
from app.repositories.flight_repository import FlightRepository


class SeatService:

    @staticmethod
    def generate_for_flight(
        db: Session,
        flight: Flight,
    ) -> None:

        layout = AIRCRAFT_LAYOUTS.get(
            flight.aircraft_type
        )

        if layout is None:
            raise UnsupportedAircraftTypeError(
                flight.aircraft_type
            )

        seats = SeatGenerator.generate(
            flight,
            layout,
        )

        SeatRepository.bulk_create(
            db,
            seats,
        )

    @staticmethod
    def get_seats_by_flight(
        db: Session,
        flight_id: int,
    ) -> list[SeatResponse]:

        flight = FlightRepository.get_by_id(
            db,
            flight_id,
        )

        if not flight:
            raise FlightNotFoundError(
                "Flight not found."
            )

        seats = SeatRepository.get_by_flight(
            db,
            flight_id,
        )

        if not seats:
            raise FlightSeatsNotFoundError(
                "No seats found for this flight."
            )

        return [
            SeatResponse(
                id=seat.id,
                seat_number=seat.seat_number,
                seat_class=seat.seat_class,
                seat_position=seat.seat_position,
                price_multiplier=seat.price_multiplier,
                availability=SeatAvailability.AVAILABLE,
            )
            for seat in seats
        ]