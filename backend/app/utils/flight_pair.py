from dataclasses import dataclass

from app.models.flights import Flight


@dataclass(frozen=True)
class FlightPair:
    first_leg: Flight
    second_leg: Flight