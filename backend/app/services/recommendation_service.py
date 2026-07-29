from sqlalchemy.orm import Session

from app.models.recommendation_log import RecommendationLog
from app.models.search import Search
from app.models.flights import Flight
from app.repositories.recommendation_repository import RecommendationRepository
from app.utils.recommendation_scoring import (
    RecommendationResult,
    calculate_scores,
)
from app.core.exceptions import RecommendationWeightsNotFound


class RecommendationService:

    @staticmethod
    def rank_flights(
        db: Session,
        search: Search,
        flights: list[Flight],
    ) -> list[RecommendationResult]:

        if not flights:
            return []

        weights = RecommendationRepository.get_weights_by_mode(
            db=db,
            mode=search.mode,
        )

        if weights is None:
            raise RecommendationWeightsNotFound(
                f"No recommendation weights found for mode '{search.mode.value}'."
            )

        ranked_results = calculate_scores(
            flights=flights,
            weights=weights,
        )

        logs = []

        for result in ranked_results:

            logs.append(
                RecommendationLog(
                    search_id=search.id,
                    flight_id=result.flight.id,
                    computed_score=result.computed_score,
                    price_component=result.price_component,
                    duration_component=result.duration_component,
                    stops_component=result.stops_component,
                    rank_position=result.rank_position,
                )
            )

        RecommendationRepository.bulk_create_logs(
            db=db,
            logs=logs,
        )

        return ranked_results