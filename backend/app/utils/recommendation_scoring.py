from dataclasses import dataclass

from app.models.flights import Flight
from app.models.recommendation_weights import RecommendationWeight


@dataclass(frozen=True)
class RecommendationResult:
    flight: Flight
    computed_score: float
    price_component: float
    duration_component: float
    stops_component: float
    rank_position: int


def normalize_lower_better(
    value: float,
    minimum: float,
    maximum: float,
) -> float:

    if maximum == minimum:
        return 1.0

    return 1 - ((value - minimum) / (maximum - minimum))


def calculate_scores(
    flights: list[Flight],
    weights: RecommendationWeight,
) -> list[RecommendationResult]:

    if not flights:
        return []

    prices = [
        float(flight.base_price)
        for flight in flights
    ]

    durations = [
        float(flight.duration_minutes)
        for flight in flights
    ]

    min_price = min(prices)
    max_price = max(prices)

    min_duration = min(durations)
    max_duration = max(durations)

    results: list[RecommendationResult] = []

    for flight in flights:

        price_component = normalize_lower_better(
            value=float(flight.base_price),
            minimum=min_price,
            maximum=max_price,
        )

        duration_component = normalize_lower_better(
            value=float(flight.duration_minutes),
            minimum=min_duration,
            maximum=max_duration,
        )

        stops_component = 1 / (1 + flight.stops)

        computed_score = round(
            price_component * float(weights.price_weight)
            + duration_component * float(weights.duration_weight)
            + stops_component * float(weights.stops_weight),
            4
        )

        results.append(
            RecommendationResult(
                flight=flight,
                computed_score=computed_score,
                price_component=price_component,
                duration_component=duration_component,
                stops_component=stops_component,
                rank_position=0,
            )
        )

    results.sort(
        key=lambda result: result.computed_score,
        reverse=True,
    )

    ranked_results: list[RecommendationResult] = []

    for rank, result in enumerate(results, start=1):
        ranked_results.append(
            RecommendationResult(
                flight=result.flight,
                computed_score=result.computed_score,
                price_component=result.price_component,
                duration_component=result.duration_component,
                stops_component=result.stops_component,
                rank_position=rank,
            )
        )

    return ranked_results