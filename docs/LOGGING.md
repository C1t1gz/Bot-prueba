# Sistema de Logging con Loguru

Este proyecto utiliza **Loguru** como sistema de logging centralizado para registrar todas las actividades del bot de Discord y el sistema RAG. Incluye integración con el sistema de métricas para monitoreo completo.

## Configuración

El sistema de logging está configurado en `src/utils/logger.py` y se inicializa automáticamente al importar el módulo.

### Características

- **Logs en consola**: Con colores y formato legible
- **Logs en archivos**: Separados por categorías
- **Rotación automática**: Los archivos se rotan cuando alcanzan cierto tamaño
- **Compresión**: Los archivos antiguos se comprimen automáticamente
- **Retención**: Los archivos se eliminan después de un período específico
- **Integración con métricas**: Logs sincronizados con el sistema de métricas

## Archivos de Log

### 1. `logs/app.log`
- **Nivel**: DEBUG
- **Contenido**: Todos los logs de la aplicación
- **Rotación**: 10 MB
- **Retención**: 30 días

### 2. `logs/errors.log`
- **Nivel**: ERROR
- **Contenido**: Solo errores y excepciones
- **Rotación**: 5 MB
- **Retención**: 60 días

### 3. `logs/discord.log`
- **Nivel**: INFO
- **Contenido**: Interacciones y eventos de Discord
- **Rotación**: 5 MB
- **Retención**: 30 días
- **Filtro**: Solo logs relacionados con Discord

### 4. `logs/chat.log`
- **Nivel**: INFO
- **Contenido**: Actividad del chat y sistema RAG
- **Rotación**: 5 MB
- **Retención**: 30 días
- **Filtro**: Solo logs relacionados con chat/IA

## Uso

### Importar el logger

```python
from src.utils.logger import logger
```

### Niveles de logging

```python
# Debug - Información detallada para desarrollo
logger.debug("Información de debug")

# Info - Información general
logger.info("Información general")

# Warning - Advertencias
logger.warning("Advertencia")

# Error - Errores
logger.error("Error en la aplicación")

# Success - Éxitos (nivel personalizado)
logger.success("Operación exitosa")
```

### Ejemplos de uso

```python
# Log de inicio de aplicación
logger.info("Iniciando aplicación Discord Bot")

# Log de comandos ejecutados
logger.info(f"Comando ejecutado: {command_name} por usuario {user_id}")

# Log de errores con stack trace
try:
    # código que puede fallar
    pass
except Exception as e:
    logger.error(f"Error procesando comando: {e}", exc_info=True)

# Log de éxito
logger.success("Comando procesado exitosamente")

# Log de métricas del ACK diferido
logger.info(f"Petición {request_id} completada en {total_time:.2f}s")
```

## Formato de Logs

### Consola
```
2024-01-15 10:30:45 | INFO     | main:handle_discord_interactions:45 - Interacción recibida: Tipo 2
```

### Archivos
```
2024-01-15 10:30:45 | INFO     | main:handle_discord_interactions:45 - Interacción recibida: Tipo 2
```

## Integración con Sistema de Métricas

El sistema de logging está integrado con el sistema de métricas para proporcionar monitoreo completo:

### Logs de Métricas

```python
# Registrar métricas de interacciones
metrics_collector.increment_counter("discord_interactions_total", labels={"command": "chat"})

# Registrar tiempo de respuesta
metrics_collector.record_response_time("discord_response_time_ms", start_time, labels={"command": "chat"})

# Registrar errores
metrics_collector.increment_counter("discord_interactions_failed", labels={"command": "chat", "error": str(e)[:50]})
```

### Logs de ACK Diferido

```python
# Log de procesamiento de petición
logger.info(f"Procesando petición {request_id} (intento {request.retry_count + 1})")

# Log de chat procesado
logger.info(f"Chat procesado en {processing_time:.2f}s para usuario {request.user_id}")

# Log de respuesta enviada
logger.info(f"Petición {request_id} completada exitosamente en {total_time:.2f}s")

# Log de reintentos
logger.info(f"Reintentando petición {request_id} en {delay}s (intento {request.retry_count})")
```

