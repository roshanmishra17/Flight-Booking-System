from pydantic import BaseModel, ConfigDict

from app.schemas.flights import FlightResponse

class RankedFlightResponse(BaseModel):
    flight: FlightResponse
    computed_score: float
    price_component: float
    duration_component: float
    stops_component: float
    rank_position: int

    model_config = ConfigDict(from_attributes=True)