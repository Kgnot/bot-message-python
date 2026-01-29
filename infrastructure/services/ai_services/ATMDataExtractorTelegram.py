import os

from google import genai
from google.genai import types

from infrastructure.utils import clean_json


class ATMDataExtractorTelegram:
    def __init__(self):
        # Introducimos la key
        self.client = genai.Client(api_key=os.getenv("GEMINI_KEY"))

        # definimos el modelo a usar
        self.model_id = "gemini-2.5-flash"

        self.prompt = """
        Eres un experto en visión artificial para banca. 
        Analiza la imagen o texto y extrae estos datos en JSON:
        {
          "lugar": "Nombre del municipio o barrio",
          "entidad": "Nombre del banco (ej: Bancolombia, Banco de Occidente, etc)",
          "codCajero": "Busca un código numérico o 'Número de índice'"
        }
        Responde exclusivamente con el JSON.
        """

    async def extract_from_image(self, image_bytes: bytes, additional_text: str = None):
        try:
            # Creamos la lista de contenidos
            content_list = [self.prompt, types.Part.from_bytes(data=image_bytes, mime_type="image/jpeg")]

            # Si el usuario escribió algo, se lo pasamos como contexto extra
            if additional_text:
                content_list.append(f"Contexto adicional proporcionado por el usuario: {additional_text}")

            response = self.client.models.generate_content(
                model=self.model_id,
                contents=content_list
            )
            return clean_json(response.text)
        except Exception as e:
            print(f"Error en la API: {e}")
            return None

    async def extract_from_text(self, text_content: str):
        try:
            # Enviamos el prompt seguido del texto del usuario
            response = self.client.models.generate_content(
                model=self.model_id,
                contents=[self.prompt, f"Texto del usuario: {text_content}"]
            )
            return clean_json(response.text)
        except Exception as e:
            print(f"Error en la API (Texto): {e}")
            return {"lugar": None, "entidad": None, "codCajero": None}