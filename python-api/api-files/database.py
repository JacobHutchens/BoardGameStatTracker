"""
Async database engine and session for FastAPI + SQLModel.
DATABASE_URL must be set (e.g. via .env: mysql+aiomysql://user:pass@host:3306/dbname).
"""
import os
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy import text

# Load from environment (call dotenv.load_dotenv() in app startup if using .env)
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "mysql+aiomysql://jacob:password@127.0.0.1:3306/BoardGameTracker",
)

engine = create_async_engine(
    DATABASE_URL,
    echo=os.getenv("SQL_ECHO", "0").lower() in ("1", "true", "yes"),
    pool_pre_ping=True,
)

async_session_maker = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """FastAPI dependency: yields an async DB session without auto-commit/rollback.

    Callers are responsible for committing or rolling back explicitly.
    """
    async with async_session_maker() as session:
        yield session


async def check_db_connection() -> bool:
    """Run a simple query to verify the database is reachable. Used by health check."""
    try:
        async with async_session_maker() as session:
            await session.execute(text("SELECT 1"))
        return True
    except Exception:
        return False
