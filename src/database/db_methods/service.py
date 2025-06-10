from loguru import logger
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import Service


async def add_service(session: AsyncSession, name: str, subscription_price: float, user_price: float):
    result = await session.execute(select(Service).where(Service.name == name))
    service_obj = result.scalars().first()
    if service_obj:
        logger.info(f"Service with name: {name} already exists")
        return service_obj

    service = Service(name=name, subscription_price=subscription_price, user_price=user_price)
    session.add(service)
    await session.commit()
    logger.info(f"Service with name: {name} added to database")
    return service

async def get_all_services(session: AsyncSession):
    result = await session.execute(select(Service))
    return result.scalars().all()

async def update_service_price(session: AsyncSession, service_name: str, user_price: float = None, subscription_price: float = None):
    result = await session.execute(select(Service).where(Service.name == service_name))
    service_obj = result.scalars().first()
    if not service_obj:
        logger.info(f"Service with name: {service_name} not found")
        return None

    if user_price is not None:
        service_obj.user_price = user_price
    if subscription_price is not None:
        service_obj.subscription_price = subscription_price

    await session.commit()
    logger.info(f"Service with name: {service_name} updated in database")
    return service_obj

async def get_service(session: AsyncSession, service_name: str):
    result = await session.execute(select(Service).where(Service.name == service_name))
    return result.scalars().first()