import requests
import os
from dotenv import load_dotenv

load_dotenv()

APPLICATION_ID = os.getenv("DISCORD_APPLICATION_ID")  # Pega tu Application ID aquí o en el .env
BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")            # Pega tu Bot Token aquí o en el .env
GUILD_ID = os.getenv("DISCORD_GUILD_ID")              # Pega tu Guild ID aquí o en el .env

if not all([APPLICATION_ID, BOT_TOKEN, GUILD_ID]):
    print("Faltan variables en el .env (DISCORD_APPLICATION_ID, DISCORD_BOT_TOKEN, DISCORD_GUILD_ID)")
    exit(1)

# Define los comandos que quieres registrar
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
    }
]

# URL para registrar comandos SOLO en el servidor de prueba
url = f"https://discord.com/api/v10/applications/{APPLICATION_ID}/guilds/{GUILD_ID}/commands"

headers = {
    "Authorization": f"Bot {BOT_TOKEN}",
    "Content-Type": "application/json"
}

for command in commands:
    response = requests.post(url, headers=headers, json=command)
    if response.status_code == 201:
        print(f"Comando /{command['name']} registrado correctamente en el servidor de prueba.")
    elif response.status_code == 200:
        print(f"Comando /{command['name']} ya existe y fue actualizado en el servidor de prueba.")
    else:
        print(f"Error registrando /{command['name']}: {response.status_code}\n{response.text}")
