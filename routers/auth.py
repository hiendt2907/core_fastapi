# /routers/auth.py
from fastapi import APIRouter, Depends, HTTPException, status, Form
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime, timedelta
from jose import jwt
from passlib.context import CryptContext
from typing import Optional
from schemas import LoginRequest
from config import settings
from database import get_db
import models, schemas, crud
#from auth import create_access_token

router = APIRouter(prefix="/auth", tags=["Auth"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.JWT_SECRET, algorithm=ALGORITHM)


# ----- Admin token (access_key + secret_key) -----
@router.post("/token", response_model=schemas.TokenOut)
async def get_admin_token(payload: schemas.AdminKeyLogin, db: AsyncSession = Depends(get_db)):
    q = select(models.AdminKey).where(models.AdminKey.access_key == payload.access_key)
    res = await db.execute(q)
    admin = res.scalar_one_or_none()
    if not admin or admin.secret_key != payload.secret_key:
        # do not reveal which part failed
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token({"access_key": admin.access_key, "role": "admin"})
    return {"access_token": token}


# ----- Member token (username + password via OAuth2 form) -----

@router.post("/gettoken")
async def login_for_access_token(data: LoginRequest, db: AsyncSession = Depends(get_db)):
    user = await crud.get_member_by_username(db, data.username)
    if not user or not crud.pwd_context.verify(data.password, user.password):
        return {"error": "Invalid credentials"}

    token = create_access_token({"sub": str(user.member_id)})
    return {"access_token": token, "token_type": "bearer"}
