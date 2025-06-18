from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from src.configs.db_conf import ASYNC_DATABASE_URL

engine = create_async_engine(ASYNC_DATABASE_URL, echo=True)

async_session = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


@asynccontextmanager
async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session
