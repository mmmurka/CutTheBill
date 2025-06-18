from datetime import datetime

from loguru import logger
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.database.models import Payment, PaymentStatus, PaymentLog
from src.services.payments.functions import generate_payment_code


async def create_payment(session: AsyncSession, linked_service_id: int, amount: float) -> Payment:
    payment = Payment(
        linked_service_id=linked_service_id,
        amount=amount,
        status=PaymentStatus.WAITING,
        payment_code=generate_payment_code(),
    )
    try:
        session.add(payment)
        await session.commit()
        await session.refresh(payment)
        return payment
    except Exception as e:
        logger.error(f"Error creating payment: {e}")
        raise


async def update_payment(session: AsyncSession, payment_id: int, status: PaymentStatus):
    payment = await session.get(Payment, payment_id)
    if not payment:
        logger.warning(f"Payment not found: id={payment_id}")
        return None
    payment.status = status
    session.add(payment)
    await session.commit()
    await session.refresh(payment)
    return payment


async def get_payment_by_code(session: AsyncSession, code: str) -> Payment | None:
    stmt = (
        select(Payment)
        .where(Payment.payment_code == code)
        .options(selectinload(Payment.linked_service))
    )
    result = await session.execute(stmt)
    return result.scalars().first()


async def confirm_payment_by_code(session: AsyncSession, code: str, amount: float, paid_at: datetime) -> bool:
    payment = await get_payment_by_code(session, code)
    if not payment:
        logger.warning(f"❌ Payment not found for code: {code}")
        return False

    diff = abs(payment.amount - amount)
    if diff > 2:
        logger.warning(
            f"⚠️ Сума не збігається! Очікувалось {payment.amount}, отримано {amount} (code={code})"
        )
        return False

    payment.status = PaymentStatus.PAID
    session.add(payment)

    log = PaymentLog(payment_id=payment.id, amount=amount, paid_at=paid_at)
    session.add(log)

    await session.commit()

    logger.success(f"✅ Платіж підтверджено: {payment.id}, user={payment.linked_service.user_id}")
    return True


# Для ручного тесту
async def main():
    from src.configs.db_conf import get_async_session
    async for session in get_async_session():
        await create_payment(session, linked_service_id=1, amount=1)


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
