from sqlalchemy.orm import Session

from app.models.booking import (
    Booking,
    BookingStatus,
)


class BookingRepository:

    @staticmethod
    def create(
        db: Session,
        booking: Booking,
    ) -> Booking:
        db.add(booking)
        db.flush()
        db.refresh(booking)

        return booking

    @staticmethod
    def get_by_id(
        db: Session,
        booking_id: int,
    ) -> Booking | None:
        return (
            db.query(Booking)
            .filter(Booking.id == booking_id)
            .first()
        )

    @staticmethod
    def get_by_pnr(
        db: Session,
        pnr: str,
    ) -> Booking | None:
        return (
            db.query(Booking)
            .filter(Booking.pnr == pnr)
            .first()
        )

    @staticmethod
    def get_by_user_id(
        db: Session,
        user_id: int,
    ) -> list[Booking]:
        return (
            db.query(Booking)
            .filter(Booking.user_id == user_id)
            .order_by(Booking.booked_at.desc())
            .all()
        )

    @staticmethod
    def get_confirmed_by_seat(
        db: Session,
        seat_id: int,
    ) -> Booking | None:
        return (
            db.query(Booking)
            .filter(
                Booking.seat_id == seat_id,
                Booking.status == BookingStatus.CONFIRMED,
            )
            .first()
        )