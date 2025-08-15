import requests
import os
from dotenv import load_dotenv

load_dotenv()

APPLICATION_ID = os.getenv("DISCORD_APPLICATION_ID")  # Pega tu Application ID aquí o en el .env
BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")            # Pega tu Bot Token aquí o en el .env

# Define los comandos que quieres registrar
commands = [
    {
        "name": "dados",
        "description": "Tira dos dados y muestra el resultado.",
        "type": 1  # CHAT_INPUT
    },
    {
        "name": "ruleta",
        "description": "Gira la ruleta y muestra el resultado.",
        "type": 1
    },
    {
        "name": "coinflip",
        "description": "Lanza una moneda y muestra el resultado.",
        "type": 1
    },
    {
        "name": "help",
        "description": "Muestra los comandos disponibles.",
        "type": 1
    }
    {
        "name": "chat",
        "description": "Chatea con la IA Gemini (requiere parámetro 'prompt').",
        "type": 1,
        "options": [
            {
                "name": "prompt",
                "description": "Mensaje o pregunta para la IA",
                "type": 3,  # STRING
                "required": True
            }
        ]
    }
]

# URL para registrar comandos globales
url = f"https://discord.com/api/v10/applications/{APPLICATION_ID}/commands"

headers = {
    "Authorization": f"Bot {BOT_TOKEN}",
    "Content-Type": "application/json"
}

for command in commands:
    response = requests.post(url, headers=headers, json=command)
    if response.status_code == 201:
        print(f"Comando /{command['name']} registrado correctamente.")
    elif response.status_code == 200:
        print(f"Comando /{command['name']} ya existe y fue actualizado.")
    else:
        print(f"Error registrando /{command['name']}: {response.status_code}\n{response.text}")
