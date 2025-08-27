#!/usr/bin/env python3
"""
Script para gestionar las memorias persistentes de los usuarios
"""

import sys
import os
from pathlib import Path

# Agregar el directorio padre al path para importar módulos del proyecto
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.utils.persistent_memory import persistent_memory
from src.utils.logger import logger

def print_header(title: str):
    """Imprime un encabezado formateado"""
    print("\n" + "="*60)
    print(f"  {title}")
    print("="*60)

def print_section(title: str):
    """Imprime un título de sección"""
    print(f"\n📊 {title}")
    print("-" * 40)

def list_all_memories():
    """Lista todas las memorias de usuario"""
    print_header("MEMORIAS PERSISTENTES DE USUARIOS")
    
    try:
        memories = persistent_memory.get_all_memory_info()
        
        if not memories:
            print("📭 No hay memorias persistentes almacenadas")
            return
        
        print(f"📋 Total de usuarios con memoria: {len(memories)}")
        
        for i, memory in enumerate(memories, 1):
            print(f"\n{i}. Usuario: {memory['user_id']}")
            print(f"   📝 Mensajes: {memory['message_count']}")
            print(f"   📅 Última actualización: {memory['last_updated']}")
            print(f"   💾 Tamaño del archivo: {memory['file_size']} bytes")
        
    except Exception as e:
        logger.error(f"Error listando memorias: {e}")
        print(f"❌ Error: {e}")

def show_user_memory(user_id: str):
    """Muestra la memoria de un usuario específico"""
    print_header(f"MEMORIA DEL USUARIO {user_id}")
    
    try:
        memory_info = persistent_memory.get_user_memory_info(user_id)
        
        if not memory_info:
            print(f"❌ No se encontró memoria para el usuario {user_id}")
            return
        
        print(f"📝 Mensajes almacenados: {memory_info['message_count']}")
        print(f"📅 Última actualización: {memory_info['last_updated']}")
        print(f"💾 Tamaño del archivo: {memory_info['file_size']} bytes")
        
        # Mostrar algunos mensajes de ejemplo
        memory = persistent_memory.get_user_memory(user_id)
        messages = memory.chat_memory.messages
        
        if messages:
            print(f"\n📋 Últimos mensajes:")
            for i, msg in enumerate(messages[-5:], 1):  # Últimos 5 mensajes
                if hasattr(msg, 'content'):
                    content = msg.content[:100] + "..." if len(msg.content) > 100 else msg.content
                    print(f"   {i}. {content}")
        
    except Exception as e:
        logger.error(f"Error mostrando memoria del usuario {user_id}: {e}")
        print(f"❌ Error: {e}")

def clear_user_memory(user_id: str):
    """Borra la memoria de un usuario específico"""
    print_header(f"BORRAR MEMORIA DEL USUARIO {user_id}")
    
    try:
        # Verificar si existe la memoria
        memory_info = persistent_memory.get_user_memory_info(user_id)
        if not memory_info:
            print(f"❌ No se encontró memoria para el usuario {user_id}")
            return
        
        print(f"📝 Mensajes a borrar: {memory_info['message_count']}")
        print(f"📅 Última actualización: {memory_info['last_updated']}")
        
        # Confirmar borrado
        confirm = input("\n¿Estás seguro de que quieres borrar esta memoria? (s/N): ")
        if confirm.lower() != 's':
            print("❌ Operación cancelada")
            return
        
        success = persistent_memory.clear_user_memory(user_id)
        if success:
            print("✅ Memoria borrada exitosamente")
        else:
            print("❌ Error borrando la memoria")
        
    except Exception as e:
        logger.error(f"Error borrando memoria del usuario {user_id}: {e}")
        print(f"❌ Error: {e}")

def clear_all_memories():
    """Borra todas las memorias"""
    print_header("BORRAR TODAS LAS MEMORIAS")
    
    try:
        memories = persistent_memory.get_all_memory_info()
        
        if not memories:
            print("📭 No hay memorias para borrar")
            return
        
        print(f"📋 Total de memorias a borrar: {len(memories)}")
        total_messages = sum(m['message_count'] for m in memories)
        print(f"📝 Total de mensajes a borrar: {total_messages}")
        
        # Confirmar borrado
        confirm = input("\n¿Estás seguro de que quieres borrar TODAS las memorias? (s/N): ")
        if confirm.lower() != 's':
            print("❌ Operación cancelada")
            return
        
        # Borrar cada memoria
        success_count = 0
        for memory in memories:
            if persistent_memory.clear_user_memory(memory['user_id']):
                success_count += 1
        
        print(f"✅ {success_count}/{len(memories)} memorias borradas exitosamente")
        
    except Exception as e:
        logger.error(f"Error borrando todas las memorias: {e}")
        print(f"❌ Error: {e}")

def cleanup_old_memories(days: int = 30):
    """Limpia memorias antiguas"""
    print_header(f"LIMPIAR MEMORIAS ANTIGUAS (> {days} días)")
    
    try:
        removed_count = persistent_memory.cleanup_old_memories(days)
        print(f"✅ {removed_count} memorias antiguas eliminadas")
        
    except Exception as e:
        logger.error(f"Error limpiando memorias antiguas: {e}")
        print(f"❌ Error: {e}")

def main():
    """Función principal del script"""
    if len(sys.argv) < 2:
        print("Uso: python manage_memory.py [comando] [opciones]")
        print("\nComandos disponibles:")
        print("  list                    - Listar todas las memorias")
        print("  show <user_id>          - Mostrar memoria de un usuario")
        print("  clear <user_id>         - Borrar memoria de un usuario")
        print("  clear-all               - Borrar todas las memorias")
        print("  cleanup [days]          - Limpiar memorias antiguas")
        print("\nEjemplos:")
        print("  python manage_memory.py list")
        print("  python manage_memory.py show 123456789")
        print("  python manage_memory.py clear 123456789")
        print("  python manage_memory.py cleanup 30")
        return
    
    command = sys.argv[1].lower()
    
    if command == "list":
        list_all_memories()
    elif command == "show":
        if len(sys.argv) < 3:
            print("❌ Error: Debes especificar un user_id")
            return
        user_id = sys.argv[2]
        show_user_memory(user_id)
    elif command == "clear":
        if len(sys.argv) < 3:
            print("❌ Error: Debes especificar un user_id")
            return
        user_id = sys.argv[2]
        clear_user_memory(user_id)
    elif command == "clear-all":
        clear_all_memories()
    elif command == "cleanup":
        days = int(sys.argv[2]) if len(sys.argv) > 2 else 30
        cleanup_old_memories(days)
    else:
        print(f"❌ Comando no reconocido: {command}")

if __name__ == "__main__":
    main()
