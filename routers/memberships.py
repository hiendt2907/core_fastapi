from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

import crud, schemas
from database import get_db

router = APIRouter(prefix="/memberships", tags=["Memberships"])


@router.post("/", response_model=schemas.MembershipOut)
async def create_membership(membership: schemas.MembershipCreate, db: AsyncSession = Depends(get_db)):
    return await crud.create_membership(db, membership.member_id, membership.program_id)