## Configuración Avanzada

### Cambiar nivel de logging

Para cambiar el nivel de logging en tiempo de ejecución:

```python
from loguru import logger

# Cambiar nivel de consola
logger.remove()
logger.add(sys.stdout, level="DEBUG")

# Cambiar nivel de archivo
logger.add("logs/app.log", level="INFO")
```

### Agregar nuevos handlers

```python
# Log específico para base de datos
logger.add(
    "logs/database.log",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
    level="INFO",
    filter=lambda record: "database" in record["name"].lower()
)

# Log específico para métricas
logger.add(
    "logs/metrics.log",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
    level="INFO",
    filter=lambda record: "metrics" in record["name"].lower()
)
```

## Monitoreo

### Ver logs en tiempo real

```bash
# Ver logs de la aplicación
tail -f logs/app.log

# Ver solo errores
tail -f logs/errors.log

# Ver logs de Discord
tail -f logs/discord.log

# Ver logs de chat
tail -f logs/chat.log
```

### Análisis de logs

```bash
# Contar errores por día
grep "ERROR" logs/errors.log | cut -d' ' -f1 | sort | uniq -c

# Buscar patrones específicos
grep "chat" logs/chat.log | grep "ERROR"

# Ver comandos más usados
grep "Comando ejecutado" logs/discord.log | cut -d' ' -f8 | sort | uniq -c

# Analizar tiempos de respuesta
grep "completada exitosamente" logs/app.log | grep -o "[0-9]\+\.[0-9]\+s" | sort -n
```

### Monitoreo de ACK Diferido

```bash
# Ver peticiones procesadas
grep "Procesando petición" logs/app.log

# Ver reintentos
grep "Reintentando petición" logs/app.log

# Ver errores de envío
grep "Error enviando respuesta a Discord" logs/app.log

# Ver métricas de rendimiento
grep "completada exitosamente" logs/app.log
```

## Troubleshooting

### Problemas comunes

1. **No se crean los archivos de log**
   - Verificar permisos de escritura en el directorio
   - Asegurar que el directorio `logs/` existe

2. **Logs muy verbosos**
   - Cambiar nivel de logging a INFO o WARNING
   - Usar filtros para logs específicos

3. **Archivos de log muy grandes**
   - Reducir el tamaño de rotación
   - Ajustar la retención de archivos

4. **Logs de ACK diferido muy frecuentes**
   - Ajustar el nivel de logging para workers
   - Usar filtros específicos para métricas

### Limpiar logs antiguos

```bash
# Eliminar logs de más de 30 días
find logs/ -name "*.log" -mtime +30 -delete

# Comprimir logs antiguos
find logs/ -name "*.log" -mtime +7 -exec gzip {} \;
```

## Integración con Heroku/Producción

En entornos de producción, los logs se pueden enviar a servicios externos:

```python
# Ejemplo para Papertrail
logger.add(
    "syslog://logs.papertrailapp.com:12345",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}"
)

# Ejemplo para Datadog
logger.add(
    "udp://localhost:8125",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}"
)
```

## Configuración de Métricas

El sistema de logging está configurado para trabajar en conjunto con el sistema de métricas:

### Variables de Entorno

```bash
# Habilitar métricas
DISCORD_METRICS_ENABLED=true

# Configurar retención de métricas
DISCORD_METRICS_RETENTION_HOURS=24

# Configurar limpieza automática
DISCORD_METRICS_CLEANUP_INTERVAL=60
```

### Endpoints de Monitoreo

```bash
# Estado general del sistema
curl http://localhost:8000/health

# Métricas detalladas
curl http://localhost:8000/metrics

# Métricas en formato Prometheus
curl http://localhost:8000/metrics/prometheus
```
