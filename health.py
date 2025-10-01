# health.py
from fastapi import APIRouter, Request
from datetime import datetime, timezone
from fastapi.responses import JSONResponse
import json
import uuid

router = APIRouter()

@router.get("/health", summary="Health check", tags=["Health"])
async def health_check(request: Request):
    client_ip = request.client.host if request.client else "unknown"
    user_agent = request.headers.get("user-agent", "unknown")
    timestamp = datetime.now(timezone.utc).isoformat()

    log_entry = {
        "ip": client_ip,
        "user_agent": user_agent,
        "timestamp": timestamp,
        "endpoint": "/health"
    }

    from main import redis_client
    log_id = str(uuid.uuid4())
    await redis_client.setex(f"health_log:{log_id}", 3600, json.dumps(log_entry))

    return JSONResponse(
        status_code=200,
        content={
            "status": "ok",
            "timestamp": timestamp
        }
    )



@router.get("/ping", summary="Ping endpoint", tags=["Health"])
async def ping(request: Request):
    
    client_ip = request.client.host if request.client else "unknown"
    user_agent = request.headers.get("user-agent", "unknown")
    timestamp = datetime.now(timezone.utc).isoformat()

    log_entry = {
        "ip": client_ip,
        "user_agent": user_agent,
        "timestamp": timestamp,
        "endpoint": "/ping"
    }

    from main import redis_client
    log_id = str(uuid.uuid4())
    await redis_client.setex(f"health_log:{log_id}", 3600, json.dumps(log_entry))

    return JSONResponse(
        status_code=200,
        content={
            "message": "pong",
            "timestamp": timestamp
        }
    )