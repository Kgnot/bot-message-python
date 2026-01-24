# Automatización Bot

Un sistema de automatización de conversaciones basado en arquitectura hexagonal con integración para Telegram.

## Arquitectura

El proyecto sigue una arquitectura hexagonal (clean architecture) con las siguientes capas:

- **Domain**: Modelos de negocio y puertos de dominio
- **Application**: Casos de uso y servicios de aplicación
- **Infrastructure**: Implementaciones concretas (Telegram, Redis, etc.)

## Características

- Gestión de conversaciones con expiración automática
- Integración con Telegram mediante webhooks
- Almacenamiento de sesiones en memoria o Redis
- Mapeo de mensajes entre Telegram y modelos de dominio
- Configuración mediante variables de entorno

## Requisitos Previos

- Python 3.12+
- Redis (opcional, para almacenamiento persistente)

## Instalación

1. Clonar el repositorio:
```bash
git clone <repository-url>
cd autoamtizacion
```

2. Crear entorno virtual:
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# o
.venv\Scripts\activate  # Windows
```

3. Instalar dependencias:
```bash
pip install -r requirements.txt
```

## Configuración

Crear un archivo `.env` con las siguientes variables:

```env
TELEGRAM_BOT_TOKEN=tu_token_de_bot
WEBHOOK_URL=https://tu-dominio.com/telegram/webhook
```

## Uso

Iniciar el servidor:

```bash
python main.py
```

El servidor se iniciará en `http://localhost:8000` por defecto.

## Endpoints

- `POST /telegram/webhook` - Webhook para recibir mensajes de Telegram

## Estructura del Proyecto

```
autoamtizacion/
├── domain/
│   ├── models/          # Modelos de dominio
│   └── ports/           # Puertos de dominio
├── application/
│   ├── services/        # Servicios de aplicación
│   ├── usecases/        # Casos de uso
│   └── ports/           # Puertos de aplicación
├── infrastructure/
│   ├── controllers/     # Controladores HTTP
│   ├── bot_services/    # Servicios de bots
│   ├── session_store/   # Almacenamiento de sesiones
│   ├── mapper/          # Mapeo de datos
│   └── config/          # Configuración
├── utils/               # Utilidades
└── main.py             # Punto de entrada
```

## Desarrollo

El proyecto utiliza:
- **FastAPI** para la API web
- **Aiogram** para la integración con Telegram
- **Redis** para almacenamiento persistente (opcional)
- **Python-dotenv** para gestión de variables de entorno

## Licencia

[Agregar información de licencia]