from pydantic import BaseModel, ConfigDict, Field, field_validator


class AirportCreate(BaseModel):

    iata_code: str = Field(min_length=3, max_length=3)

    @field_validator("iata_code")
    @classmethod
    def validate_iata_format(cls, v: str) -> str:
        v = v.strip().upper()
        if not v.isalpha():
            raise ValueError("IATA code must contain only letters")
        return v
    name: str = Field(min_length=2, max_length=255)
    city: str = Field(min_length=2, max_length=100)
    country: str = Field(min_length=2, max_length=100)


class AirportUpdate(BaseModel):
    iata_code: str | None = Field(default=None, min_length=3, max_length=3)
    name: str | None = Field(default=None, min_length=2, max_length=255)
    city: str | None = Field(default=None, min_length=2, max_length=100,)
    country: str | None = Field(default=None, min_length=2, max_length=100)


class AirportResponse(BaseModel):
    id: int
    iata_code: str
    name: str
    city: str
    country: str

    model_config = ConfigDict(from_attributes=True)