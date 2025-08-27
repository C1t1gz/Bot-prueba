# 🤖 PythonBots - Bot de Discord Inteligente

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green.svg)](https://fastapi.tiangolo.com/)
[![LangChain](https://img.shields.io/badge/LangChain-0.1+-orange.svg)](https://langchain.com/)
[![Discord](https://img.shields.io/badge/Discord-Bot-purple.svg)](https://discord.com/)

Un bot de Discord inteligente con sistema RAG (Retrieval-Augmented Generation) mejorado que mantiene contexto de conversación y responde preguntas de manera coherente. Incluye un sistema robusto de ACK diferido para garantizar la entrega confiable de mensajes.

## ✨ Características Principales

- 🧠 **Sistema RAG Mejorado**: Búsqueda semántica + heurísticas de contexto
- 💬 **Memoria de Conversación**: Mantiene historial por usuario
- 🎮 **Comandos Interactivos**: Dados, ruleta, moneda y más
- 🔒 **Seguridad**: Verificación de firmas de Discord
- 📚 **Base de Conocimiento**: Respuestas basadas en datos reales
- 🚀 **Arquitectura Modular**: Código organizado y mantenible
- 🤖 **Multi-LLM**: Soporte para Google Gemini, OpenAI GPT y Ollama
- 🔧 **Configuración Flexible**: Fácil cambio entre proveedores de LLM
- 📝 **Sistema de Logging**: Logs completos con Loguru para monitoreo y debugging
- ⚡ **ACK Diferido Robusto**: Sistema mejorado para garantizar entrega de mensajes
- 📊 **Métricas en Tiempo Real**: Monitoreo completo del rendimiento
- 🔄 **Reintentos Automáticos**: Recuperación automática de errores

## 🏗️ Estructura del Proyecto

```
PythonBots/
├── 📁 src/                    # Código fuente principal
│   ├── 📁 core/              # Funcionalidades core
│   │   └── chat.py           # Sistema de chat principal
│   ├── 📁 rag/               # Sistema RAG
│   │   └── enhanced_rag.py   # RAG mejorado con contexto
│   ├── 📁 discord/           # Integración Discord
│   │   ├── client.py         # Cliente de Discord
│   │   └── interaction_handler.py  # Manejador de interacciones mejorado
│   └── 📁 utils/             # Utilidades
│       ├── security.py       # Verificación de seguridad
│       ├── logger.py         # Sistema de logging centralizado
│       └── metrics.py        # Sistema de métricas
├── 📁 data/                  # Datos y configuraciones
│   └── base.txt              # Base de conocimiento
├── 📁 config/                # Configuraciones
│   ├── settings.py           # Configuraciones centralizadas
│   └── discord_settings.py   # Configuraciones específicas de Discord
├── 📁 scripts/               # Scripts de utilidad
│   ├── run_bot.py            # Script de inicio
│   ├── cleanup.py            # Limpieza de archivos temporales
│   ├── verify_structure.py   # Verificación de estructura
│   └── fix_dependencies.py   # Reparación de dependencias
├── 📁 docs/                  # Documentación
│   ├── README.md             # Documentación técnica
│   ├── LOGGING.md            # Guía del sistema de logging
│   └── ACK_DEFERRED_IMPROVEMENTS.md  # Mejoras del ACK diferido
├── 📁 tests/                 # Pruebas
│   ├── test_ack_deferred.py  # Pruebas del sistema ACK diferido
│   └── test_response_time.py # Pruebas de tiempo de respuesta
├── 📁 logs/                  # Archivos de log
├── main.py                   # Servidor FastAPI
├── requirements.txt          # Dependencias
└── README.md                 # README principal
```

## 🚀 Inicio Rápido

### 1. Instalación
```bash
# Clonar repositorio
git clone <url-del-repositorio>
cd PythonBots

# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt
```

### 2. Configuración
Crear archivo `.env` en la raíz:
```env
# Discord (requerido)
DISCORD_PUBLIC_KEY=tu_public_key_de_discord
DISCORD_TOKEN=tu_token_de_discord

# LLM Provider (elegir uno)
GOOGLE_API_KEY=tu_api_key_de_google      # Para Gemini
OPENAI_API_KEY=tu_api_key_de_openai      # Para GPT
# Ollama no requiere API key (se ejecuta localmente)

# Configuraciones del ACK diferido (opcional)
DISCORD_MAX_WORKERS=5
DISCORD_REQUEST_TIMEOUT=30
DISCORD_MAX_RETRIES=3
DISCORD_QUEUE_MAX_SIZE=100
DISCORD_METRICS_ENABLED=true
```

### 3. Configurar Proveedor LLM
Editar `config/settings.py`:
```python
MODEL_PROVIDER = "gemini"  # "gemini", "openai", o "ollama"
MODEL_NAME = "gemini-2.5-flash"  # Modelo específico del proveedor
```

### 4. Ejecutar
```bash
python scripts/run_bot.py
```

## 🎮 Comandos Disponibles

| Comando | Descripción | Ejemplo |
|---------|-------------|---------|
| `/chat` | Chat inteligente con RAG | `/chat prompt:` |
| `/dados` | Tirar dados | `/dados` |
| `/ruleta` | Girar ruleta | `/ruleta` |
| `/coinflip` | Lanzar moneda | `/coinflip` |
| `/forget` | Borrar memoria de conversación | `/forget` |
| `/help` | Mostrar ayuda | `/help` |

## 🧠 Sistema RAG Mejorado

### Características
- **Búsqueda Semántica**: Utiliza FAISS para búsqueda vectorial eficiente
- **Heurísticas de Contexto**: Extrae entidades del historial de conversación
- **Query Enhancement**: Mejora automáticamente las consultas con contexto
- **Memoria de Conversación Persistente**: Mantiene historial por usuario entre sesiones
- **Comando de Borrado**: Permite a los usuarios borrar su memoria de conversación

### Ejemplo de Funcionamiento
```
Usuario: "¿quién es Joaquín?"
Bot: "Joaquín es el creador y administrador de este bot."

Usuario: "¿cuándo nació?"
Bot: "Joaquín nació el 15 de Julio del 2003"

Usuario: "Ahora te llamas Pepe"
Bot: "Entendido, me llamo Pepe"

Usuario: "¿Cuál es tu nombre?"
Bot: "Me llamo Pepe" (recuerda el contexto de la conversación)
```

## ⚡ Sistema de ACK Diferido Mejorado

### Características Principales
- **Cola de Procesamiento Robusta**: Maneja múltiples peticiones simultáneamente
- **Workers Paralelos**: Procesamiento eficiente con workers múltiples
- **Reintentos Automáticos**: Recuperación automática de errores con delays progresivos
- **Métricas en Tiempo Real**: Monitoreo completo del rendimiento
- **Configuración Flexible**: Parámetros ajustables via variables de entorno

### Endpoints de Monitoreo
```bash
# Estado general del sistema
curl http://localhost:8000/health

# Métricas detalladas
curl http://localhost:8000/metrics

# Métricas en formato Prometheus
curl http://localhost:8000/metrics/prometheus
```

### Configuración Recomendada
```bash
# Para desarrollo
DISCORD_MAX_WORKERS=3
DISCORD_REQUEST_TIMEOUT=30
DISCORD_MAX_RETRIES=2

# Para producción
DISCORD_MAX_WORKERS=10
DISCORD_REQUEST_TIMEOUT=45
DISCORD_MAX_RETRIES=3
DISCORD_QUEUE_MAX_SIZE=200
```

## 🤖 Proveedores de LLM Soportados

### Google Gemini (Recomendado)
```python
MODEL_PROVIDER = "gemini"
MODEL_NAME = "gemini-2.5-flash"
```

### OpenAI GPT
```python
MODEL_PROVIDER = "openai"
MODEL_NAME = "gpt-4o-mini"  # o "gpt-4", "gpt-3.5-turbo"
```

### Ollama (Local)
```python
MODEL_PROVIDER = "ollama"
MODEL_NAME = "llama2"  # o "llama3.1", "mistral", etc.
```

## 🧪 Pruebas

```bash
# Ejecutar todas las pruebas
cd tests
python test_ack_deferred.py

# Pruebas individuales
python test_logic.py      # Prueba lógica RAG
python test_context.py    # Prueba contexto completo
python test_response_time.py  # Prueba tiempo de respuesta
python check_dependencies.py  # Verificar dependencias
```

## 🔧 Scripts de Utilidad

```bash
# Ejecutar el bot
python scripts/run_bot.py

# Probar sistema de logging
python scripts/test_logging.py

# Probar tiempo de respuesta
python scripts/test_response_time.py

# Registrar comandos de Discord
python scripts/register_guild_commands.py         # Para un servidor específico (con logger del proyecto)
python scripts/register_global_commands.py        # Para todos los servidores (con logger del proyecto)
python scripts/register_guild_commands_simple.py  # Para un servidor específico (versión simple)
python scripts/register_global_commands_simple.py # Para todos los servidores (versión simple)

# Limpiar archivos temporales
python scripts/cleanup.py

# Verificar estructura del proyecto
python scripts/verify_structure.py

# Reparar dependencias
python scripts/fix_dependencies.py

# Gestionar memorias persistentes
python scripts/manage_memory.py list
python scripts/manage_memory.py show 123456789
python scripts/manage_memory.py clear 123456789
```

## 📚 Documentación

- 📖 [Documentación Completa](docs/README.md)
- 📝 [Sistema de Logging](docs/LOGGING.md)
- ⚡ [Mejoras del ACK Diferido](docs/ACK_DEFERRED_IMPROVEMENTS.md)
- 📊 [Sistema de Almacenamiento de Contextos](docs/CONTEXT_STORAGE.md)
- 🔧 [Configuración](config/settings.py)
- 🧪 [Guía de Pruebas](tests/README.md)

## 📊 Sistema de Almacenamiento de Contextos

### Descripción
El bot incluye un sistema completo para almacenar y analizar todas las consultas realizadas, permitiendo:

- **Análisis de uso**: Identificar patrones de consulta y usuarios más activos
- **Métricas de rendimiento**: Tiempos de procesamiento y documentos utilizados
- **Estadísticas detalladas**: Consultas por hora, día, palabras clave más comunes
- **Exportación de datos**: Para análisis externos y reportes

### Uso Rápido

```bash
# Ver estadísticas generales
python scripts/analyze_contexts.py stats

# Ver contextos de un usuario específico
python scripts/analyze_contexts.py user 123456789 10

# Exportar todos los contextos
python scripts/analyze_contexts.py export

# Limpiar contextos antiguos (más de 30 días)
python scripts/analyze_contexts.py cleanup 30
```

### Endpoints API

```bash
# Estadísticas generales
curl http://localhost:8000/contexts/stats

# Contextos de usuario
curl http://localhost:8000/contexts/user/123456789?limit=10

# Exportar contextos
curl -X POST http://localhost:8000/contexts/export

# Limpiar contextos antiguos
curl -X DELETE http://localhost:8000/contexts/cleanup?days=30
```

### Documentación Completa
Ver [docs/CONTEXT_STORAGE.md](docs/CONTEXT_STORAGE.md) para documentación detallada.

## 🧠 Sistema de Memoria Persistente

### Descripción
El bot ahora incluye un sistema de **memoria persistente por usuario** que mantiene el contexto de conversación entre sesiones:

- **Memoria Persistente**: El contexto se guarda en disco y persiste entre reinicios del servidor
- **Comando de Borrado**: Los usuarios pueden borrar su memoria con `/forget`
- **Gestión Administrativa**: Scripts y APIs para gestionar las memorias

### Uso Rápido

```bash
# Listar todas las memorias
python scripts/manage_memory.py list

# Ver memoria de un usuario específico
python scripts/manage_memory.py show 123456789

# Borrar memoria de un usuario
python scripts/manage_memory.py clear 123456789

# Borrar todas las memorias
python scripts/manage_memory.py clear-all

# Limpiar memorias antiguas
python scripts/manage_memory.py cleanup 30
```

### Endpoints API

```bash
# Listar todas las memorias
curl http://localhost:8000/memory/list

# Información de memoria de usuario
curl http://localhost:8000/memory/user/123456789

# Borrar memoria de usuario
curl -X DELETE http://localhost:8000/memory/user/123456789

# Borrar todas las memorias
curl -X DELETE http://localhost:8000/memory/clear-all

# Limpiar memorias antiguas
curl -X DELETE http://localhost:8000/memory/cleanup?days=30
```

### Ejemplo de Funcionamiento

```
Sesión 1:
Usuario: "Ahora te llamas Pepe"
Bot: "Entendido, me llamo Pepe"

Sesión 2 (después de cerrar Discord y volver):
Usuario: "¿Cuál es tu nombre?"
Bot: "Me llamo Pepe" (recuerda el contexto)

Usuario: "/forget"
Bot: "🧹 ¡Memoria borrada! He olvidado todo lo que habíamos conversado."

Usuario: "¿Cuál es tu nombre?"
Bot: "Soy un asistente de IA..." (ya no recuerda)
```

## 🛠️ Tecnologías Utilizadas

- **Python 3.8+**: Lenguaje principal
- **FastAPI**: Framework web para la API
- **LangChain**: Framework para aplicaciones LLM
- **FAISS**: Búsqueda vectorial
- **Discord.py**: Integración con Discord
- **Google Gemini**: Modelo de lenguaje (predeterminado)
- **OpenAI GPT**: Modelo de lenguaje alternativo
- **Ollama**: Modelos locales
- **HuggingFace**: Embeddings
- **Loguru**: Sistema de logging avanzado
- **Threading**: Procesamiento paralelo para ACK diferido

## 🔄 Cambios Recientes

### v1.5.0 - Sistema de Memoria Persistente 🧠
- ✅ **Memoria persistente** por usuario que mantiene contexto entre sesiones
- ✅ **Comando `/forget`** para que los usuarios borren su memoria
- ✅ **Gestión administrativa** de memorias con scripts y APIs
- ✅ **Almacenamiento en disco** con formato JSON para persistencia
- ✅ **Cache en memoria** para acceso rápido
- ✅ **Limpieza automática** de memorias antiguas
- ✅ **Thread-safe** para múltiples usuarios simultáneos
- ✅ **Documentación completa** del sistema

### v1.4.0 - Sistema de Almacenamiento de Contextos 📊
- ✅ **Almacenamiento automático** de todas las consultas y respuestas
- ✅ **Análisis de usuarios** más activos y patrones de uso
- ✅ **Estadísticas detalladas** por hora, día y palabras clave
- ✅ **Scripts de análisis** para generar reportes
- ✅ **Endpoints API** para acceso programático a estadísticas
- ✅ **Exportación de datos** en formato JSON para análisis externos
- ✅ **Limpieza automática** de contextos antiguos
- ✅ **Cache de estadísticas** para optimizar rendimiento
- ✅ **Documentación completa** del sistema

### v1.3.0 - Sistema de ACK Diferido Mejorado ⭐
- ✅ **Sistema de cola robusto** con workers múltiples
- ✅ **Reintentos automáticos** con delays progresivos
- ✅ **Métricas en tiempo real** para monitoreo completo
- ✅ **Configuración centralizada** via variables de entorno
- ✅ **Endpoints de monitoreo** (/health, /metrics, /metrics/prometheus)
- ✅ **Manejo de errores robusto** con recuperación automática
- ✅ **Limpieza automática** de datos antiguos
- ✅ **Pruebas completas** del sistema mejorado
- ✅ **Documentación detallada** de las mejoras

### v1.2.0 - Sistema de Logging Completo
- ✅ Integración completa de Loguru en todo el proyecto
- ✅ Logs separados por categorías (app, errors, discord, chat)
- ✅ Rotación automática y compresión de archivos de log
- ✅ Logs en consola con colores y formato legible
- ✅ Documentación completa del sistema de logging

### v1.1.0 - Soporte Multi-LLM
- ✅ Soporte para Google Gemini, OpenAI GPT y Ollama
- ✅ Configuración centralizada en `config/settings.py`
- ✅ Corrección de warnings de deprecación de LangChain
- ✅ Mejoras en la estructura del proyecto
- ✅ Scripts de utilidad para mantenimiento

### v1.0.0 - Sistema RAG Mejorado
- ✅ Sistema RAG con contexto y heurísticas
- ✅ Memoria de conversación por usuario
- ✅ Arquitectura modular y organizada
- ✅ Integración completa con Discord

## 🤝 Contribución

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## 👨‍💻 Autor

**Joaquín** - Creador y administrador del bot

---

⭐ Si te gusta este proyecto, ¡dale una estrella!
