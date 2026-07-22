import enum

from sqlalchemy import (
    CheckConstraint,
    Column,
    Enum,
    ForeignKey,
    Index,
    Integer,
    Numeric,
    String,
    UniqueConstraint,
    text,
)
from sqlalchemy.orm import relationship

from app.core.database import Base


class SeatClass(enum.Enum):
    ECONOMY = "economy"
    BUSINESS = "business"

class SeatPosition(enum.Enum):
    WINDOW = "window"
    MIDDLE = "middle"
    AISLE = "aisle"


class Seat(Base):
    __tablename__ = "seats"

    __table_args__ = (
        UniqueConstraint(
            "flight_id",
            "seat_number",
            name="uq_flight_seat",
        ),
        CheckConstraint(
            "price_multiplier > 0",
            name="ck_price_multiplier_positive",
        ),
        Index(
            "idx_flight_seat_class",
            "flight_id",
            "seat_class",
        ),
    )

    id = Column(Integer, primary_key=True)

    flight_id = Column(
        Integer,
        ForeignKey(
            "flights.id",
            ondelete="CASCADE",
        ),
        nullable=False,
    )

    seat_number = Column(
        String(5),
        nullable=False,
    )

    seat_class = Column(
        Enum(
            SeatClass,
            values_callable=lambda x: [e.value for e in x],
            name="seat_class",
        ),
        nullable=False,
    )

    price_multiplier = Column(
        Numeric(4, 2),
        nullable=False,
    )

    flight = relationship(
        "Flight",
        back_populates="seats",
    )

    bookings = relationship(
        "Booking",
        back_populates="seat",
        passive_deletes=True,
    )