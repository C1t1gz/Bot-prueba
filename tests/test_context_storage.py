#!/usr/bin/env python3
"""
Script de prueba para verificar el sistema de almacenamiento de contextos
"""

import sys
import os
import time
from datetime import datetime

# Agregar el directorio padre al path para importar módulos del proyecto
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.utils.context_storage import context_storage, QueryContext
from src.utils.logger import logger

def test_context_storage():
    """Prueba el sistema de almacenamiento de contextos"""
    print("🧪 Probando el sistema de almacenamiento de contextos...\n")
    
    try:
        # Crear contextos de prueba
        test_contexts = [
            QueryContext(
                user_id="test_user_1",
                username="UsuarioPrueba1",
                prompt="¿Qué es Python?",
                response="Python es un lenguaje de programación...",
                timestamp=time.time(),
                roles=["member"],
                documents_used=["base.txt"],
                processing_time=1.5,
                model_used="gpt-4o-mini",
                interaction_token="test_token_1",
                guild_id="test_guild_1",
                channel_id="test_channel_1"
            ),
            QueryContext(
                user_id="test_user_2",
                username="UsuarioPrueba2",
                prompt="¿Cómo funciona el RAG?",
                response="RAG significa Retrieval-Augmented Generation...",
                timestamp=time.time(),
                roles=["admin", "member"],
                documents_used=["base.txt", "docs/README.md"],
                processing_time=2.1,
                model_used="gpt-4o-mini",
                interaction_token="test_token_2",
                guild_id="test_guild_1",
                channel_id="test_channel_1"
            ),
            QueryContext(
                user_id="test_user_1",
                username="UsuarioPrueba1",
                prompt="¿Cuáles son las mejores prácticas?",
                response="Las mejores prácticas incluyen...",
                timestamp=time.time(),
                roles=["member"],
                documents_used=["docs/README.md"],
                processing_time=0.8,
                model_used="gpt-4o-mini",
                interaction_token="test_token_3",
                guild_id="test_guild_1",
                channel_id="test_channel_1"
            )
        ]
        
        # Almacenar contextos de prueba
        print("📝 Almacenando contextos de prueba...")
        for i, context in enumerate(test_contexts, 1):
            success = context_storage.store_context(context)
            if success:
                print(f"  ✅ Contexto {i} almacenado correctamente")
            else:
                print(f"  ❌ Error almacenando contexto {i}")
        
        # Obtener estadísticas
        print("\n📊 Obteniendo estadísticas...")
        stats = context_storage.get_query_statistics()
        print(f"  📈 Total de consultas: {stats['total_queries']}")
        print(f"  👥 Usuarios únicos: {stats['unique_users']}")
        print(f"  ⏱️  Tiempo promedio: {stats['average_processing_time']:.2f}s")
        
        # Verificar usuarios más activos
        if stats['top_users']:
            print("\n👑 Usuarios más activos:")
            for user in stats['top_users'][:3]:
                print(f"  - {user['username']}: {user['count']} consultas")
        
        # Obtener contextos de un usuario específico
        print("\n🔍 Obteniendo contextos del usuario test_user_1...")
        user_contexts = context_storage.get_user_contexts("test_user_1", limit=5)
        print(f"  📋 Encontrados {len(user_contexts)} contextos")
        
        for i, ctx in enumerate(user_contexts, 1):
            print(f"    {i}. {ctx.prompt[:50]}...")
        
        # Exportar contextos
        print("\n📤 Exportando contextos...")
        export_file = context_storage.export_contexts()
        if export_file:
            print(f"  ✅ Contextos exportados a: {export_file}")
        else:
            print("  ❌ Error exportando contextos")
        
        print("\n✅ Todas las pruebas completadas exitosamente!")
        
    except Exception as e:
        logger.error(f"Error en pruebas de almacenamiento de contextos: {e}")
        print(f"❌ Error: {e}")

def test_performance():
    """Prueba el rendimiento del sistema de almacenamiento"""
    print("\n⚡ Probando rendimiento del sistema...\n")
    
    try:
        import time
        
        # Medir tiempo de almacenamiento
        start_time = time.time()
        
        for i in range(100):
            context = QueryContext(
                user_id=f"perf_user_{i % 10}",
                username=f"UsuarioPerf{i % 10}",
                prompt=f"Consulta de rendimiento #{i}",
                response=f"Respuesta de rendimiento #{i}",
                timestamp=time.time(),
                roles=["member"],
                documents_used=["base.txt"],
                processing_time=0.5,
                model_used="gpt-4o-mini",
                interaction_token=f"perf_token_{i}",
                guild_id="perf_guild",
                channel_id="perf_channel"
            )
            context_storage.store_context(context)
        
        storage_time = time.time() - start_time
        print(f"📝 Tiempo para almacenar 100 contextos: {storage_time:.2f}s")
        print(f"📊 Promedio por contexto: {(storage_time/100)*1000:.2f}ms")
        
        # Medir tiempo de obtención de estadísticas
        start_time = time.time()
        stats = context_storage.get_query_statistics()
        stats_time = time.time() - start_time
        print(f"📊 Tiempo para obtener estadísticas: {stats_time:.2f}s")
        
        print(f"📈 Total de consultas en estadísticas: {stats['total_queries']}")
        
        print("\n✅ Pruebas de rendimiento completadas!")
        
    except Exception as e:
        logger.error(f"Error en pruebas de rendimiento: {e}")
        print(f"❌ Error: {e}")

def main():
    """Función principal"""
    print("🚀 Iniciando pruebas del sistema de almacenamiento de contextos")
    print("=" * 60)
    
    # Ejecutar pruebas básicas
    test_context_storage()
    
    # Ejecutar pruebas de rendimiento
    test_performance()
    
    print("\n" + "=" * 60)
    print("🎉 Todas las pruebas completadas!")

if __name__ == "__main__":
    main()
