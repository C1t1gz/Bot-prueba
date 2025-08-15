"""
Script para verificar que todas las dependencias estén instaladas correctamente
"""

import importlib
import sys
import os

def check_dependency(module_name, package_name=None):
    """
    Verifica si una dependencia está instalada.
    """
    try:
        importlib.import_module(module_name)
        print(f"✅ {package_name or module_name}: INSTALADO")
        return True
    except ImportError:
        print(f"❌ {package_name or module_name}: NO INSTALADO")
        return False

def main():
    """
    Verifica todas las dependencias necesarias.
    """
    print("🔍 Verificando dependencias...\n")
    
    # Lista de dependencias a verificar
    dependencies = [
        ("langchain", "langchain"),
        ("langchain_core", "langchain-core"),
        ("langchain_community", "langchain-community"),
        ("langchain_google_genai", "langchain-google-genai"),
        ("langchain_huggingface", "langchain-huggingface"),
        ("faiss", "faiss-cpu"),
        ("sentence_transformers", "sentence-transformers"),
        ("discord", "discord.py"),
        ("fastapi", "fastapi"),
        ("uvicorn", "uvicorn"),
        ("dotenv", "python-dotenv"),
        ("pydantic", "pydantic"),
        ("pydantic_settings", "pydantic-settings"),
        ("nacl", "pynacl"),
        ("requests", "requests"),
        ("numpy", "numpy"),
    ]
    
    missing_deps = []
    installed_deps = 0
    
    for module, package in dependencies:
        if check_dependency(module, package):
            installed_deps += 1
        else:
            missing_deps.append(package)
    
    print(f"\n📊 Resumen:")
    print(f"✅ Dependencias instaladas: {installed_deps}/{len(dependencies)}")
    
    if missing_deps:
        print(f"❌ Dependencias faltantes: {len(missing_deps)}")
        print("\n📦 Para instalar las dependencias faltantes, ejecuta:")
        print("pip install -r requirements.txt")
        print("\nO instala manualmente:")
        for dep in missing_deps:
            print(f"pip install {dep}")
    else:
        print("🎉 ¡Todas las dependencias están instaladas correctamente!")
        print("\n🚀 Tu bot está listo para funcionar con todas las mejoras de LangChain.")

if __name__ == "__main__":
    main()
