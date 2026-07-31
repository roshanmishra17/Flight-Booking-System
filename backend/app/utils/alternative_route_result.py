from dataclasses import dataclass
from decimal import Decimal

from app.models.flights import Flight


@dataclass(frozen=True)
class AlternativeRouteResult:
    first_leg: Flight
    second_leg: Flight
    layover_minutes: int
    total_duration: int
    estimated_total_price: Decimal