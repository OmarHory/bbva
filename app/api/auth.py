from datetime import datetime, timedelta
from fastapi import APIRouter, HTTPException, status, Header
from jose import jwt
from pydantic import BaseModel
from app.auth.security import SECRET_KEY, ALGORITHM
import logging
from typing import Optional

logger = logging.getLogger("api.auth")

auth_router = APIRouter()

class AccessRequest(BaseModel):
    expires_in_hours: Optional[int] = 24

class AccessToken(BaseModel):
    access_token: str
    token_type: str
    expires_at: datetime

@auth_router.post("/access", response_model=AccessToken)
async def generate_access_token(
    request: AccessRequest, 
    x_api_key: str = Header(..., description="Secret API key")
):
    """
    Generate a JWT access token using the secret key
    
    This endpoint requires the secret key to be passed in the X-API-Key header.
    The secret key should only be shared with trusted clients.
    """
    if x_api_key != SECRET_KEY:
        logger.warning(f"Invalid secret key attempt")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid secret key"
        )
    
    expires_delta = timedelta(hours=request.expires_in_hours)
    expire = datetime.utcnow() + expires_delta
    
    to_encode = {"exp": expire}
    
    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    
    logger.info(f"Generated JWT access token")
    return {
        "access_token": token,
        "token_type": "bearer",
        "expires_at": expire
    }