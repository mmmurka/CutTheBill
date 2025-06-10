
from loguru import logger
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import Admin


async def add_admin(session: AsyncSession, telegram_id: int):
    result = await session.execute(select(Admin).where(Admin.telegram_id == telegram_id))
    admin_obj = result.scalars().first()
    if admin_obj:
        logger.info(f"Admin with telegram id: {telegram_id} already exists")
        return admin_obj

    admin = Admin(telegram_id=telegram_id)
    session.add(admin)
    await session.commit()
    logger.info(f"Admin with {telegram_id} added to database")
    return admin

async def get_all_admins(session: AsyncSession):
    result = await session.execute(select(Admin))
    return result.scalars().all()
