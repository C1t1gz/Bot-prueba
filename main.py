from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse
import logging
from timbero import verify_discord_signature, tirar_dados, girar_ruleta, lanzar_moneda, mensaje_ayuda


logging.basicConfig(level=logging.INFO)


app = FastAPI()

@app.post("/discord-interactions")
async def handle_discord_interactions(request: Request):
    """
    Endpoint principal para manejar las interacciones de Discord.
    Parámetros:
        request (Request): Solicitud HTTP recibida desde Discord.
    Retorna:
        Response o dict: Respuesta para Discord según el tipo de interacción.
    """
    # --- VERIFICACIÓN DE FIRMA DE DISCORD ---
    signature = request.headers.get("X-Signature-Ed25519")
    timestamp = request.headers.get("X-Signature-Timestamp")
    body = await request.body()

    if not (signature and timestamp):
        return Response(content="Faltan cabeceras de firma de Discord", status_code=401)

    if not verify_discord_signature(signature, timestamp, body):
        return Response(content="Firma de Discord inválida", status_code=401)


    interaction_data = await request.json()
    interaction_type = interaction_data.get("type")

    logging.info(f"Interacción recibida: Tipo {interaction_type}")

    # --- APRETÓN DE MANOS DE VERIFICACIÓN ---
    if interaction_type == 1:
        logging.info("Recibido PING de Discord. Enviando PONG de vuelta.")
        return {"type": 1}

    # --- LÓGICA NORMAL DE COMANDOS ---
    if interaction_type == 2:
        logging.info("Recibido comando. Procesando...")
        # Obtener el nombre del comando
        command_data = interaction_data.get("data", {})
        command_name = command_data.get("name", "")
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
            # Responder rápido con ACK diferido
            import threading
            interaction_token = interaction_data.get("token")
            application_id = interaction_data.get("application_id")
            user_id = str(interaction_data.get("member", {}).get("user", {}).get("id", "unknown"))
            # Extraer roles del usuario
            roles = interaction_data.get("member", {}).get("roles", [])
            # Lanzar el procesamiento de Gemini en segundo plano
            def send_followup():
                """
                Envía una respuesta de seguimiento a un webhook de Discord utilizando el resultado de una función de chat LLM.

                La función realiza lo siguiente:
                - Obtiene una respuesta de un modelo de lenguaje (chat_llm) usando el prompt, user_id y roles.
                - Envía la respuesta al webhook de Discord especificado por application_id e interaction_token.
                - Guarda la interacción en el historial de chat.
                - Envía un mensaje adicional indicando que la memoria fue actualizada.
                - Maneja y muestra errores en caso de que ocurra algún problema durante el proceso.

                Nota: Se asume que las variables 'prompt', 'user_id', 'roles', 'application_id' y 'interaction_token' están definidas en el ámbito donde se llama la función.
                """
                from timbero import chat as chat_llm
                import requests
                from chat_history import save_interaction
                respuesta = chat_llm(prompt, user_id=user_id, roles=roles)
                url = f"https://discord.com/api/v10/webhooks/{application_id}/{interaction_token}"
                data = {"content": respuesta}
                try:
                    save_interaction(user_id, prompt, respuesta, roles)
                    requests.post(url, json=data)
                    # Avisar que la memoria fue actualizada
                    data_mem = {"content": "🧠 La memoria fue actualizada."}
                    requests.post(url, json=data_mem)
                except Exception as e:
                    print(f"Error enviando followup: {e}")
            threading.Thread(target=send_followup).start()
            return {"type": 5}  # DEFERRED_CHANNEL_MESSAGE_WITH_SOURCE

        elif command_name == "help":
            content = mensaje_ayuda()
        else:
            content = "Comando no reconocido. Usa /help para ver los comandos disponibles."
        # Responder directamente a Discord con el resultado
        return {
            "type": 4,  # CHANNEL_MESSAGE_WITH_SOURCE
            "data": {"content": content}
        }

    return Response(content="Tipo de interacción no manejado", status_code=400)
