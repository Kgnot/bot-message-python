from fastapi import APIRouter, Request
from aiogram import Router
from aiogram.types import Message, Update
from datetime import datetime

from application.services import ConversationServiceController
from domain.models import User, Conversation
from infrastructure.mapper import telegram_to_domain_message, telegram_user_mapper
from infrastructure.bot_instance import bot_service

fastapi_router = APIRouter()
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

# FastAPI endpoint for webhook
@fastapi_router.post("/telegram/webhook")
async def telegram_webhook(request: Request):
    data = await request.json()
    update = Update(**data)
    await bot_service.dispatcher.process_update(update)
    return {"status": "ok"}