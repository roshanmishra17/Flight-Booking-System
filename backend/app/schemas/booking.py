from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator
from app.models.seats import (
    SeatClass,
    SeatPosition,
)
from datetime import datetime
from decimal import Decimal
import re
from app.models.booking import BookingStatus



class BookingCreate(BaseModel):
    flight_id: int = Field(gt=0)
    seat_id: int = Field(gt=0)
    passenger_name: str = Field(
        min_length=1,
        max_length=100,
    )
    passenger_age: int = Field(ge=1, le=120)
    passenger_phone: str
    passenger_email: EmailStr

    model_config = ConfigDict(
        extra="forbid",
        str_strip_whitespace=True,
    )
    @field_validator("passenger_phone")
    @classmethod
    def validate_phone(cls, v: str) -> str:
        digits = re.sub(r"[\s\-]", "", v)
        match = re.fullmatch(r"(?:\+91|91|0)?([6-9]\d{9})", digits)
        if not match:
            raise ValueError("Enter a valid 10-digit Indian mobile number")
        return match.group(1)


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
    passenger_age: int | None = None
    passenger_phone: str | None = None
    passenger_email: str | None = None
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