from datetime import date

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.exceptions import (
    AirportNotFoundError,
    FlightAlreadyExistsError,
    FlightInUseError,
    FlightNotFoundError,
    InvalidFlightPriceError,
    InvalidFlightRouteError,
    InvalidFlightScheduleError,
)
from app.models.flights import Flight
from app.repositories.airport_repository import AirportRepository
from app.repositories.flight_repository import FlightRepository
from app.schemas.flights import FlightCreate, FlightUpdate
from app.services.seat_service import SeatService
from app.models.recommendation_weights import RecommendationMode
from app.models.search import Search
from app.models.seats import SeatClass
from app.models.users import User
from app.services.recommendation_service import RecommendationService
from app.utils.recommendation_scoring import RecommendationResult
from app.repositories.booking_repository import BookingRepository
from app.services.pricing_service import PricingService
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

        if duration_minutes < 15:
            raise InvalidFlightScheduleError(
                "Flight duration must be at least 15 minutes."
            )

        if flight_data.base_price <= 0:
            raise InvalidFlightPriceError(
                "Flight base price must be greater than 0."
            )

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
            FlightRepository.create(
                db,
                flight,
            )
            db.flush()

            SeatService.generate_for_flight(
                db,
                flight,
            )

            db.commit()

            db.refresh(flight)

            return flight

        except IntegrityError:
            db.rollback()
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
        
        origin_iata = origin_iata.upper()
        destination_iata = destination_iata.upper()

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
        if origin.id == destination.id:
            raise InvalidFlightRouteError(
                "Origin and destination airports must be different."
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

        base_price = (
            updates.base_price
            if updates.base_price is not None
            else flight.base_price
        )

        if base_price <= 0:
            raise InvalidFlightPriceError(
                "Flight base price must be greater than 0."
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
        duration_minutes = int((arrival_time - departure_time).total_seconds() / 60)

        if duration_minutes < 15:
            raise InvalidFlightScheduleError(
                "Flight duration must be at least 15 minutes."
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
        flight.duration_minutes = duration_minutes
        flight.base_price = base_price
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
            db.rollback()
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

    @staticmethod
    def search_flights_ranked(
        db: Session,
        current_user: User,
        origin_iata: str,
        destination_iata: str,
        departure_date: date,
        travel_class: SeatClass,
        mode: RecommendationMode,
    ) -> list[RecommendationResult]:

        origin_iata = origin_iata.upper()
        destination_iata = destination_iata.upper()

        origin = AirportRepository.get_by_iata_code(db, origin_iata)
        if not origin:
            raise AirportNotFoundError("Origin airport not found.")

        destination = AirportRepository.get_by_iata_code(db, destination_iata)
        if not destination:
            raise AirportNotFoundError("Destination airport not found.")

        if origin.id == destination.id:
            raise InvalidFlightRouteError("Origin and destination airports must be different.")

        search = Search(
            user_id=current_user.id,
            origin_airport_id=origin.id,
            destination_airport_id=destination.id,
            travel_date=departure_date,
            travel_class=travel_class,
            mode=mode,
        )

        try:
            db.add(search)
            db.flush()

            flights = FlightRepository.search_flights(
                db=db,
                origin_airport_id=origin.id,
                destination_airport_id=destination.id,
                departure_date=departure_date,
            )
            if not flights:
                db.commit()
                return []

            flight_ids = [flight.id for flight in flights]

            occupancy_data = BookingRepository.get_occupancy_data(
                db=db,
                flight_ids=flight_ids,
            )

            # Compute dynamic price for each flight
            for flight in flights:

                booked_seats, total_seats = occupancy_data.get(
                    flight.id,
                    (0, 0),
                )

                occupancy = PricingService.calculate_occupancy(
                    total_seats=total_seats,
                    booked_seats=booked_seats,
                )

                current_price = PricingService.calculate_current_price(
                    base_price=flight.base_price,
                    occupancy=occupancy,
                    departure_time=flight.departure_time,
                )            
                occupancy_adjustment = PricingService.get_occupancy_adjustment(
                    occupancy,
                )

                days_adjustment = PricingService.get_days_adjustment(
                    flight.departure_time,
                )
                print(
                    f"""
                Flight: {flight.flight_number}
                Booked Seats: {booked_seats}
                Total Seats: {total_seats}
                Occupancy: {occupancy}
                Occupancy Adjustment: {occupancy_adjustment}
                Days Adjustment: {days_adjustment}
                Current Price: {current_price}
                """
                )

                # Temporary attribute (not stored in DB)
                flight.current_price = current_price
            ranked_results = RecommendationService.rank_flights(db=db, search=search, flights=flights)

            db.commit()
            return ranked_results

        except Exception:
            db.rollback()
            raise