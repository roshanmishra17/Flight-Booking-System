import enum

from sqlalchemy import (
    CheckConstraint,
    Column,
    Enum,
    Integer,
    Numeric,
)

from app.core.database import Base


class RecommendationMode(enum.Enum):
    CHEAPEST = "cheapest"
    FASTEST = "fastest"
    BALANCED = "balanced"


class RecommendationWeight(Base):
    __tablename__ = "recommendation_weights"

    __table_args__ = (
        CheckConstraint(
            "price_weight >= 0 AND price_weight <= 1",
            name="ck_price_weight_range",
        ),
        CheckConstraint(
            "duration_weight >= 0 AND duration_weight <= 1",
            name="ck_duration_weight_range",
        ),
        CheckConstraint(
            "stops_weight >= 0 AND stops_weight <= 1",
            name="ck_stops_weight_range",
        ),
        CheckConstraint(
            "price_weight + duration_weight + stops_weight = 1.00",
            name="ck_weights_sum_to_one",
        ),
    )

    id = Column(Integer, primary_key=True)

    mode = Column(
        Enum(
            RecommendationMode,
            values_callable=lambda x: [e.value for e in x],
            name="recommendation_mode",
        ),
        nullable=False,
        unique=True,
    )

    price_weight = Column(
        Numeric(3, 2, asdecimal=True),
        nullable=False,
    )

    duration_weight = Column(
        Numeric(3, 2, asdecimal=True),
        nullable=False,
    )

    stops_weight = Column(
        Numeric(3, 2, asdecimal=True),
        nullable=False,
    )