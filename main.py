"""
Servidor FastAPI principal para el bot de Discord
"""

from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse
import logging
import threading
import requests
import os
import time
from dotenv import load_dotenv

# Importar desde la nueva estructura
from src.core.chat import chat, tirar_dados, girar_ruleta, lanzar_moneda, mensaje_ayuda
from src.utils.security import verify_discord_signature

# Cargar variables de entorno
load_dotenv()

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Crear aplicación FastAPI
app = FastAPI(
    title="PythonBots - Discord Bot API",
    description="API para el bot de Discord con sistema RAG mejorado",
    version="1.0.0"
)

@app.post("/discord-interactions")
async def handle_discord_interactions(request: Request):
    """
    Endpoint principal para manejar las interacciones de Discord.
    
    Args:
        request (Request): Solicitud HTTP recibida desde Discord.
        
    Returns:
        Response o dict: Respuesta para Discord según el tipo de interacción.
    """
    # Verificación de firma de Discord
    signature = request.headers.get("X-Signature-Ed25519")
    timestamp = request.headers.get("X-Signature-Timestamp")
    body = await request.body()

    if not (signature and timestamp):
        return Response(content="Faltan cabeceras de firma de Discord", status_code=401)

    if not verify_discord_signature(signature, timestamp, body):
        return Response(content="Firma de Discord inválida", status_code=401)

    # Procesar datos de la interacción
    interaction_data = await request.json()
    interaction_type = interaction_data.get("type")

    logger.info(f"Interacción recibida: Tipo {interaction_type}")

    # Apretón de manos de verificación
    if interaction_type == 1:
        logger.info("Recibido PING de Discord. Enviando PONG de vuelta.")
        return {"type": 1}

    # Lógica normal de comandos
    if interaction_type == 2:
        logger.info("Recibido comando. Procesando...")
        
        # Obtener el nombre del comando
        command_data = interaction_data.get("data", {})
        command_name = command_data.get("name", "")
        
        # Manejar diferentes comandos
        if command_name == "dados":
            content = tirar_dados()
        elif command_name == "ruleta":
            content = girar_ruleta()
        elif command_name == "coinflip":
            content = lanzar_moneda()
        elif command_name == "chat":
            # Obtener el prompt enviado como opción del comando
            prompt = None
            options = command_data.get("options", [])
            if options and isinstance(options, list):
                for opt in options:
                    if opt.get("name") == "prompt":
                        prompt = opt.get("value")
                        break
                        
            if not prompt:
                return {
                    "type": 4,
                    "data": {"content": "Debes enviar un mensaje para el chat. Ejemplo: /chat prompt:Tu pregunta"}
                }
                
            # Responder inmediatamente con ACK diferido para evitar timeout
            interaction_token = interaction_data.get("token")
            application_id = interaction_data.get("application_id")
            user_id = str(interaction_data.get("member", {}).get("user", {}).get("id", "unknown"))
            roles = interaction_data.get("member", {}).get("roles", [])
            
            def send_followup():
                """
                Envía una respuesta de seguimiento a un webhook de Discord utilizando el resultado de la función de chat LLM.
                """
                try:
                    logger.info(f"Procesando chat para usuario {user_id}: {prompt}")
                    
                    # Procesar la respuesta del chat
                    respuesta = chat(prompt, user_id=user_id, roles=roles)
                    
                    # Construir URL del webhook
                    url = f"https://discord.com/api/v10/webhooks/{application_id}/{interaction_token}"
                    
                    # Enviar respuesta principal
                    data = {"content": respuesta}
                    response = requests.post(url, json=data, timeout=10)
                    
                    if response.status_code == 200:
                        logger.info("Respuesta enviada exitosamente")
                    else:
                        logger.error(f"Error enviando respuesta: {response.status_code} - {response.text}")
                    
                except Exception as e:
                    logger.error(f"Error en send_followup: {e}")
                    # Intentar enviar mensaje de error
                    try:
                        error_url = f"https://discord.com/api/v10/webhooks/{application_id}/{interaction_token}"
                        error_data = {"content": "❌ Error procesando tu mensaje. Inténtalo de nuevo."}
                        requests.post(error_url, json=error_data, timeout=5)
                    except:
                        logger.error("No se pudo enviar mensaje de error")
                    
            # Iniciar procesamiento en segundo plano
            thread = threading.Thread(target=send_followup)
            thread.daemon = True  # El thread se cerrará cuando el programa principal termine
            thread.start()
            
            # Responder inmediatamente con ACK diferido
            logger.info("Enviando ACK diferido para comando chat")
            return {"type": 5}  # DEFERRED_CHANNEL_MESSAGE_WITH_SOURCE

        elif command_name == "help":
            content = mensaje_ayuda()
        else:
            content = "Comando no reconocido. Usa /help para ver los comandos disponibles."
            
        # Responder directamente a Discord con el resultado (para comandos rápidos)
        return {
            "type": 4,  # CHANNEL_MESSAGE_WITH_SOURCE
            "data": {"content": content}
        }

    return Response(content="Tipo de interacción no manejado", status_code=400)

@app.get("/")
async def root():
    """Endpoint raíz para verificar que el servidor está funcionando."""
    return {
        "message": "PythonBots - Discord Bot API",
        "status": "running",
        "version": "1.0.0"
    }

@app.get("/health")
async def health_check():
    """Endpoint de verificación de salud del servidor."""
    return {
        "status": "healthy",
        "timestamp": "2024-01-01T00:00:00Z"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
