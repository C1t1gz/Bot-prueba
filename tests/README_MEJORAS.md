# Mejoras en el Sistema RAG - Manejo de Contexto

## Problema Identificado

El bot tenía dificultades para mantener el contexto entre preguntas relacionadas. Por ejemplo:
- Pregunta 1: "¿quién es joaquin?" → Respuesta correcta
- Pregunta 2: "¿cuándo nació?" → El bot no reconocía que se refería a Joaquín

## Soluciones Implementadas

### 1. Mejora en el Prompt del Sistema (`timbero.py`)

**Antes:**
```python
system_prompt = (
    "Utiliza el contexto proporcionado para responder la pregunta. "
    "Si no sabes la respuesta, di que no la sabes. "
    "Contexto: {context}"
)
```

**Después:**
```python
system_prompt = (
    "Eres un asistente útil que responde preguntas basándose en el contexto proporcionado y el historial de la conversación. "
    "IMPORTANTE: Si la pregunta hace referencia a alguien o algo mencionado anteriormente en la conversación, "
    "usa esa información del contexto para entender a qué se refiere la pregunta. "
    "Por ejemplo, si alguien pregunta '¿quién es Joaquín?' y luego pregunta '¿cuándo nació?', "
    "debes entender que se refiere a Joaquín y buscar esa información en el contexto. "
    "Contexto de la base de conocimiento: {context}\n"
    "Historial de la conversación: {history}"
)
```

### 2. Sistema RAG Mejorado (`enhanced_rag.py`)

Se creó un nuevo módulo que incluye:

- **Extracción de entidades**: Identifica nombres propios mencionados en el historial
- **Mejora de consultas**: Agrega contexto automáticamente a las consultas
- **Retriever inteligente**: Considera el historial para mejorar la búsqueda

### 3. Manejo Mejorado del Historial

El sistema ahora:
- Mantiene el historial de conversación por usuario
- Usa el historial para mejorar las consultas al RAG
- Proporciona contexto adicional al LLM

## Archivos Modificados

1. **`timbero.py`**: Mejorado el prompt del sistema y el manejo del historial
2. **`enhanced_rag.py`**: Nuevo módulo RAG con manejo de contexto
3. **`simple_rag.py`**: Actualizado con mejoras en el retriever
4. **`test_context.py`**: Script de prueba para verificar las mejoras

## Instalación y Configuración

### 1. Instalar Dependencias
```bash
pip install -r requirments.txt
```

### 2. Verificar Dependencias
```bash
python check_dependencies.py
```

### 3. Configurar Variables de Entorno
Asegúrate de tener configurada la `GOOGLE_API_KEY` en tu archivo `.env`

### 4. Probar las Mejoras
```bash
python test_context.py
```

3. En Discord, prueba la secuencia:
   - `/chat prompt:¿quién es joaquin?`
   - `/chat prompt:¿cuándo nació?`
   - `/chat prompt:¿qué le gusta?`

## Resultados Esperados

- ✅ La primera pregunta debería responder correctamente sobre Joaquín
- ✅ La segunda pregunta debería reconocer que se refiere a Joaquín y dar su fecha de nacimiento
- ✅ La tercera pregunta debería reconocer que se refiere a Joaquín y mencionar el chocolate

## Notas Técnicas

- El sistema usa `ConversationBufferMemory` para mantener el historial por usuario
- Se implementó un `EnhancedRetriever` que considera el contexto del historial
- El prompt del sistema ahora incluye instrucciones específicas sobre el manejo de referencias
- Se mantiene compatibilidad con el sistema anterior
- Se aprovechan las funcionalidades avanzadas de LangChain como `ContextualCompressionRetriever` y `LLMChainExtractor`

## Dependencias Principales

### Core LangChain
- `langchain>=0.1.0` - Framework principal
- `langchain-core>=0.1.0` - Componentes core
- `langchain-community>=0.0.20` - Integraciones de la comunidad
- `langchain-google-genai>=0.0.6` - Integración con Google Gemini
- `langchain-huggingface>=0.0.6` - Integración con HuggingFace

### Vector Store y Embeddings
- `faiss-cpu>=1.7.4` - Almacenamiento vectorial
- `sentence-transformers>=2.2.2` - Modelos de embeddings

### Bot y Web Framework
- `discord.py>=2.3.0` - API de Discord
- `fastapi>=0.104.0` - Framework web
- `uvicorn>=0.24.0` - Servidor ASGI

## Próximas Mejoras Posibles

1. Implementar limpieza automática de memoria antigua
2. Agregar más tipos de entidades (lugares, fechas, etc.)
3. Implementar análisis de sentimiento para mejor contexto
4. Agregar métricas de rendimiento del sistema RAG
