from datetime import date

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.exceptions import (
    AirportNotFoundError,
    FlightAlreadyExistsError,
    FlightInUseError,
    FlightNotFoundError,
    InvalidFlightRouteError,
    InvalidFlightScheduleError,
)
from app.models.flights import Flight
from app.repositories.airport_repository import AirportRepository
from app.repositories.flight_repository import FlightRepository
from app.schemas.flights import FlightCreate, FlightUpdate
class FlightService:
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
        
        origin = origin_iata.upper()
        destination = destination_iata.upper()

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

    @staticmethod
    def update_flight(
        db: Session,
        flight_id: int,
        updates: FlightUpdate,
    ) -> Flight:

        flight = FlightRepository.get_by_id(
            db,
            flight_id,
        )

        if not flight:
            raise FlightNotFoundError(
                "Flight not found."
            )

        origin_airport_id = (
            updates.origin_airport_id
            if updates.origin_airport_id is not None
            else flight.origin_airport_id
        )

        destination_airport_id = (
            updates.destination_airport_id
            if updates.destination_airport_id is not None
            else flight.destination_airport_id
        )

        departure_time = (
            updates.departure_time
            if updates.departure_time is not None
            else flight.departure_time
        )

        arrival_time = (
            updates.arrival_time
            if updates.arrival_time is not None
            else flight.arrival_time
        )

        if (
            not AirportRepository.get_by_id(
                db,
                origin_airport_id,
            )
        ):
            raise AirportNotFoundError(
                "Origin airport not found."
            )

        if (
            not AirportRepository.get_by_id(
                db,
                destination_airport_id,
            )
        ):
            raise AirportNotFoundError(
                "Destination airport not found."
            )

        if origin_airport_id == destination_airport_id:
            raise InvalidFlightRouteError(
                "Origin and destination airports must be different."
            )

        if arrival_time <= departure_time:
            raise InvalidFlightScheduleError(
                "Arrival time must be after departure time."
            )

        flight_number = (
            updates.flight_number
            if updates.flight_number is not None
            else flight.flight_number
        )

        existing = FlightRepository.get_by_flight_number_and_departure(
            db,
            flight_number,
            departure_time,
        )

        if existing and existing.id != flight.id:
            raise FlightAlreadyExistsError(
                "Flight already exists."
            )

        flight.flight_number = flight_number
        flight.airline = (
            updates.airline
            if updates.airline is not None
            else flight.airline
        )
        flight.origin_airport_id = origin_airport_id
        flight.destination_airport_id = destination_airport_id
        flight.departure_time = departure_time
        flight.arrival_time = arrival_time
        flight.duration_minutes = int(
            (arrival_time - departure_time).total_seconds() / 60
        )
        flight.base_price = (
            updates.base_price
            if updates.base_price is not None
            else flight.base_price
        )
        flight.aircraft_type = (
            updates.aircraft_type
            if updates.aircraft_type is not None
            else flight.aircraft_type
        )
        flight.stops = (
            updates.stops
            if updates.stops is not None
            else flight.stops
        )

        try:
            return FlightRepository.update(
                db,
                flight,
            )

        except IntegrityError:
            raise FlightAlreadyExistsError(
                "Flight already exists."
            )
        
    @staticmethod
    def delete_flight(
        db: Session,
        flight_id: int,
    ) -> None:

        flight = FlightRepository.get_by_id(
            db,
            flight_id,
        )

        if not flight:
            raise FlightNotFoundError(
                "Flight not found."
            )

        try:
            FlightRepository.delete(
                db,
                flight,
            )

        except IntegrityError:
            raise FlightInUseError(
                "Flight cannot be deleted because it has associated records."
            )