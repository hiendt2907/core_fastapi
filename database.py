from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import declarative_base
from sqlalchemy.ext.asyncio import AsyncAttrs
import os

SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")
if not SQLALCHEMY_DATABASE_URL:
    # fallback for dev only; prefer .env
    SQLALCHEMY_DATABASE_URL = "postgresql+asyncpg://postgres:JoKPQHLgXTBHpSxXXVlvFVBKgRRdYpBk@yamanote.proxy.rlwy.net:35479/railway"

engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL,
    echo=False,
    pool_pre_ping=True,
)

Base = declarative_base(cls=AsyncAttrs)

SessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

async def get_db():
    async with SessionLocal() as session:
        yield session
