from fastapi import APIRouter, Request
from aiogram.types import Update

from infrastructure.services.TelegramBotServices import TelegramBotServices

fastapi_router = APIRouter()


@fastapi_router.post("/telegram/webhook")
async def telegram_webhook(request: Request):
    update = Update(**await request.json())
    bot_service = TelegramBotServices()
    await bot_service.dispatcher.feed_update(bot_service.bot, update)
    return {"ok": True}


