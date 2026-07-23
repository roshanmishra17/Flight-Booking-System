from pydantic import BaseModel, ConfigDict, Field
from app.models.seats import (
    SeatClass,
    SeatPosition,
)
from datetime import datetime
from decimal import Decimal

from app.models.booking import BookingStatus



class BookingCreate(BaseModel):
    flight_id: int = Field(gt=0)
    seat_id: int = Field(gt=0)
    passenger_name: str = Field(
        min_length=1,
        max_length=100,
    )

    model_config = ConfigDict(
        extra="forbid",
        str_strip_whitespace=True,
    )


class BookedSeatResponse(BaseModel):
    id: int
    seat_number: str
    seat_class: SeatClass
    seat_position: SeatPosition

    model_config = ConfigDict(
        from_attributes=True,
    )


class BookingResponse(BaseModel):
    id: int
    pnr: str
    flight_id: int
    passenger_name: str
    seat: BookedSeatResponse
    status: BookingStatus
    total_price: Decimal
    booked_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )

class BookingSummaryResponse(BaseModel):
    id: int
    pnr: str
    passenger_name: str
    status: BookingStatus
    total_price: Decimal
    seat: BookedSeatResponse

    model_config = ConfigDict(
        from_attributes=True,
    )