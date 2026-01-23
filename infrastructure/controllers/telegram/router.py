from aiogram import Router
from aiogram.types import Message
from datetime import datetime

from application.services import ConversationServiceController
from domain.models import Conversation
from infrastructure.mapper import telegram_to_domain_message, telegram_user_mapper

telegram_router = Router()
conversationServiceController = ConversationServiceController()

@telegram_router.message()
async def handle_message(message: Message):
    user = telegram_user_mapper(message)
    domain_message = telegram_to_domain_message(message)

    conversation = Conversation(user, datetime.now())
    conversation.addMessage(domain_message, datetime.now())

    conversationServiceController.add_conversation(conversation)
    await message.reply("Message received!")
