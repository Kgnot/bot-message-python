import uuid
from datetime import datetime
from typing import Union

from application.services import ConversationManager
from domain.models import Conversation, Message, User
from infrastructure.session_store import InMemoryConversationStore
from utils import singleton


@singleton
class ConversationServiceController:
    instance = None

    def __init__(self):
        self.conversationManager = ConversationManager()
        self.store = InMemoryConversationStore()
        ## Aquí implementamos el conversation store en el manager, aunque el main debería encargarse creo
        self.conversationManager.store = self.store

    def handle_message(self, user: User, message: Message) -> Conversation:
        now = datetime.now()

        conversation = self.store.get_by_user(user)

        if not conversation:
            conversation = Conversation(user, now)
            print("Empezamos de nuevo yei")
        if conversation.is_expired(datetime.now()):
            self.conversationManager.deleteByUser(user)
            # Si expiro generamos otra conversación
            print("la conversación expiro y le daremos otro lugar")
            conversation = Conversation(user, now)

        conversation.addMessage(message, now)

        self.store.save(conversation)

        return conversation