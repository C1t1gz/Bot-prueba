#!/usr/bin/env python3
"""
Script para ejecutar el bot de Discord
"""

import sys
import os
from pathlib import Path

# Agregar el directorio raíz al path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from config.settings import validate_config
import uvicorn
from main import app

def main():
    """
    Función principal para ejecutar el bot.
    """
    print("🚀 Iniciando PythonBots - Discord Bot...")
    
    # Validar configuraciones
    if not validate_config():
        print("❌ Error en la configuración. Verifica tu archivo .env")
        sys.exit(1)
    
    print("✅ Configuración válida")
    print("🌐 Iniciando servidor FastAPI...")
    
    try:
        # Ejecutar el servidor
        uvicorn.run(
            app,
            host="0.0.0.0",
            port=8000,
            log_level="info",
            reload=True
        )
    except KeyboardInterrupt:
        print("\n🛑 Bot detenido por el usuario")
    except Exception as e:
        print(f"❌ Error ejecutando el bot: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
