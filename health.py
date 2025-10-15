from fastapi import APIRouter, Request, Depends
from datetime import datetime, timezone
from fastapi.responses import JSONResponse
import json
import uuid
from deps import RedisDep
from auth.auth import validate_token 

router = APIRouter()

@router.get("/health", summary="Health check", tags=["Health"])
async def health_check(request: Request, redis: RedisDep):
    client_ip = request.client.host if request.client else "unknown"
    user_agent = request.headers.get("user-agent", "unknown")
    timestamp = datetime.now(timezone.utc).isoformat()

    log_entry = {
        "ip": client_ip,
        "user_agent": user_agent,
        "timestamp": timestamp,
        "endpoint": "/health"
    }

    log_id = str(uuid.uuid4())
    await redis.setex(f"health_log:{log_id}", 3600, json.dumps(log_entry))

    return JSONResponse(
        status_code=200,
        content={
            "status": "ok",
            "timestamp": timestamp
        }
    )

@router.get("/ping", summary="Ping endpoint", tags=["Health"])
async def ping(request: Request, redis: RedisDep):
    client_ip = request.client.host if request.client else "unknown"
    user_agent = request.headers.get("user-agent", "unknown")
    timestamp = datetime.now(timezone.utc).isoformat()

    log_entry = {
        "ip": client_ip,
        "user_agent": user_agent,
        "timestamp": timestamp,
        "endpoint": "/ping"
    }

    log_id = str(uuid.uuid4())
    await redis.setex(f"health_log:{log_id}", 3600, json.dumps(log_entry))

    return JSONResponse(
        status_code=200,
        content={
            "message": "pong",
            "timestamp": timestamp
        }
    )

@router.get("/get-responses", summary="Get all health/ping logs", tags=["Health"])
async def get_responses(
    redis: RedisDep,
    token: str = Depends(validate_token) 
):
    """
    Devuelve todos los registros guardados de /health y /ping.
    Requiere un token válido en el header Authorization.
    """
    keys = await redis.keys("health_log:*")
    
    responses = []
    for key in keys:
        data = await redis.get(key)
        if data:
            log_data = json.loads(data)
            log_data["id"] = key.split(":", 1)[1]
            responses.append(log_data)
    
    responses.sort(key=lambda x: x["timestamp"], reverse=True)
    
    return JSONResponse(
        status_code=200,
        content={
            "total": len(responses),
            "logs": responses
        }
    )