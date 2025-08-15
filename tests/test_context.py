"""
Script de prueba para verificar el manejo de contexto en el bot
"""

import sys
import os

# Agregar el directorio padre al path para importar módulos del proyecto principal
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv

# Cargar variables de entorno desde el directorio padre
load_dotenv(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.env'))

def test_context_handling():
    """
    Prueba el manejo de contexto con preguntas sobre Joaquín
    """
    print("🧪 Probando el manejo de contexto...\n")
    
    try:
        from timbero import chat
    except ImportError as e:
        print(f"❌ Error importando timbero: {e}")
        print("💡 Asegúrate de ejecutar este script desde la carpeta tests/")
        return
    
    # Simular una conversación
    user_id = "test_user_123"
    
    # Primera pregunta: "¿quién es joaquin?"
    print("1️⃣ Pregunta: ¿quién es joaquin?")
    response1 = chat("¿quién es joaquin?", user_id=user_id)
    print(f"Respuesta: {response1}\n")
    
    # Segunda pregunta: "¿cuándo nació?" (debería referirse a Joaquín)
    print("2️⃣ Pregunta: ¿cuándo nació?")
    response2 = chat("¿cuándo nació?", user_id=user_id)
    print(f"Respuesta: {response2}\n")
    
    # Tercera pregunta: "¿qué le gusta?" (debería referirse a Joaquín)
    print("3️⃣ Pregunta: ¿qué le gusta?")
    response3 = chat("¿qué le gusta?", user_id=user_id)
    print(f"Respuesta: {response3}\n")
    
    # Verificar si las respuestas contienen la información correcta
    print("📊 Análisis de resultados:")
    
    if "Joaquin es el creador" in response1:
        print("✅ Primera respuesta: CORRECTA")
    else:
        print("❌ Primera respuesta: INCORRECTA")
    
    if "15 de Julio del 2003" in response2:
        print("✅ Segunda respuesta: CORRECTA")
    else:
        print("❌ Segunda respuesta: INCORRECTA")
    
    if "chocolate" in response3:
        print("✅ Tercera respuesta: CORRECTA")
    else:
        print("❌ Tercera respuesta: INCORRECTA")

if __name__ == "__main__":
    # Verificar que la API key esté configurada
    if not os.getenv("GOOGLE_API_KEY"):
        print("❌ Error: GOOGLE_API_KEY no está configurada en el archivo .env")
        print("Por favor, configura tu API key de Google antes de ejecutar las pruebas.")
    else:
        test_context_handling()
