# core_fastapi/main.py
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text

from config import settings
from database import engine, Base
from routers import (
    auth,
    admin,
    members,
    wallets,
    transactions,
    programs,
    rewards,
    memberships,
)

app = FastAPI(
    title="LYTNW Core API",
    description="Loyalty platform API",
    version="1.0.0",
)

# CORS (dev only: allow all; restrict in prod)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"] if settings.APP_ENV == "dev" else ["https://your-frontend.example"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(admin.router)
app.include_router(members.router)
app.include_router(wallets.router)
app.include_router(transactions.router)
app.include_router(programs.router)
app.include_router(rewards.router)
app.include_router(memberships.router)

@app.on_event("startup")
async def on_startup():
    """
    Create schemas & tables only in dev mode.
    In production, use Alembic migrations instead.
    """
    if settings.APP_ENV == "dev":
        async with engine.begin() as conn:
            # Create schemas if not exist
            schemas = [
                "member", "wallet", "transaction",
                "program", "reward", "common", "merchant"
            ]
            for schema in schemas:
                await conn.execute(text(f"CREATE SCHEMA IF NOT EXISTS {schema}"))

            # Create tables
            await conn.run_sync(Base.metadata.create_all)

@app.get("/", tags=["Health"])
async def health_check():
    return {"status": "ok", "env": settings.APP_ENV}
