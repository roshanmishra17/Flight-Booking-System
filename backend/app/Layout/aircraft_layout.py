from dataclasses import dataclass
from decimal import Decimal
import enum

from app.models.seats import SeatClass
from app.models.seats import SeatPosition




@dataclass(frozen=True)
class SeatSection:
    start_row: int
    end_row: int
    seat_letters: str
    seat_positions: dict[str, SeatPosition]
    seat_class: SeatClass
    price_multiplier: Decimal


@dataclass(frozen=True)
class AircraftLayout:
    sections: list[SeatSection]


STANDARD_180_LAYOUT = AircraftLayout(
    sections=[
        SeatSection(
            start_row=1,
            end_row=3,
            seat_letters="ABCD",
            seat_positions={
                "A": SeatPosition.WINDOW,
                "B": SeatPosition.AISLE,
                "C": SeatPosition.AISLE,
                "D": SeatPosition.WINDOW,
            },
            seat_class=SeatClass.BUSINESS,
            price_multiplier=Decimal("2.00"),
        ),
        SeatSection(
            start_row=4,
            end_row=31,
            seat_letters="ABCDEF",
            seat_positions={
                "A": SeatPosition.WINDOW,
                "B": SeatPosition.MIDDLE,
                "C": SeatPosition.AISLE,
                "D": SeatPosition.AISLE,
                "E": SeatPosition.MIDDLE,
                "F": SeatPosition.WINDOW,
            },
            seat_class=SeatClass.ECONOMY,
            price_multiplier=Decimal("1.00"),
        ),
    ]
)


ATR72_LAYOUT = AircraftLayout(
    sections=[
        SeatSection(
            start_row=1,
            end_row=2,
            seat_letters="ABCD",
            seat_positions={
                "A": SeatPosition.WINDOW,
                "B": SeatPosition.AISLE,
                "C": SeatPosition.AISLE,
                "D": SeatPosition.WINDOW,
            },
            seat_class=SeatClass.BUSINESS,
            price_multiplier=Decimal("2.00"),
        ),
        SeatSection(
            start_row=3,
            end_row=18,
            seat_letters="ABCD",
            seat_positions={
                "A": SeatPosition.WINDOW,
                "B": SeatPosition.AISLE,
                "C": SeatPosition.AISLE,
                "D": SeatPosition.WINDOW,
            },
            seat_class=SeatClass.ECONOMY,
            price_multiplier=Decimal("1.00"),
        ),
    ]
)


AIRCRAFT_LAYOUTS = {
    "Airbus A320": STANDARD_180_LAYOUT,
    "Boeing 737": STANDARD_180_LAYOUT,
    "ATR 72": ATR72_LAYOUT,
}