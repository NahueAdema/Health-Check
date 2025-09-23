from fastapi import APIRouter
from datetime import datetime
from fastapi.responses import JSONResponse

router = APIRouter()

@router.get("/health", summary="Health check", tags=["Health"])
def health_check():
    return JSONResponse(
        status_code=200,
        content={
            "status": "ok",
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }
    )
