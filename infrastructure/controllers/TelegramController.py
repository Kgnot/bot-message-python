from aiogram import Router
from aiogram.types import Message
from datetime import datetime

from application.services import ConversationServiceController
from domain.models import User, Conversation
from infrastructure.mapper import telegram_to_domain_message, telegram_user_mapper

telegram_router = Router()
# El servicio de la conversación
conversationServiceController = ConversationServiceController()

@telegram_router.message()  # Handle all messages
async def handle_message(message: Message):
    # Map to domain objects (now using aiogram Message)
    user: User = telegram_user_mapper(message)
    domain_message = telegram_to_domain_message(message)

    # Create/update conversation
    conversation = Conversation(user, datetime.now())
    conversation.addMessage(domain_message, datetime.now())
    conversationServiceController.add_conversation(conversation=conversation)

    # Optional: Send response back to Telegram
    await message.reply("Message received!")