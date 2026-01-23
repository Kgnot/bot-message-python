from aiogram.types import Message

from domain.models import User


def telegram_user_mapper(message: Message) -> User:
    tg_user = message.from_user
    assert tg_user is not None  # In practice, messages have from_user

    user_id = str(tg_user.id)
    nombre = tg_user.first_name or ""

    celular = ""

    return User(
        nombre=nombre,
        celular=celular,
        userId=user_id
    )
