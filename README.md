# PythonBots - Bot de Discord con RAG Mejorado

Bot de Discord inteligente que utiliza un sistema RAG (Retrieval-Augmented Generation) mejorado para responder preguntas con contexto y memoria de conversación.

## 🚀 Características Principales

- **Sistema RAG Mejorado**: Búsqueda semántica en base de conocimiento
- **Manejo de Contexto**: Mantiene el contexto entre preguntas relacionadas
- **Memoria de Conversación**: Recuerda el historial por usuario
- **Comandos de Juego**: Dados, ruleta, moneda
- **Integración con Discord**: Comandos slash y respuestas inteligentes

## 📁 Estructura del Proyecto

```
PythonBots/
├── main.py              # Servidor FastAPI principal
├── timbero.py           # Funciones del bot (actualizado)
├── enhanced_rag.py      # Sistema RAG mejorado
├── base.txt             # Base de conocimiento
├── requirements.txt     # Dependencias
├── register_commands.py # Registro de comandos de Discord
├── register_guild_commands.py # Registro de comandos de guild
├── tests/               # Archivos de prueba
│   ├── test_context.py
│   ├── test_logic.py
│   ├── check_dependencies.py
│   └── README.md
└── legacy/              # Archivos obsoletos
    ├── simple_rag.py
    └── README.md
```

## 🛠️ Instalación

### 1. Clonar el repositorio
```bash
git clone <tu-repositorio>
cd PythonBots
```

### 2. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 3. Verificar instalación
```bash
python tests/check_dependencies.py
```

### 4. Configurar variables de entorno
Crear archivo `.env` con:
```env
GOOGLE_API_KEY=tu_api_key_de_google
DISCORD_PUBLIC_KEY=tu_public_key_de_discord
DISCORD_TOKEN=tu_token_de_discord
```

## 🧪 Pruebas

### Probar la lógica básica (sin dependencias externas)
```bash
python tests/test_logic.py
```

### Probar el sistema completo
```bash
python tests/test_context.py
```

## 🎮 Comandos Disponibles

- `/chat prompt:tu_pregunta` - Pregunta al bot
- `/dados` - Tira los dados
- `/ruleta` - Gira la ruleta
- `/coinflip` - Lanza una moneda
- `/help` - Muestra ayuda

## 🔧 Funcionalidades Avanzadas

### Sistema RAG Mejorado
- **Búsqueda semántica**: Usa embeddings para encontrar información relevante
- **Manejo de contexto**: Mantiene el contexto entre preguntas
- **Extracción de entidades**: Identifica nombres propios en el historial
- **Mejora de consultas**: Agrega contexto automáticamente

### Memoria de Conversación
- **Por usuario**: Cada usuario tiene su propio historial
- **Persistencia**: El contexto se mantiene durante la sesión
- **Límite inteligente**: Evita que el historial sea demasiado largo

## 📚 Base de Conocimiento

El archivo `base.txt` contiene la información que el bot puede consultar. Puedes agregar más información editando este archivo.

## 🚀 Despliegue

### Desarrollo local
```bash
uvicorn main:app --reload
```

### Producción
```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

## 📖 Documentación Adicional

- **Mejoras implementadas**: `tests/README_MEJORAS.md`
- **Archivos de prueba**: `tests/README.md`
- **Archivos obsoletos**: `legacy/README.md`

## 🤝 Contribuir

1. Fork el proyecto
2. Crea una rama para tu feature
3. Commit tus cambios
4. Push a la rama
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.
