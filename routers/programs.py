from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

import crud, schemas
from database import get_db

router = APIRouter(prefix="/programs", tags=["Programs"])


@router.post("/", response_model=schemas.ProgramOut)
async def create_program(program: schemas.ProgramCreate, db: AsyncSession = Depends(get_db)):
    return await crud.create_program(db, program.name, program.description, program.merchant_id)

