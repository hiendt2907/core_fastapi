from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

import crud, schemas
from database import get_db

router = APIRouter(prefix="/transactions", tags=["Transactions"])


@router.post("/", response_model=schemas.TransactionOut)
async def create_transaction(txn: schemas.TransactionCreate, db: AsyncSession = Depends(get_db)):
    try:
        return await crud.create_transaction(
            db,
            wallet_id=txn.wallet_id,
            trans_type=txn.trans_type.value,
            points=txn.points,
            description=txn.description
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

