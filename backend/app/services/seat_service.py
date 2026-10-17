from sqlalchemy.orm import Session

from app.layout.aircraft_layout import AIRCRAFT_LAYOUTS
from app.models.flights import Flight
from app.repositories.seat_repository import SeatRepository
from app.services.seat_generator import SeatGenerator
from app.core.exceptions import FlightNotFoundError, FlightSeatsNotFoundError, UnsupportedAircraftTypeError
from app.schemas.seats import SeatAvailability, SeatResponse
from app.repositories.flight_repository import FlightRepository
from app.repositories.booking_repository import BookingRepository
from app.services.seat_lock_service import SeatLockService


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

        from sqlalchemy.orm import Session

from app.layout.aircraft_layout import AIRCRAFT_LAYOUTS
from app.models.flights import Flight
from app.repositories.seat_repository import SeatRepository
from app.services.seat_generator import SeatGenerator
from app.core.exceptions import FlightNotFoundError, FlightSeatsNotFoundError, UnsupportedAircraftTypeError
from app.schemas.seats import SeatAvailability, SeatResponse
from app.repositories.flight_repository import FlightRepository
from app.repositories.booking_repository import BookingRepository
from app.services.seat_lock_service import SeatLockService
from backend.app.models import seats


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

        from sqlalchemy.orm import Session

from app.layout.aircraft_layout import AIRCRAFT_LAYOUTS
from app.models.flights import Flight
from app.repositories.seat_repository import SeatRepository
from app.services.seat_generator import SeatGenerator
from app.core.exceptions import FlightNotFoundError, FlightSeatsNotFoundError, UnsupportedAircraftTypeError
from app.schemas.seats import SeatAvailability, SeatResponse
from app.repositories.flight_repository import FlightRepository
from app.repositories.booking_repository import BookingRepository
from app.services.seat_lock_service import SeatLockService
from backend.app.models import seats


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
        
        booked_ids = BookingRepository.get_confirmed_seat_ids_for_flight(db, flight_id)
        locked_ids = SeatLockService.get_locked_seat_ids(flight_id, [s.id for s in seats])


        def availability_for(seat_id: int) -> SeatAvailability:
            if seat_id in booked_ids:
                return SeatAvailability.BOOKED
            if seat_id in locked_ids:
                return SeatAvailability.RESERVED
            return SeatAvailability.AVAILABLE

        return [
            SeatResponse(
                id=seat.id,
                seat_number=seat.seat_number,
                seat_class=seat.seat_class,
                seat_position=seat.seat_position,
                price_multiplier=seat.price_multiplier,
                availability=availability_for(seat.id),
            )
            for seat in seats
        ]

