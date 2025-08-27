"""
Servidor FastAPI principal para el bot de Discord
"""

from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse
import threading
import requests
import os
import time
from dotenv import load_dotenv

# Importar desde la nueva estructura
from src.core.chat import chat, tirar_dados, girar_ruleta, lanzar_moneda, mensaje_ayuda, borrar_memoria_usuario
from src.utils.security import verify_discord_signature
from src.utils.logger import logger
from src.discord.interaction_handler import interaction_handler
from src.utils.metrics import metrics_collector
from src.utils.context_storage import context_storage
from src.utils.persistent_memory import persistent_memory

# Cargar variables de entorno
load_dotenv()

# Importar configuración de Discord
from config.discord_settings import DiscordConfig

# Validar configuración al inicio
if not DiscordConfig.validate_config():
    logger.error("Configuración de Discord inválida. Verificando configuración...")
    DiscordConfig.print_config_summary()
    raise SystemExit("Configuración inválida. Revisa las variables de entorno.")

# Crear aplicación FastAPI
app = FastAPI(
    title="PythonBots - Discord Bot API",
    description="API para el bot de Discord con sistema RAG mejorado y ACK diferido robusto",
    version="1.0.0"
)

@app.post("/discord-interactions")
async def handle_discord_interactions(request: Request):
    """
    Endpoint principal para manejar las interacciones de Discord.
    
    Args:
        request (Request): Solicitud HTTP recibida desde Discord.
        
    Returns:
        Response o dict: Respuesta para Discord según el tipo de interacción.
    """
    # Verificación de firma de Discord
    signature = request.headers.get("X-Signature-Ed25519")
    timestamp = request.headers.get("X-Signature-Timestamp")
    body = await request.body()

    if not (signature and timestamp):
        return Response(content="Faltan cabeceras de firma de Discord", status_code=401)

    if not verify_discord_signature(signature, timestamp, body):
        return Response(content="Firma de Discord inválida", status_code=401)

    # Procesar datos de la interacción
    interaction_data = await request.json()
    interaction_type = interaction_data.get("type")

    logger.info(f"Interacción recibida: Tipo {interaction_type}")

    # Apretón de manos de verificación
    if interaction_type == 1:
        logger.info("Recibido PING de Discord. Enviando PONG de vuelta.")
        return {"type": 1}

    # Lógica normal de comandos
    if interaction_type == 2:
        logger.info("Recibido comando. Procesando...")
        
        # Obtener el nombre del comando
        command_data = interaction_data.get("data", {})
        command_name = command_data.get("name", "")
        
        # Manejar diferentes comandos
        if command_name == "dados":
            content = tirar_dados()
        elif command_name == "ruleta":
            content = girar_ruleta()
        elif command_name == "coinflip":
            content = lanzar_moneda()
        elif command_name == "chat":
            # Obtener el prompt enviado como opción del comando
            prompt = None
            options = command_data.get("options", [])
            if options and isinstance(options, list):
                for opt in options:
                    if opt.get("name") == "prompt":
                        prompt = opt.get("value")
                        break
                        
            if not prompt:
                return {
                    "type": 4,
                    "data": {"content": "Debes enviar un mensaje para el chat. Ejemplo: /chat prompt:Tu pregunta"}
                }
            
            # Usar el nuevo sistema mejorado de ACK diferido
            success = interaction_handler.submit_interaction(interaction_data, prompt)
            
            if success:
                logger.info("Interacción enviada al sistema mejorado de ACK diferido")
                return {"type": 5}  # DEFERRED_CHANNEL_MESSAGE_WITH_SOURCE
            else:
                logger.error("Error enviando interacción al sistema de ACK diferido")
                return {
                    "type": 4,
                    "data": {"content": "❌ Error interno del servidor. Por favor, inténtalo de nuevo."}
                }

        elif command_name == "help":
            content = mensaje_ayuda()
        elif command_name == "forget":
            # Obtener el user_id del usuario que ejecutó el comando
            user_id = str(interaction_data.get("member", {}).get("user", {}).get("id", "unknown"))
            content = borrar_memoria_usuario(user_id)
        else:
            content = "Comando no reconocido. Usa /help para ver los comandos disponibles."
            
        # Responder directamente a Discord con el resultado (para comandos rápidos)
        return {
            "type": 4,  # CHANNEL_MESSAGE_WITH_SOURCE
            "data": {"content": content}
        }

    return Response(content="Tipo de interacción no manejado", status_code=400)

@app.get("/")
async def root():
    """Endpoint raíz para verificar que el servidor está funcionando."""
    return {
        "message": "PythonBots - Discord Bot API",
        "status": "running",
        "version": "1.0.0"
    }

@app.get("/contexts/stats")
async def get_context_statistics():
    """Endpoint para obtener estadísticas de contextos de consultas."""
    try:
        stats = context_storage.get_query_statistics()
        return {
            "success": True,
            "data": stats
        }
    except Exception as e:
        logger.error(f"Error obteniendo estadísticas de contextos: {e}")
        return {
            "success": False,
            "error": str(e)
        }

