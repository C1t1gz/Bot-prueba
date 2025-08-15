#!/usr/bin/env python3
"""
Script para verificar que la estructura del proyecto está correcta
"""

import os
import sys
from pathlib import Path

def verify_project_structure():
    """
    Verifica que la estructura del proyecto esté correcta.
    """
    print("🔍 Verificando estructura del proyecto...")
    
    # Directorio raíz del proyecto
    project_root = Path(__file__).parent.parent
    
    # Estructura esperada
    expected_structure = {
        "src": {
            "core": ["__init__.py", "chat.py"],
            "rag": ["__init__.py", "enhanced_rag.py"],
            "discord": ["__init__.py", "client.py"],
            "utils": ["__init__.py", "security.py"],
            "__init__.py": None
        },
        "data": ["base.txt"],
        "config": ["settings.py"],
        "scripts": ["run_bot.py", "cleanup.py", "verify_structure.py"],
        "docs": ["README.md"],
        "tests": ["__init__.py", "README.md"],
        "legacy": ["README.md"],
        "main.py": None,
        "requirements.txt": None,
        "README.md": None,
        ".gitignore": None
    }
    
    errors = []
    warnings = []
    
    # Verificar estructura
    for item, expected in expected_structure.items():
        item_path = project_root / item
        
        if not item_path.exists():
            errors.append(f"❌ Falta: {item}")
            continue
            
        if expected is None:
            # Es un archivo
            if not item_path.is_file():
                errors.append(f"❌ {item} debería ser un archivo")
        else:
            # Es un directorio
            if not item_path.is_dir():
                errors.append(f"❌ {item} debería ser un directorio")
            else:
                # Verificar contenido del directorio
                for subitem in expected:
                    subitem_path = item_path / subitem
                    if not subitem_path.exists():
                        warnings.append(f"⚠️ Falta: {item}/{subitem}")
    
    # Verificar imports básicos (sin dependencias externas)
    print("\n🔍 Verificando imports básicos...")
    try:
        # Agregar el directorio raíz al path
        sys.path.insert(0, str(project_root))
        
        # Verificar imports básicos que no requieren dependencias externas
        from config.settings import validate_config
        
        print("✅ Imports básicos funcionan correctamente")
        
    except ImportError as e:
        errors.append(f"❌ Error de import básico: {e}")
    
    # Verificar estructura de archivos sin importar
    print("🔍 Verificando estructura de archivos...")
    try:
        # Verificar que los archivos principales existen
        core_chat = project_root / "src" / "core" / "chat.py"
        rag_enhanced = project_root / "src" / "rag" / "enhanced_rag.py"
        discord_client = project_root / "src" / "discord" / "client.py"
        
        if not core_chat.exists():
            errors.append("❌ Falta: src/core/chat.py")
        if not rag_enhanced.exists():
            errors.append("❌ Falta: src/rag/enhanced_rag.py")
        if not discord_client.exists():
            errors.append("❌ Falta: src/discord/client.py")
            
        print("✅ Estructura de archivos verificada")
        
    except Exception as e:
        errors.append(f"❌ Error verificando archivos: {e}")
    
    # Mostrar resultados
    print(f"\n📊 Resultados de la verificación:")
    print(f"✅ Errores: {len(errors)}")
    print(f"⚠️ Advertencias: {len(warnings)}")
    
    if errors:
        print("\n❌ Errores encontrados:")
        for error in errors:
            print(f"  {error}")
    
    if warnings:
        print("\n⚠️ Advertencias:")
        for warning in warnings:
            print(f"  {warning}")
    
    if not errors and not warnings:
        print("\n🎉 ¡Estructura del proyecto verificada correctamente!")
        return True
    else:
        print("\n🔧 Por favor, corrige los errores antes de continuar.")
        return False

def verify_data_files():
    """
    Verifica que los archivos de datos estén correctos.
    """
    print("\n📁 Verificando archivos de datos...")
    
    project_root = Path(__file__).parent.parent
    data_file = project_root / "data" / "base.txt"
    
    if not data_file.exists():
        print("❌ Falta archivo data/base.txt")
        return False
    
    try:
        with open(data_file, 'r', encoding='utf-8') as f:
            content = f.read()
            if len(content.strip()) == 0:
                print("⚠️ El archivo data/base.txt está vacío")
                return False
            print(f"✅ data/base.txt encontrado con {len(content.split())} palabras")
            return True
    except Exception as e:
        print(f"❌ Error leyendo data/base.txt: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Verificación de estructura del proyecto PythonBots")
    print("=" * 50)
    
    structure_ok = verify_project_structure()
    data_ok = verify_data_files()
    
    if structure_ok and data_ok:
        print("\n🎉 ¡Proyecto listo para usar!")
        print("💡 Para ejecutar el bot: python scripts/run_bot.py")
    else:
        print("\n❌ Hay problemas que necesitan ser corregidos.")
        sys.exit(1)
