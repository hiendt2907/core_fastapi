from pydantic import BaseModel, EmailStr
from enum import Enum
from typing import List, Optional

# Member
class MemberCreate(BaseModel):
    username: str
    email: str
    phone: str
    password: str

class MemberOut(BaseModel):
    member_id: int
    username: str
    email: EmailStr
    phone: str
    kyc_status: str
    wallet_id: Optional[int] = None

    model_config = {"from_attributes": True}

class MemberLoginOut(BaseModel):
    member_id: int
    username: str
    email: EmailStr
    phone: str
    password: str  # cần để bcrypt.compare()
    kyc_status: str

    model_config = {"from_attributes": True}

# Wallet
class WalletOut(BaseModel):
    wallet_id: int
    member_id: int
    balance_points: int

    model_config = {"from_attributes": True}

# Transaction
class TransactionType(str, Enum):
    earn = "earn"
    redeem = "redeem"
    adjust = "adjust"
    bonus = "bonus"
    donate = "donate"
    refund = "refund"
    other = "other"

class TransactionCreate(BaseModel):
    wallet_id: int
    trans_type: TransactionType
    points: int
    description: Optional[str] = None

class TransactionOut(BaseModel):
    transaction_id: int
    wallet_id: int
    trans_type: TransactionType
    points: int
    description: Optional[str]

    model_config = {"from_attributes": True}

# Loyalty Program
class ProgramCreate(BaseModel):
    name: str
    description: Optional[str] = None
    merchant_id: Optional[int] = None

class ProgramOut(BaseModel):
    program_id: int
    name: str
    description: Optional[str]
    merchant_id: Optional[int]

    model_config = {"from_attributes": True}

# Reward
class RewardCreate(BaseModel):
    program_id: int
    name: str
    description: Optional[str] = None
    points_cost: int
    quantity: int

class RewardOut(BaseModel):
    reward_id: int
    program_id: int
    name: str
    description: Optional[str]
    points_cost: int
    quantity: int

    model_config = {"from_attributes": True}

# Membership
class MembershipCreate(BaseModel):
    member_id: int
    program_id: int

class MembershipOut(BaseModel):
    membership_id: int
    member_id: int
    program_id: int

    model_config = {"from_attributes": True}

# Admin login
class AdminKeyLogin(BaseModel):
    access_key: str
    secret_key: str

class TokenOut(BaseModel):
    access_token: str

# Member List (for listing users)
class MemberListOut(BaseModel):
    count: int
    members: List[MemberOut]

class LoginRequest(BaseModel):
    username: str
    password: str
