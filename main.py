from contextlib import asynccontextmanager
from fastapi import FastAPI

from infrastructure.config.Configuration import Configuration
from infrastructure.bot_instance import bot_service
from infrastructure.controllers import telegram_router, fastapi_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: set webhook
    Configuration.validate()
    webhook_url = Configuration.WEBHOOK_URL
    await bot_service.startup(webhook_url)
    yield

    await bot_service.shutdown()

app = FastAPI(title="Chat Telegram Service", lifespan=lifespan)

# Register aiogram router with dispatcher
bot_service.dispatcher.include_router(telegram_router)

# Include FastAPI router for webhook endpoint
app.include_router(fastapi_router)
