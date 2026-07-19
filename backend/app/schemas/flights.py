from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


class FlightCreate(BaseModel):
    flight_number: str = Field(min_length=2, max_length=20)
    airline: str = Field(min_length=2, max_length=100)
    origin_airport_id: int = Field(gt=0)
    destination_airport_id: int = Field(gt=0)
    departure_time: datetime
    arrival_time: datetime
    base_price: Decimal = Field(gt=0)
    aircraft_type: str = Field(min_length=2, max_length=100)
    stops: int = Field(default=0, ge=0)

    @field_validator("flight_number")
    @classmethod
    def normalize_flight_number(cls, value: str) -> str:
        return value.strip().upper()

    @field_validator("airline", "aircraft_type")
    @classmethod
    def strip_text_fields(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("Field cannot be empty.")
        return value

    @model_validator(mode="after")
    def validate_route_and_times(self) -> "FlightCreate":
        if self.origin_airport_id == self.destination_airport_id:
            raise ValueError("Origin and destination airports must be different.")
        if self.arrival_time <= self.departure_time:
            raise ValueError("Arrival time must be after departure time.")
        return self


class FlightUpdate(BaseModel):
    flight_number: str | None = Field(default=None, min_length=2, max_length=20)
    airline: str | None = Field(default=None, min_length=2, max_length=100)
    origin_airport_id: int | None = Field(default=None, gt=0)
    destination_airport_id: int | None = Field(default=None, gt=0)
    departure_time: datetime | None = None
    arrival_time: datetime | None = None
    base_price: Decimal | None = Field(default=None, gt=0)
    aircraft_type: str | None = Field(default=None, min_length=2, max_length=100)
    stops: int | None = Field(default=None, ge=0)

    @field_validator("flight_number")
    @classmethod
    def normalize_flight_number(cls, value: str | None) -> str | None:
        if value is None:
            return None
        return value.strip().upper()

    @field_validator("airline", "aircraft_type")
    @classmethod
    def strip_text_fields(cls, value: str | None) -> str | None:
        if value is None:
            return None

        value = value.strip()
        if not value:
            raise ValueError("Field cannot be empty.")

        return value


class FlightResponse(BaseModel):
    id: int
    flight_number: str
    airline: str
    origin_airport_id: int
    destination_airport_id: int
    departure_time: datetime
    arrival_time: datetime
    duration_minutes: int
    base_price: Decimal
    aircraft_type: str
    stops: int

    model_config = ConfigDict(from_attributes=True)