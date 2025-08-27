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
GUILD_ID = os.getenv("DISCORD_GUILD_ID")              # Pega tu Guild ID aquí o en el .env

if not all([APPLICATION_ID, BOT_TOKEN, GUILD_ID]):
    logger.error("Faltan variables en el .env (DISCORD_APPLICATION_ID, DISCORD_BOT_TOKEN, DISCORD_GUILD_ID)")
    exit(1)

# Define los comandos que quieres registrar
commands = [
    {
        "name": "dados",
        "description": "Tira dos dados y obtén un resultado aleatorio.",
        "type": 1
    },
    {
        "name": "coinflip",
        "description": "Lanza una moneda y obtén cara o cruz.",
        "type": 1
    },
    {
        "name": "ruleta",
        "description": "Gira la ruleta y obtén un resultado aleatorio.",
        "type": 1
    },
    

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
        "name": "forget",
        "description": "Borra tu memoria de conversación con el bot.",
        "type": 1
    },
    {
        "name": "help",
        "description": "Muestra la lista de comandos disponibles.",
        "type": 1
    },
]

# URL para registrar comandos SOLO en el servidor de prueba
url = f"https://discord.com/api/v10/applications/{APPLICATION_ID}/guilds/{GUILD_ID}/commands"

headers = {
    "Authorization": f"Bot {BOT_TOKEN}",
    "Content-Type": "application/json"
}

logger.info(f"Registrando {len(commands)} comandos en el servidor de Discord...")
logger.info(f"Guild ID: {GUILD_ID}")
logger.info(f"Application ID: {APPLICATION_ID}")

for command in commands:
    logger.info(f"Registrando comando: /{command['name']}")
    response = requests.post(url, headers=headers, json=command)
    if response.status_code == 201:
        logger.success(f"✅ Comando /{command['name']} registrado correctamente en el servidor de prueba.")
    elif response.status_code == 200:
        logger.info(f"🔄 Comando /{command['name']} ya existe y fue actualizado en el servidor de prueba.")
    else:
        logger.error(f"❌ Error registrando /{command['name']}: {response.status_code}\n{response.text}")

logger.info("🎉 Proceso de registro de comandos completado.")
logger.info("💡 Los comandos pueden tardar hasta 1 hora en aparecer en Discord.")
