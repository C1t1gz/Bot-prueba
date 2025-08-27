#!/usr/bin/env python3
"""
Script para analizar las estadísticas de contextos almacenados
"""

import sys
import os
from pathlib import Path

# Agregar el directorio padre al path para importar módulos del proyecto
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.utils.context_storage import context_storage
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

def analyze_contexts():
    """Función principal para analizar contextos"""
    print_header("ANÁLISIS DE CONTEXTOS DE CONSULTAS")
    
    try:
        # Obtener estadísticas
        stats = context_storage.get_query_statistics()
        
        # Estadísticas generales
        print_section("ESTADÍSTICAS GENERALES")
        print(f"📈 Total de consultas: {stats['total_queries']:,}")
        print(f"👥 Usuarios únicos: {stats['unique_users']:,}")
        print(f"⏱️  Tiempo promedio de procesamiento: {stats['average_processing_time']:.2f}s")
        print(f"🕒 Última actualización: {stats['last_updated']}")
        
        # Usuarios más activos
        if stats['top_users']:
            print_section("USUARIOS MÁS ACTIVOS")
            for i, user in enumerate(stats['top_users'][:10], 1):
                print(f"{i:2d}. {user['username']} ({user['user_id']}) - {user['count']} consultas")
        
        # Consultas más comunes
        if stats['top_queries']:
            print_section("PALABRAS CLAVE MÁS COMUNES")
            for i, query in enumerate(stats['top_queries'][:15], 1):
                print(f"{i:2d}. '{query['keyword']}' - {query['count']} veces")
        
        # Consultas por hora del día
        if stats['queries_by_hour']:
            print_section("CONSULTAS POR HORA DEL DÍA")
            for hour in sorted(stats['queries_by_hour'].keys()):
                count = stats['queries_by_hour'][hour]
                bar = "█" * min(count // 5, 20)  # Barra de progreso
                print(f"{hour:02d}:00 - {count:3d} consultas {bar}")
        
        # Consultas por día de la semana
        if stats['queries_by_day']:
            print_section("CONSULTAS POR DÍA DE LA SEMANA")
            days_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
            for day in days_order:
                if day in stats['queries_by_day']:
                    count = stats['queries_by_day'][day]
                    bar = "█" * min(count // 3, 15)  # Barra de progreso
                    print(f"{day:10} - {count:3d} consultas {bar}")
        
        # Información adicional
        print_section("INFORMACIÓN ADICIONAL")
        print("💾 Los contextos se almacenan en: data/contexts/")
        print("📄 Formato: JSONL (una línea por consulta)")
        print("🔄 Cache de estadísticas: 5 minutos")
        print("🧹 Limpieza automática: 30 días por defecto")
        
    except Exception as e:
        logger.error(f"Error analizando contextos: {e}")
        print(f"❌ Error: {e}")

def export_contexts():
    """Exporta todos los contextos a un archivo JSON"""
    print_header("EXPORTAR CONTEXTOS")
    
    try:
        output_file = context_storage.export_contexts()
        if output_file:
            print(f"✅ Contextos exportados exitosamente a: {output_file}")
        else:
            print("❌ Error exportando contextos")
    except Exception as e:
        logger.error(f"Error exportando contextos: {e}")
        print(f"❌ Error: {e}")

def show_user_contexts(user_id: str, limit: int = 10):
    """Muestra los contextos de un usuario específico"""
    print_header(f"CONTEXTOS DEL USUARIO {user_id}")
    
    try:
        contexts = context_storage.get_user_contexts(user_id, limit)
        
        if not contexts:
            print(f"❌ No se encontraron contextos para el usuario {user_id}")
            return
        
        print(f"📋 Mostrando los últimos {len(contexts)} contextos:")
        
        for i, ctx in enumerate(contexts, 1):
            print(f"\n{i}. Consulta #{i}")
            print(f"   📝 Prompt: {ctx.prompt[:100]}{'...' if len(ctx.prompt) > 100 else ''}")
            print(f"   ⏰ Fecha: {ctx.timestamp}")
            print(f"   ⏱️  Tiempo: {ctx.processing_time:.2f}s")
            print(f"   📚 Documentos: {len(ctx.documents_used)}")
            if ctx.documents_used:
                print(f"      - {', '.join(ctx.documents_used[:3])}{'...' if len(ctx.documents_used) > 3 else ''}")
        
    except Exception as e:
        logger.error(f"Error mostrando contextos del usuario: {e}")
        print(f"❌ Error: {e}")

def cleanup_old_contexts(days: int = 30):
    """Limpia contextos antiguos"""
    print_header(f"LIMPIAR CONTEXTOS ANTIGUOS (> {days} días)")
    
    try:
        removed_count = context_storage.cleanup_old_contexts(days)
        print(f"✅ Limpieza completada: {removed_count} contextos eliminados")
    except Exception as e:
        logger.error(f"Error limpiando contextos: {e}")
        print(f"❌ Error: {e}")

def main():
    """Función principal del script"""
    if len(sys.argv) < 2:
        print("Uso: python analyze_contexts.py [comando] [opciones]")
        print("\nComandos disponibles:")
        print("  stats                    - Mostrar estadísticas generales")
        print("  export                   - Exportar contextos a JSON")
        print("  user <user_id> [limit]   - Mostrar contextos de un usuario")
        print("  cleanup [days]           - Limpiar contextos antiguos")
        print("\nEjemplos:")
        print("  python analyze_contexts.py stats")
        print("  python analyze_contexts.py user 123456789 5")
        print("  python analyze_contexts.py cleanup 30")
        return
    
    command = sys.argv[1].lower()
    
    if command == "stats":
        analyze_contexts()
    elif command == "export":
        export_contexts()
    elif command == "user":
        if len(sys.argv) < 3:
            print("❌ Error: Debes especificar un user_id")
            return
        user_id = sys.argv[2]
        limit = int(sys.argv[3]) if len(sys.argv) > 3 else 10
        show_user_contexts(user_id, limit)
    elif command == "cleanup":
        days = int(sys.argv[2]) if len(sys.argv) > 2 else 30
        cleanup_old_contexts(days)
    else:
        print(f"❌ Comando no reconocido: {command}")

if __name__ == "__main__":
    main()
