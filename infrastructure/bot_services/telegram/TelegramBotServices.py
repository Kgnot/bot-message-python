from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from application.ports.out import MessagingPort
from infrastructure.config.Configuration import Configuration
from infrastructure.controllers.telegram.router import telegram_router
from utils import singleton

@singleton
class TelegramBotServices(MessagingPort):

    def __init__(self):
        Configuration.validate()

        self.bot = Bot(
            token=Configuration.TELEGRAM_BOT_TOKEN,
            default=DefaultBotProperties(parse_mode=ParseMode.HTML)
        )

        self.dispatcher = Dispatcher()
        self.dispatcher.include_router(telegram_router)

    async def startup(self, webhook_url: str):
        await self.bot.set_webhook(webhook_url)

    async def shutdown(self):
        await self.bot.delete_webhook()

    async def send_text(self, chat_id: str, text: str):
        await self.bot.send_message(chat_id, text)
