import redis

from app.core.redis import redis_client
from app.core.exceptions import RedisUnavailableError


class SeatLockService:

    LOCK_TTL = 300  # 5 minutes

    @staticmethod
    def _lock_key(flight_id: int, seat_id: int) -> str:
        return f"seat_lock:{flight_id}:{seat_id}"

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

    @staticmethod
    def release_lock(flight_id: int, seat_id: int) -> None:
        key = SeatLockService._lock_key(flight_id, seat_id)
        try:
            redis_client.delete(key)
        except redis.exceptions.ConnectionError as e:
            raise RedisUnavailableError(
                "Seat locking service is temporarily unavailable."
            ) from e


    @staticmethod
    def get_locked_seat_ids(flight_id: int, seat_ids: list[int]) -> set[int]:
        if not seat_ids:
            return set()

        keys = [SeatLockService._lock_key(flight_id, sid) for sid in seat_ids]
        try:
            values = redis_client.mget(keys)  # one round trip for all seats
        except redis.exceptions.ConnectionError:
            return set()  # Redis down: show as available, booking still checks the lock

        return {sid for sid, value in zip(seat_ids, values) if value is not None}