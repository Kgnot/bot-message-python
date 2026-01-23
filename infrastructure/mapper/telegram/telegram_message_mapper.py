from datetime import datetime
from aiogram.types import Message

from domain.models import Message as DomainMessage


def telegram_to_domain_message(message: Message) -> DomainMessage:
    text = message.text or ""
    image_url = None

    if message.photo:
        image_url = message.photo[-1].file_id

    return DomainMessage(
        text=text,
        image_url=image_url,
        created_at=datetime.now(),
    )



