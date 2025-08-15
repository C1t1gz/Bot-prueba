# Carpeta de Tests

Esta carpeta contiene todos los archivos de prueba y verificación del bot.

## Archivos Incluidos

### `run_tests.py`
Script principal para ejecutar todas las pruebas de una vez.
- Ejecuta todas las pruebas en secuencia
- Muestra resultados detallados
- Maneja errores y advertencias
- **Recomendado**: Usar este script para ejecutar todas las pruebas

### `diagnose_venv.py`
Script de diagnóstico para identificar problemas con el entorno virtual.
- Verifica el estado del entorno virtual
- Lista dependencias instaladas y faltantes
- Proporciona recomendaciones específicas
- **Recomendado**: Usar si hay problemas con las dependencias

### `activate_venv.py`
Gestor de entorno virtual para ejecutar pruebas.
- Activa automáticamente el entorno virtual
- Ejecuta las pruebas con el Python correcto
- Interfaz interactiva para diferentes opciones
- **Recomendado**: Usar si tienes problemas con la activación del venv

### `check_dependencies.py`
Script para verificar que todas las dependencias estén instaladas correctamente.
- Lista todas las dependencias necesarias
- Verifica si están instaladas
- Proporciona comandos de instalación si faltan

### `test_logic.py`
Script de prueba simplificado que verifica solo la lógica de mejora de consultas.
- No depende de LangChain ni librerías externas
- Prueba la extracción de entidades y mejora de consultas
- Útil para verificar que la lógica funciona sin instalar dependencias

### `test_context.py`
Script de prueba principal que verifica el manejo de contexto del bot.
- Prueba la secuencia: "¿quién es joaquin?" → "¿cuándo nació?" → "¿qué le gusta?"
- Verifica que el bot mantenga el contexto entre preguntas relacionadas
- Requiere `GOOGLE_API_KEY` configurada y todas las dependencias instaladas

### `test_context_simple.py`
Script de prueba simplificado que verifica solo la lógica de contexto.
- Prueba la misma secuencia que test_context.py pero sin dependencias externas
- Simula las respuestas del bot para verificar la lógica
- No requiere API keys ni dependencias pesadas
- **Recomendado**: Usar si hay problemas con las dependencias

### `README_MEJORAS.md`
Documentación detallada de las mejoras implementadas en el sistema RAG.
- Explica el problema original y las soluciones
- Detalla los cambios técnicos realizados
- Incluye instrucciones de instalación y uso

## Cómo Usar

### 🔧 Si tienes problemas con las dependencias (Recomendado)
```bash
# Diagnóstico completo
python tests/diagnose_venv.py

# O usar el gestor de entorno virtual
python tests/activate_venv.py
```

### 🚀 Ejecutar todas las pruebas
```bash
# Desde el directorio principal del proyecto
python tests/run_tests.py

# O desde la carpeta tests (con venv activado)
cd tests
python run_tests.py
```

### 🔍 Ejecutar pruebas individuales

1. **Verificar dependencias:**
   ```bash
   python tests/check_dependencies.py
   ```

2. **Probar la lógica básica:**
   ```bash
   python tests/test_logic.py
   ```

3. **Probar el sistema completo:**
   ```bash
   python tests/test_context.py
   ```

4. **Probar la lógica de contexto (sin dependencias):**
   ```bash
   python tests/test_context_simple.py
   ```

### 📁 Ejecutar desde la carpeta tests
```bash
cd tests
python check_dependencies.py
python test_logic.py
python test_context.py
```

## Notas Importantes

- **Rutas corregidas**: Todos los scripts ahora funcionan correctamente desde la carpeta `tests/`
- **Importaciones**: Los scripts agregan automáticamente el directorio padre al path de Python
- **Variables de entorno**: Los scripts buscan el archivo `.env` en el directorio principal
- **Dependencias**: Algunos tests requieren que las dependencias estén instaladas
- **API Keys**: `test_context.py` requiere `GOOGLE_API_KEY` configurada

## Estructura de Archivos

```
tests/
├── run_tests.py              # Script principal para ejecutar todas las pruebas
├── diagnose_venv.py          # Diagnóstico del entorno virtual
├── activate_venv.py          # Gestor de entorno virtual
├── check_dependencies.py     # Verificador de dependencias
├── test_logic.py            # Prueba de lógica básica
├── test_context.py          # Prueba del sistema completo
├── test_context_simple.py   # Prueba de contexto simplificada
├── README.md                # Este archivo
└── README_MEJORAS.md        # Documentación de mejoras
```
