# Carpeta de Tests

Esta carpeta contiene todos los archivos de prueba y verificación del bot.

## Archivos Incluidos

### `run_tests.py`
Script principal para ejecutar todas las pruebas de una vez.
- Ejecuta todas las pruebas en secuencia
- Muestra resultados detallados
- Maneja errores y advertencias
- **Recomendado**: Usar este script para ejecutar todas las pruebas

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
- Requiere `GOOGLE_API_KEY` configurada

### `README_MEJORAS.md`
Documentación detallada de las mejoras implementadas en el sistema RAG.
- Explica el problema original y las soluciones
- Detalla los cambios técnicos realizados
- Incluye instrucciones de instalación y uso

## Cómo Usar

### 🚀 Ejecutar todas las pruebas (Recomendado)
```bash
# Desde el directorio principal del proyecto
python tests/run_tests.py

# O desde la carpeta tests
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
├── run_tests.py           # Script principal para ejecutar todas las pruebas
├── check_dependencies.py  # Verificador de dependencias
├── test_logic.py         # Prueba de lógica básica
├── test_context.py       # Prueba del sistema completo
├── README.md             # Este archivo
└── README_MEJORAS.md     # Documentación de mejoras
```
