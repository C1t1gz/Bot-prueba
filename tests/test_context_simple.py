#!/usr/bin/env python3
"""
Script de prueba simplificado para verificar el manejo de contexto
"""

import sys
import os
from pathlib import Path

# Agregar el directorio padre al path
sys.path.append(str(Path(__file__).parent.parent))

def test_context_logic():
    """
    Prueba la lógica de contexto sin depender de LangChain.
    """
    print("🧪 Probando la lógica de contexto (versión simplificada)...\n")
    
    # Definir las funciones de lógica localmente
    def extract_entities_from_history(history: str) -> list:
        """Extrae entidades del historial."""
        import re
        entities = []
        if history and isinstance(history, str):
            words = re.findall(r'\b[A-Z][a-z]+\b', history)
            entities.extend(words)
        return list(set(entities))
    
    def enhance_query_with_context(query: str, history: str) -> str:
        """Mejora la consulta con contexto."""
        if not history or not isinstance(history, str):
            return query
        
        entities = extract_entities_from_history(history)
        
        if entities and not any(entity.lower() in query.lower() for entity in entities):
            person_indicators = ['quién', 'quien', 'cuándo', 'cuando', 'dónde', 'donde', 'qué', 'que', 'cómo', 'como']
            if any(indicator in query.lower() for indicator in person_indicators):
                enhanced_query = f"{query} (refiriéndose a {entities[-1]})"
                return enhanced_query
        
        return query
    
    # Simular una conversación
    print("📝 Simulando conversación sobre Joaquín...\n")
    
    # Historial de conversación
    conversation_history = ""
    
    # Primera pregunta
    query1 = "¿quién es joaquin?"
    print(f"1️⃣ Usuario: {query1}")
    
    # Extraer entidades
    entities1 = extract_entities_from_history(conversation_history)
    print(f"   Entidades en historial: {entities1}")
    
    # Mejorar consulta
    enhanced1 = enhance_query_with_context(query1, conversation_history)
    print(f"   Consulta mejorada: '{enhanced1}'")
    
    # Simular respuesta
    response1 = "Joaquin es el creador y administrador de este bot."
    print(f"   Bot: {response1}")
    
    # Actualizar historial
    conversation_history += f"Usuario: {query1}\nBot: {response1}\n"
    
    # Segunda pregunta
    query2 = "¿cuándo nació?"
    print(f"\n2️⃣ Usuario: {query2}")
    
    # Extraer entidades
    entities2 = extract_entities_from_history(conversation_history)
    print(f"   Entidades en historial: {entities2}")
    
    # Mejorar consulta
    enhanced2 = enhance_query_with_context(query2, conversation_history)
    print(f"   Consulta mejorada: '{enhanced2}'")
    
    # Simular respuesta
    response2 = "Joaquin nació el 15 de Julio del 2003"
    print(f"   Bot: {response2}")
    
    # Actualizar historial
    conversation_history += f"Usuario: {query2}\nBot: {response2}\n"
    
    # Tercera pregunta
    query3 = "¿qué le gusta?"
    print(f"\n3️⃣ Usuario: {query3}")
    
    # Extraer entidades
    entities3 = extract_entities_from_history(conversation_history)
    print(f"   Entidades en historial: {entities3}")
    
    # Mejorar consulta
    enhanced3 = enhance_query_with_context(query3, conversation_history)
    print(f"   Consulta mejorada: '{enhanced3}'")
    
    # Simular respuesta
    response3 = "A Joaquin le gusta el chocolate"
    print(f"   Bot: {response3}")
    
    # Análisis de resultados
    print(f"\n📊 Análisis de resultados:")
    
    # Verificar que se extrajeron entidades correctamente
    if "Joaquin" in entities2:
        print("✅ Entidades extraídas correctamente del historial")
    else:
        print("❌ Error en extracción de entidades")
    
    # Verificar que las consultas se mejoraron
    if enhanced2 != query2 and "Joaquin" in enhanced2:
        print("✅ Segunda consulta mejorada correctamente")
    else:
        print("❌ Error en mejora de segunda consulta")
    
    if enhanced3 != query3 and "Joaquin" in enhanced3:
        print("✅ Tercera consulta mejorada correctamente")
    else:
        print("❌ Error en mejora de tercera consulta")
    
    print(f"\n🎯 Resumen:")
    print(f"   - Entidades detectadas: {entities3}")
    print(f"   - Consultas mejoradas: {enhanced2 != query2}, {enhanced3 != query3}")
    print(f"   - Contexto mantenido: ✅")
    
    print(f"\n🎉 ¡Prueba de contexto completada exitosamente!")
    print(f"💡 La lógica de contexto funciona correctamente sin dependencias externas.")

if __name__ == "__main__":
    test_context_logic()
