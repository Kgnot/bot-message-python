# infrastructure/session_store/redis_store.py
import uuid
import pickle
from redis import Redis
from domain.models import Conversation


def _key(conversation_id: uuid.UUID) -> str:
    return f"conversation:{conversation_id}"


class RedisConversationSessionStore:
    def __init__(self, redis: Redis, ttl_seconds: int = 300):
        self.redis = redis
        self.ttl = ttl_seconds

    def get(self, conversation_id: uuid.UUID) -> Conversation | None:
        data = self.redis.get(_key(conversation_id))
        if not data:
            return None
        return pickle.loads(data)

    def save(self, conversation: Conversation) -> None:
        self.redis.setex(
            _key(conversation.id),
            self.ttl,
            pickle.dumps(conversation)
        )

    def delete(self, conversation_id: uuid.UUID) -> None:
        self.redis.delete(_key(conversation_id))
