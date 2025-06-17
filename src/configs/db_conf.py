from typing import AsyncGenerator, Final

from sqlalchemy import Engine, create_engine
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import sessionmaker

from src.constants import DB_HOST, DB_NAME, DB_PASS, DB_PORT, DB_USER

# =============================================== ASYNC FastAPI Session ===============================================

ASYNC_DATABASE_URL: Final = (
    f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

async_engine: AsyncEngine = create_async_engine(
    ASYNC_DATABASE_URL,
    echo=False,
    echo_pool=True,
    future=True,
    pool_pre_ping=False,
    pool_size=10,
    max_overflow=50,
    pool_timeout=120,
    pool_recycle=600,
)

AsyncSessionFactory = async_sessionmaker(
    bind=async_engine, expire_on_commit=False, autoflush=False
)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionFactory() as session:
        try:
            yield session
        except Exception as e:
            raise e
        finally:
            await session.close()


# =============================================== SYNC Celery Session ===============================================

SYNC_DATABASE_URL: Final = (
    f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

sync_engine: Engine = create_engine(
    SYNC_DATABASE_URL,
    echo=False,
    echo_pool=True,
    future=True,
    pool_pre_ping=False,
    pool_size=10,
    max_overflow=50,
    pool_timeout=120,
    pool_recycle=300,
)

SyncSessionFactory = sessionmaker(
    bind=sync_engine, expire_on_commit=False, autoflush=False
)
