from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from infrastructure.config.Configuration import Configuration
from utils import singleton
from infrastructure.controllers.TelegramController import telegram_router


@singleton
class TelegramBotServices:

    def __init__(self):
        Configuration.validate()

        self.bot = Bot(
            token=Configuration.TELEGRAM_BOT_TOKEN,
            default=DefaultBotProperties(parse_mode=ParseMode.HTML)
        )

        self.dispatcher = Dispatcher()
        self.dispatcher.include_router(telegram_router)

    def get_bot(self) -> Bot:
        return self.bot

    def get_dispatcher(self) -> Dispatcher:
        return self.dispatcher

    async def startup(self, webhook_url: str):
        await self.bot.set_webhook(webhook_url)

    async def shutdown(self):
        await self.bot.delete_webhook()
