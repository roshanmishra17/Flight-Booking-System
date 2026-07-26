import redis

from app.core.redis import redis_client
from app.core.exceptions import RedisUnavailableError


class SeatLockService:

    LOCK_TTL = 300  # 5 minutes

    @staticmethod
    def acquire_lock(
        flight_id: int,
        seat_id: int,
        user_id: int,
    ) -> bool:
        key = f"seat_lock:{flight_id}:{seat_id}"
        try:
            return bool(
                    redis_client.set(
                    name=key,
                    value=user_id,
                    nx=True,
                    ex=SeatLockService.LOCK_TTL,
                )
            )
        except redis.exceptions.ConnectionError as e:
            raise RedisUnavailableError(
                "Seat locking service is temporarily unavailable."
            ) from e