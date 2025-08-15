
"""
Módulo RAG usando LangChain y FAISS para búsqueda semántica en base.txt
"""

from pathlib import Path
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.schema import Document
from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors import LLMChainExtractor

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

embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
documents = load_documents()
vectorstore = FAISS.from_documents(documents, embeddings)

# Configurar un retriever más inteligente con compresión contextual
base_retriever = vectorstore.as_retriever(search_kwargs={"k": 5})

# Crear un retriever con compresión contextual para mejorar la relevancia
def create_contextual_retriever():
    """
    Crea un retriever con compresión contextual para mejorar la relevancia de los resultados.
    """
    try:
        from langchain_google_genai import ChatGoogleGenerativeAI
        import os
        from dotenv import load_dotenv
        
        load_dotenv()
        api_key = os.getenv("GOOGLE_API_KEY")
        
        if api_key:
            llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", google_api_key=api_key)
            compressor_prompt = """
            Dado el siguiente contexto de conversación y la pregunta del usuario, 
            determina qué información del contexto es más relevante para responder la pregunta.
            
            Contexto de conversación: {context}
            Pregunta del usuario: {question}
            
            Responde solo con la información más relevante del contexto que ayude a responder la pregunta.
            """
            
            compressor = LLMChainExtractor.from_llm(llm)
            contextual_retriever = ContextualCompressionRetriever(
                base_compressor=compressor,
                base_retriever=base_retriever
            )
            return contextual_retriever
        else:
            print("⚠️ No se encontró GOOGLE_API_KEY, usando retriever básico")
            return base_retriever
    except Exception as e:
        print(f"⚠️ Error creando retriever contextual: {e}, usando retriever básico")
        return base_retriever

retriever = create_contextual_retriever()
