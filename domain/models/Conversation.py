from datetime import datetime, timedelta
import uuid
from domain.models import User, Message


class Conversation:
    MAX_IDLE_TIME = timedelta(minutes=5)

    def __init__(self, user: User, started_at: datetime):
        self.user = user
        self.id = uuid.uuid4()
        self.last_interaction_at = started_at
        self.messages: list[Message] = []

    def addMessage(self, message: Message, now: datetime):
        self.messages.append(message)
        self.touch(now)

    def touch(self, now: datetime):
        self.last_interaction_at = now

    def is_expired(self, now: datetime) -> bool:
        return now - self.last_interaction_at > self.MAX_IDLE_TIME
