# PythonBots - Bot de Discord con RAG Mejorado

## 📋 Descripción

PythonBots es un bot de Discord inteligente que utiliza un sistema RAG (Retrieval-Augmented Generation) mejorado para responder preguntas de manera contextual y mantener conversaciones coherentes. Soporta múltiples proveedores de LLM (Google Gemini, OpenAI GPT, Ollama) con configuración flexible.

## 🏗️ Arquitectura del Proyecto

```
PythonBots/
├── 📁 src/                    # Código fuente principal
│   ├── 📁 core/              # Funcionalidades core del bot
│   │   └── chat.py           # Sistema de chat principal
│   ├── 📁 rag/               # Sistema RAG
│   │   └── enhanced_rag.py   # RAG mejorado con contexto
│   ├── 📁 discord/           # Integración con Discord
│   │   └── client.py         # Cliente de Discord
│   └── 📁 utils/             # Utilidades
│       └── security.py       # Verificación de seguridad
├── 📁 data/                  # Datos y configuraciones
│   └── base.txt              # Base de conocimiento
├── 📁 config/                # Configuraciones
│   └── settings.py           # Configuraciones centralizadas
├── 📁 scripts/               # Scripts de utilidad
│   ├── run_bot.py            # Script de inicio
│   ├── cleanup.py            # Limpieza de archivos temporales
│   ├── verify_structure.py   # Verificación de estructura
│   └── fix_dependencies.py   # Reparación de dependencias
├── 📁 docs/                  # Documentación
├── 📁 tests/                 # Pruebas
├── 📁 legacy/                # Archivos obsoletos
├── main.py                   # Servidor FastAPI
├── requirements.txt          # Dependencias
└── README.md                 # README principal
```

## 🚀 Características Principales

### 🤖 Sistema RAG Mejorado
- **Búsqueda Semántica**: Utiliza FAISS para búsqueda vectorial eficiente
- **Heurísticas de Contexto**: Extrae entidades del historial de conversación
- **Query Enhancement**: Mejora automáticamente las consultas con contexto
- **Memoria de Conversación**: Mantiene historial por usuario

### 🎮 Comandos de Discord
- `/chat` - Chat inteligente con RAG
- `/dados` - Tirar dados
- `/ruleta` - Girar ruleta
- `/coinflip` - Lanzar moneda
- `/help` - Mostrar ayuda

### 🔒 Seguridad
- Verificación de firmas de Discord
- Validación de configuraciones
- Manejo seguro de tokens

### 🤖 Multi-LLM Support
- **Google Gemini**: Modelo predeterminado, alta calidad
- **OpenAI GPT**: Alternativa con modelos GPT-4 y GPT-3.5
- **Ollama**: Modelos locales para privacidad total

## 🛠️ Instalación

### 1. Clonar el repositorio
```bash
git clone <url-del-repositorio>
cd PythonBots
```

### 2. Crear entorno virtual
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno
Crear archivo `.env` en la raíz del proyecto:
```env
# Discord (requerido)
DISCORD_PUBLIC_KEY=tu_public_key_de_discord
DISCORD_TOKEN=tu_token_de_discord

# LLM Provider (elegir uno)
GOOGLE_API_KEY=tu_api_key_de_google      # Para Gemini
OPENAI_API_KEY=tu_api_key_de_openai      # Para GPT
# Ollama no requiere API key (se ejecuta localmente)
```

### 5. Configurar proveedor LLM
Editar `config/settings.py`:
```python
MODEL_PROVIDER = "gemini"  # "gemini", "openai", o "ollama"
MODEL_NAME = "gemini-2.5-flash"  # Modelo específico del proveedor
```

### 6. Ejecutar el bot
```bash
python scripts/run_bot.py
```

## 🔧 Configuración

### Variables de Entorno Requeridas

| Variable | Descripción | Ejemplo | Requerido |
|----------|-------------|---------|-----------|
| `DISCORD_PUBLIC_KEY` | Clave pública de tu bot de Discord | `abc123...` | ✅ |
| `DISCORD_TOKEN` | Token de tu bot de Discord | `xyz789...` | ✅ |
| `GOOGLE_API_KEY` | API Key de Google para Gemini | `def456...` | Para Gemini |
| `OPENAI_API_KEY` | API Key de OpenAI para GPT | `ghi789...` | Para OpenAI |

### Configuraciones del RAG

Las configuraciones del sistema RAG se pueden modificar en `config/settings.py`:

```python
# Número de resultados a retornar
RAG_K_RESULTS = 5

# Límite de historial por usuario
HISTORY_LIMIT = 10

# Modelo de embeddings
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
```

### Configuraciones del LLM

