from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

import crud, schemas
from database import get_db

router = APIRouter(prefix="/rewards", tags=["Rewards"])


@router.post("/", response_model=schemas.RewardOut)
async def create_reward(reward: schemas.RewardCreate, db: AsyncSession = Depends(get_db)):
    return await crud.create_reward(
        db,
        reward.program_id,
        reward.name,
        reward.points_cost,
        reward.quantity,
        reward.description
    )


@router.post("/redeem")
async def redeem_reward(wallet_id: int, reward_id: int, db: AsyncSession = Depends(get_db)):
    try:
        result = await crud.redeem_reward(db, wallet_id, reward_id)
        return {
            "status": "success",
            "wallet_balance": int(result["wallet"].balance_points),
            "reward": result["reward"].name,
            "transaction_id": result["transaction"].transaction_id,
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

