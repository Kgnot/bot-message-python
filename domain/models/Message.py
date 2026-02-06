import datetime
import uuid
from typing import Optional


class Message:
    def __init__(
        self,
        text: Optional[str],
        foto: Optional[str],               # URL o path de la imagen
        created_at: datetime.datetime,

        # --- Datos extraídos de la IMAGEN ---
        lugarFoto: Optional[str] = None,
        estadoBanco: Optional[str] = None,
        indice: Optional[str] = None,
        fecha_foto: Optional[str] = None,
        altitud: Optional[str] = None,
        velocidad: Optional[str] = None,
        residencia: Optional[str] = None,

        # --- Datos extraídos del TEXTO ---
        lugar: Optional[str] = None,
        entidad: Optional[str] = None,
        codCajero: Optional[str] = None,
    ):
        self.id = uuid.uuid4()

        # Mensaje original
        self.text = text
        self.foto = foto
        self.created_at = created_at

        # Imagen (visión)
        self.lugarFoto = lugarFoto
        self.estadoBanco = estadoBanco
        self.indice = indice
        self.fecha_foto = fecha_foto
        self.altitud = altitud
        self.velocidad = velocidad
        self.residencia = residencia

        # Texto (PLN)
        self.lugar = lugar
        self.entidad = entidad
        self.codCajero = codCajero
