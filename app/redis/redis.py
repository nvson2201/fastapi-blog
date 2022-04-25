from typing import AsyncIterator
import aioredis


async def init_redis_pool(host: str, password: str) -> AsyncIterator[aioredis.Redis]:
    pool = aioredis.ConnectionPool.from_url(
        "redis://localhost", encoding="utf-8", decode_responses=True
    )
    meanings = aioredis.Redis(connection_pool=pool)
    try:
        await meanings.set("life", 42)
        print(f"The answer: {await meanings.get('life')}")
    finally:
        await pool.disconnect()