```python
# Proveedor de LLM
MODEL_PROVIDER = "gemini"  # "gemini", "openai", "ollama"

# Modelo específico
MODEL_NAME = "gemini-2.5-flash"  # Depende del proveedor
```

## 🤖 Proveedores de LLM

### Google Gemini (Recomendado)
- **Ventajas**: Alta calidad, buena documentación, gratuito con límites
- **Modelos**: `gemini-2.5-flash`, `gemini-1.5-pro`
- **Configuración**:
  ```python
  MODEL_PROVIDER = "gemini"
  MODEL_NAME = "gemini-2.5-flash"
  ```

### OpenAI GPT
- **Ventajas**: Muy alta calidad, modelos avanzados
- **Modelos**: `gpt-4o-mini`, `gpt-4`, `gpt-3.5-turbo`
- **Configuración**:
  ```python
  MODEL_PROVIDER = "openai"
  MODEL_NAME = "gpt-4o-mini"
  ```

### Ollama (Local)
- **Ventajas**: Privacidad total, sin costos de API
- **Modelos**: `llama2`, `llama3.1`, `mistral`, `codellama`
- **Configuración**:
  ```python
  MODEL_PROVIDER = "ollama"
  MODEL_NAME = "llama2"
  ```

## 🧪 Pruebas

### Ejecutar todas las pruebas
```bash
cd tests
python run_tests.py
```

### Pruebas individuales
```bash
# Prueba de lógica RAG
python tests/test_logic.py

# Prueba de contexto completo
python tests/test_context.py

# Verificar dependencias
python tests/check_dependencies.py
```

## 🔧 Scripts de Utilidad

### Ejecutar el bot
```bash
python scripts/run_bot.py
```

### Limpiar archivos temporales
```bash
python scripts/cleanup.py
```

### Verificar estructura del proyecto
```bash
python scripts/verify_structure.py
```

### Reparar dependencias
```bash
python scripts/fix_dependencies.py
```

## 📚 Base de Conocimiento

El archivo `data/base.txt` contiene la información que el bot puede consultar. Cada línea representa un hecho o información:

```
Joaquin es el creador y administrador de este bot.
Joaquin nació el 15 de Julio del 2003
a Joaquin le gusta el chocolate
```

## 🔄 Flujo de Funcionamiento

1. **Recepción de Mensaje**: Discord envía interacción al endpoint `/discord-interactions`
2. **Verificación**: Se valida la firma de Discord
3. **Procesamiento**: Se extrae el comando y parámetros
4. **RAG**: Para comandos `/chat`:
   - Se extrae contexto del historial
   - Se mejora la query con heurísticas
   - Se busca en la base de conocimiento
5. **Respuesta**: Se genera respuesta con LLM y se envía a Discord

## 🧠 Sistema RAG Técnico

### Componentes Principales

1. **FAISS Vector Store**: Almacena embeddings de la base de conocimiento
2. **HuggingFace Embeddings**: Genera embeddings usando `all-MiniLM-L6-v2`
3. **Heurísticas de Contexto**: Extrae entidades del historial de conversación
4. **Query Enhancement**: Mejora consultas basándose en contexto previo
5. **LangChain Integration**: Combina retriever con LLM para respuestas

### Flujo de Procesamiento

```
Usuario → Query → Extracción de Entidades → Query Enhancement → FAISS Search → LLM → Respuesta
```

### Heurísticas Implementadas

- **Entity Extraction**: Identifica nombres propios del historial
- **Context Enhancement**: Añade contexto a consultas ambiguas
- **Person Reference**: Maneja referencias a personas mencionadas previamente

## 🐛 Solución de Problemas

### Error: "Variables de entorno faltantes"
- Verifica que el archivo `.env` existe y contiene todas las variables requeridas
- Asegúrate de que las variables no tengan espacios extra

### Error: "Firma de Discord inválida"
- Verifica que `DISCORD_PUBLIC_KEY` sea correcta
- Asegúrate de que el endpoint esté configurado correctamente en Discord

### Error: "No se encontró base.txt"
- Verifica que el archivo `data/base.txt` existe
- Asegúrate de que el archivo tenga contenido válido

### Error: "LangChainDeprecationWarning"
- El proyecto ya incluye las correcciones necesarias
- Si persisten warnings, ejecuta `python scripts/fix_dependencies.py`

### Error: "API Key no válida"
- Verifica que la API key corresponda al proveedor configurado
- Asegúrate de que `MODEL_PROVIDER` y `MODEL_NAME` sean correctos

## 🔄 Cambios Recientes

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

## 🙏 Agradecimientos

- LangChain por el framework de LLM
- Discord por la API
- Google por Gemini
- OpenAI por GPT
- Ollama por modelos locales
- FAISS por la búsqueda vectorial
