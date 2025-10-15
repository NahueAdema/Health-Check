from fastapi import Depends, HTTPException, Request, status
from deps import RedisDep

async def validate_token(request: Request, redis: RedisDep):
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing token"
        )
    
    token = auth_header.split("Bearer ")[1].strip()
    exists = await redis.exists(f"token:{token}")
    if not exists:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing token"
        )
    return token