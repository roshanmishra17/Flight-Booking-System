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
    String,
    text,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.database import Base


class BookingStatus(enum.Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"
    EXPIRED = "expired"


class Booking(Base):
    __tablename__ = "bookings"

    __table_args__ = (
        CheckConstraint(
            "total_price >= 0",
            name="ck_booking_total_price_non_negative",
        ),
        Index(
            "ix_booking_user_booked_at",
            "user_id",
            "booked_at",
        ),

        Index(
            "ix_booking_flight",
            "flight_id",
        ),

        Index(
            "ix_booking_seat",
            "seat_id",
        ),

        Index(
            "ux_booking_confirmed_seat",
            "seat_id",
            unique=True,
            postgresql_where=text("status = 'confirmed'"),
        ),
    )

    id = Column(Integer, primary_key=True)

    pnr = Column(
        String(10),
        unique=True,
        nullable=False,
        index=True,
    )

    user_id = Column(
        Integer,
        ForeignKey(
            "users.id",
            ondelete="RESTRICT",
        ),
        nullable=False,
    )

    flight_id = Column(
        Integer,
        ForeignKey(
            "flights.id",
            ondelete="RESTRICT",
        ),
        nullable=False,
    )

    seat_id = Column(
        Integer,
        ForeignKey(
            "seats.id",
            ondelete="RESTRICT",
        ),
        nullable=False,
    )

    passenger_name = Column(
        String(100),
        nullable=False,
    )

    status = Column(
        Enum(
            BookingStatus,
            values_callable=lambda x: [e.value for e in x],
            name="booking_status",
        ),
        nullable=False,
        default=BookingStatus.PENDING,
        server_default=text("'pending'"),
    )

    total_price = Column(
        Numeric(10, 2, asdecimal=True),
        nullable=False,
    )

    booked_at = Column(
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

    user = relationship(
        "User",
        back_populates="bookings",
    )

    flight = relationship(
        "Flight",
        back_populates="bookings",
    )

    seat = relationship(
        "Seat",
        back_populates="bookings",
    )
    payment = relationship(
        "Payment",
        back_populates="booking",
        uselist=False,
    )