from fastapi import FastAPI

from src.services.payments.api import monobank_webhook

app = FastAPI()
app.include_router(monobank_webhook.router)
