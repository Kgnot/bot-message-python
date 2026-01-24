from aiogram import Router
from aiogram.types import Message

from application.services import ConversationServiceController
from infrastructure.mapper import telegram_to_domain_message, telegram_user_mapper

telegram_router = Router()
conversationServiceController = ConversationServiceController()

# Esto se usa en: TelegramBotServices. Le decimos al dispatcher que routee la respuesta de esta forma
@telegram_router.message()
async def handle_message(message: Message):
    user = telegram_user_mapper(message)
    domain_message = telegram_to_domain_message(message)

    conversationServiceController.handle_message(user, domain_message)

    await message.reply("Message received 🚀")

