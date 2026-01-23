from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.webhook.fastapi import SimpleRequestHandler
from fastapi import FastAPI

from infrastructure.config.Configuration import Configuration


class TelegramBotServices:

    def __init__(self):
        Configuration.validate()
        assert Configuration.TELEGRAM_BOT_TOKEN is not None  # Type guard after validation
        self.bot = Bot(
            token=Configuration.TELEGRAM_BOT_TOKEN,
            default=DefaultBotProperties(parse_mode=ParseMode.HTML)
        )
        self.dispatcher = Dispatcher()

    def register_webhook(self, app: FastAPI, webhook_path: str = "/telegram/webhook"):
        """Integrate aiogram webhook with FastAPI."""
        webhook_handler = SimpleRequestHandler(
            dispatcher=self.dispatcher,
            bot=self.bot,
            secret_token=None  # Optional: add for security
        )

        # Use add_api_route with methods for POST
        app.add_api_route(webhook_path, webhook_handler, methods=["POST"])

    async def startup(self, webhook_url: str):
        """Called on app startup to set webhook."""
        await self.bot.set_webhook(webhook_url)

    async def shutdown(self):
        """Called on app shutdown to remove webhook."""
        await self.bot.delete_webhook()
