# Carpeta Legacy

Esta carpeta contiene archivos obsoletos o versiones anteriores del código que ya no se usan en la versión actual del bot.

## Archivos Incluidos

### `simple_rag.py`
Versión anterior del sistema RAG que fue reemplazada por `enhanced_rag.py`.
- **Razón de obsolescencia**: No manejaba correctamente el contexto entre preguntas
- **Reemplazado por**: `enhanced_rag.py` con mejoras en manejo de contexto
- **Estado**: No se usa en el código actual

## Por Qué Se Mantuvo

Los archivos legacy se mantienen por las siguientes razones:
- **Referencia histórica**: Para entender cómo evolucionó el código
- **Rollback**: En caso de que sea necesario volver a una versión anterior
- **Comparación**: Para ver las mejoras implementadas
- **Documentación**: Como ejemplo de la evolución del proyecto

## Nota Importante

**NO usar estos archivos en el código actual**. El bot ahora usa:
- `enhanced_rag.py` para el sistema RAG mejorado
- `timbero.py` actualizado para usar las nuevas funcionalidades

## Estructura del Proyecto Actual

```
PythonBots/
├── main.py              # Servidor FastAPI principal
├── timbero.py           # Funciones del bot (actualizado)
├── enhanced_rag.py      # Sistema RAG mejorado
├── base.txt             # Base de conocimiento
├── requirements.txt     # Dependencias
├── tests/               # Archivos de prueba
└── legacy/              # Archivos obsoletos (esta carpeta)
```
