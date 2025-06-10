from loguru import logger
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import Group


async def create_group(session: AsyncSession, group_name: str, service_id: int, max_slots: int, free_slots: int, admin_email: str):
    result = await session.execute(select(Group).where(Group.group_name == group_name))
    group_obj = result.scalars().first()
    if group_obj:
        logger.error(f"Group with name: {group_name} already exists")
        return "group exists"
    group = Group(group_name=group_name, service_id=service_id, max_slots=max_slots, free_slots=free_slots, admin_email=admin_email)
    session.add(group)
    await session.commit()
    return group

async def get_group(session: AsyncSession, group_name: str):
    result = await session.execute(select(Group).where(Group.group_name == group_name))
    return result.scalars().first()

async def get_all_groups(session: AsyncSession):
    result = await session.execute(select(Group))
    return result.scalars().all()

async def delete_group(session: AsyncSession, group_name: str):
    result = await session.execute(select(Group).where(Group.group_name == group_name))
    group_obj = result.scalars().first()
    if not group_obj:
        logger.error(f"Group with name: {group_name} not found")
        return None
    await session.delete(group_obj)
    await session.commit()
    return group_obj
