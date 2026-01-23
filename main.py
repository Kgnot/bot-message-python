from contextlib import asynccontextmanager
from fastapi import FastAPI

from infrastructure.services.TelegramBotServices import TelegramBotServices
from infrastructure.controllers import telegram_router

# Initialize bot service
bot_service = TelegramBotServices()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: register webhook and set it
    bot_service.register_webhook(app)
    webhook_url = "https://yourdomain.com/telegram/webhook"  # TODO: Make configurable (e.g., from env)
    await bot_service.startup(webhook_url)

    yield

    # Shutdown: remove webhook
    await bot_service.shutdown()

app = FastAPI(title="Chat Telegram Service", lifespan=lifespan)

# Register aiogram router with dispatcher
bot_service.dispatcher.include_router(telegram_router)
