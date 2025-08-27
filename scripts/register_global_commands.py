import requests
import os
import sys
from pathlib import Path

# Agregar el directorio padre al path para importar módulos del proyecto
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
from src.utils.logger import logger

load_dotenv()

APPLICATION_ID = os.getenv("DISCORD_APPLICATION_ID")  # Pega tu Application ID aquí o en el .env
BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")            # Pega tu Bot Token aquí o en el .env

if not all([APPLICATION_ID, BOT_TOKEN]):
    logger.error("Faltan variables en el .env (DISCORD_APPLICATION_ID, DISCORD_BOT_TOKEN)")
    exit(1)

# Define los comandos que quieres registrar globalmente
commands = [
    {
        "name": "chat",
        "description": "Chatea con la IA Gemini (requiere parámetro 'prompt').",
        "type": 1,
        "options": 
        [
            {
                "name": "prompt",
                "description": "Mensaje o pregunta para la IA",
                "type": 3,  # STRING
                "required": True
            }
        ]
    },
    {
        "name": "dados",
        "description": "Tira dos dados y obtén un resultado aleatorio.",
        "type": 1
    },
    {
        "name": "ruleta",
        "description": "Gira la ruleta y obtén un resultado aleatorio.",
        "type": 1
    },
    {
        "name": "coinflip",
        "description": "Lanza una moneda y obtén cara o cruz.",
        "type": 1
    },
    {
        "name": "forget",
        "description": "Borra tu memoria de conversación con el bot.",
        "type": 1
    },
    {
        "name": "help",
        "description": "Muestra la lista de comandos disponibles.",
        "type": 1
    }
]

# URL para registrar comandos GLOBALMENTE (funcionan en todos los servidores)
url = f"https://discord.com/api/v10/applications/{APPLICATION_ID}/commands"

headers = {
    "Authorization": f"Bot {BOT_TOKEN}",
    "Content-Type": "application/json"
}

logger.info(f"Registrando {len(commands)} comandos GLOBALMENTE en Discord...")
logger.info(f"Application ID: {APPLICATION_ID}")
logger.warning("⚠️  Los comandos globales pueden tardar hasta 24 horas en propagarse a todos los servidores.")

for command in commands:
    logger.info(f"Registrando comando global: /{command['name']}")
    response = requests.post(url, headers=headers, json=command)
    if response.status_code == 201:
        logger.success(f"✅ Comando global /{command['name']} registrado correctamente.")
    elif response.status_code == 200:
        logger.info(f"🔄 Comando global /{command['name']} ya existe y fue actualizado.")
    else:
        logger.error(f"❌ Error registrando comando global /{command['name']}: {response.status_code}\n{response.text}")

logger.info("🎉 Proceso de registro de comandos globales completado.")
logger.info("⏰ Los comandos globales pueden tardar hasta 24 horas en aparecer en todos los servidores.")
logger.info("💡 Para desarrollo, es recomendable usar comandos de guild primero.")
