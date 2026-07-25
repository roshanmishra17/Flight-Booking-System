from decimal import Decimal

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.exceptions import (
    BookingAlreadyExistsError,
    BookingNotFoundError,
    FlightNotFoundError,
    InvalidBookingStatusError,
    InvalidPaymentStatusError,
    PaymentNotFoundError,
    SeatAlreadyBookedError,
    SeatNotBelongsToFlightError,
    SeatNotFoundError,
)
from app.models.booking import Booking, BookingStatus
from app.models.users import User, UserRole
from app.repositories.booking_repository import BookingRepository
from app.repositories.flight_repository import FlightRepository
from app.repositories.seat_repository import SeatRepository
from app.schemas.booking import BookingCreate
from app.utils.pnr_generator import generate_pnr
from app.repositories.payment_repository import PaymentRepository
from app.models.payment import PaymentStatus


class BookingService:

    @staticmethod
    def _generate_unique_pnr(
        db: Session,
    ) -> str:
        while True:
            pnr = generate_pnr()

            if not BookingRepository.get_by_pnr(
                db,
                pnr,
            ):
                return pnr

    @staticmethod
    def create_booking(
        db: Session,
        current_user: User,
        booking_data: BookingCreate,
    ) -> Booking:

        flight = FlightRepository.get_by_id(
            db,
            booking_data.flight_id,
        )
        if not flight:
            raise FlightNotFoundError("Flight not found.")

        seat = SeatRepository.get_by_id(
            db,
            booking_data.seat_id,
        )
        if not seat:
            raise SeatNotFoundError("Seat not found.")

        if seat.flight_id != flight.id:
            raise SeatNotBelongsToFlightError(
                "Seat does not belong to this flight."
            )

        existing_user_booking = (
            BookingRepository.get_active_by_user_and_seat(
                db,
                current_user.id,
                seat.id,
            )
        )

        if existing_user_booking:
            raise BookingAlreadyExistsError(
                "You already have an active booking for this seat."
            )


        existing_booking = BookingRepository.get_confirmed_by_seat(
            db,
            seat.id,
        )
        if existing_booking:
            raise SeatAlreadyBookedError(
                "Seat is already booked."
            )

        total_price = (
            flight.base_price
            * seat.price_multiplier
        )

        booking = Booking(
            pnr=BookingService._generate_unique_pnr(db),
            user_id=current_user.id,
            flight_id=flight.id,
            seat_id=seat.id,
            passenger_name=booking_data.passenger_name,
            status=BookingStatus.PENDING,
            total_price=total_price,
        )

        try:
            booking = BookingRepository.create(
                db,
                booking,
            )
            db.commit()
            return booking

        except IntegrityError:
            db.rollback()
            raise

    @staticmethod
    def get_booking_by_id(
        db: Session,
        booking_id: int,
        current_user: User,
    ) -> Booking:

        booking = BookingRepository.get_by_id(
            db,
            booking_id,
        )

        if not booking:
            raise BookingNotFoundError(
                "Booking not found."
            )

        if (
            booking.user_id != current_user.id
            and current_user.role != UserRole.ADMIN
        ):
            raise BookingNotFoundError(
                "Booking not found."
            )

        return booking


    @staticmethod
    def get_my_bookings(
        db: Session,
        current_user: User,
    ) -> list[Booking]:

        return BookingRepository.get_by_user_id(
            db,
            current_user.id,
        )

    @staticmethod
    def cancel_booking(
        db: Session,
        current_user: User,
        booking_id: int,
    ) -> Booking:

        booking = BookingRepository.get_by_id(db, booking_id)
        if not booking:
            raise BookingNotFoundError("Booking not found.")

        if (
            booking.user_id != current_user.id
            and current_user.role != UserRole.ADMIN
        ):
            raise BookingNotFoundError("Booking not found.")

        if booking.status == BookingStatus.CANCELLED:
            raise InvalidBookingStatusError("Booking is already cancelled.")

        if booking.status == BookingStatus.EXPIRED:
            raise InvalidBookingStatusError("Expired bookings cannot be cancelled.")

        if booking.status == BookingStatus.CONFIRMED:
            payment = PaymentRepository.get_by_booking_id(db, booking.id)
            if not payment:
                raise PaymentNotFoundError(
                    "Payment not found for confirmed booking."
                )

            if payment.status != PaymentStatus.SUCCESS:
                raise InvalidPaymentStatusError(
                    "Only successful payment can be refunded."
                )

            payment.status = PaymentStatus.REFUNDED

        booking.status = BookingStatus.CANCELLED

        try:
            db.commit()
        except Exception:
            db.rollback()
            raise

        db.refresh(booking)
        return booking