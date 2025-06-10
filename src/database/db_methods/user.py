from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from loguru import logger

from src.database.database import get_session
from src.database.models import User


async def create_user(
        session: AsyncSession,
        telegram_id: int,
        username: str = None):

    result = await session.execute(select(User).where(User.telegram_id == telegram_id))
    user_obj = result.scalars().first()
    if user_obj:
        if user_obj.username != username:
            user_obj.username = username
            logger.info(f"User {telegram_id} username changed to {username}")
            await session.commit()
        else:
            logger.info(f"User with telegram id: {telegram_id} already exists")
        return user_obj

    user = User(telegram_id=telegram_id, username=username)
    session.add(user)
    await session.commit()
    logger.info(f"User with {telegram_id} added to database")
    return user

async def get_all_users(session: AsyncSession):
    result = await session.execute(select(User))
    return result.scalars().all()

async def get_user(session: AsyncSession, telegram_id: int):
    result = await session.execute(select(User).where(User.telegram_id == telegram_id))
    return result.scalars().first()
