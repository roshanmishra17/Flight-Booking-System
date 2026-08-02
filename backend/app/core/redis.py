import redis
from app.core.config import REDIS_URL
redis_client = redis.Redis(
    REDIS_URL,
    decode_responses=True,
    protocol=2,
)