from sqlalchemy.orm import Session

from app.layout.aircraft_layout import AIRCRAFT_LAYOUTS
from app.models.flights import Flight
from app.repositories.seat_repository import SeatRepository
from app.services.seat_generator import SeatGenerator
from app.core.exceptions import UnsupportedAircraftTypeError


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