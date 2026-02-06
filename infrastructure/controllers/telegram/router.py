from datetime import datetime

from aiogram import Router
from aiogram.types import Message, FSInputFile
from domain.models import Message as DomainMessage, Conversation, User

from application.services import ConversationServiceController
from infrastructure.services.ai_services import ATMDataExtractorTelegram
from infrastructure.mapper import telegram_user_mapper, telegram_to_domain_message
from infrastructure.services.excel_service.ExcelGenerator import ExcelGenerator
from infrastructure.utils.utils import merge_json

telegram_router = Router()
extractor = ATMDataExtractorTelegram()
conversation_controller = ConversationServiceController()


@telegram_router.message()
async def handle_message(message: Message):
    user: User = telegram_user_mapper(message)
    texto_usuario: str = ""
    # print("Mensaje recibido",message)

    total_extracted = {}

    if message.photo:
        photo = message.photo[-1]
        file = await message.bot.get_file(photo.file_id)
        photo_bytes = await message.bot.download_file(file.file_path)
        texto_usuario = message.caption
        image_data = await extractor.extract_from_image(photo_bytes.read(), texto_usuario)
        text_data = await extractor.extract_from_text(texto_usuario)

        total_extracted = merge_json(text_data or {}, image_data or {})
        foto_file_id = photo.file_id
    else:
        texto_usuario = message.text or ""
        total_extracted = await extractor.extract_from_text(texto_usuario) or {}
        foto_file_id = None

    # 1. Mensaje de dominio
    new_message: DomainMessage = DomainMessage(
        text=texto_usuario,
        foto=foto_file_id,
        created_at=datetime.now(),

        lugarFoto=total_extracted.get("lugarFoto"),
        estadoBanco=total_extracted.get("estadoBanco"),
        indice=total_extracted.get("indice"),
        fecha_foto=total_extracted.get("fecha_foto"),
        altitud=total_extracted.get("altitud"),
        velocidad=total_extracted.get("velocidad"),
        residencia=total_extracted.get("residencia"),

        lugar=total_extracted.get("lugar"),
        entidad=total_extracted.get("entidad"),
        codCajero=total_extracted.get("codCajero"),
    )

    conversation: Conversation = conversation_controller.handle_message(user, new_message)

    excel_path = await ExcelGenerator.create_report(
        conversation.messages,
        user.id,
        message.bot  # 👈 necesario para descargar imágenes
    )

    await message.reply(
        f"✅ Registrado: {new_message.estadoBanco} en {new_message.lugar} (Índice: {new_message.indice})"
    )
