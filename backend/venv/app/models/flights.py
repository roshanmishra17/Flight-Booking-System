from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey,
    Numeric,
    Index,
    CheckConstraint,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship

from app.core.database import Base


class Flight(Base):
    __tablename__ = "flights"

    __table_args__ = (
        Index(
            "idx_flight_search",
            "origin_airport_id",
            "destination_airport_id",
            "departure_time",
        ),
        UniqueConstraint(
            "flight_number",
            "departure_time",
            name="uq_flight_number_departure",
        ),
        CheckConstraint(
            "origin_airport_id <> destination_airport_id",
            name="ck_origin_destination_different",
        ),

        CheckConstraint(
            "arrival_time > departure_time",
            name="ck_arrival_after_departure",
        ),
        CheckConstraint(
            "duration_minutes > 0",
            name="ck_duration_positive",
        ),
        CheckConstraint(
            "base_price > 0",
            name="ck_base_price_positive",
        ),
        CheckConstraint(
            "stops >= 0",
            name="ck_stops_non_negative",
        ),
    )

    id = Column(Integer, primary_key=True)

    flight_number = Column(
        String(20),
        nullable=False,
        index=True,
    )

    airline = Column(
        String(100),
        nullable=False,
    )

    origin_airport_id = Column(
        Integer,
        ForeignKey("airports.id"),
        nullable=False,
    )

    destination_airport_id = Column(
        Integer,
        ForeignKey("airports.id"),
        nullable=False,
    )

    departure_time = Column(
        DateTime,
        nullable=False,
    )

    arrival_time = Column(
        DateTime,
        nullable=False,
    )

    duration_minutes = Column(
        Integer,
        nullable=False,
    )

    base_price = Column(
        Numeric(10, 2),
        nullable=False,
    )

    aircraft_type = Column(
        String(100),
        nullable=False,
    )

    stops = Column(
        Integer,
        default=0,
        nullable=False,
    )

    origin_airport = relationship(
        "Airport",
        foreign_keys=[origin_airport_id],
        back_populates="origin_flights",
    )

    destination_airport = relationship(
        "Airport",
        foreign_keys=[destination_airport_id],
        back_populates="destination_flights",
    )
    seats = relationship(
        "Seat",
        back_populates="flight",
        cascade="all, delete-orphan",
    )
    bookings = relationship(
        "Booking",
        back_populates="flight",
    )
    recommendation_logs = relationship(
        "RecommendationLog",
        back_populates="flight",
    )
    saved_flights = relationship(
        "SavedFlight",
        back_populates="flight",
    )