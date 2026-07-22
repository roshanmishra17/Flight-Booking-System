import enum
from decimal import Decimal

from pydantic import BaseModel, ConfigDict

from app.models.seats import SeatClass, SeatPosition


class SeatAvailability(enum.Enum):
    AVAILABLE = "available"
    RESERVED = "reserved"
    BOOKED = "booked"


class SeatResponse(BaseModel):
    id: int
    seat_number: str
    seat_class: SeatClass
    seat_position: SeatPosition
    price_multiplier: Decimal
    availability: SeatAvailability

    model_config = ConfigDict(from_attributes=True)



class SeatMapResponse(BaseModel):
    id: int
    seat_number: str
    seat_class: SeatClass
    price_multiplier: Decimal
    availability: SeatAvailability

    model_config = ConfigDict(
        from_attributes=True,
    )