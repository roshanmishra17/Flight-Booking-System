from sqlalchemy import (
    CheckConstraint,
    Column,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    Numeric,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.database import Base


class RecommendationLog(Base):
    __tablename__ = "recommendation_logs"

    __table_args__ = (

        UniqueConstraint(
            "search_id",
            "flight_id",
            name="uq_search_flight",
        ),

        UniqueConstraint(
            "search_id",
            "rank_position",
            name="uq_search_rank",
        ),

        CheckConstraint(
            "computed_score >= 0",
            name="ck_computed_score_non_negative",
        ),
        CheckConstraint(
            "price_component >= 0",
            name="ck_price_component_non_negative",
        ),
        CheckConstraint(
            "duration_component >= 0",
            name="ck_duration_component_non_negative",
        ),
        CheckConstraint(
            "stops_component >= 0",
            name="ck_stops_component_non_negative",
        ),
        CheckConstraint(
            "rank_position > 0",
            name="ck_rank_position_positive",
        ),
        Index(
            "ix_recommendation_search_rank",
            "search_id",
            "rank_position",
        ),
    )

    id = Column(Integer, primary_key=True)

    search_id = Column(
        Integer,
        ForeignKey(
            "searches.id",
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

    computed_score = Column(
        Numeric(5, 4, asdecimal=True),
        nullable=False,
    )

    price_component = Column(
        Numeric(5, 4, asdecimal=True),
        nullable=False,
    )

    duration_component = Column(
        Numeric(5, 4, asdecimal=True),
        nullable=False,
    )

    stops_component = Column(
        Numeric(5, 4, asdecimal=True),
        nullable=False,
    )

    rank_position = Column(
        Integer,
        nullable=False,
    )

    created_at = Column(
        DateTime,
        server_default=func.now(),
        nullable=False,
    )

    search = relationship(
        "Search",
        back_populates="recommendation_logs",
    )

    flight = relationship(
        "Flight",
        back_populates="recommendation_logs",
    )