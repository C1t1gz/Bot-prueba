# Sistema de Almacenamiento de Contextos

## 📋 Descripción

El sistema de almacenamiento de contextos permite guardar y analizar todas las consultas realizadas al bot, incluyendo información detallada sobre usuarios, consultas, respuestas, documentos utilizados y métricas de rendimiento.

## 🏗️ Arquitectura

### Componentes Principales

1. **`QueryContext`** - Estructura de datos para almacenar información de cada consulta
2. **`ContextStorage`** - Clase principal para gestionar el almacenamiento
3. **Endpoints API** - Para acceder a las estadísticas y datos
4. **Scripts de análisis** - Para generar reportes y análisis

### Estructura de Datos

```python
@dataclass
class QueryContext:
    user_id: str              # ID del usuario de Discord
    username: str             # Nombre del usuario
    prompt: str               # Consulta del usuario
    response: str             # Respuesta del bot
    timestamp: float          # Timestamp de la consulta
    roles: List[str]          # Roles del usuario en Discord
    documents_used: List[str] # Documentos utilizados por RAG
    processing_time: float    # Tiempo de procesamiento
    model_used: str           # Modelo de IA utilizado
    interaction_token: str    # Token de interacción de Discord
    guild_id: Optional[str]   # ID del servidor
    channel_id: Optional[str] # ID del canal
```

## 📁 Almacenamiento

### Ubicación de Archivos

- **Directorio principal**: `data/contexts/`
- **Archivo de contextos**: `query_contexts.jsonl` (formato JSONL)
- **Archivo de estadísticas**: `query_stats.json` (cache de estadísticas)

### Formato JSONL

Cada línea del archivo contiene un contexto completo en formato JSON:

```json
{
  "user_id": "123456789",
  "username": "usuario_ejemplo",
  "prompt": "¿Qué es Python?",
  "response": "Python es un lenguaje de programación...",
  "timestamp": 1703123456.789,
  "datetime": "2023-12-21T10:30:56.789",
  "roles": ["member"],
  "documents_used": ["base.txt"],
  "processing_time": 1.5,
  "model_used": "gpt-4o-mini",
  "interaction_token": "abc123",
  "guild_id": "987654321",
  "channel_id": "456789123"
}
```

## 🔧 Uso

### Integración Automática

El sistema se integra automáticamente en el flujo de chat. Cada vez que se procesa una consulta, se almacena automáticamente el contexto.

### Scripts de Análisis

#### Estadísticas Generales

```bash
python scripts/analyze_contexts.py stats
```

**Salida ejemplo:**
```
============================================================
  ANÁLISIS DE CONTEXTOS DE CONSULTAS
============================================================

📊 ESTADÍSTICAS GENERALES
----------------------------------------
📈 Total de consultas: 1,234
👥 Usuarios únicos: 45
⏱️  Tiempo promedio de procesamiento: 1.23s
🕒 Última actualización: 2023-12-21T10:30:56.789

📊 USUARIOS MÁS ACTIVOS
----------------------------------------
 1. UsuarioPrueba1 (test_user_1) - 156 consultas
 2. UsuarioPrueba2 (test_user_2) - 89 consultas
 3. UsuarioPrueba3 (test_user_3) - 67 consultas
```

#### Contextos de Usuario Específico

```bash
python scripts/analyze_contexts.py user 123456789 10
```

#### Exportar Contextos

```bash
python scripts/analyze_contexts.py export
```

#### Limpiar Contextos Antiguos

```bash
python scripts/analyze_contexts.py cleanup 30
```

### Endpoints API

#### Obtener Estadísticas

```http
GET /contexts/stats
```

**Respuesta:**
```json
{
  "success": true,
  "data": {
    "total_queries": 1234,
    "unique_users": 45,
    "top_users": [...],
    "top_queries": [...],
    "average_processing_time": 1.23,
    "queries_by_hour": {...},
    "queries_by_day": {...},
    "last_updated": "2023-12-21T10:30:56.789"
  }
}
```

#### Contextos de Usuario

```http
GET /contexts/user/{user_id}?limit=10
```

#### Exportar Contextos

```http
POST /contexts/export
```

#### Limpiar Contextos

```http
DELETE /contexts/cleanup?days=30
```

## 📊 Estadísticas Disponibles

### Métricas Generales

