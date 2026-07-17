from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.database import Base


class SavedFlight(Base):
    __tablename__ = "saved_flights"

    __table_args__ = (
        UniqueConstraint(
            "user_id",
            "flight_id",
            name="uq_user_saved_flight",
        ),
        Index(
            "ix_saved_flight_user",
            "user_id",
        ),
    )

    id = Column(Integer, primary_key=True)

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

    saved_at = Column(
        DateTime,
        server_default=func.now(),
        nullable=False,
    )

    user = relationship(
        "User",
        back_populates="saved_flights",
    )

    flight = relationship(
        "Flight",
        back_populates="saved_flights",
    )