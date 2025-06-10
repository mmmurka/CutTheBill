from loguru import logger
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import GroupUser


async def add_user_to_group(session: AsyncSession, user_id: int, group_id: int, email: str):
    result = await session.execute(select(GroupUser).where(GroupUser.user_id == user_id).where(GroupUser.group_id == group_id))
    group_user_obj = result.scalars().first()
    if group_user_obj:
        logger.error(f"User with user_id: {user_id} and group_id: {group_id} already exists")
        return "user already in group"
    group_user = GroupUser(user_id=user_id, group_id=group_id, email=email)
    session.add(group_user)
    await session.commit()
    return group_user

async def delete_user_from_group(session: AsyncSession, user_id: int, group_id: int):
    result = await session.execute(select(GroupUser).where(GroupUser.user_id == user_id).where(GroupUser.group_id == group_id))
    group_user_obj = result.scalars().first()
    if not group_user_obj:
        logger.error(f"User with user_id: {user_id} and group_id: {group_id} not found")
        return None
    await session.delete(group_user_obj)
    await session.commit()
    return group_user_obj