- **Total de consultas**: Número total de consultas procesadas
- **Usuarios únicos**: Número de usuarios diferentes
- **Tiempo promedio**: Tiempo promedio de procesamiento
- **Última actualización**: Timestamp de la última actualización

### Análisis de Usuarios

- **Usuarios más activos**: Top 10 usuarios por número de consultas
- **Contextos por usuario**: Historial completo de consultas de un usuario

### Análisis de Consultas

- **Palabras clave más comunes**: Análisis de términos más utilizados
- **Consultas por hora**: Distribución temporal por hora del día
- **Consultas por día**: Distribución por día de la semana

### Métricas de Rendimiento

- **Tiempo de procesamiento**: Análisis de rendimiento
- **Documentos utilizados**: Qué documentos se consultan más
- **Modelos utilizados**: Distribución de modelos de IA

## 🧪 Pruebas

### Ejecutar Pruebas

```bash
python tests/test_context_storage.py
```

### Pruebas Incluidas

1. **Pruebas básicas**: Almacenamiento, recuperación y estadísticas
2. **Pruebas de rendimiento**: Medición de tiempos de procesamiento
3. **Pruebas de exportación**: Verificación de exportación de datos

## ⚙️ Configuración

### Variables de Entorno

No se requieren variables de entorno adicionales. El sistema utiliza la configuración existente del proyecto.

### Personalización

#### Cambiar Directorio de Almacenamiento

```python
from src.utils.context_storage import ContextStorage

# Crear instancia personalizada
custom_storage = ContextStorage(storage_dir="custom/path")
```

#### Configurar Cache de Estadísticas

```python
# En src/utils/context_storage.py
self._cache_ttl = 600  # 10 minutos en lugar de 5
```

## 🔒 Seguridad y Privacidad

### Datos Almacenados

- **Información del usuario**: ID, username, roles
- **Contenido de consultas**: Prompts y respuestas completas
- **Metadatos**: Timestamps, tiempos de procesamiento
- **Información de Discord**: Guild ID, Channel ID

### Consideraciones de Privacidad

1. **Datos sensibles**: Las consultas pueden contener información personal
2. **Retención**: Los datos se mantienen por 30 días por defecto
3. **Acceso**: Solo administradores del sistema pueden acceder
4. **Exportación**: Los datos se pueden exportar para análisis

### Recomendaciones

- Revisar regularmente los datos almacenados
- Configurar limpieza automática según políticas de retención
- Implementar encriptación si es necesario
- Cumplir con regulaciones de privacidad locales

## 🚀 Optimizaciones

### Cache de Estadísticas

- **TTL**: 5 minutos por defecto
- **Invalidación**: Automática al almacenar nuevos contextos
- **Persistencia**: Estadísticas guardadas en archivo JSON

### Rendimiento

- **Thread-safe**: Operaciones seguras para múltiples hilos
- **Escritura asíncrona**: No bloquea el procesamiento de consultas
- **Límites configurables**: Límites en consultas y exportaciones

### Escalabilidad

- **Formato JSONL**: Fácil de procesar y analizar
- **Separación de datos**: Contextos y estadísticas en archivos separados
- **Exportación incremental**: Posibilidad de exportar por rangos de fechas

## 📈 Análisis Avanzado

### Casos de Uso

1. **Análisis de uso**: Identificar patrones de consulta
2. **Optimización de respuestas**: Mejorar calidad basada en feedback
3. **Análisis de usuarios**: Comportamiento y preferencias
4. **Monitoreo de rendimiento**: Identificar cuellos de botella

### Herramientas de Análisis

- **Scripts personalizados**: Para análisis específicos
- **Exportación a herramientas externas**: Excel, PowerBI, etc.
- **APIs para dashboards**: Integración con sistemas de monitoreo

## 🐛 Troubleshooting

### Problemas Comunes

1. **Error de permisos**: Verificar permisos de escritura en `data/contexts/`
2. **Archivo corrupto**: Eliminar archivo de estadísticas para regenerar
3. **Memoria insuficiente**: Reducir límites de consultas en estadísticas
4. **Rendimiento lento**: Verificar tamaño del archivo de contextos

### Logs

El sistema utiliza el logger principal del proyecto. Buscar mensajes con:
- `context_storage`
- `QueryContext`
- `ContextStorage`

## 📝 Changelog

### v1.0.0
- Implementación inicial del sistema
- Almacenamiento automático de contextos
- Estadísticas básicas
- Scripts de análisis
- Endpoints API
