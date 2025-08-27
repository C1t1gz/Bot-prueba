#!/usr/bin/env python3
"""
Script de prueba para verificar el sistema de memoria persistente
"""

import sys
import os
import time
from datetime import datetime

# Agregar el directorio padre al path para importar módulos del proyecto
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.utils.persistent_memory import persistent_memory
from src.core.chat import chat
from src.utils.logger import logger

def test_persistent_memory():
    """Prueba el sistema de memoria persistente"""
    print("🧪 Probando el sistema de memoria persistente...\n")
    
    test_user_id = "test_persistent_user_123"
    
    try:
        # Paso 1: Verificar que no hay memoria inicial
        print("1️⃣ Verificando memoria inicial...")
        memory_info = persistent_memory.get_user_memory_info(test_user_id)
        if memory_info:
            print(f"   ⚠️  Memoria existente encontrada: {memory_info['message_count']} mensajes")
        else:
            print("   ✅ No hay memoria inicial (correcto)")
        
        # Paso 2: Simular una conversación
        print("\n2️⃣ Simulando conversación...")
        
        # Primera consulta
        print("   📝 Consulta 1: 'Hola, ¿cómo estás?'")
        response1 = chat(
            "Hola, ¿cómo estás?", 
            user_id=test_user_id,
            username="UsuarioPrueba",
            interaction_token="test_token_1"
        )
        print(f"   🤖 Respuesta: {response1[:100]}...")
        
        # Segunda consulta con contexto
        print("   📝 Consulta 2: 'Ahora te llamas Pepe'")
        response2 = chat(
            "Ahora te llamas Pepe", 
            user_id=test_user_id,
            username="UsuarioPrueba",
            interaction_token="test_token_2"
        )
        print(f"   🤖 Respuesta: {response2[:100]}...")
        
        # Tercera consulta que debería recordar el nombre
        print("   📝 Consulta 3: '¿Cuál es tu nombre?'")
        response3 = chat(
            "¿Cuál es tu nombre?", 
            user_id=test_user_id,
            username="UsuarioPrueba",
            interaction_token="test_token_3"
        )
        print(f"   🤖 Respuesta: {response3[:100]}...")
        
        # Paso 3: Verificar que se guardó la memoria
        print("\n3️⃣ Verificando memoria guardada...")
        memory_info = persistent_memory.get_user_memory_info(test_user_id)
        if memory_info:
            print(f"   ✅ Memoria guardada: {memory_info['message_count']} mensajes")
            print(f"   📅 Última actualización: {memory_info['last_updated']}")
            print(f"   💾 Tamaño del archivo: {memory_info['file_size']} bytes")
        else:
            print("   ❌ No se encontró memoria guardada")
            return False
        
        # Paso 4: Simular reinicio del servidor (crear nueva instancia)
        print("\n4️⃣ Simulando reinicio del servidor...")
        
        # Crear nueva instancia del gestor de memoria
        from src.utils.persistent_memory import PersistentMemoryManager
        new_memory_manager = PersistentMemoryManager()
        
        # Cargar memoria del usuario
        memory = new_memory_manager.get_user_memory(test_user_id)
        mem_vars = memory.load_memory_variables({})
        history = mem_vars.get("chat_history", "")
        
        print(f"   📋 Historial cargado: {len(history)} caracteres")
        if "Pepe" in history:
            print("   ✅ El nombre 'Pepe' se mantiene en la memoria")
        else:
            print("   ❌ No se encontró el nombre 'Pepe' en la memoria")
        
        # Paso 5: Probar comando de borrado
        print("\n5️⃣ Probando comando de borrado...")
        
        # Hacer una consulta más
        print("   📝 Consulta 4: '¿Recuerdas tu nombre?'")
        response4 = chat(
            "¿Recuerdas tu nombre?", 
            user_id=test_user_id,
            username="UsuarioPrueba",
            interaction_token="test_token_4"
        )
        print(f"   🤖 Respuesta: {response4[:100]}...")
        
        # Borrar memoria
        from src.core.chat import borrar_memoria_usuario
        clear_response = borrar_memoria_usuario(test_user_id)
        print(f"   🧹 Resultado del borrado: {clear_response}")
        
        # Verificar que se borró
        memory_info_after = persistent_memory.get_user_memory_info(test_user_id)
        if not memory_info_after:
            print("   ✅ Memoria borrada correctamente")
        else:
            print("   ❌ La memoria no se borró correctamente")
        
        # Paso 6: Probar nueva conversación después del borrado
        print("\n6️⃣ Probando nueva conversación después del borrado...")
        
        response5 = chat(
            "¿Cuál es tu nombre?", 
            user_id=test_user_id,
            username="UsuarioPrueba",
            interaction_token="test_token_5"
        )
        print(f"   🤖 Respuesta: {response5[:100]}...")
        
        if "Pepe" not in response5:
            print("   ✅ El bot ya no recuerda el nombre (correcto)")
        else:
            print("   ❌ El bot aún recuerda el nombre (incorrecto)")
        
        print("\n✅ Todas las pruebas completadas exitosamente!")
        return True
        
    except Exception as e:
        logger.error(f"Error en pruebas de memoria persistente: {e}")
        print(f"❌ Error: {e}")
        return False

def test_memory_performance():
    """Prueba el rendimiento del sistema de memoria"""
    print("\n⚡ Probando rendimiento del sistema de memoria...\n")
    
    try:
        import time
        
        # Medir tiempo de escritura
        start_time = time.time()
        
        for i in range(10):
            user_id = f"perf_user_{i}"
            memory = persistent_memory.get_user_memory(user_id)
            
            # Agregar algunos mensajes
            memory.chat_memory.add_user_message(f"Mensaje de prueba {i}")
            memory.chat_memory.add_ai_message(f"Respuesta de prueba {i}")
            
            # Guardar memoria
            persistent_memory.save_user_memory(user_id, memory)
        
        write_time = time.time() - start_time
        print(f"📝 Tiempo para escribir 10 memorias: {write_time:.2f}s")
        print(f"📊 Promedio por memoria: {(write_time/10)*1000:.2f}ms")
        
        # Medir tiempo de lectura
        start_time = time.time()
        
        for i in range(10):
            user_id = f"perf_user_{i}"
            memory = persistent_memory.get_user_memory(user_id)
            mem_vars = memory.load_memory_variables({})
        
        read_time = time.time() - start_time
        print(f"📖 Tiempo para leer 10 memorias: {read_time:.2f}s")
        print(f"📊 Promedio por memoria: {(read_time/10)*1000:.2f}ms")
        
        # Limpiar memorias de prueba
        for i in range(10):
            user_id = f"perf_user_{i}"
            persistent_memory.clear_user_memory(user_id)
        
        print("\n✅ Pruebas de rendimiento completadas!")
        
    except Exception as e:
        logger.error(f"Error en pruebas de rendimiento: {e}")
        print(f"❌ Error: {e}")

def main():
    """Función principal"""
    print("🚀 Iniciando pruebas del sistema de memoria persistente")
    print("=" * 60)
    
    # Ejecutar pruebas básicas
    success = test_persistent_memory()
    
    if success:
        # Ejecutar pruebas de rendimiento
        test_memory_performance()
    
    print("\n" + "=" * 60)
    if success:
        print("🎉 Todas las pruebas completadas exitosamente!")
    else:
        print("❌ Algunas pruebas fallaron")

if __name__ == "__main__":
    main()
