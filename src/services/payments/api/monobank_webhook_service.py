from datetime import datetime
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession
from src.database.db_methods.payment import confirm_payment_by_code


async def handle_monobank_webhook(session: AsyncSession, body: dict) -> bool:
    try:
        statement_item = body.get("data", {}).get("statementItem", {})
        comment = statement_item.get("comment", "").strip()

        if not comment:
            logger.info("⚠️ Немає коментарю ")
            return False

        amount = statement_item.get("amount", 0) / 100
        paid_at = datetime.now()

        result = await confirm_payment_by_code(session, code=comment, amount=amount, paid_at=paid_at)
        return result
    except Exception as e:
        logger.error(f"❌ Error in webhook handler: {e}")
        return False
