from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

import crud, schemas, models
from database import get_db

router = APIRouter(prefix="/members", tags=["Members"])


@router.post("/", response_model=schemas.MemberOut)
async def create_member(member: schemas.MemberCreate, db: AsyncSession = Depends(get_db)):
    # Check unique
    exists_username = await db.scalar(select(models.Member).where(models.Member.username == member.username))
    if exists_username:
        raise HTTPException(status_code=400, detail="Username đã tồn tại")

    exists_email = await db.scalar(select(models.Member).where(models.Member.email == member.email))
    if exists_email:
        raise HTTPException(status_code=400, detail="Email đã tồn tại")

    exists_phone = await db.scalar(select(models.Member).where(models.Member.phone == member.phone))
    if exists_phone:
        raise HTTPException(status_code=400, detail="Số điện thoại đã tồn tại")

    return await crud.create_member(db, member.username, member.email, member.phone, member.password)


@router.get("/{member_id}", response_model=schemas.MemberOut)
async def get_member(member_id: int, db: AsyncSession = Depends(get_db)):
    db_member = await crud.get_member(db, member_id)
    if not db_member:
        raise HTTPException(status_code=404, detail="Member not found")
    return db_member


@router.get("/by-username/{username}", response_model=schemas.MemberLoginOut)
async def get_member_by_username(username: str, db: AsyncSession = Depends(get_db)):
    db_member = await crud.get_member_by_username(db, username)
    if not db_member:
        raise HTTPException(status_code=404, detail="Member not found")
    return db_member

