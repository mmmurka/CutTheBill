from fastapi import APIRouter, Request, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import JSONResponse

from src.configs.db_conf import get_async_session
from src.services.payments.api.monobank_webhook_service import handle_monobank_webhook

router = APIRouter()


@router.post("/")
async def monobank_webhook(
    request: Request,
    session: AsyncSession = Depends(get_async_session),
):
    body = await request.json()
    success = await handle_monobank_webhook(session, body)
    return JSONResponse(content={"status": "ok" if success else "skipped"})

@router.get("/")
async def monobank_get():
    return JSONResponse(content={"status": "ok"})
