from sqlalchemy.orm import Session

from app.core.exceptions import (
    BookingNotFoundError,
    InvalidBookingStatusError,
    PaymentAlreadyExistsError,
    PaymentNotFoundError,
)
from app.models.booking import BookingStatus
from app.models.payment import Payment, PaymentStatus
from app.models.users import User, UserRole
from app.repositories.booking_repository import BookingRepository
from app.repositories.payment_repository import PaymentRepository
from app.schemas.payment import PaymentCreate


class PaymentService:

    @staticmethod
    def make_payment(
        db: Session,
        current_user: User,
        payment_data: PaymentCreate,
    ) -> Payment:

        booking = BookingRepository.get_by_id(db, payment_data.booking_id)
        if not booking:
            raise BookingNotFoundError("Booking not found.")

        if (
            booking.user_id != current_user.id
            and current_user.role != UserRole.ADMIN
        ):
            raise BookingNotFoundError("Booking not found.")

        if booking.status != BookingStatus.PENDING:
            raise InvalidBookingStatusError(
                "Only pending bookings can be paid."
            )

        existing_payment = PaymentRepository.get_by_booking_id(db, booking.id)

        if existing_payment and existing_payment.status == PaymentStatus.SUCCESS:
            raise PaymentAlreadyExistsError(
                "Payment already completed for this booking."
            )

        if existing_payment:
            payment = existing_payment
            payment.payment_method = payment_data.payment_method
            payment.status = PaymentStatus.PENDING
        else:
            payment = Payment(
                booking_id=booking.id,
                amount=booking.total_price,
                payment_method=payment_data.payment_method,
                status=PaymentStatus.PENDING,
            )
            PaymentRepository.create(db, payment)

        payment_succeeded = not payment_data.simulate_failure

        if payment_succeeded:
            payment.status = PaymentStatus.SUCCESS
            booking.status = BookingStatus.CONFIRMED
        else:
            payment.status = PaymentStatus.FAILED

        try:
            db.commit()
        except Exception:
            db.rollback()
            raise

        db.refresh(payment)
        db.refresh(booking)
        return payment

    @staticmethod
    def get_payment(
        db: Session,
        current_user: User,
        payment_id: int,
    ) -> Payment:

        payment = PaymentRepository.get_by_id(
            db,
            payment_id,
        )

        if not payment:
            raise PaymentNotFoundError(
                "Payment not found."
            )

        booking = payment.booking

        if (
            booking.user_id != current_user.id
            and current_user.role != UserRole.ADMIN
        ):
            raise PaymentNotFoundError(
                "Payment not found."
            )

        return payment