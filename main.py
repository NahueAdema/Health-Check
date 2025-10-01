# main.py
from fastapi import FastAPI
from contextlib import asynccontextmanager
import redis.asyncio as redis
from health import router as health_router

# Variable global para la conexión (o usa dependency injection)
redis_client = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global redis_client
    # Conectar a Redis

    redis_client = redis.Redis(host="localhost", port=6379, decode_responses=True)
    try:
        await redis_client.ping()
        print("✅ Conectado a Redis")
    except Exception as e:
        print(f"❌ Error al conectar a Redis: {e}")
        raise
    yield
    # Cerrar conexión al apagar
    await redis_client.close()

app = FastAPI(lifespan=lifespan)

app.include_router(health_router)