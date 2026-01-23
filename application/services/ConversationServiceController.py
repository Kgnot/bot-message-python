import uuid
from datetime import datetime

from application.services import ConversationManager
from domain.models import Conversation, Message
from infrastructure.session_store import InMemoryConversationStore
from utils import singleton


@singleton
class ConversationServiceController:
    instance = None

    def __init__(self):
        store = InMemoryConversationStore()
        self.conversationManager = ConversationManager(store)

    def add_conversation(self,conversation: Conversation):
        self.conversationManager.save(conversation) # guardamos la conversación

    def add_message_to_conversation(self,conversation_id: uuid.UUID, message: Message):
        # Añadimos el mensaje
        self.conversationManager.get(conversation_id).addMessage(message,datetime.now())