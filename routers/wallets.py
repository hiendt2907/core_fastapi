from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

import crud, schemas, models
from database import get_db

router = APIRouter(prefix="/wallets", tags=["Wallets"])


@router.post("/", response_model=schemas.WalletOut)
async def create_wallet(member_id: int, db: AsyncSession = Depends(get_db)):
    member = await db.scalar(select(models.Member).where(models.Member.member_id == member_id))
    if not member:
        raise HTTPException(status_code=404, detail="Member not found")
    return await crud.create_wallet(db, member_id)


@router.get("/{wallet_id}", response_model=schemas.WalletOut)
async def get_wallet(wallet_id: int, db: AsyncSession = Depends(get_db)):
    wallet = await crud.get_wallet(db, wallet_id)
    if not wallet:
        raise HTTPException(status_code=404, detail="Wallet not found")
    return wallet


@router.get("/by-member/{member_id}", response_model=schemas.WalletOut)
async def get_wallet_by_member(member_id: int, db: AsyncSession = Depends(get_db)):
    wallet = await crud.get_wallet_by_member(db, member_id)
    if not wallet:
        raise HTTPException(status_code=404, detail="Wallet not found")
    return wallet


@router.post("/earn", response_model=schemas.TransactionOut)
async def earn_points(wallet_id: int, points: int, db: AsyncSession = Depends(get_db)):
    try:
        txn = await crud.create_transaction(db, wallet_id=wallet_id, trans_type="earn", points=points, description="Earned points")
        return txn
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

