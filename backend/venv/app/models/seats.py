import enum

from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    Enum,
    Numeric,
    CheckConstraint,
    UniqueConstraint,
    text,
)
from sqlalchemy.orm import relationship

from app.core.database import Base


class SeatClass(enum.Enum):
    ECONOMY = "economy"
    BUSINESS = "business"
    FIRST = "first"


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
    )

    id = Column(Integer, primary_key=True)

    flight_id = Column(
        Integer,
        ForeignKey("flights.id"),
        nullable=False,
        index=True
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
        default=SeatClass.ECONOMY,
        server_default=text("'economy'"),
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