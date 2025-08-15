"""
Módulo principal de chat con funcionalidades del bot
"""

import os
import random
from pydantic import SecretStr
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama
from langchain.memory import ConversationBufferMemory

from config.settings import MODEL_PROVIDER, MODEL_NAME

# Importar desde la nueva estructura
from src.rag.enhanced_rag import get_retriever, set_history, get_enhanced_documents

# Memoria global por usuario
USER_MEMORIES = {}

# Cache para LLM y chain (evita recrearlos en cada llamada)
_llm_cache = None
_chain_cache = None

def get_llm():
    """Obtiene el LLM configurado, usando cache si está disponible."""
    global _llm_cache
    
    if _llm_cache is not None:
        return _llm_cache
    
    if MODEL_PROVIDER == "ollama":
        _llm_cache = ChatOllama(model=MODEL_NAME)
    elif MODEL_PROVIDER == "openai":
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("Error: Falta OPENAI_API_KEY en el entorno.")
        _llm_cache = ChatOpenAI(model=MODEL_NAME, api_key=SecretStr(api_key))
    else:  # google
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("Error: Falta GOOGLE_API_KEY en el entorno.")
        _llm_cache = ChatGoogleGenerativeAI(model=MODEL_NAME, google_api_key=api_key)
    
    return _llm_cache

def get_chain():
    """Obtiene el chain configurado, usando cache si está disponible."""
    global _chain_cache
    
    if _chain_cache is not None:
        return _chain_cache
    
    # Obtener LLM
    llm = get_llm()
    
    # Crear prompt optimizado
    system_prompt = (
        "Eres un asistente útil que responde preguntas basándose en el contexto proporcionado y el historial de la conversación. "
        "IMPORTANTE: Si la pregunta hace referencia a alguien o algo mencionado anteriormente en la conversación, usa esa información del contexto para entender a qué se refiere la pregunta. "
        "Intenta entender la pregunta y responderla con la información del contexto. "
        "Trata de ser conciso y directo en la respuesta. "
        "Si no sabes la respuesta de la pregunta, debes decir que no lo sabes y no intentes adivinar. "
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
    _chain_cache = create_retrieval_chain(retriever, question_answer_chain)
    
    return _chain_cache

def tirar_dados():
    """Tira dos dados y retorna el resultado."""
    dice1 = random.randint(1, 6)
    dice2 = random.randint(1, 6)
    return f'🎲 ¡Tirando los dados! 🎲\n🎲 Resultado: {dice1} y {dice2} 🎲'

def girar_ruleta():
    """Gira la ruleta y retorna el resultado."""
    colors = ['rojo', 'negro', 'verde']
    result = random.choice(colors)
    number = random.randint(0, 36)
    if number == 0:
        return f'🎰 Resultado: {number} Verde 🎰'
    else:
        return f'🎰 Resultado: {result} {number} 🎰'

def lanzar_moneda():
    """Lanza una moneda y retorna el resultado."""
    result = random.choice(['cara', 'cruz'])
    return f'🪙 ¡Lanzando la moneda! Resultado: {result} 🪙'

def mensaje_ayuda():
    """Retorna el mensaje de ayuda con los comandos disponibles."""
    return (
        "¡Hola! Aquí están los comandos disponibles:\n"
        "!dados - Tira los dados.\n"
        "!ruleta - Gira la ruleta.\n"
        "!coinflip - Lanza una moneda.\n"
        "!help - Muestra este mensaje de ayuda."
    )

def chat(prompt: str, user_id: str = "default", roles=None, history_limit: int = 10) -> str:
    """
    Función principal de chat que maneja las conversaciones con el bot.
    
    Args:
        prompt (str): Mensaje del usuario
        user_id (str): ID del usuario para memoria
        roles (list): Roles del usuario en Discord
        history_limit (int): Límite de historial a mantener
        
    Returns:
        str: Respuesta del bot
    """
    global USER_MEMORIES
    
    try:
        # Obtener memoria del usuario
        memory = USER_MEMORIES.get(user_id)
        if memory is None:
            memory = ConversationBufferMemory(return_messages=True)
            USER_MEMORIES[user_id] = memory

        # Obtener historial de memoria
        mem_vars = memory.load_memory_variables({})
        history = mem_vars.get("chat_history", "")
        
        # Obtener chain (usando cache)
        chain = get_chain()
        
        # Asignar memoria si el chain lo permite
        if hasattr(chain, 'memory'):
            chain.memory = memory

        # Construir el prompt completo
        roles_info = ""
        if roles:
            roles_info = f"Roles del usuario: {', '.join([str(r) for r in roles])}\n"
        
        if history:
            full_prompt = f"{roles_info}{history}\nUSUARIO: {prompt}\n"
        else:
            full_prompt = f"{roles_info}USUARIO: {prompt}\n"

        # Crear el contexto con el historial
        context_with_history = {
            "input": full_prompt,
            "history": history if history else "No hay historial previo."
        }

        # Usar el retriever mejorado con el historial (solo si hay historial)
        if history:
            set_history(history)
            relevant_docs = get_enhanced_documents(prompt)
            if relevant_docs:
                context_text = "\n".join([doc.page_content for doc in relevant_docs])
                context_with_history["context"] = context_text

        # Procesar con el chain
        result = chain.invoke(context_with_history)
        response_text = result.get("answer") or str(result)

        # Actualizar memoria
        memory.chat_memory.add_user_message(prompt)
        memory.chat_memory.add_ai_message(response_text)

        # Añadir aviso si es necesario
        aviso = '📚 *Esta respuesta utiliza información de la base de conocimiento.*\n\n'
        if isinstance(response_text, str) and not response_text.startswith(aviso):
            return aviso + response_text
        return str(response_text)
        
    except Exception as e:
        # Manejo de errores
        error_msg = f"❌ Error procesando tu mensaje: {str(e)}"
        print(f"Error en chat: {e}")
        return error_msg
