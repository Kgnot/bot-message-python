import uuid
from typing import Protocol, Union

from domain.models import Conversation


# Esto es un protocolo | interfaz que usaremos
class ConversationStore(Protocol):

    def create(self, conversation: Conversation) -> Conversation: ...
    def get(self, conversation_id: uuid.UUID) -> Union[Conversation, None]: ...
    def save(self, conversation: Conversation) -> None: ...
    def delete(self, conversation_id: uuid.UUID) -> None: ...

