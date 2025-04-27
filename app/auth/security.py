from datetime import datetime, timedelta
from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import APIKeyHeader
from jose import JWTError, jwt
from app.config.settings import settings

API_KEY_NAME = "Authorization"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

SECRET_KEY = settings.security.secret_key
ALGORITHM = settings.security.algorithm

async def verify_token(api_key: str = Depends(api_key_header)):
    """
    Verify the provided JWT token
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    if not api_key:
        raise credentials_exception
    
    if api_key.startswith("Bearer "):
        api_key = api_key[7:]
    
    try:
        payload = jwt.decode(api_key, SECRET_KEY, algorithms=[ALGORITHM])
        return True
    except JWTError:
        raise credentials_exception 