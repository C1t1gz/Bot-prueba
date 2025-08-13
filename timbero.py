import discord  
import random
import os
from nacl.signing import VerifyKey
from nacl.exceptions import BadSignatureError
from dotenv import load_dotenv

load_dotenv()

def verify_discord_signature(signature: str, timestamp: str, body: bytes) -> bool:
    """
    Verifica la firma de una solicitud recibida desde Discord.
    Parámetros:
        signature (str): Firma enviada por Discord en la cabecera 'X-Signature-Ed25519'.
        timestamp (str): Marca de tiempo enviada por Discord en la cabecera 'X-Signature-Timestamp'.
        body (bytes): Cuerpo de la solicitud HTTP recibida.
    Retorna:
        bool: True si la firma es válida, False si no.
    """
    public_key = os.getenv("DISCORD_PUBLIC_KEY")
    if not public_key:
        raise ValueError("DISCORD_PUBLIC_KEY no está configurada en el .env")
    try:
        verify_key = VerifyKey(bytes.fromhex(public_key))
        verify_key.verify(timestamp.encode() + body, bytes.fromhex(signature))
        return True
    except BadSignatureError:
        return False
    except Exception as e:
        # Puedes loguear el error si lo deseas
        return False


def tirar_dados():
    """
    Simula tirar dos dados y devuelve el resultado como string.
    No recibe parámetros.
    Retorna:
        str: Mensaje con el resultado de los dos dados.
    """
    dice1 = random.randint(1, 6)
    dice2 = random.randint(1, 6)
    return f'🎲 ¡Tirando los dados! 🎲\n🎲 Resultado: {dice1} y {dice2} 🎲'

def girar_ruleta():
    """
    Simula girar una ruleta de casino y devuelve el resultado como string.
    No recibe parámetros.
    Retorna:
        str: Mensaje con el color y número obtenido.
    """
    colors = ['rojo', 'negro', 'verde']
    result = random.choice(colors)
    number = random.randint(0, 36)
    if number == 0:
        return f'🎰 Resultado: {number} Verde 🎰'
    else:
        return f'🎰 Resultado: {result} {number} 🎰'

def lanzar_moneda():
    """
    Simula lanzar una moneda y devuelve el resultado como string.
    No recibe parámetros.
    Retorna:
        str: Mensaje con el resultado (cara o cruz).
    """
    result = random.choice(['cara', 'cruz'])
    return f'🪙 ¡Lanzando la moneda! Resultado: {result} 🪙'

def mensaje_ayuda():
    """
    Devuelve el mensaje de ayuda con los comandos disponibles para el bot.
    No recibe parámetros.
    Retorna:
        str: Mensaje con la lista de comandos disponibles.
    """
    return (
        "¡Hola! Aquí están los comandos disponibles:\n"
        "!dados - Tira los dados.\n"
        "!ruleta - Gira la ruleta.\n"
        "!coinflip - Lanza una moneda.\n"
        "!help - Muestra este mensaje de ayuda."
    )

def chat(prompt: str, user_id: str = None, roles=None, history_limit: int = 10) -> str: # type: ignore
    """
    Genera una respuesta usando Gemini (Google Generative AI) considerando el historial de chat y contexto relevante.
    Parámetros:
        prompt (str): Mensaje o pregunta del usuario.
        user_id (str, opcional): ID del usuario para cargar historial personalizado.
        roles (list, opcional): Lista de roles del usuario para personalizar la respuesta.
        history_limit (int, opcional): Cantidad máxima de mensajes de historial a considerar (por defecto 10).
    Retorna:
        str: Respuesta generada por el modelo.
    """
    try:
        from langchain_google_genai import ChatGoogleGenerativeAI
        import os
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            return "Error: Falta la variable GOOGLE_API_KEY en el entorno."
        llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", google_api_key=api_key)

        # Cargar historial de conversación
        from chat_history import load_history
        history = load_history(user_id if user_id else "", limit=history_limit)  # Últimos mensajes según history_limit

        # Obtener contexto relevante de la base de conocimiento
        rag_context = ""
        if prompt and prompt.strip():
            from simple_rag import get_relevant_chunks
            relevant_chunks = get_relevant_chunks(prompt, top_k=2)
            rag_context = "\n".join(relevant_chunks)

        # Construir contexto de conversación
        context = ""
        if history:
            context = "\n".join(f"USUARIO: {msg['prompt']}\nBOT: {msg['response']}" 
                               for msg in history[-history_limit:])  # Últimos 'history_limit' intercambios

        # Agregar información de roles si está disponible
        roles_info = ""
        if roles:
            roles_info = f"Roles del usuario: {', '.join([str(r) for r in roles])}\n"

        # Construir el prompt final
        if rag_context or roles_info or context:
            full_prompt = f"""{roles_info}
BASE DE CONOCIMIENTO:
{rag_context}

CONVERSACIÓN ANTERIOR:
{context}

USUARIO: {prompt}
BOT: """
        else:
            full_prompt = prompt

        response = llm.invoke(full_prompt)
        response_text = response.content if hasattr(response, 'content') else str(response)

        aviso = '📚 *Esta respuesta utiliza información de la base de conocimiento.*\n\n'
        if rag_context and isinstance(response_text, str) and not response_text.startswith(aviso):
            return aviso + response_text
        return str(response_text)
    except Exception as exc:
        return "Error al generar respuesta con Gemini: {}".format(str(exc))

class Timbero(discord.Client):
    """
    Cliente principal del bot de Discord. Hereda de discord.Client.
    """
    async def on_ready(self):
        """
        Evento que se ejecuta cuando el bot se conecta exitosamente a Discord.
        No recibe parámetros.
        """
        print(f'Logged in as {self.user}!')

    async def on_message(self, message):
        """
        Evento que se ejecuta cuando el bot recibe un mensaje en un canal.
        Parámetros:
            message (discord.Message): Mensaje recibido en el canal.
        """
        if message.author == self.user:
            return

        # Responde a los comandos definidos
        if message.content.startswith("!help"):
            await message.channel.send(mensaje_ayuda())
        elif message.content.startswith("!dados"):
            await message.channel.send(tirar_dados())
        elif message.content.startswith("!ruleta"):
            await message.channel.send(girar_ruleta())
        elif message.content.startswith("!coinflip"):
            await message.channel.send(lanzar_moneda())
        else:
            # Use chat function for other messages
            response = chat(message.content, user_id=str(message.author.id), roles=[role.name for role in getattr(message.author, 'roles', [])])
            await message.channel.send(response)


