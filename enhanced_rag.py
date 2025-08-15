"""
Módulo RAG mejorado para manejar mejor el contexto y las referencias a entidades
"""

from pathlib import Path
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.schema import Document
import re

BASE_PATH = Path(__file__).parent / "base.txt"

def load_documents():
    """
    Carga base.txt y lo convierte en una lista de Documentos para LangChain.
    """
    if not BASE_PATH.exists():
        print("⚠️ No se encontró base.txt")
        return []
    with open(BASE_PATH, 'r', encoding='utf-8') as f:
        return [Document(page_content=line.strip()) for line in f if line.strip() and not line.strip().startswith('#')]

def extract_entities_from_history(history: str) -> list:
    """
    Extrae entidades mencionadas en el historial de conversación.
    """
    entities = []
    if history and isinstance(history, str):
        # Buscar nombres propios (palabras que empiezan con mayúscula)
        words = re.findall(r'\b[A-Z][a-z]+\b', history)
        entities.extend(words)
    return list(set(entities))

def enhance_query_with_context(query: str, history: str) -> str:
    """
    Mejora la consulta agregando contexto del historial.
    """
    if not history or not isinstance(history, str):
        return query
    
    # Extraer entidades del historial
    entities = extract_entities_from_history(history)
    
    # Si la consulta no menciona una entidad específica pero hay entidades en el historial
    # y la consulta parece referirse a una persona, agregar la entidad más reciente
    if entities and not any(entity.lower() in query.lower() for entity in entities):
        # Detectar si la consulta se refiere a una persona
        person_indicators = ['quién', 'quien', 'cuándo', 'cuando', 'dónde', 'donde', 'qué', 'que', 'cómo', 'como']
        if any(indicator in query.lower() for indicator in person_indicators):
            # Agregar la entidad más reciente al contexto
            enhanced_query = f"{query} (refiriéndose a {entities[-1]})"
            return enhanced_query
    
    return query

embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
documents = load_documents()
vectorstore = FAISS.from_documents(documents, embeddings)

# Configurar un retriever básico
base_retriever = vectorstore.as_retriever(search_kwargs={"k": 5})

# Variable global para almacenar el historial
_current_history = ""

def set_history(history: str):
    """
    Establece el historial de conversación para el contexto.
    """
    global _current_history
    _current_history = history

def get_enhanced_documents(query: str) -> list:
    """
    Obtiene documentos relevantes considerando el contexto del historial.
    """
    global _current_history
    
    # Mejorar la consulta con el contexto
    enhanced_query = enhance_query_with_context(query, _current_history)
    
    # Obtener documentos del retriever base usando invoke (método actualizado)
    docs = base_retriever.invoke(enhanced_query)
    
    # Si no hay documentos relevantes y hay entidades en el historial,
    # intentar buscar con las entidades del historial
    if not docs and _current_history:
        entities = extract_entities_from_history(_current_history)
        if entities:
            for entity in entities:
                entity_docs = base_retriever.invoke(entity)
                if entity_docs:
                    docs.extend(entity_docs)
                    break
    
    return docs[:5]  # Limitar a 5 documentos

# Función para obtener el retriever básico (compatible con LangChain)
def get_retriever():
    """
    Retorna el retriever básico de FAISS.
    """
    return base_retriever
