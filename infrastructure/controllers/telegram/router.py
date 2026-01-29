from aiogram import Router
from aiogram.types import Message

from application.services import ConversationServiceController
from infrastructure.services.ai_services import ATMDataExtractorTelegram
from infrastructure.mapper import telegram_user_mapper, telegram_to_domain_message

telegram_router = Router()
extractor = ATMDataExtractorTelegram()
conversation_controller = ConversationServiceController()


@telegram_router.message()
async def handle_message(message: Message):
    user = telegram_user_mapper(message) # Obtenemos el usuario
    domain_message = telegram_to_domain_message(message) # Obtenemos el mensaje general

    extracted_data = None
    # Campturamos el texto
    texto_usuario = message.text or message.caption

    # CASO: Imagen (con o sin texto)
    if message.photo:
        photo = message.photo[-1]
        file_info = await message.bot.get_file(photo.file_id)
        photo_bytes = await message.bot.download_file(file_info.file_path)
        img_buffer = photo_bytes.read()
        # Enviamos ambos a la IA para que use el texto como contexto de la imagen
        extracted_data = await extractor.extract_from_image(img_buffer, texto_usuario)
    # CASO: Solo Texto
    elif texto_usuario:
        extracted_data = await extractor.extract_from_text(texto_usuario)

    # Procesamiento del resultado
    if extracted_data and any(extracted_data.values()):  # Verifica que no sea un JSON de nulls
        conversation_controller.handle_message(user, extracted_data)

        resp_text = (
            f"Datos procesados:\n"
            f"Lugar: {extracted_data.get('lugar') or 'No detectado'}\n"
            f"Entidad: {extracted_data.get('entidad') or 'No detectado'}\n"
            f"Código: {extracted_data.get('codCajero') or 'No detectado'}"
        )
        await message.reply(resp_text)
    else:
        await message.reply(
            "No detecté información suficiente. Por favor, envía una foto del cajero o el texto con los datos. 🧐")