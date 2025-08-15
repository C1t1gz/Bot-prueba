"""
Script para ejecutar todas las pruebas desde la carpeta tests
"""

import sys
import os
import subprocess

def run_test(test_name, description):
    """
    Ejecuta una prueba específica y muestra el resultado.
    """
    print(f"\n{'='*60}")
    print(f"🧪 Ejecutando: {test_name}")
    print(f"📝 Descripción: {description}")
    print(f"{'='*60}")
    
    try:
        # Ejecutar el script de prueba
        result = subprocess.run([sys.executable, test_name], 
                              capture_output=True, 
                              text=True, 
                              cwd=os.path.dirname(os.path.abspath(__file__)))
        
        # Mostrar la salida
        if result.stdout:
            print(result.stdout)
        if result.stderr:
            print(f"⚠️ Advertencias/Errores: {result.stderr}")
        
        # Mostrar el resultado
        if result.returncode == 0:
            print(f"✅ {test_name} completado exitosamente")
        else:
            print(f"❌ {test_name} falló con código {result.returncode}")
            
    except Exception as e:
        print(f"❌ Error ejecutando {test_name}: {e}")

def main():
    """
    Ejecuta todas las pruebas disponibles.
    """
    print("🚀 Iniciando suite de pruebas del bot...")
    print(f"📁 Directorio de trabajo: {os.getcwd()}")
    
    # Lista de pruebas a ejecutar
    tests = [
        ("check_dependencies.py", "Verificar que todas las dependencias estén instaladas"),
        ("test_logic.py", "Probar la lógica de mejora de consultas (sin dependencias externas)"),
        ("test_context.py", "Probar el sistema completo de manejo de contexto")
    ]
    
    print(f"\n📋 Se ejecutarán {len(tests)} pruebas:")
    for i, (test, desc) in enumerate(tests, 1):
        print(f"  {i}. {test} - {desc}")
    
    # Ejecutar cada prueba
    for test_name, description in tests:
        run_test(test_name, description)
    
    print(f"\n{'='*60}")
    print("🎉 Suite de pruebas completada")
    print(f"{'='*60}")
    
    print("\n💡 Notas importantes:")
    print("- test_logic.py: No requiere dependencias externas")
    print("- test_context.py: Requiere GOOGLE_API_KEY configurada")
    print("- check_dependencies.py: Verifica que todo esté instalado correctamente")

if __name__ == "__main__":
    main()
