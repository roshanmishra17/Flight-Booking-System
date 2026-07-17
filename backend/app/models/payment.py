import enum

from sqlalchemy import (
    CheckConstraint,
    Column,
    DateTime,
    Enum,
    ForeignKey,
    Index,
    Integer,
    Numeric,
    text,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.database import Base


class PaymentMethod(enum.Enum):
    UPI = "upi"
    CREDIT_CARD = "credit_card"
    DEBIT_CARD = "debit_card"


class PaymentStatus(enum.Enum):
    PENDING = "pending"
    SUCCESS = "success"
    FAILED = "failed"
    REFUNDED = "refunded"


class Payment(Base):
    __tablename__ = "payments"

    __table_args__ = (
        CheckConstraint(
            "amount > 0",
            name="ck_payment_amount_positive",
        ),
        Index(
            "ix_payment_status",
            "status",
        ),
    )

    id = Column(Integer, primary_key=True)

    booking_id = Column(
        Integer,
        ForeignKey(
            "bookings.id",
            ondelete="RESTRICT",
        ),
        nullable=False,
        unique=True,
    )

    amount = Column(
        Numeric(10, 2, asdecimal=True),
        nullable=False,
    )

    payment_method = Column(
        Enum(
            PaymentMethod,
            values_callable=lambda x: [e.value for e in x],
            name="payment_method",
        ),
        nullable=False,
    )

    status = Column(
        Enum(
            PaymentStatus,
            values_callable=lambda x: [e.value for e in x],
            name="payment_status",
        ),
        nullable=False,
        default=PaymentStatus.PENDING,
        server_default=text("'pending'"),
    )

    created_at = Column(
        DateTime,
        server_default=func.now(),
        nullable=False,
    )

    updated_at = Column(
        DateTime,
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    booking = relationship(
        "Booking",
        back_populates="payment",
    )