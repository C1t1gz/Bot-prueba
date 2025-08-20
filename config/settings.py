"""
Configuraciones centralizadas del bot
"""

import os
from pathlib import Path
import dotenv

# Cargar variables de entorno
dotenv.load_dotenv()

# Rutas del proyecto
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
TESTS_DIR = BASE_DIR / "tests"
LEGACY_DIR = BASE_DIR / "legacy"

# Configuraciones de Discord
DISCORD_PUBLIC_KEY = os.getenv("DISCORD_PUBLIC_KEY")
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

# Configuraciones de API
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Configuraciones del modelo
MODEL_PROVIDER = "gemini"  # ollama, gemini y openai.
MODEL_NAME = "gemini-2.5-flash"  # gemini-2.5-flash, llama3.1, gpt-4o-mini
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

# Configuraciones del RAG
RAG_K_RESULTS = 5
HISTORY_LIMIT = 10

# Configuraciones del servidor
HOST = "0.0.0.0"
PORT = 8000

# Configuraciones de logging
LOG_LEVEL = "INFO"

# Validaciones
def validate_config():
    """
    Valida que todas las configuraciones necesarias estén presentes.
    
    Returns:
        bool: True si todas las configuraciones son válidas
    """
    required_vars = [
        "DISCORD_PUBLIC_KEY",
        "DISCORD_TOKEN", 
        "GOOGLE_API_KEY"
    ]
    
    missing_vars = []
    for var in required_vars:
        if not globals().get(var):
            missing_vars.append(var)
    
    if missing_vars:
        print(f"❌ Variables de entorno faltantes: {', '.join(missing_vars)}")
        print("💡 Asegúrate de configurar estas variables en tu archivo .env")
        return False
    
    return True
