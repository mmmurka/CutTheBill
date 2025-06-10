from loguru import logger
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.database.db_methods import user, service
from src.database.models import LinkedService


async def create_linked_service(session: AsyncSession, user_id: int, service_id: int):
    result = await session.execute(select(LinkedService).where(LinkedService.user_id == user_id).where(LinkedService.service_id == service_id))
    linked_service_obj = result.scalars().first()
    if linked_service_obj:
        logger.error(f"Linked service with user_id: {user_id} and service_id: {service_id} already exists")
        return "user exists"
    linked_service = LinkedService(user_id=user_id, service_id=service_id)
    session.add(linked_service)
    await session.commit()
    return linked_service

async def link_user_to_service(session: AsyncSession, telegram_id, service_name):
    user_id = (await user.get_user(session, telegram_id)).id
    service_id = (await service.get_service(session, service_name)).id
    return await create_linked_service(session, user_id, service_id)


async def unlink_user_from_service(session: AsyncSession, telegram_id, service_name):
    user_id = (await user.get_user(session, telegram_id)).id
    service_id = (await service.get_service(session, service_name)).id
    result = await session.execute(select(LinkedService).where(LinkedService.user_id == user_id).where(LinkedService.service_id == service_id))
    linked_service_obj = result.scalars().first()
    if not linked_service_obj:
        logger.error(f"Linked service with user_id: {user_id} and service_id: {service_id} not found")
        return None
    await session.delete(linked_service_obj)
    await session.commit()
    return linked_service_obj
