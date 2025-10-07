from fastapi import Depends
from redis.asyncio import Redis
from typing import Annotated

redis_client: Redis | None = None

async def get_redis_client() -> Redis:
    if redis_client is None:
        raise RuntimeError("Redis client not initialized")
    return redis_client

RedisDep = Annotated[Redis, Depends(get_redis_client)]