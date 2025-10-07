from fastapi import FastAPI
from contextlib import asynccontextmanager
import redis.asyncio as redis
from health import router as health_router
import deps

def create_app(use_lifespan: bool = True):
    if use_lifespan:
        @asynccontextmanager
        async def lifespan(app: FastAPI):
            deps.redis_client = redis.Redis(host="localhost", port=6379, decode_responses=True)
            try:
                await deps.redis_client.ping()
                print("✅ Conectado a Redis")
            except Exception as e:
                print(f"❌ Error al conectar a Redis: {e}")
                raise
            yield
            await deps.redis_client.close()
        
        app = FastAPI(lifespan=lifespan)
    else:
        # Para tests: usa un mock o cliente dummy
        from unittest.mock import AsyncMock
        if deps.redis_client is None:
            deps.redis_client = AsyncMock()
        app = FastAPI()
    
    app.include_router(health_router)
    return app

app = create_app(use_lifespan=True)