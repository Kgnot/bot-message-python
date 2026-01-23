import datetime
import uuid
from typing import Optional

from domain.models import Conversation


class Message:
    def __init__(self, text: Optional[str], image_url:Optional[str] ,created_at: datetime):
        self.id = uuid.uuid4()
        self.text = text
        self.image_url = image_url
        self.created_at = created_at