
"""
Módulo RAG usando LangChain y FAISS para búsqueda semántica en base.txt
"""

from pathlib import Path
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.schema import Document

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
retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