@app.get("/contexts/user/{user_id}")
async def get_user_contexts(user_id: str, limit: int = 10):
    """Endpoint para obtener contextos de un usuario específico."""
    try:
        contexts = context_storage.get_user_contexts(user_id, limit)
        # Convertir a diccionarios para serialización JSON
        contexts_data = []
        for ctx in contexts:
            ctx_dict = {
                "user_id": ctx.user_id,
                "username": ctx.username,
                "prompt": ctx.prompt,
                "response": ctx.response,
                "timestamp": ctx.timestamp,
                "roles": ctx.roles,
                "documents_used": ctx.documents_used,
                "processing_time": ctx.processing_time,
                "model_used": ctx.model_used,
                "guild_id": ctx.guild_id,
                "channel_id": ctx.channel_id
            }
            contexts_data.append(ctx_dict)
        
        return {
            "success": True,
            "data": contexts_data,
            "count": len(contexts_data)
        }
    except Exception as e:
        logger.error(f"Error obteniendo contextos del usuario {user_id}: {e}")
        return {
            "success": False,
            "error": str(e)
        }

@app.post("/contexts/export")
async def export_contexts():
    """Endpoint para exportar todos los contextos."""
    try:
        output_file = context_storage.export_contexts()
        if output_file:
            return {
                "success": True,
                "file_path": output_file,
                "message": "Contextos exportados exitosamente"
            }
        else:
            return {
                "success": False,
                "error": "Error exportando contextos"
            }
    except Exception as e:
        logger.error(f"Error exportando contextos: {e}")
        return {
            "success": False,
            "error": str(e)
        }

@app.delete("/contexts/cleanup")
async def cleanup_contexts(days: int = 30):
    """Endpoint para limpiar contextos antiguos."""
    try:
        removed_count = context_storage.cleanup_old_contexts(days)
        return {
            "success": True,
            "removed_count": removed_count,
            "message": f"Limpieza completada: {removed_count} contextos eliminados"
        }
    except Exception as e:
        logger.error(f"Error limpiando contextos: {e}")
        return {
            "success": False,
            "error": str(e)
        }

# Endpoints para gestión de memoria persistente

@app.get("/memory/list")
async def list_memories():
    """Endpoint para listar todas las memorias de usuario."""
    try:
        memories = persistent_memory.get_all_memory_info()
        return {
            "success": True,
            "data": memories,
            "count": len(memories)
        }
    except Exception as e:
        logger.error(f"Error listando memorias: {e}")
        return {
            "success": False,
            "error": str(e)
        }

@app.get("/memory/user/{user_id}")
async def get_user_memory_info(user_id: str):
    """Endpoint para obtener información de la memoria de un usuario."""
    try:
        memory_info = persistent_memory.get_user_memory_info(user_id)
        if memory_info:
            return {
                "success": True,
                "data": memory_info
            }
        else:
            return {
                "success": False,
                "error": "Memoria no encontrada"
            }
    except Exception as e:
        logger.error(f"Error obteniendo memoria del usuario {user_id}: {e}")
        return {
            "success": False,
            "error": str(e)
        }

@app.delete("/memory/user/{user_id}")
async def clear_user_memory(user_id: str):
    """Endpoint para borrar la memoria de un usuario."""
    try:
        success = persistent_memory.clear_user_memory(user_id)
        if success:
            return {
                "success": True,
                "message": f"Memoria del usuario {user_id} borrada exitosamente"
            }
        else:
            return {
                "success": False,
                "error": "Error borrando la memoria"
            }
    except Exception as e:
        logger.error(f"Error borrando memoria del usuario {user_id}: {e}")
        return {
            "success": False,
            "error": str(e)
        }

@app.delete("/memory/clear-all")
async def clear_all_memories():
    """Endpoint para borrar todas las memorias."""
    try:
        memories = persistent_memory.get_all_memory_info()
        success_count = 0
        
        for memory in memories:
            if persistent_memory.clear_user_memory(memory['user_id']):
                success_count += 1
        
        return {
            "success": True,
            "cleared_count": success_count,
            "total_count": len(memories),
            "message": f"{success_count}/{len(memories)} memorias borradas exitosamente"
        }
    except Exception as e:
        logger.error(f"Error borrando todas las memorias: {e}")
        return {
            "success": False,
            "error": str(e)
        }

@app.delete("/memory/cleanup")
async def cleanup_memories(days: int = 30):
    """Endpoint para limpiar memorias antiguas."""
    try:
        removed_count = persistent_memory.cleanup_old_memories(days)
        return {
            "success": True,
            "removed_count": removed_count,
            "message": f"Limpieza completada: {removed_count} memorias eliminadas"
        }
    except Exception as e:
        logger.error(f"Error limpiando memorias: {e}")
        return {
            "success": False,
            "error": str(e)
        }

@app.get("/health")
async def health_check():
    """Endpoint de verificación de salud del servidor."""
    health_data = metrics_collector.get_system_health()
    return {
        "status": health_data["status"],
        "uptime": health_data["uptime_formatted"],
        "success_rate": f"{health_data['success_rate_percent']}%",
        "avg_response_time_ms": health_data["average_response_time_ms"],
        "total_interactions": health_data["total_interactions"],
        "failed_interactions": health_data["failed_interactions"],
        "queue_size": health_data["current_queue_size"],
        "timestamp": "2024-01-01T00:00:00Z"
    }

@app.get("/metrics")
async def get_metrics():
    """Endpoint para obtener métricas del sistema."""
    return {
        "system_health": metrics_collector.get_system_health(),
        "queue_status": {
            "size": interaction_handler.get_queue_size(),
            "active_requests": interaction_handler.get_active_requests_count()
        },
        "metrics_summary": metrics_collector.get_all_metrics_summary(300)  # Últimos 5 minutos
    }

@app.get("/metrics/prometheus")
async def get_metrics_prometheus():
    """Endpoint para obtener métricas en formato Prometheus."""
    from fastapi.responses import PlainTextResponse
    return PlainTextResponse(metrics_collector.export_metrics_prometheus())

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
