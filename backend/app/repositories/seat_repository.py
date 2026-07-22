from sqlalchemy.orm import Session

from app.models.seats import Seat


class SeatRepository:
    @staticmethod
    def bulk_create(
        db: Session,
        seats: list[Seat],
    ) -> None:
        db.add_all(seats)

    @staticmethod
    def get_by_id(
        db: Session,
        seat_id: int,
    ) -> Seat | None:
        return (
            db.query(Seat)
            .filter(Seat.id == seat_id)
            .first()
        )

    @staticmethod
    def get_by_flight(
        db: Session,
        flight_id: int,
    ) -> list[Seat]:

        return (
            db.query(Seat)
            .filter(Seat.flight_id == flight_id)
            .all()
        )

    @staticmethod
    def get_by_flight_and_number(
        db: Session,
        flight_id: int,
        seat_number: str,
    ) -> Seat | None:
        
        return (
            db.query(Seat)
            .filter(
                Seat.flight_id == flight_id,
                Seat.seat_number == seat_number,
            )
            .first()
        )