
from datetime import date, timedelta
from decimal import Decimal

from sqlalchemy.orm import Session

from app.repositories.booking_repository import BookingRepository
from app.repositories.flight_repository import FlightRepository
from app.services.pricing_service import PricingService
from app.utils.alternative_route_result import AlternativeRouteResult
from app.utils.flight_pair import FlightPair


class AlternativeRouteService:

    MIN_LAYOVER = timedelta(minutes=45)
    MAX_LAYOVER = timedelta(hours=4)

    @staticmethod
    def find_alternative_routes(
        db: Session,
        origin_airport_id: int,
        destination_airport_id: int,
        departure_date: date,
    ) -> list[AlternativeRouteResult]:

        first_leg_flights = FlightRepository.get_departing_flights(
            db=db,
            origin_airport_id=origin_airport_id,
            departure_date=departure_date,
        )

        candidate_pairs: list[FlightPair] = []

        for first_leg in first_leg_flights:

            earliest_departure = (
                first_leg.arrival_time
                + AlternativeRouteService.MIN_LAYOVER
            )

            latest_departure = (
                first_leg.arrival_time
                + AlternativeRouteService.MAX_LAYOVER
            )

            second_leg_flights = (
                FlightRepository.get_flights_between_airports(
                    db=db,
                    origin_airport_id=first_leg.destination_airport_id,
                    destination_airport_id=destination_airport_id,
                    earliest_departure=earliest_departure,
                    latest_departure=latest_departure,
                )
            )

            for second_leg in second_leg_flights:
                candidate_pairs.append(
                    FlightPair(
                        first_leg=first_leg,
                        second_leg=second_leg,
                    )
                )

        if not candidate_pairs:
            return []

        flight_ids: set[int] = set()

        for pair in candidate_pairs:
            flight_ids.add(pair.first_leg.id)
            flight_ids.add(pair.second_leg.id)

        occupancy_data = BookingRepository.get_occupancy_data(
            db=db,
            flight_ids=list(flight_ids),
        )

        routes: list[AlternativeRouteResult] = []

        for pair in candidate_pairs:

            first_leg = pair.first_leg
            second_leg = pair.second_leg

            layover_minutes = int(
                (
                    second_leg.departure_time
                    - first_leg.arrival_time
                ).total_seconds()
                / 60
            )

            total_duration = (
                first_leg.duration_minutes
                + layover_minutes
                + second_leg.duration_minutes
            )

            first_booked, first_total = occupancy_data.get(
                first_leg.id,
                (0, 0),
            )

            second_booked, second_total = occupancy_data.get(
                second_leg.id,
                (0, 0),
            )

            first_price = PricingService.calculate_current_price(
                base_price=first_leg.base_price,
                occupancy=PricingService.calculate_occupancy(
                    total_seats=first_total,
                    booked_seats=first_booked,
                ),
                departure_time=first_leg.departure_time,
            )

            second_price = PricingService.calculate_current_price(
                base_price=second_leg.base_price,
                occupancy=PricingService.calculate_occupancy(
                    total_seats=second_total,
                    booked_seats=second_booked,
                ),
                departure_time=second_leg.departure_time,
            )

            # Attach runtime prices for API response
            first_leg.current_price = first_price
            second_leg.current_price = second_price

            routes.append(
                AlternativeRouteResult(
                    first_leg=first_leg,
                    second_leg=second_leg,
                    layover_minutes=layover_minutes,
                    total_duration=total_duration,
                    estimated_total_price=Decimal(
                        str(first_price + second_price)
                    ),
                )
            )

        routes.sort(
            key=lambda route: (
                route.total_duration,
                route.estimated_total_price,
            )
        )

        return routes[:3]