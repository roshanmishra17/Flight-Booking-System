import enum

from sqlalchemy import (
    CheckConstraint,
    Column,
    Date,
    DateTime,
    Enum,
    ForeignKey,
    Index,
    Integer,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.database import Base
from app.models.recommendation_weights import RecommendationMode
from app.models.seats import SeatClass


class Search(Base):
    __tablename__ = "searches"

    __table_args__ = (
        CheckConstraint(
            "origin_airport_id <> destination_airport_id",
            name="ck_search_origin_destination_different",
        ),
        Index(
            "ix_search_user_searched_at",
            "user_id",
            "searched_at",
        ),
        Index(
            "ix_search_route_date",
            "origin_airport_id",
            "destination_airport_id",
            "travel_date",
        ),
    )

    id = Column(Integer, primary_key=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )

    origin_airport_id = Column(
        Integer,
        ForeignKey("airports.id", ondelete="RESTRICT"),
        nullable=False,
    )

    destination_airport_id = Column(
        Integer,
        ForeignKey("airports.id", ondelete="RESTRICT"),
        nullable=False,
    )

    travel_date = Column(
        Date,
        nullable=False,
    )

    travel_class = Column(
        Enum(
            SeatClass,
            values_callable=lambda x: [e.value for e in x],
            name="seat_class",
        ),
        nullable=False,
    )

    mode = Column(
        Enum(
            RecommendationMode,
            values_callable=lambda x: [e.value for e in x],
            name="recommendation_mode",
        ),
        nullable=False,
    )

    searched_at = Column(
        DateTime,
        server_default=func.now(),
        nullable=False,
    )

    user = relationship(
        "User",
        back_populates="searches",
    )

    origin_airport = relationship(
        "Airport",
        foreign_keys=[origin_airport_id],
        back_populates="origin_searches",
    )

    destination_airport = relationship(
        "Airport",
        foreign_keys=[destination_airport_id],
        back_populates="destination_searches",
    )

    recommendation_logs = relationship(
        "RecommendationLog",
        back_populates="search",
    )
