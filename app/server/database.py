"""
Database connection and session management for Valargen server.
"""
import os
from typing import AsyncGenerator

import asyncpg
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.pool import NullPool

try:
    from app.server.config import settings
    from app.server.models import Base
except ModuleNotFoundError:
    from config import settings
    from models import Base


# Create async engine with proper connection pooling
engine = create_async_engine(
    settings.async_database_url,
    echo=settings.debug,
    poolclass=NullPool if os.getenv("TESTING") else None,
    future=True,
)

# Create async session factory
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency function that yields a database session.
    Used in FastAPI route dependencies.
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()


async def init_database() -> None:
    """
    Initialize database by creating all tables.
    Only used for testing or initial setup.
    In production, use Alembic migrations instead.
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def check_database_connection() -> dict:
    """Check if PostgreSQL database connection is successful."""
    database_url = os.getenv("DATABASE_URL")

    if not database_url:
        return {"status": "disconnected", "error": "DATABASE_URL not configured"}

    conn = None
    try:
        conn = await asyncpg.connect(database_url)
        return {"status": "connected", "database": "postgresql"}
    except Exception as e:
        return {"status": "disconnected", "error": str(e)}
    finally:
        if conn:
            await conn.close()
