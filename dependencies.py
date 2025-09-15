# core_fastapi/dependencies.py
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError

from config import settings

# tokenUrl should point to the primary token endpoint (admin token here)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


def get_current_payload(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=["HS256"])
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")


def admin_required(payload: dict = Depends(get_current_payload)):
    if payload.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Forbidden")
    return payload


def member_required(payload: dict = Depends(get_current_payload)):
    if payload.get("role") != "member":
        raise HTTPException(status_code=403, detail="Forbidden")
    return payload

