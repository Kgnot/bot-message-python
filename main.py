from contextlib import asynccontextmanager
from fastapi import FastAPI

from infrastructure.config.Configuration import Configuration
from infrastructure.controllers.telegram.WebhookTelegram import fastapi_router
from infrastructure.services.bot_services import TelegramBotServices


bot_service = TelegramBotServices()

@asynccontextmanager
async def lifespan(app: FastAPI):
    await bot_service.startup(Configuration.WEBHOOK_URL)
    yield
    await bot_service.shutdown()

app = FastAPI(lifespan=lifespan)
app.include_router(fastapi_router)
