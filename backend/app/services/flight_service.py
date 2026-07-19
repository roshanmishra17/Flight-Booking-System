from datetime import date

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.exceptions import (
    AirportNotFoundError,
    FlightAlreadyExistsError,
    FlightNotFoundError,
    InvalidFlightRouteError,
    InvalidFlightScheduleError,
)
from app.models.flights import Flight
from app.repositories.airport_repository import AirportRepository
from app.repositories.flight_repository import FlightRepository
from app.schemas.flights import FlightCreate
@staticmethod
def create_flight(
    db: Session,
    flight_data: FlightCreate,
) -> Flight:

    origin = AirportRepository.get_by_id(
        db,
        flight_data.origin_airport_id,
    )

    if not origin:
        raise AirportNotFoundError(
            "Origin airport not found."
        )

    destination = AirportRepository.get_by_id(
        db,
        flight_data.destination_airport_id,
    )

    if not destination:
        raise AirportNotFoundError(
            "Destination airport not found."
        )

    if (
        flight_data.origin_airport_id
        == flight_data.destination_airport_id
    ):
        raise InvalidFlightRouteError(
            "Origin and destination airports must be different."
        )

    if (flight_data.arrival_time <= flight_data.departure_time):
        raise InvalidFlightScheduleError(
            "Arrival time must be after departure time."
        )

    existing = FlightRepository.get_by_flight_number_and_departure(
        db,
        flight_data.flight_number,
        flight_data.departure_time,
    )

    if existing:
        raise FlightAlreadyExistsError(
            "Flight already exists."
        )

    duration_minutes = int((flight_data.arrival_time - flight_data.departure_time).total_seconds()/ 60)

    flight = Flight(
        flight_number=flight_data.flight_number,
        airline=flight_data.airline,
        origin_airport_id=flight_data.origin_airport_id,
        destination_airport_id=flight_data.destination_airport_id,
        departure_time=flight_data.departure_time,
        arrival_time=flight_data.arrival_time,
        duration_minutes=duration_minutes,
        base_price=flight_data.base_price,
        aircraft_type=flight_data.aircraft_type,
        stops=flight_data.stops,
    )

    try:
        return FlightRepository.create(
            db,
            flight,
        )

    except IntegrityError:
        raise FlightAlreadyExistsError(
            "Flight already exists."
        )
@staticmethod
def get_flight(
    db: Session,
    flight_id: int,
) -> Flight:

    flight = FlightRepository.get_by_id(
        db,
        flight_id,
    )

    if not flight:
        raise FlightNotFoundError(
            "Flight not found."
        )

    return flight

@staticmethod
def get_flights(
    db: Session,
) -> list[Flight]:

    return FlightRepository.get_all(db)

@staticmethod
def search_flights(
    db: Session,
    origin_iata: str,
    destination_iata: str,
    departure_date: date,
) -> list[Flight]:

    origin = AirportRepository.get_by_iata_code(
        db,
        origin_iata,
    )

    if not origin:
        raise AirportNotFoundError(
            "Origin airport not found."
        )

    destination = AirportRepository.get_by_iata_code(
        db,
        destination_iata,
    )

    if not destination:
        raise AirportNotFoundError(
            "Destination airport not found."
        )

    return FlightRepository.search_flights(
        db,
        origin.id,
        destination.id,
        departure_date,
    )