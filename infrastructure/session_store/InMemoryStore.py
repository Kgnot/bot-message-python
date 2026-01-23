import uuid
import time
from typing import Union

from domain.models import Conversation, User

# usa el dominio, el puerto del dominio
class InMemoryConversationStore:
    def __init__(self, ttl_seconds: int = 300):
        self.ttl_seconds = ttl_seconds
        self._store: dict[str, tuple[Conversation, float]] = {}

    def get_by_user(self, user: User) -> Conversation | None:
        entry = self._store.get(user.id)
        if not entry:
            return None

        conversation, last_ts = entry
        if time.time() - last_ts > self.ttl_seconds:
            del self._store[user.id]
            return None

        return conversation

    def save(self, conversation: Conversation) -> None:
        self._store[conversation.user.id] = (conversation, time.time())

    def delete_by_user(self, user: User) -> None:
        self._store.pop(user.id)