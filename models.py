# models.py
from sqlalchemy import Column, Integer, String, BigInteger, ForeignKey, TIMESTAMP, Text, DateTime
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import ENUM
from database import Base
from datetime import datetime

# Member
class Member(Base):
    __tablename__ = "members"
    __table_args__ = {'schema': 'member'}
    member_id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False, index=True)
    email = Column(String, unique=True, nullable=False, index=True)
    phone = Column(String(20), unique=True, nullable=True, index=True)
    password = Column(String(255), nullable=False)
    kyc_status = Column(String, default="pending")
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

# Wallet
class Wallet(Base):
    __tablename__ = "wallets"
    __table_args__ = {'schema': 'wallet'}
    wallet_id = Column(Integer, primary_key=True, index=True)
    member_id = Column(Integer, ForeignKey("member.members.member_id", ondelete="CASCADE"), index=True)
    balance_points = Column(BigInteger, default=0)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

# Transaction
TransTypeEnum = ENUM(
    'earn', 'redeem', 'transfer', 'adjust', 'donate', 'bonus', 'refund', 'other',
    name='trans_type_enum',
    create_type=True
)

class Transaction(Base):
    __tablename__ = "transactions"
    __table_args__ = {'schema': 'transaction'}
    transaction_id = Column(Integer, primary_key=True, index=True)
    wallet_id = Column(Integer, ForeignKey("wallet.wallets.wallet_id", ondelete="CASCADE"), index=True)
    # Giữ cả hai field để tương thích ngược, nhưng sẽ chuẩn hóa dùng trans_type
    type = Column(String, nullable=True)  # legacy
    trans_type = Column(TransTypeEnum, nullable=False)
    points = Column(BigInteger, nullable=False)
    description = Column(Text)
    reference_id = Column(String)
    created_at = Column(TIMESTAMP, server_default=func.now())

# Loyalty Program
class LoyaltyProgram(Base):
    __tablename__ = "loyalty_programs"
    __table_args__ = {'schema': 'program'}
    program_id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(Text)
    merchant_id = Column(Integer, ForeignKey("merchant.merchants.merchant_id", ondelete="SET NULL"))
    start_date = Column(TIMESTAMP)
    end_date = Column(TIMESTAMP)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

# Reward
class Reward(Base):
    __tablename__ = "rewards"
    __table_args__ = {'schema': 'reward'}
    reward_id = Column(Integer, primary_key=True, index=True)
    program_id = Column(Integer, ForeignKey("program.loyalty_programs.program_id", ondelete="CASCADE"), index=True)
    name = Column(String, nullable=False)
    description = Column(Text)
    points_cost = Column(BigInteger, nullable=False)
    quantity = Column(Integer, default=0)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

# Membership
class Membership(Base):
    __tablename__ = "memberships"
    __table_args__ = {'schema': 'program'}
    membership_id = Column(Integer, primary_key=True, index=True)
    member_id = Column(Integer, ForeignKey("member.members.member_id", ondelete="CASCADE"), index=True)
    program_id = Column(Integer, ForeignKey("program.loyalty_programs.program_id", ondelete="CASCADE"), index=True)
    joined_at = Column(TIMESTAMP, server_default=func.now())

class Tier(Base):
    __tablename__ = "tiers"
    __table_args__ = {'schema': 'program'}
    tier_id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    earn_multiplier = Column(Integer, default=1)
    spend_multiplier = Column(Integer, default=1)

class TransactionLimit(Base):
    __tablename__ = "transaction_limits"
    __table_args__ = {'schema': 'transaction'}
    limit_id = Column(Integer, primary_key=True)
    wallet_id = Column(Integer, ForeignKey("wallet.wallets.wallet_id"), index=True)
    daily_limit = Column(BigInteger, default=10000)
    per_tx_limit = Column(BigInteger, default=5000)

class AuditLog(Base):
    __tablename__ = "audit_logs"
    __table_args__ = {'schema': 'common'}
    log_id = Column(Integer, primary_key=True)
    action = Column(String)
    actor = Column(String)
    details = Column(Text)
    created_at = Column(TIMESTAMP, server_default=func.now())

# models.py
class AdminKey(Base):
    __tablename__ = "admin_keys"
    id = Column(Integer, primary_key=True)
    access_key = Column(String, unique=True, index=True)
    secret_key = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

class Merchant(Base):
    __tablename__ = "merchants"
    __table_args__ = {'schema': 'merchant'}
    merchant_id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True)
    created_at = Column(TIMESTAMP, server_default=func.now())

