"""
Script para probar el tiempo de respuesta del sistema RAG
"""

import time
import sys
from pathlib import Path

# Agregar el directorio raíz del proyecto al path
sys.path.append(str(Path(__file__).parent.parent))

from src.utils.logger import logger

def test_response_time():
    """Prueba el tiempo de respuesta del sistema RAG."""
    logger.info("🧪 Probando tiempo de respuesta del sistema RAG...")
    
    try:
        from src.core.chat import chat
        
        # Primera pregunta (sin historial)
        logger.info("1️⃣ Primera pregunta (sin historial):")
        start_time = time.time()
        
        response1 = chat("¿quién es joaquin?", user_id="test_user")
        
        end_time = time.time()
        response_time = end_time - start_time
        
        logger.info(f"   Tiempo de respuesta: {response_time:.2f} segundos")
        logger.info(f"   Respuesta: {response1[:100]}...")
        
        # Segunda pregunta (con historial)
        logger.info("2️⃣ Segunda pregunta (con historial):")
        start_time = time.time()
        
        response2 = chat("¿cuándo nació?", user_id="test_user")
        
        end_time = time.time()
        response_time = end_time - start_time
        
        logger.info(f"   Tiempo de respuesta: {response_time:.2f} segundos")
        logger.info(f"   Respuesta: {response2[:100]}...")
        
        # Tercera pregunta (con más historial)
        logger.info("3️⃣ Tercera pregunta (con más historial):")
        start_time = time.time()
        
        response3 = chat("¿qué le gusta?", user_id="test_user")
        
        end_time = time.time()
        response_time = end_time - start_time
        
        logger.info(f"   Tiempo de respuesta: {response_time:.2f} segundos")
        logger.info(f"   Respuesta: {response3[:100]}...")
        
        # Análisis
        logger.info("📊 Análisis de tiempos:")
        if response_time < 3.0:
            logger.success("✅ Tiempo de respuesta aceptable (< 3 segundos)")
        else:
            logger.warning("⚠️ Tiempo de respuesta lento (> 3 segundos)")
            logger.info("💡 Considera optimizar el sistema RAG")
            
        logger.success("🎯 El sistema está listo para Discord con respuestas diferidas")
        
    except Exception as e:
        logger.error(f"❌ Error en la prueba: {e}")
        return False
    
    return True

if __name__ == "__main__":
    test_response_time()
