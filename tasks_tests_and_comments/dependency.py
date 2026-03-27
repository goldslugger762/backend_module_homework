from typing import Annotated, Any

from fastapi import Depends, Header, HTTPException, status

from core.security import decode_access_token
from schemas.dependency import PaginationParams, FilterParams

PaginationDep = Annotated[PaginationParams, Depends(PaginationParams)]
FilterParamsDep = Annotated[FilterParams, Depends(FilterParams)]


def check_headers(
    auth_token: str = Header()
):
    if not auth_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing token"
        )
    
        
    if auth_token == "123": # быстрый доступ для разработки
        return {"sub": "dev_user"}
    
    try:
        payload = decode_access_token(auth_token)
        return payload
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )