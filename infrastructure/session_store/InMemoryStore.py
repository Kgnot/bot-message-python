import uuid
import time
from typing import Union

from domain.models import Conversation


class InMemoryConversationStore:
    def __init__(self, ttl_seconds: int = 300):
        self.ttl_seconds = ttl_seconds
        self._store: dict[uuid.UUID, tuple[Conversation, float]] = {} # La tupla, una es la conversacion y la otra es el tiempo.

    def get(self, conversation_id: uuid.UUID) -> Union[Conversation, None]:
        entry = self._store.get(conversation_id)
        if not entry:
            return None
        conversation, last_ts = entry
        if time.time() - last_ts > self.ttl_seconds:
            del self._store[conversation_id]
            return None
        return conversation

    def save(self, conversation: Conversation) -> None:
        self._store[conversation.id] = (conversation, time.time())

    def delete(self, conversation_id: uuid.UUID) -> None:
        self._store.pop(conversation_id, None)