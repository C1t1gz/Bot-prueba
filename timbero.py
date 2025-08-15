import discord
import random
import os
from nacl.signing import VerifyKey
from nacl.exceptions import BadSignatureError
from dotenv import load_dotenv
from langchain.memory import ConversationBufferMemory

load_dotenv()
USER_MEMORIES = {}

def verify_discord_signature(signature: str, timestamp: str, body: bytes) -> bool:
    """
    Verifica la firma de una solicitud recibida desde Discord.
    """
    public_key = os.getenv("DISCORD_PUBLIC_KEY")
    if not public_key:
        return False
    try:
        verify_key = VerifyKey(bytes.fromhex(public_key))
        verify_key.verify(timestamp.encode() + body, bytes.fromhex(signature))
        return True
    except BadSignatureError:
        return False
    except Exception:
        return False

def tirar_dados():
    dice1 = random.randint(1, 6)
    dice2 = random.randint(1, 6)
    return f'🎲 ¡Tirando los dados! 🎲\n🎲 Resultado: {dice1} y {dice2} 🎲'

def girar_ruleta():
    colors = ['rojo', 'negro', 'verde']
    result = random.choice(colors)
    number = random.randint(0, 36)
    if number == 0:
        return f'🎰 Resultado: {number} Verde 🎰'
    else:
        return f'🎰 Resultado: {result} {number} 🎰'

def lanzar_moneda():
    result = random.choice(['cara', 'cruz'])
    return f'🪙 ¡Lanzando la moneda! Resultado: {result} 🪙'

def mensaje_ayuda():
    return (
        "¡Hola! Aquí están los comandos disponibles:\n"
        "!dados - Tira los dados.\n"
        "!ruleta - Gira la ruleta.\n"
        "!coinflip - Lanza una moneda.\n"
        "!help - Muestra este mensaje de ayuda."
    )

def chat(prompt: str, user_id: str = None, roles=None, history_limit: int = 10) -> str: # type: ignore
    global USER_MEMORIES
    memory = USER_MEMORIES.get(user_id)
    if memory is None:
        memory = ConversationBufferMemory(return_messages=True)
        USER_MEMORIES[user_id] = memory

    roles_info = ""
    if roles:
        roles_info = f"Roles del usuario: {', '.join([str(r) for r in roles])}\n"

    from enhanced_rag import get_retriever, set_history, get_enhanced_documents
    from langchain_google_genai import ChatGoogleGenerativeAI
    from langchain.chains.combine_documents import create_stuff_documents_chain
    from langchain.chains import create_retrieval_chain
    from langchain_core.prompts import ChatPromptTemplate

    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        return "Error: Falta GOOGLE_API_KEY en el entorno."
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", google_api_key=api_key)

    # Obtener historial de memoria y construir el prompt completo
    mem_vars = memory.load_memory_variables({})
    history = mem_vars.get("history", "")
    
    # Mejorar el prompt del sistema para manejar mejor el contexto
    system_prompt = (
        "Eres un asistente útil que responde preguntas basándose en el contexto proporcionado y el historial de la conversación."
        "IMPORTANTE: Si la pregunta hace referencia a alguien o algo mencionado anteriormente en la conversación, "
        "usa esa información del contexto para entender a qué se refiere la pregunta. "
        "Si la pregunta no hace referencia a alguien o algo mencionado anteriormente en la conversación, "
        "No te inventes información. "
        "Si no sabes la respuesta, responde con 'No sé la respuesta a esa pregunta.'"
        "Contexto de la base de conocimiento: {context}\n"
        "Historial de la conversación: {history}"
    )
    
    chat_prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "{input}"),
    ])
    
    question_answer_chain = create_stuff_documents_chain(llm, chat_prompt)
    
    # Obtener el retriever mejorado
    retriever = get_retriever()
    chain = create_retrieval_chain(retriever, question_answer_chain)
    
    # Asignar memoria si el chain lo permite
    if hasattr(chain, 'memory'):
        chain.memory = memory

    # Construir el prompt completo incluyendo el historial
    if history:
        full_prompt = f"{roles_info}{history}\nUSUARIO: {prompt}\n"
    else:
        full_prompt = f"{roles_info}USUARIO: {prompt}\n"

    # Crear el contexto con el historial para que el LLM lo considere
    context_with_history = {
        "input": full_prompt,
        "history": history if history else "No hay historial previo."
    }

    # Usar el retriever mejorado con el historial
    if history:
        # Establecer el historial para el contexto
        set_history(history)
        # Obtener documentos relevantes considerando el historial
        relevant_docs = get_enhanced_documents(prompt)
        # Crear un contexto mejorado con los documentos relevantes
        if relevant_docs:
            context_text = "\n".join([doc.page_content for doc in relevant_docs])
            context_with_history["context"] = context_text

    result = chain.invoke(context_with_history)
    response_text = result.get("answer") or str(result)

    memory.chat_memory.add_user_message(prompt)
    memory.chat_memory.add_ai_message(response_text)

    aviso = '📚 *Esta respuesta utiliza información de la base de conocimiento.*\n\n'
    if isinstance(response_text, str) and not response_text.startswith(aviso):
        return aviso + response_text
    return str(response_text)

class Timbero(discord.Client):
    async def on_ready(self):
        print(f'Logged in as {self.user}!')

    async def on_message(self, message):
        if message.author == self.user:
            return
        if message.content.startswith("!help"): 
            await message.channel.send(mensaje_ayuda())
        elif message.content.startswith("!dados"):
            await message.channel.send(tirar_dados())
        elif message.content.startswith("!ruleta"):
            await message.channel.send(girar_ruleta())
        elif message.content.startswith("!coinflip"):
            await message.channel.send(lanzar_moneda())
        else:
            response = chat(message.content, user_id=str(message.author.id), roles=[role.name for role in getattr(message.author, 'roles', [])])
            await message.channel.send(response)
