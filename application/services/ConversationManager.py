import uuid
from datetime import datetime
from typing import Union

from application.errors import ConversationManagerError
from domain.models import Conversation, User
from domain.ports import ConversationSessionStore
from utils import singleton




@singleton
class ConversationManager:
    def __init__(self,):
        self._store:ConversationSessionStore = None

    def _validate_store_attached(self):
        # centralizamos el apartado de validación
        if not self._store:
            raise ConversationManagerError(
                "No se adjuntó un store de almacenamiento de conversaciones"
            )

    def create(self, user: User) -> Conversation:
        self._validate_store_attached()
        conversation = Conversation(
            user=user,
            started_at=datetime.now()
        )
        self._store.save(conversation)
        return conversation

    def getByUser(self, user: User) -> Union[Conversation, None]:
        self._validate_store_attached()
        return self._store.getByUser(user)

    def save(self, conversation: Conversation) -> None:
        self._validate_store_attached()
        self._store.save(conversation)

    def deleteByUser(self, user: User) -> None:
        self._validate_store_attached()
        self._store.deleteByUser(user)

    # apartado de accesibilidad
    @property
    def store(self) -> ConversationSessionStore:
        return self._store

    @store.setter
    def store(self, store: ConversationSessionStore):
        self._store = store