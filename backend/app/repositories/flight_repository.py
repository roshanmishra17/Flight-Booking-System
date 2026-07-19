from datetime import date, datetime, time

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from app.models.flights import Flight
class FlightRepository:
    @staticmethod
    def get_by_id(db: Session, flight_id: int) -> Flight | None:
        return (
            db.query(Flight).filter(Flight.id == flight_id).first()
        )
    
    @staticmethod
    def get_all(db: Session) -> list[Flight]:
        return (
            db.query(Flight).order_by(Flight.departure_time).all()
        )
    
    @staticmethod
    def get_by_flight_number_and_departure(
        db: Session,
        flight_number: str,
        departure_time: datetime,
    ) -> Flight | None:
        return (
            db.query(Flight)
            .filter(
                Flight.flight_number == flight_number,
                Flight.departure_time == departure_time,
            ).first()
        )
    @staticmethod
    def get_by_flight_number(
        db: Session,
        flight_number: str,
    ) -> list[Flight]:
        return (
            db.query(Flight)
            .filter(Flight.flight_number == flight_number)
            .order_by(Flight.departure_time)
            .all()
        )
    @staticmethod
    def create(
        db: Session,
        flight: Flight,
    ) -> Flight:
        try:
            db.add(flight)
            db.commit()
            db.refresh(flight)
            return flight

        except IntegrityError:
            db.rollback()
            raise

    @staticmethod
    def update(
        db: Session,
        flight: Flight,
    ) -> Flight:
        try:
            db.commit()
            db.refresh(flight)
            return flight

        except IntegrityError:
            db.rollback()
            raise
    
    @staticmethod
    def delete(
        db: Session,
        flight: Flight,
    ) -> None:
        try:
            db.delete(flight)
            db.commit()

        except IntegrityError:
            db.rollback()
            raise

    @staticmethod
    def search_flights(
        db: Session,
        origin_airport_id: int,
        destination_airport_id: int,
        departure_date: date,
    ) -> list[Flight]:

        start_of_day = datetime.combine(
            departure_date,
            time.min,
        )

        end_of_day = datetime.combine(
            departure_date,
            time.max,
        )

        return (
            db.query(Flight)
            .filter(
                Flight.origin_airport_id == origin_airport_id,
                Flight.destination_airport_id == destination_airport_id,
                Flight.departure_time >= start_of_day,
                Flight.departure_time <= end_of_day,
            )
            .order_by(
                Flight.departure_time,
                Flight.base_price,
            )
            .all()
        )