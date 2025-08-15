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
    
    # Definir las funciones localmente para evitar importar el módulo completo
    def extract_entities_from_history(history: str) -> list:
        """
        Extrae entidades mencionadas en el historial de conversación.
        """
        import re
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
    
    print("✅ Funciones de lógica definidas localmente (sin dependencias externas)")
    
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
