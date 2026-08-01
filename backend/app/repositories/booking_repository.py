import datetime

from sqlalchemy import case, func
from sqlalchemy.orm import Session

from app.models.booking import (
    Booking,
    BookingStatus,
)
from app.models.seats import Seat
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

    @staticmethod
    def get_active_by_user_and_seat(
        db: Session,
        user_id: int,
        seat_id: int,
    ) -> Booking | None:
        return (
            db.query(Booking)
            .filter(
                Booking.user_id == user_id,
                Booking.seat_id == seat_id,
                Booking.status.in_([
                    BookingStatus.PENDING,
                    BookingStatus.CONFIRMED,
                ]),
            )
            .first()
        )


    @staticmethod
    def get_stale_pending(
        db: Session,
        threshold_seconds: int,
    ) -> list[Booking]:

        cutoff = datetime.datetime.now() - datetime.timedelta(
            seconds=threshold_seconds,
        )
        
        pending = (
                db.query(Booking)
                .filter(Booking.status == BookingStatus.PENDING)
                .all()
            )

        for booking in pending:
            print(
                f"id={booking.id}, booked_at={booking.booked_at}, "
                f"booked_at<=cutoff? {booking.booked_at <= cutoff}"
            )
        return (
            db.query(Booking)
            .filter(
                Booking.status == BookingStatus.PENDING,
                Booking.booked_at <= cutoff,
            )
            .all()
        )

    from sqlalchemy import case, func


    @staticmethod
    def get_occupancy_data(
        db: Session,
        flight_ids: list[int],
    ) -> dict[int, tuple[int, int]]:

        if not flight_ids:
            return {}

        rows = (
            db.query(
                Seat.flight_id,
                func.count(Seat.id).label("total_seats"),
                func.count(
                    case(
                        (
                            Booking.status == BookingStatus.CONFIRMED,
                            1,
                        ),
                    )
                ).label("booked_seats"),
            )
            .select_from(Seat)
            .outerjoin(
                Booking,
                Booking.seat_id == Seat.id,
            )
            .filter(
                Seat.flight_id.in_(flight_ids),
            )
            .group_by(
                Seat.flight_id,
            )
            .all()
        )

        return {
            row.flight_id: (
                row.booked_seats,
                row.total_seats,
            )
            for row in rows
        }