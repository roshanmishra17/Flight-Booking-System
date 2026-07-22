from app.layout.aircraft_layout import AircraftLayout
from app.models.flights import Flight
from app.models.seats import Seat


class SeatGenerator:

    @staticmethod
    def generate(
        flight: Flight,
        layout: AircraftLayout,
    ) -> list[Seat]:


        seats = []

        for section in layout.sections:

            for row in range(
                section.start_row,
                section.end_row + 1,
            ):

                for letter in section.seat_letters:

                    seats.append(
                        Seat(
                            flight=flight,
                            seat_number=f"{row}{letter}",
                            seat_class=section.seat_class,
                            seat_position=section.seat_positions[
                                letter
                            ],
                            price_multiplier=section.price_multiplier,
                        )
                    )

        return seats