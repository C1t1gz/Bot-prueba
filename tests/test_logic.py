"""
Script de prueba para verificar la lógica de mejora de consultas
"""

import sys
import os

# Agregar el directorio padre al path para importar módulos del proyecto principal
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_enhance_query_logic():
    """
    Prueba la lógica de mejora de consultas sin depender de LangChain.
    """
    print("🧪 Probando la lógica de mejora de consultas...\n")
    
    # Importar las funciones de enhanced_rag
    try:
        from enhanced_rag import enhance_query_with_context, extract_entities_from_history
        print("✅ Módulo enhanced_rag importado correctamente")
    except ImportError as e:
        print(f"❌ Error importando enhanced_rag: {e}")
        print("💡 Asegúrate de ejecutar este script desde la carpeta tests/")
        return
    
    # Casos de prueba
    test_cases = [
        {
            "query": "¿quién es joaquin?",
            "history": "",
            "expected_enhancement": False
        },
        {
            "query": "¿cuándo nació?",
            "history": "Usuario: ¿quién es Joaquín?\nAsistente: Joaquín es el creador del bot.",
            "expected_enhancement": True
        },
        {
            "query": "¿qué le gusta?",
            "history": "Usuario: ¿quién es Joaquín?\nAsistente: Joaquín es el creador del bot.",
            "expected_enhancement": True
        },
        {
            "query": "¿dónde vive?",
            "history": "Usuario: ¿quién es Joaquín?\nAsistente: Joaquín es el creador del bot.",
            "expected_enhancement": True
        }
    ]
    
    print("📋 Ejecutando casos de prueba:\n")
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"Prueba {i}:")
        print(f"  Consulta: '{test_case['query']}'")
        print(f"  Historial: '{test_case['history']}'")
        
        # Extraer entidades del historial
        entities = extract_entities_from_history(test_case['history'])
        print(f"  Entidades encontradas: {entities}")
        
        # Mejorar la consulta
        enhanced_query = enhance_query_with_context(test_case['query'], test_case['history'])
        print(f"  Consulta mejorada: '{enhanced_query}'")
        
        # Verificar si se mejoró
        was_enhanced = enhanced_query != test_case['query']
        expected = test_case['expected_enhancement']
        
        if was_enhanced == expected:
            print(f"  ✅ Resultado: CORRECTO")
        else:
            print(f"  ❌ Resultado: INCORRECTO (esperado: {expected}, obtenido: {was_enhanced})")
        
        print()
    
    print("🎯 Pruebas de extracción de entidades:")
    
    # Probar extracción de entidades
    test_histories = [
        "Usuario: ¿quién es Joaquín?",
        "Usuario: ¿quién es Joaquín?\nAsistente: Joaquín es el creador del bot.",
        "Usuario: ¿qué hace María?\nAsistente: María es programadora.",
        "Usuario: ¿dónde vive Pedro?\nAsistente: Pedro vive en Madrid."
    ]
    
    for i, history in enumerate(test_histories, 1):
        entities = extract_entities_from_history(history)
        print(f"  Historial {i}: {entities}")
    
    print("\n🎉 Pruebas completadas!")

if __name__ == "__main__":
    test_enhance_query_logic()
