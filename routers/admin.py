from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from dependencies import admin_required
from database import get_db
import models, schemas

router = APIRouter(prefix="/admin", tags=["Admin"])


@router.get("/members", response_model=schemas.MemberListOut, dependencies=[Depends(admin_required)])
async def list_members(
    db: AsyncSession = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
):
    result = await db.execute(
        select(models.Member).offset(skip).limit(limit)
    )
    members = result.scalars().all()

    total = await db.execute(select(func.count()).select_from(models.Member))
    count = total.scalar_one()

    return {"count": count, "members": members}

