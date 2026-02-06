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

        # infrastructure/services/ai_services.py
        self.prompt = """
        Analiza la imagen de este cajero. Debes extraer información de dos fuentes:
        1. La apariencia del cajero (logos).
        2. La marca de agua de texto blanco en la esquina inferior derecha.
        RESPONDE ÚNICAMENTE CON UN JSON VÁLIDO. NO INCLUYAS EXPLICACIONES NI RUIDO.
        
        Extrae este JSON:
        {
          "lugarFoto": "Nombre municipio (ej: Guatapé)",
          "estadoBanco": "Aceptable, Bueno, Dañado, Muy Dañado")",
          "indice": "El número de índice (ej: 4380)",
          "fecha_foto": "La fecha y hora que aparece la zona inferior derecha de la foto en letras blancas",
          "altitud": "La altitud que aparece la zona inferior derecha de la foto en letras blancas",
          "velocidad": "La velocidad (ej: 0.0mi/h) que aparece la zona inferior derecha de la foto en letras blancas ",
          "residencia": "El lugar de residencia/departamento que aparece bajo el municipio"
        }
        """

        self.prompt_text = """
            Analiza el texto y extrae 3 variables lugar, entidad y cajero. Intenta entender que estas variables tengan
            sentido. 
            RESPONDE ÚNICAMENTE CON UN JSON VÁLIDO. NO INCLUYAS EXPLICACIONES NI RUIDO.
            
            Extrae el JSON: 
            {
                "lugar": "El lugar donde se encuentra el cajero (ej: Medellín)",
                "entidad": "La entidad bancaria del cajero (ej: Bancolombia)",
                "codCajero": "El código del cajero (ej: 12345)"
            }
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
                contents=[self.prompt_text, f"Texto del usuario: {text_content}"]
            )
            return clean_json(response.text)
        except Exception as e:
            print(f"Error en la API (Texto): {e}")
            return {"lugar": None, "entidad": None, "codCajero": None}