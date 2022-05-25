import redis
from app.config import settings

pool = redis.ConnectionPool(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    password=settings.REDIS_PASSWORD,
)
redis_session = redis.Redis(connection_pool=pool)
