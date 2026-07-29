from sqlalchemy.orm import Session

from app.models.recommendation_log import RecommendationLog
from app.models.recommendation_weights import (
    RecommendationMode,
    RecommendationWeight,
)

class RecommendationRepository:

    @staticmethod
    def get_weights_by_mode(
        db: Session,
        mode: RecommendationMode,
    ) -> RecommendationWeight | None:

        return (
            db.query(RecommendationWeight)
            .filter(RecommendationWeight.mode == mode)
            .first()
        )

    @staticmethod
    def bulk_create_logs(
        db: Session,
        logs: list[RecommendationLog],
    ) -> None:

        db.add_all(logs)