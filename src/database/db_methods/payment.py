import datetime

from loguru import logger
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import Payment

async def add_payment(session: AsyncSession, linked_service_id: int, amount: float):
    last_payment = datetime.datetime.now()
    next_payment = last_payment + datetime.timedelta(days=30)

    payment = Payment(linked_service_id=linked_service_id, amount=amount, last_payment=last_payment, next_payment=next_payment)
    session.add(payment)
    await session.commit()
    logger.info(f"Payment with id: {payment.id} added to database")
    return payment

async def update_payment_price(session: AsyncSession, payment_id: int, amount: float):
    result = await session.execute(select(Payment).where(Payment.id == payment_id))
    payment_obj = result.scalars().first()
    if not payment_obj:
        logger.error(f"Payment with id: {payment_id} not found")
        return None

    payment_obj.amount = amount
    await session.commit()
    return payment_obj