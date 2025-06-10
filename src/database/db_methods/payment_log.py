from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import PaymentLog


async def add_log(session: AsyncSession, payment_id: int, amount: float, paid_at: datetime):
    log = PaymentLog(payment_id=payment_id, amount=amount, paid_at=paid_at)
    session.add(log)
    await session.commit()
    return log

async def get_payment_logs(session: AsyncSession, payment_id: int):
    result = await session.execute(select(PaymentLog).where(PaymentLog.payment_id == payment_id))
    return result.scalars().all()