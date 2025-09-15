from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from passlib.context import CryptContext
from typing import Optional
import models

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

# ---------------- Member ----------------
async def create_member(db: AsyncSession, username: str, email: str, phone: str, password: str):
    hashed_password = get_password_hash(password)

    new_member = models.Member(
        username=username,
        email=email,
        phone=phone,
        password=hashed_password,
        kyc_status="pending"
    )
    db.add(new_member)
    await db.flush()

    new_wallet = models.Wallet(
        member_id=new_member.member_id,
        balance_points=0
    )
    db.add(new_wallet)
    await db.commit()

    await db.refresh(new_member)
    await db.refresh(new_wallet)
    setattr(new_member, "wallet_id", new_wallet.wallet_id)
    return new_member

async def get_member(db: AsyncSession, member_id: int):
    res = await db.execute(select(models.Member).where(models.Member.member_id == member_id))
    return res.scalar_one_or_none()

async def get_member_by_username(db: AsyncSession, username: str):
    res = await db.execute(select(models.Member).where(models.Member.username == username))
    return res.scalar_one_or_none()

# ---------------- Wallet ----------------
async def create_wallet(db: AsyncSession, member_id: int):
    wallet = models.Wallet(member_id=member_id, balance_points=0)
    db.add(wallet)
    await db.commit()
    await db.refresh(wallet)
    return wallet

async def get_wallet(db: AsyncSession, wallet_id: int):
    res = await db.execute(select(models.Wallet).where(models.Wallet.wallet_id == wallet_id))
    return res.scalar_one_or_none()

async def get_wallet_by_member(db: AsyncSession, member_id: int):
    res = await db.execute(select(models.Wallet).where(models.Wallet.member_id == member_id))
    return res.scalar_one_or_none()

# ---------------- Transaction ----------------
async def create_transaction(db: AsyncSession, wallet_id: int, trans_type: str, points: int, description: Optional[str] = None):
    stmt = select(models.Wallet).where(models.Wallet.wallet_id == wallet_id).with_for_update()
    wallet = (await db.execute(stmt)).scalar_one_or_none()
    if not wallet:
        raise Exception("Wallet not found")

    limit = (await db.execute(select(models.TransactionLimit).where(models.TransactionLimit.wallet_id == wallet_id))).scalar_one_or_none()
    if limit and points > int(limit.per_tx_limit):
        raise Exception("Exceeds per-transaction limit")

    if trans_type == "earn":
        wallet.balance_points += points
    elif trans_type in ("spend", "redeem"):
        if wallet.balance_points < points:
            raise Exception("Insufficient balance")
        wallet.balance_points -= points
        trans_type = "redeem"

    txn = models.Transaction(
        wallet_id=wallet_id,
        type=trans_type,
        trans_type=trans_type,
        points=points,
        description=description
    )
    db.add(txn)

    log = models.AuditLog(
        action="transaction",
        actor=f"wallet:{wallet_id}",
        details=f"{trans_type} {points} points"
    )
    db.add(log)

    await db.commit()
    await db.refresh(txn)
    return txn

# ---------------- Loyalty Program ----------------
async def create_program(db: AsyncSession, name: str, description: Optional[str] = None, merchant_id: Optional[int] = None):
    program = models.LoyaltyProgram(name=name, description=description, merchant_id=merchant_id)
    db.add(program)
    await db.commit()
    await db.refresh(program)
    return program

# ---------------- Reward ----------------
async def create_reward(db: AsyncSession, program_id: int, name: str, points_cost: int, quantity: int, description: Optional[str] = None):
    reward = models.Reward(
        program_id=program_id,
        name=name,
        points_cost=points_cost,
        quantity=quantity,
        description=description
    )
    db.add(reward)
    await db.commit()
    await db.refresh(reward)
    return reward

# ---------------- Membership ----------------
async def create_membership(db: AsyncSession, member_id: int, program_id: int):
    membership = models.Membership(member_id=member_id, program_id=program_id)
    db.add(membership)
    await db.commit()
    await db.refresh(membership)
    return membership

# ---------------- Redeem Reward ----------------
async def redeem_reward(db: AsyncSession, wallet_id: int, reward_id: int):
    wallet_stmt = select(models.Wallet).where(models.Wallet.wallet_id == wallet_id).with_for_update()
    reward_stmt = select(models.Reward).where(models.Reward.reward_id == reward_id).with_for_update()

    wallet = (await db.execute(wallet_stmt)).scalar_one_or_none()
    reward = (await db.execute(reward_stmt)).scalar_one_or_none()

    if not wallet:
        raise Exception("Wallet not found")
    if not reward:
        raise Exception("Reward not found")
    if wallet.balance_points < reward.points_cost:
        raise Exception("Insufficient points")
    if reward.quantity <= 0:
        raise Exception("Reward out of stock")

    wallet.balance_points -= reward.points_cost
    reward.quantity -= 1

    txn = models.Transaction(
        wallet_id=wallet_id,
        type="redeem",
        trans_type="redeem",
        points=reward.points_cost,
        description=f"Redeem reward {reward.name}"
    )
    db.add(txn)

    log = models.AuditLog(
        action="redeem",
        actor=f"wallet:{wallet_id}",
        details=f"Redeem {reward.name}"
    )
    db.add(log)

    await db.commit()
    await db.refresh(txn)
    return {"wallet": wallet, "reward": reward, "transaction": txn}

