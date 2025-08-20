"""
Script para probar el tiempo de respuesta del sistema RAG
"""

import time
import sys
from pathlib import Path

# Agregar el directorio padre al path
sys.path.append(str(Path(__file__).parent))

def test_response_time():
    """Prueba el tiempo de respuesta del sistema RAG."""
    print("🧪 Probando tiempo de respuesta del sistema RAG...\n")
    
    try:
        from src.core.chat import chat
        
        # Primera pregunta (sin historial)
        print("1️⃣ Primera pregunta (sin historial):")
        start_time = time.time()
        
        response1 = chat("¿quién es joaquin?", user_id="test_user")
        
        end_time = time.time()
        response_time = end_time - start_time
        
        print(f"   Tiempo de respuesta: {response_time:.2f} segundos")
        print(f"   Respuesta: {response1[:100]}...")
        
        # Segunda pregunta (con historial)
        print(f"\n2️⃣ Segunda pregunta (con historial):")
        start_time = time.time()
        
        response2 = chat("¿cuándo nació?", user_id="test_user")
        
        end_time = time.time()
        response_time = end_time - start_time
        
        print(f"   Tiempo de respuesta: {response_time:.2f} segundos")
        print(f"   Respuesta: {response2[:100]}...")
        
        # Tercera pregunta (con más historial)
        print(f"\n3️⃣ Tercera pregunta (con más historial):")
        start_time = time.time()
        
        response3 = chat("¿qué le gusta?", user_id="test_user")
        
        end_time = time.time()
        response_time = end_time - start_time
        
        print(f"   Tiempo de respuesta: {response_time:.2f} segundos")
        print(f"   Respuesta: {response3[:100]}...")
        
        # Análisis
        print(f"\n📊 Análisis de tiempos:")
        if response_time < 3.0:
            print("✅ Tiempo de respuesta aceptable (< 3 segundos)")
        else:
            print("⚠️ Tiempo de respuesta lento (> 3 segundos)")
            print("💡 Considera optimizar el sistema RAG")
            
        print(f"\n🎯 El sistema está listo para Discord con respuestas diferidas")
        
    except Exception as e:
        print(f"❌ Error en la prueba: {e}")
        return False
    
    return True

if __name__ == "__main__":
    test_response_time()
