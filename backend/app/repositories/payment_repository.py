from sqlalchemy.orm import Session

from app.models.payment import Payment
from app.models.booking import Booking


class PaymentRepository:

    @staticmethod
    def create(
        db : Session,
        payment : Payment
    ) -> Payment :
        db.add(payment)
        db.flush()
        db.refresh(payment)
        return payment

    @staticmethod
    def get_by_id(
        db : Session,
        payment_id : int
    ) -> Payment | None :
        return (
            db.query(Payment)
            .filter(payment_id == Payment.id)
            .first()
        )

    @staticmethod
    def get_by_booking_id(
        db : Session,
        booking_id : int
    ) -> Payment :
        return (
            db.query(Payment)
            .filter(Payment.booking_id == booking_id)
            .first()
        )

    @staticmethod
    def update(
        db: Session,
        payment: Payment,
    ) -> Payment:
        db.flush()
        db.refresh(payment)
        return payment